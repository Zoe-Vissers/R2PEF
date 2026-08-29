# r2pef Transformation Evaluation Orchestrator

Automated execution of rdf2pg (SDM/GDM/CDM), QSE+KG2PG (S3PG parsimonious and
non-parsimonious), and the r2pef pipeline across a corpus of RDF 
datasets, with a single ledger of results.

## Conceptual model

For each `(dataset, pipeline)` combination, the driver:

1. Generates the required configuration files.
2. Invokes the translation algorithm.
3. Invokes the evaluation framework a number of times.

Each run lives in `<output_root>/<dataset>/<family>/<pipeline>/<utc_timestamp>/`:
 
```
<output_root>/
├── results.csv                                       # the results log
└── <dataset>/
    └── <family>/                                     # rdf2pg | kg2pg | prebuilt
        └── <pipeline>/                               # sdm | gdm | cdm | parsi | nonparsi
            └── <utc_timestamp>/                      # one pipeline_id
                ├── qse/                              # kg2pg pipelines only
                │   ├── qse.properties
                │   ├── log.txt
                │   └── <dataset>_QSE_FULL_SHACL.ttl
                ├── kg2pg/  (or rdf2pg_sdm/ etc.)
                │   ├── kg2pg.properties
                │   ├── log.txt
                │   └── <output subdir or instance.ypg>
                ├── eval_rep0/
                │   ├── pipeline_config.yaml
                │   ├── log.txt
                │   └── (eval framework outputs)
                ├── eval_rep1/
                └── eval_rep2/
```
 
Available **pipelines**:
 
| Pipeline         | Family   | Pre-step | Translation     | Eval adapter |
| ---------------- | -------- | -------- | --------------- | ------------ |
| `sdm`            | rdf2pg   | -        | rdf2pg -sdm     | sdm          |
| `gdm`            | rdf2pg   | -        | rdf2pg -gdm     | gdm          |
| `cdm`            | rdf2pg   | -        | rdf2pg -cdm     | cdm          |
| `parsi`          | kg2pg    | qse      | kg2pg parsi=T   | kg2pg        |
| `nonparsi`       | kg2pg    | qse      | kg2pg parsi=F   | kg2pg        |
| `(prebuilt)`     | prebuilt | -        | -               | file         |

## Prerequisites

Install once per machine:

* JDK (whichever version rdf2pg / QSE / KG2PG require)
* Python 3.12 environment with the dependencies from environment.yml / requirements.txt
* All three translation implementations cloned and built (see details below):
  * **QSE** - `qse.jar`
  * **KG2PG** - `kg2pg.jar`
  * **rdf2pg** - `rdf2pg.jar` and `lib/` with `rdfs-processor.jar`
* RDF datasets placed under one directory (`data_root` below)

### Third-Party Tools
 
This repository contains only the orchestrator that invokes the following
tools. The tools themselves are not bundled; each must be installed
separately by the user, per the upstream project's instructions. Their
sources, licenses, and copyrights are unaffected by inclusion in this
workflow.
 
#### QSE - Quality Shapes Extraction
- Repository: https://github.com/dkw-aau/qse
- Licence: MIT
- Reference:
  > Rabbani, Kashif, Matteo Lissandrini, and Katja Hose. "Extraction of validating shapes from very large knowledge graphs." Proceedings of the VLDB Endowment 16.5 (2023): 1023-1032.
#### KG2PG - Knowledge Graph to Property Graph
- Repository: https://github.com/dkw-aau/KG2PG
- Companion artifact (S3PG): https://github.com/dkw-aau/s3pg
- License: MIT
- Reference (S3PG, ACM SIGMOD 2025):
  > Rabbani, Kashif, et al. "Transforming RDF graphs to property graphs using standardized schemas." Proceedings of the ACM on Management of Data 2.6 (2024): 1-25.
#### rdf2pg
- Repository: https://github.com/renzoar/rdf2pg
- License: Apache 2.0
- Reference: 
  > Angles, Renzo, Harsh Thakkar, and Dominik Tomaszuk. "Mapping RDF databases to property graph databases." IEEE Access 8 (2020): 86091-86110.


## Setup

```bash
git clone <this-repo>
cd rdf-pg-eval
cp machine.example.yaml machine.yaml
$EDITOR machine.yaml
$EDITOR datasets.yaml
$EDITOR runs.yaml
```

| File                   | Purpose                                          | Per-machine? |
|------------------------|--------------------------------------------------|--------------|
| `machine.yaml`         | jar paths, data_root, output_root, timeouts      | Yes (gitignored) |
| `datasets.yaml`        | dataset names, relative paths, expected counts   | No |
| `runs.yaml`            | which adapters x datasets to run, skip list      | No |


Validate the plan without executing:

```bash
python3 run_evaluation.py --dry-run
```
```
 
Run / resume / retry:
 
```bash
python3 run_evaluation.py                 # skip already-completed pipelines
python3 run_evaluation.py --retry-failed  # redo only failed pipelines
python3 run_evaluation.py --force         # redo everything
```

## Adding a new dataset

1. Place the file under `data_root`.
2. Add an entry to `datasets.yaml` with `path_rel`, `expected_classes`,
   `expected_lines`. Use `wc -l` for the line count.
3. Re-run the driver.
