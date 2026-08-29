"""Configuration schemas for the pipeline.

The YAML format intentionally maps one algorithm key under ``cpgm:`` to
the adapter parameters for that algorithm. Alternatively, ``cpgm.file:``
points at a pre-computed CPGM JSON file.

Example (adapter mode)::

    cpgm:
      rdf2pg_gdm:
        instance: /path/to/instance.ypg
        synthetic_labels: ["Resource", "Literal"]

Example (file mode)::

    cpgm:
      file: /path/to/cpgm.json

These two are mutually exclusive — exactly one of them must be present.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ---------------------------------------------------------------------------
# Per-section blocks
# ---------------------------------------------------------------------------
class SourceRDFConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: Path = Field(..., description="Path to .nt or .ttl source RDF file.")


class AdapterConfig(BaseModel):
    """Generic adapter parameters.

    Keys recognised by all four adapters:

    - ``instance``  — single .ypg / .json input file (sdm / gdm / cdm)
    - ``input_dir`` — directory of inputs (kg2pg)
    - ``synthetic_labels`` — set of labels the adapter should treat as
      synthetic (no source-RDF counterpart). 
    - ``synthetic_keys`` — same semantics, for property keys.

    The pipeline forwards ``instance`` and ``input_dir`` as ``Path``,
    ``synthetic_labels`` and ``synthetic_keys`` as ``frozenset`` (or
    ``None``), and any additional keys verbatim.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    instance: Optional[Path] = None
    input_dir: Optional[Path] = None
    synthetic_labels: Optional[List[str]] = None
    synthetic_keys: Optional[List[str]] = None


class CPGMConfig(BaseModel):
    """Holds *either* a single adapter entry *or* a ``file:`` entry."""

    model_config = ConfigDict(extra="allow")

    # If present, just load the CPGM from disk.
    file: Optional[Path] = None

    # Each adapter has its own optional sub-block.
    kg2pg: Optional[AdapterConfig] = None
    rdf2pg_sdm: Optional[AdapterConfig] = None
    rdf2pg_gdm: Optional[AdapterConfig] = None
    rdf2pg_cdm: Optional[AdapterConfig] = None

    @model_validator(mode="after")
    def _check_exactly_one(self) -> "CPGMConfig":
        adapters_present = [
            name
            for name in ("kg2pg", "rdf2pg_sdm", "rdf2pg_gdm", "rdf2pg_cdm")
            if getattr(self, name) is not None
        ]
        n_modes = (1 if self.file is not None else 0) + len(adapters_present)
        if n_modes == 0:
            raise ValueError(
                "cpgm: must specify either `file: <path>` or one adapter section "
                "(kg2pg / rdf2pg_sdm / rdf2pg_gdm / rdf2pg_cdm)."
            )
        if n_modes > 1:
            raise ValueError(
                "cpgm: specify exactly one of `file:` or a single adapter section."
            )
        return self

    def chosen_adapter(self) -> Optional[str]:
        """Return the adapter name in adapter mode, or None in file mode."""
        for name in ("kg2pg", "rdf2pg_sdm", "rdf2pg_gdm", "rdf2pg_cdm"):
            if getattr(self, name) is not None:
                return name
        return None


class EvaluationConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metrics: List[Literal["if", "ip", "ir"]] = Field(default_factory=lambda: ["if", "ip", "ir"])


class ReporterConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Base directory for reports. The pipeline appends a run-specific
    # subdirectory (see pipeline.py docstring); use `run_name` to override.
    output_dir: Path = Path("report")
    # Optional explicit name for the run subdirectory. If unset, the
    # pipeline derives one from the algorithm + source-RDF stem (adapter
    # mode) or the CPGM filename stem (file mode).
    run_name: Optional[str] = None
    visualize: bool = False


class ThresholdConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    threshold: float = 0.9


class FairnessConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mandatory_metrics: List[str] = Field(default_factory=list)
    optional_metrics: List[str] = Field(default_factory=list)


class ScorerConfig(BaseModel):
    """Per-scorer thresholds and the fairness aggregator."""

    model_config = ConfigDict(extra="forbid")

    # Note the trailing underscore on `if_` — `if` is a reserved word in Python.
    if_: ThresholdConfig = Field(default_factory=ThresholdConfig, alias="if_")
    ip: ThresholdConfig = Field(default_factory=ThresholdConfig)
    ir: ThresholdConfig = Field(default_factory=ThresholdConfig)
    fairness: FairnessConfig = Field(default_factory=FairnessConfig)


# ---------------------------------------------------------------------------
# Top-level
# ---------------------------------------------------------------------------
class PipelineConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_rdf: SourceRDFConfig
    cpgm: CPGMConfig
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)
    reporter: ReporterConfig = Field(default_factory=ReporterConfig)
    scorer: ScorerConfig = Field(default_factory=ScorerConfig)
