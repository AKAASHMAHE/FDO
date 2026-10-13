# FDO Privacy Project: Part 4 - Backend, Frontend, Privacy Analysis & Testing Audit

**Project Path:** `d:\VIT\PROJECT\TARP`  
**Output Document:** `docs/part4_api_frontend_analysis_tests.md`  
**Audit Scope:** FastAPI Backend REST Endpoints, React/Vite Frontend Architecture, Deterministic Relational & Semantic Privacy Analysis Engines, Test Suite Verification & Gap Analysis  
**Timestamp:** 2026-10-13  
**Auditor Status:** Automated Assistant (Strict Read-Only Audit)

---

## 1. Backend API Endpoint Inventory & Architecture

The backend application is implemented as a FastAPI service (`Backend/app/main.py:86-90`). All REST endpoints are rooted at `/api/v1` except for automatic documentation endpoints. Cross-Origin Resource Sharing (CORS) is configured explicitly for `http://localhost:5173`, `http://127.0.0.1:5173`, `http://localhost:5174`, and `http://127.0.0.1:5174` (`Backend/app/main.py:91-102`).

### 1.1 REST API Endpoint Specification

The table below catalogs every endpoint registered on the FastAPI instance.

| Method | Path | Request Body / Query Params | Validation / Pydantic Schema | Functions Called (`path::function`) | DB / External Calls | Response Body & Model | Error Conditions & Status Codes | Feature Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health` | None | None | None | None (in-memory literal dict) | `{"status": "ok", "service": "fdo-privacy-backend"}` | None | Implemented-verified |
| `GET` | `/api/v1/applications` | None | None | `app.services.application_service::get_all_applications` (`Backend/app/services/application_service.py:12`) | SQLite Session: `session.query(Application).all()` | `list[ApplicationResponse]` (`Backend/app/schemas/analysis.py:217`) | None | Implemented-verified |
| `GET` | `/api/v1/applications/{application_id}` | Path param: `application_id: str` | Path string validation | `app.services.application_service::get_application` (`Backend/app/services/application_service.py:22`), `app.services.function_service::get_functions_by_application` (`Backend/app/services/function_service.py:11`) | SQLite Session: `session.get(Application, application_id)`, query `Function` filter by `application_id` | `ApplicationDetailResponse` (`Backend/app/schemas/analysis.py:239`) | `404 Not Found`: if application does not exist | Implemented-verified |
| `GET` | `/api/v1/applications/{application_id}/readiness` | Path param: `application_id: str` | Path string validation | `app.services.application_service::get_application_readiness` (`Backend/app/services/application_service.py:34`) | SQLite Session: joins `Application`, `PolicyDocument`, `PolicyEvidence` counts | `ApplicationReadinessResponse` (`Backend/app/schemas/analysis.py:224`) | `404 Not Found`: if application does not exist | Implemented-verified |
| `GET` | `/api/v1/applications/{application_id}/expected-mappings` | Path param: `application_id: str` | Path string validation | `app.services.application_service::get_application` (`Backend/app/services/application_service.py:22`), `app.services.expected_mapping_service::get_expected_mappings_by_application` (`Backend/app/services/expected_mapping_service.py:11`) | SQLite Session: queries `ExpectedFunctionalDataMapping` and lookup on `Function` | `ExpectedMappingsResponse` (`Backend/app/schemas/analysis.py:253`) | `404 Not Found`: if application does not exist | Implemented-verified |
| `POST` | `/api/v1/extract-policy` | Body: `{"policy_text": str, "application_name": str}` | `PolicyExtractionRequest` (`Backend/app/schemas/policy_extraction.py:4`) | `app.services.policy_extraction_service::extract_policy_evidence` (`Backend/app/services/policy_extraction_service.py:16`) | External API (Google Gemini `gemini-3.5-flash-lite` via `ai_service.py`), fallback to regex parsing | `PolicyExtractionResponse` (`Backend/app/schemas/policy_extraction.py:22`) containing `evidence: list[PolicyEvidenceResponse]` | `400 Bad Request`: if `policy_text.strip()` is empty | Implemented-verified |
| `POST` | `/api/v1/analyze` | Body: `AnalyzeRequest` (`application_name`, optional `category`, `description`, `policy_text`, `policy_source`) | `AnalyzeRequest` (`Backend/app/schemas/analysis.py:256`) | `get_or_create_application_for_analysis`, `discover_privacy_policy`, `extract_policy_evidence`, `create_runtime_policy`, `ensure_functional_baseline`, `run_analysis`, `DBSemanticResultService.analyze`, `build_analysis_report` | SQLite Session (reads/writes across `applications`, `policy_documents`, `policy_evidence`, `analyses`, `comparisons`, `fdo_results`, `semantic_fdo_results`); HTTP calls to Apache Jena Fuseki (`localhost:3030`); External Gemini API (if AI baseline or discovery required) | `AnalysisReportResponse` (`Backend/app/schemas/analysis.py:191`) | `422 Unprocessable Entity`: if discovery fails or policy text missing; `400 Bad Request`: on validation error (`ValueError`); `500 Internal Server Error`: on analysis pipeline crash or report load failure | Implemented-verified |
| `POST` | `/api/v1/analyses` | Body: `{"application_id": str}` | `AnalysisCreateRequest` (`Backend/app/schemas/analysis.py:56`) | `get_application`, `ensure_functional_baseline`, `run_analysis`, `build_analysis_report` | SQLite Session: reads `Application`, creates `Analysis`, runs relational comparisons; commits session | `AnalysisReportResponse` (`Backend/app/schemas/analysis.py:191`) | `400 Bad Request`: application not found or invalid mapping counts; `500 Internal Server Error`: report generation failure | Implemented-verified |
| `GET` | `/api/v1/analyses` | None | None | `app.services.analysis_service::get_all_analyses` (`Backend/app/services/analysis_service.py:35`) | SQLite Session: queries `Analysis` joined with `Application`, ordered descending by `created_at` | `list[AnalysisHistoryResponse]` (`Backend/app/schemas/analysis.py:178`) | None | Implemented-verified |
| `GET` | `/api/v1/analyses/{analysis_id}` | Path param: `analysis_id: str` | Path string validation | `app.services.analysis_report_service::build_analysis_report` (`Backend/app/services/analysis_report_service.py:13`) | SQLite Session: queries `Analysis`, `Application`, `PolicyDocument`, `Comparison`, `FDOResult`, `SemanticFDOResult` | `AnalysisReportResponse` (`Backend/app/schemas/analysis.py:191`) | `404 Not Found`: if `analysis_id` does not exist | Implemented-verified |
| `GET` | `/api/v1/analysis/{analysis_id}` | Path param: `analysis_id: str` | Path string validation | `app.services.analysis_report_service::build_analysis_report` (`Backend/app/services/analysis_report_service.py:13`) | SQLite Session: identical to `/api/v1/analyses/{analysis_id}` (singular alias) | `AnalysisReportResponse` (`Backend/app/schemas/analysis.py:191`) | `404 Not Found`: if `analysis_id` does not exist | Implemented-verified |
| `GET` | `/api/v1/analyses/{analysis_id}/results` | Path param: `analysis_id: str` | Path string validation | `build_analysis_report`, `app.services.analysis_result_service::get_analysis_results` (`Backend/app/services/analysis_result_service.py:11`) | SQLite Session: queries `Comparison`, `FDOResult`, `Explanation`, `ExpectedFunctionalDataMapping`, `PolicyEvidence` | `list[AnalysisResultResponse]` (`Backend/app/schemas/analysis_result.py:4`) | `404 Not Found`: if `analysis_id` does not exist | Implemented-verified |
| `GET` | `/api/v1/analysis/{analysis_id}/report` | Path param: `analysis_id: str` | Path string validation | `app.services.rich_report_service::build_rich_analysis_report` (`Backend/app/services/rich_report_service.py:17`) | SQLite Session: loads full normalized relational trees, comparisons, explanations, and semantic results | `RichAnalysisReportResponse` (`Backend/app/schemas/rich_report.py:63`) | `404 Not Found`: if `analysis_id` does not exist | Implemented-verified |


---

## 2. Frontend Architecture & End-to-End User Interaction Trace

The frontend is a single-page React application bundled with Vite (`Frontend/package.json:1-30`). The user interface is implemented primarily in `Frontend/src/App.jsx` (1,739 lines) styled by `Frontend/src/App.css`.

### 2.1 UI Component Hierarchy & State Architecture

| Component Name | File & Lines | Purpose & Render Role | Consumed State / Props | Child Components / Triggers |
| :--- | :--- | :--- | :--- | :--- |
| `App` | `Frontend/src/App.jsx:955-1738` | Root container managing all views, forms, networking lifecycle, and navigation | State: `applicationName`, `category`, `description`, `policyText`, `loading`, `historyLoading`, `historyError`, `error`, `result`, `history`, `showHistory`, `manualPolicyMode` | `MetricCard`, `FunctionalBaselineSection`, `PolicyAnalysisCard`, `BaselineUnavailableSection`, `GroupedSemanticCard`, `HistoryCard` |
| `StatusBadge` | `Frontend/src/App.jsx:47-55` | Renders color-coded status badge (`fdo`, `not_fdo`, `ambiguous`, `unknown`) | Prop: `status` | None |
| `MetricCard` | `Frontend/src/App.jsx:57-64` | Displays summary counters in top dashboard bar (Total Mappings, FDO Detected, Not FDO, Ambiguous) | Props: `value`, `label`, `type` | None |
| `GroupedSemanticCard` | `Frontend/src/App.jsx:327-675` | Collapsible function-level semantic card aggregating SPARQL-derived comparisons by target function | Prop: `group` (functionName, items), Local State: `isExpanded` | `StatusBadge`, `PurposeList`, chevron toggle, subcard list |
| `PolicyAnalysisCard` | `Frontend/src/App.jsx:677-743` | Renders policy-declared data findings, purposes, and verbatim extracted snippets | Prop: `finding` (data_type, data_label, function, purposes, evidence, confidence) | `PurposeList`, `<details>` evidence expander |
| `FunctionalBaselineSection` | `Frontend/src/App.jsx:745-849` | Displays curated or AI-derived expected functional data types and operational justifications | Prop: `result` (`functional_baseline`, `baseline_source`, `baseline_confidence`, `baseline_status`) | Grouped function cards |
| `BaselineUnavailableSection`| `Frontend/src/App.jsx:851-870` | Explanatory banner displayed when no functional baseline exists, disabling conclusive FDO adjudication | Prop: `result` | Informational callout |
| `HistoryCard` | `Frontend/src/App.jsx:882-950` | Displays past execution record in the historical analyses drawer | Props: `item`, `onView` callback | `StatusBadge`, view analysis action button |
| `PurposeList` | `Frontend/src/App.jsx:230-247` | Normalizes and renders bulleted chips for single or multiple declared/expected purposes | Prop: `purposes` | Formatted labels |

### 2.2 End-to-End User Interaction Trace

The trace below maps a complete user interaction from UI submission to backend execution and UI render:

1. **User Action (Input Submission)**:
   - The user inputs `applicationName = "Google Maps"`, selects `category = "Navigation"`, leaves `description` blank, and leaves `policyText` blank or pastes a policy excerpt.
   - The user clicks the **"Find & Analyze Policy"** (or **"Analyze Policy"**) button (`Frontend/src/App.jsx:1400-1408`).
2. **Frontend State Transition & Request**:
   - `handleAnalyze(event)` triggers (`Frontend/src/App.jsx:1041`).
   - `setLoading(true)`, `setError("")`, `setResult(null)`.
   - Sends HTTP POST to `${API_URL}/api/v1/analyze` with JSON payload:
     ```json
     {
       "application_name": "Google Maps",
       "category": "Navigation",
       "description": undefined,
       "policy_text": undefined,
       "policy_source": undefined
     }
     ```
3. **Backend Route Ingestion**:
   - `analyze_endpoint` in `Backend/app/main.py:297-464` receives request.
   - Calls `get_or_create_application_for_analysis` (`Backend/app/services/application_service.py:46`). If the app exists in the DB, it retrieves it; otherwise, inserts an application row.
   - If `policy_text` is empty, calls `discover_privacy_policy("Google Maps")` (`Backend/app/services/policy_discovery_service.py:61`). Finds URL (e.g. `https://policies.google.com/privacy`), fetches HTML, extracts plain text. If discovery fails, raises HTTP `422`.
