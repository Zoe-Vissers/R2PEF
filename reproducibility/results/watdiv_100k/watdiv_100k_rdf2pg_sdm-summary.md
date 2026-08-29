# r2pef report — rdf2pg_sdm

_Generated 2026-07-03 14:47:06_

## Overview

- Source RDF: `/home/zoe/data/watdiv/watdiv_100k.nt`
- Source triples: **103,152**
- CPGM nodes: **5,901** ; relations: **93,495**
- Derived triples (|derived_triples(C)|): **0**

## Structural overview

**Source RDF**

- 103,152 triples, 5,597 unique subjects, 84 unique predicates
- Object positions: 89,898 IRI, 13,254 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **1,395** (24.9%) ; without `rdf:type`: **4,202**

**CPGM**

- 5,901 nodes (5,901 synthetic)
- 93,495 edges (93,495 labelled, 0 generic-edge)
- 13,254 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 21.653 s |
| role classification | 3.607 s |
| context build (R, R⁻¹, PGIUs) | 4.231 s |
| IF scoring | 0.210 s |
| IP scoring | 0.157 s |
| IR scoring | 0.218 s |
| **total** | **30.078 s** |

## Scores vs thresholds

```
IP   [░░░░░░░░░░░░░░░░░░░░░░░░░░░│] 0.000 / 0.950 ✗
IF   [███████████████████████████│] 1.000 / 0.950 ✓
IR   [░░░░░░░░░░░░░░░░░░░░░░░░░░░│] 0.000 / 0.950 ✗
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 0.0000 | 0.9500 | ✗ | 0/103,152 full |
| IF | 1.0000 | 0.9500 | ✓ | undef rate 93.15% |
| IR | 0.0000 | 0.9500 | ✗ | universe=108,256 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 1.0000 — pass
- IP: 0.0000 — FAIL

Optional metrics:
- IR: 0.0000 — fail

## Lost triples (IP)

### By expected PGIU type

_These triples have no PGIU by definition — they are lost. The "expected PGIU type" is the kind the framework would have produced had the triple been encoded idiomatically for its source role (derived from the role classifier's output)._

| Expected PGIU type | Lost triples | Share |
|---|---|---|
| Label | 1,507 | 1.5% |
| Property | 16,198 | 15.7% |
| Edge | 85,447 | 82.8% |

### By source subject (sampled)

_Subjects ranked by lost-triple count across all predicates. Counts here are computed from the per-predicate samples — when a predicate's losses exceed its sample cap (5), the per-subject counts shown are lower bounds. Useful for spotting subjects that are missing across multiple predicates at once._

- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer5` — **6** triple(s) in sample
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer369`
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer16`
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer435`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer6` — **6** triple(s) in sample
    - `http://schema.org/telephone → "8759765"`
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User749`
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User699`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Product54` — **5** triple(s) in sample
    - `http://schema.org/actor → http://db.uwaterloo.ca/~galuc/wsdbm/User333`
    - `http://schema.org/actor → http://db.uwaterloo.ca/~galuc/wsdbm/User72`
    - `http://schema.org/actor → http://db.uwaterloo.ca/~galuc/wsdbm/User728`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer7` — **5** triple(s) in sample
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User705`
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User821`
    - `http://purl.org/goodrelations/description → "summertime's condone pneumonia's Stoic's doorknob tacitness's actresses calendars pickpocket's saltshaker Odis's tradition's hula's comfortable orbital's extrapolation's purebreds Powell rascals dia…`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Product78` — **5** triple(s) in sample
    - `http://schema.org/publisher → "watt finch pandering saunter's payer volatility's Gaza unbounded extremism ciders quadratic"`
    - `http://schema.org/printEdition → "24"`
    - `http://schema.org/printSection → "4"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Product27` — **4** triple(s) in sample
    - `http://purl.org/stuff/rev#hasReview → http://db.uwaterloo.ca/~galuc/wsdbm/Review687`
    - `http://schema.org/datePublished → "1990-01-15"`
    - `http://schema.org/printEdition → "15"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer0` — **4** triple(s) in sample
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer7`
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User791`
    - `http://schema.org/contactPoint → http://db.uwaterloo.ca/~galuc/wsdbm/User276`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Product116` — **4** triple(s) in sample
    - `http://schema.org/description → "epaulets troubles"`
    - `http://purl.org/ontology/mo/artist → http://db.uwaterloo.ca/~galuc/wsdbm/User943`
    - `http://purl.org/ontology/mo/producer → "serialization gent's Istanbul's terrorizing chorus's reupholsters presences vacantly businesswoman magazines gentian Good ascertainable madam"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Product112` — **4** triple(s) in sample
    - `http://schema.org/contentRating → "10"`
    - `http://schema.org/publisher → "onset's"`
    - `http://schema.org/datePublished → "1987-09-21"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Product164` — **4** triple(s) in sample
    - `http://schema.org/contentSize → "1292"`
    - `http://purl.org/ontology/mo/movement → "1"`
    - `http://purl.org/ontology/mo/performed_in → http://db.uwaterloo.ca/~galuc/wsdbm/City2`

