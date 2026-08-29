"""
adapter_rdf2pg_sdm.py — CPGM adapter for the rdf2pg_sdm algorithm.

Input file:
  instance.ypg — local names only, no prefix info, numeric node ids.
"""

import sys
from pathlib import Path

from .cpgm_core import (
    make_cpgm, make_handle, make_handle_synthetic, make_handle_literal,
    make_label_entry, make_node, make_property_entry, make_relation,
    node_canonical_id, parse_ypg_lines, validate_cpgm,
)

ALGORITHM = "rdf2pg_sdm"


def stage2_nodes(node_records: list, synthetic_keys: frozenset = frozenset()) -> list:
    nodes = []
    for rec in node_records:
        # sdm: all nodes are synthetic (numeric id, no source IRI)
        node_ref = make_handle_synthetic()
        labels = [
            make_label_entry(lbl, make_handle(lbl, "local_only", lbl))
            for lbl in rec["labels"]
        ]
        properties = []
        for k, v in rec["props"]:
            key_ref = make_handle_synthetic() if k in synthetic_keys else make_handle(k, "local_only", k)
            properties.append(make_property_entry(
                k, key_ref, make_handle_literal(v),  # already unquoted by YPG parser
            ))
        nodes.append(make_node(
            id=f"sdm_{rec['node_id']}",
            node_ref=node_ref,
            labels=labels,
            properties=properties,
        ))
    return nodes


def stage3_edges(edge_records: list, node_registry: dict) -> list:
    relations = []
    for rec in edge_records:
        start_ref, end_ref = rec["start"], rec["end"]
        if start_ref not in node_registry:
            raise KeyError(f"Edge start not in registry: {start_ref!r}")
        if end_ref not in node_registry:
            raise KeyError(f"Edge end not in registry: {end_ref!r}")
        start = node_canonical_id(node_registry[start_ref])
        end   = node_canonical_id(node_registry[end_ref])
        lbl_ref = make_handle(rec["label"], "local_only", rec["label"])
        relations.append(make_relation(
            start=start,
            end=end,
            labels=[make_label_entry(rec["label"], lbl_ref)],
            properties=[],
        ))
    return relations


def run(ypg_path: Path, synthetic_labels: frozenset = frozenset(), synthetic_keys: frozenset = frozenset()) -> dict:
    if not ypg_path.exists() or ypg_path.stat().st_size == 0:
        import warnings
        warnings.warn(f"Empty or missing file: {ypg_path}", stacklevel=2)
        return make_cpgm(ALGORITHM, [], [], [])
    lines = ypg_path.read_text(encoding="utf-8").splitlines()
    node_records, edge_records = parse_ypg_lines(lines)
    nodes = stage2_nodes(node_records, synthetic_keys)
    # Registry keyed by raw YPG node_id — edges use the raw integer for wiring;
    # the node's CPGM id uses the sdm_ prefix.
    node_registry = {rec["node_id"]: node for rec, node in zip(node_records, nodes)}
    relations = stage3_edges(edge_records, node_registry)
    return make_cpgm(ALGORITHM, [], nodes, relations)


def main():
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <instance.ypg> <output.json>")
        sys.exit(1)
    cpgm = run(Path(sys.argv[1]))
    validate_cpgm(cpgm)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(cpgm, f, indent=2, ensure_ascii=False)
    print(f"Written: {sys.argv[2]}")


if __name__ == "__main__":
    main()