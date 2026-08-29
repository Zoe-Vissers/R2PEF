"""Path resolution helpers."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import os
import shutil


def abspath(p) -> Path:
    """Expand ~ and resolve to absolute, following symlinks.
    Use for data/jar/output paths."""
    return Path(p).expanduser().resolve()


def abspath_keep_symlink(p, base: Path | None = None) -> Path:
    """Expand ~ and make absolute WITHOUT resolving symlinks.

    Used for the eval interpreter. A venv's ``bin/python`` is a symlink to the
    base interpreter, and Python only picks up the venv's site-packages when it
    is invoked *via that symlink*; resolving it would silently bypass the venv.
    A conda env's ``bin/python`` symlinks to ``python3.x`` inside the same env,
    so resolving it would be harmless there — but not resolving is correct for
    both, so we never resolve.

    Relative paths are anchored at ``base`` (the machine.yaml directory) when
    given, otherwise at the current working directory.
    """
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        pp = (Path(base) if base is not None else Path.cwd()) / pp
    return Path(os.path.normpath(str(pp)))


def run_id() -> str:
    """UTC timestamp suitable for directory names. Sortable, no coordination."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def pipeline_dir(output_root: Path, dataset: str, family: str,
                  pipeline: str, rid: str) -> Path:
    return abspath(output_root) / dataset / family / pipeline / rid


def free_disk_gb(path: Path) -> float:
    p = path
    while not p.exists() and p.parent != p:
        p = p.parent
    return shutil.disk_usage(str(p)).free / (1024 ** 3)


def find_reusable_translation(output_root: Path, dataset: str, family: str,
                              pipeline: str, translation: str) -> Path | None:
    """Search prior pipeline_id directories of this (dataset, family, pipeline)
    for a translation phase whose ACTUAL output files still exist. Returns the
    phase dir to reuse, or None. Newest run wins.

    For rdf2pg_{sdm,gdm,cdm}: requires `instance.ypg` to exist.
    For kg2pg: requires a subdir containing PG-files.
    """
    base = abspath(output_root) / dataset / family / pipeline
    if not base.exists():
        return None
    for run in sorted([p for p in base.iterdir() if p.is_dir()], reverse=True):
        phase = run / translation
        if not phase.exists():
            continue
        if translation == "kg2pg":
            for sd in phase.iterdir():
                if (sd.is_dir()
                        and (sd / "PG_NODES_PROPS_JSON.json").exists()
                        and (sd / "PG_NODES_WD_LABELS.csv").exists()
                        and (sd / "PG_NODES_LITERALS.csv").exists()
                        and (sd / "PG_PREFIX_MAP.csv").exists()
                        and (sd / "PG_RELATIONS.csv").exists()):
                    return phase
        else:  # rdf2pg_*
            if (phase / "instance.ypg").exists():
                return phase
    return None