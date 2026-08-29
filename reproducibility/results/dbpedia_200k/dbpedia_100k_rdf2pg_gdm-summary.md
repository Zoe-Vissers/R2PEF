# r2pef report — rdf2pg_gdm

_Generated 2026-07-03 15:41:36_

## Overview

- Source RDF: `/home/zoe/data/dbpedia/dbpedia_geo_200k.nt`
- Source triples: **194,307**
- CPGM nodes: **149,543** ; relations: **194,307**
- Derived triples (|derived_triples(C)|): **388,444**

## Structural overview

**Source RDF**

- 194,307 triples, 17,664 unique subjects, 227 unique predicates
- Object positions: 62,444 IRI, 131,863 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **17,664** (100.0%) ; without `rdf:type`: **0**

**CPGM**

- 149,543 nodes (17,680 full_iri, 131,863 literal-form)
- 194,307 edges (0 labelled, 194,307 generic-edge)
- 458,033 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 188.328 s |
| role classification | 10.853 s |
| context build (R, R⁻¹, PGIUs) | 15.090 s |
| IF scoring | 1.204 s |
| IP scoring | 0.175 s |
| IR scoring | 0.928 s |
| **total** | **216.581 s** |

## Scores vs thresholds

```
IP   [███████████████████████████│] 0.995 / 0.950 ✓
IF   [█░░░░░░░░░░░░░░░░░░░░░░░░░░│] 0.049 / 0.950 ✗
IR   [███████████████████████████│] 1.000 / 0.950 ✓
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 0.9948 | 0.9500 | ✓ | 193,211/194,222 full |
| IF | 0.0489 | 0.9500 | ✗ | undef rate 0.56% |
| IR | 1.0000 | 0.9500 | ✓ | universe=343,850 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.0489 — FAIL
- IP: 0.9948 — pass

Optional metrics:
- IR: 1.0000 — pass

## Lost triples (IP)

### By expected PGIU type

_These triples have no PGIU by definition — they are lost. The "expected PGIU type" is the kind the framework would have produced had the triple been encoded idiomatically for its source role (derived from the role classifier's output)._

| Expected PGIU type | Lost triples | Share |
|---|---|---|
| Unknown | 1,011 | 100.0% |

### By source subject (sampled)

_Subjects ranked by lost-triple count across all predicates. Counts here are computed from the per-predicate samples — when a predicate's losses exceed its sample cap (5), the per-subject counts shown are lower bounds. Useful for spotting subjects that are missing across multiple predicates at once._

- `http://dbpedia.org/resource/Sinclair_Broadcast_Group` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/revenue → "2.73E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/ontology/equity → "5.579E8"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/resource/Starbucks` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/operatingIncome → "4.87E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/ontology/assets → "3.139E10"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/resource/Fiat_Chrysler_Automobiles` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/assets → "9.687E10"^^<http://dbpedia.org/datatype/euro>`
    - `http://dbpedia.org/ontology/equity → "2.49E10"^^<http://dbpedia.org/datatype/euro>`
- `http://dbpedia.org/resource/BP` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/assets → "2.8727E11"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/ontology/equity → "9.044E10"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/resource/Siemens` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/assets → "1.39608E11"^^<http://dbpedia.org/datatype/euro>`
    - `http://dbpedia.org/ontology/netIncome → "6.697E9"^^<http://dbpedia.org/datatype/euro>`
- `http://dbpedia.org/resource/Boston_University_School_of_Law` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/tuition → "55700.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/ontology/tuition → "1282.0"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/resource/Eton_College` — **2** triple(s) in sample
    - `http://dbpedia.org/ontology/fees → "55875.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/ontology/fees → "46296.0"^^<http://dbpedia.org/datatype/poundSterling>`
- `http://dbpedia.org/resource/Drake_University` — **1** triple(s) in sample
    - `http://dbpedia.org/ontology/endowment → "2.198E8"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/resource/Kalamazoo_College` — **1** triple(s) in sample
    - `http://dbpedia.org/ontology/endowment → "2.436E8"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/resource/Texas_State_University` — **1** triple(s) in sample
    - `http://dbpedia.org/ontology/endowment → "3.42E8"^^<http://dbpedia.org/datatype/usDollar>`

### By predicate

Predicates ranked by number of source triples with no PGIU match:

- `http://dbpedia.org/ontology/endowment` — **616** triple(s)
    - `http://dbpedia.org/resource/Drake_University` → `"2.198E8"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Kalamazoo_College` → `"2.436E8"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Texas_State_University` → `"3.42E8"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Sarah_Lawrence_College` → `"1.102E8"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/University_of_Turin` → `"4.6E8"^^<http://dbpedia.org/datatype/euro>`
