# r2pef report — rdf2pg_cdm

_Generated 2026-07-03 15:50:50_

## Overview

- Source RDF: `/home/zoe/data/dbpedia/dbpedia_geo_200k.nt`
- Source triples: **194,307**
- CPGM nodes: **17,664** ; relations: **44,780**
- Derived triples (|derived_triples(C)|): **388,444**

## Structural overview

**Source RDF**

- 194,307 triples, 17,664 unique subjects, 227 unique predicates
- Object positions: 62,444 IRI, 131,863 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **17,664** (100.0%) ; without `rdf:type`: **0**

**CPGM**

- 17,664 nodes (17,664 full_iri)
- 44,780 edges (44,780 labelled, 0 generic-edge)
- 131,863 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 44.525 s |
| role classification | 10.587 s |
| context build (R, R⁻¹, PGIUs) | 13.563 s |
| IF scoring | 1.059 s |
| IP scoring | 0.405 s |
| IR scoring | 1.805 s |
| **total** | **71.946 s** |

## Scores vs thresholds

```
IP   [███████████████████████████│] 0.995 / 0.950 ✓
IF   [███████████████████████████│] 0.990 / 0.950 ✓
IR   [███████████████░░░░░░░░░░░░│] 0.542 / 0.950 ✗
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 0.9948 | 0.9500 | ✓ | 193,211/194,222 full |
| IF | 0.9897 | 0.9500 | ✓ | undef rate 0.56% |
| IR | 0.5417 | 0.9500 | ✗ | universe=211,971 |

## Fairness verdict

**Passed:** yes

Mandatory metrics:
- IF: 0.9897 — pass
- IP: 0.9948 — pass

Optional metrics:
- IR: 0.5417 — fail

## Lost triples (IP)

### By expected PGIU type

_These triples have no PGIU by definition — they are lost. The "expected PGIU type" is the kind the framework would have produced had the triple been encoded idiomatically for its source role (derived from the role classifier's output)._

| Expected PGIU type | Lost triples | Share |
|---|---|---|
| Unknown | 1,011 | 100.0% |

### By source subject (sampled)

_Subjects ranked by lost-triple count across all predicates. Counts here are computed from the per-predicate samples — when a predicate's losses exceed its sample cap (5), the per-subject counts shown are lower bounds. Useful for spotting subjects that are missing across multiple predicates at once._

- `http://dbpedia.org/resource/Mattel` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/revenue → "5.46E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/ontology/netIncome → "9.03E8"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/resource/Vodafone` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/revenue → "4.3809E10"^^<http://dbpedia.org/datatype/euro>`
    - `http://dbpedia.org/ontology/equity → "5.7816E10"^^<http://dbpedia.org/datatype/euro>`
- `http://dbpedia.org/resource/Ford_Motor_Company` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/operatingIncome → "4.5E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/ontology/assets → "2.57E11"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/resource/Diageo` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/assets → "3.6516E10"^^<http://dbpedia.org/datatype/poundSterling>`
    - `http://dbpedia.org/ontology/equity → "9.514E9"^^<http://dbpedia.org/datatype/poundSterling>`
- `http://dbpedia.org/resource/United_States_Department_of_Commerce` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/budget → "9.3E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/ontology/budget → "1.42E10"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/resource/Hotchkiss_School` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/tuition → "59990.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/ontology/tuition → "50990.0"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/resource/Eton_College` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/fees → "55875.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/ontology/fees → "46296.0"^^<http://dbpedia.org/datatype/poundSterling>`
- `http://dbpedia.org/resource/Fairfield_University` — **1** triple(s) in sample
    - `http://dbpedia.org/ontology/endowment → "3.508E8"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/resource/University_of_Gothenburg` — **1** triple(s) in sample
    - `http://dbpedia.org/ontology/endowment → "4.785E9"^^<http://dbpedia.org/datatype/swedishKrona>`
- `http://dbpedia.org/resource/Yale_Law_School` — **1** triple(s) in sample
    - `http://dbpedia.org/ontology/endowment → "1.2E9"^^<http://dbpedia.org/datatype/usDollar>`

### By predicate

Predicates ranked by number of source triples with no PGIU match:

