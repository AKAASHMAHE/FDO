# IDF-B diagnostic report

Diagnostic-only, read-only inspection of application source, Stage 3 workbook labels/data, and `Backend/fdo_privacy.db`. No application code, workbook, or database was changed. The only generated artifacts are this report and the diagnostic script under the permitted folders.

## 1. Type-code consistency

Stage 3 `Expected Data` (`Data Type ID`): **36 distinct non-empty codes** across 99 populated rows.

| Expected Data sheet codes |
|---|
| `DATA.ACCOUNT.GOOGLE` |
| `DATA.ACCOUNT.USER_ID` |
| `DATA.AUTH.SECRET_KEY` |
| `DATA.COM.MESSAGE_CONTENT` |
| `DATA.COMM.MESSAGE_CONTENT` |
| `DATA.CONTACT.ADDRESS` |
| `DATA.CONTACT.EMAIL` |
| `DATA.CONTACT.EMAIL_PHONE_USERNAME` |
| `DATA.CONTACTS.LIST` |
| `DATA.DEVICE.ID` |
| `DATA.DEVICE.SMART_HOME` |
| `DATA.DEVICE.STORAGE` |
| `DATA.FILE.USER_FILES` |
| `DATA.FINANCIAL.PAYMENT` |
| `DATA.FINANCIAL.TRANSACTION` |
| `DATA.GAMING.GAMEPLAY` |
| `DATA.HEALTH.ACTIVITY` |
| `DATA.HEALTH.APPOINTMENT` |
| `DATA.HEALTH.HEART_RATE` |
| `DATA.HEALTH.PROVIDER_PREFERENCES` |
| `DATA.HEALTH.RECORD` |
| `DATA.LOCATION.APPROXIMATE` |
| `DATA.LOCATION.PRECISE` |
| `DATA.MEDIA.CAMERA` |
| `DATA.MEDIA.MICROPHONE` |
| `DATA.MEDIA.PHOTOS_VIDEOS` |
| `DATA.USAGE.ACTIVITY_HISTORY` |
| `DATA.USAGE.ASSIGNMENT_CONTENT` |
| `DATA.USAGE.CART_ACTIVITY` |
| `DATA.USAGE.COMMENT_CONTENT` |
| `DATA.USAGE.LESSON_ACTIVITY` |
| `DATA.USAGE.PLAYBACK_ACTIVITY` |
| `DATA.USAGE.POST_CONTENT` |
| `DATA.USAGE.PROGRESS_RECORDS` |
| `DATA.USAGE.SEARCH_HISTORY` |
| `DATA.USAGE.WATCH_HISTORY` |

`expected_mappings.data_type` in SQLite: **42 distinct non-empty codes**. Workbook-vs-DB set differences: **6**.

| Codes present in only one expected-type source |
|---|
| `DATA.ACCOUNT` (DB only) |
| `DATA.CONTACTS` (DB only) |
| `DATA.DEVICE` (DB only) |
| `DATA.FINANCIAL` (DB only) |
| `DATA.MEDIA` (DB only) |
| `DATA.USAGE` (DB only) |

Complete `expected_mappings.data_type` set (shared values plus DB-only values):

| SQLite expected_mappings.data_type |
|---|
| `DATA.ACCOUNT` |
| `DATA.ACCOUNT.GOOGLE` |
| `DATA.ACCOUNT.USER_ID` |
| `DATA.AUTH.SECRET_KEY` |
| `DATA.COM.MESSAGE_CONTENT` |
| `DATA.COMM.MESSAGE_CONTENT` |
| `DATA.CONTACT.ADDRESS` |
| `DATA.CONTACT.EMAIL` |
| `DATA.CONTACT.EMAIL_PHONE_USERNAME` |
| `DATA.CONTACTS` |
| `DATA.CONTACTS.LIST` |
| `DATA.DEVICE` |
| `DATA.DEVICE.ID` |
| `DATA.DEVICE.SMART_HOME` |
| `DATA.DEVICE.STORAGE` |
| `DATA.FILE.USER_FILES` |
| `DATA.FINANCIAL` |
| `DATA.FINANCIAL.PAYMENT` |
| `DATA.FINANCIAL.TRANSACTION` |
| `DATA.GAMING.GAMEPLAY` |
| `DATA.HEALTH.ACTIVITY` |
| `DATA.HEALTH.APPOINTMENT` |
| `DATA.HEALTH.HEART_RATE` |
| `DATA.HEALTH.PROVIDER_PREFERENCES` |
| `DATA.HEALTH.RECORD` |
| `DATA.LOCATION.APPROXIMATE` |
| `DATA.LOCATION.PRECISE` |
| `DATA.MEDIA` |
| `DATA.MEDIA.CAMERA` |
| `DATA.MEDIA.MICROPHONE` |
| `DATA.MEDIA.PHOTOS_VIDEOS` |
| `DATA.USAGE` |
| `DATA.USAGE.ACTIVITY_HISTORY` |
| `DATA.USAGE.ASSIGNMENT_CONTENT` |
| `DATA.USAGE.CART_ACTIVITY` |
| `DATA.USAGE.COMMENT_CONTENT` |
| `DATA.USAGE.LESSON_ACTIVITY` |
| `DATA.USAGE.PLAYBACK_ACTIVITY` |
| `DATA.USAGE.POST_CONTENT` |
| `DATA.USAGE.PROGRESS_RECORDS` |
| `DATA.USAGE.SEARCH_HISTORY` |
| `DATA.USAGE.WATCH_HISTORY` |

