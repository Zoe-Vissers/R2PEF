"""
cpgm_core.py — Shared utilities for all CPGM adapters.

Provides:
  - ResourceHandle constructors
  - CPGM element constructors (Node, Relation, LabelEntry, PropertyEntry)
  - Prefix resolution and string classification
  - YPG file parser (used by rdf2pg_sdm, rdf2pg_gdm, rdf2pg_cdm)
  - JSON Schema validator
  - Unicode normalisation helper for downstream scoring
"""

import re
import json
import jsonschema
import unicodedata
from pathlib import Path
from urllib.parse import unquote

# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------

_SCHEMA_PATH = Path(__file__).parent.parent / "cpgm.schema.json"

def load_schema() -> dict:
    with open(_SCHEMA_PATH) as f:
        return json.load(f)

def validate_cpgm(doc: dict) -> None:
    """Raise jsonschema.ValidationError if doc does not conform to cpgm.schema.json."""
    jsonschema.Draft202012Validator(load_schema()).validate(doc)

# ---------------------------------------------------------------------------
# ResourceHandle constructors
#
# A ResourceHandle captures how one identifier-bearing element was expressed
# in the algorithm's output:
#   raw      — exact string from the file, before any resolution
#   form     — ExpressionForm: full_iri | namespace_plus_local | local_only | literal
#   resolved — best available expanded form (full IRI if prefix mapped, else raw)
#   synthetic — True when the element has no source RDF counterpart;
#               raw / form / resolved are all null in that case
# ---------------------------------------------------------------------------

def make_handle_synthetic() -> dict:
    """No source-side identifier available — all provenance fields are null."""
    return {"raw": None, "form": None, "resolved": None, "synthetic": True}

def make_handle(raw: str, form: str, resolved: str) -> dict:
    """Source-derived handle with explicit form and resolved value."""
    return {"raw": raw, "form": form, "resolved": resolved, "synthetic": False}

def make_handle_literal(lexical: str) -> dict:
    """Convenience: a plain literal value. raw == resolved == lexical."""
    return make_handle(lexical, "literal", lexical)

def make_handle_full_iri(iri: str) -> dict:
    """Convenience: a full IRI. raw == resolved == iri."""
    return make_handle(iri, "full_iri", iri)

# ---------------------------------------------------------------------------
# CPGM element constructors
# ---------------------------------------------------------------------------

def make_prefix_mapping(prefix: str, namespace: str) -> dict:
    return {"prefix": prefix, "namespace": namespace}

def make_label_entry(label: str, label_ref: dict) -> dict:
    """
    label     — display string (resolved form, or raw string when synthetic).
    label_ref — ResourceHandle carrying provenance.
    """
    return {"label": label, "label_ref": label_ref}

def make_property_entry(key: str, key_ref: dict, value_ref: dict) -> dict:
    """
    key       — resolved canonical key string.
    key_ref   — ResourceHandle for the predicate.
    value_ref — ResourceHandle for the value.
    """
    return {"key": key, "key_ref": key_ref, "value_ref": value_ref}

def make_node(id: str, node_ref: dict, labels: list, properties: list) -> dict:
    """
    id        — file-scoped identifier referenced by Relation.start / .end.
    node_ref  — ResourceHandle recording the node's RDF-level provenance.
    """
    return {"id": id, "node_ref": node_ref, "labels": labels, "properties": properties}

def make_relation(start: str, end: str, labels: list, properties: list) -> dict:
    """Predicate provenance lives on label_ref of each LabelEntry, not here."""
    return {"start": start, "end": end, "labels": labels, "properties": properties}

def make_cpgm(algorithm: str, prefixes: list, nodes: list, relations: list) -> dict:
    return {"algorithm": algorithm, "prefixes": prefixes, "nodes": nodes, "relations": relations}

# ---------------------------------------------------------------------------
# Node id accessor
# ---------------------------------------------------------------------------

def node_canonical_id(node: dict) -> str:
    return node["id"]

def build_node_registry(nodes: list) -> dict:
    """Build {node.id: node} dict. kg2pg uses this since its registry key is the resolved IRI."""
    registry = {}
    for n in nodes:
        if n["id"] in registry:
            raise ValueError(f"Duplicate node id: {n['id']!r}")
        registry[n["id"]] = n
    return registry

# ---------------------------------------------------------------------------
# Prefix resolution
# ---------------------------------------------------------------------------

def build_prefix_index(prefixes: list) -> dict:
    """Build {prefix: namespace} dict for fast lookup during string resolution."""
    return {pm["prefix"]: pm["namespace"] for pm in prefixes}

