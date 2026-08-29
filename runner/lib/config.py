"""Load and validate machine.yaml, datasets.yaml, runs.yaml."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml

from .paths import abspath, abspath_keep_symlink


@dataclass
class Dataset:
    name: str
    path: Path
    expected_classes: int
    expected_lines: int


@dataclass
class Machine:
    java_home: Path | None
    java_xmx: str
    rdf2pg_jar: Path
    rdf2pg_lib: Path
    qse_jar: Path
    qse_resources: Path
    kg2pg_jar: Path
    eval_root: Path
    eval_python: Path
    data_root: Path
    output_root: Path
    timeouts: dict[str, float]                   # hours, by step
    memory_caps_gb: dict[str, int]               # by step, 0 = disabled
    min_free_disk_gb: float
    overrides: dict[str, dict[str, dict]]        # dataset -> { timeouts/memory_caps_gb -> {...} }
    xmx_overhead_gb: float                       # headroom added on top of -Xmx for the --as cap
    xmx_per_step: dict[str, str]                  # step -> -Xmx string (e.g. {'qse': '8g'})

    def timeout_seconds(self, step: str, dataset: str) -> float:
        hours = self._lookup(dataset, "timeouts", step,
                              self.timeouts.get(step, 1.0))
        return float(hours) * 3600.0

    def xmx_for(self, step: str, dataset: str) -> str:
        """The -Xmx string for a Java step. Per-dataset override > per-step
        xmx map > global java_xmx."""
        return self._lookup(dataset, "xmx", step,
                            self.xmx_per_step.get(step, self.java_xmx))

    def memory_cap_bytes(self, step: str, dataset: str,
                          xmx_gb: float | None = None) -> int | None:
        """Address-space cap for prlimit --as, in bytes.

        Semantics:
          - For PYTHON steps (xmx_gb=None): 0 or absent -> no cap (None).
          - For JAVA steps: any configured cap below xmx + xmx_overhead_gb is
            raised silently to that floor. Setting 0 with a Java step yields
            the floor (xmx + overhead), not "unlimited" — capping the address
            space below the heap would always crash the JVM, so 0 is treated
            as "use the minimum safe value" rather than "off". To genuinely
            disable a Java cap, omit memory_caps_gb for that step AND ensure
            no per-dataset override sets it.

        CRITICAL: prlimit --as bounds TOTAL virtual memory, which must exceed
        the JVM heap (-Xmx) by enough for metaspace, thread stacks, code cache,
        and JIT."""
        gb = self._lookup(dataset, "memory_caps_gb", step,
                          self.memory_caps_gb.get(step, 0))
        gb = float(gb) if gb else 0.0
        if xmx_gb is not None:
            floor = xmx_gb + self.xmx_overhead_gb
            if gb <= 0 or gb < floor:
                gb = floor
        if gb <= 0:
            return None
        return int(gb * 1024 ** 3)

    def _lookup(self, dataset: str, section: str, key: str, default):
        ov = self.overrides.get(dataset, {})
        return ov.get(section, {}).get(key, default)


@dataclass
class Pipeline:
    name: str
    translation: str | None                # None for prebuilt CPGM (Mode A)
    eval_adapter: str                      # sdm | gdm | cdm | kg2pg | file
    family: str                            # subdir grouping under <dataset>/
    kg2pg_parsimonious: bool = True        # only used for translation==kg2pg
    cpgm_file: Path | None = None          # Mode A only
    source_rdf: Path | None = None         # Mode A only

def _rel_to(base: Path, p) -> Path:
    q = Path(p).expanduser()
    return q.resolve() if q.is_absolute() else (base / q).resolve()

def load_machine(path: Path) -> Machine:
    base = Path(path).expanduser().resolve().parent      # ← NEW
    with open(path) as f:
        m = yaml.safe_load(f)
    jh = m["java"].get("java_home")
    return Machine(
        java_home     = abspath(jh) if jh else None,
        java_xmx      = m["java"]["xmx"],
        rdf2pg_jar    = abspath(m["rdf2pg"]["jar"]),
        rdf2pg_lib    = abspath(m["rdf2pg"]["lib"]),
        qse_jar       = abspath(m["qse"]["jar"]),
        qse_resources = abspath(m["qse"]["resources_path"]),
        kg2pg_jar     = abspath(m["kg2pg"]["jar"]),
        eval_python   = abspath_keep_symlink(m["eval"]["python"]),
        data_root   = _rel_to(base, m["data_root"]),          # was: abspath(...)
        output_root = _rel_to(base, m["output_root"]),        # was: abspath(...)
        eval_root   = _rel_to(base, m["eval"]["root"]),       # was: abspath(...)
        timeouts      = m.get("timeouts", {}) or {},
        memory_caps_gb = m.get("memory_caps_gb", {}) or {},
        min_free_disk_gb = float(m.get("min_free_disk_gb", 0)),
        overrides     = m.get("overrides", {}) or {},
        xmx_overhead_gb = float(m["java"].get("xmx_overhead_gb", 2)),
        xmx_per_step  = m["java"].get("xmx_per_step", {}) or {},
    )


def xmx_to_gb(xmx: str) -> float:
    """Parse a Java -Xmx string ('16g', '512m', '8192k') into GB (float)."""
    s = str(xmx).strip().lower()
    if s.endswith("g"):
        return float(s[:-1])
    if s.endswith("m"):
        return float(s[:-1]) / 1024.0
    if s.endswith("k"):
        return float(s[:-1]) / (1024.0 ** 2)
    # bare number = bytes
    return float(s) / (1024.0 ** 3)


def load_datasets(path: Path, data_root: Path) -> list[Dataset]:
    with open(path) as f:
        d = yaml.safe_load(f)
    out: list[Dataset] = []
    for entry in d["datasets"]:
        out.append(Dataset(
            name             = entry["name"],
            path             = abspath(data_root / entry["path_rel"]),
            expected_classes = int(entry["expected_classes"]),
            expected_lines   = int(entry["expected_lines"]),
        ))
    return out


def load_runs(path: Path) -> dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def parse_pipelines(runs_cfg: dict, base: Path | None = None) -> list[Pipeline]:
    base = Path(base).resolve() if base is not None else Path.cwd()
    out: list[Pipeline] = []
    for p in runs_cfg.get("pipelines", []) or []:
        translation = p["translation"]
        if translation.startswith("rdf2pg_"):
            default_family = "rdf2pg"
        elif translation == "kg2pg":
            default_family = "kg2pg"
        else:
            default_family = p["name"]
        out.append(Pipeline(
            name               = p["name"],
            translation        = translation,
            eval_adapter       = p["eval_adapter"],
            family             = p.get("family", default_family),
            kg2pg_parsimonious = bool(p.get("kg2pg_parsimonious", True)),
        ))
    for p in runs_cfg.get("prebuilt_pipelines", []) or []:
        out.append(Pipeline(
            name         = p["name"],
            translation  = None,
            eval_adapter = "file",
            family       = p.get("family", "prebuilt"),
            cpgm_file    = _rel_to(base, p["cpgm_file"]),    
            source_rdf   = _rel_to(base, p["source_rdf"]), 
        ))
    return out


def plan_pipelines(runs_cfg: dict, datasets: list[Dataset],
                   pipelines: list[Pipeline]) -> list[tuple[Dataset | None, Pipeline]]:
    """Return ordered list of (dataset_or_None, pipeline) to execute.
    Prebuilt pipelines pair with dataset=None and run FIRST (they're usually
    small smoke tests, useful to surface problems before the full sweep)."""
    only_ds = set(runs_cfg.get("only_datasets") or [])
    only_p  = set(runs_cfg.get("only_pipelines") or [])
    skip    = set(runs_cfg.get("skip") or [])

    plan: list[tuple[Dataset | None, Pipeline]] = []

    # Prebuilt first.
    for p in pipelines:
        if p.translation is not None:
            continue
        if only_p and p.name not in only_p:
            continue
        plan.append((None, p))

    # Then the dataset x pipeline cross-product.
    for ds in datasets:
        if only_ds and ds.name not in only_ds:
            continue
        for p in pipelines:
            if p.translation is None:
                continue
            if only_p and p.name not in only_p:
                continue
            if f"{ds.name}:{p.name}" in skip:
                continue
            plan.append((ds, p))
    return plan