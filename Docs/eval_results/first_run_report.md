# IDF-B experimental results

## 8.1 Dataset and ground truth

- Ground-truth source: `DATA/FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx`, `Stage 5 Final Mapping Dataset`.
- Ground-truth mapping columns: `Expected ID`, `App ID`, `Function`, `Data Type`, and `Final FDO Status`; `FDO Label` was used as a consistency check.
- The same 93 mapping IDs and labels are present in `DATA/FDO-Privacy_Stage4E_Ambiguous_Case_Resolution_v1.0.xlsx`, sheet `Stage 4E Ambiguous Resolution`, columns `Expected ID`, `App ID`, `Function`, `Data Type`, and `Final FDO Label`; the Stage 4E labels match Stage 6 `Final FDO Status` exactly.
- App display name and category: `DATA/FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx`, `Applications` sheet, columns `App ID`, `Application`, and `Category`.
- Labeled mappings: **93**; apps: **29**; canonical policy records: **29** (19 with stored evidence, 10 without stored evidence).
- Ground-truth labels: FDO **0**, NOT_FDO **60**, AMBIGUOUS **33**.
- Coverage against the Stage 3 `Expected Data` sheet: **99** mappings exist; 6 do not appear in the Stage 6 labeled set (EXP-002, EXP-003, EXP-008, EXP-009, EXP-025, EXP-036). The 1 Stage 3 app without Stage 6 ground-truth mappings: ECO-01 (Amazon Shopping).
- Label mapping used: `FDO` → `FDO`; `NOT_FDO` → `NOT_FDO`; `AMBIGUOUS` → `AMBIGUOUS`; the parallel Stage 6 `FDO Label` values `NO_FDO_ESTABLISHED` → `NOT_FDO` and `PENDING` → `AMBIGUOUS`. The canonical `Final FDO Status` column already contains the normalized class values.
- Stage 4 workbooks contain intermediate values such as `NOT_ASSIGNED`, `NO_FDO_LABEL`, and `NO_FINAL_FDO`; these are workflow placeholders, not final outcome labels, and were not counted as ground truth.
- The separate Stage 4D `4D Adjudication` sheet uses `NOT_FDO_ON_CURRENT_EVIDENCE` and `AMBIGUOUS_NEEDS_EVIDENCE` as adjudication decisions while its `Final FDO Label` is `NO_FINAL_FDO`; these preliminary decisions were not substituted for the Stage 4E/Stage 6 final labels.
- The Stage 6 ground truth has no FDO-positive mappings. Consequently no correctly predicted FDO worked example exists, and FDO recall/F1 are undefined; precision is zero only when a method predicted one or more FDOs, otherwise precision is undefined. These undefined values are `NA`, not imputed.
- App mapping IDs in the Stage 6 set were checked against `Backend/fdo_privacy.db`; all 93 expected IDs were found. Each evaluated app used its canonical stored policy ID `POL-<App ID>`, not additional test/runtime policy records.
- `normalized_evidence` has no records. For B1, canonical `policy_evidence.data_type` values were used as the stored normalized data-type evidence. All non-empty data types for the selected policy were considered, without filtering on extraction status.
- Extraction in this evaluation used existing database evidence only. The run did not invoke Gemini/LLM extraction or the regex fallback. The database has no per-row extractor provenance, so the original extraction route for its pre-existing evidence cannot be determined from these fields.

### Annotator agreement

No paired annotator labels for the final FDO / NOT_FDO / AMBIGUOUS outcome are present. `DATA/FDO-Privacy_Stage2B_AnnotatorB_All4Batches.xlsx`, sheet `Sheet1`, contains paired `Necessity (A)` / `Necessity (B)` and `Purpose (A)` / `Purpose (B)` annotations, which are not FDO outcome labels; no Cohen's kappa for the FDO ground-truth classes can therefore be computed. Per-class kappa is likewise unavailable.

## 8.2 Method results

| Method | N | FDO precision | FDO recall | FDO F1 | Accuracy | Predicted AMBIGUOUS share |
|---|---:|---:|---:|---:|---:|---:|
| Relational (analysis_runner) | 93 | 0.000 | NA | NA | 0.323 | 0.903 |
| B1 | 93 | 0.000 | NA | NA | 0.075 | 0.000 |
| B2 | 93 | NA | NA | NA | 0.355 | 0.871 |
| Semantic | NA | NA | NA | NA | NA | NA |

The Fuseki ping at `http://localhost:3030/$/ping` timed out, so no semantic predictions or semantic metrics were computed.

### Per-app-category accuracy