- `http://dbpedia.org/ontology/revenue` — **86** triple(s)
    - `http://dbpedia.org/resource/Nippon_TV` → `"326423.0"^^<http://dbpedia.org/datatype/japaneseYen>`
    - `http://dbpedia.org/resource/RAI` → `"2.493E9"^^<http://dbpedia.org/datatype/euro>`
    - `http://dbpedia.org/resource/Universal_Pictures` → `"4.239E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Philips` → `"1.9535E10"^^<http://dbpedia.org/datatype/euro>`
    - `http://dbpedia.org/resource/Sinclair_Broadcast_Group` → `"2.73E9"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/operatingIncome` — **69** triple(s)
    - `http://dbpedia.org/resource/AT&T` → `"2.335E10"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/WPP_plc` → `"1252.0"^^<http://dbpedia.org/datatype/poundSterling>`
    - `http://dbpedia.org/resource/Starbucks` → `"4.87E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Hasbro` → `"2.204E8"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Danone` → `"3.84E9"^^<http://dbpedia.org/datatype/euro>`
- `http://dbpedia.org/ontology/assets` — **67** triple(s)
    - `http://dbpedia.org/resource/Fiat_Chrysler_Automobiles` → `"9.687E10"^^<http://dbpedia.org/datatype/euro>`
    - `http://dbpedia.org/resource/BP` → `"2.8727E11"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Starbucks` → `"3.139E10"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Siemens` → `"1.39608E11"^^<http://dbpedia.org/datatype/euro>`
    - `http://dbpedia.org/resource/Warner_Music_Group` → `"7.828E9"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/netIncome` — **67** triple(s)
    - `http://dbpedia.org/resource/McDonald's` → `"7.545E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Apple_Inc.` → `"9.98E10"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Tesco` → `"6.147E9"^^<http://dbpedia.org/datatype/poundSterling>`
    - `http://dbpedia.org/resource/Siemens` → `"6.697E9"^^<http://dbpedia.org/datatype/euro>`
    - `http://dbpedia.org/resource/EBay` → `"1.361E10"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/equity` — **57** triple(s)
    - `http://dbpedia.org/resource/BP` → `"9.044E10"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Nestlé` → `"5.373E10"^^<http://dbpedia.org/datatype/swissFranc>`
    - `http://dbpedia.org/resource/Fiat_Chrysler_Automobiles` → `"2.49E10"^^<http://dbpedia.org/datatype/euro>`
    - `http://dbpedia.org/resource/Sinclair_Broadcast_Group` → `"5.579E8"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Wells_Fargo` → `"1.901E11"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/budget` — **37** triple(s)
    - `http://dbpedia.org/resource/Department_for_Business,_Innovation_and_Skills` → `"1.65E10"^^<http://dbpedia.org/datatype/poundSterling>`
    - `http://dbpedia.org/resource/Ministry_of_Education_(Malaysia)` → `"4.39884681E10"^^<http://dbpedia.org/datatype/malaysianRinggit>`
    - `http://dbpedia.org/resource/United_States_Department_of_Commerce` → `"8.6E9"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Ministry_of_Defence_(United_Kingdom)` → `"4.14E10"^^<http://dbpedia.org/datatype/poundSterling>`
    - `http://dbpedia.org/resource/Southwest_Florida_Water_Management_District__Southwest_Florida_Water_Management_District__1` → `"1.882E8"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/tuition` — **8** triple(s)
    - `http://dbpedia.org/resource/The_Albany_Academy` → `"13500.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Boston_University_School_of_Law` → `"55700.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Hotchkiss_School` → `"50990.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Boston_University_School_of_Law` → `"1282.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Deerfield_Academy` → `"61480.0"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/assetUnderManagement` — **2** triple(s)
    - `http://dbpedia.org/resource/Bain_Capital` → `"1.55E11"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Temasek_Holdings` → `"6.3E11"^^<http://dbpedia.org/datatype/usDollar>`
