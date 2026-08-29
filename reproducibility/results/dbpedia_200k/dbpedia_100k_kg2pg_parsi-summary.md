# r2pef report — kg2pg

_Generated 2026-07-03 15:55:32_

## Overview

- Source RDF: `/home/zoe/data/dbpedia/dbpedia_geo_200k.nt`
- Source triples: **194,307**
- CPGM nodes: **48,990** ; relations: **76,105**
- Derived triples (|derived_triples(C)|): **390,646**

## Structural overview

**Source RDF**

- 194,307 triples, 17,664 unique subjects, 227 unique predicates
- Object positions: 62,444 IRI, 131,863 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **17,664** (100.0%) ; without `rdf:type`: **0**

**CPGM**

- 48,990 nodes (17,665 full_iri, 31,325 literal-form)
- 76,105 edges (76,105 labelled, 0 generic-edge)
- 179,378 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 76.392 s |
| role classification | 10.443 s |
| context build (R, R⁻¹, PGIUs) | 14.082 s |
| IF scoring | 0.958 s |
| IP scoring | 0.177 s |
| IR scoring | 0.605 s |
| **total** | **102.660 s** |

## Scores vs thresholds

```
IP   [██████████████████████████░│] 0.922 / 0.950 ✗
IF   [███████████████████████░░░░│] 0.817 / 0.950 ✗
IR   [█████████████████████████░░│] 0.879 / 0.950 ✗
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 0.9219 | 0.9500 | ✗ | 179,056/194,222 full |
| IF | 0.8174 | 0.9500 | ✗ | undef rate 8.32% |
| IR | 0.8793 | 0.9500 | ✗ | universe=259,488 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.8174 — FAIL
- IP: 0.9219 — FAIL

Optional metrics:
- IR: 0.8793 — fail

## Lost triples (IP)

### By expected PGIU type

_These triples have no PGIU by definition — they are lost. The "expected PGIU type" is the kind the framework would have produced had the triple been encoded idiomatically for its source role (derived from the role classifier's output)._

| Expected PGIU type | Lost triples | Share |
|---|---|---|
| Property | 163 | 1.1% |
| Unknown | 15,003 | 98.9% |

### By source subject (sampled)

_Subjects ranked by lost-triple count across all predicates. Counts here are computed from the per-predicate samples — when a predicate's losses exceed its sample cap (5), the per-subject counts shown are lower bounds. Useful for spotting subjects that are missing across multiple predicates at once._

- `http://dbpedia.org/resource/Virginio_Rognoni` — **11** triple(s) in sample
    - `http://dbpedia.org/ontology/orderInOffice → "Minister of Defence"`
    - `http://dbpedia.org/ontology/orderInOffice → "Minister of the Interior"`
    - `http://dbpedia.org/ontology/orderInOffice → "Minister of Justice"`
- `http://dbpedia.org/resource/Circassia` — **5** triple(s) in sample
    - `http://dbpedia.org/ontology/leaderTitle → "1672–1695"@en`
    - `http://dbpedia.org/ontology/leaderTitle → "1810–1822"@en`
    - `http://dbpedia.org/ontology/leaderTitle → "1827–1839"@en`
- `http://dbpedia.org/resource/Commonwealth_of_Nations` — **4** triple(s) in sample
    - `http://dbpedia.org/ontology/membership → "Guyana"@en`
    - `http://dbpedia.org/ontology/membership → "Seychelles"@en`
    - `http://dbpedia.org/ontology/membership → "Papua New Guinea"@en`
- `http://dbpedia.org/resource/Kingdom_of_the_Netherlands` — **4** triple(s) in sample
    - `http://dbpedia.org/ontology/membership → "Aruba"@en`
    - `http://dbpedia.org/ontology/countryCode → "+297"`
    - `http://dbpedia.org/ontology/countryCode → ""`
- `http://dbpedia.org/resource/Indonesian_National_Party` — **4** triple(s) in sample
    - `http://dbpedia.org/ontology/dissolutionYear → "1945"^^<http://www.w3.org/2001/XMLSchema#gYear>`
    - `http://dbpedia.org/ontology/dissolutionYear → "1931"^^<http://www.w3.org/2001/XMLSchema#gYear>`
    - `http://dbpedia.org/ontology/dissolutionDate → "1945-08-31"^^<http://www.w3.org/2001/XMLSchema#date>`
- `http://dbpedia.org/resource/Karnataka_State_Road_Transport_Corporation` — **3** triple(s) in sample
    - `http://dbpedia.org/ontology/formerName → "* Mysore Government Road Transport Department (1948-1961)"@en`
    - `http://dbpedia.org/ontology/foundingYear → "1961"^^<http://www.w3.org/2001/XMLSchema#gYear>`
    - `http://dbpedia.org/ontology/numberOfLocations → "166"^^<http://www.w3.org/2001/XMLSchema#nonNegativeInteger>`
