#!/usr/bin/env python3
"""Orchestrate rdf2pg / QSE / KG2PG / eval-pipeline experiments.

A pipeline runs once over a dataset:
    optional QSE pre-step (for kg2pg only)
    -> translation phase (rdf2pg_sdm/gdm/cdm or kg2pg)
       (reused from a prior pipeline_id if its artifacts still exist)
    -> evaluation phase x eval_repeats

Each phase is timed and ledgered separately in results.csv so translation
time and evaluation time are distinguishable.

Eval rep deduplication: only eval_rep0 keeps the full eval framework output;
subsequent reps keep only report.json + summary.md (everything else is
identical across reps and is deleted to save disk).

Usage:
    python3 run_evaluation.py              # run plan; skip already-OK pipelines
    python3 run_evaluation.py --dry-run    # show plan, don't execute
    python3 run_evaluation.py --force      # redo every pipeline in the plan

To start completely fresh, delete the output directory:
    rm -rf <output_root>
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from lib.config  import (
    load_machine, load_datasets, load_runs, parse_pipelines, plan_pipelines,
    Machine, Dataset, Pipeline,
)
from lib.ledger  import LedgerRow, LEDGER_FIELDS, append, pipeline_completed
from lib.paths   import (pipeline_dir, run_id, free_disk_gb,
                          find_reusable_translation)
from lib.runners import (
    run_rdf2pg_simple, run_rdf2pg_cdm, run_qse, run_kg2pg, run_eval,
)

# Files the eval framework writes per rep. Only these are kept on rep 1+;
# everything else in the rep dir is identical to rep 0 and deleted.
EVAL_KEEP_PER_REP = {"report.json", "summary.md",
                      "pipeline_config.yaml", "log.txt", "error.txt"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ----------------------------------------------------------------------------

def execute_phase(fn, *,
                  log_path: Path, pid: str, dataset: str, family: str,
                  pipeline: str, phase: str, rep_index: int,
                  phase_dir: Path,
                  min_free_gb: float, output_root: Path) -> bool:
    """Run one phase, ledger the outcome. Returns True on OK."""
    if min_free_gb > 0:
        free = free_disk_gb(output_root)
        if free < min_free_gb:
            append(log_path, LedgerRow(
                pipeline_id=pid, dataset=dataset, family=family,
                pipeline=pipeline, phase=phase, rep_index=rep_index,
                status="SKIPPED",
                started_utc=utc_now(), finished_utc=utc_now(),
                duration_sec=0.0, exit_code=None,
                phase_dir=str(phase_dir), config_path="", log_path="",
                artifacts="",
                error=f"insufficient free disk: {free:.1f}GB < {min_free_gb}GB",
            ))
            print(f"      {phase} SKIPPED: only {free:.1f}GB free")
            return False

    started = utc_now()
    t0 = datetime.now(timezone.utc)
    try:
        artifacts = fn()
        dur = (datetime.now(timezone.utc) - t0).total_seconds()
        append(log_path, LedgerRow(
            pipeline_id=pid, dataset=dataset, family=family, pipeline=pipeline,
            phase=phase, rep_index=rep_index, status="OK",
            started_utc=started, finished_utc=utc_now(),
            duration_sec=round(dur, 3), exit_code=0,
            phase_dir=str(phase_dir),
            config_path=str(next(phase_dir.glob("*.properties"), "")
                          or next(phase_dir.glob("*.yaml"), "")),
            log_path=str(phase_dir / "log.txt"),
            artifacts=";".join(artifacts), error="",
        ))
        print(f"      {phase} OK ({dur:.1f}s)")
        return True

    except subprocess.TimeoutExpired as e:
        dur = (datetime.now(timezone.utc) - t0).total_seconds()
        append(log_path, LedgerRow(
            pipeline_id=pid, dataset=dataset, family=family, pipeline=pipeline,
            phase=phase, rep_index=rep_index, status="TIMEOUT",
            started_utc=started, finished_utc=utc_now(),
            duration_sec=round(dur, 3), exit_code=None,
            phase_dir=str(phase_dir), config_path="",
            log_path=str(phase_dir / "log.txt"),
            artifacts="", error=f"timeout after {e.timeout}s",
        ))
        print(f"      {phase} TIMEOUT after {e.timeout}s")
        return False

    except Exception as e:
        dur = (datetime.now(timezone.utc) - t0).total_seconds()
        (phase_dir / "error.txt").write_text(traceback.format_exc())
        append(log_path, LedgerRow(
            pipeline_id=pid, dataset=dataset, family=family, pipeline=pipeline,
            phase=phase, rep_index=rep_index, status="FAILED",
            started_utc=started, finished_utc=utc_now(),
            duration_sec=round(dur, 3), exit_code=None,
            phase_dir=str(phase_dir), config_path="",
            log_path=str(phase_dir / "log.txt"),
            artifacts="", error=str(e)[:500],
        ))
        print(f"      {phase} FAILED: {str(e)[:120]}")
        return False


def dedupe_eval_rep(rep_dir: Path) -> None:
    """Delete files/dirs that duplicate what eval_rep0 already produced.
    Keeps only the rep-specific outputs (report.json, summary.md) and the
    orchestrator's own files. Idempotent and tolerant of unexpected layouts."""
    if not rep_dir.exists():
        return
    # The eval framework nests its outputs under <rep_dir>/<run_name>/.
    # We dedupe inside that nested dir.
    for run_subdir in rep_dir.iterdir():
        if not run_subdir.is_dir():
            continue
        for entry in run_subdir.iterdir():
            if entry.name in EVAL_KEEP_PER_REP:
                continue
            if entry.is_dir():
                shutil.rmtree(entry, ignore_errors=True)
            else:
                try:
                    entry.unlink()
                except OSError:
                    pass


