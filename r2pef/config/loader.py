"""YAML loader for pipeline configuration.

Relative paths inside the config file are resolved against the *directory of
the config file itself*, not the process working directory. This is the
behaviour practitioners expect: the YAML names files relative to where it
lives. Absolute paths are passed through untouched.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Union

import yaml

from .schemas import PipelineConfig


# Dotted paths inside the parsed YAML that should be resolved against the
# config file's parent directory when they are relative.
_RELATIVE_PATH_KEYS = (
    ("source_rdf", "path"),
    ("cpgm", "file"),
    ("cpgm", "kg2pg", "instance"),
    ("cpgm", "kg2pg", "input_dir"),
    ("cpgm", "rdf2pg_sdm", "instance"),
    ("cpgm", "rdf2pg_sdm", "input_dir"),
    ("cpgm", "rdf2pg_gdm", "instance"),
    ("cpgm", "rdf2pg_gdm", "input_dir"),
    ("cpgm", "rdf2pg_cdm", "instance"),
    ("cpgm", "rdf2pg_cdm", "input_dir"),
    ("reporter", "output_dir"),
)


def _resolve(raw: Any, base: Path, dotted: tuple) -> None:
    """Walk ``raw`` along ``dotted`` and rewrite the leaf path relative to ``base``."""
    cur = raw
    for key in dotted[:-1]:
        if not isinstance(cur, dict) or key not in cur or cur[key] is None:
            return
        cur = cur[key]
    leaf = dotted[-1]
    if not isinstance(cur, dict) or leaf not in cur or cur[leaf] is None:
        return
    p = Path(cur[leaf])
    if not p.is_absolute():
        cur[leaf] = str((base / p).resolve())


def load_config(path: Union[str, Path]) -> PipelineConfig:
    """Load + validate ``pipeline_config.yaml``."""
    path = Path(path).resolve()
    base = path.parent
    with path.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    if not isinstance(raw, dict):
        raise ValueError(f"Config root must be a mapping, got {type(raw).__name__}.")

    for dotted in _RELATIVE_PATH_KEYS:
        _resolve(raw, base, dotted)

    return PipelineConfig.model_validate(raw)