# r2pef report — kg2pg

_Generated 2026-07-03 15:26:12_

## Overview

- Source RDF: `/home/zoe/data/bsbm/bsbm_100k.nt`
- Source triples: **100,075**
- CPGM nodes: **25,046** ; relations: **42,251**
- Derived triples (|derived_triples(C)|): **210,340**

## Structural overview

**Source RDF**

- 100,075 triples, 10,032 unique subjects, 40 unique predicates
- Object positions: 47,948 IRI, 52,127 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **10,032** (100.0%) ; without `rdf:type`: **0**

**CPGM**

- 25,046 nodes (10,033 full_iri, 15,013 literal-form)
- 42,251 edges (42,251 labelled, 0 generic-edge)
- 92,073 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 39.041 s |
| role classification | 4.441 s |
| context build (R, R⁻¹, PGIUs) | 8.381 s |
| IF scoring | 0.473 s |
| IP scoring | 0.075 s |
| IR scoring | 0.287 s |
| **total** | **52.699 s** |

## Scores vs thresholds

```
IP   [███████████████████████████│] 1.000 / 0.950 ✓
IF   [█████████████████████░░░░░░│] 0.766 / 0.950 ✗
IR   [███████████████████████████│] 0.961 / 0.950 ✓
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 1.0000 | 0.9500 | ✓ | 100,075/100,075 full |
| IF | 0.7663 | 0.9500 | ✗ | undef rate 0.00% |
| IR | 0.9608 | 0.9500 | ✓ | universe=130,228 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.7663 — FAIL
- IP: 1.0000 — pass

Optional metrics:
- IR: 0.9608 — pass

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 4,895 | 5,137 | 0 | 48.8% |
| NPVR | 12,861 | 10,209 | 0 | 55.7% |
| TMR | 10,032 | 0 | 0 | 100.0% |
| ELR | 27,238 | 765 | 0 | 97.3% |
| NPKR | 47,027 | 15,013 | 0 | 75.8% |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NR** → realized as `literal_node`, `node` and `prop_value` instead of `node` (**4,964 units**)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor3/Offer4953` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_11914]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1832` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_5668]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3974` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_9954]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer652` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_3308]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3085` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_8176]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
- **NR** → realized as `node` and `node_label` instead of `node` (**36 units**)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType36`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType1` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer5/Product201].label[0]`, raw=`ns1_ProductType1`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType37`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType4` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product27].label[1]`, raw=`ns1_ProductType4`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType7` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer4/Product153].label[2]`, raw=`ns1_ProductType7`

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **NPKR** → realized as `Edge` instead of `Property` (**4,755 occurrence(s)**)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3414', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer249', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocab…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer2239', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review1555', 'http://purl.org/dc/elements/1.1/publisher', 'h…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature233', 'http://purl.org/dc/elements/1.1/publisher', 'http://www4.wi…`
- **ELR** → realized as `Label` instead of `Edge` (**245 occurrence(s)**)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product41', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer2/Product83', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product34', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product54', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer5/Product204', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'…`

## Identifier retention tier distribution (IR)

- full: **125,128** ; partial: **0** ; local: **5,100** / universe 130,228

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 10,033 | 10,033 | 0 | 0 | 0 | 10,033 | 1.0000 |
| `node.label` | 10,797 | 0 | 10,797 | 0 | 5,100 | 15,897 | 0.6792 |
| `node.property.key` | 47,034 | 7 | 47,027 | 0 | 0 | 47,034 | 1.0000 |
| `node.property.value` | 15,013 | 15,013 | 0 | 0 | 0 | 15,013 | 1.0000 |
| `edge.label` | 42,251 | 0 | 42,251 | 0 | 0 | 42,251 | 1.0000 |

Local-tier handle examples (bare local name, namespace discarded):
- `node[lit_kg2pg_2005].label[0]` resolved=`USD` form=`local_only`
- `node[lit_kg2pg_2007].label[0]` resolved=`USD` form=`local_only`
- `node[lit_kg2pg_2009].label[0]` resolved=`USD` form=`local_only`
- `node[lit_kg2pg_2011].label[0]` resolved=`USD` form=`local_only`
- `node[lit_kg2pg_2013].label[0]` resolved=`USD` form=`local_only`

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

