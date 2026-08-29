# r2pef report — CPGM file

_Generated 2026-07-03 10:02:57_

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

- 3 nodes (3 namespace_plus_local)
- 2 edges (2 labelled, 0 generic-edge)
- 2 properties total

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
| **total** | **0.021 s** |

## Scores vs thresholds

```
IP   [███████████████████████████│] 1.000 / 0.950 ✓
IF   [███████████████████████████│] 1.000 / 0.950 ✓
IR   [██████████████░░░░░░░░░░░░░│] 0.500 / 0.950 ✗
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 1.0000 | 0.9500 | ✓ | 5/5 full |
| IF | 1.0000 | 0.9500 | ✓ | undef rate 0.00% |
| IR | 0.5000 | 0.9500 | ✗ | universe=8 |

## Fairness verdict

**Passed:** yes

Mandatory metrics:
- IF: 1.0000 — pass
- IP: 1.0000 — pass

Optional metrics:
- IR: 0.5000 — fail

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 3 | 0 | 0 | 100.0% |
| NPVR | 3 | 0 | 0 | 100.0% |
| TMR | 1 | 0 | 0 | 100.0% |
| ELR | 2 | 0 | 0 | 100.0% |
| NPKR | 2 | 0 | 0 | 100.0% |

## Identifier retention tier distribution (IR)

- full: **0** ; partial: **8** ; local: **0** / universe 8

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 0 | 0 | 0 | 3 | 0 | 3 | 0.5000 |
| `node.label` | 0 | 0 | 0 | 1 | 0 | 1 | 0.5000 |
| `node.property.key` | 0 | 0 | 0 | 2 | 0 | 2 | 0.5000 |
| `edge.label` | 0 | 0 | 0 | 2 | 0 | 2 | 0.5000 |

Partial-tier handle examples (namespace shortform kept, full IRI not reconstructable):
- `node[http://example.org/Movie1]` resolved=`ns1_Movie1` form=`namespace_plus_local`
- `node[http://example.org/Movie1].label[0]` resolved=`ns1_Movie` form=`namespace_plus_local`
- `node[http://example.org/Movie1].property[0].key` resolved=`ns1_title` form=`namespace_plus_local`
- `node[http://example.org/Movie1].property[1].key` resolved=`ns2_type` form=`namespace_plus_local`
- `node[http://example.org/Oscar2013]` resolved=`ns1_Oscar2013` form=`namespace_plus_local`

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![ir_tiers](visualizations/ir_tiers.png)

