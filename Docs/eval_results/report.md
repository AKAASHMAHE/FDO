# IDF-B follow-up evaluation

## Ground truth and agreement

- Ground truth remains read-only: `DATA/FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx` has 99 expected mappings; the final 93 labels are in the Stage 6 `Stage 5 Final Mapping Dataset` sheet, with columns `Expected ID`, `App ID`, `Function`, `Data Type`, and `Final FDO Status`. Matching Stage 4E `Final FDO Label` values were left unchanged.
- Final labeled set: 93 mappings across 29 apps; 0 FDO, 60 NOT_FDO, and 33 AMBIGUOUS. Six of the 99 expected mappings are unlabeled; Amazon Shopping has no Stage 6 mapping.
- Label remaps: `NO_FDO_ESTABLISHED` → `NOT_FDO`; `PENDING` → `AMBIGUOUS` from the parallel Stage 6 `FDO Label`. No other labels were remapped. Placeholder Stage 4 labels were not used.
- No paired final-outcome annotator labels exist, so Cohen's kappa (overall or per category) is not computable.

## Evidence coverage and original run

- Benchmark: 93 labeled mappings across 29 apps; 19 canonical policies had stored evidence (10 did not).
- The following policies had no stored `policy_evidence` rows before extraction:

| App | Policy ID | Labeled mappings covered | Stored policy text status | Text length |
|---|---|---:|---|---:|
| WhatsApp (COM-01) | POL-COM-01 | 3 | NOT_CAPTURED | 81 |
| Telegram (COM-02) | POL-COM-02 | 2 | NOT_CAPTURED | 81 |
| eBay (ECO-02) | POL-ECO-02 | 4 | NOT_CAPTURED | 81 |
| Google Classroom (EDU-01) | POL-EDU-01 | 4 | NOT_CAPTURED | 81 |
| PayPal (FIN-01) | POL-FIN-01 | 3 | NOT_CAPTURED | 81 |
| Google Pay (FIN-02) | POL-FIN-02 | 2 | NOT_CAPTURED | 81 |
| MyChart (HEA-01) | POL-HEA-01 | 6 | NOT_CAPTURED | 81 |
| Waze (NAV-02) | POL-NAV-02 | 2 | PENDING_CAPTURE | 107 |
| Reddit (SOC-02) | POL-SOC-02 | 3 | NOT_CAPTURED | 81 |
| YouTube (STR-02) | POL-STR-02 | 3 | NOT_CAPTURED | 81 |

The ten no-evidence policies cover **32 of the 93 labeled mappings**.

Mappings were classified from the first-run relational comparisons as **79** NO_EVIDENCE / Rule 1, **5** insufficient / Rule 2, and **9** real matched comparisons.

| Evidence-driven group | FDO | NOT_FDO | AMBIGUOUS | Total |
|---|---:|---:|---:|---:|
| NO_EVIDENCE (Rule 1) | 0 | 0 | 79 | 79 |
| INSUFFICIENT_EVIDENCE (Rule 2) | 0 | 0 | 5 | 5 |
| REAL_MATCH_COMPARISON | 6 | 3 | 0 | 9 |

NOT_FDO recall restricted to mappings with a selected stored evidence match: **2/4** (0.500)

The per-mapping original coverage group is included in `results.csv` under `evidence_coverage_group_first_run` and in the preserved first-run details.

## Fill the evidence gap

- Extraction used the app's standard `extract_policy_evidence()` pipeline on the database's stored `raw_text` only; no policy URL was fetched. `GEMINI_API_KEY` is configured in `Backend/.env`, so the pipeline attempted Gemini and used its regex fallback whenever Gemini returned no validated evidence or raised an error. No secret value is recorded.
- All ten no-evidence policies have `NOT_CAPTURED` or `PENDING_CAPTURE`/`PENDING_REGION_CHECK` placeholder text, not a captured policy body. This limits what extraction can produce.