- `http://dbpedia.org/resource/Wenatchee,_Washington` — **3** triple(s) in sample
    - `http://dbpedia.org/ontology/areaUrban → "8.125569698557132E7"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/ontology/populationUrbanDensity → "81.25519926525774"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/ontology/populationMetroDensity → "8.84"^^<http://www.w3.org/2001/XMLSchema#double>`
- `http://dbpedia.org/resource/St._Paul's_School_(New_Hampshire)` — **3** triple(s) in sample
    - `http://dbpedia.org/ontology/postalCode → ""`
    - `http://dbpedia.org/ontology/mascot → ""`
    - `http://dbpedia.org/ontology/ceeb → ""`
- `http://dbpedia.org/resource/The_Albany_Academy` — **3** triple(s) in sample
    - `http://dbpedia.org/ontology/mascot → ""`
    - `http://dbpedia.org/ontology/campusType → ""@en`
    - `http://dbpedia.org/ontology/ceeb → ""`
- `http://dbpedia.org/resource/Ghana_Institute_of_Management_and_Public_Administration` — **3** triple(s) in sample
    - `http://dbpedia.org/ontology/campusType → ""@en`
    - `http://dbpedia.org/ontology/status → ""`
    - `http://dbpedia.org/ontology/offeredClasses → ""`

### By predicate

Predicates ranked by number of source triples with no PGIU match:

- `http://xmlns.com/foaf/0.1/name` — **4,483** triple(s)
    - `http://dbpedia.org/resource/Split,_Croatia` → `"City of Split"@en`
    - `http://dbpedia.org/resource/Newry` → `"Iúr Cinn Trá/An tIúr"@en`
    - `http://dbpedia.org/resource/Serbia_and_Montenegro` → `"Federal Republic of Yugoslavia"@en`
    - `http://dbpedia.org/resource/Monterey_County,_California` → `"County of Monterey"@en`
    - `http://dbpedia.org/resource/North_Korea` → `"Democratic People's Republic of Korea"@en`
- `http://dbpedia.org/ontology/areaTotal` — **1,567** triple(s)
    - `http://dbpedia.org/resource/Mitchell,_South_Dakota` → `"3.18568537571328E7"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Orangeburg,_South_Carolina` → `"2.336169275523072E7"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Fairbanks,_Alaska` → `"8.448541215916032E7"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Bloomsburg,_Pennsylvania` → `"1.214704423747584E7"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Modesto,_California` → `"1.160314673430528E8"^^<http://www.w3.org/2001/XMLSchema#double>`
- `http://dbpedia.org/ontology/areaLand` — **1,492** triple(s)
    - `http://dbpedia.org/resource/Vancouver,_Washington` → `"1.2623602049777664E8"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/North_Little_Rock,_Arkansas` → `"1.3737296937222144E8"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Encinitas,_California` → `"4.935E7"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Waco,_Texas` → `"2.2980964503011328E8"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Saratoga,_California` → `"3.310004805009408E7"^^<http://www.w3.org/2001/XMLSchema#double>`
- `http://dbpedia.org/ontology/populationDensity` — **1,414** triple(s)
    - `http://dbpedia.org/resource/Dobbs_Ferry,_New_York` → `"1839.043191353524"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Circleville,_Ohio` → `"745.1848880300914"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Stony_Brook,_New_York` → `"892.91"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/United_Kingdom` → `"270.7"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/York,_Pennsylvania` → `"3237.0"^^<http://www.w3.org/2001/XMLSchema#double>`
- `http://dbpedia.org/ontology/areaWater` — **1,368** triple(s)
    - `http://dbpedia.org/resource/North_Haven,_Connecticut` → `"776996.4331008"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/South_Carolina` → `"1.911E9"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Lawton,_Oklahoma` → `"77699.64331008"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Newark,_Ohio` → `"1243194.29296128"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Wheaton,_Illinois` → `"430000.0"^^<http://www.w3.org/2001/XMLSchema#double>`
- `http://dbpedia.org/ontology/elevation` — **1,189** triple(s)
    - `http://dbpedia.org/resource/Shen_County` → `"42.0"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Houlton,_Maine` → `"118.872"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Norwood,_Massachusetts` → `"44.5008"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Tijuana` → `"19.812"^^<http://www.w3.org/2001/XMLSchema#double>`
    - `http://dbpedia.org/resource/Reading,_Pennsylvania` → `"92.964"^^<http://www.w3.org/2001/XMLSchema#double>`