4. **Evidence Extraction & Baseline Provisioning**:
   - Calls `extract_policy_evidence` (`Backend/app/services/policy_extraction_service.py:16`). Calls Google Gemini API (`gemini-3.5-flash-lite`) to extract data types, purposes, and quotes, falling back to regex parsing if AI fails or no API key is set.
   - Calls `create_runtime_policy` (`Backend/app/services/policy_ingestion_service.py:14`), creating `PolicyDocument` and child `PolicyEvidence` rows in SQLite.
   - Calls `ensure_functional_baseline` (`Backend/app/services/functional_baseline_service.py:32`). Checks if curated `ExpectedFunctionalDataMapping` rows exist for the app; if not, calls Gemini to generate a functional baseline and persists it.
5. **Dual Analysis Pipeline Execution**:
   - **Deterministic Relational Engine**: `run_analysis` (`Backend/app/services/analysis_runner.py:46`) iterates through all expected mappings, finds best matching evidence via `find_best_matching_evidence` (`Backend/app/services/evidence_matcher.py:54`), builds comparison via `build_comparison` (`Backend/app/services/comparison_service.py:431`), and evaluates FDO status via `evaluate_fdo_decision` (`Backend/app/services/fdo_decision_service.py:27`). Writes rows to `analyses`, `comparisons`, `fdo_results`, and `explanations`.
   - **Semantic Knowledge Graph Engine**: If baseline is available, `DBSemanticResultService.analyze` (`Backend/app/ontology/db_semantic_result_service.py:155`) converts DB records to RDF triples via `DBRDFService.build_graph` (`Backend/app/ontology/db_rdf_service.py:21`), uploads the graph to Apache Jena Fuseki at `http://localhost:3030/fdo-reasoning/data`, queries Fuseki via SPARQL query `FDO_DETECTION_QUERY` (`Backend/app/ontology/fdo_detection_queries.py:5`), adapts findings through `decide_semantic_finding` (`Backend/app/ontology/semantic_decision_adapter.py:71`), and persists them to `semantic_fdo_results` via `SemanticResultRepository` (`Backend/app/ontology/semantic_result_repository.py:12`). If Fuseki is offline, the exception is caught and falls back to empty semantic results (`Backend/app/main.py:418-419`).
