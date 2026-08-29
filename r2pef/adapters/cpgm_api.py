"""
cpgm_api.py — Public API for the CPGM adapter suite.

Provides two ways to obtain a validated CPGM dict from any of the four
adapters, suitable for direct consumption by downstream scripts:

  1. run_adapter(algorithm, ...)  — run an adapter in-process and return the
                                    CPGM dict directly (no file I/O needed).

  2. load_cpgm(path)              — load a previously written CPGM JSON file
                                    and return the validated dict.

Both always validate against cpgm.schema.json before returning.

Typical usage
-------------
From a downstream script that wants to consume KG2PG output directly:

    from .cpgm_api import run_adapter, load_cpgm
    from pathlib import Path

    # Option A: run the adapter in-process
    cpgm = run_adapter("kg2pg", input_dir=Path("exp_watdiv/pg_plain/"))

    # Option B: load a file written by a previous adapter run
    cpgm = load_cpgm(Path("out_kg2pg.json"))

    # Either way, cpgm is a validated dict ready to iterate:
    for node in cpgm["nodes"]:
        print(node["identity_iri"], node["labels"])

    for relation in cpgm["relations"]:
        print(relation["start"], "->", relation["end"])

Supported algorithm names (case-insensitive):
    "kg2pg"
    "rdf2pg_sdm"   or  "sdm"
    "rdf2pg_gdm"   or  "gdm"
    "rdf2pg_cdm"   or  "cdm"
"""

import json
from pathlib import Path

from .cpgm_core import validate_cpgm

# ---------------------------------------------------------------------------
# Algorithm name aliases
# ---------------------------------------------------------------------------

# Known algorithm-generated labels for each algorithm.
# Passed as defaults to run_adapter(); pipeline.py can override or extend.
# Known synthetic labels and keys per algorithm — exposed here for reference
# and for use in the test suite. Callers supply these explicitly to run_adapter();
# no defaults are injected automatically.
#
# synthetic_labels: label strings the algorithm generates with no RDF class counterpart.
# synthetic_keys:   property key strings with no RDF predicate counterpart.
#
# kg2pg labels:  Node, LitNode, IRI, Prefixes, KG2PG
# kg2pg keys:    object_value, object_type, type  (column names from PG_NODES_LITERALS.csv)
# gdm labels:   Resource, Literal, BlankNode, DatatypeProperty, ObjectProperty
# gdm keys:     iri, value, type, id  (algorithm-internal property names)
# sdm / cdm:    no synthetic labels or keys

_ALIASES = {
    "kg2pg":       "kg2pg",
    "rdf2pg_sdm":  "rdf2pg_sdm",
    "sdm":         "rdf2pg_sdm",
    "rdf2pg_gdm":  "rdf2pg_gdm",
    "gdm":         "rdf2pg_gdm",
    "rdf2pg_cdm":  "rdf2pg_cdm",
    "cdm":         "rdf2pg_cdm",
}


def _resolve_algorithm(name: str) -> str:
    key = name.lower().strip()
    if key not in _ALIASES:
        raise ValueError(
            f"Unknown algorithm {name!r}. "
            f"Valid names: {sorted(set(_ALIASES.values()))}"
        )
    return _ALIASES[key]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run_adapter(algorithm: str, synthetic_labels: frozenset | None = None, synthetic_keys: frozenset | None = None, **kwargs) -> dict:
    """
    Run the named adapter in-process and return a validated CPGM dict.

    Parameters
    ----------
    algorithm : str
        One of: "kg2pg",
                "rdf2pg_sdm" / "sdm",
                "rdf2pg_gdm" / "gdm",
                "rdf2pg_cdm" / "cdm"  (case-insensitive).

    Parameters
    ----------
    synthetic_labels : frozenset | None
        Label strings the algorithm generates internally (no RDF counterpart).
        These get label_ref.synthetic=True. If None, defaults from
        _SYNTHETIC_LABELS are used. Pass frozenset() to disable.

    synthetic_keys : frozenset | None
        Property key strings the algorithm generates internally (no RDF
        predicate counterpart). These get key_ref.synthetic=True. If None,
        defaults from _SYNTHETIC_KEYS are used. Pass frozenset() to disable.

    Keyword arguments (algorithm-specific)
    ---------------------------------------
    kg2pg:
        input_dir : Path | str   — directory containing the five KG2PG CSV/JSON files.

    rdf2pg_sdm:
        instance  : Path | str   — path to instance.ypg

    rdf2pg_gdm:
        instance  : Path | str   — path to instance.ypg

    rdf2pg_cdm:
        instance  : Path | str   — path to instance.ypg

    Returns
    -------
    dict
        Validated CPGM document. Raises jsonschema.ValidationError if the
        adapter produces invalid output (indicates an adapter bug).

    Raises
    ------
    ValueError   — unknown algorithm name or missing required argument.
    KeyError     — edge endpoint references a node not in the registry.
    FileNotFoundError — a required input file does not exist.
    """
    canonical = _resolve_algorithm(algorithm)
    # Callers are responsible for supplying synthetic_labels and synthetic_keys.
    # Defaults to empty sets — no synthetic classification without explicit opt-in.
    labels = synthetic_labels if synthetic_labels is not None else frozenset()
    keys   = synthetic_keys   if synthetic_keys   is not None else frozenset()

    if canonical == "kg2pg":
        from .adapter_kg2pg import run
        input_dir = kwargs.get("input_dir")
        if input_dir is None:
            raise ValueError("KG2PG requires keyword argument: input_dir")
        return run(Path(input_dir), synthetic_labels=labels, synthetic_keys=keys)

    if canonical == "rdf2pg_sdm":
        from .adapter_rdf2pg_sdm import run
        instance = kwargs.get("instance")
        if instance is None:
            raise ValueError("rdf2pg_sdm requires keyword argument: instance")
        return run(Path(instance), synthetic_labels=labels, synthetic_keys=keys)

    if canonical == "rdf2pg_gdm":
        from .adapter_rdf2pg_gdm import run
        instance = kwargs.get("instance")
        if instance is None:
            raise ValueError("rdf2pg_gdm requires keyword argument: instance")
        return run(Path(instance), synthetic_labels=labels, synthetic_keys=keys)

    if canonical == "rdf2pg_cdm":
        from .adapter_rdf2pg_cdm import run
        instance = kwargs.get("instance")
        if instance is None:
            raise ValueError("rdf2pg_cdm requires keyword argument: instance")
        return run(Path(instance), synthetic_labels=labels, synthetic_keys=keys)


def load_cpgm(path) -> dict:
    """
    Load and validate a CPGM JSON file written by a previous adapter run.

    Parameters
    ----------
    path : Path | str
        Path to the CPGM JSON file.

    Returns
    -------
    dict
        Validated CPGM document.

    Raises
    ------
    FileNotFoundError        — file does not exist.
    json.JSONDecodeError     — file is not valid JSON.
    jsonschema.ValidationError — file does not conform to cpgm.schema.json.
    """
    path = Path(path)
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    validate_cpgm(doc)
    return doc


def save_cpgm(doc: dict, path) -> None:
    """
    Validate and write a CPGM dict to a JSON file.

    Useful when a downstream script mutates a CPGM and wants to persist it
    while ensuring it stays schema-conformant.

    Parameters
    ----------
    doc  : dict       — CPGM document.
    path : Path | str — destination file path.
    """
    validate_cpgm(doc)
    path = Path(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)