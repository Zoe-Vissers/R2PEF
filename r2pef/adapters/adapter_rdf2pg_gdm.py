"""
adapter_rdf2pg_gdm.py — CPGM adapter for the rdf2pg_gdm algorithm.

Input file:
  instance.ypg — Resource nodes (full IRIs), Literal nodes (value+type),
                 DatatypeProperty and ObjectProperty edges.
"""

import sys
from pathlib import Path

from .cpgm_core import (
    handle_from_iri_string, handle_from_value_string, make_cpgm, make_handle,
    make_handle_literal, make_handle_synthetic, make_label_entry, make_node,
    make_property_entry, make_relation, node_canonical_id, parse_ypg_lines,
    strip_quotes, validate_cpgm,
)

ALGORITHM = "rdf2pg_gdm"


def _label(raw: str, synthetic_labels: frozenset) -> dict:
    """Build a LabelEntry, consulting synthetic_labels for algorithm-invented ones.
    Non-synthetic labels are classified via handle_from_iri_string (gdm has no prefix
    index, so namespace_plus_local (npl) labels would remain unresolved).
    """
    if raw in synthetic_labels:
        return make_label_entry(raw, make_handle_synthetic())
    ref = handle_from_iri_string(raw, {})
    return make_label_entry(ref["resolved"], ref)


def _key_ref(synthetic_keys: frozenset, k: str) -> dict:
    """Return a synthetic handle if k is an algorithm-internal key, else inspect via
    handle_from_iri_string. gdm has no prefix index so npl labels remain unresolved."""
    if k in synthetic_keys:
        return make_handle_synthetic()
    return handle_from_iri_string(k, {})


def stage2_nodes(node_records: list, synthetic_labels: frozenset = frozenset(), synthetic_keys: frozenset = frozenset()) -> list:
    nodes = []
    for rec in node_records:
        labels_raw = rec["labels"]
        # Use dict only for single-value lookups (iri, value, type are unique in gdm).
        # Iterate the original list for property building to preserve duplicate keys.
        props_lookup = dict(rec["props"])
        props_list   = rec["props"]

        if "Resource" in labels_raw:
            raw_iri = props_lookup.get("iri", "") or None
            if raw_iri:
                node_ref = handle_from_iri_string(raw_iri, {})  # gdm has no prefix index
                identity_iri = node_ref["resolved"]
            else:
                node_ref = make_handle_synthetic()
                identity_iri = None
            labels = [_label("Resource", synthetic_labels)]
            properties = []
            for k, v in props_list:
                if k == "iri":
                    continue   # iri is identity, not a property
                properties.append(make_property_entry(
                    k, _key_ref(synthetic_keys, k), make_handle_literal(v),
                ))
            nodes.append(make_node(
                id=identity_iri if identity_iri else f"gdm_{rec['node_id']}",
                node_ref=node_ref,
                labels=labels,
                properties=properties,
            ))

        elif "Literal" in labels_raw:
            # node_ref is populated from the value property — the literal value
            # is what this node reifies. Read it from the bag like any other property.
            value = props_lookup.get("value", "")  # already unquoted by YPG parser
            node_ref = make_handle(value, "literal", value)
            labels = [_label("Literal", synthetic_labels)]
            properties = []
            for k, v in props_list:
                # value: plain literal; type: datatype IRI — classify via hvs
                val_handle = make_handle_literal(v) if k == "value" \
                             else handle_from_value_string(v)
                properties.append(make_property_entry(
                    k, _key_ref(synthetic_keys, k), val_handle,
                ))
            nodes.append(make_node(
                id=f"lit_gdm_{rec['node_id']}",
                node_ref=node_ref,
                labels=labels,
                properties=properties,
            ))

        elif "BlankNode" in labels_raw:
            # Blank node: id property holds the blank node identifier e.g. "_:b1500105655"
            raw_bnode_id = props_lookup.get("id", rec["node_id"])  # already unquoted
            node_ref = make_handle(raw_bnode_id, "local_only", raw_bnode_id)
            labels   = [_label("BlankNode", synthetic_labels)]
            properties = []
            for k, v in props_list:
                if k == "id":
                    continue   # id is the node's identity, excluded from properties
                properties.append(make_property_entry(
                    k, _key_ref(synthetic_keys, k), make_handle_literal(v),
                ))
            nodes.append(make_node(
                id=raw_bnode_id,
                node_ref=node_ref,
                labels=labels,
                properties=properties,
            ))

        else:
            lbl_entries = [_label(lbl, synthetic_labels) for lbl in labels_raw]
            properties  = []
            for k, v in props_list:
                properties.append(make_property_entry(
                    k, _key_ref(synthetic_keys, k), make_handle_literal(v),
                ))
            nodes.append(make_node(
                id=f"gdm_{rec['node_id']}",
                node_ref=make_handle_synthetic(),
                labels=lbl_entries,
                properties=properties,
            ))

    return nodes


def stage3_edges(edge_records: list, node_registry: dict, synthetic_labels: frozenset = frozenset(), synthetic_keys: frozenset = frozenset()) -> list:
    relations = []
    for rec in edge_records:
        start_ref  = rec["start"]
        end_ref    = rec["end"]
        edge_label = rec["label"]
        props_list = rec["props"]

        if start_ref not in node_registry:
            raise KeyError(f"Edge start not in registry: {start_ref!r}")
        if end_ref not in node_registry:
            raise KeyError(f"Edge end not in registry: {end_ref!r}")

        start = node_canonical_id(node_registry[start_ref])
        end   = node_canonical_id(node_registry[end_ref])

        lbl_entry = _label(edge_label, synthetic_labels)

        # Edge properties: use synthetic_keys to decide key_ref
        edge_properties = [
            make_property_entry(
                k,
                _key_ref(synthetic_keys, k),
                handle_from_value_string(v),
            )
            for k, v in props_list
        ]

        relations.append(make_relation(
            start=start,
            end=end,
            labels=[lbl_entry],
            properties=edge_properties,
        ))
    return relations


def run(ypg_path: Path, synthetic_labels: frozenset = frozenset(), synthetic_keys: frozenset = frozenset()) -> dict:
    if not ypg_path.exists() or ypg_path.stat().st_size == 0:
        import warnings
        warnings.warn(f"Empty or missing file: {ypg_path}", stacklevel=2)
        return make_cpgm(ALGORITHM, [], [], [])
    lines = ypg_path.read_text(encoding="utf-8").splitlines()
    node_records, edge_records = parse_ypg_lines(lines)

    nodes        = stage2_nodes(node_records, synthetic_labels, synthetic_keys)
    # Registry keyed by YPG node_id — edges reference nodes by this integer.
    # node_canonical_id() resolves to the CPGM node id after lookup.
    node_registry = {rec["node_id"]: node for rec, node in zip(node_records, nodes)}
    relations    = stage3_edges(edge_records, node_registry, synthetic_labels, synthetic_keys)

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