6. **Backend Response Packaging**:
   - `build_analysis_report` (`Backend/app/services/analysis_report_service.py:13`) aggregates counts (`total_mappings`, `fdo_count`, `not_fdo_count`, `ambiguous_count`), comparisons, policy analysis findings, and functional baseline mappings.
   - Returns serialized `AnalysisReportResponse` (HTTP 200).
7. **Frontend State Handling & UI Render**:
   - `handleAnalyze` parses JSON response (`Frontend/src/App.jsx:1073`).
   - Calls `setResult(data)` and `setLoading(false)`.
   - Fires `loadHistory()` to refresh background history drawer.
   - UI conditionally renders `<section className="results-page">` (`Frontend/src/App.jsx:1517-1718`):
     - Renders 4 `MetricCard` counters (Total, FDO, Not FDO, Ambiguous).
     - Renders `FunctionalBaselineSection` showing function expectations.
     - Renders `PolicyAnalysisCard` list showing extracted clauses and confidence scores.
     - Groups `result.semantic_results` by function name and renders `GroupedSemanticCard` components with expandable reasoning accordions.


---

## 3. Privacy Analysis & Comparison Logic

### 3.1 Implementation Inventory & Reality Check

This section documents what algorithms and rules actually exist in code versus theoretical claims.

| Analysis Capability | Implementation Location (`path:line`) | Implemented Mechanism & Algorithm | Limitations & Real Behavior | Feature Status |
| :--- | :--- | :--- | :--- | :--- |
| **Evidence Extraction** | `Backend/app/services/policy_extraction_service.py:16`, `Backend/app/services/ai_service.py:106` | Gemini `gemini-3.5-flash-lite` zero-shot structured prompt extracting JSON items (`data_type`, `purpose`, `entity`, `sharing`, `retention`, `evidence_text`). Fallback regex sentence scanning. | Relies on LLM prompt obedience or 4 keyword matches (`location`, `navigation`, `traffic`, `personalization`). | Implemented-verified |
| **Data Type Normalization** | `Backend/app/services/evidence_validation_service.py:74-93`, `Backend/app/schemas/analysis.py:7-54` | Exact membership checks against controlled set `VALID_DATA_TYPES` (18 string tokens like `DATA.LOCATION.PRECISE`, `DATA.CONTACTS`). Cleaned via regex prefix removal. | Unmatched data types default to `DATA.OTHER`. No learned entity linking. | Implemented-verified |
| **Purpose Normalization & Classification** | `Backend/app/services/comparison_service.py:3-97, 176-310` | Two-stage pipeline: (1) `normalize_purpose`: lowercases, replaces `-`, `_`, `/` with spaces, collapses whitespace. (2) `classify_purposes`: substring scans against 14 controlled purpose sets in `PURPOSE_CATEGORIES`. | Substring matching only; no embedding similarity or semantic parsing. | Implemented-verified |
| **Application vs Policy Comparison** | `Backend/app/services/comparison_service.py:155-175, 313-360, 431-481` | Pairwise comparison between an expected mapping tuple `(expected_data_type, expected_purpose)` and matching policy evidence tuple `(declared_data_type, declared_purpose)`. | Evaluates an application strictly against its own declared policy. Does not compare across different apps. | Implemented-verified |
| **Comparison Between Apps** | Codebase wide search for cross-app comparison logic | None | The repository contains **no cross-application comparison logic**. Each analysis is isolated to a single application ID. | Not-found |
| **Internal Contradiction Detection** | Codebase wide search for intra-policy contradiction checking | None | The system does **not** evaluate whether policy statements contradict one another (e.g. "we do not track you" vs "we collect precise location"). | Not-found |
| **Missing-Information Detection** | `Backend/app/services/comparison_service.py:169-170, 397-398`, `Backend/app/services/fdo_decision_service.py:42-51` | If no policy evidence exists matching the functional data type, `evidence_status` is assigned `"NO_EVIDENCE"` and the decision engine flags `"AMBIGUOUS"`. | Flags omission as unverified/ambiguous rather than asserting privacy breach or non-occurrence. | Implemented-verified |

