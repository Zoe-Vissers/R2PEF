"""
adapter_rdf2pg_cdm.py — CPGM adapter for the rdf2pg_cdm algorithm.

Input file:
  instance.ypg — node and edge declarations using prefixed names (nss1_, nss2_, ...).
                 Nodes carry either an iri property (named resource) or an id property
                 (blank node). No prefix mappings are available; all prefixed names
                 remain unresolved in the CPGM output.
"""

import sys
from pathlib import Path

from .cpgm_core import (
    build_prefix_index, handle_from_iri_string, make_cpgm, make_handle,
    make_handle_literal, make_handle_synthetic, make_label_entry, make_node,
    make_prefix_mapping, make_property_entry, make_relation, node_canonical_id,
    parse_ypg_lines, strip_quotes, validate_cpgm,
)

ALGORITHM = "rdf2pg_cdm"


def stage2_nodes(node_records: list, prefix_index: dict, synthetic_keys: frozenset = frozenset()) -> list:
    nodes = []
    for rec in node_records:
        # Use dict only for the single iri lookup; iterate list to preserve duplicates
        props_lookup = dict(rec["props"])
        raw_iri      = props_lookup.get("iri", "") or None  # already unquoted by YPG parser

        # iri takes precedence over id if both are present; id is then also
        # excluded from the property bag (same rule as iri).
        if raw_iri:
            node_ref = handle_from_iri_string(raw_iri, prefix_index)
            node_id  = node_ref["resolved"]
        else:
            # No iri property — check for id property (blank node: "_:b...")
            raw_id = props_lookup.get("id", "") or None  # already unquoted by YPG parser
            if raw_id:
                node_ref = make_handle(raw_id, "local_only", raw_id)
                node_id  = raw_id
            else:
                node_ref = make_handle_synthetic()
                node_id  = rec["node_id"]

        labels = []
        for lbl in rec["labels"]:
            ref = handle_from_iri_string(lbl, prefix_index)
            labels.append(make_label_entry(ref["resolved"], ref))

        properties = []
        for k, v in rec["props"]:
            if k in ("iri", "id"):
                continue   # identity fields, not properties
            if k in synthetic_keys:
                key_ref = make_handle_synthetic()
                key = k
            else:
                key_ref = handle_from_iri_string(k, prefix_index)
                key = key_ref["resolved"]
            properties.append(make_property_entry(
                key, key_ref, make_handle_literal(v),  # already unquoted by YPG parser
            ))

        nodes.append(make_node(
            id=node_id,
            node_ref=node_ref,
            labels=labels,
            properties=properties,
        ))
    return nodes


def stage3_edges(edge_records: list, prefix_index: dict, node_registry: dict) -> list:
    relations = []
    for rec in edge_records:
        start_ref  = rec["start"]
        end_ref    = rec["end"]
        edge_label = rec["label"]

        if start_ref not in node_registry:
            raise KeyError(f"Edge start not in registry: {start_ref!r}")
        if end_ref not in node_registry:
            raise KeyError(f"Edge end not in registry: {end_ref!r}")

        start    = node_canonical_id(node_registry[start_ref])
        end      = node_canonical_id(node_registry[end_ref])
        lbl_ref  = handle_from_iri_string(edge_label, prefix_index)
        lbl_entry = make_label_entry(lbl_ref["resolved"], lbl_ref)

        relations.append(make_relation(
            start=start,
            end=end,
            labels=[lbl_entry],
            properties=[],
        ))
    return relations


def run(instance_path: Path, synthetic_labels: frozenset = frozenset(), synthetic_keys: frozenset = frozenset()) -> dict:
    if not instance_path.exists() or instance_path.stat().st_size == 0:
        import warnings
        warnings.warn(f"Empty or missing file: {instance_path}", stacklevel=2)
        return make_cpgm(ALGORITHM, [], [], [])
    lines = instance_path.read_text(encoding="utf-8").splitlines()
    node_records, edge_records = parse_ypg_lines(lines)

    # cdm provides no prefix mappings — all prefixed names remain unresolved.
    prefixes     = []
    prefix_index = build_prefix_index(prefixes)
    nodes         = stage2_nodes(node_records, prefix_index, synthetic_keys)
    # Registry keyed by YPG node_id — same pattern as gdm.
    node_registry = {rec["node_id"]: node for rec, node in zip(node_records, nodes)}
    relations     = stage3_edges(edge_records, prefix_index, node_registry)

    return make_cpgm(ALGORITHM, prefixes, nodes, relations)


def main():
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <instance.ypg> <output.json>")
        sys.exit(1)
    instance_path = Path(sys.argv[1])
    output_path   = sys.argv[2]
    cpgm = run(instance_path)
    validate_cpgm(cpgm)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cpgm, f, indent=2, ensure_ascii=False)
    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()