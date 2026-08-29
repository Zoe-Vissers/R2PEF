"""Build an EvaluationContext from a CPGM and source RDF.

The algorithms below run in a single pass over the CPGM, 
building all registries and indices that the three scorers need:

- ``R``               — ProvenanceRegistry (forward handle → resolved string)
- ``R⁻¹``             — ProvenanceReverseRegistry (direct + local-name index)
- ``PGIUs`` — Property Graph Information Units, one per non-synthetic
  label / property / generic-edge property
- ``derived_triples(C)`` — the set produced by applying the function
  ``derive`` to ``(PGIUs(C), R)``; each PGIU yields one triple via R
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from rdflib import Graph

from r2pef.models.cpgm import (
    CPGM,
    Node,
    Relation,
    ResourceHandle,
)
from r2pef.models.evaluation import (
    EvaluationContext,
    Handle,
    PGIU,
    ProvenanceRegistry,
    ProvenanceReverseRegistry,
)

from .canonicalization import local_name, object_variants


# The RDF type predicate used by Label PGIUs.
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"


# ---------------------------------------------------------------------------
# Source-RDF parsing
# ---------------------------------------------------------------------------
def parse_source_rdf(
    path: Path,
) -> Tuple[List[Tuple[str, str, str]], Dict[Tuple[str, str, str], Tuple[str, str, str]]]:
    """Parse the source graph and return both matching-form triples and a
    matching-tuple → display-tuple lookup.

    Returns
    -------
    (triples, display)
        ``triples``: list of (s, p, o) string triples in matching form.
        Literal objects are lexical-only (datatype and language suffixes
        stripped) so that the framework's string-equality matching against
        adapter outputs — which by design treat literals as lexical strings
        — produces consistent results.

        ``display``: a mapping from each matching tuple to a parallel
        (s, p, o) tuple in *display* form, which preserves datatype and
        language suffixes via ``rdflib.term.Literal.n3()`` (e.g.
        ``"272.68"^^<http://example.org/USD>``). This is used by the
        reporter and the IP scorer's lost-sample bookkeeping to render
        diagnostic information faithfully without altering the matching
        semantics.

    Notes
    -----
    The matching-form vs display-form split is deliberate: the framework
    matches by lexical-form string equality (it does not implement xsd
    value-space equivalence), so the matching form must stay datatype-stripped. 
    But for diagnosing lost triples, showing the datatype suffix could be 
    helpful.
    """
    g = Graph()
    if str(path).endswith(".nt"):
        g.parse(str(path), format="nt")
    elif str(path).endswith(".ttl"):
        g.parse(str(path), format="turtle")
    else:
        g.parse(str(path))

    triples: List[Tuple[str, str, str]] = []
    display: Dict[Tuple[str, str, str], Tuple[str, str, str]] = {}
    for s, p, o in g:
        match_t = (_term_to_str(s), _term_to_str(p), _term_to_str(o))
        triples.append(match_t)
        # Only record a display form when it differs informatively from
        # the matching form (i.e., for literals with a datatype or language
        # tag). For plain IRIs and untyped literals, the matching form is
        # already the display form.
        if match_t not in display:
            display[match_t] = (
                _term_to_display(s),
                _term_to_display(p),
                _term_to_display(o),
            )
    return triples, display


def _term_to_display(term: Any) -> str:
    """Render an rdflib term for human display, preserving datatype and
    language annotations on literals.

    Unlike :func:`_term_to_str`, which produces the lexical-only matching
    form, this returns the N3-style serialisation when the literal carries
    a datatype or language tag::

        Literal("272.68", datatype=USD)  → '"272.68"^^<http://...USD>'
        Literal("hello", lang="en")       → '"hello"@en'

    For plain literals (no datatype/lang) the result is identical to the
    matching form. URIRefs and BNodes are unchanged.
    """
    from rdflib import BNode, Literal, URIRef

    if isinstance(term, URIRef):
        return str(term)
    if isinstance(term, BNode):
        return f"_:{term}"
    if isinstance(term, Literal):
        if term.datatype is not None or term.language is not None:
            return term.n3()
        # Plain literal — fall through to the matching-form rendering so
        # display and matching strings agree when there's nothing extra
        # to show.
        return _term_to_str(term)
    return str(term)


def _term_to_str(term: Any) -> str:
    """Normalise an rdflib term to a flat string the framework can compare.

    - URIRefs : the bare IRI string.
    - BNodes  : ``_:<id>``.
    - Literals: the lexical value, surrounded by ``"``.
    """
    from rdflib import BNode, Literal, URIRef

    if isinstance(term, URIRef):
        return str(term)
    if isinstance(term, BNode):
        return f"_:{term}"
    if isinstance(term, Literal):
        lex = str(term)
        # Smart wrap: don't double-wrap a value whose lexical form already
        # starts and ends with quote characters.
        if len(lex) >= 2 and lex.startswith('"') and lex.endswith('"'):
            return lex
        return f'"{lex}"'
    return str(term)


# ---------------------------------------------------------------------------
# Provenance registry construction
# ---------------------------------------------------------------------------
def _record(
    forward: Dict[Handle, str],
    direct: Dict[str, Set[Handle]],
    h: Handle,
    ref: ResourceHandle,
) -> None:
    """Insert handle ``h`` into R and R⁻¹.direct if the ref is usable.

    Inserts the handle under *every* object variant of ``ref.resolved`` so
    quoted/unquoted lookups both succeed.
    """
    if ref.synthetic:
        return
    if ref.resolved is None:
        return
    forward[h] = ref.resolved
    for v in object_variants(ref.resolved):
        bucket = direct.get(v)
        if bucket is None:
            bucket = set()
            direct[v] = bucket
        bucket.add(h)


def build_registries(
    cpgm: CPGM,
) -> Tuple[ProvenanceRegistry, ProvenanceReverseRegistry]:
    """Single pass over the CPGM, producing R and R⁻¹.

    The function builds the direct (Phase 1) and local-name (Phase 2)
    sides of R⁻¹ in the same loop — there is no point in two passes when
    every element is visited exactly once anyway.
    """
    forward: Dict[Handle, str] = {}
    direct: Dict[str, Set[Handle]] = {}
    ln_index: Dict[str, Set[Handle]] = {}

    def _index_ln(h: Handle, resolved: str) -> None:
        # Index under the local name of every object variant. This is what
        # makes ``nss9_parentCountry`` reachable from a query for
        # ``http://www.geonames.org/ontology#parentCountry``: both reduce
        # to local name ``parentCountry``.
        for v in object_variants(resolved):
            ln = local_name(v)
            bucket = ln_index.get(ln)
            if bucket is None:
                bucket = set()
                ln_index[ln] = bucket
            bucket.add(h)

    # --- nodes ------------------------------------------------------------
    for node in cpgm.nodes:
        node_id = node.id
        h_node: Handle = ("node", node_id)
        if not node.node_ref.synthetic and node.node_ref.resolved is not None:
            forward[h_node] = node.node_ref.resolved
            for v in object_variants(node.node_ref.resolved):
                direct.setdefault(v, set()).add(h_node)
            _index_ln(h_node, node.node_ref.resolved)

        for i, lab in enumerate(node.labels):
            h = ("node.label", node_id, i)
            _record(forward, direct, h, lab.label_ref)
            if h in forward:
                _index_ln(h, forward[h])

        for i, prop in enumerate(node.properties):
            h_k: Handle = ("node.property.key", node_id, i)
            h_v: Handle = ("node.property.value", node_id, i)
            _record(forward, direct, h_k, prop.key_ref)
            _record(forward, direct, h_v, prop.value_ref)
            if h_k in forward:
                _index_ln(h_k, forward[h_k])
            if h_v in forward:
                _index_ln(h_v, forward[h_v])

    # --- relations --------------------------------------------------------
    for ei, rel in enumerate(cpgm.relations):
        for i, lab in enumerate(rel.labels):
            h = ("edge.label", ei, i)
            _record(forward, direct, h, lab.label_ref)
            if h in forward:
                _index_ln(h, forward[h])

        for i, prop in enumerate(rel.properties):
            h_k = ("edge.property.key", ei, i)
            h_v = ("edge.property.value", ei, i)
            _record(forward, direct, h_k, prop.key_ref)
            _record(forward, direct, h_v, prop.value_ref)
            if h_k in forward:
                _index_ln(h_k, forward[h_k])
            if h_v in forward:
                _index_ln(h_v, forward[h_v])

    return (
        ProvenanceRegistry(forward=forward),
        ProvenanceReverseRegistry(direct=direct, ln_index=ln_index),
    )


# ---------------------------------------------------------------------------
# PGIU construction
# ---------------------------------------------------------------------------
def _is_generic_relation(rel: Relation) -> bool:
    """All labels synthetic → relation is "generic", carries predicate as prop key."""
    # Empty-labels edges are considered generic too — they have no idiomatic
    # representation, only property-carried provenance.
    return all(lab.label_ref.synthetic for lab in rel.labels)


def _node_end_object(node_by_id: Dict[str, Node]) -> Dict[str, Optional[str]]:
    """Pre-compute the "object" string for every node identity.

    For a normal resource node this is ``node_ref.resolved`` (the resolved
    IRI). For a value-bearing node (``node_ref.form == literal``) the schema
    guarantees ``node_ref.resolved`` is the literal value itself — the
    adapter is responsible for promoting the literal value into
    ``node_ref.resolved`` regardless of whether it ALSO appears as a
    property on the node. Synthetic nodes have no source-side counterpart
    and contribute ``None`` (any edge into a synthetic end is dropped).

    Returns a dict so Edge / Generic-edge PGIU construction can look up
    the end-object in O(1) per edge.
    """
    out: Dict[str, Optional[str]] = {}
    for node_id, node in node_by_id.items():
        if node.node_ref.synthetic:
            out[node_id] = None
        else:
            out[node_id] = node.node_ref.resolved
    return out


def build_pgius(
    cpgm: CPGM,
    R: ProvenanceRegistry,
) -> List[PGIU]:
    """Build PGIUs from a CPGM and its provenance registry.

    See the spec table:

      Label         (R(node), rdf:type, R(node.label))
      Property      (R(node), R(node.prop.key),   R(node.prop.value))
      Edge          (R(start), R(edge.label), R(end))           — value-bearing end rule
      Generic-edge  (R(start), R(edge.prop.value), R(end))

    Each non-synthetic label / property / generic-edge property yields one
    PGIU. The PGIU carries its anchor (a Handle pointing back into the CPGM)
    and the triple it would derive under ``derive``. Apply ``derive`` to the
    result of this function to obtain ``derived_triples(C)``.
    """
    pgius: List[PGIU] = []

    node_by_id: Dict[str, Node] = {n.id: n for n in cpgm.nodes}
    end_object_lookup = _node_end_object(node_by_id)

    # --- node-anchored PGIUs (Label + Property) ---------------------------
    for node in cpgm.nodes:
        node_id = node.id
        if node.node_ref.synthetic:
            continue
        subj = node.node_ref.resolved
        if subj is None:
            continue

        # Label PGIUs.
        for i, lab in enumerate(node.labels):
            if lab.label_ref.synthetic or lab.label_ref.resolved is None:
                continue
            anchor: Handle = ("node.label", node_id, i)
            t = (subj, RDF_TYPE, lab.label_ref.resolved)
            pgius.append(PGIU(kind="Label", anchor=anchor, triple=t))

        # Property PGIUs.
        for i, prop in enumerate(node.properties):
            if prop.key_ref.synthetic or prop.value_ref.synthetic:
                continue
            if prop.key_ref.resolved is None or prop.value_ref.resolved is None:
                continue
            anchor = ("node.property.key", node_id, i)
            t = (subj, prop.key_ref.resolved, prop.value_ref.resolved)
            pgius.append(PGIU(kind="Property", anchor=anchor, triple=t))

    # --- edge-anchored PGIUs (Edge + Generic-edge) ------------------------
    for ei, rel in enumerate(cpgm.relations):
        s_node = node_by_id.get(rel.start)
        e_node = node_by_id.get(rel.end)
        if s_node is None or e_node is None:
            continue
        if s_node.node_ref.synthetic:
            continue
        subj = s_node.node_ref.resolved
        if subj is None:
            continue
        obj = end_object_lookup.get(rel.end)
        if obj is None:
            continue

        if _is_generic_relation(rel):
            # Generic-edge encoding: the relation's label is synthetic (e.g.
            # "DatatypeProperty" / "ObjectProperty"), and the
            # real predicate is carried as a *property value* on the edge
            # (the property's key is itself a synthetic housekeeping label
            # like "type" or "predicate"). To reconstruct the source triple
            # we use the value of each non-synthetic property as the
            # predicate. Anchor on the value handle since that's where the
            # predicate provenance lives.
            for i, prop in enumerate(rel.properties):
                if prop.value_ref.synthetic or prop.value_ref.resolved is None:
                    continue
                anchor = ("edge.property.value", ei, i)
                t = (subj, prop.value_ref.resolved, obj)
                pgius.append(PGIU(kind="Generic-edge", anchor=anchor, triple=t))
        else:
            # Edge: one PGIU per non-synthetic label.
            for i, lab in enumerate(rel.labels):
                if lab.label_ref.synthetic or lab.label_ref.resolved is None:
                    continue
                anchor = ("edge.label", ei, i)
                t = (subj, lab.label_ref.resolved, obj)
                pgius.append(PGIU(kind="Edge", anchor=anchor, triple=t))

    return pgius


def derive(pgius: List[PGIU]) -> frozenset:
    """Apply the function ``derive`` to a list of PGIUs.

    Each derived triple is registered under every object-variant
    (``raw``, ``quoted``, ``unquoted``) so that IP's direct
    ``t in derived_triples(C)`` check matches regardless of whether
    the source-side or CPGM-side object happens to be quoted. 

    Returns the resulting set as a frozenset.
    """
    triples: Set[Tuple[str, str, str]] = set()
    for u in pgius:
        for o_var in object_variants(u.triple[2]):
            triples.add((u.triple[0], u.triple[1], o_var))
    return frozenset(triples)


def _index_pgius_by_triple(
    pgius: List[PGIU],
) -> Tuple[Dict[Tuple[str, str, str], List[PGIU]], Dict[Tuple[str, str, str], List[PGIU]]]:
    """Index PGIUs by direct triple and by local-name triple.
    """
    by_triple: Dict[Tuple[str, str, str], List[PGIU]] = {}
    by_ln_triple: Dict[Tuple[str, str, str], List[PGIU]] = {}
    for u in pgius:
        s, p, o = u.triple
        for o_var in object_variants(o):
            by_triple.setdefault((s, p, o_var), []).append(u)
            ln_t = (local_name(s), local_name(p), local_name(o_var))
            by_ln_triple.setdefault(ln_t, []).append(u)
    return by_triple, by_ln_triple


# ---------------------------------------------------------------------------
# Top-level builder
# ---------------------------------------------------------------------------
def build_context(
    cpgm: CPGM,
    source_rdf_path: Path,
    role_classification: Dict[str, Any],
) -> EvaluationContext:
    """Construct the EvaluationContext shared by all scorers.

    The order is deliberate — every later step depends only on the earlier
    ones, so a failure in one phase produces a clean diagnostic.
    """
    t0 = time.perf_counter()

    source_triples, source_triple_display = parse_source_rdf(source_rdf_path)
    R, R_inv = build_registries(cpgm)
    pgius = build_pgius(cpgm, R)
    derived = derive(pgius)
    by_triple, by_ln_triple = _index_pgius_by_triple(pgius)

    return EvaluationContext(
        cpgm=cpgm,
        source_triples=source_triples,
        source_triple_display=source_triple_display,
        role_classification=role_classification,
        R=R,
        R_inv=R_inv,
        pgius=pgius,
        derived_triples=derived,
        triple_to_pgius=by_triple,
        ln_triple_to_pgius=by_ln_triple,
        wall_time_build_s=time.perf_counter() - t0,
    )