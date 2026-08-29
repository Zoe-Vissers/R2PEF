# r2pef report — kg2pg

_Generated 2026-07-03 14:57:03_

## Overview

- Source RDF: `/home/zoe/data/watdiv/watdiv_100k.nt`
- Source triples: **103,152**
- CPGM nodes: **14,013** ; relations: **89,958**
- Derived triples (|derived_triples(C)|): **182,468**

## Structural overview

**Source RDF**

- 103,152 triples, 5,597 unique subjects, 84 unique predicates
- Object positions: 89,898 IRI, 13,254 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **1,395** (24.9%) ; without `rdf:type`: **4,202**

**CPGM**

- 14,013 nodes (1,396 full_iri, 12,617 literal-form)
- 89,958 edges (89,958 labelled, 0 generic-edge)
- 37,861 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 31.881 s |
| role classification | 3.880 s |
| context build (R, R⁻¹, PGIUs) | 5.397 s |
| IF scoring | 0.353 s |
| IP scoring | 0.082 s |
| IR scoring | 0.265 s |
| **total** | **41.862 s** |

## Scores vs thresholds

```
IP   [████████████████████████░░░│] 0.846 / 0.950 ✗
IF   [████████████████████████░░░│] 0.846 / 0.950 ✗
IR   [███████████████████████████│] 0.959 / 0.950 ✓
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 0.8459 | 0.9500 | ✗ | 87,257/103,152 full |
| IF | 0.8459 | 0.9500 | ✗ | undef rate 17.90% |
| IR | 0.9592 | 0.9500 | ✓ | universe=109,977 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.8459 — FAIL
- IP: 0.8459 — FAIL

Optional metrics:
- IR: 0.9592 — pass

## Lost triples (IP)

### By expected PGIU type

_These triples have no PGIU by definition — they are lost. The "expected PGIU type" is the kind the framework would have produced had the triple been encoded idiomatically for its source role (derived from the role classifier's output)._

| Expected PGIU type | Lost triples | Share |
|---|---|---|
| Property | 8,815 | 55.5% |
| Edge | 7,080 | 44.5% |

### By source subject (sampled)

_Subjects ranked by lost-triple count across all predicates. Counts here are computed from the per-predicate samples — when a predicate's losses exceed its sample cap (5), the per-subject counts shown are lower bounds. Useful for spotting subjects that are missing across multiple predicates at once._

- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer0` — **7** triple(s) in sample
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer3`
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer59`
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User791`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer6` — **7** triple(s) in sample
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer301`
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User749`
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User963`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer7` — **5** triple(s) in sample
    - `http://purl.org/goodrelations/name → "sirup's Cruikshank Shasta recognizance snapdragon's Regor's utilized dissemination's Mulligan devastates pore's skinflint impromptus O'Keeffe enumerates prodigal's dwindled Powers auditory illegitim…`
    - `http://schema.org/email → "fanzine acrostics puerile assaulting entrances flunkey's coffees ministry's wiggling Tuscaloosa's vitiation's thunders hypothesis potpourri"`
    - `http://schema.org/contactPoint → http://db.uwaterloo.ca/~galuc/wsdbm/User777`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer5` — **4** triple(s) in sample
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer199`
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer196`
    - `http://schema.org/openingHours → "11"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer2` — **4** triple(s) in sample
    - `http://purl.org/goodrelations/name → "longed manliness encroaching supreme Verizon haversack elicits antagonized"`
    - `http://schema.org/telephone → "2156062"`
    - `http://schema.org/paymentAccepted → "majorettes rowelled balusters wimps produced hodgepodge plowman's interleaves drinker sinkhole crewmen"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer9` — **4** triple(s) in sample
    - `http://purl.org/goodrelations/name → "glamourizing positrons Anthony's Bhutan's epic's farrow"`
    - `http://schema.org/openingHours → "10"`
    - `http://schema.org/aggregateRating → "2"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer8` — **4** triple(s) in sample
    - `http://purl.org/goodrelations/description → "digestible Shelly's emoluments brainiest glory's founders conceive scrub's beck esquire"`
    - `http://schema.org/openingHours → "11"`
    - `http://schema.org/email → "crematoriums Juliana's Lucia's galloping immunizations mocked memorization's grocers Charity's ergonomics's stubborner randy unwholesome McDonald's jewelry diffraction's hysteresis obligates hoax"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer4` — **4** triple(s) in sample
    - `http://schema.org/openingHours → "16"`
    - `http://schema.org/email → "monograph Stephenson dogmatists fibber's floured Sacco goutier Yoknapatawpha funicular's Jerry enclosure telexing sunken"`
    - `http://schema.org/paymentAccepted → "Unions vegetable sanitizing Tass's exhuming incapacitating"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer3` — **4** triple(s) in sample
    - `http://schema.org/email → "populist Royce's Gantry horsefly's onion Itasca Nan's lustiness's funnel"`
    - `http://schema.org/contactPoint → http://db.uwaterloo.ca/~galuc/wsdbm/User653`
    - `http://schema.org/telephone → "4373193"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer10` — **3** triple(s) in sample
    - `http://purl.org/goodrelations/name → "come pessimists Lusitania's Zulu existentialist's Lexington tautness's sashays Dorsey's Diaspora dazing Giles's soothes scrips lay lacier lukewarm carnation's"`
    - `http://purl.org/goodrelations/description → "author inoculation's Basel saucers festivity's hind Cressida Magnitogorsk's Barbuda girls monkey's Frazier tablet's Bourbon awarded substantiates unforgettably propitious stepmoms elm starting"`
    - `http://schema.org/openingHours → "15"`