Near-duplicate diagnostic rule: case/outer-whitespace-insensitive code equality after replacing only the `DATA.COMM.` namespace prefix with `DATA.COM.`. This is a hypothesis used only for counting; no stored code was normalized or altered.

| Near-duplicate spellings |
|---|
| `DATA.COM.MESSAGE_CONTENT` ↔ `DATA.COMM.MESSAGE_CONTENT` |

Additional namespace/granularity warnings (these are not treated as equal codes):

- Evidence-only `LOCATION`, `LOCATION.PRECISE`, and `precise_location` lack the same canonical `DATA.LOCATION.PRECISE` spelling/namespace used by expected mappings.
- Evidence types `DATA.ACCOUNT`, `DATA.CONTACTS`, `DATA.DEVICE`, `DATA.FINANCIAL`, `DATA.MEDIA`, and `DATA.USAGE` are parent/broader codes while expected values include namespaced descendants (for example `DATA.DEVICE.ID` or `DATA.USAGE.WATCH_HISTORY`).
- `DATA.ACCOUNT.PERSONAL_INFO`, `DATA.CONTACT.PHONE_EMAIL`, `DATA.HEALTH.PERSONAL_HEALTH`, `DATA.HEALTH.VITALS`, `DATA.MEDIA.AUDIO_VIDEO`, `DATA.USAGE.ACTIVITY_LOGS`, and `DATA.USAGE.TRIP_DETAILS` are related-sounding but not canonical exact expected codes. Their semantic equivalence is not assumed.


Distinct `policy_evidence.data_type` values across the entire source DB: **31 distinct values**, 31 non-empty.

| Evidence data_type | Rows |
|---|---:|
| `DATA.ACCOUNT` | 37 |
| `DATA.ACCOUNT.PERSONAL_INFO` | 8 |
| `DATA.ACCOUNT.USER_ID` | 1 |
| `DATA.AUTH.SECRET_KEY` | 1 |
| `DATA.CONTACT.PHONE_EMAIL` | 1 |
| `DATA.CONTACTS` | 29 |
| `DATA.DEVICE` | 32 |
| `DATA.DEVICE.ID` | 2 |
| `DATA.DEVICE.SENSOR` | 1 |
| `DATA.DEVICE.SMART_HOME` | 1 |
| `DATA.FILE.USER_FILES` | 2 |
| `DATA.FINANCIAL` | 19 |
| `DATA.FINANCIAL.PAYMENT` | 1 |
| `DATA.GAMING.GAMEPLAY` | 1 |
| `DATA.HEALTH.ACTIVITY` | 2 |
| `DATA.HEALTH.HEART_RATE` | 1 |
| `DATA.HEALTH.PERSONAL_HEALTH` | 1 |
| `DATA.HEALTH.VITALS` | 1 |
| `DATA.LOCATION` | 19 |
| `DATA.LOCATION.APPROXIMATE` | 19 |
| `DATA.LOCATION.PRECISE` | 103 |
| `DATA.MEDIA` | 5 |
| `DATA.MEDIA.AUDIO_VIDEO` | 1 |
| `DATA.MEDIA.PHOTOS_VIDEOS` | 2 |
| `DATA.OTHER` | 14 |
| `DATA.USAGE` | 21 |
| `DATA.USAGE.ACTIVITY_LOGS` | 3 |
| `DATA.USAGE.TRIP_DETAILS` | 1 |
| `LOCATION` | 5 |
| `LOCATION.PRECISE` | 2 |
| `precise_location` | 133 |

Evidence types that never exactly equal a code in `expected_mappings`: **13**.

| Evidence type with no exact expected-type equality |
|---|
| `DATA.ACCOUNT.PERSONAL_INFO` |
| `DATA.CONTACT.PHONE_EMAIL` |
| `DATA.DEVICE.SENSOR` |
| `DATA.HEALTH.PERSONAL_HEALTH` |
| `DATA.HEALTH.VITALS` |
| `DATA.LOCATION` |
| `DATA.MEDIA.AUDIO_VIDEO` |
| `DATA.OTHER` |
| `DATA.USAGE.ACTIVITY_LOGS` |
| `DATA.USAGE.TRIP_DETAILS` |
| `LOCATION` |
| `LOCATION.PRECISE` |
| `precise_location` |

## 2. Rule 1 despite app-level stored evidence

First-run relational rows matching `Rule 1: No declared evidence` where the canonical app policy nevertheless has at least one stored evidence row: **47 labeled mappings**.
For each mapping, `app evidence (type — purpose)` lists the canonical policy's distinct type/purpose pairs. `alias match` uses only the diagnostic `DATA.COMM.` → `DATA.COM.` normalization above.

