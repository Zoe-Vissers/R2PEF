"""Build and write the evaluation report.

Output files (see spec table)::

    report.json               aggregate scores + fairness verdict
    if_detail.json            per-unit IF
    ip_detail_lost.json       triples with tier `none`, grouped by predicate
    ip_detail_pgius.json      all PGIUs with anchors and derived triples
    ir_detail.json            per-handle tier, score, form, resolved (target-side IR universe)
    role_classification.json  full classifier output
    cpgm.json                 adapter-produced CPGM (adapter mode only;
                              written by pipeline.py before validation)
    summary.md                human-readable narrative
    visualizations/*.png      bar / radar charts (if `visualize: true`)
"""
from __future__ import annotations

import json
import logging
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from r2pef.config.schemas import FairnessConfig, PipelineConfig
from r2pef.models.evaluation import EvaluationContext
from r2pef.scorers.base import ScoreResult

log = logging.getLogger("r2pef")


@dataclass
class FairnessVerdict:
    passed: bool
    details: Dict[str, Any]


# How many concrete examples to print per group in the IF / dropped /
# lost-predicate sections. The spec example asks for "<5 examples>".
_EXAMPLES_PER_GROUP = 5

# Canonical ordering for IF roles in tables, bullet lists, and visualisations.
# Element-level roles first (NR, NPVR), then occurrence-level (TMR, ELR, NPKR).
_IF_ROLE_ORDER = ["NR", "NPVR", "TMR", "ELR", "NPKR"]


def _ordered_roles(roles) -> list:
    """Return ``roles`` in canonical IF order, with any unknown role appended
    in sorted order at the end. Defensive against future role additions or
    upstream classifier variants.
    """
    known = [r for r in _IF_ROLE_ORDER if r in roles]
    extra = sorted(r for r in roles if r not in _IF_ROLE_ORDER)
    return known + extra


class Reporter:
    """Assemble result files. Stateless aside from the output path."""

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------------- API

    def write_all(
        self,
        cfg: PipelineConfig,
        ctx: EvaluationContext,
        results: Dict[str, ScoreResult],
        wall_time_total_s: float,
        cpgm_produced_by_adapter: bool,
        wall_times: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Path]:
        out: Dict[str, Path] = {}

        verdict = self._fairness_verdict(cfg.scorer.fairness, results)
        wall_times = wall_times or {}

        # report.json — emit scores in the canonical order IP, IF, IR
        # (the order the report consumer most often reads them in).
        _SCORE_ORDER = ("ip", "if", "ir")
        ordered_scores = {
            m: results[m].to_dict()
            for m in _SCORE_ORDER if m in results
        }
        # Anything outside the canonical set keeps insertion order at the end.
        for m, r in results.items():
            if m not in _SCORE_ORDER:
                ordered_scores[m] = r.to_dict()

        report = {
            "algorithm": ctx.cpgm.algorithm,
            "cpgm_source": "adapter" if cpgm_produced_by_adapter else "file",
            "wall_time_total_s": wall_time_total_s,
            "wall_time_build_s": ctx.wall_time_build_s,
            "wall_times_s": dict(wall_times),  # per-phase breakdown
            "scores": ordered_scores,
            "fairness": {
                "verdict_passed": verdict.passed,
                **verdict.details,
            },
            "config_summary": {
                "metrics": cfg.evaluation.metrics,
                "thresholds": {
                    "ip": cfg.scorer.ip.threshold,
                    "if": cfg.scorer.if_.threshold,
                    "ir": cfg.scorer.ir.threshold,
                },
            },
        }
        # `report.json` is the most essential output — always write it.
        out["report.json"] = self._write_json("report.json", report)

        # Detail files: each one is guarded so a single OOM (e.g. on a
        # huge role_classification dump) doesn't drop the others.
        if "if" in results:
            self._safe_write_json(out, "if_detail.json", results["if"].detail)
        if "ip" in results:
            self._safe_write_json(
                out, "ip_detail_lost.json",
                {"lost_groups": results["ip"].detail.get("lost_groups", [])},
            )
            self._safe_write_json(out, "ip_detail_pgius.json", _pgiu_detail(ctx))
        if "ir" in results:
            self._safe_write_json(out, "ir_detail.json", results["ir"].detail)

        self._safe_write_json(
            out, "role_classification.json",
            _serialise_role(ctx.role_classification),
        )

        # NOTE: cpgm.json is written by pipeline.obtain_cpgm() in adapter
        # mode, *before* schema validation. Not re-written here.
        if cpgm_produced_by_adapter:
            cpgm_path = self.output_dir / "cpgm.json"
            if cpgm_path.exists():
                out["cpgm.json"] = cpgm_path

        # ---- visualisations (optional) ----------------------------------
        vis_paths: List[Path] = []
        if cfg.reporter.visualize:
            try:
                from r2pef.reporting.visualization import render_all
                thresholds = {
                    "if": cfg.scorer.if_.threshold,
                    "ip": cfg.scorer.ip.threshold,
                    "ir": cfg.scorer.ir.threshold,
                }
                vis_paths = render_all(self.output_dir, results, thresholds)
                if vis_paths:
                    log.info("wrote %d visualisation(s) to %s",
                             len(vis_paths), self.output_dir / "visualizations",
                             extra={"phase": "report"})
            except Exception as exc:  # noqa: BLE001
                # Don't let a chart failure abort the whole report — just log.
                log.warning("visualisation step failed: %s", exc,
                            extra={"phase": "report"})

        # summary.md — written LAST so it can list visualisations
        try:
            out["summary.md"] = self._write_text(
                "summary.md",
                _summary_markdown(
                    cfg, ctx, results, verdict, wall_time_total_s, vis_paths,
                    wall_times, cpgm_produced_by_adapter,
                ),
            )
        except Exception as exc:  # noqa: BLE001
            log.warning("failed to write summary.md: %s", exc,
                        extra={"phase": "report"})

        return out

    # ------------------------------------------------------------- helpers

    def _write_json(self, name: str, payload: Any) -> Path:
        path = self.output_dir / name
        with path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=False, default=str)
        return path

    def _safe_write_json(
        self, out: Dict[str, Path], name: str, payload: Any
    ) -> None:
        """Best-effort JSON write — log + skip on failure, don't propagate.

        Used for the secondary detail files. ``report.json`` itself is
        written unguarded so the one essential file's failure surfaces
        immediately.
        """
        try:
            out[name] = self._write_json(name, payload)
        except Exception as exc:  # noqa: BLE001
            log.warning("failed to write %s: %s", name, exc,
                        extra={"phase": "report"})

    def _write_text(self, name: str, content: str) -> Path:
        path = self.output_dir / name
        with path.open("w", encoding="utf-8") as fh:
            fh.write(content)
        return path

    @staticmethod
    def _fairness_verdict(
        cfg: FairnessConfig, results: Dict[str, ScoreResult]
    ) -> FairnessVerdict:
        details: Dict[str, Any] = {"mandatory": {}, "optional": {}}
        passed = True
        for m in cfg.mandatory_metrics:
            r = results.get(m)
            ok = bool(r and r.extras.get("passed_threshold", False))
            details["mandatory"][m] = {"passed": ok, "score": r.score if r else None}
            if not ok:
                passed = False
        for m in cfg.optional_metrics:
            r = results.get(m)
            details["optional"][m] = {
                "passed": bool(r and r.extras.get("passed_threshold", False)),
                "score": r.score if r else None,
            }
        return FairnessVerdict(passed=passed, details=details)


