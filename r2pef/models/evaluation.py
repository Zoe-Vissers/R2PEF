"""Shared data structures consumed by all three scorers.

The ``EvaluationContext`` is built once by ``context/builder.py`` and is read
(never mutated) by the IF, IP, and IR scorers. It contains:

- The parsed source triples (for IP and μ_o pattern matching)
- The role-classifier output (for IF)
- The ``ProvenanceRegistry`` R                       — handle → resolved string
- The ``ProvenanceReverseRegistry`` R⁻¹              — resolved string → handles
- The ``PGIUSet`` and derived-triple frozenset       — used by IP and IF
- Per-node and per-edge indices that PGIU and μ_o construction need
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import (
    Any,
    Dict,
    FrozenSet,
    List,
    Optional,
    Set,
    Tuple,
)

from r2pef.models.cpgm import CPGM


# ---------------------------------------------------------------------------
# Element handle algebra
# ---------------------------------------------------------------------------
# An *element handle* is a tuple identifying one identifier-bearing element inside a
# CPGM. 
#
# Element handle kinds (first element of the tuple):
#   ("node",            node_id)
#   ("node.label",      node_id, label_index)
#   ("node.property.key",   node_id, prop_index)
#   ("node.property.value", node_id, prop_index)
#   ("edge.label",      edge_index, label_index)
#   ("edge.property.key",   edge_index, prop_index)
#   ("edge.property.value", edge_index, prop_index)
#
# ``node_id`` is the string used by Relation.start/end (Node.id). 
# ``edge_index`` is the integer index into ``CPGM.relations``.
Handle = Tuple  # alias only; runtime shape is the tuples above.


def handle_kind(h: Handle) -> str:
    """Return the first element of the handle tuple."""
    return h[0]


# ---------------------------------------------------------------------------
# Provenance registries
# ---------------------------------------------------------------------------
@dataclass
class ProvenanceRegistry:
    """R : H(C) → S.

    ``R[handle]`` gives the ``resolved`` string for that element. Handles
    whose underlying ResourceHandle was synthetic or had a null ``resolved``
    are not in the map.
    """

    forward: Dict[Handle, str] = field(default_factory=dict)

    # --- basic API ---------------------------------------------------------
    def __contains__(self, h: Handle) -> bool:
        return h in self.forward

    def __getitem__(self, h: Handle) -> str:
        return self.forward[h]

    def get(self, h: Handle, default: Optional[str] = None) -> Optional[str]:
        return self.forward.get(h, default)

    def __len__(self) -> int:
        return len(self.forward)

    def items(self):
        return self.forward.items()


@dataclass
class ProvenanceReverseRegistry:
    """R⁻¹ : S → 2^{H(C)}.

    Phase 1: direct inverse of R. Phase 2: local-name index over CPGM strings
    only. Query merges both, so the caller never needs to know which phase a
    handle came from.
    """

    direct: Dict[str, Set[Handle]] = field(default_factory=dict)
    ln_index: Dict[str, Set[Handle]] = field(default_factory=dict)

    def lookup(self, q: str, ln_q: Optional[str] = None) -> Set[Handle]:
        """Return the union of direct and local-name matches.

        Pass ``ln_q`` if the caller already has the local name to save a
        recomputation (this matters in tight loops over millions of triples).
        """
        from r2pef.context.canonicalization import local_name

        if ln_q is None:
            ln_q = local_name(q)
        out: Set[Handle] = set()
        if q in self.direct:
            out.update(self.direct[q])
        if ln_q in self.ln_index:
            out.update(self.ln_index[ln_q])
        return out


# ---------------------------------------------------------------------------
# PGIUs — Property-Graph Information Units
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class PGIU:
    """A single Property Graph Information Unit.

    ``kind`` ∈ {"Label", "Property", "Edge", "Generic-edge"}.

    ``anchor`` is the handle that produced this unit (e.g. the label handle for
    a Label PGIU, the property-key handle for a Property PGIU, the label
    handle for an Edge PGIU, the property-key handle for a Generic-edge PGIU).

    ``triple`` is the derived triple (s, p, o) — all strings, fully resolved.
    """

    kind: str
    anchor: Handle
    triple: Tuple[str, str, str]


# ---------------------------------------------------------------------------
# Aggregate context
# ---------------------------------------------------------------------------
@dataclass
class EvaluationContext:
    """Everything the three scorers need, computed once."""

    # --- raw inputs --------------------------------------------------------
    cpgm: CPGM
    source_triples: List[Tuple[str, str, str]]
    # Diagnostic display form: maps each matching-form triple to a parallel
    # (s, p, o) tuple that preserves literal datatype and language
    # annotations via n3-style rendering. Used only for human-facing
    # diagnostic output (the IP scorer's lost-sample bookkeeping and the
    # reporter); the scoring logic itself operates on ``source_triples`` in
    # matching form.
    source_triple_display: Dict[Tuple[str, str, str], Tuple[str, str, str]]
    role_classification: Dict[str, Any]

    # --- registries --------------------------------------------------------
    R: ProvenanceRegistry
    R_inv: ProvenanceReverseRegistry

    # --- PGIUs / derived_triples(C) -------------------------------------------------
    pgius: List[PGIU]
    derived_triples: FrozenSet[Tuple[str, str, str]]

    # Lookup index: triple (s,p,o)  -> list of PGIUs producing it.
    # Used by IF occurrence-level scoring (direct hits only).
    triple_to_pgius: Dict[Tuple[str, str, str], List[PGIU]]

    # Local-name index over derived triples.
    # Keys are (ln(s), ln(p), ln(o)); values are sets of PGIUs.
    # Used by IF when direct triple lookup misses, and by IP for ln-matching.
    ln_triple_to_pgius: Dict[Tuple[str, str, str], List[PGIU]]

    # --- per-element helpers used by IF and μ_o ---------------------------
    # node_id → set of node-property handles whose value is x.
    # Currently built lazily inside the IF scorer; kept here as a slot for
    # future eager caching.

    # --- prefix and timing meta -------------------------------------------
    wall_time_build_s: float = 0.0