| Expected ID | App | Expected type | App evidence (type — purpose) | Alias match |
|---|---|---|---|---|
| EXP-010 | Instagram (SOC-01) | `DATA.COM.MESSAGE_CONTENT` | DATA.USAGE.ACTIVITY_LOGS — Service operation; personalization/ads where applicable | none |
| EXP-011 | Instagram (SOC-01) | `DATA.MEDIA.CAMERA` | DATA.USAGE.ACTIVITY_LOGS — Service operation; personalization/ads where applicable | none |
| EXP-037 | Practo (HEA-02) | `DATA.HEALTH.APPOINTMENT` | DATA.CONTACT.PHONE_EMAIL — Account registration; service communication; DATA.HEALTH.PERSONAL_HEALTH — Provide services; research/statistical/business intelligence in aggregated or non-personally identifiable form; service improvement | none |
| EXP-038 | Practo (HEA-02) | `DATA.MEDIA.CAMERA` | DATA.CONTACT.PHONE_EMAIL — Account registration; service communication; DATA.HEALTH.PERSONAL_HEALTH — Provide services; research/statistical/business intelligence in aggregated or non-personally identifiable form; service improvement | none |
| EXP-039 | Practo (HEA-02) | `DATA.MEDIA.MICROPHONE` | DATA.CONTACT.PHONE_EMAIL — Account registration; service communication; DATA.HEALTH.PERSONAL_HEALTH — Provide services; research/statistical/business intelligence in aggregated or non-personally identifiable form; service improvement | none |
| EXP-044 | Duolingo (EDU-02) | `DATA.USAGE.LESSON_ACTIVITY` | DATA.USAGE.ACTIVITY_LOGS — Service operation; advertising/targeted advertising where applicable | none |
| EXP-045 | Duolingo (EDU-02) | `DATA.USAGE.PROGRESS_RECORDS` | DATA.USAGE.ACTIVITY_LOGS — Service operation; advertising/targeted advertising where applicable | none |
| EXP-046 | Netflix (STR-01) | `DATA.USAGE.PLAYBACK_ACTIVITY` | DATA.ACCOUNT.PERSONAL_INFO — Account management; service delivery | none |
| EXP-047 | Netflix (STR-01) | `DATA.USAGE.WATCH_HISTORY` | DATA.ACCOUNT.PERSONAL_INFO — Account management; service delivery | none |
| EXP-048 | Netflix (STR-01) | `DATA.DEVICE.STORAGE` | DATA.ACCOUNT.PERSONAL_INFO — Account management; service delivery | none |
| EXP-053 | Google Drive (PRO-01) | `DATA.DEVICE.STORAGE` | DATA.FILE.USER_FILES — Provide storage/search; spam filtering; virus/malware protection; service improvement | none |
| EXP-054 | Google Drive (PRO-01) | `DATA.CONTACT.EMAIL` | DATA.FILE.USER_FILES — Provide storage/search; spam filtering; virus/malware protection; service improvement | none |
| EXP-056 | Microsoft OneDrive (PRO-02) | `DATA.CONTACT.EMAIL` | DATA.FILE.USER_FILES — Provide, improve and protect service; search/indexing | none |
| EXP-057 | Microsoft OneDrive (PRO-02) | `DATA.DEVICE.STORAGE` | DATA.FILE.USER_FILES — Provide, improve and protect service; search/indexing | none |
| EXP-059 | Google Authenticator (UTL-01) | `DATA.ACCOUNT.GOOGLE` | DATA.AUTH.SECRET_KEY — Generate verification codes | none |
| EXP-061 | Google Home (UTL-02) | `DATA.MEDIA.MICROPHONE` | DATA.DEVICE.ID — Service operation; diagnostics; performance; security; DATA.DEVICE.SENSOR — Connected-home functionality; safety; service improvement; DATA.DEVICE.SMART_HOME — Device/home management; service operation; DATA.MEDIA.AUDIO_VIDEO — Voice/video features; device functionality; safety/improvement | none |
| EXP-062 | Booking.com (TRV-01) | `DATA.LOCATION.APPROXIMATE` | DATA.ACCOUNT.PERSONAL_INFO — Trip reservation; customer support | none |
| EXP-063 | Booking.com (TRV-01) | `DATA.CONTACT.EMAIL` | DATA.ACCOUNT.PERSONAL_INFO — Trip reservation; customer support | none |
| EXP-064 | Booking.com (TRV-01) | `DATA.FINANCIAL.PAYMENT` | DATA.ACCOUNT.PERSONAL_INFO — Trip reservation; customer support | none |
| EXP-065 | Uber (TRV-02) | `DATA.LOCATION.PRECISE` | DATA.ACCOUNT.PERSONAL_INFO — Account access; ride service; payment | none |
| EXP-066 | Uber (TRV-02) | `DATA.LOCATION.PRECISE` | DATA.ACCOUNT.PERSONAL_INFO — Account access; ride service; payment | none |
| EXP-067 | Uber (TRV-02) | `DATA.FINANCIAL.PAYMENT` | DATA.ACCOUNT.PERSONAL_INFO — Account access; ride service; payment | none |
| EXP-068 | Uber Eats (FOD-01) | `DATA.LOCATION.APPROXIMATE` | DATA.ACCOUNT.PERSONAL_INFO — Ordering and delivery; customer support; DATA.USAGE.TRIP_DETAILS — Order fulfillment; support; service operation | none |
| EXP-069 | Uber Eats (FOD-01) | `DATA.CONTACT.ADDRESS` | DATA.ACCOUNT.PERSONAL_INFO — Ordering and delivery; customer support; DATA.USAGE.TRIP_DETAILS — Order fulfillment; support; service operation | none |
| EXP-070 | Uber Eats (FOD-01) | `DATA.FINANCIAL.PAYMENT` | DATA.ACCOUNT.PERSONAL_INFO — Ordering and delivery; customer support; DATA.USAGE.TRIP_DETAILS — Order fulfillment; support; service operation | none |
| EXP-071 | Uber Eats (FOD-01) | `DATA.LOCATION.PRECISE` | DATA.ACCOUNT.PERSONAL_INFO — Ordering and delivery; customer support; DATA.USAGE.TRIP_DETAILS — Order fulfillment; support; service operation | none |
| EXP-072 | DoorDash (FOD-02) | `DATA.LOCATION.APPROXIMATE` | DATA.ACCOUNT.PERSONAL_INFO — Ordering and delivery; account/service operation | none |
| EXP-073 | DoorDash (FOD-02) | `DATA.CONTACT.ADDRESS` | DATA.ACCOUNT.PERSONAL_INFO — Ordering and delivery; account/service operation | none |
| EXP-074 | DoorDash (FOD-02) | `DATA.FINANCIAL.PAYMENT` | DATA.ACCOUNT.PERSONAL_INFO — Ordering and delivery; account/service operation | none |
| EXP-075 | DoorDash (FOD-02) | `DATA.LOCATION.PRECISE` | DATA.ACCOUNT.PERSONAL_INFO — Ordering and delivery; account/service operation | none |
| EXP-077 | Strava (FIT-01) | `DATA.LOCATION.PRECISE` | DATA.ACCOUNT.PERSONAL_INFO — Account creation/update; service delivery; DATA.DEVICE.ID — Service operation; analytics; security; DATA.FINANCIAL.PAYMENT — Subscription/payment processing; DATA.HEALTH.ACTIVITY — Record activities; analyze performance; GPS features; DATA.HEALTH.HEART_RATE — Performance insights | none |
| EXP-078 | Strava (FIT-01) | `DATA.CONTACTS.LIST` | DATA.ACCOUNT.PERSONAL_INFO — Account creation/update; service delivery; DATA.DEVICE.ID — Service operation; analytics; security; DATA.FINANCIAL.PAYMENT — Subscription/payment processing; DATA.HEALTH.ACTIVITY — Record activities; analyze performance; GPS features; DATA.HEALTH.HEART_RATE — Performance insights | none |
| EXP-079 | Strava (FIT-01) | `DATA.USAGE.ACTIVITY_HISTORY` | DATA.ACCOUNT.PERSONAL_INFO — Account creation/update; service delivery; DATA.DEVICE.ID — Service operation; analytics; security; DATA.FINANCIAL.PAYMENT — Subscription/payment processing; DATA.HEALTH.ACTIVITY — Record activities; analyze performance; GPS features; DATA.HEALTH.HEART_RATE — Performance insights | none |
| EXP-081 | Google Fit (FIT-02) | `DATA.HEALTH.HEART_RATE` | DATA.HEALTH.ACTIVITY — Track activities; analytics; activity history; DATA.HEALTH.VITALS — Health/fitness tracking; DATA.LOCATION.PRECISE — Calculate distance; create activity maps | none |
| EXP-083 | PUBG MOBILE (GAM-01) | `DATA.ACCOUNT.USER_ID` | DATA.ACCOUNT.PERSONAL_INFO — Account creation; game provision; security; support/improvement; DATA.GAMING.GAMEPLAY — Provide enabled game features/services; personalize gaming experience | none |
| EXP-084 | PUBG MOBILE (GAM-01) | `DATA.CONTACTS.LIST` | DATA.ACCOUNT.PERSONAL_INFO — Account creation; game provision; security; support/improvement; DATA.GAMING.GAMEPLAY — Provide enabled game features/services; personalize gaming experience | none |
| EXP-085 | PUBG MOBILE (GAM-01) | `DATA.FINANCIAL.PAYMENT` | DATA.ACCOUNT.PERSONAL_INFO — Account creation; game provision; security; support/improvement; DATA.GAMING.GAMEPLAY — Provide enabled game features/services; personalize gaming experience | none |
| EXP-086 | Minecraft (GAM-02) | `DATA.GAMING.GAMEPLAY` | DATA.ACCOUNT.USER_ID — Account/game access; multiplayer | none |
| EXP-088 | Minecraft (GAM-02) | `DATA.FINANCIAL.PAYMENT` | DATA.ACCOUNT.USER_ID — Account/game access; multiplayer | none |
| EXP-092 | Google Photos (AMB-01) | `DATA.CONTACT.EMAIL` | DATA.MEDIA.PHOTOS_VIDEOS — AI/Gemini features inside Photos; DATA.MEDIA.PHOTOS_VIDEOS — Photo/video storage, organization, editing, sharing | none |
| EXP-093 | Google Photos (AMB-01) | `DATA.DEVICE.STORAGE` | DATA.MEDIA.PHOTOS_VIDEOS — AI/Gemini features inside Photos; DATA.MEDIA.PHOTOS_VIDEOS — Photo/video storage, organization, editing, sharing | none |
| EXP-094 | WeChat (AMB-02) | `DATA.COM.MESSAGE_CONTENT` | DATA.ACCOUNT.PERSONAL_INFO — PENDING official policy capture | none |
| EXP-095 | WeChat (AMB-02) | `DATA.MEDIA.MICROPHONE` | DATA.ACCOUNT.PERSONAL_INFO — PENDING official policy capture | none |
| EXP-096 | WeChat (AMB-02) | `DATA.MEDIA.CAMERA` | DATA.ACCOUNT.PERSONAL_INFO — PENDING official policy capture | none |
| EXP-097 | WeChat (AMB-02) | `DATA.FINANCIAL.PAYMENT` | DATA.ACCOUNT.PERSONAL_INFO — PENDING official policy capture | none |
| EXP-098 | WeChat (AMB-02) | `DATA.USAGE.POST_CONTENT` | DATA.ACCOUNT.PERSONAL_INFO — PENDING official policy capture | none |
| EXP-099 | WeChat (AMB-02) | `DATA.LOCATION.PRECISE` | DATA.ACCOUNT.PERSONAL_INFO — PENDING official policy capture | none |

