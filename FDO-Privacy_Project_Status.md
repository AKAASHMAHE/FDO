# FDO-Privacy Project — Complete Current Status

**Audit Date:** 2026-09-08  
**Project Name:** FDO-Privacy (Functional Data Ontology based Privacy Policy Analysis)  
**Project Root:** `D:\VIT\PROJECT\TARP`  
**Overall Project Status:** Stage 7 (Research & Benchmark Package) COMPLETE; Stage 8 (Software Implementation & AI Pipeline Integration) IN PROGRESS — Core Backend, Deterministic Decision Engine, and Live AI Evidence Extraction Pipeline OPERATIONAL and Experimentally Validated.  
**Current Implementation Stage:** Stage 8.5+ (Live End-to-End AI-to-Database Analysis Pipeline Operational)

---

# Executive Summary

The **FDO-Privacy** project addresses a fundamental limitation in existing automated privacy-policy analysis research: while prior work focuses on policy readability, disclosure completeness, internal contradictions, or runtime network traffic consistency, it fails to evaluate whether declared data collection is **functionally necessary** for the application's stated features and capabilities. 

FDO-Privacy introduces a formal framework to detect **Functional Data Overreach (FDO)** — data collection that exceeds what is required to deliver an application's functions and is not substantively justified in its privacy policy.

The project is structured into two main layers:
1. **Research & Benchmark Layer (Stages 1–7):** Established the research design, Functional Data Ontology, 30-application pilot, 27-application analytical cohort, 99 expected mappings, 93 evidence-backed mappings, manual FDO adjudication, benchmark dataset freeze (60 NOT_FDO, 33 AMBIGUOUS, 0 FDO established in benchmark), visualization, and final research report package.
2. **Software & Productization Layer (Stage 8):** Converts the research methodology into a reusable, auditable software system. It features a FastAPI REST backend, SQLAlchemy/SQLite database schema (10 tables), a deterministic 5-rule FDO decision engine, and live AI-powered evidence extraction using Google Gemini (`gemini-3.5-flash-lite`).

### Core Architectural Principle
> **AI Extracts Evidence. Deterministic Rules Adjudicate FDO.**

Gemini AI is strictly scoped to extracting structured policy evidence and supporting quotes from raw privacy policy text. Gemini is **never** permitted to independently assign final FDO, NOT_FDO, or AMBIGUOUS status. The final determination is executed strictly by deterministic, auditable python decision rules.

---

# 1. Project Background & Overview

## 1.1 Problem Statement
Privacy policies are dense legal documents that users rarely read. Traditional NLP summarization tools condense text but inherit the policy's own framing (e.g., summarizing "we collect precise location to personalize ads" accurately, without questioning why a flashlight app collects location). Existing mobile security tools (e.g., WHYPER, AutoCog) check OS permission fidelity against short app-store descriptions, but do not analyze fine-grained personal data categories, third-party sharing, or explicit policy justification text.

FDO-Privacy fills this gap by evaluating declared data practices against an explicit, function-specific **Expected Data Profile**.

## 1.2 Conceptual Chain
```text
Application 
   ↓
Category 
   ↓
Function (Main unit of necessity analysis) 
   ↓
Feature 
   ↓
Data Type 
   ↓
Necessity Level 
   ↓
Expected Purpose 
   ↓
Policy Evidence (Extracted by AI) 
   ↓
Functional Comparison 
   ↓
Deterministic FDO Decision 
   ↓
Explainable Result
```

## 1.3 Definition of Terms
- **Functional Necessity:** Whether a specific data item is required for a named application function to operate.
- **Expected Data Mapping:** A baseline rule establishing what data types and necessity levels are expected for a specific function.
- **Functional Data Overreach (FDO):** A condition where declared/collected data exceeds expected functional need and lacks a compatible, substantive functional justification.
- **NOT_FDO:** A condition where declared data matches expected data and serves a compatible functional purpose.
- **AMBIGUOUS:** A condition where policy evidence is missing, incomplete, vague, or insufficient to reach a conclusive binary judgment.

---

# 2. Research & Methodology Audit (Stages 1–8)

Based on project documentation (`FDO-Privacy_Stage1_Research_Foundation (1).md`, `FDO-Privacy_Stage2_Functional_Data_Ontology.md`, `FDO-Privacy_Project_File_Inventory.md`, `before_ai_audit.md`, and Excel datasets), the project methodology follows eight distinct stages:

### Stage 1 — Research Scope & Design
- Defined problem statement, research questions (RQs 1–5), literature review across 10 streams (including PoliGraph, PolicyLint, PoliCheck, WHYPER, AutoCog), and contribution boundaries.
- Formulated the core thesis: AI can extract evidence and compare expected vs. declared data, but necessity reasoning must be structured and explainable per item rather than an opaque aggregate score.

### Stage 2 — Expected-Data Baseline & Ontology
- Designed the **Functional Data Ontology**:
  - `Application → Category → Function → Feature → Data Type → Necessity → Purpose → Rationale`
- Established **Function** as the primary unit of necessity analysis.
- Defined necessity levels (e.g., Level 1 Required, Level 2 Conditional/Optional, Level 3 Unexpected).
- Conducted Stage 2B pilot annotations across 30 original applications in 4 annotation batches.