# ---------------------------------------------------------------------------
# Detail-payload helpers
# ---------------------------------------------------------------------------
def _pgiu_detail(ctx: EvaluationContext) -> Dict[str, Any]:
    """Serialise every PGIU together with its anchor handle and the
    source triple it derives. Each entry is one PGIU; the file's top-
    level ``pgius`` key reflects this. The set of *unique* derived
    triples is the projection of the ``triple`` field across this list
    (after object-variant expansion, performed at scoring time, not
    in this serialisation).
    """
    items = []
    for u in ctx.pgius:
        items.append(
            {
                "kind": u.kind,
                "anchor": list(u.anchor),
                "triple": list(u.triple),
            }
        )
    return {"pgius": items, "count": len(items)}


def _serialise_role(role: Dict[str, Any]) -> Dict[str, Any]:
    """Make the role classifier dict JSON-safe.

    The classifier emits ``occurrence_roles`` with plain integer keys (one
    per source triple). JSON serialises those as strings, but ``json.dump``
    handles int-keyed dicts natively, so we pass the dict through unchanged.

    """
    out: Dict[str, Any] = {}
    for k, v in role.items():
        if k == "occurrence_roles" and isinstance(v, dict):
            occ_out: Dict[str, Any] = {str(tk): tv for tk, tv in v.items()}
            out[k] = occ_out
        else:
            out[k] = v
    return out


# ---------------------------------------------------------------------------
# summary.md
# ---------------------------------------------------------------------------
def _fmt_int(n: int) -> str:
    """1234567 → '1,234,567' — thousands separator for readability."""
    return f"{n:,}"


# ---------------------------------------------------------------------------
# Structural overview helpers
# ---------------------------------------------------------------------------
# Two compact summaries computed from data already in the EvaluationContext

RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"


