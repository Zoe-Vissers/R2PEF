"""Append-only results log. One row per completed phase.

Rows are tied together by pipeline_id. Translation phases run once
per pipeline; eval phases run `eval_repeats` times (rep_index distinguishes them).
"""
from __future__ import annotations
import csv
from pathlib import Path
from dataclasses import dataclass, asdict

LEDGER_FIELDS = [
    "pipeline_id", "dataset", "family", "pipeline", "phase", "rep_index",
    "status",                                # OK | FAILED | TIMEOUT | SKIPPED
    "started_utc", "finished_utc", "duration_sec",
    "exit_code", "phase_dir", "config_path", "log_path",
    "artifacts",
    "error",
]


@dataclass
class LedgerRow:
    pipeline_id: str
    dataset: str
    family: str
    pipeline: str
    phase: str
    rep_index: int
    status: str
    started_utc: str
    finished_utc: str
    duration_sec: float
    exit_code: int | None
    phase_dir: str
    config_path: str
    log_path: str
    artifacts: str
    error: str


def append(log_path: Path, row: LedgerRow) -> None:
    new_file = not log_path.exists()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_FIELDS)
        if new_file:
            w.writeheader()
        w.writerow(asdict(row))
        f.flush()


def read_all(log_path: Path) -> list[dict]:
    if not log_path.exists():
        return []
    with open(log_path) as f:
        return list(csv.DictReader(f))


def pipeline_completed(log_path: Path, dataset: str, pipeline: str,
                        eval_repeats: int) -> bool:
    """True iff `eval_repeats` OK eval rows exist for this (dataset, pipeline).
    The eval phase is the last; if all reps are OK, prior phases must have
    succeeded too."""
    eval_ok = sum(1 for row in read_all(log_path)
                  if row["dataset"] == dataset
                  and row["pipeline"] == pipeline
                  and row["phase"] == "eval"
                  and row["status"] == "OK")
    return eval_ok >= eval_repeats