Under the stated alias normalization, **0/47** Rule-1 mappings would have a type-equal evidence row. **47/47** have no type-related row even after that alias mapping, although every row in this subset's app has some stored evidence. Thus **0/47** have no evidence row at all at the app level; **47/47** lack a type-equal or alias-equal row. This distinction matters: Rule 1 is per expected-type lookup, not an app-wide absence-of-evidence test.

## 3. Rule-4 false FDO predictions

The first-run relational output contains **6 FDO predictions**; all are false against this gold set because it has no FDO labels. Purpose categories below are produced with the app's existing deterministic purpose classifier; `app category` is the Stage 3 application category.

| Expected ID | App / app category | Expected purpose / purpose category | Selected evidence purpose / category | Compatibility | Cause under current classifier |
|---|---|---|---|---|---|
| EXP-017 | Google Maps (NAV-01; Navigation) | Search/localization / `SEARCH` | Relevant results; security; localization / `SECURITY` | `INCOMPATIBLE` | Taxonomy gap/collision: `localization` is not a taxonomy term; the declared `security` clause wins classification |
| EXP-052 | Google Drive (PRO-01; Productivity) | File storage/sync / `UNCLASSIFIED` | Provide storage/search; spam filtering; virus/malware protection; service improvement / `SEARCH` | `INCOMPATIBLE` | Taxonomy coverage gap: at least one purpose is unclassified |
| EXP-055 | Microsoft OneDrive (PRO-02; Productivity) | File storage/sync / `UNCLASSIFIED` | Provide, improve and protect service; search/indexing / `SEARCH` | `INCOMPATIBLE` | Taxonomy coverage gap: at least one purpose is unclassified |
| EXP-060 | Google Home (UTL-02; Utilities) | Device control / `UNCLASSIFIED` | Device/home management; service operation / `SERVICE_OPERATION` | `INCOMPATIBLE` | Taxonomy coverage gap: at least one purpose is unclassified |
| EXP-076 | Strava (FIT-01; Fitness) | Activity tracking / `UNCLASSIFIED` | Record activities; analyze performance; GPS features / `UNCLASSIFIED` | `INCOMPATIBLE` | Taxonomy coverage gap: at least one purpose is unclassified |
| EXP-080 | Google Fit (FIT-02; Fitness) | Fitness tracking / `UNCLASSIFIED` | Track activities; analytics; activity history / `ANALYTICS` | `INCOMPATIBLE` | Taxonomy coverage gap: at least one purpose is unclassified |