def _source_structural_summary(ctx: Any) -> Dict[str, Any]:
    """One-pass structural digest of the source RDF.

    Returned shape::

        {
          "triples":    int,
          "subjects":   int,
          "predicates": int,
          "objects_iri":     int,
          "objects_literal": int,
          "objects_bnode":   int,
          "subjects_with_rdf_type":    int,
          "subjects_without_rdf_type": int,
        }
    """
    subjects: set = set()
    predicates: set = set()
    obj_iri = obj_lit = obj_bn = 0
    typed_subjects: set = set()

    for s, p, o in ctx.source_triples:
        subjects.add(s)
        predicates.add(p)
        if isinstance(o, str) and o.startswith('"'):
            obj_lit += 1
        elif isinstance(o, str) and o.startswith("_:"):
            obj_bn += 1
        else:
            obj_iri += 1
        if p == RDF_TYPE:
            typed_subjects.add(s)

    return {
        "triples":    len(ctx.source_triples),
        "subjects":   len(subjects),
        "predicates": len(predicates),
        "objects_iri":     obj_iri,
        "objects_literal": obj_lit,
        "objects_bnode":   obj_bn,
        "subjects_with_rdf_type":    len(typed_subjects),
        "subjects_without_rdf_type": len(subjects) - len(typed_subjects),
    }


def _cpgm_structural_summary(ctx: Any) -> Dict[str, Any]:
    """One-pass structural digest of the CPGM.

    Reports:
      - node count broken down by node_ref.form (and synthetic)
      - edge count split into labelled vs generic-edge
      - property total
    """
    node_buckets = {"full_iri": 0, "namespace_plus_local": 0,
                    "local_only": 0, "literal": 0, "synthetic": 0}
    for n in ctx.cpgm.nodes:
        ref = n.node_ref
        if ref.synthetic:
            node_buckets["synthetic"] += 1
            continue
        form = ref.form.value if ref.form is not None else None
        if form in node_buckets:
            node_buckets[form] += 1
        else:
            # Unknown form — bucket as synthetic for accounting; should not happen
            # given the schema enum, but defensive.
            node_buckets["synthetic"] += 1

    edges_total = len(ctx.cpgm.relations)
    edges_generic = sum(
        1 for r in ctx.cpgm.relations
        if r.labels and all(lab.label_ref.synthetic for lab in r.labels)
    )
    edges_labelled = edges_total - edges_generic

    prop_count = sum(len(n.properties) for n in ctx.cpgm.nodes) \
               + sum(len(r.properties) for r in ctx.cpgm.relations)

    return {
        "nodes_total":  len(ctx.cpgm.nodes),
        "nodes_by_form": node_buckets,
        "edges_total":  edges_total,
        "edges_labelled": edges_labelled,
        "edges_generic":  edges_generic,
        "properties_total": prop_count,
    }


# ---------------------------------------------------------------------------
# IP detail re-projection helpers
# ---------------------------------------------------------------------------
# These add new groupings (by expected PGIU type, by subject) computed from
# the existing IP detail + role classification. 

# Mapping from occurrence-level role → the PGIU kind that *would have*
# covered the triple had it been encoded idiomatically.
_ROLE_TO_EXPECTED_PGIU_KIND = {
    "TMR":  "Label",
    "NPKR": "Property",
    "ELR":  "Edge",
}


def _build_triple_role_index(ctx: Any) -> Dict[Tuple[str, str, str], str]:
    """Map (s, p, o) → occurrence role, using the role classifier's output.

    Built once per report, used to project lost-triple groupings by the
    PGIU kind that *would have* covered each lost triple had the encoding
    produced one. Lost triples have no PGIU by definition — the kind here
    is the framework's expectation, not an observation.
    """
    occ = (ctx.role_classification or {}).get("occurrence_roles") or {}
    out: Dict[Tuple[str, str, str], str] = {}
    for _idx, info in occ.items():
        if not isinstance(info, dict):
            continue
        triple = info.get("triple")
        role = info.get("role")
        if triple is None or role is None:
            continue
        out[tuple(triple)] = role
    return out


def _lost_by_expected_kind(
    lost_groups: List[Dict[str, Any]],
    triple_role_index: Dict[Tuple[str, str, str], str],
) -> Dict[str, int]:
    """Aggregate lost-triple counts by *expected* PGIU kind.

    The "expected PGIU kind" is what the framework would have produced
    had the encoding been idiomatic for the triple's occurrence role.
    Since these triples are lost, no PGIU actually exists for them —
    the kind is purely the framework's expectation.

    Returns a dict keyed by ``"Label" | "Property" | "Edge" | "Unknown"``.
    "Unknown" covers any lost triple whose source role cannot be looked
    up (defensive — should be rare).
    """
    counts: Dict[str, int] = {"Label": 0, "Property": 0, "Edge": 0, "Unknown": 0}
    for g in lost_groups:
        # Each group is per-predicate. To classify by role each sample triple 
        # is looked up; assumption is that every triple with the same predicate 
        # has the same occurrence role which conforms in most of real datasets).
        # Sample-classification on the group's first triple as a heuristic
        examples = g.get("triples") or []
        if not examples:
            counts["Unknown"] += g.get("count", 0)
            continue
        first_t = tuple(examples[0].get("triple") or ())
        role = triple_role_index.get(first_t)
        kind = _ROLE_TO_EXPECTED_PGIU_KIND.get(role, "Unknown") if role else "Unknown"
        counts[kind] += g.get("count", 0)
    return counts


