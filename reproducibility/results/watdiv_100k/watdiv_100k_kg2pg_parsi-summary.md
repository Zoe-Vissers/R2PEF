# r2pef report — kg2pg

_Generated 2026-07-03 14:54:45_

## Overview

- Source RDF: `/home/zoe/data/watdiv/watdiv_100k.nt`
- Source triples: **103,152**
- CPGM nodes: **9,524** ; relations: **85,469**
- Derived triples (|derived_triples(C)|): **174,534**

## Structural overview

**Source RDF**

- 103,152 triples, 5,597 unique subjects, 84 unique predicates
- Object positions: 89,898 IRI, 13,254 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **1,395** (24.9%) ; without `rdf:type`: **4,202**

**CPGM**

- 9,524 nodes (1,396 full_iri, 8,128 literal-form)
- 85,469 edges (85,469 labelled, 0 generic-edge)
- 28,883 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 27.494 s |
| role classification | 3.622 s |
| context build (R, R⁻¹, PGIUs) | 6.331 s |
| IF scoring | 0.304 s |
| IP scoring | 0.085 s |
| IR scoring | 0.234 s |
| **total** | **38.074 s** |

## Scores vs thresholds

```
IP   [████████████████████████░░░│] 0.846 / 0.950 ✗
IF   [██████████████████████████░│] 0.934 / 0.950 ✗
IR   [███████████████████████████│] 1.000 / 0.950 ✓
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 0.8459 | 0.9500 | ✗ | 87,257/103,152 full |
| IF | 0.9339 | 0.9500 | ✗ | undef rate 17.90% |
| IR | 1.0000 | 0.9500 | ✓ | universe=100,999 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.9339 — FAIL
- IP: 0.8459 — FAIL

Optional metrics:
- IR: 1.0000 — pass

## Lost triples (IP)

### By expected PGIU type

_These triples have no PGIU by definition — they are lost. The "expected PGIU type" is the kind the framework would have produced had the triple been encoded idiomatically for its source role (derived from the role classifier's output)._

| Expected PGIU type | Lost triples | Share |
|---|---|---|
| Property | 8,815 | 55.5% |
| Edge | 7,080 | 44.5% |

### By source subject (sampled)

_Subjects ranked by lost-triple count across all predicates. Counts here are computed from the per-predicate samples — when a predicate's losses exceed its sample cap (5), the per-subject counts shown are lower bounds. Useful for spotting subjects that are missing across multiple predicates at once._

- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer6` — **7** triple(s) in sample
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer871`
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer289`
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User963`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer2` — **6** triple(s) in sample
    - `http://purl.org/goodrelations/name → "longed manliness encroaching supreme Verizon haversack elicits antagonized"`
    - `http://purl.org/goodrelations/description → "gayety woolliness's ironical disillusions bordello marble citation hocking conservator lesion bettering disposing interrogatives represented discrepancy noggin grooved stepsons"`
    - `http://schema.org/openingHours → "11"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer5` — **5** triple(s) in sample
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User314`
    - `http://purl.org/goodrelations/name → "Phoebe palate's skier drawback's turmeric Tarazed's slack"`
    - `http://schema.org/openingHours → "11"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer9` — **5** triple(s) in sample
    - `http://schema.org/contactPoint → http://db.uwaterloo.ca/~galuc/wsdbm/User330`
    - `http://schema.org/telephone → "8417424"`
    - `http://schema.org/paymentAccepted → "brokerage samba betook evildoers territory agrarian's towelling Glasgow households entrepreneurial classicist mucky pontificates reprobate's plating's Barry expatriated hackle's prizing watermarking…`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer8` — **4** triple(s) in sample
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer771`
    - `http://purl.org/goodrelations/description → "digestible Shelly's emoluments brainiest glory's founders conceive scrub's beck esquire"`
    - `http://schema.org/email → "crematoriums Juliana's Lucia's galloping immunizations mocked memorization's grocers Charity's ergonomics's stubborner randy unwholesome McDonald's jewelry diffraction's hysteresis obligates hoax"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer3` — **4** triple(s) in sample
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer340`
    - `http://schema.org/email → "populist Royce's Gantry horsefly's onion Itasca Nan's lustiness's funnel"`
    - `http://schema.org/contactPoint → http://db.uwaterloo.ca/~galuc/wsdbm/User653`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer4` — **4** triple(s) in sample
    - `http://purl.org/goodrelations/offers → http://db.uwaterloo.ca/~galuc/wsdbm/Offer472`
    - `http://schema.org/contactPoint → http://db.uwaterloo.ca/~galuc/wsdbm/User143`
    - `http://schema.org/paymentAccepted → "Unions vegetable sanitizing Tass's exhuming incapacitating"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer7` — **4** triple(s) in sample
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User606`
    - `http://purl.org/goodrelations/name → "sirup's Cruikshank Shasta recognizance snapdragon's Regor's utilized dissemination's Mulligan devastates pore's skinflint impromptus O'Keeffe enumerates prodigal's dwindled Powers auditory illegitim…`
    - `http://purl.org/goodrelations/description → "summertime's condone pneumonia's Stoic's doorknob tacitness's actresses calendars pickpocket's saltshaker Odis's tradition's hula's comfortable orbital's extrapolation's purebreds Powell rascals dia…`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer0` — **4** triple(s) in sample
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User791`
    - `http://schema.org/employee → http://db.uwaterloo.ca/~galuc/wsdbm/User465`
    - `http://schema.org/email → "Jersey's shrugged perambulator horseback caravans invalidate suites"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer11` — **4** triple(s) in sample
    - `http://purl.org/goodrelations/name → "Gilliam's outplay colic's whimpered malingers cuing"`
    - `http://schema.org/openingHours → "10"`
    - `http://schema.org/email → "fearsome Auriga Macmillan compacting jackrabbit's Gene layaway's bumpkin's"`

