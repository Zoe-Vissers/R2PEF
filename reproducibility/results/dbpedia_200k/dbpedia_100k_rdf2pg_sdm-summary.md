# r2pef report — rdf2pg_sdm

_Generated 2026-07-03 15:35:17_

## Overview

- Source RDF: `/home/zoe/data/dbpedia/dbpedia_geo_200k.nt`
- Source triples: **194,307**
- CPGM nodes: **17,664** ; relations: **44,780**
- Derived triples (|derived_triples(C)|): **0**

## Structural overview

**Source RDF**

- 194,307 triples, 17,664 unique subjects, 227 unique predicates
- Object positions: 62,444 IRI, 131,863 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **17,664** (100.0%) ; without `rdf:type`: **0**

**CPGM**

- 17,664 nodes (17,664 synthetic)
- 44,780 edges (44,780 labelled, 0 generic-edge)
- 131,863 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 42.146 s |
| role classification | 10.106 s |
| context build (R, R⁻¹, PGIUs) | 11.093 s |
| IF scoring | 0.792 s |
| IP scoring | 0.291 s |
| IR scoring | 1.978 s |
| **total** | **66.409 s** |

## Scores vs thresholds

```
IP   [░░░░░░░░░░░░░░░░░░░░░░░░░░░│] 0.000 / 0.950 ✗
IF   [███████████████████████████│] 0.966 / 0.950 ✓
IR   [░░░░░░░░░░░░░░░░░░░░░░░░░░░│] 0.000 / 0.950 ✗
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 0.0000 | 0.9500 | ✗ | 0/194,222 full |
| IF | 0.9658 | 0.9500 | ✓ | undef rate 69.89% |
| IR | 0.0000 | 0.9500 | ✗ | universe=194,307 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.9658 — pass
- IP: 0.0000 — FAIL

Optional metrics:
- IR: 0.0000 — fail

## Lost triples (IP)

### By expected PGIU type

_These triples have no PGIU by definition — they are lost. The "expected PGIU type" is the kind the framework would have produced had the triple been encoded idiomatically for its source role (derived from the role classifier's output)._

| Expected PGIU type | Lost triples | Share |
|---|---|---|
| Label | 17,664 | 9.1% |
| Property | 32,746 | 16.9% |
| Edge | 44,780 | 23.1% |
| Unknown | 99,032 | 51.0% |

### By source subject (sampled)

_Subjects ranked by lost-triple count across all predicates. Counts here are computed from the per-predicate samples — when a predicate's losses exceed its sample cap (5), the per-subject counts shown are lower bounds. Useful for spotting subjects that are missing across multiple predicates at once._

- `http://dbpedia.org/resource/Virginio_Rognoni` — **13** triple(s) in sample
    - `http://dbpedia.org/ontology/almaMater → http://dbpedia.org/resource/University_of_Pavia`
    - `http://dbpedia.org/ontology/almaMater → http://dbpedia.org/resource/Yale_University`
    - `http://dbpedia.org/ontology/orderInOffice → "Vice presidentofCSM"`
- `http://dbpedia.org/resource/Monica_Babuc` — **11** triple(s) in sample
    - `http://dbpedia.org/ontology/president → http://dbpedia.org/resource/Igor_Dodon`
    - `http://dbpedia.org/ontology/president → http://dbpedia.org/resource/Nicolae_Timofti`
    - `http://dbpedia.org/ontology/activeYearsStartDate → "2019-03-09"^^<http://www.w3.org/2001/XMLSchema#date>`
- `http://dbpedia.org/resource/Henry_Ford` — **8** triple(s) in sample
    - `http://dbpedia.org/ontology/party → http://dbpedia.org/resource/Republican_Party_(United_States)`
    - `http://dbpedia.org/ontology/deathPlace → http://dbpedia.org/resource/Dearborn,_Michigan`
    - `http://dbpedia.org/ontology/deathYear → "1947"^^<http://www.w3.org/2001/XMLSchema#gYear>`
- `http://dbpedia.org/resource/Baltimore_City_College` — **7** triple(s) in sample
    - `http://dbpedia.org/ontology/budget → "9373000.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/ontology/staff → "25"^^<http://www.w3.org/2001/XMLSchema#nonNegativeInteger>`
    - `http://dbpedia.org/ontology/campusType → "Urban"@en`
- `http://dbpedia.org/resource/Commonwealth_of_Nations` — **6** triple(s) in sample
    - `http://dbpedia.org/ontology/membership → "Tonga"@en`
    - `http://dbpedia.org/ontology/membership → "Seychelles"@en`
    - `http://dbpedia.org/ontology/membership → "Namibia"@en`
