# r2pef

A framework for evaluating RDF→property-graph translations along the
three orthogonal axes **IP** (Information Preservation), **IF** (Idiomatic Fidelity), and **IR** (Identifier Retention).

---

## Installation

The framework needs Python 3.12 and `rdflib`, `pydantic`, `pyyaml`, `jsonschema`
and `matplotlib`. 

```bash
# conda
conda env create -f environment.yml && conda activate r2pef
```

The dependency files live in the repository root.

## Running

Run from the **repository root** — the directory that contains `r2pef/`:

```bash
python -m r2pef.pipeline r2pef/examples/pipeline_config.example.yaml
```

Options: `-v` for DEBUG logs, `-q` for warnings only.

If you invoke it from somewhere else, put the repository root on the import path:

```bash
PYTHONPATH=/path/to/repo python -m r2pef.pipeline <config.yaml>
```

Relative paths *inside* a pipeline config are resolved against the config file's own
directory, not the working directory — so a config can be moved around with its inputs.

For the full experiment matrix (all algorithms × all datasets, automated), use the
orchestrator in `../runner/` instead. See `../REPRODUCIBILITY.md`.

## Project layout

```
r2pef/
├── pipeline.py              # CLI + orchestrator
├── cpgm.schema.json         # JSON Schema for CPGM JSON files
├── classification/
│   └── role_classifier.py   # classifies U_so and T into NR, NPVR, TMR, NPKR, ELR
├── config/
│   ├── loader.py            # YAML loader for pipeline configuration
│   └── schemas.py           # Pydantic config models
├── models/
│   ├── cpgm.py              # Pydantic CPGM models
│   └── evaluation.py        # EvaluationContext, R, R⁻¹, PGIU dataclasses
├── context/
│   ├── builder.py           # builds evaluation context
│   └── canonicalization.py  # local_name(s) helper
├── scorers/
│   ├── if_scorer.py
│   ├── ip_scorer.py
│   ├── ir_scorer.py
│   └── base.py              # ScoreResult, Scorer ABC
├── reporting/
│   └── reporter.py          # writes report.json + detail files + summary.md
└── adapters/
    ├── cpgm_api.py          # run_adapter()
    └── cpgm_core.py         
    └── adapter_kg2pg.py 
    └── adapter_rdf2pg_cdm.py 
    └── adapter_rdf2pg_gdm.py 
    └── adapter_rdf2pg_sdm.py 

```

---

## Pipeline

`pipeline.py` runs six steps in order.

### 1. Load config

### 2. Obtain CPGM

Two modes: file-mode (use prebuilt CPGM) or adapter-mode (build CPGM from translation outputs)

### 3. Role classification

The role classifier reads the source RDF and assigns elements **NR** (Node Role) or **NPVR** (Node Property Value Role), respectively occurrences **TMR** (Type Marker Role), **NPKR** (Node Property Key Role) or **ELR** (Edge Label Role).

### 4. Build EvaluationContext

Generates common ground for computation of all scores.

```text
build_context(cpgm, source_rdf_path, role):
    1. T := parse_rdf(source_rdf_path)                  
    2. R := build_provenance_registry(cpgm)             
    3. R_inv := build_reverse_registry(R)              
    4. (pgius, derive_C, triple_index) := build_pgius(cpgm, R)
    5. return EvaluationContext(T, role, R, R_inv, pgius, derive_C, ...)
```

### 5. Score

The three scorers are independent. They run in any order over the same
context.

#### IF aggregate

```text
IF = scored_1 / (scored_0 + scored_1)
undefined_rate = undefined / total
```

#### IP aggregate

```text
IP = |{ t in T : t ∈ derived_triples(C) directly or via local-name match }| / |T|
```

#### IR aggregate

```text
IR = (1 / |U_{IR}(C)|) · Σ_{h in U_{IR}(C)} w(IR-tier(h))
```

#### Fairness verdict

```text
verdict_passed =
    all(score(m) ≥ threshold(m) for m in cfg.fairness.mandatory_metrics)
```

The optional metrics are reported alongside but do not gate the verdict.

### 6. Report

The reporter writes seven files:

| File                       | Content |
|---|---|
| `report.json`              | Aggregate scores, tier distributions, fairness verdict, `wall_time_total` |
| `if_detail.json`           | Per-unit IF results |
| `ip_detail_lost.json`      | Triples not in `derived_triples(C)`, grouped by predicate |
| `ip_detail_pgius.json`     | All derived triples with CPGM anchors |
| `ir_detail.json`           | Per-IRI tier, score, `cpgm_value` (raw), `location` |
| `role_classification.json` | Full classifier output |
| `summary.md`               | Human-readable narrative |
| `cpgm.json`                | Adapter-produced CPGM (adapter mode only) |

---


## Configuration

A minimal config:

```yaml
source_rdf:
  path: input.nt  

evaluation:
  metrics: ["if", "ip", "ir"]

reporter:
  output_dir: report/
  run_name: null
  visualize: true

scorer:
  if_:  { threshold: 0.9 }
  ip:   { threshold: 0.9 }
  ir:   { threshold: 0.9 }
  fairness:
    mandatory_metrics: ["if", "ip"]
    optional_metrics:  ["ir"]

cpgm:
  file: cpgm.json  
```

In adapter mode:

```yaml
cpgm:
  rdf2pg_gdm:
    instance: my_translation.ypg
    synthetic_labels: [Resource, Literal, DatatypeProperty, ObjectProperty]
```

Relative paths in the config are resolved against the config file's own
directory.

---