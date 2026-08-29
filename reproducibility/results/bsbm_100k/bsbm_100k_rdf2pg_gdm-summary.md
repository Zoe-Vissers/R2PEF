# r2pef report — rdf2pg_gdm

_Generated 2026-07-03 15:19:02_

## Overview

- Source RDF: `/home/zoe/data/bsbm/bsbm_100k.nt`
- Source triples: **100,075**
- CPGM nodes: **67,288** ; relations: **100,075**
- Derived triples (|derived_triples(C)|): **200,150**

## Structural overview

**Source RDF**

- 100,075 triples, 10,032 unique subjects, 40 unique predicates
- Object positions: 47,948 IRI, 52,127 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **10,032** (100.0%) ; without `rdf:type`: **0**

**CPGM**

- 67,288 nodes (15,161 full_iri, 52,127 literal-form)
- 100,075 edges (0 labelled, 100,075 generic-edge)
- 204,329 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 93.497 s |
| role classification | 5.408 s |
| context build (R, R⁻¹, PGIUs) | 7.791 s |
| IF scoring | 0.570 s |
| IP scoring | 0.084 s |
| IR scoring | 0.487 s |
| **total** | **107.840 s** |

## Scores vs thresholds

```
IP   [███████████████████████████│] 0.949 / 0.950 ✗
IF   [██░░░░░░░░░░░░░░░░░░░░░░░░░│] 0.082 / 0.950 ✗
IR   [███████████████████████████│] 1.000 / 0.950 ✓
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 0.9490 | 0.9500 | ✗ | 94,975/100,075 full |
| IF | 0.0816 | 0.9500 | ✗ | undef rate 7.65% |
| IR | 1.0000 | 0.9500 | ✓ | universe=167,363 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.0816 — FAIL
- IP: 0.9490 — FAIL

Optional metrics:
- IR: 1.0000 — pass

## Lost triples (IP)

### By expected PGIU type

_These triples have no PGIU by definition — they are lost. The "expected PGIU type" is the kind the framework would have produced had the triple been encoded idiomatically for its source role (derived from the role classifier's output)._

| Expected PGIU type | Lost triples | Share |
|---|---|---|
| Unknown | 5,100 | 100.0% |

### By source subject (sampled)

_Subjects ranked by lost-triple count across all predicates. Counts here are computed from the per-predicate samples — when a predicate's losses exceed its sample cap (5), the per-subject counts shown are lower bounds. Useful for spotting subjects that are missing across multiple predicates at once._

- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3640` — **1** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price → "2579.02"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4394` — **1** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price → "3778.41"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer65` — **1** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price → "1857.69"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4340` — **1** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price → "4023.60"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3868` — **1** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price → "4635.92"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`

### By predicate

Predicates ranked by number of source triples with no PGIU match:

- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price` — **5,100** triple(s)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3640` → `"2579.02"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4394` → `"3778.41"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer65` → `"1857.69"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4340` → `"4023.60"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3868` → `"4635.92"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 10,032 | 0 | 0 | 100.0% |
| NPVR | 0 | 17,982 | 5,088 | 0.0% |
| TMR | 0 | 10,032 | 0 | 0.0% |
| ELR | 0 | 28,003 | 0 | 0.0% |
| NPKR | 0 | 56,940 | 5,100 | 0.0% |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NPVR** → realized as `literal_node` and `prop_value` instead of `prop_value` (**3,535 units**)
    - `"valences absconders soughing pointedly speciating sowable demobilizes pools extras obovate invaded refrying saccharinely uneaten stypsis g…` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_133005]`, raw=`valences absconders soughing pointedly speciating sowable d…`
    - `"957"` — handle=`prop_value`, form=`literal`, at `node[lit_gdm_25650].property[0].value`, raw=`957`
    - `"394"` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_27111]`, raw=`394`
    - `"2008-05-21T00:00:00"` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_81301]`, raw=`2008-05-21T00:00:00`
    - `"sailable ghettoing"` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_7107]`, raw=`sailable ghettoing`
- **NPVR** → realized as `node` instead of `prop_value` (**1,465 units**)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1924/`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer660/` — handle=`node`, form=`full_iri`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer660]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer2667/` — handle=`node`, form=`full_iri`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer2667]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3846/` — handle=`node`, form=`full_iri`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3846]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3257/` — handle=`node`, form=`full_iri`, at `node[http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3257]`, raw=`http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/da…`

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **NPKR** → realized as `Generic-edge` instead of `Property` (**2,997 occurrence(s)**)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review407', 'http://purl.org/stuff/rev#text', '"overtime poe…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review819', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer3/Product119', 'http://www.w3.org/2000/01/rdf-schema#label', '"p…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer2066', 'http://purl.org/dc/elements/1.1/date', '"2008-03-29…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer3/Product130', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/v…`
- **ELR** → realized as `Generic-edge` instead of `Edge` (**1,517 occurrence(s)**)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer918', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocab…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3705', 'http://purl.org/dc/elements/1.1/publisher', 'http:/…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review321', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1220', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4088', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
- **TMR** → realized as `Generic-edge` instead of `Label` (**486 occurrence(s)**)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4775', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', '…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review1533', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#typ…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer803', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'h…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer2433', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', '…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review1992', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#typ…`

### Dropped / undefined units (IF)

- Elements without a μ_e match (or with no scorable kind set): **5,000**
- Occurrences with no covering PGIU: **5,000**

Element-level examples (per role):
- **NPVR** (5 shown)
    - `"2573.89"`
    - `"4155.22"`
    - `"6656.19"`
    - `"8334.83"`
    - `"8720.06"`

Occurrence-level examples (per role):
- **NPKR** (5 shown)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3640', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4394', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer65', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabu…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4340', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3868', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`

## Identifier retention tier distribution (IR)

- full: **167,363** ; partial: **0** ; local: **0** / universe 167,363

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 15,161 | 15,161 | 0 | 0 | 0 | 15,161 | 1.0000 |
| `node.property.value` | 52,127 | 52,127 | 0 | 0 | 0 | 52,127 | 1.0000 |
| `edge.property.value` | 100,075 | 100,075 | 0 | 0 | 0 | 100,075 | 1.0000 |

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

![ip_lost_predicates](visualizations/ip_lost_predicates.png)

