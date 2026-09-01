"""
adapter_kg2pg.py — CPGM adapter for the KG2PG algorithm.

Input files (all in input_dir):
  PG_PREFIX_MAP.csv       — NAMESPACE,PREFIX rows
  PG_NODES_WD_LABELS.csv  — iri:ID|:LABEL
  PG_NODES_LITERALS.csv   — id:ID|object_value|object_type|type|:LABEL
  PG_RELATIONS.csv        — :START_ID|property|:END_ID|:TYPE
  PG_NODES_PROPS_JSON.json (or PG_NODES_PROPS.json as fallback)
"""

import csv
import json
import sys
from pathlib import Path

from .cpgm_core import (
    build_node_registry, build_prefix_index, handle_from_iri_string,
    handle_from_value_string, make_cpgm, make_handle, make_handle_literal,
    make_handle_synthetic, make_label_entry, make_node, make_prefix_mapping,
    make_property_entry, make_relation, node_canonical_id, strip_quotes,
    validate_cpgm,
)

ALGORITHM = "kg2pg"

_WD_HEADERS     = {"iri:ID", ":ID", "iri"}
_LIT_HEADERS    = {"id:ID", ":ID", "id"}
_REL_HEADERS    = {":START_ID", "START_ID"}
_PREFIX_HEADERS = {"NAMESPACE", "namespace"}
_PROPS_FILENAMES = ["PG_NODES_PROPS_JSON.json", "PG_NODES_PROPS.json"]


# ---------------------------------------------------------------------------
# Stage 1: Prefix Normalization
# ---------------------------------------------------------------------------

def stage1_prefixes(input_dir: Path) -> list:
    prefixes = []
    path = input_dir / "PG_PREFIX_MAP.csv"
    if not path.exists():
        return prefixes
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) < 2:
                continue
            namespace, prefix = row[0].strip(), row[1].strip()
            if not namespace or not prefix or namespace in _PREFIX_HEADERS:
                continue
            prefixes.append(make_prefix_mapping(prefix, namespace))
    return prefixes


# ---------------------------------------------------------------------------
# Stage 2: Node Registry
# ---------------------------------------------------------------------------

def _label_entry(raw: str, prefix_index: dict, synthetic_labels: frozenset) -> dict:
    """
    Build a LabelEntry for a single label string.
    Synthetic labels (algorithm-invented, no RDF class counterpart) get a null handle.
    All others are classified and optionally expanded via the prefix index.
    """
    if raw in synthetic_labels:
        return make_label_entry(raw, make_handle_synthetic())
    ref = handle_from_iri_string(raw, prefix_index)
    return make_label_entry(ref["resolved"], ref)


def stage2_nodes(input_dir: Path, prefix_index: dict, synthetic_labels: frozenset, synthetic_keys: frozenset = frozenset()) -> list:
    nodes = []

    # --- IRI-identified nodes (PG_NODES_WD_LABELS.csv) ---
    wd_path = input_dir / "PG_NODES_WD_LABELS.csv"
    if wd_path.exists():
        with open(wd_path, newline="", encoding="utf-8") as f:
            for row in csv.reader(f, delimiter="|"):
                if not row or not row[0].strip():
                    continue
                iri = row[0].strip()
                if iri in _WD_HEADERS:
                    continue
                label_col = row[1].strip() if len(row) > 1 else ""
                labels = []
                for raw_lbl in label_col.split(";"):
                    s = raw_lbl.strip()
                    if s:
                        labels.append(_label_entry(s, prefix_index, synthetic_labels))
                # Inspect the IRI string — always classify via handle_from_iri_string
                node_ref = handle_from_iri_string(iri, prefix_index)
                nodes.append(make_node(
                    id=node_ref["resolved"],
                    node_ref=node_ref,
                    labels=labels,
                    properties=[],      # populated in Stage 4
                ))

    # --- Value-bearing nodes (PG_NODES_LITERALS.csv) ---
    lit_path = input_dir / "PG_NODES_LITERALS.csv"
    if lit_path.exists():
        with open(lit_path, newline="", encoding="utf-8") as f:
            for row in csv.reader(f, delimiter="|"):
                if not row or not row[0].strip():
                    continue
                raw_id = row[0].strip()
                if raw_id in _LIT_HEADERS:
                    continue
                object_value = row[1] if len(row) > 1 else ""  # preserve significant whitespace
                object_type  = row[2].strip() if len(row) > 2 else ""
                pg_type      = row[3].strip() if len(row) > 3 else ""
                label_col = row[4].strip() if len(row) > 4 else ""

                labels = []
                for raw_lbl in label_col.split(";"):
                    s = raw_lbl.strip()
                    if s:
                        labels.append(_label_entry(s, prefix_index, synthetic_labels))

                # node_ref: value-bearing node — form=literal, resolved=object_value
                node_ref = make_handle(object_value, "literal", object_value)

                # Properties: columns as synthetic-keyed entries
                # key_ref is synthetic when the key name is in synthetic_keys
                def _key_ref(k):
                    return make_handle_synthetic() if k in synthetic_keys else make_handle(k, "local_only", k)
                properties = [
                    make_property_entry(
                        "object_value",
                        _key_ref("object_value"),
                        handle_from_value_string(object_value),
                    ),
                ]
                if object_type:
                    properties.append(make_property_entry(
                        "object_type",
                        _key_ref("object_type"),
                        handle_from_value_string(object_type),
                    ))
                if pg_type:
                    properties.append(make_property_entry(
                        "type",
                        _key_ref("type"),
                        make_handle_literal(pg_type),
                    ))
                nodes.append(make_node(
                    id=f"lit_kg2pg_{raw_id}",
                    node_ref=node_ref,
                    labels=labels,
                    properties=properties,
                ))

    return nodes


