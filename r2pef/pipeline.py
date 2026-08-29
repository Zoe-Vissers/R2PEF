"""Pipeline orchestrator + CLI.

Invocation::

    python3 -m r2pef.pipeline pipeline_config.yaml

Order of operations:

1. Load + validate the YAML config (Pydantic).
2. Obtain the CPGM — either by loading a precomputed file (validated against
   ``cpgm.schema.json``) or by invoking the adapter named in the config.
3. Run the role classifier on the source RDF.
4. Build the shared EvaluationContext (R, R⁻¹, PGIUs; apply derive to obtain derived_triples(C)).
5. Run the enabled scorers (IF, IP, IR) independently.
6. The reporter writes all output files. In adapter mode the reporter also
   serialises the produced CPGM to ``<run_dir>/cpgm.json``.

The role classifier is **mandatory**. If
``classification.role_classifier.classify`` cannot be imported or raises at
runtime, the pipeline aborts with the original traceback — it never falls
back to a stub.

Run-directory naming
--------------------
``reporter.output_dir`` is treated as a *base directory*. The pipeline
appends a run-specific subdirectory inside it:

- Adapter mode: ``<base>/<algorithm>__<source_rdf_stem>/``
- File mode:    ``<base>/<cpgm_filename_stem>/``

Override with ``reporter.run_name: <my-tag>`` in the YAML to pick the
subdirectory name yourself.
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from r2pef.classification.role_classifier import classify
from r2pef.adapters import cpgm_api

from r2pef.config.loader import load_config
from r2pef.config.schemas import AdapterConfig, PipelineConfig
from r2pef.context.builder import build_context
from r2pef.models.cpgm import CPGM
from r2pef.reporting.reporter import Reporter
from r2pef.scorers.base import ScoreResult
from r2pef.scorers.if_scorer import IFScorer
from r2pef.scorers.ip_scorer import IPScorer
from r2pef.scorers.ir_scorer import IRScorer


log = logging.getLogger("r2pef")


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
class _PhaseFormatter(logging.Formatter):
    """Compact phase-aware formatter: ``[HH:MM:SS] phase ┃ message``."""

    def format(self, record: logging.LogRecord) -> str:
        ts = time.strftime("%H:%M:%S", time.localtime(record.created))
        phase = getattr(record, "phase", "")
        if phase:
            return f"[{ts}] {phase:<8}┃ {record.getMessage()}"
        return f"[{ts}] {record.getMessage()}"


def _setup_logging(level: int) -> None:
    """Install our handler exactly once. Idempotent across re-imports."""
    root = logging.getLogger("r2pef")
    root.setLevel(level)
    for h in list(root.handlers):
        root.removeHandler(h)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(_PhaseFormatter())
    handler.setLevel(level)
    root.addHandler(handler)
    root.propagate = False


def _phase(phase: str, msg: str, level: int = logging.INFO) -> None:
    """Log a one-liner tagged with a pipeline phase."""
    log.log(level, msg, extra={"phase": phase})


# ---------------------------------------------------------------------------
# CPGM acquisition
# ---------------------------------------------------------------------------
def _validate_against_schema(payload: Any) -> None:
    """Validate ``payload`` against ``cpgm.schema.json``.

    If validation fails, raises ``ValueError`` with a compact message.
    """
    schema_path = Path(__file__).parent / "cpgm.schema.json"
    if not schema_path.exists():
        return
    try:
        import jsonschema
        from jsonschema.exceptions import ValidationError
    except ImportError:
        return
    with schema_path.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)
    try:
        jsonschema.validate(instance=payload, schema=schema)
    except ValidationError as e:
        path = "/" + "/".join(str(p) for p in e.absolute_path) if e.absolute_path else "/"
        schema_path_str = "/" + "/".join(str(p) for p in e.absolute_schema_path)
        try:
            snippet = json.dumps(e.instance, default=str)
        except Exception:
            snippet = repr(e.instance)
        if len(snippet) > 200:
            snippet = snippet[:200] + "…"
        msg = (
            f"CPGM failed schema validation\n"
            f"  at instance path: {path}\n"
            f"  schema rule:      {schema_path_str}\n"
            f"  problem:          {e.message}\n"
            f"  offending value:  {snippet}"
        )
        raise ValueError(msg) from None


def _coerce_to_cpgm(result: Any, *, validate: bool = True) -> CPGM:
    """Normalise whatever the adapter dispatcher returns to a CPGM model.

    Pass ``validate=False`` to skip JSON-Schema validation.
    """
    if isinstance(result, CPGM):
        return result
    if isinstance(result, dict):
        if validate:
            _validate_against_schema(result)
        return CPGM.model_validate(result)
    raise TypeError(
        f"cpgm_api returned {type(result).__name__}; expected dict or CPGM."
    )


def _write_cpgm_json(payload: Any, run_dir: Path) -> Path:
    """Serialise an adapter-produced CPGM payload to ``<run_dir>/cpgm.json``.

    Accepts a dict or a Pydantic CPGM model. The directory is created if
    missing. Returns the written path.
    """
    run_dir.mkdir(parents=True, exist_ok=True)
    out_path = run_dir / "cpgm.json"
    if isinstance(payload, CPGM):
        data = payload.model_dump(mode="json", by_alias=True, exclude_none=False)
    else:
        data = payload
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, default=str)
    return out_path


def _resolve_run_dir_for_adapter(cfg: PipelineConfig, adapter_name: str) -> Path:
    """Resolve the run directory before the adapter runs (adapter mode only).

    Adapter mode names are derived from ``<algorithm>__<source-rdf-stem>``
    or the user-supplied ``run_name``; both are known without running the
    adapter, so we can save the CPGM even if it later fails validation.
    """
    base = Path(cfg.reporter.output_dir)
    tag = getattr(cfg.reporter, "run_name", None)
    if tag is None:
        source_stem = Path(cfg.source_rdf.path).stem
        tag = f"{adapter_name}__{source_stem}"
    tag = str(tag).replace("/", "_").replace("\\", "_").strip()
    if not tag:
        raise ValueError("Could not derive a run directory name.")
    return base / tag


def obtain_cpgm(cfg: PipelineConfig) -> Tuple[CPGM, bool, Path]:
    """Return ``(cpgm, produced_by_adapter, run_dir)``.

    In adapter mode, the produced CPGM is written to ``<run_dir>/cpgm.json``
    *before* JSON-Schema validation. That way, when an adapter emits an
    invalid CPGM, the user can open the file and inspect the offending
    location reported by the validator.
    """
    cpgm_cfg = cfg.cpgm

    # ---- file mode ------------------------------------------------------
    if cpgm_cfg.file is not None:
        # File-mode run_dir: <base>/<run_name or cpgm-filename-stem>
        base = Path(cfg.reporter.output_dir)
        tag = getattr(cfg.reporter, "run_name", None) or Path(cpgm_cfg.file).stem
        tag = str(tag).replace("/", "_").replace("\\", "_").strip()
        run_dir = base / tag

        _phase("cpgm", f"loading CPGM from file: {cpgm_cfg.file}")
        with Path(cpgm_cfg.file).open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
        _validate_against_schema(payload)
        cpgm = CPGM.model_validate(payload)
        _phase("cpgm", f"loaded — algorithm={cpgm.algorithm}, "
                       f"nodes={len(cpgm.nodes)}, relations={len(cpgm.relations)}")
        return cpgm, False, run_dir

    # ---- adapter mode ---------------------------------------------------
    adapter_name = cpgm_cfg.chosen_adapter()
    if adapter_name is None:  # pragma: no cover — schema enforces this
        raise RuntimeError("cpgm config validates but no adapter chosen")

    run_dir = _resolve_run_dir_for_adapter(cfg, adapter_name)

    adapter_cfg: AdapterConfig = getattr(cpgm_cfg, adapter_name)

    call_kwargs: Dict[str, Any] = {}
    for attr, kwarg in (("instance", "instance"),
                        ("input_dir", "input_dir")):
        v = getattr(adapter_cfg, attr, None)
        if v is not None:
            call_kwargs[kwarg] = v   

    # synthetic_labels / synthetic_keys: distinguish the three states
    #   None         → "use adapter defaults"    → forward as None
    #   []           → "disable entirely"        → forward as frozenset()
    #   ["A","B"]    → "override with this set"  → forward as frozenset(...)
    # Pydantic stores None when the YAML key is absent or explicitly null;
    # an empty list is preserved as [].
    for attr in ("synthetic_labels", "synthetic_keys"):
        v = getattr(adapter_cfg, attr, None)
        if v is None:
            call_kwargs[attr] = None
        else:
            call_kwargs[attr] = frozenset(v)

    extras = adapter_cfg.model_dump(exclude_none=True, by_alias=True)
    for k, v in extras.items():
        if k in call_kwargs:
            continue
        if k in ("instance", "input_dir", "synthetic_labels", "synthetic_keys"):
            continue
        call_kwargs.setdefault(k, v)

    _phase("cpgm", f"running adapter '{adapter_name}'")
    log.debug("adapter kwargs: %s", call_kwargs, extra={"phase": "cpgm"})

    t0 = time.perf_counter()

    if hasattr(cpgm_api, "run_adapter"):
        result = cpgm_api.run_adapter(adapter_name, **call_kwargs)
    elif hasattr(cpgm_api, "build_cpgm"):
        result = cpgm_api.build_cpgm(algorithm=adapter_name, **call_kwargs)
    elif hasattr(cpgm_api, adapter_name):
        result = getattr(cpgm_api, adapter_name)(**call_kwargs)
    else:
        raise AttributeError(
            f"cpgm_api exposes neither run_adapter(name, **kwargs), "
            f"build_cpgm(algorithm, **kwargs), nor {adapter_name}(**kwargs). "
            f"Cannot dispatch."
        )

    _phase("cpgm", f"adapter done in {time.perf_counter()-t0:.2f}s")

    # Persist the raw payload BEFORE validation. 
    cpgm_path = _write_cpgm_json(result, run_dir)
    _phase("cpgm", f"wrote raw CPGM to {cpgm_path}")

    # Validate. The validator raises a compact ValueError if anything is off.
    cpgm = _coerce_to_cpgm(result, validate=True)
    _phase("cpgm", f"validated — nodes={len(cpgm.nodes)}, "
                   f"relations={len(cpgm.relations)}")
    return cpgm, True, run_dir


# ---------------------------------------------------------------------------
# Classifier output normalisation
# ---------------------------------------------------------------------------
_RDFLIB_LITERAL_RE = re.compile(
    r"""^rdflib\.term\.Literal\(    # prefix
        (?P<q>['"])                 # opening quote (' or ")
        (?P<body>(?:\\.|(?!(?P=q)).)*)  # body: anything except an unescaped closing quote
        (?P=q)                      # closing quote matching opener
        (?:,\s*[^)]*(?:\([^)]*\))?[^)]*)?  # optional ", datatype=..." or ", lang=..." tail
        \)$""",
    re.VERBOSE | re.DOTALL,
)


def _normalise_literal_token(s: Any) -> Any:
    """If ``s`` looks like ``rdflib.term.Literal('X')``, return ``'"X"'``.

    Returns the input unchanged for any other value (including non-string).
    """
    if not isinstance(s, str):
        return s
    m = _RDFLIB_LITERAL_RE.match(s)
    if not m:
        return s
    body = m.group("body")
    q = m.group("q")
    body = body.replace("\\" + q, q)
    return f'"{body}"'


def _normalise_classifier_output(role: Dict[str, Any]) -> Dict[str, int]:
    """Rewrite rdflib-style literal tokens in-place.

    The classifier may render literal terms using rdflib's repr() shape::

        "rdflib.term.Literal('desperately impoverishes Tesla')"

    rather than the spec's example form::

        '"desperately impoverishes Tesla"'

    This normaliser rewrites the former into the latter so element_roles
    and occurrence_roles[*].triple use the canonical quoted-literal form.
    Returns ``{"literal_tokens": N}``.
    """
    counts = {"literal_tokens": 0}

    # element_roles: rebuild with normalised keys.
    er = role.get("element_roles")
    if isinstance(er, dict):
        new_er = {}
        for k, v in er.items():
            nk = _normalise_literal_token(k)
            if nk != k:
                counts["literal_tokens"] += 1
            new_er[nk] = v
        role["element_roles"] = new_er

    # occurrence_roles: each entry has a "triple" — fix each component.
    occ = role.get("occurrence_roles")
    if isinstance(occ, dict):
        for k, info in occ.items():
            if not isinstance(info, dict):
                continue
            t = info.get("triple")
            if t is None:
                continue
            new_t = []
            for comp in t:
                nc = _normalise_literal_token(comp)
                if nc != comp:
                    counts["literal_tokens"] += 1
                new_t.append(nc)
            info["triple"] = type(t)(new_t) if not isinstance(t, tuple) else tuple(new_t)

    # u_partitions: lists of strings; rewrite any that look rdflib-ish.
    parts = role.get("u_partitions")
    if isinstance(parts, dict):
        for key, vals in list(parts.items()):
            if not isinstance(vals, (list, set, tuple)):
                continue
            new_vals = []
            for x in vals:
                nx = _normalise_literal_token(x)
                if nx != x:
                    counts["literal_tokens"] += 1
                new_vals.append(nx)
            parts[key] = new_vals

    return counts


# ---------------------------------------------------------------------------
# Sanity checks
# ---------------------------------------------------------------------------

def _input_sanity_checks(cpgm: CPGM, role: Dict[str, Any], source_path: str) -> None:
    """Warn about empty / degenerate inputs immediately after classification.

    Run BEFORE context build so the user sees the warning even if the
    context build then produces zero-everything.
    """
    n_nodes = len(cpgm.nodes)
    n_rels = len(cpgm.relations)
    if n_nodes == 0 and n_rels == 0:
        log.warning("CPGM is empty (0 nodes, 0 relations) — every metric "
                    "will be undefined or 0", extra={"phase": "sanity"})
    elif n_nodes == 0:
        log.warning("CPGM has no nodes (%d relations) — IF / IR will collapse",
                    n_rels, extra={"phase": "sanity"})

    er = role.get("element_roles") or {}
    occ = role.get("occurrence_roles") or {}
    if not er and not occ:
        log.warning("classifier output is empty (element_roles and "
                    "occurrence_roles both empty) — every metric will be "
                    "undefined", extra={"phase": "sanity"})
    elif not er:
        log.warning("classifier output has 0 element_roles — IF element-level "
                    "scoring will produce nothing", extra={"phase": "sanity"})
    elif not occ:
        log.warning("classifier output has 0 occurrence_roles — IF "
                    "occurrence-level scoring will produce nothing",
                    extra={"phase": "sanity"})

    summary = role.get("summary") or {}
    n_unique = summary.get("triples_unique")
    if n_unique == 0:
        log.warning("source RDF parsed to 0 triples (%s) — IP will be 0/0",
                    source_path, extra={"phase": "sanity"})


def _post_context_sanity_checks(ctx: Any) -> None:
    """Warn about degenerate context state after build_context."""
    if len(ctx.R) == 0 and (len(ctx.cpgm.nodes) > 0 or len(ctx.cpgm.relations) > 0):
        log.warning("R is empty despite a non-empty CPGM — every "
                    "ResourceHandle was synthetic or had resolved=None. "
                    "Check the adapter's `synthetic` flag usage.",
                    extra={"phase": "sanity"})
    if len(ctx.pgius) == 0 and (len(ctx.cpgm.nodes) > 0 or len(ctx.cpgm.relations) > 0):
        log.warning("no PGIUs were derived from the CPGM — IP will be 0 "
                    "and IF occurrence-level scoring will be 100%% undefined",
                    extra={"phase": "sanity"})
    if len(ctx.source_triples) == 0:
        log.warning("source RDF parse yielded 0 triples — IP and IF "
                    "occurrence-level scoring will produce nothing",
                    extra={"phase": "sanity"})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def run(config_path: Path) -> Dict[str, ScoreResult]:
    t0 = time.perf_counter()
    wall_times: Dict[str, float] = {}

    # Step 1 — config
    _phase("config", f"loading {config_path}")
    t_cfg = time.perf_counter()
    cfg = load_config(config_path)
    wall_times["config"] = time.perf_counter() - t_cfg

    # Step 2 — CPGM (resolves run_dir internally; in adapter mode the raw
    # payload is written to <run_dir>/cpgm.json before validation).
    t_cpgm = time.perf_counter()
    cpgm, by_adapter, run_dir = obtain_cpgm(cfg)
    wall_times["cpgm"] = time.perf_counter() - t_cpgm
    cfg.reporter.output_dir = run_dir  # so the reporter writes here
    _phase("output", f"run directory: {run_dir}")

    # Step 3 — role classification (mandatory; no fallback)
    _phase("classify", f"running classifier on {cfg.source_rdf.path}")
    t_clf = time.perf_counter()
    role = classify(str(cfg.source_rdf.path), k=1, mode="full")
    norm = _normalise_classifier_output(role)
    if norm["literal_tokens"]:
        _phase("classify", f"normalised {norm['literal_tokens']} rdflib-style "
                           f"literal token(s)")
    n_triples = role.get("summary", {}).get(
        "triples_unique", len(role.get("occurrence_roles", {}))
    )
    wall_times["classify"] = time.perf_counter() - t_clf
    _phase("classify", f"done in {wall_times['classify']:.2f}s — "
                       f"unique triples={n_triples}")

    # Sanity checks on the inputs collected so far.
    _input_sanity_checks(cpgm, role, str(cfg.source_rdf.path))

    # Step 4 — evaluation context
    _phase("context", "building registries + PGIUs")
    t_ctx = time.perf_counter()
    ctx = build_context(cpgm, cfg.source_rdf.path, role)
    wall_times["context"] = time.perf_counter() - t_ctx
    _phase("context", f"built in {ctx.wall_time_build_s:.2f}s — "
                      f"|R|={len(ctx.R)}, |PGIUs|={len(ctx.pgius)}, "
                      f"|derived_triples(C)|={len(ctx.derived_triples)}")

    # Post-context sanity checks (these need the registry to be built).
    _post_context_sanity_checks(ctx)

    # Step 5 — run scorers
    results: Dict[str, ScoreResult] = {}
    metrics = cfg.evaluation.metrics
    for m in ("ip", "if", "ir"):
        if m not in metrics:
            continue
        t_s = time.perf_counter()
        if m == "if":
            r = IFScorer(threshold=cfg.scorer.if_.threshold).score(ctx)
        elif m == "ip":
            r = IPScorer(threshold=cfg.scorer.ip.threshold).score(ctx)
        else:
            r = IRScorer(threshold=cfg.scorer.ir.threshold).score(ctx)
        results[m] = r
        wall_times[f"score_{m}"] = time.perf_counter() - t_s
        passed = r.extras.get("passed_threshold", False)
        verdict = "PASS" if passed else "FAIL"
        _phase("score", f"{m.upper():2}  {r.score:.4f}  {verdict}  "
                        f"({wall_times[f'score_{m}']:.2f}s)")

    # Step 6 — report
    _phase("report", f"writing report to {run_dir}")
    t_rep = time.perf_counter()
    reporter = Reporter(run_dir)
    wall_pre_report = time.perf_counter() - t0
    reporter.write_all(cfg, ctx, results, wall_pre_report, by_adapter, wall_times)
    wall_times["report"] = time.perf_counter() - t_rep

    wall_true = time.perf_counter() - t0
    wall_times["total"] = wall_true
    # Re-write report.json with the final wall_times
    try:
        report_path = run_dir / "report.json"
        if report_path.exists():
            with report_path.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
            payload["wall_time_total_s"] = wall_true
            payload["wall_times_s"] = dict(wall_times)
            with report_path.open("w", encoding="utf-8") as fh:
                json.dump(payload, fh, indent=2, default=str)
    except Exception as exc:  # noqa: BLE001
        log.warning("could not patch report.json with final wall time: %s",
                    exc, extra={"phase": "report"})

    _phase("done", f"total wall time: {wall_true:.2f}s")
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="r2pef.pipeline",
        description="Evaluate an RDF→PG translation algorithm.",
    )
    parser.add_argument("config", type=Path, help="Path to pipeline_config.yaml")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("-v", "--verbose", action="store_true",
                   help="Show DEBUG-level logs (kwargs, intermediate sizes).")
    g.add_argument("-q", "--quiet", action="store_true",
                   help="Show only WARNING/ERROR-level logs.")
    args = parser.parse_args(argv)

    if args.verbose:
        _setup_logging(logging.DEBUG)
    elif args.quiet:
        _setup_logging(logging.WARNING)
    else:
        _setup_logging(logging.INFO)

    # NOTE: do NOT wrap run() in a try/except — classifier and adapter
    # failures must surface with a full traceback.
    run(args.config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
