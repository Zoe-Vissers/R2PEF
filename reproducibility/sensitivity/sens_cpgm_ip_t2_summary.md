# r2pef report — CPGM file

_Generated 2026-07-03 10:02:31_

## Overview

- Source RDF: `/home/zoe/rdf-pg-eval/r2pef/examples/testcases_sensitivity/source.ttl`
- Source triples: **5**
- CPGM nodes: **3** ; relations: **2**
- Derived triples (|derived_triples(C)|): **6**

## Structural overview

**Source RDF**

- 5 triples, 2 unique subjects, 5 unique predicates
- Object positions: 3 IRI, 2 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **1** (50.0%) ; without `rdf:type`: **1**

**CPGM**

- 3 nodes (3 full_iri)
- 2 edges (2 labelled, 0 generic-edge)
- 0 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 0.014 s |
| role classification | 0.003 s |
| context build (R, R⁻¹, PGIUs) | 0.001 s |
| IF scoring | 0.000 s |
| IP scoring | 0.000 s |
| IR scoring | 0.000 s |
| **total** | **0.020 s** |

## Scores vs thresholds

```
IP   [█████████████████░░░░░░░░░░│] 0.600 / 0.950 ✗
IF   [███████████████████████████│] 1.000 / 0.950 ✓
IR   [███████████████████████████│] 1.000 / 0.950 ✓
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 0.6000 | 0.9500 | ✗ | 3/5 full |
| IF | 1.0000 | 0.9500 | ✓ | undef rate 36.36% |
| IR | 1.0000 | 0.9500 | ✓ | universe=6 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 1.0000 — pass
- IP: 0.6000 — FAIL

Optional metrics:
- IR: 1.0000 — pass

## Lost triples (IP)

### By expected PGIU type

_These triples have no PGIU by definition — they are lost. The "expected PGIU type" is the kind the framework would have produced had the triple been encoded idiomatically for its source role (derived from the role classifier's output)._

| Expected PGIU type | Lost triples | Share |
|---|---|---|
| Property | 2 | 100.0% |

### By source subject (sampled)

_Subjects ranked by lost-triple count across all predicates. Counts here are computed from the per-predicate samples — when a predicate's losses exceed its sample cap (5), the per-subject counts shown are lower bounds. Useful for spotting subjects that are missing across multiple predicates at once._

- `http://example.org/Movie1` — **2** triple(s) in sample
    - `http://purl.org/dc/elements/1.1/type → "Action"`
    - `http://example.org/title → "Django Unchained"`

### By predicate

Predicates ranked by number of source triples with no PGIU match:

- `http://purl.org/dc/elements/1.1/type` — **1** triple(s)
    - `http://example.org/Movie1` → `"Action"`
- `http://example.org/title` — **1** triple(s)
    - `http://example.org/Movie1` → `"Django Unchained"`

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 3 | 0 | 0 | 100.0% |
| NPVR | 1 | 0 | 2 | 100.0% |
| TMR | 1 | 0 | 0 | 100.0% |
| ELR | 2 | 0 | 0 | 100.0% |
| NPKR | 0 | 0 | 2 | — |

### Dropped / undefined units (IF)

- Elements without a μ_e match (or with no scorable kind set): **2**
- Occurrences with no covering PGIU: **2**

Element-level examples (per role):
- **NPVR** (2 shown)
    - `"Action"`
    - `"Django Unchained"`

Occurrence-level examples (per role):
- **NPKR** (2 shown)
    - `['http://example.org/Movie1', 'http://purl.org/dc/elements/1.1/type', '"Action"']`
    - `['http://example.org/Movie1', 'http://example.org/title', '"Django Unchained"']`

## Identifier retention tier distribution (IR)

- full: **6** ; partial: **0** ; local: **0** / universe 6

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 3 | 3 | 0 | 0 | 0 | 3 | 1.0000 |
| `node.label` | 1 | 1 | 0 | 0 | 0 | 1 | 1.0000 |
| `edge.label` | 2 | 2 | 0 | 0 | 0 | 2 | 1.0000 |

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![ir_tiers](visualizations/ir_tiers.png)

![ip_lost_predicates](visualizations/ip_lost_predicates.png)