def _lost_by_subject(
    lost_groups: List[Dict[str, Any]],
    cap: int = 10,
) -> List[Tuple[str, int, List[str]]]:
    """Aggregate lost triples by subject. Returns top-``cap`` subjects.
    """
    counts: Dict[str, int] = defaultdict(int)
    examples: Dict[str, List[str]] = defaultdict(list)
    for g in lost_groups:
        for ex in g.get("triples") or []:
            t = ex.get("triple")
            if not t:
                continue
            subj = t[0]
            counts[subj] += 1
            if len(examples[subj]) < 3:
                # Store one predicate-object pair as a peek; subject is the key.
                examples[subj].append(f"{t[1]} → {_truncate(str(t[2]), 200)}")

    top = sorted(counts.items(), key=lambda kv: -kv[1])[:cap]
    return [(subj, n, examples[subj]) for subj, n in top]


def _ascii_bar(score: float, threshold: float, width: int = 28) -> str:
    """Render a single ASCII progress bar showing score vs threshold.

    Example output (width=28, score=0.83, threshold=0.90):

        [██████████████████████░░░░░░] 0.830 / 0.900 ✗

    The threshold position is marked with ``|``.
    """
    score = max(0.0, min(1.0, float(score)))
    threshold = max(0.0, min(1.0, float(threshold)))
    filled = int(round(score * width))
    bar = ["█"] * filled + ["░"] * (width - filled)
    thr_pos = min(width - 1, int(round(threshold * width)))
    # Mark the threshold by replacing one char with "│".
    if 0 <= thr_pos < width:
        bar[thr_pos] = "│"
    flag = "✓" if score >= threshold else "✗"
    return f"[{''.join(bar)}] {score:.3f} / {threshold:.3f} {flag}"


def _truncate(s: str, limit: int = 140) -> str:
    s = str(s)
    return s if len(s) <= limit else s[: limit - 1] + "…"


