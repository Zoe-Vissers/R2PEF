# r2pef report — rdf2pg_cdm

_Generated 2026-07-03 15:23:38_

## Overview

- Source RDF: `/home/zoe/data/bsbm/bsbm_100k.nt`
- Source triples: **100,075**
- CPGM nodes: **15,153** ; relations: **37,151**
- Derived triples (|derived_triples(C)|): **200,150**

## Structural overview

**Source RDF**

- 100,075 triples, 10,032 unique subjects, 40 unique predicates
- Object positions: 47,948 IRI, 52,127 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **10,032** (100.0%) ; without `rdf:type`: **0**

**CPGM**

- 15,153 nodes (15,153 full_iri)
- 37,151 edges (37,151 labelled, 0 generic-edge)
- 52,127 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 22.992 s |
| role classification | 4.977 s |
| context build (R, R⁻¹, PGIUs) | 7.715 s |
| IF scoring | 0.493 s |
| IP scoring | 0.206 s |
| IR scoring | 0.212 s |
| **total** | **36.597 s** |

## Scores vs thresholds

```
IP   [███████████████████████████│] 0.949 / 0.950 ✗
IF   [████████████████████████░░░│] 0.871 / 0.950 ✗
IR   [████████████████░░░░░░░░░░░│] 0.566 / 0.950 ✗
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 0.9490 | 0.9500 | ✗ | 94,975/100,075 full |
| IF | 0.8712 | 0.9500 | ✗ | undef rate 7.65% |
| IR | 0.5658 | 0.9500 | ✗ | universe=115,228 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.8712 — FAIL
- IP: 0.9490 — FAIL

Optional metrics:
- IR: 0.5658 — fail

## Lost triples (IP)

### By expected PGIU type

_These triples have no PGIU by definition — they are lost. The "expected PGIU type" is the kind the framework would have produced had the triple been encoded idiomatically for its source role (derived from the role classifier's output)._

| Expected PGIU type | Lost triples | Share |
|---|---|---|
| Unknown | 5,100 | 100.0% |

### By source subject (sampled)

_Subjects ranked by lost-triple count across all predicates. Counts here are computed from the per-predicate samples — when a predicate's losses exceed its sample cap (5), the per-subject counts shown are lower bounds. Useful for spotting subjects that are missing across multiple predicates at once._

- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3514` — **1** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price → "9263.63"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer2218` — **1** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price → "9856.02"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4921` — **1** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price → "336.29"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1725` — **1** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price → "6997.35"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1344` — **1** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price → "8661.24"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`

### By predicate

Predicates ranked by number of source triples with no PGIU match:

- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price` — **5,100** triple(s)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3514` → `"9263.63"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer2218` → `"9856.02"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4921` → `"336.29"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1725` → `"6997.35"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1344` → `"8661.24"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 9,995 | 37 | 0 | 99.6% |
| NPVR | 12,861 | 5,121 | 5,088 | 71.5% |
| TMR | 10,032 | 0 | 0 | 100.0% |
| ELR | 27,238 | 765 | 0 | 97.3% |
| NPKR | 47,027 | 9,913 | 5,100 | 82.6% |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NPVR** → realized as `node` instead of `prop_value` (**4,963 units**)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer2793/`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer558/`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer2274/`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1753/` — handle=`node`, form=`full_iri`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1753]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3087/` — handle=`node`, form=`full_iri`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3087]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
- **NR** → realized as `node` and `node_label` instead of `node` (**37 units**)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType27` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer3/Product128].label[1]`, raw=`nss3_ProductType27`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType6` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product12].label[1]`, raw=`nss3_ProductType6`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType22` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer4/Product166].label[1]`, raw=`nss3_ProductType22`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType3` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer5/Product201].label[2]`, raw=`nss3_ProductType3`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType20` — handle=`node_label`, form=`namespace_plus_local`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer2/Product69].label[1]`, raw=`nss3_ProductType20`

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **NPKR** → realized as `Edge` instead of `Property` (**4,650 occurrence(s)**)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer2146', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer818', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocab…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature844', 'http://purl.org/dc/elements/1.1/publisher', 'http://www4.wi…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review1263', 'http://purl.org/dc/elements/1.1/publisher', 'h…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1885', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
- **ELR** → realized as `Label` instead of `Edge` (**350 occurrence(s)**)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product2', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', …`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product8', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', …`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer4/Product142', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product47', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer6/Product255', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'…`

### Dropped / undefined units (IF)

- Elements without a μ_e match (or with no scorable kind set): **5,000**
- Occurrences with no covering PGIU: **5,000**

Element-level examples (per role):
- **NPVR** (5 shown)
    - `"4427.18"`
    - `"3095.40"`
    - `"1860.69"`
    - `"8404.13"`
    - `"9381.49"`

Occurrence-level examples (per role):
- **NPKR** (5 shown)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3514', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer2218', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4921', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1725', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1344', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`

## Identifier retention tier distribution (IR)

- full: **15,153** ; partial: **100,075** ; local: **0** / universe 115,228

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 15,153 | 15,153 | 0 | 0 | 0 | 15,153 | 1.0000 |
| `node.label` | 0 | 0 | 0 | 10,797 | 0 | 10,797 | 0.5000 |
| `node.property.key` | 0 | 0 | 0 | 52,127 | 0 | 52,127 | 0.5000 |
| `edge.label` | 0 | 0 | 0 | 37,151 | 0 | 37,151 | 0.5000 |

Partial-tier handle examples (namespace shortform kept, full IRI not reconstructable):
- `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature1314].label[0]` resolved=`nss1_ProductFeature` form=`namespace_plus_local`
- `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature1314].property[0].key` resolved=`rdfs_label` form=`namespace_plus_local`
- `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature1314].property[1].key` resolved=`rdfs_comment` form=`namespace_plus_local`
- `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature1314].property[2].key` resolved=`nss2_date` form=`namespace_plus_local`
- `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer2751].label[0]` resolved=`nss1_Offer` form=`namespace_plus_local`

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

![ip_lost_predicates](visualizations/ip_lost_predicates.png)

