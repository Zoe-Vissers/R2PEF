"""Pydantic v2 models for the Canonical Property Graph Model (CPGM).

Mirrors `cpgm.schema.json`. The framework reads these objects after the
adapter has produced them; it never re-resolves identifiers.

Design notes
------------
- `ResourceHandle` carries the full provenance of a single identifier-bearing
  element. ``synthetic=True`` implies ``raw=form=resolved=None``. ``synthetic=False``
  always carries a non-null ``resolved`` string.
- A ``Node`` has a single ``id`` field.
- ``Relation`` carries no provenance at the relation level.
- ``model_config = ConfigDict(frozen=True)`` is intentionally NOT set: scorers
  may need to read these models repeatedly but never mutate them. 
"""
from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ---------------------------------------------------------------------------
# Primitive enums and atoms
# ---------------------------------------------------------------------------
class ExpressionForm(str, Enum):
    """How a source-side identifier was expressed in the translation output."""

    FULL_IRI = "full_iri"
    NAMESPACE_PLUS_LOCAL = "namespace_plus_local"
    LOCAL_ONLY = "local_only"
    LITERAL = "literal"


class ResourceHandle(BaseModel):
    """Provenance record for a single identifier-bearing element.

    Used for node identities, label, property keys, and property values.
    """

    model_config = ConfigDict(extra="forbid")

    raw: Optional[str] = Field(
        ...,
        description=(
            "Exact string as it appeared in the translation output "
            "before adapter resolution. Null when synthetic=true."
        ),
    )
    form: Optional[ExpressionForm] = Field(
        ...,
        description="How the identifier was expressed. Null when synthetic=true.",
    )
    resolved: Optional[str] = Field(
        ...,
        description=(
            "Best available resolved form, produced by the adapter. "
            "Never null when synthetic=false."
        ),
    )
    synthetic: bool = Field(
        ...,
        description=(
            "True when this element was invented by the translation with "
            "no source RDF counterpart."
        ),
    )

    @model_validator(mode="after")
    def _check_synthetic_consistency(self) -> "ResourceHandle":
        if self.synthetic:
            # When synthetic=true, all three other fields must be null.
            if self.raw is not None or self.form is not None or self.resolved is not None:
                raise ValueError(
                    "Synthetic ResourceHandle must have raw=form=resolved=None"
                )
        else:
            if self.resolved is None:
                raise ValueError(
                    "Non-synthetic ResourceHandle must have a non-null `resolved` "
                    "string (the adapter is responsible for resolution)."
                )
        return self


# ---------------------------------------------------------------------------
# Prefix bindings
# ---------------------------------------------------------------------------
class PrefixMapping(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prefix: str
    namespace: str


# ---------------------------------------------------------------------------
# Label and property entries
# ---------------------------------------------------------------------------
class LabelEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    label_ref: ResourceHandle


class PropertyEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    key_ref: ResourceHandle
    value_ref: ResourceHandle


# ---------------------------------------------------------------------------
# Node / Relation
# ---------------------------------------------------------------------------
class Node(BaseModel):
    """A node in the property graph.

    The kind of identity carried by ``id`` can be read off ``node_ref``:

    - ``node_ref.form == full_iri`` / ``namespace_plus_local`` / ``local_only``
      → ``id`` is a resolved IRI for a resource node.
    - ``node_ref.form == literal`` → ``id`` is an adapter-fabricated anchor
      for a value-bearing node; the literal value lives in
      ``node_ref.resolved``.
    - ``node_ref.synthetic == true`` → the node itself was invented by the
      translation algorithm (no source RDF counterpart). 

    """

    model_config = ConfigDict(extra="forbid")

    id: str
    node_ref: ResourceHandle
    labels: List[LabelEntry] = Field(default_factory=list)
    properties: List[PropertyEntry] = Field(default_factory=list)


class Relation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start: str
    end: str
    labels: List[LabelEntry] = Field(default_factory=list)
    properties: List[PropertyEntry] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Top-level CPGM
# ---------------------------------------------------------------------------
class CPGM(BaseModel):
    """Top-level CPGM document — the file the adapters produce."""

    model_config = ConfigDict(extra="forbid")

    algorithm: str = Field(
        ...,
        description="Translation algorithm that produced this CPGM.",
    )
    prefixes: List[PrefixMapping] = Field(default_factory=list)
    nodes: List[Node] = Field(default_factory=list)
    relations: List[Relation] = Field(default_factory=list)

    @model_validator(mode="after")
    def _check_algorithm_enum(self) -> "CPGM":
        allowed = {"kg2pg", "rdf2pg_sdm", "rdf2pg_gdm", "rdf2pg_cdm"}
        if self.algorithm not in allowed:
            raise ValueError(
                f"algorithm must be one of {sorted(allowed)}, got {self.algorithm!r}"
            )
        return self