### By predicate

Predicates ranked by number of source triples with no PGIU match:

- `http://db.uwaterloo.ca/~galuc/wsdbm/friendOf` — **41,054** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User585` → `http://db.uwaterloo.ca/~galuc/wsdbm/User623`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User393` → `http://db.uwaterloo.ca/~galuc/wsdbm/User689`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User322` → `http://db.uwaterloo.ca/~galuc/wsdbm/User399`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User393` → `http://db.uwaterloo.ca/~galuc/wsdbm/User381`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User608` → `http://db.uwaterloo.ca/~galuc/wsdbm/User999`
- `http://db.uwaterloo.ca/~galuc/wsdbm/follows` — **30,155** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User708` → `http://db.uwaterloo.ca/~galuc/wsdbm/User876`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User966` → `http://db.uwaterloo.ca/~galuc/wsdbm/User725`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User350` → `http://db.uwaterloo.ca/~galuc/wsdbm/User647`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User1` → `http://db.uwaterloo.ca/~galuc/wsdbm/User862`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User255` → `http://db.uwaterloo.ca/~galuc/wsdbm/User896`
- `http://purl.org/goodrelations/price` — **2,400** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase424` → `"116"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer564` → `"498"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase351` → `"416"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase981` → `"369"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase1100` → `"863"`
- `http://schema.org/eligibleRegion` — **1,924** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer163` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country6`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer293` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country0`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer451` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country8`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer476` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country1`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer710` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country7`
- `http://ogp.me/ns#tag` — **1,799** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Product35` → `http://db.uwaterloo.ca/~galuc/wsdbm/Topic163`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre23` → `http://db.uwaterloo.ca/~galuc/wsdbm/Topic204`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre37` → `http://db.uwaterloo.ca/~galuc/wsdbm/Topic63`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Product43` → `http://db.uwaterloo.ca/~galuc/wsdbm/Topic164`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Product219` → `http://db.uwaterloo.ca/~galuc/wsdbm/Topic99`
- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` — **1,507** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User212` → `http://db.uwaterloo.ca/~galuc/wsdbm/Role1`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Product68` → `http://db.uwaterloo.ca/~galuc/wsdbm/ProductCategory7`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User526` → `http://db.uwaterloo.ca/~galuc/wsdbm/Role1`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User838` → `http://db.uwaterloo.ca/~galuc/wsdbm/Role0`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre32` → `http://db.uwaterloo.ca/~galuc/wsdbm/Genre0`
- `http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor` — **1,500** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase325` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product1`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase85` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product240`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase882` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product0`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase645` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product129`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase788` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product76`
- `http://db.uwaterloo.ca/~galuc/wsdbm/makesPurchase` — **1,500** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User186` → `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase857`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User853` → `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase259`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User470` → `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase741`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User769` → `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase289`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User632` → `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase605`
- `http://purl.org/stuff/rev#reviewer` — **1,500** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review1361` → `http://db.uwaterloo.ca/~galuc/wsdbm/User495`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review188` → `http://db.uwaterloo.ca/~galuc/wsdbm/User245`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review502` → `http://db.uwaterloo.ca/~galuc/wsdbm/User644`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review519` → `http://db.uwaterloo.ca/~galuc/wsdbm/User487`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review135` → `http://db.uwaterloo.ca/~galuc/wsdbm/User888`
- `http://purl.org/stuff/rev#rating` — **1,500** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review586` → `"3"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review1383` → `"9"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review45` → `"8"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review161` → `"4"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review1374` → `"6"`

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 0 | 0 | 5,622 | — |
| NPVR | 8,016 | 0 | 279 | 100.0% |
| TMR | 0 | 0 | 1,507 | — |
| ELR | 0 | 0 | 85,447 | — |
| NPKR | 0 | 0 | 16,198 | — |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

### Dropped / undefined units (IF)

- Elements without a μ_e match (or with no scorable kind set): **5,000**
- Occurrences with no covering PGIU: **5,000**

Element-level examples (per role):
- **NR** (5 shown)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User592`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase449`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre20`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/User101`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Product98`