| App | Extraction path used | Gemini attempted | Gemini error type | New evidence rows |
|---|---|---:|---|---:|
| WhatsApp (COM-01) | regex fallback | True | none | 0 |
| Telegram (COM-02) | regex fallback | True | ServerError | 0 |
| eBay (ECO-02) | regex fallback | True | none | 0 |
| Google Classroom (EDU-01) | regex fallback | True | none | 0 |
| PayPal (FIN-01) | regex fallback | True | none | 0 |
| Google Pay (FIN-02) | regex fallback | True | ServerError | 0 |
| MyChart (HEA-01) | regex fallback | True | ServerError | 0 |
| Waze (NAV-02) | regex fallback | True | none | 0 |
| Reddit (SOC-02) | regex fallback | True | none | 0 |
| YouTube (STR-02) | regex fallback | True | ServerError | 0 |

Evidence coverage after running extraction: **19/29 policies** (34 evidence rows total). Before extraction: **19/29 policies** (34 evidence rows total).

The extraction attempt added **0** evidence records from stored policy text; these inputs are marked uncaptured or pending in the database, so this does not measure extraction quality on captured policy bodies.

### Full metric table

| Method and run | N | FDO precision | FDO recall | FDO F1 | Accuracy | Predicted AMBIGUOUS share |
|---|---:|---:|---:|---:|---:|---:|
| first_run_relational | 93 | 0.000 | NA | NA | 0.323 | 0.903 |
| first_run_B1 | 93 | 0.000 | NA | NA | 0.075 | 0.000 |
| first_run_B2 | 93 | NA | NA | NA | 0.355 | 0.871 |
| gapfilled_relational | 93 | 0.000 | NA | NA | 0.323 | 0.903 |
| gapfilled_B1 | 93 | 0.000 | NA | NA | 0.075 | 0.000 |
| gapfilled_B2 | 93 | NA | NA | NA | 0.355 | 0.871 |
| semantic_gapfilled | 93 | 0.000 | NA | NA | 0.140 | 0.376 |

### Confusion matrices

**first_run_relational** (rows ground truth; columns prediction)

| Ground truth \\ Predicted | FDO | NOT_FDO | AMBIGUOUS |
|---|---:|---:|---:|
| FDO | 0 | 0 | 0 |
| NOT_FDO | 2 | 2 | 56 |
| AMBIGUOUS | 4 | 1 | 28 |

**first_run_B1** (rows ground truth; columns prediction)

| Ground truth \\ Predicted | FDO | NOT_FDO | AMBIGUOUS |
|---|---:|---:|---:|
| FDO | 0 | 0 | 0 |
| NOT_FDO | 53 | 7 | 0 |
| AMBIGUOUS | 26 | 7 | 0 |

**first_run_B2** (rows ground truth; columns prediction)

| Ground truth \\ Predicted | FDO | NOT_FDO | AMBIGUOUS |
|---|---:|---:|---:|
| FDO | 0 | 0 | 0 |
| NOT_FDO | 0 | 6 | 54 |
| AMBIGUOUS | 0 | 6 | 27 |

**gapfilled_relational** (rows ground truth; columns prediction)

| Ground truth \\ Predicted | FDO | NOT_FDO | AMBIGUOUS |
|---|---:|---:|---:|
| FDO | 0 | 0 | 0 |
| NOT_FDO | 2 | 2 | 56 |
| AMBIGUOUS | 4 | 1 | 28 |

**gapfilled_B1** (rows ground truth; columns prediction)

| Ground truth \\ Predicted | FDO | NOT_FDO | AMBIGUOUS |
|---|---:|---:|---:|
| FDO | 0 | 0 | 0 |
| NOT_FDO | 53 | 7 | 0 |
| AMBIGUOUS | 26 | 7 | 0 |

**gapfilled_B2** (rows ground truth; columns prediction)

| Ground truth \\ Predicted | FDO | NOT_FDO | AMBIGUOUS |
|---|---:|---:|---:|
| FDO | 0 | 0 | 0 |
| NOT_FDO | 0 | 6 | 54 |
| AMBIGUOUS | 0 | 6 | 27 |

**semantic_gapfilled** (rows ground truth; columns prediction)

| Ground truth \\ Predicted | FDO | NOT_FDO | AMBIGUOUS |
|---|---:|---:|---:|
| FDO | 0 | 0 | 0 |
| NOT_FDO | 38 | 0 | 22 |
| AMBIGUOUS | 20 | 0 | 13 |

### Retained worked example