### Stage 3 — Privacy Policy Evidence Annotation & QA
- Extracted and annotated privacy-policy evidence for the pilot applications.
- Frozen the analytical cohort at **27 analytical applications** (excluding 3 policy exceptions: **Instagram**, **PUBG MOBILE**, and **WeChat** due to unparseable, regional, or unresolvable policy structures).
- Output artifacts: `FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx` and `COMPLETE.xlsx` containing 99 expected data mappings and 93 evidence-backed mappings.

### Stage 4 — FDO Adjudication
Applied a 5-tier manual adjudication pipeline to the research dataset:
- **4A Necessity Analysis:** Evaluated alignment between expected necessity and declared data.
- **4B Purpose Compatibility:** Evaluated whether declared purposes matched expected functional purposes.
- **4C Candidate Screening:** Filtered non-overreach cases from true adjudication queues.
- **4D Detailed Adjudication:** Applied multi-test FDO rules.
- **4E Ambiguous Case Resolution:** Handled vague or unresolvable policy disclosures.

### Stage 5 — Research Benchmark & Evaluation Statistics
Established the manually adjudicated research benchmark.

> [!IMPORTANT]
> **CRITICAL DISTINCTION:** The table below documents the **MANUALLY ADJUDICATED RESEARCH BENCHMARK**. It represents baseline research findings and is preserved separately from dynamic runtime software prototype results.

| Metric | Research Benchmark Value |
|---|---:|
| Original Pilot Applications | 30 |
| Analytical Cohort Applications | 27 |
| Policy Exceptions (Excluded) | 3 |
| Total Expected Mappings | 99 |
| Evidence-Backed Mappings | 93 |
| Mappings Lacking Policy Evidence | 6 |
| **NOT_FDO Mappings** | **60 (64.5%)** |
| **AMBIGUOUS Mappings** | **33 (35.5%)** |
| **Established FDO Mappings** | **0 (0.0%)** |

*Note on 0 FDO in research benchmark:* In the static pilot dataset of 27 mainstream applications, declared collections were either functionally justified (`NOT_FDO`) or so vaguely described that they fell into `AMBIGUOUS`. No definitive, un-justified excess (`FDO`) survived manual adjudication in the frozen static cohort.

### Stage 6 — Visualizations & Findings
- Generated interactive charts, comparative distribution matrices, and summary workbooks (`FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx`).

### Stage 7 — Final Research Report Package
- Consolidated all empirical methodology, inter-annotator agreement metrics, threat validation, and findings into `FDO-Privacy_Stage7_Final_Research_Report_Package_v1.0.docx`.

### Stage 8 — Software Implementation & Productization
- Converts the static research artifacts into an automated, reusable backend system.
- Implements data models, REST endpoints, database persistence, evidence matching, deterministic FDO decision logic, rich report formatting, and live Gemini AI integration.

---

# 3. Complete Backend Code Audit

The backend is built with **Python 3.10+**, **FastAPI**, **SQLAlchemy ORM**, **Pydantic**, and **SQLite**.

```text
Backend/
├── .env                              # Environment configuration (Contains GEMINI_API_KEY)
├── .gitignore                        # Git exclusion rules
├── fdo_privacy.db                    # Active SQLite database file
├── requirements.txt                  # Python dependencies
├── test_ai_extraction.py             # Direct AI service test script
├── test_gemini.py                    # Direct Gemini API connectivity script
│
├── app/
│   ├── config.py                     # App settings via Pydantic BaseSettings
│   ├── database.py                   # SQLAlchemy engine and SessionLocal setup
│   ├── init_db.py                    # Database table creation utility
│   ├── main.py                       # FastAPI application routes & dependency injection
│   │
│   ├── models/                       # SQLAlchemy ORM Models
│   │   ├── __init__.py
│   │   ├── analysis.py               # Analysis execution table
│   │   ├── application.py            # Application entity table
│   │   ├── base.py                   # SQLAlchemy DeclarativeBase
│   │   ├── comparison.py             # Expected vs Declared comparison table
│   │   ├── expected_mapping.py       # Expected data requirements table
│   │   ├── explanation.py            # Decision explanations table
│   │   ├── fdo_result.py             # Deterministic FDO decision table
│   │   ├── function.py               # Application functions table
│   │   ├── normalized_evidence.py    # Normalized evidence representation table
│   │   ├── policy_document.py        # Privacy policy documents table
│   │   └── policy_evidence.py        # Extracted policy evidence table
│   │
│   ├── schemas/                      # Pydantic Schemas (DTOs)
│   │   ├── analysis.py               # Analysis request/response schemas
│   │   ├── analysis_result.py        # Itemized result schemas
│   │   ├── policy_extraction.py      # Policy extraction request/response schemas
│   │   └── rich_report.py            # Frontend-ready rich report schemas
│   │
│   └── services/                     # Business Logic Services
│       ├── __init__.py
│       ├── ai_service.py             # Google Gemini extraction service
│       ├── analysis_report_service.py # Standard analysis report builder
│       ├── analysis_result_service.py # Detailed itemized result query service
│       ├── analysis_runner.py        # Core pipeline orchestration service
│       ├── analysis_service.py       # Analysis model CRUD service
│       ├── application_service.py    # Application & readiness query service
│       ├── comparison_persistence_service.py # Comparison DB persistence service
│       ├── comparison_service.py     # Comparison evaluation logic
│       ├── evidence_matcher.py       # Evidence-to-Expected matching logic
│       ├── evidence_service.py       # Policy evidence query service
│       ├── expected_mapping_service.py # Expected mapping query service
│       ├── explanation_service.py    # Explanation persistence service
│       ├── fdo_decision_service.py   # Deterministic FDO rule engine
│       ├── function_service.py       # Function query service
│       ├── policy_extraction_service.py # Policy extraction wrapper service
│       ├── policy_ingestion_service.py # Runtime policy & evidence persistence
│       ├── policy_service.py         # Policy document query service
│       ├── result_service.py         # FDO result persistence service
│       └── rich_report_service.py    # Structured rich report generator
│
└── scripts/                          # Administrative & Testing Scripts
    ├── import_stage3.py              # Imports Excel Stage 3 dataset into SQLite
    ├── persist_fdo_test.py           # Verification script for database persistence
    ├── test_failure_path.py          # Failure/rollback verification script
    ├── validate_multi_app.py         # Multi-application batch validation script
    ├── verify_fdo_decision.py        # Direct FDO decision logic test script
    └── verify_services.py            # Service integration test script
```