Occurrence-level examples (per role):
- **TMR** (5 shown)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User212', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://db.uwaterloo.ca/~galuc/wsdbm/Rol…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Product68', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://db.uwaterloo.ca/~galuc/wsdbm/P…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User526', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://db.uwaterloo.ca/~galuc/wsdbm/Rol…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User838', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://db.uwaterloo.ca/~galuc/wsdbm/Rol…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre32', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://db.uwaterloo.ca/~galuc/wsdbm/…`
- **ELR** (5 shown)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User585', 'http://db.uwaterloo.ca/~galuc/wsdbm/friendOf', 'http://db.uwaterloo.ca/~galuc/wsdbm/User62…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User708', 'http://db.uwaterloo.ca/~galuc/wsdbm/follows', 'http://db.uwaterloo.ca/~galuc/wsdbm/User876…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User485', 'http://db.uwaterloo.ca/~galuc/wsdbm/likes', 'http://db.uwaterloo.ca/~galuc/wsdbm/Product23…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Purchase325', 'http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor', 'http://db.uwaterloo.ca/~galuc/wsdbm…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User186', 'http://db.uwaterloo.ca/~galuc/wsdbm/makesPurchase', 'http://db.uwaterloo.ca/~galuc/wsdbm/P…`
- **NPKR** (5 shown)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User146', 'http://xmlns.com/foaf/givenName', '"NOEL"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Product77', 'http://ogp.me/ns#title', '"cable stoicism\'s kennel\'s plop\'s"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Purchase424', 'http://purl.org/goodrelations/price', '"116"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer564', 'http://purl.org/goodrelations/price', '"498"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User470', 'http://xmlns.com/foaf/familyName', '"ADOLPH"']`

## Identifier retention tier distribution (IR)

- full: **0** ; partial: **0** ; local: **108,256** / universe 108,256

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node.label` | 0 | 0 | 0 | 0 | 1,507 | 1,507 | 0.0000 |
| `node.property.key` | 0 | 0 | 0 | 0 | 13,254 | 13,254 | 0.0000 |
| `edge.label` | 0 | 0 | 0 | 0 | 93,495 | 93,495 | 0.0000 |

Local-tier handle examples (bare local name, namespace discarded):
- `node[sdm_30538].property[0].key` resolved=`eligibleQuantity` form=`local_only`
- `node[sdm_30538].property[1].key` resolved=`validFrom` form=`local_only`
- `node[sdm_30538].property[2].key` resolved=`price` form=`local_only`
- `node[sdm_30538].property[3].key` resolved=`serialNumber` form=`local_only`
- `node[sdm_32092].property[0].key` resolved=`eligibleQuantity` form=`local_only`

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![ir_tiers](visualizations/ir_tiers.png)

![ip_lost_predicates](visualizations/ip_lost_predicates.png)