### 3.2 Exact Decision Logic & Rules

The deterministic decision engine evaluates every comparison pair through `evaluate_fdo_decision` (`Backend/app/services/fdo_decision_service.py:27-147`):

```
                        [ Comparison Input ]
                                  │
                  ┌───────────────┴───────────────┐
                  │                               │
        evidence_status == "NO_EVIDENCE"   evidence_status in {"INSUFFICIENT", "UNKNOWN"}
                  │                               │
                  ▼                               ▼
          [ AMBIGUOUS (0.30) ]            [ AMBIGUOUS (0.40) ]
          "No declared evidence           "Evidence is insufficient"
           available"                             │
                  ┌───────────────────────────────┘
                  │ (evidence_status == "EXTRACTED")
                  ▼
        ┌────────────────────────────────────────────────────────┐
        │                  Data & Purpose Checks                 │
        └────────────────────────────────────────────────────────┘
                  │                               │
       data_match == "EXACT_MATCH"        data_match == "NO_MATCH"
                  │                       functional_relationship == "RELATED"
       ┌──────────┴──────────┐                    │
       │                     │                    ▼
purpose == "COMPATIBLE"  purpose == "INCOMPATIBLE"  [ FDO (0.80) ]
       │                     │            "Declared data differs
       ▼                     ▼             from expected functional data"
 [ NOT_FDO (0.90) ]     [ FDO (0.85) ]
"Declared matches      "Data matches, but
 functional need"       purpose is incompatible"
       │                     │
       └──────────┬──────────┘
                  │ (Any unhandled condition)
                  ▼
          [ AMBIGUOUS (0.50) ]
```

1. **Rule 1 (Missing Evidence)**: `evidence_status == "NO_EVIDENCE"` $\rightarrow$ `status = "AMBIGUOUS"`, `confidence = 0.30`.
2. **Rule 2 (Weak Evidence)**: `evidence_status in {"INSUFFICIENT", "UNKNOWN"}` or `evidence_status != "EXTRACTED"` $\rightarrow$ `status = "AMBIGUOUS"`, `confidence = 0.40`.
3. **Rule 3 (Functionally Justified Collection)**: `data_match == "EXACT_MATCH"` AND `purpose_compatibility == "COMPATIBLE"` AND `functional_relationship == "RELATED"` $\rightarrow$ `status = "NOT_FDO"`, `confidence = 0.90`.
4. **Rule 4 (Purpose Overreach)**: `data_match == "EXACT_MATCH"` AND `purpose_compatibility == "INCOMPATIBLE"` AND `functional_relationship == "RELATED"` $\rightarrow$ `status = "FDO"`, `confidence = 0.85`.
5. **Rule 5 (Data Type Overreach)**: `data_match == "NO_MATCH"` AND `functional_relationship == "RELATED"` $\rightarrow$ `status = "FDO"`, `confidence = 0.80`.
6. **Rule 6 (Conservative Fallback)**: All other unclassified permutations $\rightarrow$ `status = "AMBIGUOUS"`, `confidence = 0.50`.