The code normalizes case, whitespace, and `-`, `_`, `/` separators; then exact normalized text is compatible. Otherwise it compares one expected category to all categories found in the declared purpose. If either side is unclassified it returns `INCOMPATIBLE`, not `UNKNOWN`. For the six rows, five have an unclassified expected purpose; the sixth (`Search/localization` vs a declared purpose containing `security; localization`) is a taxonomy collision because `localization` is absent from the controlled phrases and `SECURITY` is selected. None is attributable only to case/separator normalization, and these outputs do not establish a true human-level purpose mismatch. Relevant code: [comparison_service.py:176-207](../../../Backend/app/services/comparison_service.py#L176-L207), [comparison_service.py:313-360](../../../Backend/app/services/comparison_service.py#L313-L360); Rule 4 decision is [fdo_decision_service.py:101-117](../../../Backend/app/services/fdo_decision_service.py#L101-L117).

## 4. Unreachable relational Rule 5

**For the current `analysis_runner` path, `data_match == NO_MATCH` is unreachable.** The matcher filters the evidence query by both policy ID and exact `PolicyEvidence.data_type == expected.data_type`; an empty result returns `NO_EVIDENCE`. A selected row necessarily has the same data type as the expected mapping. When the matcher reports ambiguity it returns `evidence=None`, which again makes comparison data `NO_EVIDENCE`, not `NO_MATCH`.

> `PolicyEvidence.data_type == expected.data_type`

> `if not evidence_rows: ... status="NO_EVIDENCE"`

Evidence matcher: [evidence_matcher.py:54-75](../../../Backend/app/services/evidence_matcher.py#L54-L75). The runner passes only `evidence_match.evidence` to comparison at [analysis_runner.py:150-165](../../../Backend/app/services/analysis_runner.py#L150-L165), and stores its type at [analysis_runner.py:168-183](../../../Backend/app/services/analysis_runner.py#L168-L183). `evaluate_data_match` can return `NO_MATCH` for unequal non-empty types [comparison_service.py:155-175](../../../Backend/app/services/comparison_service.py#L155-L175), but the exact-type matcher prevents an unequal row from reaching it. The Rule 5 branch exists at [fdo_decision_service.py:119-136](../../../Backend/app/services/fdo_decision_service.py#L119-L136), but is unreachable through this runner.

Thus seeded unrelated evidence is never compared because its type fails the matcher's SQL equality predicate; no fallback iterates over nonmatching evidence. This is a current selection design, and it makes the relational Rule 5 branch dead for this production path.

## 5. Semantic branch vs relational branch

`FDO_DETECTION_QUERY` matches expected and declared data joined to app/function, and emits a binding only when the type OR purpose strings differ: [fdo_detection_queries.py:10-36](../../../Backend/app/ontology/fdo_detection_queries.py#L10-L36). It therefore does not enumerate equal-type/equal-purpose pairs or create an explicit negative/empty finding for each expected mapping.

| SPARQL case | Semantic handling |
|---|---|
| Type-mismatch binding | `semantic_finding_to_decision_input` sets `NO_MATCH` when expected and declared type differ; it sets purpose compatibility from the shared comparator, functional relationship to `RELATED`, and evidence status to `EXTRACTED`. When the policy purpose is compatible and the type differs, FDO Rule 5 returns FDO. See [semantic_decision_adapter.py:15-57](../../../Backend/app/ontology/semantic_decision_adapter.py#L15-L57) and [fdo_decision_service.py:119-136](../../../Backend/app/services/fdo_decision_service.py#L119-L136). |
| No binding for the expected mapping | If the query returns no usable binding for that mapping, the eval harness still creates a result row for every benchmark Expected ID. Its effective binding group is empty, so the verdict set is empty and prediction becomes AMBIGUOUS. Raw findings that fail the app/service usability filter also leave an empty effective group. The reason string is `No unique semantic finding was returned...`. See [db_semantic_result_service.py:216-230](../../../Backend/app/ontology/db_semantic_result_service.py#L216-L230) and [run_idf_b_eval.py:326-336](../../../Backend/eval/run_idf_b_eval.py#L326-L336). |
| Several bindings for the expected mapping | The harness collects distinct `fdo_status` values. If all findings have one common verdict, it returns that verdict even if there are several findings; if verdicts differ, it returns AMBIGUOUS. The reason is `No unique...` whenever binding count is not exactly one. Same source lines. |

In `semantic_gapfilled` output, **59 mappings** have the `No unique semantic finding` reason. Split by recorded verdict:

| Semantic verdict | Count | Expected IDs |
|---|---:|---|
| FDO | 24 | EXP-017, EXP-037, EXP-038, EXP-039, EXP-060, EXP-061, EXP-068, EXP-069, EXP-070, EXP-071, EXP-076, EXP-077, EXP-078, EXP-079, EXP-080, EXP-081, EXP-082, EXP-083, EXP-084, EXP-085, EXP-090, EXP-091, EXP-092, EXP-093 |
| NOT_FDO | 0 | — |
| AMBIGUOUS | 35 | EXP-001, EXP-004, EXP-005, EXP-006, EXP-007, EXP-012, EXP-013, EXP-014, EXP-015, EXP-016, EXP-018, EXP-019, EXP-020, EXP-021, EXP-022, EXP-023, EXP-024, EXP-026, EXP-027, EXP-028, EXP-029, EXP-030, EXP-031, EXP-032, EXP-033, EXP-034, EXP-035, EXP-040, EXP-041, EXP-042, EXP-043, EXP-049, EXP-050, EXP-051, EXP-089 |

A `No unique...` FDO is not a zero-binding FDO: the harness's empty verdict set maps to AMBIGUOUS. For a recorded FDO with that reason, the code implies multiple findings whose distinct verdict set was exactly `{FDO}`. This follows from the independent tests of verdict-set size and finding-list size. That same-verdict aggregation is explicit implementation behavior, not evidence of a single unique semantic explanation; the diagnostic reason is misleadingly phrased for it. Whether returning FDO for unanimous multiple findings is intended cannot be established from code alone. If the design contract requires a unique binding, this is a confirmed aggregation defect; if the contract permits unanimous aggregation, the defect is the reason text/traceability. No policy intent is assumed here.

The ontology service deduplicates exact semantic rows and groups multiple purposes for identical data relationships before returning them [db_semantic_result_service.py:16-72](../../../Backend/app/ontology/db_semantic_result_service.py#L16-L72); the detector yields each remaining SPARQL binding [fuseki_semantic_detector.py:20-43](../../../Backend/app/ontology/fuseki_semantic_detector.py#L20-L43). `DBSemanticResultService.analyze` clears and rebuilds the graph, filters findings for the target app and `is_semantic_finding_usable`, then adapts each usable finding; it returns only findings that survive those filters and does not create a row for an unmatched expected mapping [db_semantic_result_service.py:177-252](../../../Backend/app/ontology/db_semantic_result_service.py#L177-L252).

## 6. Benchmark policy text and stored URL

All **29 canonical benchmark policy records** use `POL-<App ID>`. Text classification uses the stored text itself: explicit uncaptured/pending markers mean placeholder; a short value containing pipe-delimited source/status/notes is a reference/registry note, not a policy body. No record is called an actual captured policy body based only on title/status metadata. Length is Python character count; excerpt is at most 200 characters. The URL column reports `source_identifier` verbatim (not fetched); values without an `http(s)://` prefix are source descriptions, not URLs.
Classification totals: **13** explicit uncaptured/pending placeholders, **16** registry/reference-status notes, and **0** records whose stored text is identifiable as an actual policy body.

| App (ID) | Policy ID | Text classification | Length | Stored URL/source_identifier | Excerpt (max 200 chars) |
|---|---|---|---:|---|---|
| Google Photos (AMB-01) | POL-AMB-01 | placeholder/reference status note — not policy body | 170 | non-URL source descriptor: `Google Privacy Policy + Google Photos Privacy Hub` | `Google Privacy Policy + Google Photos Privacy Hub \| VERIFIED_PRODUCT_GUIDANCE \| Photos privacy hub gives product-specific rules; unified Google policy remains applicable.` |
| WeChat (AMB-02) | POL-AMB-02 | placeholder — explicit uncaptured/pending marker | 165 | non-URL source descriptor: `WeChat Privacy Protection Guidelines / official privacy source` | `WeChat Privacy Protection Guidelines / official privacy source \| PENDING_DIRECT_CAPTURE \| Need direct official WeChat privacy document before extracting policy data.` |
| WhatsApp (COM-01) | POL-COM-01 | placeholder — explicit uncaptured/pending marker | 81 | NULL: `<NULL>` | `NOT_CAPTURED \| No policy registry record was available in the extraction batches.` |
| Telegram (COM-02) | POL-COM-02 | placeholder — explicit uncaptured/pending marker | 81 | NULL: `<NULL>` | `NOT_CAPTURED \| No policy registry record was available in the extraction batches.` |
| eBay (ECO-02) | POL-ECO-02 | placeholder — explicit uncaptured/pending marker | 81 | NULL: `<NULL>` | `NOT_CAPTURED \| No policy registry record was available in the extraction batches.` |
| Google Classroom (EDU-01) | POL-EDU-01 | placeholder — explicit uncaptured/pending marker | 81 | NULL: `<NULL>` | `NOT_CAPTURED \| No policy registry record was available in the extraction batches.` |
| Duolingo (EDU-02) | POL-EDU-02 | placeholder/reference status note — not policy body | 166 | URL: `https://www.duolingo.com/privacy` | `https://www.duolingo.com/privacy \| PARTIAL_VERIFIED \| Official privacy-choice page confirms collection via interactions/cookies and sharing with advertising partners.` |
| PayPal (FIN-01) | POL-FIN-01 | placeholder — explicit uncaptured/pending marker | 81 | NULL: `<NULL>` | `NOT_CAPTURED \| No policy registry record was available in the extraction batches.` |
| Google Pay (FIN-02) | POL-FIN-02 | placeholder — explicit uncaptured/pending marker | 81 | NULL: `<NULL>` | `NOT_CAPTURED \| No policy registry record was available in the extraction batches.` |
| Strava (FIT-01) | POL-FIT-01 | placeholder/reference status note — not policy body | 90 | URL: `https://www.strava.com/legal/privacy/` | `https://www.strava.com/legal/privacy/ \| VERIFIED \| Current official Strava Privacy Policy.` |
| Google Fit (FIT-02) | POL-FIT-02 | placeholder/reference status note — not policy body | 159 | non-URL source descriptor: `Google Privacy Policy + Google Fit Help` | `Google Privacy Policy + Google Fit Help \| VERIFIED_PRODUCT_GUIDANCE \| Use unified Google Privacy Policy plus Fit-specific data/location/connected-app guidance.` |
| Uber Eats (FOD-01) | POL-FOD-01 | placeholder/reference status note — not policy body | 164 | non-URL source descriptor: `Uber Privacy Overview / Uber Eats data help` | `Uber Privacy Overview / Uber Eats data help \| VERIFIED_ENTRY_POINT \| Uber Eats points users to Uber Privacy Overview/Notice; exact regional notice must be captured.` |
| DoorDash (FOD-02) | POL-FOD-02 | placeholder/reference status note — not policy body | 125 | URL: `https://about.doordash.com/en-us/privacy` | `https://about.doordash.com/en-us/privacy \| VERIFIED_SOURCE \| Regional policy must be selected before final dataset inclusion.` |
| PUBG MOBILE (GAM-01) | POL-GAM-01 | placeholder/reference status note — not policy body | 170 | non-URL source descriptor: `PUBG MOBILE Privacy Policy linked from official site/store` | `PUBG MOBILE Privacy Policy linked from official site/store \| PARTIAL_VERIFIED \| Official store listing links the Privacy Policy; current policy text needs direct capture.` |
| Minecraft (GAM-02) | POL-GAM-02 | placeholder — explicit uncaptured/pending marker | 180 | non-URL source descriptor: `Minecraft Privacy Policy / Microsoft Privacy Statement` | `Minecraft Privacy Policy / Microsoft Privacy Statement \| PENDING_DIRECT_CAPTURE \| Official Minecraft site links to Privacy Policy; use Microsoft privacy statement where applicable.` |
| MyChart (HEA-01) | POL-HEA-01 | placeholder — explicit uncaptured/pending marker | 81 | NULL: `<NULL>` | `NOT_CAPTURED \| No policy registry record was available in the extraction batches.` |
| Practo (HEA-02) | POL-HEA-02 | placeholder/reference status note — not policy body | 158 | URL: `https://www.practo.com/company/privacy` | `https://www.practo.com/company/privacy \| PARTIAL_VERIFIED \| Current page should be captured; older official PDF provides detailed collection/purpose language.` |
| Google Maps (NAV-01) | POL-NAV-01 | placeholder/reference status note — not policy body | 57 | non-URL source descriptor: `Google Privacy Policy + Product Privacy Guide` | `Google Privacy Policy + Product Privacy Guide \| EXTRACTED` |
| Waze (NAV-02) | POL-NAV-02 | placeholder — explicit uncaptured/pending marker | 107 | URL: `https://www.waze.com/legal/privacy/` | `https://www.waze.com/legal/privacy/ \| PENDING_CAPTURE \| Exact current version/effective date needs capture.` |
| Google Drive (PRO-01) | POL-PRO-01 | placeholder/reference status note — not policy body | 118 | URL: `https://policies.google.com/privacy` | `https://policies.google.com/privacy \| VERIFIED_SOURCE_MODEL \| Use unified policy plus Drive-specific privacy guidance.` |
| Microsoft OneDrive (PRO-02) | POL-PRO-02 | placeholder/reference status note — not policy body | 143 | URL: `https://www.microsoft.com/en-us/privacy/privacystatement` | `https://www.microsoft.com/en-us/privacy/privacystatement \| VERIFIED \| OneDrive has product-specific section within Microsoft Privacy Statement.` |
| Instagram (SOC-01) | POL-SOC-01 | placeholder — explicit uncaptured/pending marker | 117 | URL: `https://privacycenter.instagram.com/policy/` | `https://privacycenter.instagram.com/policy/ \| PENDING_CAPTURE \| Exact live page/version still needs archival capture.` |
| Reddit (SOC-02) | POL-SOC-02 | placeholder — explicit uncaptured/pending marker | 81 | NULL: `<NULL>` | `NOT_CAPTURED \| No policy registry record was available in the extraction batches.` |
| Netflix (STR-01) | POL-STR-01 | placeholder/reference status note — not policy body | 31 | non-URL source descriptor: `Netflix Help Center` | `Netflix Help Center \| EXTRACTED` |
| YouTube (STR-02) | POL-STR-02 | placeholder — explicit uncaptured/pending marker | 81 | NULL: `<NULL>` | `NOT_CAPTURED \| No policy registry record was available in the extraction batches.` |
| Booking.com (TRV-01) | POL-TRV-01 | placeholder/reference status note — not policy body | 133 | URL: `https://www.booking.com/content/privacy.html` | `https://www.booking.com/content/privacy.html \| VERIFIED \| Notice states it covers websites, mobile apps and travel-related purchases.` |
| Uber (TRV-02) | POL-TRV-02 | placeholder/reference status note — not policy body | 31 | non-URL source descriptor: `Uber Data Explainer` | `Uber Data Explainer \| EXTRACTED` |
| Google Authenticator (UTL-01) | POL-UTL-01 | placeholder/reference status note — not policy body | 195 | URL: `https://policies.google.com/privacy` | `https://policies.google.com/privacy \| PRODUCT_GUIDANCE \| Authenticator help documents account sync and local/offline use; policy extraction must distinguish app function from Google Account sync.` |
| Google Home (UTL-02) | POL-UTL-02 | placeholder/reference status note — not policy body | 152 | non-URL source descriptor: `Google Home & Nest Privacy Hub` | `Google Home & Nest Privacy Hub \| VERIFIED_PRODUCT_GUIDANCE \| Uses Google's unified Privacy Policy plus connected-home product-specific privacy guidance.` |

## Confirmed defects vs design choices vs data gaps

### Confirmed implementation inconsistencies (observable; intent caveated)

- The comparator maps unclassifiable purpose text to `INCOMPATIBLE`; five Rule-4 cases have unclassified expected purpose and one hits the localization/security taxonomy collision. The decision engine then emits FDO. This path is confirmed; whether unknown purpose should be FDO or AMBIGUOUS requires a decision contract. [comparison_service.py:343-360](../../../Backend/app/services/comparison_service.py#L343-L360).
- The evaluator labels every zero-or-many binding case `No unique...`; for multiple same-verdict findings it can report FDO while describing the finding as non-unique. This is a confirmed reason/traceability inconsistency. Whether same-verdict aggregation itself violates the intended contract is unresolved without a stated contract. [run_idf_b_eval.py:326-336](../../../Backend/eval/run_idf_b_eval.py#L326-L336).

### Design choices

- Evidence selection is exact type equality and selects a best purpose match only among same-type evidence; this makes relational Rule 5 unreachable. The latter is a confirmed code-path property, but whether it is a defect or intended selection boundary depends on whether unrelated evidence is supposed to reach Rule 5. [evidence_matcher.py:54-116](../../../Backend/app/services/evidence_matcher.py#L54-L116), [analysis_runner.py:150-183](../../../Backend/app/services/analysis_runner.py#L150-L183), [fdo_decision_service.py:119-136](../../../Backend/app/services/fdo_decision_service.py#L119-L136).
- The semantic query is a positive mismatch/purpose-difference detector, not a complete per-mapping classifier; the eval harness assigns AMBIGUOUS to absent findings and aggregates unanimous verdicts [fdo_detection_queries.py:10-36](../../../Backend/app/ontology/fdo_detection_queries.py#L10-L36), [run_idf_b_eval.py:326-336](../../../Backend/eval/run_idf_b_eval.py#L326-L336).
- `DATA.COMM.` → `DATA.COM.` is only a diagnostic alias hypothesis in this report. No rule or stored type was changed.

### Data gaps

- Stage 3 policy bodies are not independently verified against live URLs; all recorded URLs were read from SQLite and not fetched. Evidence is at [report.md:279-315](report.md#L279-L315).
- Whether a repeated unanimous semantic verdict is intended to count as sufficiently unique cannot be settled without a product/design contract; observed behavior is [run_idf_b_eval.py:326-336](../../../Backend/eval/run_idf_b_eval.py#L326-L336).
- Whether type namespace aliases such as `COMM` and `COM` are semantically equivalent cannot be settled from code alone; observed values are listed at [report.md:5-172](report.md#L5-L172).
- Purpose-category labels are a code taxonomy, not human adjudications. A category mismatch can be a taxonomy limitation or an actual purpose mismatch; the rows are at [report.md:230-244](report.md#L230-L244), and the taxonomy is [comparison_service.py:3-98](../../../Backend/app/services/comparison_service.py#L3-L98).