- `http://dbpedia.org/ontology/endowment` — **616** triple(s)
    - `http://dbpedia.org/resource/Fairfield_University` → `"3.508E8"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/University_of_Gothenburg` → `"4.785E9"^^<http://dbpedia.org/datatype/swedishKrona>`
    - `http://dbpedia.org/resource/Yale_Law_School` → `"1.2E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Wright_State_University` → `"9.55E7"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Albion_College` → `"1.611E8"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/revenue` — **86** triple(s)
    - `http://dbpedia.org/resource/Service_King_Collision_Repair` → `"7.1E8"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Philips` → `"1.9535E10"^^<http://dbpedia.org/datatype/euro>`
    - `http://dbpedia.org/resource/Electronic_Arts` → `"6.99E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Mattel` → `"5.46E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Vodafone` → `"4.3809E10"^^<http://dbpedia.org/datatype/euro>`
- `http://dbpedia.org/ontology/operatingIncome` — **69** triple(s)
    - `http://dbpedia.org/resource/Ford_Motor_Company` → `"4.5E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Sainsbury's` → `"7.09E8"^^<http://dbpedia.org/datatype/poundSterling>`
    - `http://dbpedia.org/resource/BAE_Systems` → `"2.39E9"^^<http://dbpedia.org/datatype/poundSterling>`
    - `http://dbpedia.org/resource/DuPont` → `"2.2E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Sinclair_Broadcast_Group` → `"2.334E8"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/assets` — **67** triple(s)
    - `http://dbpedia.org/resource/BCE_Inc.` → `"6.015E10"^^<http://dbpedia.org/datatype/canadianDollar>`
    - `http://dbpedia.org/resource/Diageo` → `"3.6516E10"^^<http://dbpedia.org/datatype/poundSterling>`
    - `http://dbpedia.org/resource/Fiat_Chrysler_Automobiles` → `"9.687E10"^^<http://dbpedia.org/datatype/euro>`
    - `http://dbpedia.org/resource/Ford_Motor_Company` → `"2.57E11"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Fiat_S.p.A.` → `"8.2119E10"^^<http://dbpedia.org/datatype/euro>`
- `http://dbpedia.org/ontology/netIncome` — **67** triple(s)
    - `http://dbpedia.org/resource/Mattel` → `"9.03E8"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Marriott_International` → `"1.1E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Chevron_Corporation` → `"1.563E10"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/The_Walt_Disney_Company` → `"3.145E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Nippon_TV` → `"22729.0"^^<http://dbpedia.org/datatype/japaneseYen>`
- `http://dbpedia.org/ontology/equity` — **57** triple(s)
    - `http://dbpedia.org/resource/China_Railway` → `"2.150725E12"^^<http://dbpedia.org/datatype/renminbi>`
    - `http://dbpedia.org/resource/Diageo` → `"9.514E9"^^<http://dbpedia.org/datatype/poundSterling>`
    - `http://dbpedia.org/resource/Vodafone` → `"5.7816E10"^^<http://dbpedia.org/datatype/euro>`
    - `http://dbpedia.org/resource/AT&T` → `"183.86"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Shell_plc` → `"1.753E11"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/budget` — **37** triple(s)
    - `http://dbpedia.org/resource/United_States_Department_of_Commerce` → `"9.3E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Socialist_International` → `"1400000.0"^^<http://dbpedia.org/datatype/poundSterling>`
    - `http://dbpedia.org/resource/Internal_Revenue_Service` → `"1.1303E10"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/United_States_Department_of_Commerce` → `"1.42E10"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Executive_Office_of_the_President_of_the_United_States` → `"7.14E8"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/tuition` — **8** triple(s)
    - `http://dbpedia.org/resource/Boston_University_School_of_Law` → `"55700.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Hotchkiss_School` → `"59990.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Deerfield_Academy` → `"61480.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Hotchkiss_School` → `"50990.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/The_Albany_Academy` → `"13500.0"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/assetUnderManagement` — **2** triple(s)
    - `http://dbpedia.org/resource/Temasek_Holdings` → `"6.3E11"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Bain_Capital` → `"1.55E11"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/fees` — **2** triple(s)
    - `http://dbpedia.org/resource/Eton_College` → `"55875.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Eton_College` → `"46296.0"^^<http://dbpedia.org/datatype/poundSterling>`

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 14,579 | 3,085 | 0 | 82.5% |
| NPVR | 87,191 | 0 | 667 | 100.0% |
| TMR | 17,664 | 0 | 0 | 100.0% |
| ELR | 44,780 | 0 | 0 | 100.0% |
| NPKR | 130,852 | 0 | 1,011 | 100.0% |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NR** → realized as `node` and `prop_value` instead of `node` (**3,085 units**)
    - `http://dbpedia.org/resource/Chorley` — handle=`prop_value`, form=`literal`, at `node[http://dbpedia.org/resource/Chorley].property[8].value`, raw=`Chorley`
    - `http://dbpedia.org/resource/Finland` — handle=`prop_value`, form=`literal`, at `node[http://dbpedia.org/resource/Finland].property[14].value`, raw=`Finland`
    - `http://dbpedia.org/resource/Ottawa` — handle=`prop_value`, form=`literal`, at `node[http://dbpedia.org/resource/Ottawa].property[18].value`, raw=`Ottawa`
    - `http://dbpedia.org/resource/Verdun` — handle=`prop_value`, form=`literal`, at `node[http://dbpedia.org/resource/Verdun].property[5].value`, raw=`Verdun`
    - `http://dbpedia.org/resource/Longyan` — handle=`prop_value`, form=`literal`, at `node[http://dbpedia.org/resource/Longyan].property[9].value`, raw=`Longyan`