## 3.1 ORM Models Audit (`app/models/`)

| Model Name | Table Name | Primary Key | Key Foreign Keys | Purpose & Responsibilities |
|---|---|---|---|---|
| `Application` | `applications` | `application_id` | None | Stores application metadata (e.g. `NAV-01`, `Google Maps`, category `Navigation`). |
| `Function` | `functions` | `function_record_id` | `application_id` | Stores app functions (`app_id:function_id`). Anchors functional features. |
| `ExpectedMapping` | `expected_mappings` | `expected_id` | `application_id`, `function_record_id` | Stores expected data requirements, necessity levels, and expected purposes. |
| `PolicyDocument` | `policy_documents` | `policy_id` | `application_id` | Stores raw privacy policy text and source metadata (supports static & runtime AI policies). |
| `PolicyEvidence` | `policy_evidence` | `evidence_id` | `policy_id` | Stores structured policy disclosures extracted by AI or static annotations. |
| `NormalizedEvidence` | `normalized_evidence` | `normalized_id` | `evidence_id` | Stores canonical normalized representations of raw evidence (Reserved for expansion). |
| `Analysis` | `analyses` | `analysis_id` | `application_id`, `policy_id` | Tracks analysis run status (`CREATED`, `RUNNING`, `COMPLETED`), counters (`total`, `fdo`, `not_fdo`, `ambiguous`), and timestamps. |
| `Comparison` | `comparisons` | `comparison_id` | `analysis_id`, `expected_id`, `evidence_id` | Stores evaluation metrics: `data_match`, `purpose_compatibility`, `functional_relationship`, `functional_justification`, `evidence_status`. |
| `FDOResult` | `fdo_results` | `result_id` | `comparison_id` | Stores final deterministic status (`FDO`, `NOT_FDO`, `AMBIGUOUS`), decision reason, and confidence score. |
| `Explanation` | `explanations` | `explanation_id` | `result_id` | Stores human-readable audit explanations, evidence summaries, and limitation notes. |

## 3.2 Key Services Audit (`app/services/`)

- **`ai_service.py`**: Interpaces with `google.genai` SDK using model `gemini-3.5-flash-lite`. Executes prompt-driven extraction of policy evidence into JSON. Includes `_normalize_data_type()` helper to map raw extracted types to canonical `DATA.*` ontology identifiers.
- **`analysis_runner.py`**: Pipeline orchestrator. Accepts `analysis_id`, `application_id`, and optional `policy_id`. Iterates through all `ExpectedMapping` records for the app, uses `evidence_matcher` to locate matching `PolicyEvidence`, evaluates `comparison_service`, executes `fdo_decision_service`, and persists results and explanations inside atomic DB transactions.
- **`fdo_decision_service.py`**: Implements 100% deterministic decision logic based on comparison metrics (`data_match`, `purpose_compatibility`, `functional_relationship`, `evidence_status`).
- **`policy_ingestion_service.py`**: Handles runtime policy creation (`create_runtime_policy`). Persists runtime `PolicyDocument` (ID prefix `AI-POL-`) and runtime `PolicyEvidence` (ID prefix `AI-`) generated from live AI extraction.
- **`evidence_matcher.py`**: Finds matching policy evidence for an expected mapping using canonical data type equality (`PolicyEvidence.data_type == expected_data_type`).
- **`rich_report_service.py`**: Transforms raw database analysis results into a structured, frontend-ready `RichAnalysisReportResponse` grouped by application function.

---

# 4. AI / Gemini Integration Audit

## 4.1 Integration Specifications
- **AI Provider:** Google Gemini API
- **Client SDK:** `google.genai` (Modern Python SDK)
- **Configured Model:** `gemini-3.5-flash-lite`
- **Key Location:** Loaded dynamically from `.env` via `GEMINI_API_KEY` (never committed or printed).
- **Execution Mechanism:** Synchronous call in `extract_policy_evidence_with_ai()` during policy processing.

## 4.2 Strict Architectural Boundary
```text
  [ Raw Policy Text ]
          │
          ▼
   ┌──────────────┐
   │  Gemini AI   │ ──► Responsible ONLY for Evidence Extraction & Quotes
   └──────────────┘
          │ (JSON Output)
          ▼
 [ Structured Evidence ]
          │
          ▼
 ┌──────────────────┐
 │ Deterministic    │ ──► Responsible for FDO Adjudication
 │ Python Rules     │     (FDO / NOT_FDO / AMBIGUOUS)
 └──────────────────┘
```