def resolve_namespaced(raw: str, prefix_index: dict) -> tuple:
    """
    Attempt to expand a prefixed name of the form prefix_local.
    Returns (resolved_iri, prefix_used) on success, (raw, None) if no match.
    Tries longest prefix first to avoid greedy mismatch.
    """
    if "_" not in raw:
        return raw, None
    for prefix in sorted(prefix_index, key=len, reverse=True):
        if raw.startswith(prefix + "_"):
            local = raw[len(prefix) + 1:]
            return prefix_index[prefix] + local, prefix
    return raw, None

# ---------------------------------------------------------------------------
# High-level handle builders
# ---------------------------------------------------------------------------

def handle_from_iri_string(raw: str, prefix_index: dict) -> dict:
    """
    Build a ResourceHandle for an identifier string (node IRI, label, property key).
    Classifies by content and attempts prefix expansion:
      contains "://"  →  full_iri  (no expansion needed)
      contains "_"    →  namespace_plus_local  (expand via prefix_index if possible)
      otherwise       →  local_only
    """
    if "://" in raw:
        return make_handle_full_iri(raw)
    if "_" in raw:
        resolved, _ = resolve_namespaced(raw, prefix_index)
        return make_handle(raw, "namespace_plus_local", resolved)
    return make_handle(raw, "local_only", raw)

def handle_from_value_string(raw: str) -> dict:
    """
    Build a ResourceHandle for a property value.
    Same classification as handle_from_iri_string but never attempts prefix
    expansion — a value containing '_' may simply have an underscore in it.
      contains "://"  →  full_iri
      contains "_"    →  namespace_plus_local  (stored as-is, not expanded)
      otherwise       →  literal
    """
    if "://" in raw:
        return make_handle_full_iri(raw)
    if "_" in raw:
        return make_handle(raw, "namespace_plus_local", raw)
    return make_handle_literal(raw)

# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def strip_quotes(s: str) -> str:
    """Remove exactly one layer of surrounding double-quotes."""
    if s and len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    return s

def normalize_for_comparison(s: str) -> str:
    """
    Normalise a string for matching against source RDF triples.
    Applies percent-decoding then NFC normalisation, so that the same
    Unicode character encoded different ways (e.g. em-dash as \\u2013,
    as %E2%80%93, or as the literal UTF-8 glyph) compares equal.
    Used by downstream scorers, not by the adapter itself.
    """
    try:
        s = unquote(s, errors="strict")
    except Exception:
        pass
    return unicodedata.normalize("NFC", s)

# ---------------------------------------------------------------------------
# YPG parser — used by rdf2pg_sdm, rdf2pg_gdm, rdf2pg_cdm
#
# Format:
#   Node: <node_id>[<label,...>]:{<key>:"<value>",...}
#   Edge: (<start>)-[<label> {<key>:"<value>",...}]->(<end>)
#
# The parser is character-level rather than regex-based because real-world
# YPG files contain values with embedded quotes, braces, commas, and
# newlines that defeat naive regex approaches.
# ---------------------------------------------------------------------------