### By predicate

Predicates ranked by number of source triples with no PGIU match:

- `http://purl.org/goodrelations/price` — **2,400** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase199` → `"618"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer332` → `"490"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase1` → `"349"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase1428` → `"115"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer438` → `"495"`
- `http://schema.org/eligibleRegion` — **1,924** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer875` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country1`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer414` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country5`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer629` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country5`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer816` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country1`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer540` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country1`
- `http://purl.org/stuff/rev#rating` — **1,500** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review643` → `"2"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review1136` → `"6"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review534` → `"5"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review1163` → `"10"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review61` → `"5"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor` — **1,500** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase290` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product2`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase914` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product16`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase582` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product0`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase1369` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product13`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase52` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product5`
- `http://purl.org/stuff/rev#reviewer` — **1,500** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review23` → `http://db.uwaterloo.ca/~galuc/wsdbm/User76`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review678` → `http://db.uwaterloo.ca/~galuc/wsdbm/User695`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review1162` → `http://db.uwaterloo.ca/~galuc/wsdbm/User510`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review157` → `http://db.uwaterloo.ca/~galuc/wsdbm/User990`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review388` → `http://db.uwaterloo.ca/~galuc/wsdbm/User455`
- `http://purl.org/stuff/rev#text` — **1,063** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review889` → `"upholstering Ziegler sublease's Magi expeditor's antisocial Nehru's beech perturbing teak's supplement advents bordering orbs luminously inducting garnished shapelessness's cogitate Dvina awnings gardens"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review955` → `"pockmarks redeployment's simplest vindicator NoDoz's mudguards fructified"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review884` → `"furrier's rope nebulas rivals tomcats VoIP argosy's survivals sluggishly slumming"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review564` → `"trespassed Sean's jettisoning counterbalance disinterring profitability impassive stoneware plurality's Englishwoman recommending Madonna's"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review1193` → `"scrawniest sidestep policy's itemization caesura's Connie's handwriting's squawk's scruffier flakiness cub's Han scorpions portly Western's muddle's albeit tantrum fretfulness's"`
- `http://purl.org/goodrelations/offers` — **988** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer0` → `http://db.uwaterloo.ca/~galuc/wsdbm/Offer3`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer5` → `http://db.uwaterloo.ca/~galuc/wsdbm/Offer199`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer0` → `http://db.uwaterloo.ca/~galuc/wsdbm/Offer59`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer6` → `http://db.uwaterloo.ca/~galuc/wsdbm/Offer301`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer5` → `http://db.uwaterloo.ca/~galuc/wsdbm/Offer196`
- `http://schema.org/eligibleQuantity` — **900** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer376` → `"4"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer181` → `"2"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer91` → `"3"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer678` → `"6"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer404` → `"5"`
- `http://purl.org/goodrelations/serialNumber` — **900** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer268` → `"69651938"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer37` → `"36521705"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer536` → `"73757404"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer231` → `"47135438"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer886` → `"68123924"`
- `http://purl.org/goodrelations/includes` — **900** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer596` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product99`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer698` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product206`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer52` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product1`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer746` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product203`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer719` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product155`

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 1,395 | 3,190 | 1,037 | 30.4% |
| NPVR | 39 | 4,235 | 4,021 | 0.9% |
| TMR | 1,507 | 0 | 0 | 100.0% |
| ELR | 78,367 | 0 | 7,080 | 100.0% |
| NPKR | 0 | 7,383 | 8,815 | 0.0% |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NR** → realized as `literal_node` and `prop_value` instead of `node` (**3,190 units**)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase65`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review148`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase1291`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review518`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review1000`
- **NPVR** → realized as `literal_node` and `prop_value` instead of `prop_value` (**1,810 units**)
    - `"5411332"` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_2922]`, raw=`5411332`
    - `"1995-02-07"` — handle=`prop_value`, form=`literal`, at `node[lit_kg2pg_3582].property[0].value`, raw=`1995-02-07`
    - `"6755597"` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_358]`, raw=`6755597`
    - `"embroideries marshmallow deflections welshes firstborn sleepwalking's Yugoslav's bushel's philharmonic Kwanzaa's crisply theses wistful ap…` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_3681]`, raw=`embroideries marshmallow deflections welshes firstborn slee…`
    - `"WENDY"` — handle=`prop_value`, form=`literal`, at `node[lit_kg2pg_574].property[0].value`, raw=`WENDY`

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **NPKR** → realized as `Edge` instead of `Property` (**5,000 occurrence(s)**)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User16', 'http://db.uwaterloo.ca/~galuc/wsdbm/userId', '"2226110"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Product53', 'http://schema.org/description', '"oratorical Galatia\'s overall\'s conferred flatfishes …`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User364', 'http://xmlns.com/foaf/familyName', '"CHRISTOPHER"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Product155', 'http://purl.org/ontology/mo/performer', '"backrests contour scarifies Timurid streptoco…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Product30', 'http://ogp.me/ns#tag', 'http://db.uwaterloo.ca/~galuc/wsdbm/Topic141']`

