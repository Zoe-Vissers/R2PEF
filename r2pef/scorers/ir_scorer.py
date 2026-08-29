"""IR — Identifier Retention.

IR iterates over the CPGM's identifier-bearing ResourceHandles — the
target side — and asks of each: how informative is this handle as an
identifier? Each handle is judged on its own ``form`` and ``resolved``,
without any reference to the source RDF. The metric is intrinsic to
the CPGM.

Tier table (per non-synthetic, non-literal-form CPGM handle):

    full_iri                                       -> full,    w = 1.0
    namespace_plus_local + adapter expanded prefix
        (``://`` in resolved)                      -> full,    w = 1.0
    namespace_plus_local + adapter kept shortform
        (no ``://`` in resolved)                   -> partial, w = 0.5
    local_only                                     -> local,   w = 0.0


IR universe: non-synthetic, non-literal-form ResourceHandles in the
CPGM.

A blank node's encoding is classified as local-tier, which faithfully 
reflects the encoding's identifier retention on its own terms. 
No adjustment made to compensate for the source-side's lack of a
global identifier.

Aggregate: mean(per-handle tier weight) over the IR universe.

Construct-group breakdown
-------------------------
The metric also reports tier distributions per CPGM construct group
(node identifiers, node labels, node property keys, node property
values, edge labels, edge property keys, edge property values), so the
reader can see which construct groups the translation handles with
which encoding form. Different translation algorithms apply different
conventions per construct group (e.g. one might use full IRIs for node
identifiers but kept shortforms for edge labels), and the construct-
group breakdown surfaces this pattern at a glance.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List, Optional

from r2pef.models.cpgm import (
    CPGM,
    ExpressionForm,
    ResourceHandle,
)
from r2pef.models.evaluation import EvaluationContext, Handle

from .base import Scorer, ScoreResult


TIER_WEIGHT = {
    "full": 1.0,
    "partial": 0.5,
    "local": 0.0,
}


# Construct groups, in display order. The first element of a Handle
# tuple matches these keys exactly, so the group of a handle is just
# ``handle[0]``.
_CONSTRUCT_GROUPS = [
    "node",
    "node.label",
    "node.property.key",
    "node.property.value",
    "edge.label",
    "edge.property.key",
    "edge.property.value",
]


class IRScorer(Scorer):
    name = "ir"

    def __init__(self, threshold: float = 0.9) -> None:
        super().__init__(threshold=threshold)

    def score(self, ctx: EvaluationContext) -> ScoreResult:
        universe: List[tuple] = []
        for h, ref in _iter_handles_and_refs(ctx.cpgm):
            if ref.synthetic:
                continue
            if ref.form == ExpressionForm.LITERAL:
                continue
            if ref.form is None:
                continue
            universe.append((h, ref))

        # Per-handle classification and scoring.
        per_handle_details: List[Dict[str, Any]] = []
        scores: List[float] = []
        tier_dist = {"full": 0, "partial": 0, "local": 0}
        # Per-construct-group tier breakdown: 
        by_group: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {
                "full": 0,
                "partial": 0,
                "local": 0,
                "full_direct": 0,
                "full_expanded": 0,
            }
        )

        for h, ref in universe:
            tier = _classify_tier(ref)
            if tier is None:
                continue
            w = TIER_WEIGHT[tier]
            scores.append(w)
            tier_dist[tier] += 1
            group = h[0]
            by_group[group][tier] += 1
            # Diagnostic sub-classification of the full tier.
            if tier == "full":
                if ref.form == ExpressionForm.FULL_IRI:
                    by_group[group]["full_direct"] += 1
                else:
                    # namespace_plus_local with "://" in resolved
                    by_group[group]["full_expanded"] += 1
            per_handle_details.append(
                {
                    "handle": _describe_location(h),
                    "group": group,
                    "form": ref.form.value if ref.form else None,
                    "resolved": ref.resolved,
                    "raw": ref.raw,
                    "tier": tier,
                    "score": w,
                }
            )

        agg = (sum(scores) / len(scores)) if scores else 0.0

        # Build a stable, ordered view of the construct-group breakdown
        # for the detail payload.
        group_breakdown = []
        for g in _CONSTRUCT_GROUPS:
            tiers = by_group.get(g)
            if tiers is None:
                continue
            total = tiers["full"] + tiers["partial"] + tiers["local"]
            if total == 0:
                continue
            group_score = (
                tiers["full"] * TIER_WEIGHT["full"]
                + tiers["partial"] * TIER_WEIGHT["partial"]
                + tiers["local"] * TIER_WEIGHT["local"]
            ) / total
            group_breakdown.append({
                "group": g,
                "full": tiers["full"],
                "full_direct": tiers["full_direct"],
                "full_expanded": tiers["full_expanded"],
                "partial": tiers["partial"],
                "local": tiers["local"],
                "total": total,
                "score": group_score,
            })

        return ScoreResult(
            metric=self.name,
            score=agg,
            counts={
                "universe": len(scores),
                **tier_dist,
            },
            extras={
                "threshold": self.threshold,
                "passed_threshold": agg >= self.threshold,
            },
            detail={
                "handles": per_handle_details,
                "by_construct_group": group_breakdown,
            },
        )


# ---------------------------------------------------------------------------
# Tier classification
# ---------------------------------------------------------------------------
def _classify_tier(ref: ResourceHandle) -> Optional[str]:
    """Return ``"full" | "partial" | "local"`` for a single CPGM handle.
    """
    if ref.form is None:
        return None
    if ref.form == ExpressionForm.FULL_IRI:
        return "full"
    if ref.form == ExpressionForm.NAMESPACE_PLUS_LOCAL:
        if ref.resolved and "://" in ref.resolved:
            return "full"
        return "partial"
    if ref.form == ExpressionForm.LOCAL_ONLY:
        return "local"
    return None


# ---------------------------------------------------------------------------
# Iteration over CPGM handles
# ---------------------------------------------------------------------------
def _iter_handles_and_refs(cpgm: CPGM):
    """Yield every ``(handle, ResourceHandle)`` pair in the CPGM.
    """
    for node in cpgm.nodes:
        nid = node.id
        yield ("node", nid), node.node_ref
        for i, lab in enumerate(node.labels):
            yield ("node.label", nid, i), lab.label_ref
        for i, prop in enumerate(node.properties):
            yield ("node.property.key", nid, i), prop.key_ref
            yield ("node.property.value", nid, i), prop.value_ref
    for ei, rel in enumerate(cpgm.relations):
        for i, lab in enumerate(rel.labels):
            yield ("edge.label", ei, i), lab.label_ref
        for i, prop in enumerate(rel.properties):
            yield ("edge.property.key", ei, i), prop.key_ref
            yield ("edge.property.value", ei, i), prop.value_ref


def _describe_location(h: Handle) -> str:
    """A human-friendly location string for the IR detail report."""
    kind = h[0]
    if kind == "node":
        return f"node[{h[1]}]"
    if kind == "node.label":
        return f"node[{h[1]}].label[{h[2]}]"
    if kind == "node.property.key":
        return f"node[{h[1]}].property[{h[2]}].key"
    if kind == "node.property.value":
        return f"node[{h[1]}].property[{h[2]}].value"
    if kind == "edge.label":
        return f"edge[{h[1]}].label[{h[2]}]"
    if kind == "edge.property.key":
        return f"edge[{h[1]}].property[{h[2]}].key"
    if kind == "edge.property.value":
        return f"edge[{h[1]}].property[{h[2]}].value"
    return repr(h)