- `http://dbpedia.org/ontology/fees` — **2** triple(s)
    - `http://dbpedia.org/resource/Eton_College` → `"55875.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/resource/Eton_College` → `"46296.0"^^<http://dbpedia.org/datatype/poundSterling>`

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 14,579 | 3,085 | 0 | 82.5% |
| NPVR | 0 | 87,191 | 667 | 0.0% |
| TMR | 0 | 17,664 | 0 | 0.0% |
| ELR | 0 | 44,780 | 0 | 0.0% |
| NPKR | 0 | 130,852 | 1,011 | 0.0% |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NR** → realized as `literal_node`, `node` and `prop_value` instead of `node` (**3,085 units**)
    - `http://dbpedia.org/resource/Gaborone` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_196317]`, raw=`Gaborone`
    - `http://dbpedia.org/resource/Greenwich` — handle=`prop_value`, form=`literal`, at `node[lit_gdm_224763].property[0].value`, raw=`Greenwich`
    - `http://dbpedia.org/resource/Azamgarh` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_232497]`, raw=`Azamgarh`
    - `http://dbpedia.org/resource/Skibbereen` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_151865]`, raw=`Skibbereen`
    - `http://dbpedia.org/resource/Erbil` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_214821]`, raw=`Erbil`
- **NPVR** → realized as `literal_node` and `prop_value` instead of `prop_value` (**1,915 units**)
    - `""` — handle=`prop_value`, form=`literal`, at `node[lit_gdm_146337].property[0].value`, raw=``
    - `"Comune di Città di Castello"` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_296003]`, raw=`Comune di Città di Castello`
    - `"County of Fillmore"` — handle=`prop_value`, form=`literal`, at `node[lit_gdm_275157].property[0].value`, raw=`County of Fillmore`
    - `"Złotów County"` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_197679]`, raw=`Złotów County`
    - `"7.6E10"` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_200065]`, raw=`7.6E10`

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **NPKR** → realized as `Generic-edge` instead of `Property` (**3,334 occurrence(s)**)
    - `['http://dbpedia.org/resource/Montclair,_New_Jersey', 'http://dbpedia.org/ontology/areaLand', '"1.616E7"']`
    - `['http://dbpedia.org/resource/Montclair_State_University', 'http://dbpedia.org/ontology/motto', '"Carpe Diem (Latin)"']`
    - `['http://dbpedia.org/resource/Colorado', 'http://dbpedia.org/ontology/maximumElevation', '"4401.312"']`
    - `['http://dbpedia.org/resource/Gmina_Działdowo', 'http://dbpedia.org/ontology/areaTotal', '"2.7277E8"']`
    - `['http://dbpedia.org/resource/Harmanli', 'http://dbpedia.org/ontology/areaCode', '"0373"']`
- **ELR** → realized as `Generic-edge` instead of `Edge` (**1,170 occurrence(s)**)
    - `['http://dbpedia.org/resource/Duxbury,_Massachusetts', 'http://dbpedia.org/ontology/subdivision', 'http://dbpedia.org/resource/Massachusett…`
    - `['http://dbpedia.org/resource/University_of_the_South_Pacific', 'http://dbpedia.org/ontology/city', 'http://dbpedia.org/resource/Suva']`
    - `['http://dbpedia.org/resource/Fox_Entertainment_Group', 'http://dbpedia.org/ontology/successor', 'http://dbpedia.org/resource/Walt_Disney_S…`
    - `['http://dbpedia.org/resource/Elko_County,_Nevada', 'http://dbpedia.org/ontology/country', 'http://dbpedia.org/resource/United_States']`
    - `['http://dbpedia.org/resource/Drummondville', 'http://dbpedia.org/ontology/country', 'http://dbpedia.org/resource/Canada']`
- **TMR** → realized as `Generic-edge` instead of `Label` (**496 occurrence(s)**)
    - `['http://dbpedia.org/resource/Sylhet_District', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://dbpedia.org/ontology/Settlement']`
    - `['http://dbpedia.org/resource/Karbala', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://dbpedia.org/ontology/City']`
    - `['http://dbpedia.org/resource/Rivers_State', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://dbpedia.org/ontology/Settlement']`
    - `['http://dbpedia.org/resource/Bond_County,_Illinois', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://dbpedia.org/ontology/Admin…`
    - `['http://dbpedia.org/resource/University_of_the_Arctic', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://dbpedia.org/ontology/Un…`

### Dropped / undefined units (IF)

- Elements without a μ_e match (or with no scorable kind set): **667**
- Occurrences with no covering PGIU: **1,011**

Element-level examples (per role):
- **NPVR** (5 shown)
    - `"5.61E8"`
    - `"9.514E9"`
    - `"2.99E10"`
    - `"2.462E8"`
    - `"8.76693E11"`

Occurrence-level examples (per role):
- **NPKR** (5 shown)
    - `['http://dbpedia.org/resource/Drake_University', 'http://dbpedia.org/ontology/endowment', '"2.198E8"']`
    - `['http://dbpedia.org/resource/Department_for_Business,_Innovation_and_Skills', 'http://dbpedia.org/ontology/budget', '"1.65E10"']`
    - `['http://dbpedia.org/resource/Kalamazoo_College', 'http://dbpedia.org/ontology/endowment', '"2.436E8"']`
    - `['http://dbpedia.org/resource/Texas_State_University', 'http://dbpedia.org/ontology/endowment', '"3.42E8"']`
    - `['http://dbpedia.org/resource/Sarah_Lawrence_College', 'http://dbpedia.org/ontology/endowment', '"1.102E8"']`

## Identifier retention tier distribution (IR)

- full: **343,850** ; partial: **0** ; local: **0** / universe 343,850

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 17,680 | 17,680 | 0 | 0 | 0 | 17,680 | 1.0000 |
| `node.property.value` | 131,863 | 131,863 | 0 | 0 | 0 | 131,863 | 1.0000 |
| `edge.property.value` | 194,307 | 194,307 | 0 | 0 | 0 | 194,307 | 1.0000 |

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

![ip_lost_predicates](visualizations/ip_lost_predicates.png)

