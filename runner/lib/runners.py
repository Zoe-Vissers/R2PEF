"""Runners for each tool. Each function:
  - generates its config file from templates/ into phase_dir
  - invokes the subprocess with stdout+stderr -> phase_dir/log.txt
  - applies JAVA_HOME, timeout, and memory cap
  - returns list of artifact filenames (relative to phase_dir)
  - raises RuntimeError on failure
"""
from __future__ import annotations
import os
import shutil
import subprocess
from pathlib import Path

import yaml

from .config import Machine, Dataset


TEMPLATES = Path(__file__).parent.parent / "templates"


# ---------- environment & execution ---------------------------------------

def _env(m: Machine) -> dict:
    """Subprocess env with JAVA_HOME applied if configured."""
    env = dict(os.environ)
    if m.java_home:
        env["JAVA_HOME"] = str(m.java_home)
        env["PATH"] = f"{m.java_home}/bin:" + env.get("PATH", "/usr/bin:/bin")
    return env


def _java_bin(m: Machine) -> str:
    """Absolute path to the java binary we should use."""
    if m.java_home:
        return str(m.java_home / "bin" / "java")
    return "java"


def _wrap_prlimit(cmd: list[str], mem_bytes: int | None) -> list[str]:
    """Prepend `prlimit --as=<bytes>` if a memory cap is configured AND prlimit
    is available. Otherwise return cmd unchanged."""
    if not mem_bytes:
        return cmd
    if shutil.which("prlimit") is None:
        return cmd
    return ["prlimit", f"--as={mem_bytes}", "--"] + cmd


def run_subprocess(cmd: list[str], log_path: Path, cwd: Path,
                    timeout_sec: float, env: dict,
                    mem_bytes: int | None, append: bool = False) -> int:
    """Execute cmd, stream output to log_path. Returns exit code.
    Raises subprocess.TimeoutExpired on timeout.
    append=True preserves any existing log content (e.g. preflight output)."""
    wrapped = _wrap_prlimit(cmd, mem_bytes)
    with open(log_path, "a" if append else "w") as log:
        log.write(f"$ cd {cwd}\n")
        if mem_bytes:
            log.write(f"# memory cap: {mem_bytes / 1024**3:.1f} GB\n")
        if env.get("JAVA_HOME"):
            log.write(f"# JAVA_HOME={env['JAVA_HOME']}\n")
        log.write(f"$ {' '.join(wrapped)}\n\n")
        log.flush()
        proc = subprocess.run(
            wrapped, cwd=str(cwd), stdout=log, stderr=subprocess.STDOUT,
            timeout=timeout_sec, env=env, check=False,
        )
        return proc.returncode


def _check(rc: int, log_path: Path) -> None:
    if rc != 0:
        # Distinguish probable OOM (137=SIGKILL, 139=SIGSEGV, ENOMEM exits)
        suffix = " (likely OOM/killed)" if rc in (137, 139) else ""
        raise RuntimeError(f"exit {rc}{suffix}; see {log_path}")


def _load_template(name: str) -> str:
    return (TEMPLATES / name).read_text()


# ---------- rdf2pg SDM / GDM ----------------------------------------------

def run_rdf2pg_simple(mode: str, ds: Dataset, m: Machine,
                       phase_dir: Path) -> list[str]:
    assert mode in ("sdm", "gdm")
    phase_dir.mkdir(parents=True, exist_ok=True)
    log = phase_dir / "log.txt"

    from .config import xmx_to_gb
    step = f"rdf2pg_{mode}"
    xmx = m.xmx_for(step, ds.name)
    cmd = [_java_bin(m), f"-Xmx{xmx}", "-jar", str(m.rdf2pg_jar),
           f"-{mode}", str(ds.path)]
    rc = run_subprocess(
        cmd, log, cwd=phase_dir,
        timeout_sec=m.timeout_seconds(step, ds.name),
        env=_env(m),
        mem_bytes=m.memory_cap_bytes(step, ds.name, xmx_gb=xmx_to_gb(xmx)),
    )
    _check(rc, log)

    produced = phase_dir / "instance.ypg"
    if not produced.exists():
        raise RuntimeError(f"expected {produced} but it was not produced")
    return ["instance.ypg"]


# ---------- rdf2pg CDM (two java calls) -----------------------------------

