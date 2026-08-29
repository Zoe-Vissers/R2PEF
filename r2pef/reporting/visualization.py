"""Optional matplotlib-based visualisations.

Enabled by ``reporter.visualize: true`` in the pipeline config. When enabled,
this module writes a handful of PNG charts into the run directory. Each
chart is independent and skipped silently if its source data is empty (or
matplotlib is unavailable).

Charts produced
---------------
- ``scores_thresholds.png``       bar chart of IP/IF/IR with threshold markers
- ``thresholds_radar.png``        radar / spider chart of score vs threshold
- ``if_by_role.png``              stacked bar of pass/fail/undef per IF role,
                                   two panels (element-level NR, NPVR;
                                   occurrence-level TMR, ELR, NPKR)
- ``if_realized_kinds.png``       bar of "realized as <X> instead of <ideal>"
                                   grouped by role (top non-idiomatic buckets)
- ``ir_tiers.png``                bar of full/partial/local/dropped counts
- ``ip_lost_predicates.png``      horizontal bar of top-N lost predicates

Everything writes to ``<run_dir>/visualizations/``. Filenames stable across
runs so they can be diffed.
"""
from __future__ import annotations

import logging
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

log = logging.getLogger("r2pef")


# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
PALETTE = {
    "purple":   "#E8DAEF",
    "blue":     "#D6EAF8",
    "green":    "#D5F5E3",
    "orange":   "#FDEBD0",
    "red":      "#FADBD8",
    "lightblue":"#EAF2F8",
    "yellow":   "#FEF9E7",
    "mint":     "#E8F8F5",
    "ink":      "#626567",
}

# Semantic aliases — what each colour represents in this codebase.
C_PASS      = PALETTE["green"]
C_FAIL      = PALETTE["red"]
C_UNDEF     = PALETTE["lightblue"]
C_SCORE     = PALETTE["blue"]
C_SCORE_INK = PALETTE["ink"]
C_THRESHOLD = PALETTE["orange"]   # threshold markers / dashed reference
C_BAR_PRI   = PALETTE["blue"]
C_BAR_ALT   = PALETTE["purple"]

# IR tier palette
C_TIER = {
    "full":    PALETTE["green"],
    "partial": PALETTE["yellow"],
    "local":   PALETTE["orange"],
    "dropped": PALETTE["lightblue"],
}


