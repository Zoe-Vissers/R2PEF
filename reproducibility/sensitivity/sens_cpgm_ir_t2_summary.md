# r2pef report — CPGM file

_Generated 2026-07-03 10:03:02_

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

- 3 nodes (3 local_only)
- 2 edges (2 labelled, 0 generic-edge)
- 2 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 0.016 s |
| role classification | 0.003 s |
| context build (R, R⁻¹, PGIUs) | 0.001 s |
| IF scoring | 0.000 s |
| IP scoring | 0.000 s |
| IR scoring | 0.000 s |
| **total** | **0.023 s** |

## Scores vs thresholds

```
IP   [███████████████████████████│] 1.000 / 0.950 ✓
IF   [███████████████████████████│] 1.000 / 0.950 ✓
IR   [░░░░░░░░░░░░░░░░░░░░░░░░░░░│] 0.000 / 0.950 ✗
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 1.0000 | 0.9500 | ✓ | 5/5 full |
| IF | 1.0000 | 0.9500 | ✓ | undef rate 0.00% |
| IR | 0.0000 | 0.9500 | ✗ | universe=8 |

## Fairness verdict

**Passed:** yes

Mandatory metrics:
- IF: 1.0000 — pass
- IP: 1.0000 — pass

Optional metrics:
- IR: 0.0000 — fail

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 3 | 0 | 0 | 100.0% |
| NPVR | 3 | 0 | 0 | 100.0% |
| TMR | 1 | 0 | 0 | 100.0% |
| ELR | 2 | 0 | 0 | 100.0% |
| NPKR | 2 | 0 | 0 | 100.0% |

## Identifier retention tier distribution (IR)

- full: **0** ; partial: **0** ; local: **8** / universe 8

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 0 | 0 | 0 | 0 | 3 | 3 | 0.0000 |
| `node.label` | 0 | 0 | 0 | 0 | 1 | 1 | 0.0000 |
| `node.property.key` | 0 | 0 | 0 | 0 | 2 | 2 | 0.0000 |
| `edge.label` | 0 | 0 | 0 | 0 | 2 | 2 | 0.0000 |

Local-tier handle examples (bare local name, namespace discarded):
- `node[http://example.org/Movie1]` resolved=`Movie1` form=`local_only`
- `node[http://example.org/Movie1].label[0]` resolved=`Movie` form=`local_only`
- `node[http://example.org/Movie1].property[0].key` resolved=`title` form=`local_only`
- `node[http://example.org/Movie1].property[1].key` resolved=`type` form=`local_only`
- `node[http://example.org/Oscar2013]` resolved=`Oscar2013` form=`local_only`

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![ir_tiers](visualizations/ir_tiers.png)

