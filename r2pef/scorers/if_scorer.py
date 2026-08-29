"""IF — Idiomatic Fidelity.

Per source element / occurrence:

- ELEMENT-LEVEL roles (``NR``, ``NPVR``): look up handles via μ_e = R⁻¹ and
  check whether the kinds of those handles match the idiomatic construct
  for the role.
- OCCURRENCE-LEVEL roles (``TMR``, ``ELR``, ``NPKR``): use the PGIU index.
  A triple is scored 1 iff the kinds of the PGIUs covering it form
  exactly the singleton of the idiomatic kind for the role.

Non-idiomatic alternative realisations of the same source unit — whether 
demoting (element-level: a node value appearing also as a label) or redundant
(occurrence-level: an Edge PGIU and a Property PGIU duplicating the
same source triple) — score 0.

Aggregate: scored_1 / (scored_0 + scored_1). Undefined units are reported
separately.

Role glossary
-------------
- ``NR``   — Node Role 
- ``NPVR`` — Node Property Value Role 
- ``TMR``  — Type Marker Role 
- ``NPKR`` — Node Property Key Role 
- ``ELR``  — Edge Label Role 
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple

from r2pef.context.canonicalization import local_name
from r2pef.models.cpgm import ExpressionForm, Node
from r2pef.models.evaluation import EvaluationContext, Handle, PGIU

from .base import Scorer, ScoreResult

# Handle-kind sets used by element-level scoring.
_NODE_KINDS = {"node"}
_NPVR_OK_KINDS = {"node.property.value", "node.label"}
_NPVR_BAD_KINDS = {"node"} 

# Safety caps for very large inputs (e.g. 10⁶ source triples). Aggregates
# are computed from the full input; only the detail entries surfaced into
# JSON / summary.md are capped.
_MAX_DETAIL_PER_BUCKET = 5000
_MAX_CPGM_VALUES_PER_ENTRY = 8

# Idiomatic encoding per element-level / occurrence-level role.
# Used in summary.md to phrase "realized as X instead of <idiomatic>".

IDIOMATIC_FOR_ROLE: Dict[str, str] = {
    "NR":   "node",
    "NPVR": "prop_value",
    "TMR":  "Label",
    "NPKR": "Property",
    "ELR":  "Edge",
}


def _friendly_kind(handle: Handle, node_by_id: Dict[str, Node]) -> str:
    """Translate a raw handle kind into a human-readable bucket.

    ``("node", id)`` becomes ``"literal_node"`` if the underlying node has
    ``node_ref.form == LITERAL``.
    """
    kind = handle[0]
    if kind == "node":
        node = node_by_id.get(handle[1])
        if node is not None and node.node_ref.form == ExpressionForm.LITERAL:
            return "literal_node"
        return "node"
    return {
        "node.label":          "node_label",
        "node.property.key":   "prop_key",
        "node.property.value": "prop_value",
        "edge.label":          "edge_label",
        "edge.property.key":   "edge_prop_key",
        "edge.property.value": "edge_prop_value",
    }.get(kind, kind)


def _handle_cpgm_value(
    handle: Handle, node_by_id: Dict[str, Node], cpgm: Any
) -> Optional[Dict[str, Any]]:
    """Return ``{kind, location, raw, resolved}`` for the handle's underlying ref.

    Used to enrich failing IF element entries: when a resource is encoded as
    a literal-form node, the reader wants to see what string the CPGM
    actually stored (e.g. ``raw='http://.../Country6'`` on a literal-form
    node, surfaced as ``literal_node`` in the bucket).
    """
    kind = handle[0]
    try:
        if kind == "node":
            node = node_by_id.get(handle[1])
            if node is None:
                return None
            return {
                "kind": _friendly_kind(handle, node_by_id),
                "location": f"node[{handle[1]}]",
                "raw": node.node_ref.raw,
                "resolved": node.node_ref.resolved,
                "form": node.node_ref.form.value if node.node_ref.form else None,
            }
        # node.label / node.property.key / node.property.value
        if kind.startswith("node."):
            node = node_by_id.get(handle[1])
            if node is None:
                return None
            idx = handle[2]
            if kind == "node.label":
                ref = node.labels[idx].label_ref
                loc = f"node[{handle[1]}].label[{idx}]"
            elif kind == "node.property.key":
                ref = node.properties[idx].key_ref
                loc = f"node[{handle[1]}].property[{idx}].key"
            else:  # node.property.value
                ref = node.properties[idx].value_ref
                loc = f"node[{handle[1]}].property[{idx}].value"
            return {
                "kind": _friendly_kind(handle, node_by_id),
                "location": loc,
                "raw": ref.raw,
                "resolved": ref.resolved,
                "form": ref.form.value if ref.form else None,
            }
        # edge.* — index 1 is the relation index in cpgm.relations.
        if kind.startswith("edge."):
            rel = cpgm.relations[handle[1]]
            idx = handle[2]
            if kind == "edge.label":
                ref = rel.labels[idx].label_ref
                loc = f"edge[{handle[1]}].label[{idx}]"
            elif kind == "edge.property.key":
                ref = rel.properties[idx].key_ref
                loc = f"edge[{handle[1]}].property[{idx}].key"
            else:
                ref = rel.properties[idx].value_ref
                loc = f"edge[{handle[1]}].property[{idx}].value"
            return {
                "kind": _friendly_kind(handle, node_by_id),
                "location": loc,
                "raw": ref.raw,
                "resolved": ref.resolved,
                "form": ref.form.value if ref.form else None,
            }
    except (IndexError, AttributeError):
        return None
    return None


def _normalize_occ_key(k: Any) -> Any:
    """Normalize an occurrence_roles key to a plain integer when possible.

    Accepts every key shape this codebase has produced or might encounter:

    - ``int``                — current shape, returned as-is
    - ``"5"``                — JSON-loaded current shape

    Anything unrecognised is returned unchanged. This is purely cosmetic;
    the framework never uses the key to look anything up, so the worst
    case is a less-pretty ``"triple_idx"`` in detail entries.
    """
    if isinstance(k, int):
        return k
    if isinstance(k, str):
        try:
            return int(k)
        except ValueError:
            return k
    return k


class IFScorer(Scorer):
    name = "if"

    def score(self, ctx: EvaluationContext) -> ScoreResult:
        roles = ctx.role_classification

        element_roles: Dict[str, str] = roles.get("element_roles", {}) or {}
        # Shape: ``occurrence_roles[idx] = {"role": ..., "triple": (s,p,o)}``.
        occurrence_roles: Dict[Any, Dict[str, Any]] = (
            roles.get("occurrence_roles", {}) or {}
        )

        # Look-up table from node id (start/end string) to Node, for the
        # element-level checks that need node_ref.form / node_ref.synthetic.
        node_by_id: Dict[str, Node] = {n.id: n for n in ctx.cpgm.nodes}

        # Hard cap on per-bucket detail entries — protects memory and the
        # eventual JSON serialisation cost. Aggregate counts are tracked
        # *outside* the capped lists so they remain accurate.
        cap = _MAX_DETAIL_PER_BUCKET

        # -----------------------------------------------------------------
        # Element-level
        # -----------------------------------------------------------------
        elem_pass: List[Dict[str, Any]] = []
        elem_fail: List[Dict[str, Any]] = []
        elem_undef: List[Dict[str, Any]] = []
        elem_counts = {"scored_1": 0, "scored_0": 0, "undefined": 0}
        # Per-role tally for the report's "100% undefined" sanity check.
        by_role: Dict[str, Dict[str, int]] = {}

        def _bump_role(role: str, bucket: str) -> None:
            r = by_role.setdefault(role, {"scored_1": 0, "scored_0": 0, "undefined": 0})
            r[bucket] += 1

        for u, role in element_roles.items():
            handles = ctx.R_inv.lookup(u)
            mu_kinds = sorted({_friendly_kind(h, node_by_id) for h in handles}) if handles else []
            idiomatic = IDIOMATIC_FOR_ROLE.get(role, "")

            if not handles:
                elem_counts["undefined"] += 1
                _bump_role(role, "undefined")
                if len(elem_undef) < cap:
                    elem_undef.append({
                        "unit": u, "role": role, "mu_kinds": mu_kinds,
                        "idiomatic_kind": idiomatic, "score": None,
                        "reason": "mu_e empty",
                    })
                continue

            score = self._score_element(role, handles, node_by_id)
            entry = {
                "unit": u, "role": role, "mu_kinds": mu_kinds,
                "idiomatic_kind": idiomatic, "score": score,
            }
            if score is None:
                elem_counts["undefined"] += 1
                _bump_role(role, "undefined")
                if len(elem_undef) < cap:
                    elem_undef.append(entry)
            elif score == 1:
                elem_counts["scored_1"] += 1
                _bump_role(role, "scored_1")
                if len(elem_pass) < cap:
                    elem_pass.append(entry)
            else:
                elem_counts["scored_0"] += 1
                _bump_role(role, "scored_0")
                if len(elem_fail) < cap:
                    # Attach actual CPGM values for failing entries
                    entry["cpgm_values"] = [
                        v for v in (
                            _handle_cpgm_value(h, node_by_id, ctx.cpgm)
                            for h in handles
                        ) if v is not None
                    ][: _MAX_CPGM_VALUES_PER_ENTRY]
                    elem_fail.append(entry)

        # -----------------------------------------------------------------
        # Occurrence-level
        # -----------------------------------------------------------------
        occ_pass: List[Dict[str, Any]] = []
        occ_fail: List[Dict[str, Any]] = []
        occ_undef: List[Dict[str, Any]] = []
        occ_counts = {"scored_1": 0, "scored_0": 0, "undefined": 0}

        for key, info in occurrence_roles.items():
            role = info.get("role")
            triple = info.get("triple")
            if triple is None:
                continue
            t = tuple(triple)  # type: ignore[assignment]
            covering = self._covering_pgius(ctx, t)
            idiomatic = IDIOMATIC_FOR_ROLE.get(role, "")
            kinds = sorted({u.kind for u in covering}) if covering else []
            # The classifier emits int keys (each is a triple index). If the
            # data came round-trip through JSON the key may be a string;
            # normalise to int when possible so detail entries are stable
            # across direct-call vs JSON-loaded use.
            tk = _normalize_occ_key(key)

            if not covering:
                occ_counts["undefined"] += 1
                _bump_role(role, "undefined")
                if len(occ_undef) < cap:
                    occ_undef.append({
                        "triple_idx": tk, "role": role, "triple": list(t),
                        "pgiu_kinds": kinds, "idiomatic_kind": idiomatic,
                        "score": None, "reason": "no PGIU covers triple",
                    })
                continue

            score = self._score_occurrence(role, covering)
            entry = {
                "triple_idx": tk, "role": role, "triple": list(t),
                "pgiu_kinds": kinds, "idiomatic_kind": idiomatic,
                "score": score,
            }
            if score is None:
                occ_counts["undefined"] += 1
                _bump_role(role, "undefined")
                if len(occ_undef) < cap:
                    occ_undef.append(entry)
            elif score == 1:
                occ_counts["scored_1"] += 1
                _bump_role(role, "scored_1")
                if len(occ_pass) < cap:
                    occ_pass.append(entry)
            else:
                occ_counts["scored_0"] += 1
                _bump_role(role, "scored_0")
                if len(occ_fail) < cap:
                    occ_fail.append(entry)

        # -----------------------------------------------------------------
        # Aggregate
        # -----------------------------------------------------------------
        s1 = elem_counts["scored_1"] + occ_counts["scored_1"]
        s0 = elem_counts["scored_0"] + occ_counts["scored_0"]
        ud = elem_counts["undefined"] + occ_counts["undefined"]
        total = s1 + s0 + ud

        if (s1 + s0) > 0:
            agg = s1 / (s1 + s0)
            all_undefined = False
        else:
            # No units could be scored — every unit was undefined. Returning
            # a flat 0.0 conflates this with "every unit failed". The score
            # is reported as 0.0 with an explicit `all_undefined=True` flag
            # so the reporter can call it out instead of silently passing.
            agg = 0.0
            all_undefined = total > 0

        undefined_rate = (ud / total) if total > 0 else 0.0

        # Merge per-bucket detail lists, preserving order pass | fail | undef.
        return ScoreResult(
            metric=self.name,
            score=agg,
            counts={
                "scored_1": s1,
                "scored_0": s0,
                "undefined": ud,
                "total": total,
            },
            extras={
                "undefined_rate": undefined_rate,
                "element_counts": elem_counts,
                "occurrence_counts": occ_counts,
                "by_role": by_role,
                "all_undefined": all_undefined,
                "detail_truncated_at": cap,
                "threshold": self.threshold,
                "passed_threshold": agg >= self.threshold and not all_undefined,
            },
            detail={
                "elements": elem_pass + elem_fail + elem_undef,
                "occurrences": occ_pass + occ_fail + occ_undef,
            },
        )

    # ---------------------------------------------------------------- helpers

    def _covering_pgius(
        self, ctx: EvaluationContext, t: Tuple[str, str, str]
    ) -> List[PGIU]:
        """Find every PGIU covering source triple ``t``.

        Direct match first; local-name match if direct is empty. This mirrors
        the "= means exact OR local-name equality" rule in the spec.
        """
        covering = ctx.triple_to_pgius.get(t)
        if covering:
            return covering
        ln_key = (local_name(t[0]), local_name(t[1]), local_name(t[2]))
        return ctx.ln_triple_to_pgius.get(ln_key, [])

    def _score_element(
        self,
        role: str,
        handles: Set[Handle],
        node_by_id: Dict[str, Node],
    ) -> Optional[int]:
        """Return 1, 0, or None (undefined) for an element-level unit."""
        kinds = {h[0] for h in handles}

        if role == "NR":
            # All handles must be node handles, and none of those nodes may be
            # synthetic or value-bearing (form == literal).
            if kinds == _NODE_KINDS:
                for h in handles:
                    node = node_by_id.get(h[1])
                    if node is None:
                        return 0
                    if node.node_ref.synthetic:
                        return 0
                    if node.node_ref.form == ExpressionForm.LITERAL:
                        return 0
                return 1
            return 0

        if role == "NPVR":
            # No handle may be a node handle. The remaining ones must all be
            # in the NPVR-OK set.
            if _NPVR_BAD_KINDS & kinds:
                return 0
            if kinds <= _NPVR_OK_KINDS:
                return 1
            return 0

        # Unknown role — undefined.
        return None

    def _score_occurrence(self, role: str, covering: List[PGIU]) -> Optional[int]:
        # Strict subset rule (parallel to element-level): the set of PGIU
        # kinds covering the triple must be exactly the singleton of the
        # idiomatic kind. A covering set with multiple kinds — e.g. an
        # idiomatic Edge plus a redundant Property duplicating the same
        # triple — is non-idiomatic.
        kinds = {u.kind for u in covering}
        if role == "TMR":
            return 1 if kinds == {"Label"} else 0
        if role == "NPKR":
            return 1 if kinds == {"Property"} else 0
        if role == "ELR":
            return 1 if kinds == {"Edge"} else 0
        return None