# ---------------------------------------------------------------------------
# Stage 3: Edge Registry
# ---------------------------------------------------------------------------

def stage3_edges(input_dir: Path, prefix_index: dict, node_registry: dict) -> list:
    relations = []
    path = input_dir / "PG_RELATIONS.csv"
    if not path.exists():
        return relations

    def resolve_endpoint(ref: str) -> str:
        ref = ref.strip()
        if ref in node_registry:
            return node_canonical_id(node_registry[ref])
        syn = f"lit_kg2pg_{ref}"
        if syn in node_registry:
            return syn
        raise KeyError(f"Edge endpoint not found: {ref!r}")

    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="|"):
            if not row or not row[0].strip():
                continue
            start_ref = row[0].strip()
            if start_ref in _REL_HEADERS:
                continue
            edge_type = row[3].strip() if len(row) > 3 else ""
            end_ref   = row[2].strip() if len(row) > 2 else ""

            start = resolve_endpoint(start_ref)
            end   = resolve_endpoint(end_ref)

            lbl_ref = handle_from_iri_string(edge_type, prefix_index)
            lbl_entry = make_label_entry(lbl_ref["resolved"], lbl_ref)

            relations.append(make_relation(
                start=start,
                end=end,
                labels=[lbl_entry],
                properties=[],
            ))
    return relations


# ---------------------------------------------------------------------------
# Stage 4: Property Normalization (PG_NODES_PROPS.json)
# ---------------------------------------------------------------------------

def _find_props_file(input_dir: Path):
    for name in _PROPS_FILENAMES:
        p = input_dir / name
        if p.exists():
            return p
    return None


def stage4_properties(input_dir: Path, prefix_index: dict, node_registry: dict, synthetic_keys: frozenset = frozenset()):
    path = _find_props_file(input_dir)
    if path is None:
        return
    raw = path.read_text(encoding="utf-8").strip()
    # kg2pg occasionally produces a leading comma after the opening bracket,
    # e.g. "[,{...}]" instead of "[{...}]". Detect and strip it before parsing.
    if raw.startswith("[,"):
        import warnings
        warnings.warn(
            f"Malformed JSON in {path.name}: leading comma after '[' — fixing automatically.",
            stacklevel=2,
        )
        raw = "[" + raw[2:]
    records = json.loads(raw)
    for record in records:
        iri = record.get("iri", "").strip()
        if iri not in node_registry:
            continue
        node = node_registry[iri]
        is_prefixes_node = (iri == "http://relweb.cs.aau.dk/kg2pg/prefixes")
        for raw_key, raw_val in record.get("properties", {}).items():
            if raw_key in synthetic_keys:
                key_ref = make_handle_synthetic()
                key = raw_key
            elif is_prefixes_node and raw_key in prefix_index:
                # Special case: Prefixes node keys are prefix aliases resolvable
                # directly via the prefix index even without an underscore separator.
                namespace_iri = prefix_index[raw_key]
                key_ref = make_handle(raw_key, "full_iri", namespace_iri)
                key = namespace_iri
            else:
                key_ref = handle_from_iri_string(raw_key, prefix_index)
                key = key_ref["resolved"]
            lexical = strip_quotes(str(raw_val))
            node["properties"].append(
                make_property_entry(key, key_ref, make_handle_literal(lexical))
            )


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run(input_dir: Path, synthetic_labels: frozenset = frozenset(), synthetic_keys: frozenset = frozenset()) -> dict:
    if not input_dir.exists() or not input_dir.is_dir():
        import warnings
        warnings.warn(f"Empty or missing input directory: {input_dir}", stacklevel=2)
        return make_cpgm(ALGORITHM, [], [], [])
    prefixes = stage1_prefixes(input_dir)
    prefix_index = build_prefix_index(prefixes)

    nodes = stage2_nodes(input_dir, prefix_index, synthetic_labels, synthetic_keys)
    node_registry = build_node_registry(nodes)

    relations = stage3_edges(input_dir, prefix_index, node_registry)
    stage4_properties(input_dir, prefix_index, node_registry, synthetic_keys)

    return make_cpgm(ALGORITHM, prefixes, nodes, relations)


def main():
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <input_dir> <output.json>")
        sys.exit(1)
    input_dir = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    cpgm = run(input_dir)
    validate_cpgm(cpgm)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cpgm, f, indent=2, ensure_ascii=False)
    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
