# IDF-B experimental evaluation

Run from the repository root with the Backend virtual environment:

```powershell
& .\Backend\.venv\Scripts\python.exe .\Backend\eval\run_idf_b_eval.py
& .\Backend\.venv\Scripts\python.exe .\Backend\eval\run_idf_b_followup.py
```

The script reads the Stage 6 final mapping labels, Stage 3 app metadata, and
`Backend\fdo_privacy.db`. It runs the existing `analysis_runner` against a
temporary SQLite copy, so generated analyses do not modify the source database.
It writes mapping-level results, confusion matrices, and the report under
`Docs\eval_results\`.

The follow-up run preserves the initial outputs as `first_run_*`, runs standard
extraction against stored policy text for zero-evidence policies in a disposable
SQLite copy, and adds separate seeded-overreach and evidence-coverage tables.
It does not fetch URLs. Because the app's semantic pipeline clears its Fuseki
graph, the follow-up checks `localhost:3030` but evaluates semantics against a
separate temporary in-memory Fuseki instance. It stops that instance and
removes only its uniquely named temporary runtime directory after evaluation;
any already-running persistent Fuseki service and its dataset remain untouched.
The initial mapping-level outputs are preserved as `first_run_*` for comparison.

## Snapshot capture and extraction

`capture_benchmark_policies.py` fetches only usable HTTP(S) URLs already stored
in canonical benchmark policy records. It writes cleaned text, the final URL,
HTTP status, UTC retrieval time, SHA-256, and character count to
`policy_snapshots`; it never updates `policy_documents.raw_text`. Invalid or
missing stored URLs are recorded in a timestamped suggestions CSV with
`needs_human_confirmation=true`; suggested URLs are not fetched.

`snapshot_extraction.py` creates a separate working SQLite copy from the
timestamped frozen database under `Backend/eval/`. It extracts only snapshots
marked `CAPTURED` or `MANUALLY_CAPTURED`, leaving `policy_evidence` untouched.
Extraction runs and deduplicated extracted rows are saved in
`extraction_runs` and `extracted_evidence`. Legacy snapshots are migrated
idempotently to include scope, source note, capture status, and capture method.
Reports are created with unique UTC timestamped names under
`Docs/eval_results/`.

To import a browser/manual capture, supply a UTF-8 file and all provenance
metadata. The file is treated as plain text unless `--html` is provided:

```powershell
& .\Backend\.venv\Scripts\python.exe .\Backend\eval\snapshot_extraction.py `
  --from-file .\Backend\eval\captures\POL-EDU-02.txt `
  --policy-id POL-EDU-02 `
  --final-url https://www.duolingo.com/privacy `
  --http-status 200 `
  --fetched-at 2026-10-14T06:00:00Z `
  --scope "Full privacy policy" `
  --source-note "Rendered browser capture; operator-provided text"
```

`--from-file` inserts a `MANUALLY_CAPTURED` snapshot and does not start
extraction. It requires a valid policy ID, HTTP(S) final URL, successful HTTP
status, UTC timestamp, scope, and source note. The extraction command without
`--from-file` then processes only eligible snapshots. Text is split into
section-aware 10,000-character chunks with 1,000-character overlap; transient
LLM rate-limit/5xx errors use bounded backoff. The existing extractor's regex
fallback is used when no Gemini key is configured or LLM retries are exhausted.

## Test database isolation

The API persistence tests and semantic repository test that write SQLite rows
use the `isolated_app_database` fixture in `Backend/conftest.py`. The fixture
backs up the source database into pytest's temporary directory and redirects
the app engine/session factory there, so test commits and cleanup do not alter
`Backend/fdo_privacy.db`.

## Ground truth

Use `DATA\FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx`,
sheet `Stage 5 Final Mapping Dataset`. `Expected ID`, `App ID`, `Function`,
`Data Type`, and `Final FDO Status` identify each labeled mapping. App names and
categories are joined through `DATA\FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx`,
sheet `Applications`, using `App ID`, `Application`, and `Category`.

