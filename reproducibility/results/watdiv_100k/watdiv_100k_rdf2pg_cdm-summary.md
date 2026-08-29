# r2pef report — rdf2pg_cdm

_Generated 2026-07-03 14:52:41_

## Overview

- Source RDF: `/home/zoe/data/watdiv/watdiv_100k.nt`
- Source triples: **103,152**
- CPGM nodes: **5,901** ; relations: **93,495**
- Derived triples (|derived_triples(C)|): **206,304**

## Structural overview

**Source RDF**

- 103,152 triples, 5,597 unique subjects, 84 unique predicates
- Object positions: 89,898 IRI, 13,254 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **1,395** (24.9%) ; without `rdf:type`: **4,202**

**CPGM**

- 5,901 nodes (5,901 full_iri)
- 93,495 edges (93,495 labelled, 0 generic-edge)
- 13,254 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 21.819 s |
| role classification | 3.477 s |
| context build (R, R⁻¹, PGIUs) | 6.278 s |
| IF scoring | 0.424 s |
| IP scoring | 0.204 s |
| IR scoring | 0.229 s |
| **total** | **32.434 s** |

## Scores vs thresholds

```
IP   [███████████████████████████│] 1.000 / 0.950 ✓
IF   [███████████████████████████│] 0.972 / 0.950 ✓
IR   [███████████████░░░░░░░░░░░░│] 0.526 / 0.950 ✗
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 1.0000 | 0.9500 | ✓ | 103,152/103,152 full |
| IF | 0.9725 | 0.9500 | ✓ | undef rate 0.00% |
| IR | 0.5258 | 0.9500 | ✗ | universe=114,157 |

## Fairness verdict

**Passed:** yes

Mandatory metrics:
- IF: 0.9725 — pass
- IP: 1.0000 — pass

Optional metrics:
- IR: 0.5258 — fail

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 5,622 | 0 | 0 | 100.0% |
| NPVR | 8,016 | 279 | 0 | 96.6% |
| TMR | 1,507 | 0 | 0 | 100.0% |
| ELR | 85,447 | 0 | 0 | 100.0% |
| NPKR | 13,254 | 2,944 | 0 | 81.8% |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NPVR** → realized as `node` instead of `prop_value` (**279 units**)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic208`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic0`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic56`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic206`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic8`

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **NPKR** → realized as `Edge` instead of `Property` (**2,944 occurrence(s)**)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Product246', 'http://ogp.me/ns#tag', 'http://db.uwaterloo.ca/~galuc/wsdbm/Topic72']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User275', 'http://db.uwaterloo.ca/~galuc/wsdbm/gender', 'http://db.uwaterloo.ca/~galuc/wsdbm/Gender1']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Product225', 'http://ogp.me/ns#tag', 'http://db.uwaterloo.ca/~galuc/wsdbm/Topic143']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Product195', 'http://ogp.me/ns#tag', 'http://db.uwaterloo.ca/~galuc/wsdbm/Topic149']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre10', 'http://ogp.me/ns#tag', 'http://db.uwaterloo.ca/~galuc/wsdbm/Topic209']`

## Identifier retention tier distribution (IR)

- full: **5,901** ; partial: **108,256** ; local: **0** / universe 114,157

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 5,901 | 5,901 | 0 | 0 | 0 | 5,901 | 1.0000 |
| `node.label` | 0 | 0 | 0 | 1,507 | 0 | 1,507 | 0.5000 |
| `node.property.key` | 0 | 0 | 0 | 13,254 | 0 | 13,254 | 0.5000 |
| `edge.label` | 0 | 0 | 0 | 93,495 | 0 | 93,495 | 0.5000 |

Partial-tier handle examples (namespace shortform kept, full IRI not reconstructable):
- `node[http://db.uwaterloo.ca/~galuc/wsdbm/Offer353].property[0].key` resolved=`nss1_eligibleQuantity` form=`namespace_plus_local`
- `node[http://db.uwaterloo.ca/~galuc/wsdbm/Offer353].property[1].key` resolved=`nss3_validFrom` form=`namespace_plus_local`
- `node[http://db.uwaterloo.ca/~galuc/wsdbm/Offer353].property[2].key` resolved=`nss3_price` form=`namespace_plus_local`
- `node[http://db.uwaterloo.ca/~galuc/wsdbm/Offer353].property[3].key` resolved=`nss3_serialNumber` form=`namespace_plus_local`
- `node[http://db.uwaterloo.ca/~galuc/wsdbm/Offer486].property[0].key` resolved=`nss1_eligibleQuantity` form=`namespace_plus_local`

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