def run_rdf2pg_cdm(ds: Dataset, m: Machine, phase_dir: Path) -> list[str]:
    """Step 1: RDFSProcessor -d <dataset> -> produces schema.ttl (and
       instance.nt as a by-product) in CWD.
    Step 2: rdf2pg -cdm <ORIGINAL dataset> <schema.ttl> -> instance.ypg
       (and schema.ypg). """
    phase_dir.mkdir(parents=True, exist_ok=True)
    log1 = phase_dir / "log.txt"
    log2 = phase_dir / "log.step2.txt"
    from .config import xmx_to_gb
    env = _env(m)
    xmx = m.xmx_for("rdf2pg_cdm", ds.name)
    mem = m.memory_cap_bytes("rdf2pg_cdm", ds.name, xmx_gb=xmx_to_gb(xmx))
    tmo = m.timeout_seconds("rdf2pg_cdm", ds.name)

    # Step 1: schema extraction.
    classpath = f"{m.rdf2pg_lib}/rdfs-processor.jar:{m.rdf2pg_lib}/*"
    cmd1 = [_java_bin(m), f"-Xmx{xmx}", "-cp", classpath, "RDFSProcessor",
            "-d", str(ds.path)]
    rc = run_subprocess(cmd1, log1, phase_dir, tmo, env, mem)
    _check(rc, log1)

    if not (phase_dir / "schema.ttl").exists():
        raise RuntimeError("RDFSProcessor did not produce schema.ttl")

    # Step 2: CDM translation. Pass the ORIGINAL dataset as the instance input,
    cmd2 = [_java_bin(m), f"-Xmx{xmx}", "-jar", str(m.rdf2pg_jar), "-cdm",
            str(ds.path), str(phase_dir / "schema.ttl")]
    rc = run_subprocess(cmd2, log2, phase_dir, tmo, env, mem)
    _check(rc, log2)

    if not (phase_dir / "instance.ypg").exists():
        raise RuntimeError("rdf2pg -cdm did not produce instance.ypg")

    # Keep everything rdf2pg produced. Report only what's actually there.
    artifacts = ["instance.ypg", "schema.ttl"]
    if (phase_dir / "schema.ypg").exists():
        artifacts.append("schema.ypg")
    if (phase_dir / "instance.nt").exists():
        artifacts.append("instance.nt")
    return artifacts


# ---------- QSE -----------------------------------------------------------

def run_qse(ds: Dataset, m: Machine, phase_dir: Path) -> list[str]:
    phase_dir.mkdir(parents=True, exist_ok=True)
    cfg_path = phase_dir / "qse.properties"
    log      = phase_dir / "log.txt"

    output_dir = str(phase_dir) + "/"
    cfg_path.write_text(_load_template("qse.properties.tmpl").format(
        dataset_name     = ds.name,
        expected_classes = ds.expected_classes,
        expected_lines   = ds.expected_lines,
        dataset_path     = ds.path,
        resources_path   = m.qse_resources,
        config_dir       = output_dir,
        output_dir       = output_dir,
        default_dir      = output_dir,
        validation_dir   = output_dir,
    ))

    from .config import xmx_to_gb
    xmx = m.xmx_for("qse", ds.name)
    xmx_gb = xmx_to_gb(xmx)
    cmd = [_java_bin(m), f"-Xmx{xmx}", "-jar", str(m.qse_jar),
           str(cfg_path)]
    rc = run_subprocess(
        cmd, log, cwd=phase_dir,
        timeout_sec=m.timeout_seconds("qse", ds.name),
        env=_env(m),
        mem_bytes=m.memory_cap_bytes("qse", ds.name, xmx_gb=xmx_gb),
    )
    _check(rc, log)

    shacl = list(phase_dir.rglob(f"{ds.name}_QSE_FULL_SHACL.ttl"))
    if not shacl:
        raise RuntimeError(f"QSE did not produce {ds.name}_QSE_FULL_SHACL.ttl")
    canonical = phase_dir / f"{ds.name}_QSE_FULL_SHACL.ttl"
    if shacl[0] != canonical:
        shutil.copy2(shacl[0], canonical)
    return ["qse.properties", canonical.name]


# ---------- KG2PG ---------------------------------------------------------