- `http://dbpedia.org/ontology/formerName` — **603** triple(s)
    - `http://dbpedia.org/resource/Karnataka_State_Road_Transport_Corporation` → `"* Mysore Government Road Transport Department (1948-1961)"@en`
    - `http://dbpedia.org/resource/University_of_North_Texas` → `"North Texas State University (1961–1988)"@en`
    - `http://dbpedia.org/resource/Florida_State_University` → `"Florida Institute (1854–1857)"@en`
    - `http://dbpedia.org/resource/Roanoke_College` → `"(1845–1853)"@en`
    - `http://dbpedia.org/resource/North_Carolina_State_University` → `"North Carolina State College of Agriculture and Engineering (1918–1962)"@en`
- `http://xmlns.com/foaf/0.1/nick` — **439** triple(s)
    - `http://dbpedia.org/resource/Kurunegala` → `"Ethugalpura (ඇතුගල්පුර)"@en`
    - `http://dbpedia.org/resource/Cangzhou` → `")"@en`
    - `http://dbpedia.org/resource/Pyongyang` → `"(류경/"@en`
    - `http://dbpedia.org/resource/San_Diego` → `"\"America's Finest City\", \"Birthplace of California\", \"City in Motion\""@en`
    - `http://dbpedia.org/resource/Bhimavaram` → `"Las Vegas of Andhra Pradesh"@en`
- `http://dbpedia.org/ontology/foundingDate` — **421** triple(s)
    - `http://dbpedia.org/resource/Deerfield_Beach,_Florida` → `"1939-05-12"^^<http://www.w3.org/2001/XMLSchema#date>`
    - `http://dbpedia.org/resource/Bacolod` → `"1938-10-19"^^<http://www.w3.org/2001/XMLSchema#date>`
    - `http://dbpedia.org/resource/Maputo` → `"1876-12-09"^^<http://www.w3.org/2001/XMLSchema#date>`
    - `http://dbpedia.org/resource/Iwaki,_Fukushima` → `"1937-06-01"^^<http://www.w3.org/2001/XMLSchema#date>`
    - `http://dbpedia.org/resource/Fillmore_County,_Nebraska` → `"1856-01-26"^^<http://www.w3.org/2001/XMLSchema#date>`
- `http://dbpedia.org/ontology/demonym` — **377** triple(s)
    - `http://dbpedia.org/resource/Aosta_Valley` → `"(woman)"@en`
    - `http://dbpedia.org/resource/Bern` → `"Bernois(e)"@fr`
    - `http://dbpedia.org/resource/San_Salvador` → `"Sansalvadoran"@en`
    - `http://dbpedia.org/resource/Burao` → `"Burcaawi"@en`
    - `http://dbpedia.org/resource/Moudon` → `""@en`

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 14,894 | 2,770 | 0 | 84.3% |
| NPVR | 62,050 | 16,103 | 9,705 | 79.4% |
| TMR | 17,664 | 0 | 0 | 100.0% |
| ELR | 44,780 | 0 | 0 | 100.0% |
| NPKR | 85,287 | 31,325 | 15,251 | 73.1% |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NR** → realized as `node` and `prop_value` instead of `node` (**2,762 units**)
    - `http://dbpedia.org/resource/Nevers` — handle=`prop_value`, form=`literal`, at `node[http://dbpedia.org/resource/Nevers].property[5].value`, raw=`Nevers`
    - `http://dbpedia.org/resource/Mogilev` — handle=`prop_value`, form=`literal`, at `node[http://dbpedia.org/resource/Mogilev].property[3].value`, raw=`Mogilev`
    - `http://dbpedia.org/resource/Turin` — handle=`prop_value`, form=`literal`, at `node[http://dbpedia.org/resource/Turin].property[5].value`, raw=`Turin`
    - `http://dbpedia.org/resource/Uster` — handle=`prop_value`, form=`literal`, at `node[http://dbpedia.org/resource/Uster].property[3].value`, raw=`Uster`
    - `http://dbpedia.org/resource/Madrid` — handle=`prop_value`, form=`literal`, at `node[http://dbpedia.org/resource/Madrid].property[6].value`, raw=`Madrid`
- **NPVR** → realized as `literal_node` and `prop_value` instead of `prop_value` (**2,230 units**)
    - `""` — handle=`prop_value`, form=`literal`, at `node[lit_kg2pg_10573].property[0].value`, raw=``
    - `"VE-F"` — handle=`prop_value`, form=`literal`, at `node[lit_kg2pg_18213].property[0].value`, raw=`VE-F`
    - `"01752"` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_27045]`, raw=`01752`
    - `"3.25E7"` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_5715]`, raw=`3.25E7`
    - `"GLORIAM SAPIENTES POSSIDEBUNT"` — handle=`prop_value`, form=`literal`, at `node[lit_kg2pg_15701].property[0].value`, raw=`GLORIAM SAPIENTES POSSIDEBUNT`