Correct NOT_FDO — Google Maps (Navigation), Turn-by-turn navigation; expected `DATA.LOCATION.PRECISE` for Route/navigation. Matched policy text: “Google says precise location is useful in Maps for directions and nearby search; location may come from GPS/sensors/IP/activity and retention depends on product/settings.” Data match / purpose compatibility / functional relationship: EXACT_MATCH / COMPATIBLE / RELATED; rule: Rule 3: Exact data + compatible purpose + related function; confidence: 0.9; explanation: The declared data type matches the expected data type, the declared purpose is compatible with the expected purpose, and evidence is available for the function.

No correct FDO worked example is possible: the gold set has zero FDO mappings.

### False FDO flags on unseeded benchmark mappings

- First-run relational: **6** false FDO flags.
- B1: **79** false FDO flags.
- B2: **0** false FDO flags.

Every FDO prediction on the unseeded benchmark is a false FDO flag because the gold set has zero FDO labels.

## Seeded overreach sensitivity test (synthetic; not accuracy)

Ten apps with no initial evidence were selected. One evidence row was added to each temporary database, marked `SYNTHETIC_TEST`, with an expected-data type not present among any expected type for that app and purpose `Marketing`. The seeded rows and app-specific expected-type lists are recorded in `seeded_overreach_sensitivity.csv`.

| Method | Seed rows flagged FDO | Rule / confidence |
|---|---:|---|
| Relational `analysis_runner` on benchmark mappings | 0 / 10 | No synthetic row was selected: exact expected-type filtering prevented comparison. The associated anchor mappings retained Rule 1 / confidence 0.30; the synthetic row itself has no rule/confidence.
| B1 app-type presence on anchor mappings | 10 / 10 | FDO whenever anchor expected type is absent from all policy evidence; no rule/confidence (baseline).
| B2 direct data-type-only comparison to synthetic row | 10 / 10 | FDO on `NO_MATCH`; no rule/confidence (baseline).

This controlled result describes the current matching surface: the relational runner only considers evidence with an exact expected data type, so unrelated declared types do not reach its mismatch rule. The B1/B2 synthetic checks are sensitivity comparisons against each app's first sorted expected mapping; they do not claim real-world accuracy.

## Semantic branch

| Method and run | N | FDO precision | FDO recall | FDO F1 | Accuracy | Predicted AMBIGUOUS share |
|---|---:|---:|---:|---:|---:|---:|
| Semantic, gap-filled | 93 | 0.000 | NA | NA | 0.140 | 0.376 |