def run_kg2pg(ds: Dataset, m: Machine, phase_dir: Path,
              qse_phase_dir: Path, parsimonious: bool) -> list[str]:
    phase_dir.mkdir(parents=True, exist_ok=True)
    cfg_path = phase_dir / "kg2pg.properties"
    log      = phase_dir / "log.txt"

    shapes = qse_phase_dir / f"{ds.name}_QSE_FULL_SHACL.ttl"
    if not shapes.exists():
        raise RuntimeError(f"QSE shapes file missing: {shapes}")

    output_dir = str(phase_dir) + "/"
    cfg_path.write_text(_load_template("kg2pg.properties.tmpl").format(
        dataset_name     = ds.name,
        shapes_path      = shapes,
        dataset_path     = ds.path,
        output_dir       = output_dir,
        expected_classes = ds.expected_classes,
        expected_lines   = ds.expected_lines,
        parsi            = "true" if parsimonious else "false",
    ))

    from .config import xmx_to_gb
    xmx = m.xmx_for("kg2pg", ds.name)
    cmd = [_java_bin(m), f"-Xmx{xmx}", "-jar", str(m.kg2pg_jar), str(cfg_path)]
    rc = run_subprocess(
        cmd, log, cwd=phase_dir,
        timeout_sec=m.timeout_seconds("kg2pg", ds.name),
        env=_env(m),
        mem_bytes=m.memory_cap_bytes("kg2pg", ds.name, xmx_gb=xmx_to_gb(xmx)),
    )
    _check(rc, log)

    subdirs = [p for p in phase_dir.iterdir() if p.is_dir()]
    if not subdirs:
        raise RuntimeError("KG2PG produced no output subdirectory")
    return ["kg2pg.properties"] + [d.name for d in subdirs]


# ---------- Eval pipeline -------------------------------------------------

def _cpgm_block(adapter: str, **kwargs) -> str:
    """Return the cpgm adapter block, indented by 2 spaces so it nests under
    the top-level `cpgm:` key. The block in cpgm_blocks.yaml is stored at
    column 0 (yaml.safe_load strips block-scalar indentation), so indentation 
    is added here in code — the single source of truth for nesting."""
    blocks = yaml.safe_load(_load_template("cpgm_blocks.yaml"))
    if adapter not in blocks:
        raise ValueError(f"unknown cpgm adapter: {adapter}")
    body = blocks[adapter].format(**kwargs).rstrip("\n")
    indented = "\n".join(
        ("  " + line) if line.strip() else line
        for line in body.split("\n")
    )
    return indented


def run_eval(eval_adapter: str, source_rdf: Path, run_name: str,
              cpgm_args: dict, m: Machine, phase_dir: Path) -> list[str]:
    """Run the eval pipeline once. cpgm_args is the dict of substitutions
    needed by the selected cpgm block (e.g. {'instance': ...} for sdm)."""
    phase_dir.mkdir(parents=True, exist_ok=True)
    cfg_path = phase_dir / "pipeline_config.yaml"
    log      = phase_dir / "log.txt"

    cpgm_block = _cpgm_block(eval_adapter, **cpgm_args)
    cfg_text = _load_template("eval_pipeline.yaml.tmpl").format(
        dataset_path=source_rdf,
        output_dir=phase_dir,
        run_name=run_name,
        cpgm_block=cpgm_block,
    )
    cfg_path.write_text(cfg_text)

    if not Path(m.eval_python).exists():
        raise RuntimeError(
            f"eval.python does not exist: {m.eval_python}. Point it at the "
            f"interpreter of your Python environment as an ABSOLUTE path "
            f"(conda: <env>/bin/python, venv: <venv>/bin/python) — not a bare "
            f"`python`: the driver spawns subprocesses without an activated shell."
        )

    env = _env(m)
    env["PYTHONPATH"] = str(m.eval_root)

    # Preflight: prove which interpreter runs and that its dependencies are
    # importable, BEFORE launching the real pipeline.
    preflight = subprocess.run(
        [str(m.eval_python), "-c",
         "import sys; print('interpreter:', sys.executable); "
         "print('prefix:', sys.prefix); "
         "import rdflib; print('rdflib:', rdflib.__file__)"],
        cwd=str(m.eval_root), env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    with open(log, "w") as f:
        f.write("=== eval preflight ===\n")
        f.write(f"configured eval.python = {m.eval_python}\n")
        f.write(preflight.stdout)
        f.write(f"\npreflight exit = {preflight.returncode}\n\n")
    if preflight.returncode != 0:
        raise RuntimeError(
            f"eval interpreter cannot import its dependencies. The python at "
            f"{m.eval_python} ran, but a required module (e.g. rdflib) was not "
            f"found on ITS path. Either eval.python does not point at the "
            f"interpreter of the environment you prepared, or that environment "
            f"is missing the dependencies (see environment.yml / requirements.txt "
            f"in the repository root). Get the right path with:\n"
            f"    conda activate <env> && which python      # conda\n"
            f"    source <venv>/bin/activate && which python  # venv\n"
            f"See the preflight output in {log}."
        )

    cmd = [str(m.eval_python), "-m", "r2pef.pipeline", str(cfg_path)]

    rc = run_subprocess(
        cmd, log, cwd=m.eval_root,
        timeout_sec=m.timeout_seconds("eval", run_name),
        env=env,
        mem_bytes=m.memory_cap_bytes("eval", run_name),
        append=True,
    )
    _check(rc, log)
    return ["pipeline_config.yaml"]