# ----------------------------------------------------------------------------

def run_pipeline(ds: Dataset | None, p: Pipeline, m: Machine,
                 eval_repeats: int, log_path: Path) -> None:
    """Execute one pipeline. Prebuilt pipelines (translation=None) skip
    straight to eval. Non-prebuilt: optional qse + translation + N eval reps,
    with translation reused from a prior pipeline_id if its artifacts exist."""
    pid = run_id()
    # Directory naming: real datasets use ds.name; prebuilt uses the pipeline
    # name (avoids shell-hostile characters from a synthetic dataset string).
    ds_dir = ds.name if ds is not None else p.name
    pdir = pipeline_dir(m.output_root, ds_dir, p.family, p.name, pid)
    pdir.mkdir(parents=True, exist_ok=True)
    label = ds.name if ds else p.name
    print(f"  pipeline {p.name} on {label} -> {pdir}")

    common = dict(log_path=log_path, pid=pid, dataset=(ds.name if ds else ""),
                  family=p.family, pipeline=p.name,
                  min_free_gb=m.min_free_disk_gb, output_root=m.output_root)

    # --- Prebuilt CPGM (Mode A): only eval --------------------------------
    if p.translation is None:
        for rep in range(eval_repeats):
            eph = pdir / f"eval_rep{rep}"
            ok = execute_phase(
                lambda r=rep: run_eval(
                    "file", p.source_rdf,
                    f"{p.name}-rep{r}",
                    {"cpgm_file": p.cpgm_file},
                    m, eph),
                phase="eval", rep_index=rep, phase_dir=eph, **common)
            if not ok:
                return
            if rep > 0:
                dedupe_eval_rep(eph)
        return

    # --- Mode B: optional qse + translation + eval -----------------------
    # Attempt to reuse a prior translation. If found, point eval at it and
    # skip running both qse and translation again.
    reuse_dir = find_reusable_translation(
        m.output_root, ds.name, p.family, p.name, p.translation)

    if reuse_dir is not None:
        trans_dir = reuse_dir
        print(f"      reusing translation: {trans_dir}")
    else:
        # QSE pre-step (kg2pg only)
        qse_dir = None
        if p.translation == "kg2pg":
            qse_dir = pdir / "qse"
            if not execute_phase(lambda: run_qse(ds, m, qse_dir),
                                  phase="qse", rep_index=0, phase_dir=qse_dir,
                                  **common):
                return

        # Translation
        trans_dir = pdir / p.translation
        if p.translation == "rdf2pg_sdm":
            fn = lambda: run_rdf2pg_simple("sdm", ds, m, trans_dir)
        elif p.translation == "rdf2pg_gdm":
            fn = lambda: run_rdf2pg_simple("gdm", ds, m, trans_dir)
        elif p.translation == "rdf2pg_cdm":
            fn = lambda: run_rdf2pg_cdm(ds, m, trans_dir)
        elif p.translation == "kg2pg":
            fn = lambda: run_kg2pg(ds, m, trans_dir, qse_dir,
                                   p.kg2pg_parsimonious)
        else:
            raise ValueError(f"unknown translation: {p.translation}")

        if not execute_phase(fn, phase=p.translation, rep_index=0,
                              phase_dir=trans_dir, **common):
            return

    # Eval reps
    for rep in range(eval_repeats):
        eph = pdir / f"eval_rep{rep}"

        if p.eval_adapter in ("sdm", "gdm", "cdm"):
            instance = trans_dir / "instance.ypg"
            if not instance.exists():
                append(log_path, LedgerRow(
                    pipeline_id=pid, dataset=ds.name, family=p.family,
                    pipeline=p.name, phase="eval", rep_index=rep,
                    status="FAILED",
                    started_utc=utc_now(), finished_utc=utc_now(),
                    duration_sec=0.0, exit_code=None,
                    phase_dir=str(eph), config_path="", log_path="",
                    artifacts="",
                    error=f"instance.ypg missing: {instance}",
                ))
                return
            cpgm_args = {"instance": instance}
        elif p.eval_adapter == "kg2pg":
            usable = [sd for sd in trans_dir.iterdir()
                      if sd.is_dir()
                      and (sd / "PG_NODES_PROPS_JSON.json").exists()
                      and (sd / "PG_RELATIONS.csv").exists()]
            if not usable:
                append(log_path, LedgerRow(
                    pipeline_id=pid, dataset=ds.name, family=p.family,
                    pipeline=p.name, phase="eval", rep_index=rep,
                    status="FAILED",
                    started_utc=utc_now(), finished_utc=utc_now(),
                    duration_sec=0.0, exit_code=None,
                    phase_dir=str(eph), config_path="", log_path="",
                    artifacts="",
                    error=f"no usable kg2pg output in {trans_dir}",
                ))
                return
            cpgm_args = {"input_dir": usable[0]}
        else:
            raise ValueError(f"unsupported eval_adapter: {p.eval_adapter}")

        if not execute_phase(
                lambda r=rep, ca=cpgm_args: run_eval(
                    p.eval_adapter, ds.path,
                    f"{ds.name}-{p.name}-rep{r}", ca, m, eph),
                phase="eval", rep_index=rep, phase_dir=eph, **common):
            return
        if rep > 0:
            dedupe_eval_rep(eph)


