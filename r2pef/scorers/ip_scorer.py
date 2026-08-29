"""IP — Information Preservation.

For each unique source triple t = (s, p, o), check whether derived_triples(C) contains a
matching triple t' = (s', p', o') where each component matches by direct
equality or by local-name equality.

Tiers:
    full — at least one matching triple in derived_triples(C)
    none — no match

Aggregate: |full| / |T|.

Implementation
--------------
``ctx.derived_triples`` is the frozenset of all derived triples. A direct
``t in derived_triples`` check is O(1). For local-name matching we use
``ctx.ln_triple_to_pgius``: its keys are exactly the local-name signatures
of every derived triple, so a single lookup gives the answer.

"""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List

from r2pef.context.canonicalization import local_name
from r2pef.models.evaluation import EvaluationContext

from .base import Scorer, ScoreResult


# Safety caps for very large inputs.
_LOST_SAMPLES_PER_PREDICATE = 5
_SAMPLE_FULL_CAP = 25


class IPScorer(Scorer):
    name = "ip"

    def score(self, ctx: EvaluationContext) -> ScoreResult:
        # De-duplicate source triples 
        unique_triples = list(dict.fromkeys(ctx.source_triples))

        # Display-form lookup: for human-facing diagnostic output 
        display_map = ctx.source_triple_display

        full = 0
        none = 0
        # Capped sample storage
        lost_count_by_predicate: Dict[str, int] = defaultdict(int)
        lost_samples_by_predicate: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        sample_full: List[Dict[str, Any]] = []

        derived = ctx.derived_triples
        ln_index = ctx.ln_triple_to_pgius

        for t in unique_triples:
            s, p, o = t
            if t in derived:
                tier = "full"
            else:
                ln_key = (local_name(s), local_name(p), local_name(o))
                if ln_key in ln_index:
                    tier = "full"
                else:
                    tier = "none"

            if tier == "full":
                full += 1
                if len(sample_full) < _SAMPLE_FULL_CAP:
                    sample_full.append({"triple": list(display_map.get(t, t))})
            else:
                none += 1
                lost_count_by_predicate[p] += 1
                bucket = lost_samples_by_predicate[p]
                if len(bucket) < _LOST_SAMPLES_PER_PREDICATE:
                    bucket.append({"triple": list(display_map.get(t, t))})

        total = len(unique_triples)
        score_val = (full / total) if total > 0 else 0.0

        # Build the "lost" detail block, grouped by predicate (most-lost first).
        lost_groups: List[Dict[str, Any]] = []
        for p, count in sorted(
            lost_count_by_predicate.items(), key=lambda kv: -kv[1]
        ):
            lost_groups.append({
                "predicate": p,
                "count": count,
                "triples": lost_samples_by_predicate.get(p, []),
            })

        return ScoreResult(
            metric=self.name,
            score=score_val,
            counts={"full": full, "none": none, "total": total},
            extras={
                "threshold": self.threshold,
                "passed_threshold": score_val >= self.threshold,
            },
            detail={
                "lost_groups": lost_groups,
                "sample_full": sample_full,
            },
        )