## 4.3 Prompt & Schema Safeguards
The prompt in `ai_service.py` enforces:
1. Extract ONLY information explicitly stated in text.
2. Do NOT infer unstated facts.
3. Do NOT make FDO decisions.
4. Output strict JSON matching `{"evidence": [...]}`.
5. `data_type` MUST use canonical ontology identifiers (`DATA.LOCATION.PRECISE`, `DATA.LOCATION.APPROXIMATE`, `DATA.CONTACTS`, `DATA.DEVICE`, `DATA.ACCOUNT`, `DATA.FINANCIAL`, `DATA.HEALTH`, `DATA.MEDIA`, `DATA.USAGE`, `DATA.OTHER`).
6. Exact quote requirement: `evidence_text` must contain the exact supporting sentence.

## 4.4 Canonical Data-Type Normalization
To prevent matching failures due to minor formatting discrepancies from the LLM, `ai_service.py` includes `_normalize_data_type()`:
- If Gemini outputs `LOCATION.PRECISE` (missing prefix), it is automatically mapped to `DATA.LOCATION.PRECISE`.
- If Gemini outputs an invalid string not in `ALLOWED_DATA_TYPES`, it is rejected (`None`), ensuring clean data flow to the matcher.

---

# 5. Current AI Data Flow & Pipeline Tracing

## 5.1 End-to-End Analysis Pipeline (`POST /api/v1/analyze`)

```text
POST /api/v1/analyze 
  (Body: application_name, category, policy_text, policy_source)
        │
        ▼
1. Application Lookup
   Lookup app in `applications` table by name & category (e.g., "Google Maps", "Navigation").
        │
        ▼
2. AI Evidence Extraction (Gemini)
   Call `extract_policy_evidence_with_ai(policy_text, application_name)`.
   Gemini parses text and returns structured JSON evidence array.
        │
        ▼
3. Runtime Policy & Evidence Persistence
   `create_runtime_policy()` creates:
   - `PolicyDocument` (ID: `AI-POL-ANALYSIS-NAV-01-{uuid}`)
   - `PolicyEvidence` records (IDs: `AI-{hex}`) linked to the runtime policy.
        │
        ▼
4. Deterministic Pipeline Execution (`run_analysis()`)
   - Fetches all `ExpectedMapping` records for `NAV-01` (EXP-015, EXP-016, EXP-017).
   - For each expected mapping, calls `evidence_matcher.find_matching_evidence()`.
   - Constructs `Comparison` (`data_match`, `purpose_compatibility`, etc.).
   - Calls `evaluate_fdo_decision()` to obtain `FDODecisionOutput`.
   - Saves `Comparison`, `FDOResult`, and `Explanation` records to DB.
        │
        ▼
5. Report Generation & DB Commit
   `build_analysis_report()` aggregates counts, commits transaction, and returns `AnalysisReportResponse`.
```

## 5.2 Endpoint Distinction

| Endpoint | HTTP Method | Input | Purpose & Execution Flow |
|---|---|---|---|
| `/api/v1/extract-policy` | `POST` | `policy_text`, `application_name` | **Extraction Only:** Runs Gemini AI extraction and returns structured evidence JSON. Does **not** write to DB; does **not** run FDO analysis. |
| `/api/v1/analyze` | `POST` | `application_name`, `category`, `policy_text` | **Full End-to-End Pipeline:** Runs AI extraction → creates runtime `PolicyDocument` & `PolicyEvidence` in DB → executes `run_analysis()` → returns complete `AnalysisReportResponse`. |

---

# 6. Complete API Audit

Base Path: `/api/v1`

| HTTP Method | Route | Purpose | Request Body / Query | Key Response Fields | DB Interaction | Status |
|---|---|---|---|---|---|---|
| `GET` | `/api/v1/health` | Service health check | None | `status`, `service` | None | ✅ OPERATIONAL |
| `GET` | `/api/v1/applications` | List all applications | None | List of `ApplicationResponse` | Reads `applications` | ✅ OPERATIONAL |
| `GET` | `/api/v1/applications/{application_id}` | Get application details | `application_id` (path) | `application_id`, `name`, `category`, `functions` | Reads `applications`, `functions` | ✅ OPERATIONAL |
| `GET` | `/api/v1/applications/{application_id}/expected-mappings` | List expected data mappings | `application_id` (path) | `application_id`, `expected_mappings` | Reads `expected_mappings`, `functions` | ✅ OPERATIONAL |
| `GET` | `/api/v1/applications/{application_id}/readiness` | Check app analysis readiness | `application_id` (path) | `is_ready`, `expected_mappings_count`, `has_policy` | Reads `applications`, `expected_mappings`, `policy_documents` | ✅ OPERATIONAL |
| `POST` | `/api/v1/extract-policy` | Run AI policy evidence extraction | `PolicyExtractionRequest` (`policy_text`, `application_name`) | `extraction_status`, `evidence` list | None (Stateless AI call) | ✅ OPERATIONAL |
| `POST` | `/api/v1/analyze` | Run live end-to-end AI analysis | `AnalyzeRequest` (`application_name`, `category`, `policy_text`) | `analysis_id`, `fdo_count`, `not_fdo_count`, `ambiguous_count`, `comparisons` | Writes `policy_documents`, `policy_evidence`, `analyses`, `comparisons`, `fdo_results`, `explanations` | ✅ OPERATIONAL |
| `POST` | `/api/v1/analyses` | Run analysis on pre-stored static policy | `AnalysisCreateRequest` (`application_id`) | `AnalysisReportResponse` | Writes `analyses`, `comparisons`, `fdo_results`, `explanations` | ✅ OPERATIONAL |
| `GET` | `/api/v1/analysis/{analysis_id}` | Get analysis report summary | `analysis_id` (path) | `AnalysisReportResponse` | Reads `analyses`, `comparisons`, `fdo_results` | ✅ OPERATIONAL |
| `GET` | `/api/v1/analyses/{analysis_id}` | Alias for analysis report summary | `analysis_id` (path) | `AnalysisReportResponse` | Reads `analyses`, `comparisons`, `fdo_results` | ✅ OPERATIONAL |
| `GET` | `/api/v1/analyses/{analysis_id}/results` | Get detailed itemized results | `analysis_id` (path) | List of `AnalysisResultResponse` | Reads `comparisons`, `fdo_results`, `explanations`, `expected_mappings` | ✅ OPERATIONAL |
| `GET` | `/api/v1/analysis/{analysis_id}/report` | Get rich frontend-ready report | `analysis_id` (path) | `RichAnalysisReportResponse` | Reads full analysis tree and formats grouped report | ✅ OPERATIONAL |