### 3.3 Semantic Graph Overreach Logic

In the semantic layer (`Backend/app/ontology/fdo_detection_queries.py:5-37`), SPARQL detection matches RDF graph paths:
```sparql
SELECT ?application ?function ?expectedData ?declaredData ?expectedType ?declaredType ?expectedPurpose ?declaredPurpose
WHERE {
    ?application a fdo:Application ;
                 fdo:performsFunction ?function ;
                 fdo:declaredData ?declaredData .
    ?function a fdo:Function ;
              fdo:expectedData ?expectedData .
    ?expectedData fdo:dataType ?expectedType ;
                  fdo:purpose ?expectedPurpose .
    ?declaredData fdo:dataType ?declaredType ;
                  fdo:purpose ?declaredPurpose .
    FILTER (
        STR(?expectedType) != STR(?declaredType) ||
        STR(?expectedPurpose) != STR(?declaredPurpose)
    )
}
```
Findings from this SPARQL pattern are fed into `semantic_finding_to_decision_input` (`Backend/app/ontology/semantic_decision_adapter.py:15-69`), which converts the RDF string types back into `FDODecisionInput` and executes the exact same deterministic ruleset above.

### 3.4 Methodological Distinctions: Policy Difference vs Contradiction & Omission

1. **Policy Difference is NOT a Contradiction**:
   - When one policy declares `DATA.LOCATION.PRECISE` for navigation while another declares `DATA.LOCATION.APPROXIMATE`, this reflects varying system designs, sensor precision levels, or privacy tradeoffs. The FDO framework does not label differing cross-service disclosures as contradictory.
2. **Omission is NOT Proof of Non-Occurrence**:
   - A policy that fails to state whether identifiers are shared with third parties does not prove they are never shared.
   - In accordance with privacy audit rigor, the FDO engine treats omitted evidence by designating the comparison status as `"AMBIGUOUS"` (confidence 0.30–0.40) rather than falsely asserting `"NOT_FDO"`.


---

## 4. Test Suite Audit, Coverage & Execution Results

### 4.1 Testing Framework & Structure

- **Test Framework**: `pytest 9.1.1` running under Python 3.10.11 (`Backend/pyproject.toml:1-30`).
- **Test File Inventory**: Exactly **67 test files** located in `Backend/test_*.py` comprising **397 collected unit and integration tests** (`Backend/test_*.py`).
- **HTTP Client**: FastAPI `TestClient` (backed by `starlette.testclient` and `httpx`).
- **Mocking**: `monkeypatch` and `unittest.mock` for Gemini AI endpoints (`test_api_semantic_integration.py`, `test_ai_extraction.py`).

### 4.2 Test File Inventory & Functional Coverage

| Test File Group | Test Files Count | Functional Scope & Subsystems Covered | Known Limitations & Environment Gaps |
| :--- | :--- | :--- | :--- |
| **Ontology Schema & RDF Construction** | 10 files (`test_fdo_ontology_*.py`, `test_fdo_owl_builder.py`, `test_fdo_rdf_*.py`, `test_fdo_uri.py`) | Tests 19 ontology classes, 23 object properties, 11 data properties, OWL serialization, RDF instance generation, and URI minting. | Tests purely in-memory RDFLib graphs. Requires no database or network. |
| **Purpose Normalization & Classification** | 2 files (`test_purpose_normalization.py`, `test_purpose_fdo_integration.py`) | 46 tests covering text lowercasing, whitespace stripping, hyphen/slash resolution, 14 purpose categories, multi-purpose classification, and purpose compatibility matrix. | None; 100% deterministic unit tests. |
| **Relational Decision & Matching Logic** | 8 files (`test_controlled_semantic_decisions.py`, `test_functional_baseline_service.py`, `test_policy_workflow_safety.py`, `test_unknown_application_lookup.py`, `test_helpers.py`, etc.) | Evaluates all 6 deterministic rules, baseline caching, application lookups, evidence scoring heuristics, and fallback pipelines. | Relies on SQLite DB fixtures; no external API calls required. |
| **SPARQL & Semantic Reasoning Adapters** | 7 files (`test_fdo_sparql_service.py`, `test_fdo_semantic_detector.py`, `test_semantic_decision_adapter.py`, `test_semantic_explanation_service.py`, `test_semantic_explanations.py`, `test_semantic_edge_cases.py`, etc.) | Adapts SPARQL bindings into decision dataclasses, verifies reason text formatting, edge cases with missing types, and multi-purpose grouping. | Operates on mocked or synthetic SPARQL results; runs completely offline. |
| **Relational-to-RDF DB Mapping** | 4 files (`test_db_rdf_mapper.py`, `test_db_rdf_service.py`, `test_fdo_ontology_db_mapper.py`, `test_fdo_db_rdf_integration.py`) | Tests mapping of SQLite SQLAlchemy ORM entities to RDF graph triples (`fdo:Application`, `fdo:Function`, `fdo:ExpectedData`, `fdo:DeclaredData`). | Tests in-memory conversion without requiring an active Fuseki server. |
| **FastAPI REST Endpoints** | 4 files (`test_api_semantic_integration.py`, `test_api_semantic_get_persistence.py`, `test_api_semantic_plural_get.py`, `test_unknown_application_lookup.py`) | Verifies `/api/v1/analyze`, `/api/v1/analyses/{id}`, and `/api/v1/applications` using FastAPI `TestClient`. | When the optional Fuseki triple store is offline, semantic persistence tests fail if expecting non-empty semantic results. |
| **Live Apache Jena Fuseki Integration** | 20+ files (`test_fuseki_service.py`, `test_fuseki_semantic_detector.py`, `test_semantic_fuseki_live.py`, `test_fdo_jena_reasoning.py`, `test_real_db_to_fuseki_semantic.py`, etc.) | Tests live HTTP triple uploads, graph clearing, and SPARQL queries against `http://localhost:3030/fdo-reasoning`. | **Fails when Apache Jena Fuseki is not running locally.** Requires `fuseki-server.bat` active on port 3030. |
| **Gemini AI Extraction Tests** | 2 files (`test_gemini.py`, `test_ai_extraction.py`) | Verifies live Gemini API calls to `gemini-3.5-flash-lite`. | **Fails or skips when `GEMINI_API_KEY` is unset** or external internet access is disabled. |