| Method | App category | Mappings | Correct | Accuracy |
|---|---|---:|---:|---:|
| Relational (analysis_runner) | Banking / Finance | 5 | 1 | 0.200 |
| Relational (analysis_runner) | Communication | 5 | 3 | 0.600 |
| Relational (analysis_runner) | E-commerce | 4 | 1 | 0.250 |
| Relational (analysis_runner) | Education | 6 | 4 | 0.667 |
| Relational (analysis_runner) | Fitness | 6 | 2 | 0.333 |
| Relational (analysis_runner) | Food Delivery | 8 | 4 | 0.500 |
| Relational (analysis_runner) | Gaming | 7 | 1 | 0.143 |
| Relational (analysis_runner) | Healthcare | 9 | 2 | 0.222 |
| Relational (analysis_runner) | Multi-function / Stress Case | 11 | 5 | 0.455 |
| Relational (analysis_runner) | Navigation | 5 | 2 | 0.400 |
| Relational (analysis_runner) | Productivity | 6 | 0 | 0.000 |
| Relational (analysis_runner) | Social Media | 5 | 3 | 0.600 |
| Relational (analysis_runner) | Streaming / Entertainment | 6 | 1 | 0.167 |
| Relational (analysis_runner) | Travel | 6 | 0 | 0.000 |
| Relational (analysis_runner) | Utilities | 4 | 1 | 0.250 |
| B1 | Banking / Finance | 5 | 0 | 0.000 |
| B1 | Communication | 5 | 0 | 0.000 |
| B1 | E-commerce | 4 | 0 | 0.000 |
| B1 | Education | 6 | 0 | 0.000 |
| B1 | Fitness | 6 | 1 | 0.167 |
| B1 | Food Delivery | 8 | 0 | 0.000 |
| B1 | Gaming | 7 | 1 | 0.143 |
| B1 | Healthcare | 9 | 0 | 0.000 |
| B1 | Multi-function / Stress Case | 11 | 2 | 0.182 |
| B1 | Navigation | 5 | 1 | 0.200 |
| B1 | Productivity | 6 | 1 | 0.167 |
| B1 | Social Media | 5 | 0 | 0.000 |
| B1 | Streaming / Entertainment | 6 | 0 | 0.000 |
| B1 | Travel | 6 | 0 | 0.000 |
| B1 | Utilities | 4 | 1 | 0.250 |
| B2 | Banking / Finance | 5 | 1 | 0.200 |
| B2 | Communication | 5 | 3 | 0.600 |
| B2 | E-commerce | 4 | 1 | 0.250 |
| B2 | Education | 6 | 4 | 0.667 |
| B2 | Fitness | 6 | 3 | 0.500 |
| B2 | Food Delivery | 8 | 4 | 0.500 |
| B2 | Gaming | 7 | 1 | 0.143 |
| B2 | Healthcare | 9 | 2 | 0.222 |
| B2 | Multi-function / Stress Case | 11 | 5 | 0.455 |
| B2 | Navigation | 5 | 2 | 0.400 |
| B2 | Productivity | 6 | 1 | 0.167 |
| B2 | Social Media | 5 | 3 | 0.600 |
| B2 | Streaming / Entertainment | 6 | 1 | 0.167 |
| B2 | Travel | 6 | 0 | 0.000 |
| B2 | Utilities | 4 | 2 | 0.500 |

### Confusion matrices

Rows are ground truth; columns are predicted. Class order is FDO, NOT_FDO, AMBIGUOUS.

**Relational (analysis_runner)**

| Ground truth \\ Predicted | FDO | NOT_FDO | AMBIGUOUS |
|---|---:|---:|---:|
| FDO | 0 | 0 | 0 |
| NOT_FDO | 2 | 2 | 56 |
| AMBIGUOUS | 4 | 1 | 28 |

**B1**

| Ground truth \\ Predicted | FDO | NOT_FDO | AMBIGUOUS |
|---|---:|---:|---:|
| FDO | 0 | 0 | 0 |
| NOT_FDO | 53 | 7 | 0 |
| AMBIGUOUS | 26 | 7 | 0 |

**B2**

| Ground truth \\ Predicted | FDO | NOT_FDO | AMBIGUOUS |
|---|---:|---:|---:|
| FDO | 0 | 0 | 0 |
| NOT_FDO | 0 | 6 | 54 |
| AMBIGUOUS | 0 | 6 | 27 |

### Kappa

Cohen's kappa for FDO outcome annotations: **not computable** (no paired annotator outcome labels). Per-category FDO kappa: **not computable** for the same reason.

## 8.3 Worked examples

### Correct NOT_FDO — relational analysis

- App/category: Google Maps / Navigation
- Function: Turn-by-turn navigation
- Expected data and purpose: `DATA.LOCATION.PRECISE`; Route/navigation
- Verbatim matched policy text: “Google says precise location is useful in Maps for directions and nearby search; location may come from GPS/sensors/IP/activity and retention depends on product/settings.”
- Data match / purpose compatibility / functional relationship: EXACT_MATCH / COMPATIBLE / RELATED
- Rule fired: Rule 3: Exact data + compatible purpose + related function
- Confidence: 0.9
- Explanation: The declared data type matches the expected data type, the declared purpose is compatible with the expected purpose, and evidence is available for the function.

### Correct FDO

Not available: the selected Stage 6 ground truth contains zero FDO labels. Any FDO prediction would be incorrect against this benchmark, so no correct FDO example can be shown.

### Assumptions and uncomputed values

- Policy selection: the canonical Stage 3 policy record `POL-<App ID>` was used for each benchmark app. It avoids duplicate runtime/test policy records in the SQLite database.
- B1 compares the expected data-type identifier to any non-empty `policy_evidence.data_type` for that app's selected canonical policy: present → NOT_FDO; absent → FDO.
- B2 uses only the relational runner's selected evidence `data_match`: EXACT_MATCH → NOT_FDO, NO_MATCH → FDO, NO_EVIDENCE → AMBIGUOUS.
- Metric values unavailable: FDO recall and F1 for all methods (zero positive gold labels); FDO precision where no FDO predictions were made; all semantic metrics (Fuseki unavailable); and FDO-class kappa.
- The evaluation used an isolated temporary copy of the SQLite database for `analysis_runner`; the source database and application code were not modified.

See `results.csv` for mapping-level results and `confusion_matrix.csv` for all available 3×3 matrices.