def _aggregate_if_failures(
    elements: Iterable[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Group failing IF element entries by (role, realized_kinds).

    Returns a list of dicts shaped like::

        {"role": "NR",
         "realized": ["literal_node", "prop_value"],
         "idiomatic": "node",
         "count": 3165,
         "examples": ["http://example.org/X", …]}

    Sorted by count descending.
    """
    buckets: Dict[Tuple[str, Tuple[str, ...]], Dict[str, Any]] = {}
    for d in elements:
        if d.get("score") != 0:
            continue
        role = d.get("role") or "?"
        realized = tuple(d.get("mu_kinds") or [])
        key = (role, realized)
        b = buckets.setdefault(
            key,
            {
                "role": role,
                "realized": list(realized),
                "idiomatic": d.get("idiomatic_kind", ""),
                "count": 0,
                "examples": [],
                "cpgm_value_examples": [],
            },
        )
        b["count"] += 1
        if len(b["examples"]) < _EXAMPLES_PER_GROUP:
            b["examples"].append(d.get("unit"))
            cv = d.get("cpgm_values") or []
            if cv:
                pick = next(
                    (v for v in cv if v.get("form") == "literal"),
                    cv[0],
                )
                b["cpgm_value_examples"].append(pick)
            else:
                b["cpgm_value_examples"].append(None)
    return sorted(buckets.values(), key=lambda x: -x["count"])


def _aggregate_if_occurrence_failures(
    occurrences: Iterable[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Same shape as the element aggregation but for occurrence-level."""
    buckets: Dict[Tuple[str, Tuple[str, ...]], Dict[str, Any]] = {}
    for d in occurrences:
        if d.get("score") != 0:
            continue
        role = d.get("role") or "?"
        kinds = tuple(d.get("pgiu_kinds") or [])
        key = (role, kinds)
        b = buckets.setdefault(
            key,
            {
                "role": role,
                "realized": list(kinds),
                "idiomatic": d.get("idiomatic_kind", ""),
                "count": 0,
                "examples": [],
            },
        )
        b["count"] += 1
        if len(b["examples"]) < _EXAMPLES_PER_GROUP:
            b["examples"].append(d.get("triple"))
    return sorted(buckets.values(), key=lambda x: -x["count"])


def _aggregate_if_undefined(
    elements: Iterable[Dict[str, Any]],
    occurrences: Iterable[Dict[str, Any]],
) -> Dict[str, Any]:
    """Count + sample undefined (dropped / unmapped) IF units, grouped by role."""
    by_role_elem: Dict[str, List[Any]] = defaultdict(list)
    by_role_occ:  Dict[str, List[Any]] = defaultdict(list)
    n_elem = n_occ = 0
    for d in elements:
        if d.get("score") is None:
            role = d.get("role") or "?"
            n_elem += 1
            if len(by_role_elem[role]) < _EXAMPLES_PER_GROUP:
                by_role_elem[role].append(d.get("unit"))
    for d in occurrences:
        if d.get("score") is None:
            role = d.get("role") or "?"
            n_occ += 1
            if len(by_role_occ[role]) < _EXAMPLES_PER_GROUP:
                by_role_occ[role].append(d.get("triple"))
    return {
        "elements_total": n_elem,
        "occurrences_total": n_occ,
        "by_role_elements": dict(by_role_elem),
        "by_role_occurrences": dict(by_role_occ),
    }


def _summary_markdown(
    cfg: PipelineConfig,
    ctx: EvaluationContext,
    results: Dict[str, ScoreResult],
    verdict: FairnessVerdict,
    wall_time_total_s: float,
    vis_paths: List[Path],
    wall_times: Optional[Dict[str, float]] = None,
    cpgm_produced_by_adapter: bool = True,
) -> str:
    L: List[str] = []
    wall_times = wall_times or {}
    if cpgm_produced_by_adapter:
        L.append(f"# r2pef report — {ctx.cpgm.algorithm}")
    else:
        L.append("# r2pef report — CPGM file")
    L.append("")
    L.append(f"_Generated {time.strftime('%Y-%m-%d %H:%M:%S')}_")
    L.append("")

    # ---------------- Overview ----------------
    L.append("## Overview")
    L.append("")
    L.append(f"- Source RDF: `{cfg.source_rdf.path}`")
    L.append(f"- Source triples: **{_fmt_int(len(ctx.source_triples))}**")
    L.append(
        f"- CPGM nodes: **{_fmt_int(len(ctx.cpgm.nodes))}** ; "
        f"relations: **{_fmt_int(len(ctx.cpgm.relations))}**"
    )
    L.append(f"- Derived triples (|derived_triples(C)|): **{_fmt_int(len(ctx.derived_triples))}**")
    L.append("")

    # ---------------- Structural overview ----------------
    src_s = _source_structural_summary(ctx)
    cpgm_s = _cpgm_structural_summary(ctx)

    L.append("## Structural overview")
    L.append("")
    L.append("**Source RDF**")
    L.append("")
    L.append(
        f"- {_fmt_int(src_s['triples'])} triples, "
        f"{_fmt_int(src_s['subjects'])} unique subjects, "
        f"{_fmt_int(src_s['predicates'])} unique predicates"
    )
    L.append(
        f"- Object positions: "
        f"{_fmt_int(src_s['objects_iri'])} IRI, "
        f"{_fmt_int(src_s['objects_literal'])} literal, "
        f"{_fmt_int(src_s['objects_bnode'])} blank node"
    )
    if src_s["subjects"] > 0:
        typed = src_s["subjects_with_rdf_type"]
        untyped = src_s["subjects_without_rdf_type"]
        typed_pct = (typed / src_s["subjects"] * 100)
        L.append(
            f"- Subjects with ≥1 `rdf:type`: **{_fmt_int(typed)}** "
            f"({typed_pct:.1f}%) ; without `rdf:type`: "
            f"**{_fmt_int(untyped)}**"
        )
    L.append("")

    L.append("**CPGM**")
    L.append("")
    nbf = cpgm_s["nodes_by_form"]
    node_breakdown_parts = []
    for label, key in (("full_iri", "full_iri"),
                        ("namespace_plus_local", "namespace_plus_local"),
                        ("local_only", "local_only"),
                        ("literal-form", "literal"),
                        ("synthetic", "synthetic")):
        if nbf[key] > 0:
            node_breakdown_parts.append(f"{_fmt_int(nbf[key])} {label}")
    L.append(
        f"- {_fmt_int(cpgm_s['nodes_total'])} nodes "
        f"({', '.join(node_breakdown_parts) if node_breakdown_parts else 'all synthetic'})"
    )
    if cpgm_s["edges_total"] > 0:
        L.append(
            f"- {_fmt_int(cpgm_s['edges_total'])} edges "
            f"({_fmt_int(cpgm_s['edges_labelled'])} labelled, "
            f"{_fmt_int(cpgm_s['edges_generic'])} generic-edge)"
        )
    else:
        L.append("- 0 edges")
    L.append(f"- {_fmt_int(cpgm_s['properties_total'])} properties total")
    L.append("")

    # ---------------- Performance / wall time ----------------
    L.append("## Performance")
    L.append("")
    L.append("| Phase | Wall time |")
    L.append("|---|---|")

    _phase_order = [
        ("config",     "config load"),
        ("cpgm",       "CPGM acquisition"),
        ("classify",   "role classification"),
        ("context",    "context build (R, R⁻¹, PGIUs)"),
        ("score_if",   "IF scoring"),
        ("score_ip",   "IP scoring"),
        ("score_ir",   "IR scoring"),
        ("report",     "report write"),
    ]
    known: set = set()
    for key, label in _phase_order:
        if key in wall_times:
            L.append(f"| {label} | {wall_times[key]:.3f} s |")
            known.add(key)
    leftover = {k: v for k, v in wall_times.items()
                if k not in known and k != "total"}
    if leftover:
        L.append(f"| other | {sum(leftover.values()):.3f} s |")
    L.append(f"| **total** | **{wall_time_total_s:.3f} s** |")
    L.append("")

    # ---------------- Scores with ASCII bars ----------------
    L.append("## Scores vs thresholds")
    L.append("")
    L.append("```")
    for m in ("ip", "if", "ir"):
        if m not in results:
            continue
        r = results[m]
        thr = r.extras.get("threshold", 0.0)
        L.append(f"{m.upper():3}  {_ascii_bar(r.score, thr)}")
    L.append("```")
    L.append("")
    L.append("_The `│` marker on each bar shows the configured threshold._")
    L.append("")

    # ---------------- Score detail table ----------------
    L.append("| Metric | Score | Threshold | Passed | Notes |")
    L.append("|---|---|---|---|---|")
    for m in ("ip", "if", "ir"):
        if m not in results:
            continue
        r = results[m]
        thr = r.extras.get("threshold", 0.0)
        note = ""
        if m == "if":
            note = f"undef rate {r.extras.get('undefined_rate', 0):.2%}"
        elif m == "ip":
            c = r.counts
            note = f"{_fmt_int(c.get('full', 0))}/{_fmt_int(c.get('total', 0))} full"
        elif m == "ir":
            c = r.counts
            note = f"universe={_fmt_int(c.get('universe', 0))}"
        passed = r.extras.get("passed_threshold", False)
        L.append(
            f"| {m.upper()} | {r.score:.4f} | {thr:.4f} | "
            f"{'✓' if passed else '✗'} | {note} |"
        )
    L.append("")

    # ---------------- Fairness verdict ----------------
    L.append("## Fairness verdict")
    L.append("")
    L.append(f"**Passed:** {'yes' if verdict.passed else 'no'}")
    L.append("")
    if verdict.details["mandatory"]:
        L.append("Mandatory metrics:")
        for m, info in verdict.details["mandatory"].items():
            score = info["score"]
            score_s = "—" if score is None else f"{score:.4f}"
            L.append(f"- {m.upper()}: {score_s} — {'pass' if info['passed'] else 'FAIL'}")
        L.append("")
    if verdict.details["optional"]:
        L.append("Optional metrics:")
        for m, info in verdict.details["optional"].items():
            s = info["score"]
            L.append(
                f"- {m.upper()}: {('—' if s is None else f'{s:.4f}')} "
                f"— {'pass' if info['passed'] else 'fail'}"
            )
        L.append("")

    # ---------------- IP: top lost predicates ----------------
    if "ip" in results:
        groups = results["ip"].detail.get("lost_groups", [])
        if groups:
            L.append("## Lost triples (IP)")
            L.append("")

            # By expected PGIU type (a re-projection of the same data).
            triple_role_idx = _build_triple_role_index(ctx)
            by_kind = _lost_by_expected_kind(groups, triple_role_idx)
            kind_total = sum(by_kind.values())
            if kind_total > 0:
                L.append("### By expected PGIU type")
                L.append("")
                L.append(
                    "_These triples have no PGIU by definition — they are "
                    "lost. The \"expected PGIU type\" is the kind the "
                    "framework would have produced had the triple been "
                    "encoded idiomatically for its source role (derived "
                    "from the role classifier's output)._"
                )
                L.append("")
                L.append("| Expected PGIU type | Lost triples | Share |")
                L.append("|---|---|---|")
                for kind in ("Label", "Property", "Edge", "Unknown"):
                    n = by_kind.get(kind, 0)
                    if n == 0:
                        continue
                    pct = n / kind_total * 100
                    L.append(f"| {kind} | {_fmt_int(n)} | {pct:.1f}% |")
                L.append("")

            # Per-subject grouping (capped, may under-report due to per-
            # predicate sample cap).
            by_subj = _lost_by_subject(groups, cap=10)
            if by_subj:
                L.append("### By source subject (sampled)")
                L.append("")
                L.append(
                    "_Subjects ranked by lost-triple count across all "
                    "predicates. Counts here are computed from the per-"
                    "predicate samples — when a predicate's losses exceed "
                    "its sample cap (5), the per-subject counts shown "
                    "are lower bounds. Useful for spotting subjects that "
                    "are missing across multiple predicates at once._"
                )
                L.append("")
                for subj, n, preds_objs in by_subj:
                    L.append(
                        f"- `{_truncate(subj, 200)}` — "
                        f"**{_fmt_int(n)}** triple(s) in sample"
                    )
                    for po in preds_objs:
                        L.append(f"    - `{_truncate(po, 400)}`")
                L.append("")

            # Per-predicate grouping (the original).
            L.append("### By predicate")
            L.append("")
            L.append("Predicates ranked by number of source triples with no PGIU match:")
            L.append("")
            for g in groups[:10]:
                L.append(f"- `{g['predicate']}` — **{_fmt_int(g['count'])}** triple(s)")
                for sample in g["triples"][:_EXAMPLES_PER_GROUP]:
                    triple = sample.get("triple") or []
                    if len(triple) == 3:
                        s, _p, o = triple
                        L.append(
                            f"    - `{_truncate(str(s), 200)}` "
                            f"→ `{_truncate(str(o), 400)}`"
                        )
                    else:
                        L.append(f"    - `{_truncate(str(triple), 600)}`")
            L.append("")

    # ---------------- IF: non-idiomatic encodings ----------------
    if "if" in results:
        det = results["if"].detail or {}
        elements = det.get("elements", [])
        occurrences = det.get("occurrences", [])

        by_role: Dict[str, Dict[str, int]] = (
            results["if"].extras.get("by_role") or {}
        )

        # Warn loudly when the aggregate hides a 100%-undefined situation.
        if results["if"].extras.get("all_undefined"):
            L.append("> ⚠️ **All IF units were undefined.** The score 0.0000 "
                     "above does not mean every encoding was non-idiomatic — "
                     "it means no unit could be scored (μ_e empty / no PGIU "
                     "coverage). Check whether the source RDF and the CPGM "
                     "share a common identifier surface.")
            L.append("")

        if by_role:
            L.append("## IF — units per role")
            L.append("")
            L.append("| Role | Pass | Fail | Undef | %-passed |")
            L.append("|---|---|---|---|---|")
            for role in _ordered_roles(by_role.keys()):
                c = by_role[role]
                scored = c["scored_1"] + c["scored_0"]
                pct = (c["scored_1"] / scored * 100) if scored > 0 else None
                pct_s = f"{pct:.1f}%" if pct is not None else "—"
                L.append(
                    f"| {role} | {_fmt_int(c['scored_1'])} | "
                    f"{_fmt_int(c['scored_0'])} | {_fmt_int(c['undefined'])} | {pct_s} |"
                )
            L.append("")

        groups = _aggregate_if_failures(elements)
        occ_groups = _aggregate_if_occurrence_failures(occurrences)
        undef = _aggregate_if_undefined(elements, occurrences)

        cap = results["if"].extras.get("detail_truncated_at")
        if cap and (len(elements) >= cap or len(occurrences) >= cap):
            L.append(
                f"_Detail lists are capped at {_fmt_int(cap)} entries per "
                f"bucket (pass / fail / undef) for memory safety. The "
                f"aggregate counts above use the full input._"
            )
            L.append("")

        if groups or occ_groups:
            L.append("## Non-idiomatic encodings (IF)")
            L.append("")

        if groups:
            L.append("### Elements")
            L.append("")
            L.append(
                "_When multiple realizations are listed, the source element "
                "is encoded in several CPGM locations at once (e.g. once as a "
                "literal-form node and separately as a property value) — "
                "these are independent handles, not a nesting. The role "
                "fails if **any** of those locations uses a non-idiomatic "
                "kind, even when other locations use the idiomatic one._"
            )
            L.append("")
            for g in groups[:10]:
                realized_kinds = [f"`{r}`" for r in g["realized"]]
                if not realized_kinds:
                    realized = "_(none)_"
                elif len(realized_kinds) == 1:
                    realized = realized_kinds[0]
                else:
                    realized = ", ".join(realized_kinds[:-1]) + " and " + realized_kinds[-1]
                ideal = f"`{g['idiomatic']}`" if g["idiomatic"] else "_idiomatic_"
                L.append(
                    f"- **{g['role']}** → realized as {realized} instead of "
                    f"{ideal} (**{_fmt_int(g['count'])} units**)"
                )
                for ex, cv in zip(g["examples"], g.get("cpgm_value_examples") or []):
                    line = f"    - `{_truncate(ex)}`"
                    if cv:
                        loc = cv.get("location") or ""
                        form = cv.get("form") or ""
                        kind = cv.get("kind") or ""
                        raw = cv.get("raw")
                        if raw is not None and raw != ex:
                            extras_bits = []
                            if kind:
                                extras_bits.append(f"handle=`{kind}`")
                            if form:
                                extras_bits.append(f"form=`{form}`")
                            if loc:
                                extras_bits.append(f"at `{loc}`")
                            extras_bits.append(f"raw=`{_truncate(str(raw), 60)}`")
                            line += " — " + ", ".join(extras_bits)
                    L.append(line)
            L.append("")

        if occ_groups:
            L.append("### Occurrences (triples)")
            L.append("")
            L.append(
                "_For occurrences, \"realized as X\" means the source triple "
                "was reconstructed by an X PGIU rather than the idiomatic kind "
                "for the role._"
            )
            L.append("")
            for g in occ_groups[:10]:
                realized = ", ".join(f"`{r}`" for r in g["realized"]) or "_(none)_"
                ideal = f"`{g['idiomatic']}`" if g["idiomatic"] else "_idiomatic_"
                L.append(
                    f"- **{g['role']}** → realized as {realized} instead of "
                    f"{ideal} (**{_fmt_int(g['count'])} occurrence(s)**)"
                )
                if g["examples"]:
                    for ex in g["examples"]:
                        L.append(f"    - `{_truncate(str(ex))}`")
            L.append("")

        # Dropped / undefined units 
        if undef["elements_total"] or undef["occurrences_total"]:
            L.append("### Dropped / undefined units (IF)")
            L.append("")
            L.append(
                f"- Elements without a μ_e match (or with no scorable kind set): "
                f"**{_fmt_int(undef['elements_total'])}**"
            )
            L.append(
                f"- Occurrences with no covering PGIU: "
                f"**{_fmt_int(undef['occurrences_total'])}**"
            )
            L.append("")
            if undef["by_role_elements"]:
                L.append("Element-level examples (per role):")
                ordered = _ordered_roles(undef["by_role_elements"].keys())
                for role in ordered:
                    samples = undef["by_role_elements"][role]
                    L.append(f"- **{role}** ({_fmt_int(len(samples))} shown)")
                    for s in samples:
                        L.append(f"    - `{_truncate(s)}`")
                L.append("")
            if undef["by_role_occurrences"]:
                L.append("Occurrence-level examples (per role):")
                ordered = _ordered_roles(undef["by_role_occurrences"].keys())
                for role in ordered:
                    samples = undef["by_role_occurrences"][role]
                    L.append(f"- **{role}** ({_fmt_int(len(samples))} shown)")
                    for s in samples:
                        L.append(f"    - `{_truncate(str(s))}`")
                L.append("")

    # ---------------- IR: tier distribution ----------------
    if "ir" in results:
        c = results["ir"].counts
        L.append("## Identifier retention tier distribution (IR)")
        L.append("")
        L.append(
            f"- full: **{_fmt_int(c.get('full', 0))}** ; "
            f"partial: **{_fmt_int(c.get('partial', 0))}** ; "
            f"local: **{_fmt_int(c.get('local', 0))}** "
            f"/ universe {_fmt_int(c.get('universe', 0))}"
        )
        L.append("")

        # Construct-group breakdown 
        groups = results["ir"].detail.get("by_construct_group", [])
        if groups:
            L.append("### By construct group")
            L.append("")
            L.append(
                "`Full` totals are further split into `direct` (handle "
                "stored a full IRI natively, i.e. `form = full_iri`) and "
                "`exp.` (namespace-shortform expanded to a full IRI by the "
                "adapter, i.e. `form = namespace_plus_local` with `://` in "
                "`resolved`). The split is purely diagnostic — the IR score "
                "treats both as `full` (weight 1.0)."
            )
            L.append("")
            L.append("| Group | Full | direct | exp. | Partial | Local | Total | Score |")
            L.append("|---|---|---|---|---|---|---|---|")
            for g in groups:
                L.append(
                    f"| `{g['group']}` | "
                    f"{_fmt_int(g['full'])} | "
                    f"{_fmt_int(g.get('full_direct', 0))} | "
                    f"{_fmt_int(g.get('full_expanded', 0))} | "
                    f"{_fmt_int(g['partial'])} | "
                    f"{_fmt_int(g['local'])} | "
                    f"{_fmt_int(g['total'])} | "
                    f"{g['score']:.4f} |"
                )
            L.append("")

        # Per-tier examples
        partial_samples = [
            d for d in results["ir"].detail.get("handles", []) if d.get("tier") == "partial"
        ][:_EXAMPLES_PER_GROUP]
        local_samples = [
            d for d in results["ir"].detail.get("handles", []) if d.get("tier") == "local"
        ][:_EXAMPLES_PER_GROUP]
        if partial_samples:
            L.append("Partial-tier handle examples (namespace shortform kept, full IRI not reconstructable):")
            for d in partial_samples:
                L.append(f"- `{_truncate(d['handle'])}` resolved=`{_truncate(str(d.get('resolved')))}` form=`{d.get('form')}`")
            L.append("")
        if local_samples:
            L.append("Local-tier handle examples (bare local name, namespace discarded):")
            for d in local_samples:
                L.append(f"- `{_truncate(d['handle'])}` resolved=`{_truncate(str(d.get('resolved')))}` form=`{d.get('form')}`")
            L.append("")

    # ---------------- Visualisations ----------------
    if vis_paths:
        L.append("## Visualisations")
        L.append("")
        for p in vis_paths:
            rel = p.name if p.parent.name != "visualizations" else f"visualizations/{p.name}"
            L.append(f"![{p.stem}]({rel})")
            L.append("")

    return "\n".join(L) + "\n"