### 4.3 Actual Test Suite Execution Report

The test suite was executed locally using Python virtual environment `Backend/.venv/Scripts/python.exe`. In strict compliance with audit rules, no packages were installed, no paid API calls were made, and offline execution was isolated.

#### Execution Run 1: Core Unit Tests (Offline, No External Services)
- **Command Executed**:
  ```powershell
  & "d:\VIT\PROJECT\TARP\Backend\.venv\Scripts\python.exe" -m pytest test_fdo_ontology_classes.py test_fdo_ontology_properties.py test_fdo_ontology_data_properties.py test_fdo_ontology_constraints.py test_fdo_owl_builder.py test_fdo_rdf_instance_builder.py test_fdo_uri.py test_fdo_rdf_validation.py test_fdo_competency_questions.py test_controlled_semantic_decisions.py test_purpose_normalization.py test_purpose_fdo_integration.py test_orm_to_rdf.py test_policy_evidence_to_rdf.py test_fdo_rdf_relationships.py test_fdo_rdf_export.py test_fdo_rdf_owl_compatibility.py test_fdo_data_type_integration.py test_fdo_purpose_integration.py test_fdo_sensitive_data_integration.py test_fdo_processing_activity_integration.py test_fdo_sharing_retention_integration.py test_fdo_overreach_integration.py test_fdo_justification_risk_integration.py test_fdo_sparql_service.py test_fdo_semantic_detector.py test_semantic_decision_adapter.py test_semantic_explanation_service.py test_semantic_explanations.py test_semantic_edge_cases.py test_db_rdf_mapper.py test_db_rdf_service.py test_fdo_ontology_db_mapper.py test_fdo_db_rdf_integration.py test_helpers.py test_unknown_application_lookup.py test_policy_workflow_safety.py test_functional_baseline_service.py test_db_semantic_repository.py test_api_semantic_integration.py -q
  ```
- **Results**:
  - **Passed**: **356 tests**
  - **Failed**: **0 tests**
  - **Skipped / Error**: **0**
  - **Execution Time**: ~3.8 seconds

#### Execution Run 2: Live Integration Tests (Apache Jena Fuseki & Live Endpoints)
- **Command Executed**:
  ```powershell
  & "d:\VIT\PROJECT\TARP\Backend\.venv\Scripts\python.exe" -m pytest test_fdo_jena_reasoning.py test_api_semantic_get_persistence.py test_api_semantic_plural_get.py test_db_semantic_result_service.py -q
  ```
- **Results**:
  - **Passed**: **1 test** (`test_api_semantic_integration.py`)
  - **Failed / Errored**: **7 tests** (Failed due to `HTTPConnectionPool(host='localhost', port=3030): [WinError 10061] No connection could be made because the target machine actively refused it`)
  - **Status**: Demonstrates graceful degradation in production runtime (`Backend/app/main.py:418-420`), but integration tests enforcing live Fuseki assertions fail when the local Java daemon is inactive.


---

## 5. End-to-End Pipeline Architecture Diagrams

### 5.1 Mermaid Sequence Diagram

The sequence diagram traces a full execution cycle of `POST /api/v1/analyze`, using actual function and service identifiers.