The canonical status values are `FDO`, `NOT_FDO`, and `AMBIGUOUS`. For the
parallel `FDO Label` column, `NO_FDO_ESTABLISHED` maps to `NOT_FDO`, and
`PENDING` maps to `AMBIGUOUS`. Earlier Stage 4 values such as `NOT_ASSIGNED`,
`NO_FDO_LABEL`, and `NO_FINAL_FDO` are placeholders and are not evaluation
labels.

The same 93 mapping IDs and labels are present in
`DATA\FDO-Privacy_Stage4E_Ambiguous_Case_Resolution_v1.0.xlsx`, sheet
`Stage 4E Ambiguous Resolution`, columns `Expected ID`, `App ID`, `Function`,
`Data Type`, and `Final FDO Label`.

The Stage 2B A/B annotations in
`DATA\FDO-Privacy_Stage2B_AnnotatorB_All4Batches.xlsx`, sheet `Sheet1`, are
`Necessity (A)`, `Necessity (B)`, `Purpose (A)`, and `Purpose (B)`, not FDO
outcome classes. There are no paired annotator FDO outcome labels from which
to compute Cohen's kappa.

## Policy and extraction inputs

For each ground-truth app, the script selects its canonical `POL-<App ID>`
policy record and associated `policy_evidence` rows. This excludes duplicate
runtime/test policies in the database and does not fetch a live policy URL.
The database's `normalized_evidence` table is empty; the evaluation treats
non-empty canonical `policy_evidence.data_type` identifiers as normalized
evidence. It does not exclude rows based on `extraction_status`.

`analysis_runner` consumes the evidence already stored in SQLite. The
evaluation does not call the LLM extractor or the regex fallback. If
`http://localhost:3030/$/ping` is reachable, the script also invokes the
existing semantic service for each app; otherwise semantic predictions and
metrics are omitted and reported as unavailable.

## Baselines

- **B1 — app-policy type presence:** For each expected mapping, compare its
  expected data-type identifier to every non-empty `policy_evidence.data_type`
  value for that app's selected canonical policy. If present, predict
  `NOT_FDO`; if absent, predict `FDO`. No purpose, function, extraction status,
  or other decision input is considered.
- **B2 — selected-evidence type match only:** Use the relational runner's
  selected evidence and `data_match` field only. `EXACT_MATCH` predicts
  `NOT_FDO`, `NO_MATCH` predicts `FDO`, and `NO_EVIDENCE` predicts `AMBIGUOUS`.
  Purpose compatibility, functional relationship, extraction status, and
  decision confidence are ignored. The current evidence matcher selects
  exact-type evidence or no evidence, so a `NO_MATCH` verdict may not occur.

## Metrics

FDO precision is TP / predicted FDO; recall is TP / gold FDO; F1 is the
harmonic mean. A zero-positive gold set makes recall and F1 undefined. When a
method predicts no FDO labels, precision is also undefined. These values are
written as `NA`, not replaced with zero. Accuracy is overall exact agreement.
The reported AMBIGUOUS share is the fraction of method predictions classified
as `AMBIGUOUS`. Confusion matrices always use row order and column order
`FDO`, `NOT_FDO`, `AMBIGUOUS`.

The report includes accuracy grouped by the Stage 3 app category, as well as
mapping- and app-level accuracy in `results.csv`.

## Follow-up sensitivity

The follow-up script records one original relational verdict and its evidence
group (`NO_EVIDENCE`/Rule 1, insufficient/Rule 2, or a selected extracted
evidence comparison) per labeled mapping. It runs extraction only for the ten
benchmark canonical policy records with no stored evidence, using their
database `raw_text`; it does not retrieve the referenced live URLs.

The seeded overreach test is a controlled sensitivity test, not a labeled
accuracy measurement. It seeds one synthetic, explicitly marked evidence row
for each of ten zero-evidence apps, choosing a data type absent from that app's
expected-data inventory and setting purpose to marketing. The existing
relational matcher selects evidence by exact expected type; the report records
when it therefore does not compare the synthetic row. B1 and B2 sensitivity
counts are reported against each selected app's first expected mapping, with
the B2 counterfactual pairwise mismatch stated explicitly.