---

# 7. Database Audit

## 7.1 Engine & Configuration
- **Database Engine:** SQLite 3
- **Database File:** `D:\VIT\PROJECT\TARP\Backend\fdo_privacy.db`
- **ORM:** SQLAlchemy 2.0+ (`SessionLocal`, `create_all`)
- **Connection URL:** `sqlite:///./fdo_privacy.db`

## 7.2 Empirical Table & Row Counts (Verified 2026-09-08)

```text
CURRENT DATABASE STATE (fdo_privacy.db)
=======================================
applications           : 31 rows
functions              : 78 rows
expected_mappings      : 100 rows
policy_documents       : 32 rows  (31 static baseline policies + 1 live AI runtime policy)
policy_evidence        : 127 rows (126 static baseline evidence + 1 live AI extracted evidence)
normalized_evidence   : 0 rows   (Reserved schema)
analyses               : 12 rows  (Static validation runs + live AI runtime test runs)
comparisons            : 46 rows
fdo_results            : 46 rows
explanations           : 46 rows
```

## 7.3 Benchmark Preservation Strategy
To ensure that research benchmark data is never contaminated or overwritten by automated software testing, runtime AI analysis creates brand new database records:
- Runtime `PolicyDocument` receives ID `AI-POL-ANALYSIS-...`
- Runtime `PolicyEvidence` receives ID `AI-{hash}`
- Static records (`POL-NAV-01`, `DEC-101`, etc.) remain completely unmodified and preserved in their original state.

---

# 8. Dataset & Data Pipeline Audit

## 8.1 Dataset Inventory (`DATA/` Directory)
The primary dataset directory contains Excel workbooks detailing every stage of the project:
1. `FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx` — Canonical clean dataset used for DB import.
2. `FDO-Privacy_Final_Stage3_Dataset_COMPLETE.xlsx` — Master dataset with full metadata.
3. `FDO-Privacy_Stage2B_AnnotatorA/B` (12 files) — Inter-annotator agreement and pilot annotation workbooks.
4. `FDO-Privacy_Stage3A-3D` (18 files) — Schema definitions, policy extractions, QA remediation, and evidence completion matrices.
5. `FDO-Privacy_Stage4A-4E` (9 files) — Necessity analysis, purpose compatibility reviews, screening queues, and adjudication workbooks.
6. `FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx` — Visual dashboard data.
7. `FDO-Privacy_Stage7_Final_Research_Report_Package_v1.0.docx` — Complete written report.

## 8.2 Import Script Execution (`scripts/import_stage3.py`)
The `import_stage3.py` script populates `fdo_privacy.db` directly from `FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx`:
```text
Excel Dataset ──► import_stage3.py ──► SQLAlchemy Models ──► fdo_privacy.db
  Worksheets:
  - "Applications"   ──────► Application model   (31 apps)
  - "Expected Data"  ──────► Function & ExpectedMapping models (78 functions, 100 mappings)
  - "Policy Registry"──────► PolicyDocument model (31 policies)
  - "Declared Data"  ──────► PolicyEvidence model (126 evidence records)
```

---

# 9. Deterministic FDO Decision Engine Audit

The decision logic in `fdo_decision_service.py` evaluates `FDODecisionInput` against five sequential, deterministic rules:

