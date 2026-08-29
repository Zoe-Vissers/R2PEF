# r2pef report — rdf2pg_sdm

_Generated 2026-07-03 15:15:49_

## Overview

- Source RDF: `/home/zoe/data/bsbm/bsbm_100k.nt`
- Source triples: **100,075**
- CPGM nodes: **15,153** ; relations: **37,151**
- Derived triples (|derived_triples(C)|): **0**

## Structural overview

**Source RDF**

- 100,075 triples, 10,032 unique subjects, 40 unique predicates
- Object positions: 47,948 IRI, 52,127 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **10,032** (100.0%) ; without `rdf:type`: **0**

**CPGM**

- 15,153 nodes (15,153 synthetic)
- 37,151 edges (37,151 labelled, 0 generic-edge)
- 52,127 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 23.672 s |
| role classification | 4.791 s |
| context build (R, R⁻¹, PGIUs) | 5.285 s |
| IF scoring | 0.265 s |
| IP scoring | 0.143 s |
| IR scoring | 0.193 s |
| **total** | **34.353 s** |

## Scores vs thresholds

```
IP   [░░░░░░░░░░░░░░░░░░░░░░░░░░░│] 0.000 / 0.950 ✗
IF   [███████████████████████████│] 0.997 / 0.950 ✓
IR   [░░░░░░░░░░░░░░░░░░░░░░░░░░░│] 0.000 / 0.950 ✗
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 0.0000 | 0.9500 | ✗ | 0/100,075 full |
| IF | 0.9971 | 0.9500 | ✓ | undef rate 90.32% |
| IR | 0.0000 | 0.9500 | ✗ | universe=100,075 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.9971 — pass
- IP: 0.0000 — FAIL

Optional metrics:
- IR: 0.0000 — fail

## Lost triples (IP)

### By expected PGIU type

_These triples have no PGIU by definition — they are lost. The "expected PGIU type" is the kind the framework would have produced had the triple been encoded idiomatically for its source role (derived from the role classifier's output)._

| Expected PGIU type | Lost triples | Share |
|---|---|---|
| Label | 10,797 | 10.8% |
| Property | 22,591 | 22.6% |
| Edge | 21,874 | 21.9% |
| Unknown | 44,813 | 44.8% |

### By source subject (sampled)

_Subjects ranked by lost-triple count across all predicates. Counts here are computed from the per-predicate samples — when a predicate's losses exceed its sample cap (5), the per-subject counts shown are lower bounds. Useful for spotting subjects that are missing across multiple predicates at once._

- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review1920` — **2** triple(s) in sample
    - `http://purl.org/dc/elements/1.1/publisher → http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/RatingSite1`
    - `http://purl.org/dc/elements/1.1/title → "undercurrents refries viewless bifurcates manuring assonants lavalavas pointing"`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review82` — **2** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/reviewDate → "2007-07-06T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/rating4 → "6"^^<http://www.w3.org/2001/XMLSchema#integer>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer4/Product146` — **2** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyTextual3 → "understructure stuns juster interrogable highhandedly freshing condemnor heated insheathed guildry obelisks"^^<http://www.w3.org/2001/XMLSchema#string>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyTextual2 → "nuptially stubs prorated dungaree dualize"^^<http://www.w3.org/2001/XMLSchema#string>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product44` — **2** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyTextual3 → "berms sillier sectionizing incontinencies fewness stinted"^^<http://www.w3.org/2001/XMLSchema#string>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyNumeric2 → "1225"^^<http://www.w3.org/2001/XMLSchema#integer>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer6/Product215` — **2** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyTextual2 → "footbath lifeline skulkers ribber uncovering soapier ghostwrite rustily mesmerism zealously heliocentrically athenians sirrah crunches"^^<http://www.w3.org/2001/XMLSchema#string>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyTextual4 → "cooker dignitaries infraction blanketed blameful reducibly yeasts amoroso awarded insulters schoolteaching encyclic apportions tabstops"^^<http://www.w3.org/2001/XMLSchema#string>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer2/Product60` — **2** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyNumeric2 → "537"^^<http://www.w3.org/2001/XMLSchema#integer>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyNumeric4 → "870"^^<http://www.w3.org/2001/XMLSchema#integer>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer2/Product62` — **2** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyNumeric2 → "62"^^<http://www.w3.org/2001/XMLSchema#integer>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyNumeric6 → "1041"^^<http://www.w3.org/2001/XMLSchema#integer>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product21` — **2** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyTextual5 → "romanticize penthouses catamarans jolliest quiveringly decimalized teratologist puking reincorporated bargaining professionals loathsomely piggier"^^<http://www.w3.org/2001/XMLSchema#string>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyNumeric4 → "1483"^^<http://www.w3.org/2001/XMLSchema#integer>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer5/Product195` — **2** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyTextual5 → "wrestler liqueurs honeymoons rosed primacies schoolgirls recommitted drumstick momently jubilating glutted contemn gauntly"^^<http://www.w3.org/2001/XMLSchema#string>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productPropertyNumeric5 → "455"^^<http://www.w3.org/2001/XMLSchema#integer>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Reviewer46` — **2** triple(s) in sample
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/country → http://downlode.org/rdf/iso-3166/countries#US`
    - `http://xmlns.com/foaf/0.1/mbox_sha1sum → "80fafc7186c30949963512c2a70c844b9cc7d19"`

### By predicate

Predicates ranked by number of source triples with no PGIU match:

