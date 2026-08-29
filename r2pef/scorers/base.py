"""Shared interface for the three metric scorers.

Each scorer reads the EvaluationContext and produces a structured result.
Results are simple dict-like objects so the reporter can serialise them
without any per-metric special-casing.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict

from r2pef.models.evaluation import EvaluationContext


@dataclass
class ScoreResult:
    """A single scorer's output."""

    metric: str
    score: float                       # the aggregate value in [0, 1]
    counts: Dict[str, int] = field(default_factory=dict)
    extras: Dict[str, Any] = field(default_factory=dict)
    # Per-unit detail; the reporter writes these to <metric>_detail*.json.
    detail: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric": self.metric,
            "score": self.score,
            "counts": self.counts,
            "extras": self.extras,
        }


class Scorer(ABC):
    """Common base. Scorers are independent — order does not matter."""

    name: str

    def __init__(self, threshold: float = 0.9) -> None:
        self.threshold = threshold

    @abstractmethod
    def score(self, ctx: EvaluationContext) -> ScoreResult: ...