- **NR** → realized as `literal_node`, `node` and `prop_value` instead of `node` (**8 units**)
    - `http://dbpedia.org/resource/Birkirkara` — handle=`prop_value`, form=`literal`, at `node[http://dbpedia.org/resource/Birkirkara].property[5].value`, raw=`Birkirkara`
    - `http://dbpedia.org/resource/Hobart` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_4509]`, raw=`Hobart:`
    - `http://dbpedia.org/resource/Chhachh` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_24361]`, raw=`Chhachh`
    - `http://dbpedia.org/resource/Pretoria` — handle=`prop_value`, form=`literal`, at `node[http://dbpedia.org/resource/Pretoria].property[7].value`, raw=`Pretoria`
    - `http://dbpedia.org/resource/Bridgetown` — handle=`prop_value`, form=`literal`, at `node[lit_kg2pg_10512].property[0].value`, raw=`Bridgetown`

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **NPKR** → realized as `Edge` instead of `Property` (**5,000 occurrence(s)**)
    - `['http://dbpedia.org/resource/Longyan', 'http://dbpedia.org/ontology/synonym', '"Lungyen"']`
    - `['http://dbpedia.org/resource/Gmina_Tarłów', 'http://dbpedia.org/ontology/synonym', '"Tarłów Commune"']`
    - `['http://dbpedia.org/resource/Mississippi_State_University', 'http://dbpedia.org/ontology/endowment', '"6.982E8"']`
    - `['http://dbpedia.org/resource/Arrondissement_of_Aalst', 'http://dbpedia.org/ontology/utcOffset', '"+1"']`
    - `['http://dbpedia.org/resource/Okhaldhunga_District', 'http://dbpedia.org/ontology/utcOffset', '"+05:45"']`

### Dropped / undefined units (IF)

- Elements without a μ_e match (or with no scorable kind set): **5,000**
- Occurrences with no covering PGIU: **5,000**

Element-level examples (per role):
- **NPVR** (5 shown)
    - `"Chinese Culture University"`
    - `"1.488E8"`
    - `"Podunavlje District"`
    - `"City of San Buenaventura"`
    - `"1679.21"`

Occurrence-level examples (per role):
- **NPKR** (5 shown)
    - `['http://dbpedia.org/resource/Mitchell,_South_Dakota', 'http://dbpedia.org/ontology/areaTotal', '"3.18568537571328E7"']`
    - `['http://dbpedia.org/resource/Split,_Croatia', 'http://xmlns.com/foaf/0.1/name', '"City of Split"']`
    - `['http://dbpedia.org/resource/North_Haven,_Connecticut', 'http://dbpedia.org/ontology/areaWater', '"776996.4331008"']`
    - `['http://dbpedia.org/resource/Orangeburg,_South_Carolina', 'http://dbpedia.org/ontology/areaTotal', '"2.336169275523072E7"']`
    - `['http://dbpedia.org/resource/Aosta_Valley', 'http://dbpedia.org/ontology/demonym', '"(woman)"']`

## Identifier retention tier distribution (IR)

- full: **228,163** ; partial: **0** ; local: **31,325** / universe 259,488

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 17,665 | 17,665 | 0 | 0 | 0 | 17,665 | 1.0000 |
| `node.label` | 17,664 | 0 | 17,664 | 0 | 31,325 | 48,989 | 0.3606 |
| `node.property.key` | 85,403 | 4 | 85,399 | 0 | 0 | 85,403 | 1.0000 |
| `node.property.value` | 31,326 | 31,326 | 0 | 0 | 0 | 31,326 | 1.0000 |
| `edge.label` | 76,105 | 0 | 76,105 | 0 | 0 | 76,105 | 1.0000 |

Local-tier handle examples (bare local name, namespace discarded):
- `node[lit_kg2pg_0].label[0]` resolved=`string` form=`local_only`
- `node[lit_kg2pg_1].label[0]` resolved=`string` form=`local_only`
- `node[lit_kg2pg_2].label[0]` resolved=`string` form=`local_only`
- `node[lit_kg2pg_3].label[0]` resolved=`string` form=`local_only`
- `node[lit_kg2pg_4].label[0]` resolved=`string` form=`local_only`

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

![ip_lost_predicates](visualizations/ip_lost_predicates.png)