- `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` — **10,797** triple(s)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature376` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/ProductFeature`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review2245` → `http://purl.org/stuff/rev#Review`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3588` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/Offer`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4309` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/Offer`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review476` → `http://purl.org/stuff/rev#Review`
- `http://purl.org/dc/elements/1.1/publisher` — **10,032** triple(s)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review191` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/RatingSite1`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer6/Product240` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer6/Producer6`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3185` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Vendor2`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review1920` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/RatingSite1`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review823` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/RatingSite1`
- `http://purl.org/dc/elements/1.1/date` — **10,032** triple(s)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3377` → `"2008-06-03"^^<http://www.w3.org/2001/XMLSchema#date>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3192` → `"2008-04-30"^^<http://www.w3.org/2001/XMLSchema#date>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Reviewer20` → `"2008-09-21"^^<http://www.w3.org/2001/XMLSchema#date>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer150` → `"2008-05-09"^^<http://www.w3.org/2001/XMLSchema#date>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature375` → `"2000-06-21"^^<http://www.w3.org/2001/XMLSchema#date>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/productFeature` — **6,283** triple(s)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer2/Product61` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature315`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product42` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature916`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer3/Product108` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature78`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer6/Product229` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature11`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer5/Product200` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature101`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/vendor` — **5,100** triple(s)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer87` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Vendor1`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer664` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Vendor1`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1118` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Vendor1`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4862` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Vendor2`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer2193` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Vendor1`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/validTo` — **5,100** triple(s)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3894` → `"2008-04-29T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3396` → `"2008-08-18T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor3/Offer4956` → `"2008-06-01T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1487` → `"2008-05-16T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1880` → `"2008-05-04T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/product` — **5,100** triple(s)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1418` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer3/Product109`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer2002` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product56`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3579` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer4/Product148`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1755` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer4/Product174`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer909` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer4/Product140`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/price` — **5,100** triple(s)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4281` → `"2282.03"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4090` → `"1711.08"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4697` → `"6506.21"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer384` → `"2859.91"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1074` → `"7430.76"^^<http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/USD>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/validFrom` — **5,100** triple(s)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4878` → `"2008-05-17T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1048` → `"2008-06-12T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1871` → `"2008-01-21T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor3/Offer5045` → `"2008-03-22T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer140` → `"2008-03-23T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>`
- `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabulary/offerWebpage` — **5,100** triple(s)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4806` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4806/`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1194` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1194/`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer442` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer442/`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer438` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer438/`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1448` → `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1448/`

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 0 | 37 | 9,995 | 0.0% |
| NPVR | 12,860 | 1 | 10,209 | 100.0% |
| TMR | 0 | 0 | 10,032 | — |
| ELR | 0 | 0 | 28,003 | — |
| NPKR | 0 | 0 | 62,040 | — |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NR** → realized as `node_label` instead of `node` (**37 units**)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType14` — handle=`node_label`, form=`local_only`, at `node[sdm_46777].label[1]`, raw=`ProductType14`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType15` — handle=`node_label`, form=`local_only`, at `node[sdm_40012].label[1]`, raw=`ProductType15`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType1` — handle=`node_label`, form=`local_only`, at `node[sdm_37675].label[3]`, raw=`ProductType1`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType5` — handle=`node_label`, form=`local_only`, at `node[sdm_41530].label[2]`, raw=`ProductType5`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductType23` — handle=`node_label`, form=`local_only`, at `node[sdm_32818].label[1]`, raw=`ProductType23`
- **NPVR** → realized as `edge_label` and `prop_value` instead of `prop_value` (**1 units**)
    - `"producer"` — handle=`edge_label`, form=`local_only`, at `edge[3573].label[0]`, raw=`producer`

### Dropped / undefined units (IF)

- Elements without a μ_e match (or with no scorable kind set): **5,000**
- Occurrences with no covering PGIU: **5,000**

Element-level examples (per role):
- **NR** (5 shown)
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review93`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer1/Product27`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review77`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1716`
    - `http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer2106`

Occurrence-level examples (per role):
- **TMR** (5 shown)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature376', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://w…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review2245', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#typ…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3588', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', '…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer4309', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', '…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review476', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type…`
- **ELR** (5 shown)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer87', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vocabu…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer1418', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer2/Product61', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/vo…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review596', 'http://purl.org/stuff/rev#reviewer', 'http://ww…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer6/Product240', 'http://purl.org/dc/elements/1.1/publisher', 'htt…`
- **NPKR** (5 shown)
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3894', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer4/Product146', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/v…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review1210', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review191', 'http://purl.org/dc/elements/1.1/publisher', 'ht…`
    - `['http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor2/Offer3396', 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/voca…`

## Identifier retention tier distribution (IR)

- full: **0** ; partial: **0** ; local: **100,075** / universe 100,075

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node.label` | 0 | 0 | 0 | 0 | 10,797 | 10,797 | 0.0000 |
| `node.property.key` | 0 | 0 | 0 | 0 | 52,127 | 52,127 | 0.0000 |
| `edge.label` | 0 | 0 | 0 | 0 | 37,151 | 37,151 | 0.0000 |

Local-tier handle examples (bare local name, namespace discarded):
- `node[sdm_20359].label[0]` resolved=`ProductFeature` form=`local_only`
- `node[sdm_20359].property[0].key` resolved=`label` form=`local_only`
- `node[sdm_20359].property[1].key` resolved=`comment` form=`local_only`
- `node[sdm_20359].property[2].key` resolved=`date` form=`local_only`
- `node[sdm_144850].label[0]` resolved=`Offer` form=`local_only`

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

![ip_lost_predicates](visualizations/ip_lost_predicates.png)