### By predicate

Predicates ranked by number of source triples with no PGIU match:

- `http://purl.org/goodrelations/price` — **2,400** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase1448` → `"904"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer785` → `"202"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer270` → `"16"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer118` → `"811"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase502` → `"939"`
- `http://schema.org/eligibleRegion` — **1,924** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer488` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country11`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer543` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country5`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer889` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country2`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer560` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country3`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer230` → `http://db.uwaterloo.ca/~galuc/wsdbm/Country15`
- `http://purl.org/stuff/rev#rating` — **1,500** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review183` → `"4"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review154` → `"6"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review781` → `"6"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review360` → `"10"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review1347` → `"1"`
- `http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor` — **1,500** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase556` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product26`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase1099` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product2`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase311` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product10`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase244` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product13`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase549` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product4`
- `http://purl.org/stuff/rev#reviewer` — **1,500** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review411` → `http://db.uwaterloo.ca/~galuc/wsdbm/User466`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review893` → `http://db.uwaterloo.ca/~galuc/wsdbm/User644`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review16` → `http://db.uwaterloo.ca/~galuc/wsdbm/User518`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review370` → `http://db.uwaterloo.ca/~galuc/wsdbm/User946`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review403` → `http://db.uwaterloo.ca/~galuc/wsdbm/User200`
- `http://purl.org/stuff/rev#text` — **1,063** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review1098` → `"Ivan's indefinitely Carney centrals descent rasps babushka's Rayburn's Dalton's Mandelbrot's Tisha inglorious shortcake's Ujungpandang's sybarites learners lesbian"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review1123` → `"paternally Kresge outlaws purl plunking Leah's phonetic route hornpipe's trimester's"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review772` → `"Rochelle smit Thimbu's shriller marketability pock stewing earthling's typeface flagpoles epistle yahoos semester curler's syphoning protectorates airfares six's distributions sardonically straighter unsure shudders saviors"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review664` → `"Denise's Newtonian's misguides bolstered corrective seediest carburetor's Woodard's emulsion weirdo carousing acorn adulteress coliseum's nippier reprieve specified crossbars Ara Eakins's Solis's entertainingly extorted outgrew rapacity"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review1091` → `"smarter motherfucking MGM exceptional mathematician's fifteens spires saffron O'Connell's birthers Lemuria's bravos sprinkling grooming"`
- `http://purl.org/goodrelations/offers` — **988** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer8` → `http://db.uwaterloo.ca/~galuc/wsdbm/Offer771`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer6` → `http://db.uwaterloo.ca/~galuc/wsdbm/Offer871`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer3` → `http://db.uwaterloo.ca/~galuc/wsdbm/Offer340`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer4` → `http://db.uwaterloo.ca/~galuc/wsdbm/Offer472`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Retailer6` → `http://db.uwaterloo.ca/~galuc/wsdbm/Offer289`
- `http://purl.org/goodrelations/includes` — **900** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer718` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product77`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer592` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product64`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer18` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product67`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer694` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product215`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer731` → `http://db.uwaterloo.ca/~galuc/wsdbm/Product238`
- `http://schema.org/eligibleQuantity` — **900** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer712` → `"8"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer495` → `"6"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer104` → `"7"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer392` → `"6"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer334` → `"2"`
- `http://purl.org/goodrelations/serialNumber` — **900** triple(s)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer611` → `"51846620"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer45` → `"60167295"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer350` → `"24649428"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer767` → `"52305720"`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer867` → `"47949524"`

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 1,395 | 3,190 | 1,037 | 30.4% |
| NPVR | 4,006 | 268 | 4,021 | 93.7% |
| TMR | 1,507 | 0 | 0 | 100.0% |
| ELR | 78,367 | 0 | 7,080 | 100.0% |
| NPKR | 4,489 | 2,894 | 8,815 | 60.8% |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NR** → realized as `literal_node` and `prop_value` instead of `node` (**3,190 units**)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review8`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review910`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase1272`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Purchase63`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Review695`
- **NPVR** → realized as `literal_node` and `prop_value` instead of `prop_value` (**268 units**)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic209`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic172`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic88`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic191`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic132`

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **NPKR** → realized as `Edge` instead of `Property` (**2,894 occurrence(s)**)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User27', 'http://db.uwaterloo.ca/~galuc/wsdbm/gender', 'http://db.uwaterloo.ca/~galuc/wsdbm/Gender1']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Product6', 'http://ogp.me/ns#tag', 'http://db.uwaterloo.ca/~galuc/wsdbm/Topic94']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre26', 'http://ogp.me/ns#tag', 'http://db.uwaterloo.ca/~galuc/wsdbm/Topic152']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User781', 'http://db.uwaterloo.ca/~galuc/wsdbm/gender', 'http://db.uwaterloo.ca/~galuc/wsdbm/Gender1']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Product157', 'http://ogp.me/ns#tag', 'http://db.uwaterloo.ca/~galuc/wsdbm/Topic177']`