| Rule # | Condition Matrix | FDO Status | Confidence | Decision Reason Summary |
|---|---|---|---:|---|
| **Rule 1** | `evidence_status == "NO_EVIDENCE"` | `AMBIGUOUS` | 0.30 | No declared evidence is available to determine functional justification. |
| **Rule 2** | `evidence_status in {"INSUFFICIENT", "UNKNOWN"}` | `AMBIGUOUS` | 0.40 | Evidence is insufficient to make a deterministic decision. |
| **Fallback 2B**| `evidence_status != "EXTRACTED"` | `AMBIGUOUS` | 0.40 | Evidence status does not support deterministic decision. |
| **Rule 3** | `data_match == "EXACT_MATCH"` AND `purpose_compatibility == "COMPATIBLE"` AND `functional_relationship == "RELATED"` | `NOT_FDO` | 0.90 | Declared data matches expected data, purpose is compatible, and functional evidence exists. |
| **Rule 4** | `data_match == "EXACT_MATCH"` AND `purpose_compatibility == "INCOMPATIBLE"` AND `functional_relationship == "RELATED"` | `FDO` | 0.85 | Declared data matches expected data, but declared purpose is incompatible with expected purpose. |
| **Rule 5** | `data_match == "NO_MATCH"` AND `functional_relationship == "RELATED"` | `FDO` | 0.80 | Declared data type differs from expected functional data type despite available evidence. |
| **Fallback** | Unmatched criteria combination | `AMBIGUOUS` | 0.50 | Available comparison evidence does not satisfy deterministic rules. |

---

# 10. Testing & Validation Audit

All test and validation scripts in the repository have been inspected and executed:

| Test Script | Tested Component | Observed Execution Result | Status |
|---|---|---|---|
| `test_gemini.py` | Direct Google Gemini API connectivity (`gemini-3.5-flash-lite`) | Output: `FDO Gemini API test successful` | ✅ PASSED |
| `test_ai_extraction.py` | Standalone AI evidence extraction (`ai_service.py`) | Successfully extracted `DATA.LOCATION.PRECISE` evidence for Google Maps | ✅ PASSED |
| `scripts/verify_fdo_decision.py` | Deterministic FDO decision logic (`EXP-099` vs `DEC-101`) | Output: `Status: FDO`, `Confidence: 0.85` (Purpose incompatibility rule triggered) | ✅ PASSED |
| `scripts/persist_fdo_test.py` | Full ORM persistence & transaction integrity | Analysis `ANALYSIS-NAV-01-TEST` committed successfully | ✅ PASSED |
| `scripts/test_failure_path.py` | Error handling & rollback on invalid inputs | Successfully caught invalid app error, verified DB rollback | ✅ PASSED |
| `scripts/validate_multi_app.py` | Multi-app batch analysis (`AMB-01`, `EDU-02`, `FIT-01`, `FOD-01`) | Executed all 4 apps, total mappings matched classified counts | ✅ PASSED |

---

# 11. Important Current End-to-End Test

The project has achieved a major milestone: **Full End-to-End Live AI-to-Database Pipeline Execution**.

### Test Execution Details (Verified from `fdo_privacy.db`)
- **Target Application:** `Google Maps` (`NAV-01`)
- **Analysis ID:** `ANALYSIS-NAV-01-8883cfd5`
- **Executed Endpoint:** `POST /api/v1/analyze`
- **Input Policy Text:** *"Google Maps collects precise location information for directions and nearby search."*

### Live Execution Flow & Output:
1. **Gemini Extraction:** Extracted 1 evidence item (`AI-35c2818b`), identifying `data_type="DATA.LOCATION.PRECISE"`, `purpose="directions and nearby search"`, `confidence=0.9`.
2. **Runtime Policy Creation:** Created `PolicyDocument` `AI-POL-ANALYSIS-NAV-01-8883cfd5` and `PolicyEvidence` `AI-35c2818b`.
3. **Evidence Matching & Decision Execution:**
   - **`EXP-015`** (`DATA.LOCATION.PRECISE` for Turn-by-Turn Navigation): Matched `AI-35c2818b`. Data match: `EXACT_MATCH`. Purpose compatibility evaluated as `INCOMPATIBLE` (exact string mismatch against expected purpose string). Decision: **`FDO`**.
   - **`EXP-016`** (`DATA.LOCATION.PRECISE` for Route Calculation): Matched `AI-35c2818b`. Data match: `EXACT_MATCH`. Purpose compatibility evaluated as `INCOMPATIBLE`. Decision: **`FDO`**.
   - **`EXP-017`** (`DATA.LOCATION.APPROXIMATE` for Location Search): No evidence extracted for approximate location (`NO_EVIDENCE`). Decision: **`AMBIGUOUS`**.
4. **Final Summary Statistics for Analysis `ANALYSIS-NAV-01-8883cfd5`:**
   - **Total Mappings:** 3
   - **FDO:** 2
   - **NOT_FDO:** 0
   - **AMBIGUOUS:** 1

> [!NOTE]
> This run demonstrates that live AI extraction feeds directly into the deterministic decision engine, persisting all intermediate artifacts and generating itemized explanations.

---

# 12. Implementation Bugs & Resolved Issues

The following technical issues were identified and successfully resolved during implementation:

1. **Uvicorn Working Directory Issue:**
   - *Problem:* Uvicorn server failed to load modules when executed from the root directory instead of `Backend/`.
   - *Fix:* Configured execution context to `Backend/` with proper `PYTHONPATH`.
2. **Disconnected AI Extraction in Early Prototype:**
   - *Problem:* `/analyze` originally ran on static stored policy data rather than live AI extractions.
   - *Fix:* Integrated `extract_policy_evidence()` and `create_runtime_policy()` directly into `analyze_endpoint()` in `main.py`.
3. **Ontology Data-Type Mismatch (`LOCATION.PRECISE` vs `DATA.LOCATION.PRECISE`):**
   - *Problem:* Gemini occasionally omitted the `DATA.` prefix, causing `evidence_matcher` to return `None`.
   - *Fix:* Implemented `_normalize_data_type()` in `ai_service.py` to enforce strict canonical `DATA.*` formatting.