# ----------------------------------------------------------------------------

def preflight_environment(log_path: Path) -> None:
    if sys.version_info < (3, 10):
        sys.exit(f"Requires Python 3.10+. You have "
                 f"{sys.version_info.major}.{sys.version_info.minor}.")
    if shutil.which("prlimit") is None:
        print("WARNING: `prlimit` not found. Memory caps will NOT be enforced.",
              file=sys.stderr)
    if log_path.exists():
        with open(log_path) as f:
            header = f.readline().rstrip("\n").split(",")
        if set(header) != set(LEDGER_FIELDS):
            sys.exit(
                f"results.csv schema does not match current LedgerRow.\n"
                f"  file: {log_path}\n"
                f"  missing: {sorted(set(LEDGER_FIELDS) - set(header))}\n"
                f"  extra:   {sorted(set(header) - set(LEDGER_FIELDS))}\n"
                f"Move or rename the old file, then re-run."
            )


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--machine",  default="machine.yaml")
    ap.add_argument("--datasets", default="datasets.yaml")
    ap.add_argument("--runs",     default="runs.yaml")
    ap.add_argument("--dry-run",  action="store_true",
                    help="print the plan, don't execute")
    ap.add_argument("--force",    action="store_true",
                    help="ignore results.csv and redo every pipeline")
    args = ap.parse_args()

    here = Path(__file__).parent.resolve()
    m         = load_machine(here / args.machine)
    datasets  = load_datasets(here / args.datasets, m.data_root)
    runs_cfg  = load_runs(here / args.runs)
    pipelines = parse_pipelines(runs_cfg, base=here)
    plan      = plan_pipelines(runs_cfg, datasets, pipelines)
    eval_n    = int(runs_cfg.get("eval_repeats", 1))

    log_path = m.output_root / "results.csv"
    preflight_environment(log_path)

    print(f"Plan: {len(plan)} pipeline(s), eval_repeats={eval_n}.")
    print(f"Results log: {log_path}")

    if args.dry_run:
        for ds, p in plan:
            label = ds.name if ds else "(prebuilt)"
            print(f"  {label:24s} {p.family:10s} {p.name}")
        return 0

    for idx, (ds, p) in enumerate(plan, 1):
        ds_name_for_check = ds.name if ds else ""
        label = ds.name if ds else p.name
        if not args.force and pipeline_completed(log_path, ds_name_for_check,
                                                  p.name, eval_n):
            print(f"[{idx}/{len(plan)}] {label} :: {p.name}  SKIP (complete)")
            continue
        print(f"[{idx}/{len(plan)}] {label} :: {p.name}")
        try:
            run_pipeline(ds, p, m, eval_n, log_path)
        except Exception as e:
            print(f"  *** orchestrator error: {e}")
            traceback.print_exc()

    print(f"Done. Results log: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())