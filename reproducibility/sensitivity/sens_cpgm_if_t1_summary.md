# r2pef report — CPGM file

_Generated 2026-07-03 10:02:40_

## Overview

- Source RDF: `/home/zoe/rdf-pg-eval/r2pef/examples/testcases_sensitivity/source.ttl`
- Source triples: **5**
- CPGM nodes: **4** ; relations: **3**
- Derived triples (|derived_triples(C)|): **10**

## Structural overview

**Source RDF**

- 5 triples, 2 unique subjects, 5 unique predicates
- Object positions: 3 IRI, 2 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **1** (50.0%) ; without `rdf:type`: **1**

**CPGM**

- 4 nodes (4 full_iri)
- 3 edges (3 labelled, 0 generic-edge)
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
| IR | 1.0000 | 0.9500 | ✓ | universe=9 |

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
| NPVR | 2 | 1 | 0 | 66.7% |
| TMR | 0 | 1 | 0 | 0.0% |
| ELR | 2 | 0 | 0 | 100.0% |
| NPKR | 2 | 0 | 0 | 100.0% |

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NPVR** → realized as `node` instead of `prop_value` (**1 units**)
    - `http://example.org/Movie`

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **TMR** → realized as `Edge` instead of `Label` (**1 occurrence(s)**)
    - `['http://example.org/Movie1', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://example.org/Movie']`

## Identifier retention tier distribution (IR)

- full: **9** ; partial: **0** ; local: **0** / universe 9

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 4 | 4 | 0 | 0 | 0 | 4 | 1.0000 |
| `node.property.key` | 2 | 2 | 0 | 0 | 0 | 2 | 1.0000 |
| `edge.label` | 3 | 3 | 0 | 0 | 0 | 3 | 1.0000 |

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