### Dropped / undefined units (IF)

- Elements without a μ_e match (or with no scorable kind set): **5,000**
- Occurrences with no covering PGIU: **5,000**

Element-level examples (per role):
- **NR** (5 shown)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer341`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer825`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer81`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer492`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer709`
- **NPVR** (5 shown)
    - `"327"`
    - `"windbreak transpiration's boozed archeologists Bessemer fishbowl's hinged rematch's resemblance posers navigated narwhal's auditors escort…`
    - `"53"`
    - `"2012-09-13"`
    - `"62974901"`

Occurrence-level examples (per role):
- **ELR** (5 shown)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer875', 'http://schema.org/eligibleRegion', 'http://db.uwaterloo.ca/~galuc/wsdbm/Country1']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Purchase290', 'http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor', 'http://db.uwaterloo.ca/~galuc/wsdbm…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Purchase914', 'http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor', 'http://db.uwaterloo.ca/~galuc/wsdbm…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer414', 'http://schema.org/eligibleRegion', 'http://db.uwaterloo.ca/~galuc/wsdbm/Country5']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer629', 'http://schema.org/eligibleRegion', 'http://db.uwaterloo.ca/~galuc/wsdbm/Country5']`
- **NPKR** (5 shown)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer882', 'http://schema.org/priceValidUntil', '"2013-07-28"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer806', 'http://purl.org/goodrelations/validFrom', '"2013-05-16"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Review643', 'http://purl.org/stuff/rev#rating', '"2"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer376', 'http://schema.org/eligibleQuantity', '"4"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer733', 'http://purl.org/goodrelations/validFrom', '"2013-05-25"']`

## Identifier retention tier distribution (IR)

- full: **105,488** ; partial: **0** ; local: **4,489** / universe 109,977

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 1,396 | 1,396 | 0 | 0 | 0 | 1,396 | 1.0000 |
| `node.label` | 1,507 | 0 | 1,507 | 0 | 4,489 | 5,996 | 0.2513 |
| `node.property.key` | 10 | 10 | 0 | 0 | 0 | 10 | 1.0000 |
| `node.property.value` | 12,617 | 12,617 | 0 | 0 | 0 | 12,617 | 1.0000 |
| `edge.label` | 89,958 | 0 | 89,958 | 0 | 0 | 89,958 | 1.0000 |

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

