# r2pef report — rdf2pg_gdm

_Generated 2026-07-03 14:49:30_

## Overview

- Source RDF: `/home/zoe/data/watdiv/watdiv_100k.nt`
- Source triples: **103,152**
- CPGM nodes: **19,194** ; relations: **108,373**
- Derived triples (|derived_triples(C)|): **206,304**

## Structural overview

**Source RDF**

- 103,152 triples, 5,597 unique subjects, 84 unique predicates
- Object positions: 89,898 IRI, 13,254 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **1,395** (24.9%) ; without `rdf:type`: **4,202**

**CPGM**

- 19,194 nodes (5,940 full_iri, 13,254 literal-form)
- 108,373 edges (0 labelled, 108,373 generic-edge)
- 134,881 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 59.064 s |
| role classification | 3.596 s |
| context build (R, R⁻¹, PGIUs) | 6.479 s |
| IF scoring | 0.335 s |
| IP scoring | 0.061 s |
| IR scoring | 0.363 s |
| **total** | **69.948 s** |

## Scores vs thresholds

```
IP   [███████████████████████████│] 1.000 / 0.950 ✓
IF   [█░░░░░░░░░░░░░░░░░░░░░░░░░░│] 0.048 / 0.950 ✗
IR   [███████████████████████████│] 1.000 / 0.950 ✓
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 1.0000 | 0.9500 | ✓ | 103,152/103,152 full |
| IF | 0.0480 | 0.9500 | ✗ | undef rate 0.00% |
| IR | 1.0000 | 0.9500 | ✓ | universe=127,567 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.0480 — FAIL
- IP: 1.0000 — pass

Optional metrics:
- IR: 1.0000 — pass

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 5,622 | 0 | 0 | 100.0% |
| NPVR | 0 | 8,295 | 0 | 0.0% |
| TMR | 0 | 1,507 | 0 | 0.0% |
| ELR | 0 | 85,447 | 0 | 0.0% |
| NPKR | 0 | 16,198 | 0 | 0.0% |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NPVR** → realized as `literal_node` and `prop_value` instead of `prop_value` (**4,812 units**)
    - `"hatchet Gallo Senate's hunkers preexisting Guernsey bestirred chintz's meddling newtons pocketknives immanence hollowed tapir musketry's A…` — handle=`prop_value`, form=`literal`, at `node[lit_gdm_31105].property[0].value`, raw=`hatchet Gallo Senate's hunkers preexisting Guernsey bestirr…`
    - `"blandishment nickelodeons philatelist Bruce"` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_11898]`, raw=`blandishment nickelodeons philatelist Bruce`
    - `"stupidly doses jigged vortexes Lowenbrau's embryos marshalling robes hairpin budgies cancellation heckler Paine's webmaster Robeson vessel…` — handle=`prop_value`, form=`literal`, at `node[lit_gdm_3175].property[0].value`, raw=`stupidly doses jigged vortexes Lowenbrau's embryos marshall…`
    - `"67264069"` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_24479]`, raw=`67264069`
    - `"38442641"` — handle=`literal_node`, form=`literal`, at `node[lit_gdm_21978]`, raw=`38442641`
- **NPVR** → realized as `node` instead of `prop_value` (**188 units**)
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic220`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic79`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic210`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic89`
    - `http://db.uwaterloo.ca/~galuc/wsdbm/Topic154`

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **ELR** → realized as `Generic-edge` instead of `Edge` (**4,184 occurrence(s)**)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User973', 'http://db.uwaterloo.ca/~galuc/wsdbm/follows', 'http://db.uwaterloo.ca/~galuc/wsdbm/User509…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User672', 'http://db.uwaterloo.ca/~galuc/wsdbm/friendOf', 'http://db.uwaterloo.ca/~galuc/wsdbm/User81…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User149', 'http://db.uwaterloo.ca/~galuc/wsdbm/friendOf', 'http://db.uwaterloo.ca/~galuc/wsdbm/User79…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User880', 'http://db.uwaterloo.ca/~galuc/wsdbm/friendOf', 'http://db.uwaterloo.ca/~galuc/wsdbm/User60…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Review424', 'http://purl.org/stuff/rev#reviewer', 'http://db.uwaterloo.ca/~galuc/wsdbm/User798']`
- **NPKR** → realized as `Generic-edge` instead of `Property` (**759 occurrence(s)**)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User895', 'http://db.uwaterloo.ca/~galuc/wsdbm/gender', 'http://db.uwaterloo.ca/~galuc/wsdbm/Gender1']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer612', 'http://purl.org/goodrelations/price', '"767"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Offer102', 'http://purl.org/goodrelations/validThrough', '"2013-12-15"']`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/Product53', 'http://schema.org/text', '"Aymara\'s predilection interlopers debilitates cauterized Uri…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User168', 'http://xmlns.com/foaf/givenName', '"EMMA"']`
- **TMR** → realized as `Generic-edge` instead of `Label` (**57 occurrence(s)**)
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User887', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://db.uwaterloo.ca/~galuc/wsdbm/Rol…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User776', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://db.uwaterloo.ca/~galuc/wsdbm/Rol…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User895', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://db.uwaterloo.ca/~galuc/wsdbm/Rol…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User619', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://db.uwaterloo.ca/~galuc/wsdbm/Rol…`
    - `['http://db.uwaterloo.ca/~galuc/wsdbm/User907', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://db.uwaterloo.ca/~galuc/wsdbm/Rol…`

## Identifier retention tier distribution (IR)

- full: **127,567** ; partial: **0** ; local: **0** / universe 127,567

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 5,940 | 5,940 | 0 | 0 | 0 | 5,940 | 1.0000 |
| `node.property.value` | 13,254 | 13,254 | 0 | 0 | 0 | 13,254 | 1.0000 |
| `edge.property.value` | 108,373 | 108,373 | 0 | 0 | 0 | 108,373 | 1.0000 |

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