- `http://dbpedia.org/resource/Achimota_School` — **6** triple(s) in sample
    - `http://dbpedia.org/ontology/budget → "1000000.0"^^<http://dbpedia.org/datatype/usDollar>`
    - `http://dbpedia.org/ontology/status → "Active"`
    - `http://dbpedia.org/ontology/status → ""`
- `http://dbpedia.org/resource/DreamWorks_Pictures` — **6** triple(s) in sample
    - `http://dbpedia.org/ontology/owner → http://dbpedia.org/resource/NBCUniversal`
    - `http://dbpedia.org/ontology/owner → http://dbpedia.org/resource/Universal_Pictures`
    - `http://dbpedia.org/ontology/owningCompany → http://dbpedia.org/resource/Entertainment_One`
- `http://dbpedia.org/resource/Hishammuddin_Hussein` — **5** triple(s) in sample
    - `http://dbpedia.org/ontology/birthPlace → http://dbpedia.org/resource/Johor`
    - `http://dbpedia.org/ontology/education → http://dbpedia.org/resource/Malay_College_Kuala_Kangsar`
    - `http://dbpedia.org/ontology/almaMater → http://dbpedia.org/resource/London_School_of_Economics`
- `http://dbpedia.org/resource/Bill_Gates` — **4** triple(s) in sample
    - `http://dbpedia.org/ontology/birthPlace → http://dbpedia.org/resource/Seattle`
    - `http://dbpedia.org/ontology/birthPlace → http://dbpedia.org/resource/Washington_(state)`
    - `http://dbpedia.org/ontology/activeYearsStartYear → "1972"^^<http://www.w3.org/2001/XMLSchema#gYear>`
- `http://dbpedia.org/resource/José_Rizal` — **4** triple(s) in sample
    - `http://dbpedia.org/ontology/birthPlace → http://dbpedia.org/resource/Captaincy_General_of_the_Philippines`
    - `http://dbpedia.org/ontology/birthYear → "1861"^^<http://www.w3.org/2001/XMLSchema#gYear>`
    - `http://dbpedia.org/ontology/deathYear → "1896"^^<http://www.w3.org/2001/XMLSchema#gYear>`

### By predicate

Predicates ranked by number of source triples with no PGIU match:

- `http://xmlns.com/foaf/0.1/name` — **21,734** triple(s)
    - `http://dbpedia.org/resource/Põlva_Parish` → `"Põlva Parish"@en`
    - `http://dbpedia.org/resource/Duke_University` → `""@en`
    - `http://dbpedia.org/resource/Igor_Dodon` → `"Igor Dodon"@en`
    - `http://dbpedia.org/resource/Mississippi_College_School_of_Law` → `"School of Law"@en`
    - `http://dbpedia.org/resource/Qalkhani_Rural_District` → `"Qalkhani Rural District"@en`
- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` — **17,664** triple(s)
    - `http://dbpedia.org/resource/Alt_Empordà` → `http://dbpedia.org/ontology/Settlement`
    - `http://dbpedia.org/resource/Biella` → `http://dbpedia.org/ontology/Settlement`
    - `http://dbpedia.org/resource/Pindra` → `http://dbpedia.org/ontology/Settlement`
    - `http://dbpedia.org/resource/Manchester_Grammar_School` → `http://dbpedia.org/ontology/School`
    - `http://dbpedia.org/resource/Minnehaha_County,_South_Dakota` → `http://dbpedia.org/ontology/AdministrativeRegion`
- `http://dbpedia.org/ontology/subdivision` — **15,974** triple(s)
    - `http://dbpedia.org/resource/Biała_County,_Lublin_Voivodeship` → `http://dbpedia.org/resource/Gmina_Piszczac`
    - `http://dbpedia.org/resource/South_India` → `http://dbpedia.org/resource/Andaman_and_Nicobar_Islands`
    - `http://dbpedia.org/resource/British_Columbia_Coast` → `http://dbpedia.org/resource/Vancouver`
    - `http://dbpedia.org/resource/Jalpaiguri_district` → `http://dbpedia.org/resource/West_Bengal`
    - `http://dbpedia.org/resource/Decatur,_Alabama` → `http://dbpedia.org/resource/Limestone_County,_Alabama`
- `http://dbpedia.org/ontology/country` — **13,716** triple(s)
    - `http://dbpedia.org/resource/Warsaw` → `http://dbpedia.org/resource/Poland`
    - `http://dbpedia.org/resource/Clerkenwell` → `http://dbpedia.org/resource/United_Kingdom`
    - `http://dbpedia.org/resource/Jõgeva_County` → `http://dbpedia.org/resource/Estonia`
    - `http://dbpedia.org/resource/Yellowstone_County,_Montana` → `http://dbpedia.org/resource/United_States`
    - `http://dbpedia.org/resource/Gateshead` → `http://dbpedia.org/resource/United_Kingdom`