def _extract_props_block(line: str, opening_brace: int) -> tuple:
    """
    Find the closing '}' that matches the '{' at opening_brace.
    Returns (props_content_string, index_of_closing_brace).
    Tracks brace depth only — no quote-state tracking, because the
    structural key parser handles ambiguous quote boundaries correctly.
    """
    depth = 1
    i = opening_brace + 1
    while i < len(line):
        c = line[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return line[opening_brace + 1 : i], i
        i += 1
    raise ValueError(f"Unmatched '{{' in line: {line!r}")


def _parse_props_chars(props_str: str) -> list:
    """
    Parse a props string into [(key, value), ...].

    Locates key positions using the unambiguous pattern (comma-or-start)(word+)(:),
    then slices the string between consecutive keys to extract each value.
    This is robust to any characters inside values (embedded quotes, braces,
    commas) because value boundaries are inferred from key positions, not
    from value content. Duplicate keys are preserved as separate tuples.
    Outer quotes on values are stripped; inner content is kept verbatim.
    """
    s = props_str.strip()
    if not s:
        return []
    # Require the colon to be followed by optional whitespace then a quote (?=\s*").
    # In valid YPG, every property value is a quoted string, so a real key separator
    # is always key:"value". Colons inside values (verse refs, city labels, subtitles,
    # URLs) are never immediately followed by a quote, so they are safely excluded.
    key_matches = list(re.finditer(r'(?:^|,)\s*(\w+)\s*:(?=\s*")', s))
    if not key_matches:
        return []
    result = []
    for idx, m in enumerate(key_matches):
        key = m.group(1)
        val_start = m.end()
        if idx + 1 < len(key_matches):
            raw_val = s[val_start : key_matches[idx + 1].start()].rstrip(",").strip()
        else:
            raw_val = s[val_start:].strip()
        if len(raw_val) >= 2 and raw_val[0] == '"' and raw_val[-1] == '"':
            raw_val = raw_val[1:-1]
        result.append((key, raw_val))
    return result


def _parse_line_node(line: str) -> dict | None:
    """
    Parse one node line: <id>[<labels>]:{<props>}
    Returns a dict with keys node_id, labels, props — or None if the line
    does not match the expected structure.
    """
    i = 0
    # Read node_id up to '['
    while i < len(line) and line[i] not in ("[", " ", "\t"):
        i += 1
    node_id = line[:i].strip()
    if not node_id:
        return None
    while i < len(line) and line[i] != "[":
        i += 1
    if i >= len(line):
        return None
    i += 1  # skip '['
    label_start = i
    while i < len(line) and line[i] != "]":
        i += 1
    if i >= len(line):
        return None
    labels_str = line[label_start:i]
    i += 1  # skip ']'
    while i < len(line) and line[i] in (" ", "\t", ":"):
        i += 1
    if i >= len(line) or line[i] != "{":
        return None
    try:
        props_str, _ = _extract_props_block(line, i)
    except ValueError:
        return None
    labels = [lbl.strip() for lbl in labels_str.split(",") if lbl.strip()]
    return {"node_id": node_id, "labels": labels, "props": _parse_props_chars(props_str)}


def _parse_line_edge(line: str) -> dict | None:
    """
    Parse one edge line: (<start>)-[<label> {<props>}]->(<end>)
    Returns a dict with keys start, label, props, end — or None if no match.
    """
    if not line.startswith("("):
        return None
    i = 1
    while i < len(line) and line[i] != ")":
        i += 1
    if i >= len(line):
        return None
    start = line[1:i].strip()
    i += 1
    if i >= len(line) or line[i] != "-":
        return None
    i += 1
    if i >= len(line) or line[i] != "[":
        return None
    i += 1
    label_start = i
    while i < len(line) and line[i] not in ("{", "]"):
        i += 1
    label = line[label_start:i].strip()
    props = []
    if i < len(line) and line[i] == "{":
        try:
            props_str, end_idx = _extract_props_block(line, i)
            props = _parse_props_chars(props_str)
            i = end_idx + 1
        except ValueError:
            return None
    while i < len(line) and line[i] != "]":
        i += 1
    if i >= len(line):
        return None
    i += 1  # skip ']'
    if i + 1 >= len(line) or line[i : i + 2] != "->":
        return None
    i += 2
    if i >= len(line) or line[i] != "(":
        return None
    i += 1
    end_start = i
    while i < len(line) and line[i] != ")":
        i += 1
    if i >= len(line):
        return None
    end = line[end_start:i].strip()
    return {"start": start, "label": label, "props": props, "end": end}


def parse_ypg_lines(lines: list) -> tuple:
    """
    Parse a sequence of YPG text lines into (node_records, edge_records).

    Handles multi-line declarations: some property values contain embedded
    newlines. Lines are accumulated until the outermost brace block is
    closed (brace depth returns to zero), then parsed as a single string
    with embedded newlines replaced by spaces.

    node_records: list of {node_id: str, labels: [str], props: [(k, v)]}
    edge_records: list of {start: str, label: str, props: [(k, v)], end: str}
    """
    node_records = []
    edge_records = []
    pending = []

    def brace_depth(s: str) -> int:
        depth = 0
        for c in s:
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
        return depth

    for raw_line in lines:
        line = raw_line.rstrip("\n").rstrip("\r")
        stripped = line.strip()

        # Skip blank lines and comments — unless we are mid-declaration
        if not stripped or stripped.startswith("//") or stripped.startswith("#"):
            if pending:
                pending.append(line)  # blank line inside a multi-line value
            continue

        pending.append(line)
        combined = "\n".join(pending)

        # Declaration is complete when the brace block is fully closed
        if "{" not in combined or brace_depth(combined) == 0:
            pending = []
            parse_line = combined.replace("\n", " ").replace("\r", "")
            if parse_line.lstrip().startswith("("):
                rec = _parse_line_edge(parse_line)
                if rec:
                    edge_records.append(rec)
            else:
                rec = _parse_line_node(parse_line)
                if rec:
                    node_records.append(rec)

    return node_records, edge_records