4. **Analysis Runner Policy Parameter:**
   - *Problem:* `run_analysis()` defaulted to picking the first static policy in DB, ignoring newly created runtime policies.
   - *Fix:* Added optional `policy_id` parameter to `run_analysis()`.

---

# 13. System Architecture Diagram

```text
                          USER / CLIENT
                                │
                                ▼
                       ┌──────────────────┐
                       │   FastAPI API    │
                       │   (/api/v1/...)  │
                       └────────┬─────────┘
                                │
            ┌───────────────────┴───────────────────┐
            │                                       │
            ▼                                       ▼
  POST /api/v1/analyze                    GET /api/v1/applications
  (Live AI Pipeline)                      (Static Metadata)
            │                                       │
            ▼                                       ▼
 ┌─────────────────────┐                   ┌─────────────────┐
 │  Google Gemini API  │                   │  SQLite Database│
 │(gemini-3.5-flash)   │                   │ (fdo_privacy.db)│
 └──────────┬──────────┘                   └─────────────────┘
            │ (Extracted JSON)                              ▲
            ▼                                               │
 ┌─────────────────────┐                                    │
 │ _normalize_data_type│                                    │
 │  (Canonical DATA.*) │                                    │
 └──────────┬──────────┘                                    │
            │                                               │
            ▼                                               │
 ┌─────────────────────┐                                    │
 │ Policy Ingestion    │ ──────── Persists Policy & ────────┤
 │ Service             │          Evidence Records          │
 └──────────┬──────────┘                                    │
            │                                               │
            ▼                                               │
 ┌─────────────────────┐                                    │
 │  Evidence Matcher   │ ─────── Matches Expected vs ───────┤
 │  & Comparison       │          Declared Evidence         │
 └──────────┬──────────┘                                    │
            │                                               │
            ▼                                               │
 ┌─────────────────────┐                                    │
 │ Deterministic FDO   │ ─────── Applies 5-Rule Engine ─────┤
 │ Decision Engine     │          (FDO/NOT_FDO/AMBIGUOUS)   │
 └──────────┬──────────┘                                    │
            │                                               │
            ▼                                               │
 ┌─────────────────────┐                                    │
 │ Rich Report Service │ ─────── Builds Response & ─────────┘
 └──────────┬──────────┘          Commits DB Transaction
            │
            ▼
 [ Rich JSON Response ]
```

---

# 14. Technology Stack Audit

| Technology / Library | Role / Purpose | Implementation Status | Notes |
|---|---|---|---|
| **Python 3.10** | Core Programming Language | ✅ IMPLEMENTED | Powers backend and scripts |
| **FastAPI 0.115+** | Web Framework / REST API | ✅ IMPLEMENTED | 12 endpoints operating |
| **SQLAlchemy 2.0+** | Database ORM | ✅ IMPLEMENTED | 10 models defined |
| **SQLite 3** | Relational Database | ✅ IMPLEMENTED | Primary local database (`fdo_privacy.db`) |
| **Pydantic v2** | Data Validation & Schemas | ✅ IMPLEMENTED | Request/Response DTOs |
| **Google Gemini API** | AI Evidence Extraction | ✅ IMPLEMENTED | Uses `gemini-3.5-flash-lite` |
| **Uvicorn** | ASGI Web Server | ✅ IMPLEMENTED | Production ASGI server |
| **pandas / openpyxl** | Excel Dataset Processing | ✅ IMPLEMENTED | Used in `import_stage3.py` |
| **React / Next.js** | Frontend UI Framework | 🔵 PLANNED | Planned Stage 8.7 component |
| **PostgreSQL** | Production Database | 🔵 PLANNED | Planned future database |
| **Neo4j / GraphDB** | Knowledge Graph Store | ❌ NOT IMPLEMENTED / PLANNED | Conceptual architecture choice; code currently uses SQLite |
| **RDF / OWL / SPARQL** | Formal Semantic Web Stack | ❌ NOT IMPLEMENTED / PLANNED | Research foundation conceptual model; not implemented in code |
| **Jena / Fuseki / HermiT**| OWL Reasoners & Triple Stores| ❌ NOT IMPLEMENTED | Not present in codebase |

---

# 15. Current Component Status Table

| Component | Status | Evidence | Notes |
|---|---|---|---|
| **Research Methodology (Stages 1–7)** | ✅ COMPLETE | DOCX reports, 50+ Excel files | Baseline frozen |
| **Dataset (Stages 2–3)** | ✅ COMPLETE | Cleaned dataset imported | 27 analytical apps, 99 expected mappings |
| **Ontology Definition** | ✅ COMPLETE | Stage 2 MD & code constants | Canonical `DATA.*` taxonomy |
| **Database Schema & Models** | ✅ COMPLETE | `app/models/*.py`, `fdo_privacy.db` | 10 tables active |
| **Backend REST API** | ✅ COMPLETE | `app/main.py` | 12 endpoints active |
| **AI Evidence Extraction** | ✅ COMPLETE | `app/services/ai_service.py` | Integrated with Gemini API |
| **Runtime Policy Ingestion** | ✅ COMPLETE | `policy_ingestion_service.py` | Live policy & evidence persistence |
| **Evidence Matcher** | ✅ COMPLETE | `evidence_matcher.py` | Exact canonical data type matching |
| **Comparison Engine** | ✅ COMPLETE | `comparison_service.py` | Evaluates match & compatibility |
| **Deterministic FDO Decision Engine**| ✅ COMPLETE | `fdo_decision_service.py` | 5-rule engine operating |
| **Explanation Engine** | ✅ COMPLETE | `explanation_service.py` | Generates audit explanations |
| **Report Generation** | ✅ COMPLETE | `rich_report_service.py` | Rich JSON responses |
| **System Validation & Testing** | ✅ COMPLETE | 6 test scripts | End-to-end test verified |
| **Semantic Purpose Matching (NLP/LLM)**| 🟡 PARTIAL | Exact string matching currently used | LLM-assisted purpose compatibility planned |
| **Frontend UI (Web Dashboard)** | 🔵 PLANNED | Architecture specs in `Docs/` | Next major milestone |
| **Neo4j / Graph Reasoning** | 🔵 PLANNED | Conceptual spec | Optional future enhancement |