### Dropped / undefined units (IF)

- Elements without a μ_e match (or with no scorable kind set): **5,000**
- Occurrences with no covering PGIU: **5,000**

Element-level examples (per role):
- **NR** (5 shown)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer720`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer45`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/City161`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer702`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Offer582`
- **NPVR** (5 shown)
    - `"stoned overdrawn icky airman transitioning tolerably sprayer plasterboard culpability detained tally's credo's dangle"`
    - `"54575869"`
    - `"484"`
    - `"2012-01-17"`
    - `"disciplining purists touchdown dynasty's OHSA ickier cowpuncher's nonabsorbents harden Nanette's smidgin's haters sweetener's war's"`

Occurrence-level examples (per role):
- **ELR** (5 shown)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer718', 'http://purl.org/goodrelations/includes', 'http://db.uwaterloo.ca/~galuc/wsdbm/Product77']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Purchase556', 'http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor', 'http://db.uwaterloo.ca/~galuc/wsdbm…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Purchase1099', 'http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor', 'http://db.uwaterloo.ca/~galuc/wsdb…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/City29', 'http://www.geonames.org/ontology#parentCountry', 'http://db.uwaterloo.ca/~galuc/wsdbm/Count…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer488', 'http://schema.org/eligibleRegion', 'http://db.uwaterloo.ca/~galuc/wsdbm/Country11']`
- **NPKR** (5 shown)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Review183', 'http://purl.org/stuff/rev#rating', '"4"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Review154', 'http://purl.org/stuff/rev#rating', '"6"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer712', 'http://schema.org/eligibleQuantity', '"8"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Review781', 'http://purl.org/stuff/rev#rating', '"6"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer658', 'http://purl.org/goodrelations/validFrom', '"2013-03-10"']`

## Identifier retention tier distribution (IR)

- full: **100,999** ; partial: **0** ; local: **0** / universe 100,999

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 1,396 | 1,396 | 0 | 0 | 0 | 1,396 | 1.0000 |
| `node.label` | 1,507 | 0 | 1,507 | 0 | 0 | 1,507 | 1.0000 |
| `node.property.key` | 4,499 | 10 | 4,489 | 0 | 0 | 4,499 | 1.0000 |
| `node.property.value` | 8,128 | 8,128 | 0 | 0 | 0 | 8,128 | 1.0000 |
| `edge.label` | 85,469 | 0 | 85,469 | 0 | 0 | 85,469 | 1.0000 |

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

![ip_lost_predicates](visualizations/ip_lost_predicates.png)