def _import_matplotlib() -> Optional[Any]:
    """Return ``matplotlib.pyplot`` or ``None`` if matplotlib isn't present."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # noqa: WPS433.
        plt.rcParams.update({
            "axes.edgecolor": C_SCORE_INK,
            "axes.labelcolor": C_SCORE_INK,
            "xtick.color": C_SCORE_INK,
            "ytick.color": C_SCORE_INK,
            "text.color": C_SCORE_INK,
            "axes.titlesize": 11,
            "axes.titlecolor": C_SCORE_INK,
            "axes.linewidth": 0.8,
            "grid.color": "#DDDDDD",
            "grid.alpha": 0.6,
        })
        return plt
    except ImportError:
        log.warning("matplotlib is not installed — skipping visualisations. "
                    "Install with: pip install matplotlib", extra={"phase": "report"})
        return None


def render_all(
    out_dir: Path,
    results: Dict[str, Any],          # metric -> ScoreResult
    thresholds: Dict[str, float],     # metric -> threshold
) -> List[Path]:
    """Render every chart for which data is available. Returns the file list."""
    plt = _import_matplotlib()
    if plt is None:
        return []

    vis_dir = out_dir / "visualizations"
    vis_dir.mkdir(parents=True, exist_ok=True)
    written: List[Path] = []

    # ---- chart 1: scores + thresholds ----------------------------------
    p = _render_score_bars(plt, vis_dir, results, thresholds)
    if p:
        written.append(p)

    # ---- chart 2: radar (threshold vs achievement) ---------------------
    p = _render_radar(plt, vis_dir, results, thresholds)
    if p:
        written.append(p)

    # ---- chart 3: IF distribution by role (element + occurrence in one fig) ----
    if "if" in results:
        by_role = (results["if"].extras or {}).get("by_role") or {}
        if by_role:
            p = _render_if_by_role_combined(plt, vis_dir, by_role)
            if p: written.append(p)

        p = _render_if_realized(plt, vis_dir, results["if"])
        if p:
            written.append(p)

    # ---- chart 4: IR tiers ---------------------------------------------
    if "ir" in results:
        p = _render_ir_tiers(plt, vis_dir, results["ir"])
        if p:
            written.append(p)

    # ---- chart 5: IP lost predicates -----------------------------------
    if "ip" in results:
        p = _render_ip_lost(plt, vis_dir, results["ip"])
        if p:
            written.append(p)

    return written


# ---------------------------------------------------------------------------
# Individual renderers
# ---------------------------------------------------------------------------
def _render_score_bars(plt, vis_dir: Path, results: Dict[str, Any],
                       thresholds: Dict[str, float]) -> Optional[Path]:
    # Display order: IP, IF, IR (preservation → fidelity → identifier).
    metrics = [m for m in ("ip", "if", "ir") if m in results]
    if not metrics:
        return None
    scores = [results[m].score for m in metrics]
    thr = [thresholds.get(m, 0.0) for m in metrics]

    fig, ax = plt.subplots(figsize=(6, 4))
    x = list(range(len(metrics)))
    ax.bar(
        x, scores, width=0.55,
        color=[C_PASS if s >= t else C_FAIL for s, t in zip(scores, thr)],
        edgecolor=C_SCORE_INK, linewidth=0.8,
    )
    # Threshold markers 
    for xi, t in zip(x, thr):
        ax.hlines(t, xi - 0.32, xi + 0.32, colors=C_SCORE_INK,
                  linestyles="dashed", linewidth=1.2)
    ax.set_xticks(x)
    ax.set_xticklabels([m.upper() for m in metrics])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("score")
    ax.set_title("Metric scores vs thresholds")
    for xi, s in zip(x, scores):
        ax.text(xi, s + 0.02, f"{s:.3f}", ha="center", va="bottom", fontsize=9)
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    out = vis_dir / "scores_thresholds.png"
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def _render_radar(plt, vis_dir: Path, results: Dict[str, Any],
                  thresholds: Dict[str, float]) -> Optional[Path]:
    # Display order: IP, IF, IR.
    metrics = [m for m in ("ip", "if", "ir") if m in results]
    if len(metrics) < 3:
        return None  # radar with <3 axes looks pointless
    scores = [results[m].score for m in metrics]
    thr = [thresholds.get(m, 0.0) for m in metrics]

    # Close the polygon by repeating the first value.
    angles = [n / len(metrics) * 2 * math.pi for n in range(len(metrics))]
    angles += [angles[0]]
    scores += [scores[0]]
    thr += [thr[0]]

    fig = plt.figure(figsize=(5.5, 5.5))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([m.upper() for m in metrics])
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0.25", "0.50", "0.75", "1.00"], fontsize=8)

    ax.plot(angles, thr, color=C_SCORE_INK, linewidth=1.5,
            linestyle="dashed", label="threshold")
    ax.fill(angles, thr, alpha=0.4, color=C_THRESHOLD)
    ax.plot(angles, scores, color=C_SCORE_INK, linewidth=1.6, label="score")
    ax.fill(angles, scores, alpha=0.55, color=C_SCORE)
    ax.set_title("Achievement vs thresholds", pad=18)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.10), fontsize=8)
    out = vis_dir / "thresholds_radar.png"
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


_IF_ROLE_ORDER = ["NR", "NPVR", "TMR", "ELR", "NPKR"]
_IF_ELEMENT_ROLES = {"NR", "NPVR"}
_IF_OCC_ROLES = {"TMR", "ELR", "NPKR"}


def _render_if_by_role_combined(
    plt, vis_dir: Path,
    by_role: Dict[str, Dict[str, int]],
) -> Optional[Path]:
    """Single figure, two side-by-side panels: element-level (NR, NPVR) and
    occurrence-level (TMR, ELR, NPKR), stacked-bar pass/fail/undefined.

    Roles within each panel are rendered in the canonical IF order
    (NR, NPVR, TMR, ELR, NPKR). The legend appears once, shared.

    ``by_role`` comes pre-aggregated from the IFScorer's ``extras["by_role"]``
    (it tracks the full input — the detail list itself is capped). Each
    entry is ``{"scored_1": n, "scored_0": n, "undefined": n}``.
    """
    if not by_role:
        return None

    # Partition into element-level vs occurrence-level
    elem_roles = [r for r in _IF_ROLE_ORDER if r in by_role and r in _IF_ELEMENT_ROLES]
    occ_roles  = [r for r in _IF_ROLE_ORDER if r in by_role and r in _IF_OCC_ROLES]
    unknown    = sorted(r for r in by_role
                        if r not in _IF_ELEMENT_ROLES and r not in _IF_OCC_ROLES)

    panels = []
    if elem_roles: panels.append(("Element-level", elem_roles))
    if occ_roles:  panels.append(("Occurrence-level", occ_roles))
    if unknown:    panels.append(("Other", unknown))

    if not panels:
        return None

    # Width scales with total role count; one column per panel.
    total_roles = sum(len(rs) for _, rs in panels)
    fig_w = max(8, 1.2 * total_roles + 2 * len(panels))
    fig, axes = plt.subplots(
        1, len(panels),
        figsize=(fig_w, 4.2),
        gridspec_kw={"width_ratios": [len(rs) for _, rs in panels]},
        sharey=False,
    )
    if len(panels) == 1:
        axes = [axes]

    for ax, (panel_title, roles) in zip(axes, panels):
        pass_ = [by_role[r].get("scored_1", 0) for r in roles]
        fail_ = [by_role[r].get("scored_0", 0) for r in roles]
        undef = [by_role[r].get("undefined", 0) for r in roles]
        x = list(range(len(roles)))
        ax.bar(x, pass_,  color=C_PASS,  edgecolor=C_SCORE_INK, linewidth=0.6, label="pass")
        ax.bar(x, fail_,  bottom=pass_, color=C_FAIL,  edgecolor=C_SCORE_INK, linewidth=0.6, label="fail")
        ax.bar(x, undef,  bottom=[a + b for a, b in zip(pass_, fail_)],
               color=C_UNDEF, edgecolor=C_SCORE_INK, linewidth=0.6, label="undefined")
        ax.set_xticks(x)
        ax.set_xticklabels(roles, rotation=20, ha="right")
        ax.set_title(panel_title, fontsize=10)
        ax.grid(axis="y")
        ax.set_axisbelow(True)
        for xi, (p_, f_, u_) in enumerate(zip(pass_, fail_, undef)):
            total = p_ + f_ + u_
            if total > 0:
                ax.text(xi, total, f" {total}", ha="center", va="bottom", fontsize=8)

    axes[0].set_ylabel("units")
    # Shared legend on the first axis only (avoid duplicate entries).
    axes[-1].legend(loc="upper right", fontsize=8)
    fig.suptitle("IF — units per role", fontsize=11)
    out = vis_dir / "if_by_role.png"
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def _render_if_realized(plt, vis_dir: Path, if_result: Any) -> Optional[Path]:
    """Horizontal bar: top non-idiomatic '(role) realized as X' buckets.

    Aggregates the failing element entries by (role, realized_kinds) so the
    most-common deviations come out in the bar chart, mirroring the
    statements shown in summary.md.
    """
    detail = if_result.detail or {}
    elements = detail.get("elements", [])
    buckets: Counter = Counter()
    for d in elements:
        if d.get("score") != 0:
            continue
        role = d.get("role") or "?"
        realized = d.get("mu_kinds") or []
        if not realized:
            continue
        label = f"{role} → {', '.join(realized)}"
        buckets[label] += 1
    if not buckets:
        return None

    top = buckets.most_common(10)[::-1]  # reverse so largest is on top
    labels, counts = zip(*top)
    fig, ax = plt.subplots(figsize=(8, max(3, 0.35 * len(labels) + 1)))
    y = list(range(len(labels)))
    ax.barh(y, counts, color=C_FAIL, edgecolor=C_SCORE_INK, linewidth=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("units")
    ax.set_title("IF — non-idiomatic encodings (top 10)")
    for yi, c in zip(y, counts):
        ax.text(c, yi, f" {c}", va="center", fontsize=8)
    ax.grid(axis="x")
    ax.set_axisbelow(True)
    out = vis_dir / "if_realized_kinds.png"
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def _render_ir_tiers(plt, vis_dir: Path, ir_result: Any) -> Optional[Path]:
    c = ir_result.counts or {}
    tiers = ["full", "partial", "local"]
    counts = [c.get(t, 0) for t in tiers]
    if sum(counts) == 0:
        return None
    fig, ax = plt.subplots(figsize=(6, 4))
    x = list(range(len(tiers)))
    ax.bar(x, counts,
           color=[C_TIER[t] for t in tiers],
           edgecolor=C_SCORE_INK, linewidth=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(tiers)
    ax.set_ylabel("handles")
    ax.set_title("IR — per-handle tier distribution")
    for xi, c_ in zip(x, counts):
        ax.text(xi, c_, f" {c_}", ha="center", va="bottom", fontsize=9)
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    out = vis_dir / "ir_tiers.png"
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def _render_ip_lost(plt, vis_dir: Path, ip_result: Any) -> Optional[Path]:
    detail = ip_result.detail or {}
    groups = detail.get("lost_groups", [])
    if not groups:
        return None
    top = groups[:15][::-1]
    labels = [g["predicate"] for g in top]
    counts = [g["count"] for g in top]
    fig, ax = plt.subplots(figsize=(8, max(3, 0.35 * len(labels) + 1)))
    y = list(range(len(labels)))
    ax.barh(y, counts, color=C_FAIL, edgecolor=C_SCORE_INK, linewidth=0.6)
    ax.set_yticks(y)
    # Truncate long predicate IRIs so they don't blow out the canvas.
    ax.set_yticklabels(
        [(p if len(p) <= 60 else "…" + p[-58:]) for p in labels], fontsize=7
    )
    ax.set_xlabel("lost source triples")
    ax.set_title("IP — predicates with most missing triples (top 15)")
    for yi, c_ in zip(y, counts):
        ax.text(c_, yi, f" {c_}", va="center", fontsize=8)
    ax.grid(axis="x")
    ax.set_axisbelow(True)
    out = vis_dir / "ip_lost_predicates.png"
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out