### Dropped / undefined units (IF)

- Elements without a μ_e match (or with no scorable kind set): **667**
- Occurrences with no covering PGIU: **1,011**

Element-level examples (per role):
- **NPVR** (5 shown)
    - `"1.90098063E8"`
    - `"2.359E8"`
    - `"3.293E8"`
    - `"1.4365E7"`
    - `"2.67E7"`

Occurrence-level examples (per role):
- **NPKR** (5 shown)
    - `['http://dbpedia.org/resource/Fairfield_University', 'http://dbpedia.org/ontology/endowment', '"3.508E8"']`
    - `['http://dbpedia.org/resource/China_Railway', 'http://dbpedia.org/ontology/equity', '"2.150725E12"']`
    - `['http://dbpedia.org/resource/University_of_Gothenburg', 'http://dbpedia.org/ontology/endowment', '"4.785E9"']`
    - `['http://dbpedia.org/resource/BCE_Inc.', 'http://dbpedia.org/ontology/assets', '"6.015E10"']`
    - `['http://dbpedia.org/resource/Service_King_Collision_Repair', 'http://dbpedia.org/ontology/revenue', '"7.1E8"']`

## Identifier retention tier distribution (IR)

- full: **17,664** ; partial: **194,307** ; local: **0** / universe 211,971

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 17,664 | 17,664 | 0 | 0 | 0 | 17,664 | 1.0000 |
| `node.label` | 0 | 0 | 0 | 17,664 | 0 | 17,664 | 0.5000 |
| `node.property.key` | 0 | 0 | 0 | 131,863 | 0 | 131,863 | 0.5000 |
| `edge.label` | 0 | 0 | 0 | 44,780 | 0 | 44,780 | 0.5000 |

Partial-tier handle examples (namespace shortform kept, full IRI not reconstructable):
- `node[http://dbpedia.org/resource/Vranov_nad_Topľou_District].label[0]` resolved=`nss1_AdministrativeRegion` form=`namespace_plus_local`
- `node[http://dbpedia.org/resource/Vranov_nad_Topľou_District].property[0].key` resolved=`nss1_areaTotal` form=`namespace_plus_local`
- `node[http://dbpedia.org/resource/Vranov_nad_Topľou_District].property[1].key` resolved=`nss1_populationTotal` form=`namespace_plus_local`
- `node[http://dbpedia.org/resource/Vranov_nad_Topľou_District].property[2].key` resolved=`nss1_utcOffset` form=`namespace_plus_local`
- `node[http://dbpedia.org/resource/Vranov_nad_Topľou_District].property[3].key` resolved=`nss1_utcOffset` form=`namespace_plus_local`

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

![ip_lost_predicates](visualizations/ip_lost_predicates.png)

