# Reproducibility

Everything below is copy-paste. Run from the repository root unless stated otherwise.

Original results are already in `reproducibility/results/` - **you do not have to run
anything to inspect them.**

---

## 0. Requirements

| | |
|---|---|
| OS | Linux (tested on Ubuntu 22.04, x86-64) |
| Python | 3.12 |
| Java | JDK 21 (only for [#3 full evaluation](#3-full-evaluation-java-required)) |
| Translation Tools | see `runner/README.md` "Third Party Tools" (only for [#3 full evaluation](#3-full-evaluation-java-required)) |

## 1. Environment (once)

**Conda (recommended, tested)**. Any Python 3.12 environment with the dependencies works, 
but only the Conda path is verified.
 
**Conda**:
 
```bash
conda env create -f environment.yml
conda activate r2pef
```
 
Verify:
 
```bash
python -c "import rdflib, pydantic, jsonschema, matplotlib; print('ok')"
```

## 2. Smoke test (no Java needed, ~1 min)

Evaluates a hand-built CPGM against a tiny source graph and prints IF / IP / IR.

```bash
python -m r2pef.pipeline reproducibility/sensitivity/pipeline_config_smoke.yaml
cat reproducibility/runs/smoke/*/summary.md
```

## 3. Full evaluation (Java required)

Builds every translation and evaluates it, for every dataset.

```bash
# 3a. Build the third-party jars (see README.md → Third-party tools), then:
cd runner
cp machine.example.yaml machine.yaml
$EDITOR machine.yaml       # set: the four jar paths, java_home, and eval.python
                           # eval.python = the interpreter of the env from §1, as an
                           # absolute path, e.g. ~/miniforge3/envs/r2pef/bin/python
                           # or <repo>/.venv/bin/python
                           # data_root and output_root already point into this repo.
```

Six values in `machine.yaml` are machine-specific and have no sensible default. 
Everything else in the file already works as shipped.

| Key | What to put there |
|---|---|
| `java.java_home` | Your JDK 21 root, or `null` to use the system Java. Check: `java -version` |
| `rdf2pg.jar` | Path to `rdf2pg.jar` |
| `rdf2pg.lib` | The `lib/` directory next to it — **must contain `rdfs-processor.jar`** (the CDM pipeline's first step needs it) |
| `qse.jar` | Path to `qse.jar` |
| `qse.resources_path` | QSE's `src/main/resources` directory |
| `kg2pg.jar` | Path to `kg2pg.jar` |
| `eval.python` | **Absolute** path to the interpreter of the environment you prepared. Not a bare `python` — the driver spawns subprocesses without an activated shell.<br>conda: `conda activate <env> && which python`<br>venv: `<venv>/bin/python` |

Already set, leave alone unless you have a reason:

| Key | Value | Why |
|---|---|---|
| `eval.root` | `..` | The repository root — the directory containing `r2pef/`. Used as `PYTHONPATH` and as the eval subprocess's working directory. |
| `data_root` | `../datasets` | The datasets shipped with this repository. |
| `output_root` | `../reproducibility/runs` | Where fresh runs land. The reference results in `../reproducibility/results/` are never touched. |

Now, everything is ready for fully automated pipeline runs:

```bash
python run_evaluation.py --dry-run     # prints the plan, executes nothing
python run_evaluation.py               # the real thing - use tmux/nohup, it is long
```

Results land in `reproducibility/runs/` (= `output_root`), one row per phase in
`reproducibility/runs/results.csv`.

Resume / retry:

```bash
python run_evaluation.py                 # skips pipelines already marked OK
python run_evaluation.py --retry-failed
python run_evaluation.py --force         # redo everything
```

> **Always run the driver from inside `runner/`.** The relative paths in
> `machine.yaml`, `datasets.yaml`, and `runs.yaml` are resolved against the current
> working directory.

Restrict the plan for a quick check (edit `runner/runs.yaml`):

```yaml
only_datasets: [bsbm_1k]
only_pipelines: [sdm]
```

## 4. Metric sensitivity tests
 
Nine hand-built CPGMs, each isolating one failure mode (IP t1–t3, IF t1–t4, IR t1–t2).
They are listed as `prebuilt_pipelines` in `runner/runs.yaml` and run alongside the rest;
to run *only* them, set `only_pipelines: [sens_ip_t1, sens_ip_t2, ...]`.
 
Inputs: `reproducibility/sensitivity/`. Expected scores: `reproducibility/results/sensitivity/`.

 
---