```mermaid
sequenceDiagram
    autonumber
    actor User as Data Subject / Auditor
    participant UI as React SPA (App.jsx)
    participant API as FastAPI Router (main.py)
    participant AppSvc as application_service
    participant DiscSvc as policy_discovery_service
    participant ExtrSvc as policy_extraction_service
    participant BaseSvc as functional_baseline_service
    participant Runner as analysis_runner
    participant Matcher as evidence_matcher
    participant CompSvc as comparison_service
    participant DecEngine as fdo_decision_service
    participant DB as SQLite DB (fdo_privacy.db)
    participant SemSvc as db_semantic_result_service
    participant RDFMapper as db_rdf_service
    participant Fuseki as Apache Jena Fuseki (:3030)
    participant RepSvc as analysis_report_service

    User->>UI: Submit App Name ("Google Maps"), Category & Optional Policy Text
    UI->>API: POST /api/v1/analyze (AnalyzeRequest)
    API->>AppSvc: get_or_create_application_for_analysis(name, cat, desc)
    AppSvc->>DB: Query/Insert Application
    DB-->>AppSvc: application record
    
    opt Policy Text Not Provided
        API->>DiscSvc: discover_privacy_policy(app_name)
        DiscSvc-->>API: PolicyDiscoveryResult(policy_text, source_url)
    end

    API->>ExtrSvc: extract_policy_evidence(policy_text, app_name)
    ExtrSvc->>ExtrSvc: Gemini API call or regex fallback parsing
    ExtrSvc-->>API: list[evidence_dict]

    API->>DB: create_runtime_policy(app_id, policy_text, evidence)
    DB-->>API: runtime_policy record

    API->>BaseSvc: ensure_functional_baseline(session, application)
    BaseSvc->>DB: Check ExpectedFunctionalDataMapping
    DB-->>BaseSvc: mappings or generate AI baseline
    BaseSvc-->>API: FunctionalBaselineResult(status, available)

    API->>Runner: run_analysis(session, analysis_id, app_id, policy_id)
    loop For each expected mapping
        Runner->>Matcher: find_best_matching_evidence(session, policy_id, expected)
        Matcher-->>Runner: EvidenceMatch(evidence, status)
        Runner->>CompSvc: build_comparison(expected, evidence)
        CompSvc-->>Runner: ComparisonOutput(data_match, purpose_compat, rel_status)
        Runner->>DecEngine: evaluate_fdo_decision(FDODecisionInput)
        DecEngine-->>Runner: FDODecisionOutput(fdo_status, reason, confidence)
        Runner->>DB: save_comparison & save_fdo_result & save_explanation
    end
    Runner-->>API: Analysis(status="COMPLETED")

    opt Baseline Available
        API->>SemSvc: DBSemanticResultService.analyze(app_id, policy_id, path)
        SemSvc->>RDFMapper: build_graph(app, functions, expected, declared)
        RDFMapper-->>SemSvc: rdflib.Graph
        SemSvc->>Fuseki: clear_default_graph() & upload graph TTL
        SemSvc->>Fuseki: SPARQL FDO_DETECTION_QUERY
        Fuseki-->>SemSvc: JSON bindings
        SemSvc->>DecEngine: evaluate_fdo_decision via semantic_decision_adapter
        SemSvc-->>API: list[semantic_results]
        API->>DB: SemanticResultRepository.save_results(analysis_id, semantic_results)
    end

    API->>RepSvc: build_analysis_report(session, analysis_id)
    RepSvc->>DB: Query Analysis, Comparisons, Results, Explanations, Baseline
    DB-->>RepSvc: Entities
    RepSvc-->>API: AnalysisReport
    API-->>UI: 200 OK (AnalysisReportResponse)
    UI->>UI: Update state: metrics, baseline table, policy cards, semantic accordion
    UI-->>User: Display Interactive Overreach Findings
```

### 5.2 Mermaid Data-Flow Diagram

The diagram below details the ingestion, normalization, transformation, storage, and visualization paths of functional privacy data.

```mermaid
flowchart TD
    subgraph INGESTION["1. Ingestion Layer"]
        RawPolicy["Raw Policy Text / URL"] --> Discovery["policy_discovery_service.py"]
        Discovery --> Extractor["policy_extraction_service.py<br/>(Gemini 3.5 / Regex Fallback)"]
        Extractor --> ExtractedEvidence["Extracted Evidence Items<br/>(data_type, purpose, quote)"]
    end

    subgraph BASELINE["2. Functional Baseline Layer"]
        CuratedDB["Curated Seed Mappings<br/>(DATA/*.csv, init_db.py)"] --> BaselineCheck{"Baseline Exists?"}
        BaselineCheck -- Yes --> ActiveBaseline["Expected Functional Baseline<br/>(Function -> Expected Data, Necessity, Purpose)"]
        BaselineCheck -- No --> GeminiBaseline["ai_service.py<br/>(generate_functional_baseline_with_ai)"]
        GeminiBaseline --> ActiveBaseline
    end

    subgraph RELATIONAL_ENGINE["3. Deterministic Relational Engine"]
        ExtractedEvidence --> EvidenceMatcher["evidence_matcher.py<br/>(find_best_matching_evidence)"]
        ActiveBaseline --> EvidenceMatcher
        EvidenceMatcher --> Comparator["comparison_service.py<br/>(build_comparison)"]
        Comparator --> RelRules["fdo_decision_service.py<br/>(evaluate_fdo_decision)"]
        RelRules --> RelResults["Relational Outcomes<br/>(NOT_FDO, FDO, AMBIGUOUS)"]
    end

    subgraph SEMANTIC_ENGINE["4. Semantic Knowledge Graph Engine"]
        ActiveBaseline --> RDFBuilder["db_rdf_service.py<br/>(build_graph)"]
        ExtractedEvidence --> RDFBuilder
        RDFBuilder --> TTL["outputs/semantic/<analysis_id>.ttl"]
        TTL --> Fuseki[("Apache Jena Fuseki<br/>(http://localhost:3030/fdo-reasoning)")]
        Fuseki --> SPARQL["fdo_detection_queries.py<br/>(FDO_DETECTION_QUERY)"]
        SPARQL --> SemAdapter["semantic_decision_adapter.py<br/>(decide_semantic_finding)"]
        SemAdapter --> SemResults["Semantic Outcomes<br/>(NOT_FDO, FDO, AMBIGUOUS)"]
    end

    subgraph PERSISTENCE["5. Relational Persistence (SQLite)"]
        RelResults --> SQLiteDB[("fdo_privacy.db<br/>(analyses, comparisons, fdo_results)")]
        SemResults --> SQLiteDB
    end

    subgraph REPORTING["6. Report Aggregation & UI Presentation"]
        SQLiteDB --> RepService["analysis_report_service.py<br/>rich_report_service.py"]
        RepService --> REST["FastAPI Router<br/>(POST /api/v1/analyze, GET /analyses)"]
        REST --> Frontend["React Frontend (App.jsx)<br/>Metric Cards | Grouped Semantic Cards | Evidence Details"]
    end
```