- `http://dbpedia.org/ontology/areaTotal` — **12,322** triple(s)
    - `http://dbpedia.org/resource/Gmina_Skąpe` → `"1.8128E8"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Riverside,_California` → `"2.1118763051679745E8"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Wilson_County,_Tennessee` → `"1.509963068325888E9"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Gmina_Zadzim` → `"1.4436E8"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Worcester,_Massachusetts` → `"9.957E7"^^<http://www.w3.org/2001/XMLSchema#double>`
- `http://dbpedia.org/ontology/populationTotal` — **11,650** triple(s)
    - `http://dbpedia.org/resource/La_Serena,_Chile` → `"198163"^^<http://www.w3.org/2001/XMLSchema#nonNegativeInteger>`
    - `http://dbpedia.org/resource/Lewis_County,_New_York` → `"26582"^^<http://www.w3.org/2001/XMLSchema#nonNegativeInteger>`
    - `http://dbpedia.org/resource/Safien` → `"2011"^^<http://www.w3.org/2001/XMLSchema#nonNegativeInteger>`
    - `http://dbpedia.org/resource/Redmond,_Washington` → `"73256"^^<http://www.w3.org/2001/XMLSchema#nonNegativeInteger>`
    - `http://dbpedia.org/resource/Lambeth` → `"9675"^^<http://www.w3.org/2001/XMLSchema#nonNegativeInteger>`
- `http://dbpedia.org/ontology/utcOffset` — **11,022** triple(s)
    - `http://dbpedia.org/resource/Province_of_Vercelli` → `"+2"`
    - `http://dbpedia.org/resource/Riverside,_California` → `"&minus;7"`
    - `http://dbpedia.org/resource/La_Sagra` → `"+1"`
    - `http://dbpedia.org/resource/Province_of_Brescia` → `"+1"`
    - `http://dbpedia.org/resource/Burgas_Province` → `"+3"`
- `http://dbpedia.org/ontology/postalCode` — **5,252** triple(s)
    - `http://dbpedia.org/resource/Lynn,_Massachusetts` → `"01901–01905"`
    - `http://dbpedia.org/resource/New_Plymouth` → `"4310, 4312"`
    - `http://dbpedia.org/resource/Yichang` → `"443000"`
    - `http://dbpedia.org/resource/Lenexa,_Kansas` → `"66200-66299"`
    - `http://dbpedia.org/resource/Rugby,_Warwickshire` → `"CV21, CV22, CV23"`
- `http://dbpedia.org/ontology/areaLand` — **5,161** triple(s)
    - `http://dbpedia.org/resource/Chattooga_County,_Georgia` → `"8.10666278535168E8"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Petersburg,_Virginia` → `"5.885E7"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Niagara-on-the-Lake` → `"1.3281E8"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/St._Louis_County,_Minnesota` → `"1.6179655725268991E10"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Tippecanoe_County,_Indiana` → `"1.294501957427036E9"^^<http://www.w3.org/2001/XMLSchema#double>`
- `http://dbpedia.org/ontology/areaCode` — **4,987** triple(s)
    - `http://dbpedia.org/resource/Falkirk` → `"01324"`
    - `http://dbpedia.org/resource/Quincy,_Massachusetts` → `"617 and 857"`
    - `http://dbpedia.org/resource/Chengalpattu` → `"+91-44"`
    - `http://dbpedia.org/resource/Santa_Cruz_Department_(Bolivia)` → `"+(591) 3"`
    - `http://dbpedia.org/resource/Richmond,_Virginia` → `"804"`

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 0 | 3,085 | 14,579 | 0.0% |
| NPVR | 87,189 | 2 | 667 | 100.0% |
| TMR | 0 | 0 | 17,664 | — |
| ELR | 0 | 0 | 44,780 | — |
| NPKR | 0 | 0 | 131,863 | — |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NR** → realized as `prop_value` instead of `node` (**3,085 units**)
    - `http://dbpedia.org/resource/Sirajganj` — handle=`prop_value`, form=`literal`, at `node[sdm_67546].property[6].value`, raw=`Sirajganj`
    - `http://dbpedia.org/resource/Wallsend` — handle=`prop_value`, form=`literal`, at `node[sdm_94819].property[4].value`, raw=`Wallsend`
    - `http://dbpedia.org/resource/Arrah` — handle=`prop_value`, form=`literal`, at `node[sdm_30].property[8].value`, raw=`Arrah`
    - `http://dbpedia.org/resource/Guadeloupe` — handle=`prop_value`, form=`literal`, at `node[sdm_51373].property[6].value`, raw=`Guadeloupe`
    - `http://dbpedia.org/resource/Latur` — handle=`prop_value`, form=`literal`, at `node[sdm_9688].property[10].value`, raw=`Latur`
