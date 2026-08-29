# R2PEF: RDF-PG Evaluation Framework incl. Orchestrator

This repository contains two separable components, one shared Conda environment,
the raw datasets used in all experiments, and the original results.

| # | Component | Directory | What it is |
|---|-----------|-----------|------------|
| 1 | **R2PEF** | `r2pef/` | Python package. Computes **IF** (Idiomatic Fidelity), **IP** (Information Preservation), **IR** (Identifier Retention) from a Canonical Property Graph Model (CPGM). |
| 2 | **R2PEF orchestrator** | `runner/` | Automates the full R2PEF matrix (dataset × translation algorithm × evaluation). Generates every tool config, times every phase, writes one ledger (`results.csv`). |

Reviewers who only want the numbers: see `reproducibility/`.
Reviewers who want to re-run everything: see **[REPRODUCIBILITY.md](REPRODUCIBILITY.md)**.

---

## Project layout

```
.
├── README.md                     # this file
├── REPRODUCIBILITY.md            # step-by-step: environment → runs → results
├── environment.yml               # the single shared Conda environment
├── requirements.txt              # alternatively: the single shared venv 
│
├── r2pef/                  # (1) EVALUATION FRAMEWORK  [python package]
│   ├── pipeline.py               #     CLI + orchestrator: python -m r2pef.pipeline <cfg>
│   ├── cpgm.schema.json          #     JSON Schema for the CPGM
│   ├── adapters/                 #     kg2pg, rdf2pg_sdm, rdf2pg_gdm, rdf2pg_cdm → CPGM
│   ├── classification/           #     role_classifier.py (NR, NPVR, TMR, NPKR, ELR)
│   ├── config/                   #     YAML → PipelineConfig (Pydantic)
│   ├── models/                   #     CPGM + EvaluationContext (R, R⁻¹, PGIUs)
│   ├── context/                  #     registry + PGIU construction, derive()
│   ├── scorers/                  #     if_scorer.py, ip_scorer.py, ir_scorer.py
│   ├── reporting/                #     report.json, *_detail.json, summary.md
│   ├── examples/                 #     example pipeline_config.yaml
│   └── README.md
│
├── runner/                       # (3) ORCHESTRATOR
│   ├── run_evaluation.py         #     the driver
│   ├── lib/                      #     config, paths, runners, ledger
│   ├── templates/                #     qse.properties, kg2pg.properties, eval pipeline_config
│   ├── machine.example.yaml      #     → copy to machine.yaml and edit (jar paths only)
│   ├── datasets.yaml             #     dataset catalogue (points at ../datasets)
│   ├── runs.yaml                 #     execution plan
│   └── README.md
│
├── datasets/                     # raw inputs for experiments (data_root)
│   ├── dbpedia/
│   ├── watdiv/
│   └── bsbm/
│
├── reproducibility/
    ├── results/                 # RQ1/P1,P3,P4: validation of generalizability, transparency + scalability 
    └── sensitivity/             # RQ1/P2: validation of sensitivity 
```

## Dependency direction

```
runner      ──invokes──►  r2pef.pipeline  (subprocess)
```