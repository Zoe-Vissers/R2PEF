# r2pef report — CPGM file

_Generated 2026-07-03 10:02:53_

## Overview

- Source RDF: `/home/zoe/rdf-pg-eval/r2pef/examples/testcases_sensitivity/source.ttl`
- Source triples: **5**
- CPGM nodes: **3** ; relations: **2**
- Derived triples (|derived_triples(C)|): **10**

## Structural overview

**Source RDF**

- 5 triples, 2 unique subjects, 5 unique predicates
- Object positions: 3 IRI, 2 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **1** (50.0%) ; without `rdf:type`: **1**

**CPGM**

- 3 nodes (3 full_iri)
- 2 edges (0 labelled, 2 generic-edge)
- 4 properties total

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
IP   [███████████████████████████│] 1.000 / 0.950 ✓
IF   [███████████████████████░░░░│] 0.818 / 0.950 ✗
IR   [███████████████████████████│] 1.000 / 0.950 ✓
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 1.0000 | 0.9500 | ✓ | 5/5 full |
| IF | 0.8182 | 0.9500 | ✗ | undef rate 0.00% |
| IR | 1.0000 | 0.9500 | ✓ | universe=8 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.8182 — FAIL
- IP: 1.0000 — pass

Optional metrics:
- IR: 1.0000 — pass

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 3 | 0 | 0 | 100.0% |
| NPVR | 3 | 0 | 0 | 100.0% |
| TMR | 1 | 0 | 0 | 100.0% |
| ELR | 0 | 2 | 0 | 0.0% |
| NPKR | 2 | 0 | 0 | 100.0% |

## Non-idiomatic encodings (IF)

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **ELR** → realized as `Generic-edge` instead of `Edge` (**2 occurrence(s)**)
    - `['http://example.org/Oscar2013', 'http://example.org/awardedTo', 'http://example.org/Tarantino']`
    - `['http://example.org/Movie1', 'http://example.org/director', 'http://example.org/Tarantino']`

## Identifier retention tier distribution (IR)

- full: **8** ; partial: **0** ; local: **0** / universe 8

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 3 | 3 | 0 | 0 | 0 | 3 | 1.0000 |
| `node.label` | 1 | 1 | 0 | 0 | 0 | 1 | 1.0000 |
| `node.property.key` | 2 | 2 | 0 | 0 | 0 | 2 | 1.0000 |
| `edge.property.value` | 2 | 2 | 0 | 0 | 0 | 2 | 1.0000 |

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![ir_tiers](visualizations/ir_tiers.png)