Semantic and gap-filled relational verdicts differ on **55 mappings**.
localhost:3030 answered the initial reachability probe but was unreachable at post-run verification. The semantic branch used a separate temporary in-memory endpoint (http://localhost:60380) and was stopped after analysis, avoiding changes to any existing persistent store.

| Expected ID | App | Relational | Semantic | Reason for difference |
|---|---|---|---|---|
| EXP-010 | Instagram (SOC-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-011 | Instagram (SOC-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-015 | Google Maps (NAV-01) | NOT_FDO | AMBIGUOUS | Relational: Rule 3: Exact data + compatible purpose + related function (The declared data type matches the expected data type, the declared purpose is compatible with the expected purpose, and evidence is available for the function.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-016 | Google Maps (NAV-01) | NOT_FDO | AMBIGUOUS | Relational: Rule 3: Exact data + compatible purpose + related function (The declared data type matches the expected data type, the declared purpose is compatible with the expected purpose, and evidence is available for the function.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-037 | Practo (HEA-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-038 | Practo (HEA-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-039 | Practo (HEA-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-044 | Duolingo (EDU-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-045 | Duolingo (EDU-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-046 | Netflix (STR-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-047 | Netflix (STR-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-048 | Netflix (STR-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-053 | Google Drive (PRO-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-054 | Google Drive (PRO-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-056 | Microsoft OneDrive (PRO-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-057 | Microsoft OneDrive (PRO-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-058 | Google Authenticator (UTL-01) | AMBIGUOUS | FDO | Relational: Rule 2: Insufficient or unknown evidence (Evidence is insufficient to make a deterministic FDO decision.); Semantic: The declared data type matches the expected data type, but the declared purpose is incompatible with the expected functional purpose. |
| EXP-059 | Google Authenticator (UTL-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-061 | Google Home (UTL-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-062 | Booking.com (TRV-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-063 | Booking.com (TRV-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-064 | Booking.com (TRV-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-065 | Uber (TRV-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-066 | Uber (TRV-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-067 | Uber (TRV-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-068 | Uber Eats (FOD-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-069 | Uber Eats (FOD-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-070 | Uber Eats (FOD-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-071 | Uber Eats (FOD-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-072 | DoorDash (FOD-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-073 | DoorDash (FOD-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-074 | DoorDash (FOD-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-075 | DoorDash (FOD-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-077 | Strava (FIT-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-078 | Strava (FIT-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-079 | Strava (FIT-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-081 | Google Fit (FIT-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-082 | PUBG MOBILE (GAM-01) | AMBIGUOUS | FDO | Relational: Rule 2: Insufficient or unknown evidence (Evidence is insufficient to make a deterministic FDO decision.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-083 | PUBG MOBILE (GAM-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-084 | PUBG MOBILE (GAM-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-085 | PUBG MOBILE (GAM-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-086 | Minecraft (GAM-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-087 | Minecraft (GAM-02) | AMBIGUOUS | FDO | Relational: Rule 2: Insufficient or unknown evidence (Evidence is insufficient to make a deterministic FDO decision.); Semantic: The declared data type matches the expected data type, but the declared purpose is incompatible with the expected functional purpose. |
| EXP-088 | Minecraft (GAM-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-089 | Google Photos (AMB-01) | NOT_FDO | AMBIGUOUS | Relational: Rule 3: Exact data + compatible purpose + related function (The declared data type matches the expected data type, the declared purpose is compatible with the expected purpose, and evidence is available for the function.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-090 | Google Photos (AMB-01) | AMBIGUOUS | FDO | Relational: Rule 2: Insufficient or unknown evidence (Evidence is insufficient to make a deterministic FDO decision.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-091 | Google Photos (AMB-01) | AMBIGUOUS | FDO | Relational: Rule 2: Insufficient or unknown evidence (Evidence is insufficient to make a deterministic FDO decision.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-092 | Google Photos (AMB-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-093 | Google Photos (AMB-01) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: No unique semantic finding was returned for this mapping. |
| EXP-094 | WeChat (AMB-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-095 | WeChat (AMB-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-096 | WeChat (AMB-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-097 | WeChat (AMB-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-098 | WeChat (AMB-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |
| EXP-099 | WeChat (AMB-02) | AMBIGUOUS | FDO | Relational: Rule 1: No declared evidence (No declared evidence is available to determine whether the data collection is functionally justified.); Semantic: The declared data type differs from the expected functional data type despite available evidence linking the collection to the evaluated function. |

Semantic confusion matrix (rows ground truth; columns prediction):

| Ground truth \\ Predicted | FDO | NOT_FDO | AMBIGUOUS |
|---|---:|---:|---:|
| FDO | 0 | 0 | 0 |
| NOT_FDO | 38 | 0 | 22 |
| AMBIGUOUS | 20 | 0 | 13 |

## Assumptions and uncomputed values

- Only canonical policy IDs `POL-<App ID>` and existing stored policy text/evidence were used. No source URL was fetched. All extraction/evidence seeding occurred in disposable copies of the SQLite database.
- Before/after coverage counts policy evidence rows, and per-mapping evidence group is based on the exact comparison status persisted by `analysis_runner`: `NO_EVIDENCE` = Rule 1; `INSUFFICIENT`/`UNKNOWN` or non-`EXTRACTED` = Rule 2; selected extracted evidence = real comparison.
- B1 and B2 retain the definitions in `Backend/eval/README.md`; seeded B2 is explicitly a direct synthetic expected-vs-declared data-type comparison because the production matcher does not select the injected unrelated type.
- If extraction yields zero evidence from placeholder text, the uncomputed gap-fill improvement is not a model failure measurement: source policy text is absent. Real-policy extraction quality cannot be evaluated from these rows.
- The gold set still has zero FDO cases, so FDO recall and F1 remain undefined; semantic metrics and semantic disagreement reasons are unavailable if isolated Fuseki cannot run. Kappa remains unavailable because there are no paired final-outcome annotator labels. Per-category accuracy is included for each method/mapping in `results.csv`; per-category kappa is not computable.

First-run snapshots are retained as `first_run_results.csv`, `first_run_confusion_matrix.csv`, and `first_run_report.md`. The updated full mapping-level table and matrices are in `results.csv` and `confusion_matrix.csv`.