---

# 16. What Has Been Completed

### Research Accomplishments (Stages 1–7)
- Formulated the FDO problem statement and research scope.
- Built the Functional Data Ontology taxonomy and expected data baseline.
- Conducted annotations across 30 pilot apps, establishing a frozen 27-app analytical cohort.
- Completed manual 5-tier FDO adjudication across 99 expected mappings.
- Finalized research visualization workbooks and the final research report package (`.docx`).

### Backend & Software Accomplishments (Stage 8)
- Designed and implemented 10 SQLAlchemy ORM database models.
- Built dataset import pipeline (`import_stage3.py`) to seed `fdo_privacy.db`.
- Created FastAPI backend exposing 12 REST endpoints.
- Implemented deterministic 5-rule FDO decision engine (`fdo_decision_service.py`).
- Integrated Google Gemini AI (`gemini-3.5-flash-lite`) for live policy evidence extraction.
- Developed canonical data-type normalization (`_normalize_data_type`).
- Built runtime policy and evidence persistence (`policy_ingestion_service.py`).
- Successfully executed live end-to-end AI analysis test (`Google Maps / NAV-01`).

---

# 17. Remaining Work Roadmap

### 17.1 Immediate Next Tasks (Stage 8.6 - 8.7)
1. **Enhance Purpose Compatibility Matching:** Transition `evaluate_purpose_compatibility()` from strict string equality to semantic embedding/LLM-assisted purpose comparison.
2. **Build Web Frontend (React/Next.js):** Create an interactive dashboard allowing users to select an app, paste policy text, run analysis, and inspect itemized FDO reports.

### 17.2 Mid-Term Technical Tasks (Stage 8.8 - 8.10)
1. **Automated Prototype vs. Research Benchmark Evaluation:** Build an automated evaluation script to run all 27 analytical apps through the live AI pipeline and compare prototype predictions against the Stage 5 research benchmark.
2. **Error Recovery & Rate Limiting:** Add retry logic, backoff algorithms, and fallback handling for Gemini API rate limits.

### 17.3 Long-Term / Advanced Tasks
1. **Knowledge Graph Integration (Neo4j):** (Optional) Implement graph representation of policy evidence and expected mappings if multi-hop relational querying is required.
2. **Production Deployment:** Containerize backend with Docker, set up PostgreSQL, and deploy ASGI server behind Nginx.

---

# 18. Final Project Position

1. **What is the project?**  
   FDO-Privacy is an explainable AI framework and software prototype designed to detect Functional Data Overreach (FDO) by comparing privacy-policy declared collection against expected application functionality.
2. **What problem does it solve?**  
   It evaluates whether personal data collection is functionally necessary and substantively justified, moving beyond superficial policy summarization or coarse permission checking.
3. **What has been completed?**  
   Stages 1–7 (Research foundation, baseline dataset, manual adjudication, research benchmark, and report package) and core Stage 8 backend software implementation (database schema, REST API, deterministic FDO engine, live Gemini AI integration).
4. **What is currently working?**  
   The FastAPI backend, SQLite database, deterministic decision engine, live Gemini AI extraction, runtime policy persistence, and rich report generation are fully operational.
5. **What has been experimentally validated?**  
   Standalone AI extraction, deterministic decision logic, ORM persistence, transaction rollback, multi-app batch execution, and a live end-to-end AI analysis run on Google Maps (`ANALYSIS-NAV-01-8883cfd5`).
6. **What is the current Stage 8 position?**  
   Stage 8 core pipeline integration (Stage 8.5+) is complete. The system can accept raw policy text via API, extract evidence using Gemini, run deterministic FDO analysis, and return structured reports.
7. **What is the next most important task?**  
   Developing the React/Next.js Web Frontend to provide a user-facing dashboard for the prototype.
8. **What is still required before the project can be considered complete?**  
   Frontend UI construction, semantic purpose matching enhancement, and automated evaluation of prototype predictions against the 27-app research benchmark.

---

# Recommended Next Steps

1. **Develop Web Frontend Interface:** Construct a responsive React/Next.js dashboard interfacing with `/api/v1/applications` and `/api/v1/analyze`.
2. **Upgrade Purpose Compatibility Service:** Incorporate semantic similarity scoring (e.g., using sentence-transformers or Gemini embedding API) in `comparison_service.py` to complement exact string matching.
3. **Run Full Benchmark Evaluation:** Execute an automated evaluation script over the 27 analytical applications to measure prototype precision, recall, and agreement against the manual Stage 5 research benchmark.