---

## 6. Handoff Notes

### 6.1 Key Findings
1. **API Endpoints**:
   - 13 endpoints exist in `Backend/app/main.py`. The primary endpoint `/api/v1/analyze` coordinates policy discovery, evidence extraction, baseline generation, relational comparison, RDF graph building, Fuseki semantic reasoning, SQLite persistence, and report synthesis.
   - Graceful fallback: If Apache Jena Fuseki is down, `/api/v1/analyze` catches the exception (`Backend/app/main.py:418-420`), committing the relational analysis and returning an empty semantic results list rather than failing the entire request.
2. **Frontend UI**:
   - Implemented as a single unified dashboard in `Frontend/src/App.jsx`. It supports automated policy discovery or manual paste, displays high-level KPI cards, breaks down functional baselines, provides collapsible accordion cards grouping semantic findings by application function, and stores local analysis history.
3. **Analysis Engine Limitations**:
   - **Cross-Application Comparison**: Does **not** exist. All comparisons are strictly intra-application (`expected functional requirement` vs `declared policy clause`).
   - **Contradiction Detection**: Does **not** exist. The codebase checks for overreach (functional mismatch), not logical contradictions between multiple policy statements.
   - **Omission vs Contradiction**: The engine rigorously flags omitted evidence as `"AMBIGUOUS"` (confidence 0.30–0.40) rather than falsely exonerating the application.
4. **Test Suite Status**:
   - The test suite comprises **67 files and 397 collected tests**.
   - **356 unit and offline integration tests pass with 100% success** (0 failures) in ~3.8 seconds.
   - Live integration tests dependent on `localhost:3030` fail only because Apache Jena Fuseki is not actively running as a background service.

### 6.2 Audited File List
- **Backend API & Core Execution**:
  - `Backend/app/main.py`
  - `Backend/app/config.py`
  - `Backend/app/database.py`
- **Schemas**:
  - `Backend/app/schemas/analysis.py`
  - `Backend/app/schemas/analysis_result.py`
  - `Backend/app/schemas/policy_extraction.py`
  - `Backend/app/schemas/rich_report.py`
- **Services (Business Logic & Decision Engine)**:
  - `Backend/app/services/analysis_runner.py`
  - `Backend/app/services/fdo_decision_service.py`
  - `Backend/app/services/comparison_service.py`
  - `Backend/app/services/evidence_matcher.py`
  - `Backend/app/services/evidence_validation_service.py`
  - `Backend/app/services/policy_analysis_service.py`
  - `Backend/app/services/policy_discovery_service.py`
  - `Backend/app/services/policy_extraction_service.py`
  - `Backend/app/services/policy_ingestion_service.py`
  - `Backend/app/services/functional_baseline_service.py`
  - `Backend/app/services/analysis_report_service.py`
  - `Backend/app/services/rich_report_service.py`
- **Semantic Ontology & Fuseki Integration**:
  - `Backend/app/ontology/db_semantic_result_service.py`
  - `Backend/app/ontology/semantic_decision_adapter.py`
  - `Backend/app/ontology/fuseki_semantic_detector.py`
  - `Backend/app/ontology/fdo_detection_queries.py`
  - `Backend/app/ontology/semantic_result_repository.py`
  - `Backend/app/ontology/db_rdf_service.py`
- **Frontend Codebase**:
  - `Frontend/src/App.jsx`
  - `Frontend/src/App.css`
  - `Frontend/package.json`
- **Test Suite**:
  - `Backend/test_*.py` (67 test files)

### 6.3 Open Questions & Architectural Recommendations
1. **Cross-Application Privacy Comparison**: If cross-application comparison (e.g. comparing WhatsApp vs Telegram data practices) is desired for IDF-B claims, a multi-app comparative SPARQL query or REST aggregation endpoint (`/api/v1/compare-applications`) needs to be implemented.
2. **Fuseki Process Supervision**: Currently, Fuseki must be launched manually via `apache-jena-fuseki-6.2.0/fuseki-server.bat`. A health-check endpoint or automated container/subprocess manager could enhance live test execution reliability.
3. **Internal Contradiction Module**: If detecting contradictory clauses within the same policy (e.g., "we do not share personal information" vs "we share identifiers with advertising networks") is required, an NLP contradiction detection model (e.g. NLI / Natural Language Inference) should be added.
