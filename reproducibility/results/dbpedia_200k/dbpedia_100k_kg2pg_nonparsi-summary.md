# r2pef report — kg2pg

_Generated 2026-07-03 16:03:22_

## Overview

- Source RDF: `/home/zoe/data/dbpedia/dbpedia_geo_200k.nt`
- Source triples: **194,307**
- CPGM nodes: **149,528** ; relations: **176,643**
- Derived triples (|derived_triples(C)|): **566,920**

## Structural overview

**Source RDF**

- 194,307 triples, 17,664 unique subjects, 227 unique predicates
- Object positions: 62,444 IRI, 131,863 literal, 0 blank node
- Subjects with ≥1 `rdf:type`: **17,664** (100.0%) ; without `rdf:type`: **0**

**CPGM**

- 149,528 nodes (17,665 full_iri, 131,863 literal-form)
- 176,643 edges (176,643 labelled, 0 generic-edge)
- 395,593 properties total

## Performance

| Phase | Wall time |
|---|---|
| config load | 0.002 s |
| CPGM acquisition | 190.294 s |
| role classification | 6.809 s |
| context build (R, R⁻¹, PGIUs) | 21.436 s |
| IF scoring | 1.406 s |
| IP scoring | 0.189 s |
| IR scoring | 1.163 s |
| **total** | **221.301 s** |

## Scores vs thresholds

```
IP   [███████████████████████████│] 1.000 / 0.950 ✓
IF   [███████░░░░░░░░░░░░░░░░░░░░│] 0.257 / 0.950 ✗
IR   [████████████████████░░░░░░░│] 0.723 / 0.950 ✗
```

_The `│` marker on each bar shows the configured threshold._

| Metric | Score | Threshold | Passed | Notes |
|---|---|---|---|---|
| IP | 1.0000 | 0.9500 | ✓ | 194,222/194,222 full |
| IF | 0.2569 | 0.9500 | ✗ | undef rate 0.00% |
| IR | 0.7228 | 0.9500 | ✗ | universe=475,703 |

## Fairness verdict

**Passed:** no

Mandatory metrics:
- IF: 0.2569 — FAIL
- IP: 1.0000 — pass

Optional metrics:
- IR: 0.7228 — fail

## IF — units per role

| Role | Pass | Fail | Undef | %-passed |
|---|---|---|---|---|
| NR | 14,579 | 3,085 | 0 | 82.5% |
| NPVR | 13 | 87,845 | 0 | 0.0% |
| TMR | 17,664 | 0 | 0 | 100.0% |
| ELR | 44,780 | 0 | 0 | 100.0% |
| NPKR | 0 | 131,863 | 0 | 0.0% |

_Detail lists are capped at 5,000 entries per bucket (pass / fail / undef) for memory safety. The aggregate counts above use the full input._

## Non-idiomatic encodings (IF)

### Elements

_When multiple realizations are listed, the source element is encoded in several CPGM locations at once (e.g. once as a literal-form node and separately as a property value) — these are independent handles, not a nesting. The role fails if **any** of those locations uses a non-idiomatic kind, even when other locations use the idiomatic one._

- **NR** → realized as `literal_node`, `node` and `prop_value` instead of `node` (**3,085 units**)
    - `http://dbpedia.org/resource/Andong` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_62912]`, raw=`Andong`
    - `http://dbpedia.org/resource/Campeche` — handle=`prop_value`, form=`literal`, at `node[lit_kg2pg_50146].property[0].value`, raw=`Campeche`
    - `http://dbpedia.org/resource/Nîmes` — handle=`prop_value`, form=`literal`, at `node[lit_kg2pg_97885].property[0].value`, raw=`Nîmes`
    - `http://dbpedia.org/resource/Rochford` — handle=`prop_value`, form=`literal`, at `node[lit_kg2pg_40629].property[0].value`, raw=`Rochford`
    - `http://dbpedia.org/resource/Kilflynn` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_122526]`, raw=`Kilflynn`
- **NPVR** → realized as `literal_node` and `prop_value` instead of `prop_value` (**1,915 units**)
    - `""` — handle=`prop_value`, form=`literal`, at `node[lit_kg2pg_27245].property[0].value`, raw=``
    - `"439050"` — handle=`prop_value`, form=`literal`, at `node[lit_kg2pg_59545].property[0].value`, raw=`439050`
    - `"1342977"` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_66799]`, raw=`1342977`
    - `"Miners"` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_42526]`, raw=`Miners`
    - `"6100000.0"` — handle=`literal_node`, form=`literal`, at `node[lit_kg2pg_123508]`, raw=`6100000.0`

### Occurrences (triples)

_For occurrences, "realized as X" means the source triple was reconstructed by an X PGIU rather than the idiomatic kind for the role._

- **NPKR** → realized as `Edge` instead of `Property` (**5,000 occurrence(s)**)
    - `['http://dbpedia.org/resource/Paterson,_New_Jersey', 'http://dbpedia.org/ontology/utcOffset', '"&minus;05:00"']`
    - `['http://dbpedia.org/resource/EBay', 'http://dbpedia.org/ontology/netIncome', '"1.361E10"']`
    - `['http://dbpedia.org/resource/Webster_Groves,_Missouri', 'http://dbpedia.org/ontology/areaLand', '"1.530682973208576E7"']`
    - `['http://dbpedia.org/resource/Brainerd,_Minnesota', 'http://dbpedia.org/ontology/areaTotal', '"3.320364757450752E7"']`
    - `['http://dbpedia.org/resource/Harlan_County,_Kentucky', 'http://dbpedia.org/ontology/percentageOfAreaWater', '"0.5"']`

## Identifier retention tier distribution (IR)

- full: **343,840** ; partial: **0** ; local: **131,863** / universe 475,703

### By construct group

`Full` totals are further split into `direct` (handle stored a full IRI natively, i.e. `form = full_iri`) and `exp.` (namespace-shortform expanded to a full IRI by the adapter, i.e. `form = namespace_plus_local` with `://` in `resolved`). The split is purely diagnostic — the IR score treats both as `full` (weight 1.0).

| Group | Full | direct | exp. | Partial | Local | Total | Score |
|---|---|---|---|---|---|---|---|
| `node` | 17,665 | 17,665 | 0 | 0 | 0 | 17,665 | 1.0000 |
| `node.label` | 17,664 | 0 | 17,664 | 0 | 131,863 | 149,527 | 0.1181 |
| `node.property.key` | 4 | 4 | 0 | 0 | 0 | 4 | 1.0000 |
| `node.property.value` | 131,864 | 131,864 | 0 | 0 | 0 | 131,864 | 1.0000 |
| `edge.label` | 176,643 | 0 | 176,643 | 0 | 0 | 176,643 | 1.0000 |

Local-tier handle examples (bare local name, namespace discarded):
- `node[lit_kg2pg_0].label[0]` resolved=`double` form=`local_only`
- `node[lit_kg2pg_1].label[0]` resolved=`double` form=`local_only`
- `node[lit_kg2pg_2].label[0]` resolved=`double` form=`local_only`
- `node[lit_kg2pg_3].label[0]` resolved=`gYear` form=`local_only`
- `node[lit_kg2pg_4].label[0]` resolved=`float` form=`local_only`

## Visualisations

![scores_thresholds](visualizations/scores_thresholds.png)

![thresholds_radar](visualizations/thresholds_radar.png)

![if_by_role](visualizations/if_by_role.png)

![if_realized_kinds](visualizations/if_realized_kinds.png)

![ir_tiers](visualizations/ir_tiers.png)