- **NPVR** → realized as `edge_label` and `prop_value` instead of `prop_value` (**2 units**)
    - `"city"` — handle=`edge_label`, form=`local_only`, at `edge[28952].label[0]`, raw=`city`
    - `"borough"` — handle=`prop_value`, form=`literal`, at `node[sdm_29911].property[4].value`, raw=`borough`

### Dropped / undefined units (IF)

- Elements without a μ_e match (or with no scorable kind set): **5,000**
- Occurrences with no covering PGIU: **5,000**

Element-level examples (per role):
- **NR** (5 shown)
    - `http://dbpedia.org/resource/Kelheim_(district)`
    - `http://dbpedia.org/resource/Ryazan_Oblast`
    - `http://dbpedia.org/resource/Gmina_Lidzbark_Warmiński`
    - `http://dbpedia.org/resource/Croatian_Democratic_Union`
    - `http://dbpedia.org/resource/Clayton_County,_Iowa`

Occurrence-level examples (per role):
- **TMR** (5 shown)
    - `['http://dbpedia.org/resource/Alt_Empordà', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://dbpedia.org/ontology/Settlement']`
    - `['http://dbpedia.org/resource/Biella', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://dbpedia.org/ontology/Settlement']`
    - `['http://dbpedia.org/resource/Pindra', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://dbpedia.org/ontology/Settlement']`
    - `['http://dbpedia.org/resource/Manchester_Grammar_School', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://dbpedia.org/ontology/S…`
    - `['http://dbpedia.org/resource/Minnehaha_County,_South_Dakota', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://dbpedia.org/ontol…`
- **ELR** (5 shown)
    - `['http://dbpedia.org/resource/Las_Animas_County,_Colorado', 'http://dbpedia.org/ontology/state', 'http://dbpedia.org/resource/Colorado']`
    - `['http://dbpedia.org/resource/Biała_County,_Lublin_Voivodeship', 'http://dbpedia.org/ontology/subdivision', 'http://dbpedia.org/resource/Gm…`
    - `['http://dbpedia.org/resource/University_of_Ottawa', 'http://dbpedia.org/ontology/city', 'http://dbpedia.org/resource/Ottawa']`
    - `['http://dbpedia.org/resource/Warsaw', 'http://dbpedia.org/ontology/country', 'http://dbpedia.org/resource/Poland']`
    - `['http://dbpedia.org/resource/MylesCar', 'http://dbpedia.org/ontology/regionServed', 'http://dbpedia.org/resource/Mysore']`
- **NPKR** (5 shown)
    - `['http://dbpedia.org/resource/Szeged', 'http://dbpedia.org/ontology/elevation', '"75.998832"']`
    - `['http://dbpedia.org/resource/Royal_Military_College,_Duntroon', 'http://dbpedia.org/ontology/numberOfStudents', '"425"']`
    - `['http://dbpedia.org/resource/Gmina_Skąpe', 'http://dbpedia.org/ontology/areaTotal', '"1.8128E8"']`
    - `['http://dbpedia.org/resource/Loyola_University_New_Orleans', 'http://dbpedia.org/ontology/mascot', '""']`
    - `['http://dbpedia.org/resource/Bourg-en-Bresse', 'http://dbpedia.org/ontology/minimumElevation', '"220.0"']`

## Identifier retention tier distribution (IR)

- full: **0** ; partial: **0** ; local: **194,307** / universe 194,307

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node.label` | 0 | 0 | 0 | 0 | 17,664 | 17,664 | 0.0000 |
| `node.property.key` | 0 | 0 | 0 | 0 | 131,863 | 131,863 | 0.0000 |
| `edge.label` | 0 | 0 | 0 | 0 | 44,780 | 44,780 | 0.0000 |

Local-tier handle examples (bare local name, namespace discarded):
- `node[sdm_124108].label[0]` resolved=`AdministrativeRegion` form=`local_only`
- `node[sdm_124108].property[0].key` resolved=`areaTotal` form=`local_only`
- `node[sdm_124108].property[1].key` resolved=`populationTotal` form=`local_only`
- `node[sdm_124108].property[2].key` resolved=`utcOffset` form=`local_only`
- `node[sdm_124108].property[3].key` resolved=`utcOffset` form=`local_only`

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

![ip_lost_predicates](visualizations/ip_lost_predicates.png)

