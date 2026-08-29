# r2pef report — kg2pg

_Generated 2026-07-03 15:30:11_

## Overview

- Source RDF: `/home/zoe/data/bsbm/bsbm_100k.nt`
- Source triples: **100,075**
- CPGM nodes: **72,073** ; relations: **89,278**
- Derived triples (|derived_triples(C)|): **236,046**

## Structural overview

**Source RDF**

- 100,075 triples, 10,032 unique subjects, 40 unique predicates
- Object positions: 47,948 IRI, 52,127 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **10,032** (100.0%) ; without `rdf:type`: **0**

**CPGM**

- 72,073 nodes (10,033 full_iri, 62,040 literal-form)
- 89,278 edges (89,278 labelled, 0 generic-edge)
- 186,127 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 88.816 s |
| role classification | 5.389 s |
| context build (R, R⁻¹, PGIUs) | 10.090 s |
| IF scoring | 0.578 s |
| IP scoring | 0.084 s |
| IR scoring | 0.536 s |
| **total** | **105.496 s** |

## Scores vs thresholds

```
IP   [███████████████████████████│] 1.000 / 0.950 ✓
IF   [█████████░░░░░░░░░░░░░░░░░░│] 0.317 / 0.950 ✗
IR   [█████████████████████░░░░░░│] 0.768 / 0.950 ✗
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 1.0000 | 0.9500 | ✓ | 100,075/100,075 full |
| IF | 0.3167 | 0.9500 | ✗ | undef rate 0.00% |
| IR | 0.7676 | 0.9500 | ✗ | universe=224,282 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.3167 — FAIL
- IP: 1.0000 — pass

Optional metrics:
- IR: 0.7676 — fail

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 4,895 | 5,137 | 0 | 48.8% |
| NPVR | 8 | 23,062 | 0 | 0.0% |
| TMR | 10,032 | 0 | 0 | 100.0% |
| ELR | 27,238 | 765 | 0 | 97.3% |
| NPKR | 0 | 62,040 | 0 | 0.0% |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NR** → realized as `literal_node`, `node` and `prop_value` instead of `node` (**4,963 units**)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer929` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_16494]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer2970` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_28745]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer2239` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_24354]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4445` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_37595]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3862` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_34097]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
- **NR** → realized as `node` and `node_label` instead of `node` (**37 units**)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType25` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer4/Product159].label[1]`, raw=`ns1_ProductType25`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType8` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer3/Product127].label[2]`, raw=`ns1_ProductType8`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType17` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer3/Product134].label[2]`, raw=`ns1_ProductType17`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType16` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer2/Product71].label[1]`, raw=`ns1_ProductType16`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType28` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer6/Product251].label[2]`, raw=`ns1_ProductType28`

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **NPKR** → realized as `Edge` instead of `Property` (**4,941 occurrence(s)**)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature443', 'http://www.w3.org/2000/01/rdf-schema#label', '"wotted pecul…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review255', 'http://purl.org/dc/elements/1.1/title', '"ficti…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer207', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocab…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer2246', 'http://purl.org/dc/elements/1.1/date', '"2008-05-07…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer2904', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
- **ELR** → realized as `Label` instead of `Edge` (**59 occurrence(s)**)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer5/Product194', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer2/Product66', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer5/Product207', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer3/Product106', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer3/Product117', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'…`

## Identifier retention tier distribution (IR)

- full: **172,155** ; partial: **0** ; local: **52,127** / universe 224,282

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 10,033 | 10,033 | 0 | 0 | 0 | 10,033 | 1.0000 |
| `node.label` | 10,797 | 0 | 10,797 | 0 | 52,127 | 62,924 | 0.1716 |
| `node.property.key` | 7 | 7 | 0 | 0 | 0 | 7 | 1.0000 |
| `node.property.value` | 62,040 | 62,040 | 0 | 0 | 0 | 62,040 | 1.0000 |
| `edge.label` | 89,278 | 0 | 89,278 | 0 | 0 | 89,278 | 1.0000 |

Local-tier handle examples (bare local name, namespace discarded):
- `node[lit_kg2pg_0].label[0]` resolved=`string` form=`local_only`
- `node[lit_kg2pg_1].label[0]` resolved=`string` form=`local_only`
- `node[lit_kg2pg_3].label[0]` resolved=`date` form=`local_only`
- `node[lit_kg2pg_4].label[0]` resolved=`string` form=`local_only`
- `node[lit_kg2pg_5].label[0]` resolved=`string` form=`local_only`

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

