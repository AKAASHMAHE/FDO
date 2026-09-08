# FDO-Privacy — Complete Project Master Status

**Audit date:** 2026-09-08  
**Project root:** `D:\VIT\PROJECT\TARP`

## Purpose

This is the consolidated master document created from the two supplied source documents:

1. **`full idea.md`** — the original project idea, target architecture, research vision, ontology, AI, knowledge graph, SPARQL, reasoning, evaluation, and intended user experience.
2. **`FDO-Privacy_Project_Status.md`** — what has actually been completed/implemented and tested so far.

The original idea is preserved below as the **target specification**, while the status document is preserved as the **current implementation record**. The gap assessment at the end identifies what is left.

> **Important:** The supplied documents are the source of truth. This master file does not silently convert planned technologies into implemented technologies.

---

# Part I — Current Status at a Glance

## Overall Position

**Stages 1–7:** Complete according to the supplied status document.

**Stage 8:** Core backend and live AI-to-FDO pipeline operational and validated; the broader semantic knowledge-graph architecture remains to be implemented.

## Current working pipeline

```text
Raw Privacy Policy Text
        ↓
FastAPI /analyze
        ↓
Gemini Evidence Extraction
        ↓
Canonical DATA.* Normalization
        ↓
Runtime PolicyDocument
        ↓
Runtime PolicyEvidence
        ↓
Evidence Matcher
        ↓
Expected-vs-Declared Comparison
        ↓
Deterministic FDO Decision
        ↓
Explanation
        ↓
Analysis Report
```

## Target full pipeline from the original idea

```text
Privacy Policy
        ↓
NLP / AI
        ↓
Structured Privacy Facts
        ↓
FDO OWL + RDF
        ↓
Knowledge Graph
        ↓
SPARQL
        ↓
Reasoning Engine
        ↓
Functional Data Overreach Analysis
        ↓
Explainable Report
        ↓
Dashboard
```

## Key distinction

The current implementation is primarily:

```text
AI → Structured Evidence → SQLite/SQLAlchemy → Deterministic FDO
```

The original target architecture is:

```text
AI → FDO OWL/RDF → Knowledge Graph → SPARQL/Reasoning → FDO Analysis
```

---

# Part II — Complete Current Status Document

The following section preserves the supplied implementation-status document as the detailed record of what has been done.

---

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


---

# Part III — Original Full Project Idea / Target Specification

The following section preserves the supplied original idea as the target specification for the complete system.

---

# FDO Privacy — Full Project Idea

## 1. Project Title

**FDO Privacy: An Explainable Functional Data Ontology Framework for Semantic Privacy Analysis**

### Possible IEEE-style titles
- Functional Data Ontology for Explainable Privacy Policy Analysis
- Semantic Privacy Analysis Using Functional Data Ontology and Knowledge Graph Reasoning
- An Ontology-Driven Framework for Functional Data Overreach Detection in Privacy Policies
- FDO Privacy: An AI and Knowledge-Graph Framework for Machine-Readable Privacy Analysis

---

## 2. Executive Idea

The central problem addressed by FDO Privacy is that privacy information is mostly presented as natural-language privacy policies. These policies are difficult for ordinary users to understand and, more importantly for this project, difficult for machines to interpret, connect, compare, and reason about automatically.

The project proposes a **Functional Data Ontology (FDO)** that represents privacy information as structured, machine-readable knowledge.

Instead of keeping privacy information only as statements such as:

> "The application may collect location information to provide location-based services and may share information with service providers."

the system converts the meaning into structured relationships:

```text
Application
    -> performs -> Navigation
Navigation
    -> requires -> Location
Application
    -> collects -> Location
Location
    -> usedFor -> NavigationService
Application
    -> shares -> Location
Location
    -> sharedWith -> ServiceProvider
Location
    -> retainedFor -> RetentionPeriod
User
    -> hasRightTo -> DeleteData
```

This structured representation can then be stored in an RDF/OWL knowledge graph and queried using SPARQL.

A reasoning engine can derive information that was not explicitly written as a single sentence but follows logically from the ontology.

The central pipeline is:

```text
Natural-Language Privacy Information
                |
                v
        NLP / AI Extraction
                |
                v
      Structured Privacy Facts
                |
                v
       FDO Ontology (OWL/RDF)
                |
                v
       Knowledge Graph (Neo4j / RDF Store)
                |
                v
        SPARQL / Reasoning
                |
                v
 Semantic Privacy Analysis & FDO Detection
                |
                v
     Explainable Human Report
```

---

## 3. Problem We Are Solving

Privacy policies are usually:
- lengthy;
- written in natural language;
- legally or technically complex;
- inconsistent in terminology;
- difficult to compare;
- difficult for machines to reason over.

A privacy policy may mention a data type in one section, its purpose in another, its recipient somewhere else, and its retention period in another section.

A human may understand these statements by reading the document as a whole. A machine needs the relationships to be explicitly represented or computationally inferred.

### Research gap

Existing privacy systems may focus on:
- privacy-policy summarization;
- individual privacy-statement extraction;
- consent management;
- runtime compliance;
- privacy scoring.

FDO Privacy focuses on a semantic foundation:

> **Representing the functional meaning and relationships of privacy information as machine-readable knowledge so automated semantic analysis and reasoning become possible.**

Therefore, the project is not merely another privacy-policy summarizer.

---

## 4. Core Research Questions

### Main question

> **Can natural-language privacy information be transformed into a Functional Data Ontology that enables machines to represent, query, reason about, and detect inconsistencies or functional overreach in data practices?**

### Specific question

> **Can an application's functional requirements and its declared privacy practices be represented in a common semantic model and compared automatically to identify whether data usage matches declared functionality and purpose?**

---

## 5. Functional Data Ontology (FDO)

### 5.1 What is FDO?

FDO stands for **Functional Data Ontology**.

The ontology defines concepts and relationships needed to represent how personal data functions within an application ecosystem.

It describes relationships among:
- applications;
- application functions;
- personal data;
- processing activities;
- purposes;
- recipients;
- retention;
- consent;
- user rights;
- security;
- expected data requirements;
- privacy-policy evidence.

### 5.2 Why "functional"?

The project does not only ask:

> "What data is collected?"

It asks:

> **"What function does the application perform, what data does that function require, what processing occurs, why is the data processed, and does the declared data practice correspond to that function?"**

Example:

```text
Navigation Application
        |
        +-- performsFunction --> Navigation
                                  |
                                  +-- requiresData --> Location
```

If the policy also states that the application collects Contacts or Medical History, the semantic model provides a basis for asking whether these data types are required by the identified functionality.

---

## 6. Functional Data Overreach (FDO)

### Definition

Functional Data Overreach is:

> **Collection or processing of user data that exceeds the minimum data reasonably required for the application's identified primary functionality, subject to the stated purpose and available justification.**

### Example

Flashlight application:

```text
Function:
Turn flashlight ON/OFF

Expected:
Flash/camera capability

Declared:
Location
Contacts
Microphone
Device identifiers
```

The system identifies unexpected data as FDO candidates.

Importantly, an unexpected data type is **not automatically declared illegal, malicious, or wrong**. The system continues to examine:
- purpose;
- justification;
- disclosure;
- recipients;
- processing activity;
- retention;
- consent;
- policy consistency.

The result is an explainable analytical classification rather than a simplistic good/bad label.

---

## 7. Core Philosophy

FDO Privacy follows four principles:

### 7.1 Semantic Representation
Privacy information should be represented as structured knowledge rather than remaining only as text.

### 7.2 Functional Context
Data collection should be interpreted in relation to application functionality.

### 7.3 Machine Reasoning
The representation should support semantic queries and logical inference.

### 7.4 Explainability
Every detected issue should be traceable to policy evidence, ontology relationships, queries, and reasoning.

---

# 8. Overall System Architecture

```text
                         USER
                          |
                          v
                Web Application / UI
                          |
             +------------+------------+
             |                         |
             v                         v
      Privacy Policy Input       Application Input
       PDF / URL / Text       Name / Category / Description
             |                         |
             +------------+------------+
                          |
                          v
                 FastAPI Backend
                          |
                          v
                Policy Acquisition
                          |
                          v
                 Text Extraction
                          |
                          v
                 Clause Segmentation
                          |
                          v
                  NLP / AI Layer
                          |
             +------------+------------+
             |                         |
             v                         v
     Privacy Fact Extraction    Function Extraction
             |                         |
             v                         v
     Data / Purpose / Share      App Functions
     Retention / Rights         Expected Data
             |                         |
             +------------+------------+
                          |
                          v
                  FDO Mapping Layer
                          |
                          v
                    FDO Ontology
                     OWL + RDF
                          |
                          v
                  Knowledge Graph
                  Neo4j / RDF Store
                          |
             +------------+------------+
             |                         |
             v                         v
        SPARQL Queries          Reasoning Engine
                                      |
                                      v
                               Derived Knowledge
             |                         |
             +------------+------------+
                          |
                          v
                 FDO Analysis Engine
                          |
             +------------+------------+
             |                         |
             v                         v
     Functional Gap Analysis    Policy Justification
             |                         |
             +------------+------------+
                          |
                          v
                 Risk / Analysis Layer
                          |
                          v
                 Explainable Report
                          |
                          v
                    Dashboard
                          |
                          v
                         USER
```

---

# 9. End-to-End Project Flow

## Step 1 — User input

The user provides:
- Privacy Policy PDF;
- Privacy Policy URL;
- or Privacy Policy text.

Optional application metadata:
- name;
- category;
- description;
- functionality;
- store metadata.

## Step 2 — Policy acquisition

If a URL is supplied, the system retrieves the relevant policy.

If a PDF is supplied, the system extracts its text.

The result is normalized into machine-processable text.

## Step 3 — Text preprocessing

The NLP pipeline:
- removes irrelevant formatting;
- identifies headings;
- splits paragraphs;
- performs sentence segmentation;
- performs clause segmentation;
- normalizes terminology;
- identifies candidate privacy statements.

## Step 4 — NLP and AI extraction

The AI/NLP layer extracts candidate:
- data types;
- processing activities;
- purposes;
- recipients;
- retention;
- consent;
- user rights;
- security information.

## Step 5 — Application function analysis

The system analyzes the application description and identifies functions.

Example:

```text
"Provides turn-by-turn navigation,
route planning and nearby place discovery."

        ↓

Functions:
Navigation
Route Planning
Nearby Place Discovery
```

## Step 6 — Expected data identification

The FDO/Expected Data Ontology maps application functions to reasonably expected data.

Example:

```text
Navigation -> requires -> Location
```

## Step 7 — Ontology mapping

Extracted privacy facts and functional requirements are mapped into FDO concepts and relationships.

## Step 8 — RDF/OWL representation

The semantic facts are represented using RDF triples and the FDO OWL ontology.

## Step 9 — Knowledge graph

The resulting semantic knowledge is stored and/or synchronized into the graph layer.

## Step 10 — SPARQL and reasoning

SPARQL queries retrieve relevant relationships. A reasoning engine derives implicit relationships and checks ontology consistency where applicable.

## Step 11 — FDO detection

Expected data is compared with declared/collected data.

## Step 12 — Policy justification

For unexpected data, the system checks whether the policy provides a stated purpose or justification.

## Step 13 — Explainable analysis

The system produces an evidence-backed explanation.

## Step 14 — Dashboard/report

The user receives:
- expected data;
- declared data;
- unexpected data;
- FDO classification;
- policy justification;
- data-flow relationships;
- risk indicators;
- evidence;
- recommendations;
- comparison information.

---

# 10. NLP Layer

The NLP layer converts unstructured privacy-policy language into candidate structured facts.

### Data entities
- Location
- Email
- Phone number
- Contacts
- Device ID
- IP address
- Transaction data

### Purpose entities
- Service delivery
- Analytics
- Personalization
- Advertising
- Security
- Fraud prevention

### Processing activities
- Collect
- Store
- Use
- Share
- Disclose
- Retain
- Delete

### Recipient entities
- Service provider
- Advertising partner
- Analytics provider
- Business partner
- Government authority

### User rights
- Access
- Correction
- Deletion
- Portability
- Withdrawal of consent

The NLP layer can use a combination of deterministic preprocessing, NLP libraries, embeddings, and LLM-based semantic extraction.

---

# 11. AI API Layer

An LLM API can be used for semantic extraction and classification from privacy-policy clauses.

Possible providers:
- OpenAI API;
- Google Gemini API;
- another compatible LLM service.

The LLM should not be treated as the final source of truth.

The architecture should be:

```text
Privacy Policy
      |
      v
LLM / NLP
      |
      v
Candidate Facts
      |
      v
Validation / Normalization
      |
      v
FDO Ontology Mapping
```

The AI performs language understanding. The ontology and reasoning layer provide formal structure and logical analysis.

### Example

Input:

```text
"We may collect your precise location to provide
navigation and improve our location-based services."
```

Structured output:

```json
{
  "data_type": "Location",
  "precision": "Precise",
  "activity": "Collect",
  "purpose": [
    "Navigation",
    "Service Improvement"
  ],
  "evidence": "original policy clause"
}
```

The extracted information is normalized and mapped to ontology concepts.

---

# 12. AI Output Schema

The LLM should preferably return controlled structured output rather than unrestricted prose.

Conceptually:

```text
Clause
 |
 +-- DataType
 +-- ProcessingActivity
 +-- Purpose
 +-- Recipient
 +-- Retention
 +-- Consent
 +-- UserRight
 +-- Evidence
 +-- Confidence
```

The backend validates the output before inserting it into the knowledge graph.

---

# 13. Application Function Analyzer

The second major AI/NLP task is understanding what the application does.

Example:

```text
Application description:
"Navigate, find nearby places and get
turn-by-turn directions."

        ↓

Functions:
Navigation
Location Search
Directions

        ↓

Expected Data:
Location
```

The functional model is then connected to the privacy model.

---

# 14. Expected Data Ontology

The Expected Data Ontology maps application functionality to data that is reasonably required or optionally useful.

Example:

| Application Function | Expected Data | Optional Data |
|---|---|---|
| Messaging | Phone / Contacts | Camera |
| Navigation | Location | Camera |
| Banking | Identity / Transaction data | Location |
| Streaming | Account / Device information | Location |
| Shopping | Account / Address / Payment data | Location |
| Flashlight | Device/flash capability | None |

This ontology establishes the baseline against which declared data practices can be evaluated.

---

# 15. FDO Ontology — OWL + RDF

The FDO ontology is the semantic backbone of the system.

## RDF

RDF represents information as triples:

```text
Subject -> Predicate -> Object
```

Example:

```text
NavigationApp -> performsFunction -> Navigation
Navigation -> requiresData -> Location
NavigationApp -> collectsData -> Location
Location -> usedFor -> NavigationService
NavigationApp -> sharesDataWith -> ServiceProvider
```

## OWL

OWL formally defines:
- classes;
- properties;
- restrictions;
- subclass relationships;
- equivalence;
- logical characteristics;
- semantic constraints.

Suggested classes:

```text
Application
Function
PersonalData
SensitiveData
ProcessingActivity
Purpose
Recipient
RetentionPolicy
User
UserRight
Consent
SecurityMeasure
PrivacyPolicy
PolicyClause
ExpectedData
DeclaredData
Overreach
Justification
Risk
```

Suggested relationships:

```text
performsFunction
requiresData
collectsData
usesDataFor
sharesDataWith
retainsDataFor
hasUserRight
hasPurpose
hasEvidence
hasJustification
```

---

# 16. RDF Representation Example

Conceptual representation:

```text
fdo:NavigationApp
    fdo:performsFunction fdo:Navigation .

fdo:Navigation
    fdo:requiresData fdo:Location .

fdo:NavigationApp
    fdo:collectsData fdo:Location .

fdo:NavigationApp
    fdo:collectsData fdo:Contacts .

fdo:NavigationApp
    fdo:sharesDataWith fdo:ServiceProvider .

fdo:Location
    fdo:hasPurpose fdo:NavigationService .
```

The privacy policy is therefore transformed from a document into interconnected knowledge.

---

# 17. Knowledge Graph — Neo4j

Neo4j can be used for graph storage, traversal, and visualization.

Conceptual structure:

```text
             [Application]
                  |
        performsFunction
                  |
                  v
             [Function]
                  |
             requiresData
                  |
                  v
            [PersonalData]
             /                 hasPurpose     sharedWith
          /                        v                 v
   [Purpose]          [Recipient]
```

The graph can be used to visualize relationships between applications, data, purposes, recipients, functions, and processing activities.

### Important architectural distinction

RDF/OWL and Neo4j serve different roles.

- **OWL/RDF**: formal semantic representation.
- **Neo4j**: graph-oriented storage, traversal, visualization and graph analysis.

For standards-compliant RDF/SPARQL/reasoning, **Apache Jena Fuseki** can provide the RDF/SPARQL layer.

The project should avoid maintaining two unrelated sources of truth. A canonical representation and controlled synchronization/export strategy should be defined.

---

# 18. Apache Jena Fuseki

Apache Jena Fuseki can provide an RDF dataset and SPARQL endpoint.

Conceptually:

```text
FDO OWL Ontology
        |
        v
    RDF Triples
        |
        v
Apache Jena / Fuseki
        |
        +---- SPARQL Queries
        |
        +---- Dataset Access
        |
        +---- Reasoning Integration
```

Fuseki enables semantic questions to be asked against the RDF representation.

---

# 19. SPARQL Queries

SPARQL is used to query the semantic knowledge.

### Query: What data does an application collect?

```sparql
SELECT ?data
WHERE {
    fdo:NavigationApp fdo:collectsData ?data .
}
```

### Query: What data does a function require?

```sparql
SELECT ?data
WHERE {
    fdo:Navigation fdo:requiresData ?data .
}
```

### Query: What collected data is not explicitly expected?

Conceptually:

```sparql
SELECT ?data
WHERE {
    fdo:NavigationApp fdo:collectsData ?data .
    FILTER NOT EXISTS {
        fdo:Navigation fdo:requiresData ?data .
    }
}
```

This creates an FDO candidate set for further analysis.

---

# 20. Reasoning Engine

Some conclusions are not explicitly stored as individual facts.

A reasoning engine can derive knowledge from ontology semantics and rules.

Possible technologies:
- Apache Jena reasoning;
- HermiT;
- Pellet.

Their exact role should be selected according to the OWL profile and reasoning requirements.

### Example

Explicit facts:

```text
Navigation
    requiresData
Location

NavigationApp
    performsFunction
Navigation

NavigationApp
    collectsData
Contacts
```

A semantic rule/query can support the conclusion:

```text
NavigationApp
    collects
Contacts

Contacts
    not required by identified Navigation function
```

This becomes an FDO candidate, which is then checked for policy justification.

---

# 21. HermiT / Pellet

HermiT and Pellet can be considered for OWL reasoning, consistency checking, and inference.

Their role differs from the LLM:

```text
LLM
 |
 +-- understands natural language
 +-- extracts candidate facts

OWL Reasoner
 |
 +-- applies ontology semantics
 +-- derives logical relationships
 +-- checks consistency
```

The strongest design is:

```text
AI for Language Understanding
+
Ontology for Formal Representation
+
Reasoner for Logical Inference
+
SPARQL for Querying
```

---

# 22. FDO Detection Engine

The FDO engine combines:

1. application functionality;
2. expected data;
3. declared data;
4. purposes;
5. policy justification;
6. recipients;
7. retention;
8. reasoning results.

Core logic:

```text
                APPLICATION
                     |
          +----------+----------+
          |                     |
          v                     v
    FUNCTIONAL MODEL       PRIVACY POLICY
          |                     |
          v                     v
    EXPECTED DATA          DECLARED DATA
          |                     |
          +----------+----------+
                     |
                     v
                  COMPARE
                     |
                     v
           FUNCTIONAL DATA GAP
                     |
                     v
             FDO CANDIDATE
                     |
                     v
          POLICY JUSTIFICATION
                     |
          +----------+----------+
          |          |          |
          v          v          v
       Explained  Undisclosed  Contradiction
```

---

# 23. Policy Justification Analysis

An unexpected data type should not automatically be labeled a privacy violation.

For every FDO candidate, examine whether the policy provides a purpose or justification.

Possible classifications:

### Expected
The data is reasonably associated with the application's identified functionality.

### Disclosed Overreach
The data appears unnecessary for the identified functionality, but the policy explicitly provides a purpose.

### Undisclosed Overreach
The data appears functionally unnecessary and the policy does not adequately explain why it is collected.

### Policy Contradiction
The structured evidence conflicts with another policy statement.

All classifications should retain the relevant policy evidence.

---

# 24. Explainable AI

The system should not only output:

```text
Privacy Risk = 81
```

Instead it should explain the result.

Example:

```text
Potential Functional Data Overreach Detected

Data:
Contacts

Application Function:
Navigation

Expected Requirement:
Location

Reason:
Contacts are not associated with the identified
primary navigation functionality.

Policy:
The policy declares collection of contacts.

Justification:
No clear purpose identified for navigation.

Classification:
Potential Undisclosed Functional Data Overreach

Risk:
High
```

The user should be able to trace the result to the relevant policy clause and semantic relationships.

---

# 25. Explainability Pipeline

```text
Policy Clause
     |
     v
Extracted Fact
     |
     v
Ontology Relationship
     |
     v
SPARQL / Reasoning Result
     |
     v
FDO Detection
     |
     v
Explanation Generator
     |
     v
Human-readable Explanation
```

---

# 26. Privacy Risk Scoring

Scoring is a downstream component, not the core contribution.

Possible dimensions:

```text
Functional Necessity
Transparency
Purpose Alignment
Third-party Sharing
Retention
User Control
Policy Consistency
```

The score should be described as:

> **An explainable analytical indicator derived from the project's defined criteria.**

It should not be presented as a legal certification or definitive judgment.

---

# 27. Data-Flow Visualization

The semantic graph can be used to visualize how data moves.

Example:

```text
USER
 |
 | provides
 v
[Location]
 |
 | collected by
 v
[Navigation App]
 |
 | used for
 v
[Navigation]
 |
 | shared with
 v
[Service Provider]
 |
 | retained for
 v
[Retention Period]
```

This makes privacy relationships understandable to users.

---

# 28. Application Comparison

Comparison is a secondary feature built on the common semantic model.

Instead of comparing raw privacy-policy text, the system compares structured privacy knowledge.

```text
                 PRIVACY COMPARISON
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
     APPLICATION A APPLICATION B APPLICATION C
          |             |             |
          +-------------+-------------+
                        |
                        v
              COMMON FDO ATTRIBUTES
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
   Data Collection  Data Sharing   User Rights
        |
        v
 Functional Necessity
        |
        v
 FDO / Risk Comparison
        |
        v
 COMPARISON REPORT
```

Because all applications are represented using the same ontology, their privacy information can be compared consistently.

---

# 29. Backend / API Architecture

The backend coordinates the system:

```text
Frontend
   |
   v
FastAPI
   |
   +-- Policy API
   +-- Application API
   +-- Analysis API
   +-- Ontology API
   +-- Knowledge Graph API
   +-- SPARQL Query API
   +-- Comparison API
   +-- Report API
```

Overall backend flow:

```text
Input
  |
  v
NLP / AI
  |
  v
Ontology Mapping
  |
  v
Knowledge Graph
  |
  v
SPARQL / Reasoning
  |
  v
FDO Analysis
  |
  v
Response
```

---

# 30. Suggested API Modules

## Policy API
- accepts PDF/URL/text;
- extracts policy text;
- stores policy metadata.

## NLP API
- clause segmentation;
- entity extraction;
- privacy fact extraction;
- purpose extraction;
- recipient extraction.

## Application Function API
- application classification;
- function extraction;
- expected data identification.

## Ontology API
- maps extracted concepts;
- validates ontology data;
- generates RDF/OWL representation.

## Knowledge Graph API
- stores graph information;
- retrieves relationships;
- supports graph traversal.

## SPARQL API
- semantic queries;
- expected-vs-declared data queries;
- privacy relationship queries.

## Reasoning API
- ontology inference;
- consistency checking;
- derived semantic relationships.

## FDO Analysis API
- functional gap detection;
- overreach classification;
- policy justification;
- risk generation.

## Comparison API
- application comparison;
- privacy attribute comparison;
- FDO comparison.

## Report API
- creates structured human-readable results.

---

# 31. Complete Technology Stack

| Layer | Technology | Role |
|---|---|---|
| Frontend | React / Next.js | User interface |
| UI | Tailwind CSS | Interface styling |
| Backend | Python | Core application logic |
| API | FastAPI | REST API |
| NLP | spaCy / Transformers | Text processing |
| AI | OpenAI API / Gemini API | Semantic extraction/classification |
| Embeddings | Sentence Transformers | Semantic similarity where required |
| Ontology | OWL | Formal semantic model |
| Knowledge Representation | RDF | Machine-readable triples |
| Semantic Query | SPARQL | Semantic querying |
| Graph Database | Neo4j | Graph storage/visualization |
| RDF/SPARQL Server | Apache Jena Fuseki | RDF dataset and SPARQL endpoint |
| Reasoning | Apache Jena / HermiT / Pellet | Inference and consistency |
| Relational DB | SQLite / PostgreSQL | Application/system records |
| ORM | SQLAlchemy | Relational database access |
| Visualization | React graph/chart libraries | Dashboard |
| Deployment | Docker | Environment/deployment consistency |

---

# 32. Storage Architecture

A practical system can use two storage layers.

## Relational database

SQLite/PostgreSQL can store:
- applications;
- analysis jobs;
- policy metadata;
- processing status;
- reports;
- system configuration.

## Semantic/graph layer

RDF/Neo4j can represent:
- applications;
- functions;
- personal data;
- purposes;
- processing;
- recipients;
- retention;
- rights;
- ontology relationships;
- derived knowledge.

This separates operational records from semantic knowledge.

---

# 33. Complete Working Example

Consider a navigation application.

### Application information

```text
Application:
Navigation App

Functions:
- Route planning
- Turn-by-turn navigation
- Nearby place discovery
```

### Expected data

```text
Location
```

### Privacy policy declares

```text
Collects:
- Location
- Device ID
- Contacts

Uses location for:
- Navigation
- Service improvement

Shares certain information with:
- Service providers
```

### NLP extracts

```text
Location -> Collect
Device ID -> Collect
Contacts -> Collect

Location -> Purpose -> Navigation
Location -> Purpose -> Service Improvement

Application -> SharesWith -> Service Provider
```

### Ontology representation

```text
NavigationApp
    performsFunction
        Navigation

Navigation
    requiresData
        Location

NavigationApp
    collectsData
        Location

NavigationApp
    collectsData
        DeviceID

NavigationApp
    collectsData
        Contacts
```

### FDO analysis

```text
Expected:
Location

Declared:
Location
Device ID
Contacts

Unexpected:
Device ID
Contacts
```

Suppose the policy explains Device ID for security but gives no clear purpose for Contacts.

Then:

```text
Device ID
    -> Additional collection with stated purpose

Contacts
    -> Potential Undisclosed Functional Data Overreach
```

The final report explains the evidence and reasoning.

---

# 34. Full End-to-End Architecture

```text
                         USER
                          |
                          v
              Upload Policy / Enter URL
                          |
                          v
                   FASTAPI BACKEND
                          |
                          v
                 POLICY EXTRACTION
                          |
                          v
                 CLAUSE SEGMENTATION
                          |
                          v
                  NLP + AI ANALYSIS
                          |
              +-----------+-----------+
              |                       |
              v                       v
       PRIVACY FACTS            APP FUNCTIONS
              |                       |
              v                       v
      DATA / PURPOSE /          EXPECTED DATA
      SHARING / RETENTION
              |                       |
              +-----------+-----------+
                          |
                          v
                    FDO MAPPING
                          |
                          v
                 OWL + RDF ONTOLOGY
                          |
                          v
                SEMANTIC KNOWLEDGE
                          |
             +------------+------------+
             |                         |
             v                         v
       JENA FUSEKI                 NEO4J
             |                         |
             v                         v
        SPARQL QUERIES          GRAPH ANALYSIS
             |                         |
             +------------+------------+
                          |
                          v
                  REASONING ENGINE
                          |
                          v
               FDO DETECTION ENGINE
                          |
                          v
              POLICY JUSTIFICATION
                          |
                          v
                 RISK / EXPLANATION
                          |
                          v
                 REPORT / DASHBOARD
                          |
                          v
                         USER
```

---

# 35. Major Project Modules

## Module 1 — Policy Acquisition
Input:
- PDF;
- URL;
- text.

Output:
- normalized policy text.

## Module 2 — NLP Processing
Output:
- clauses;
- entities;
- candidate privacy facts.

## Module 3 — AI Semantic Extraction
Output:
- data;
- purpose;
- processing;
- recipients;
- retention;
- rights;
- consent;
- evidence.

## Module 4 — Application Function Analysis
Output:
- application category;
- functions;
- expected data.

## Module 5 — FDO Ontology
Defines the semantic vocabulary and relationships.

## Module 6 — RDF/OWL Representation
Converts extracted facts into machine-readable semantic triples.

## Module 7 — Knowledge Graph
Stores and visualizes connected privacy information.

## Module 8 — SPARQL Query Layer
Answers semantic questions from the graph.

## Module 9 — Reasoning Engine
Derives implicit information and checks consistency.

## Module 10 — FDO Detection Engine
Compares expected and declared data.

## Module 11 — Policy Justification Engine
Determines whether unexpected processing is explained.

## Module 12 — Explainable Risk Engine
Produces evidence-backed privacy analysis.

## Module 13 — Comparison Engine
Compares applications using the common ontology.

## Module 14 — Dashboard
Displays:
- privacy data;
- data flow;
- expected data;
- declared data;
- FDO candidates;
- explanations;
- comparison;
- recommendations.

---

# 36. What the User Ultimately Sees

The complicated technical pipeline stays behind the scenes.

Example:

```text
APPLICATION: Navigation App

FUNCTION:
Navigation

EXPECTED DATA:
✓ Location

DECLARED DATA:
✓ Location
✓ Device ID
⚠ Contacts

FUNCTIONAL DATA OVERREACH:
Contacts

WHY?
Contacts are not associated with the identified
primary navigation function.

POLICY JUSTIFICATION:
No clear purpose identified.

CLASSIFICATION:
Potential Undisclosed Overreach

EVIDENCE:
Relevant privacy-policy clause

RISK:
High

RECOMMENDATION:
Review whether contact collection is necessary
for the stated navigation functionality.
```

---

# 37. What Makes the Project Innovative

The project should not claim that privacy policies, LLMs, or knowledge graphs have never been used before.

The proposed contribution is the combination of:

### 1. Functional perspective
Relating data collection to application functionality.

### 2. Formal semantic representation
Defining an FDO ontology using OWL/RDF.

### 3. AI-to-ontology pipeline
Using NLP/LLMs to transform natural-language privacy statements into structured semantic facts.

### 4. Knowledge graph representation
Connecting data, purposes, processing, recipients, retention and rights.

### 5. Machine reasoning
Using SPARQL and ontology reasoning to query and derive privacy knowledge.

### 6. Functional Data Overreach detection
Comparing expected data requirements against declared data practices.

### 7. Explainability
Providing the evidence and reasoning behind detected overreach instead of an unexplained score.

---

# 38. What the Project Is NOT

### Not simply a privacy-policy summarizer
A summarizer tells users what the policy says. FDO Privacy additionally models relationships and performs semantic analysis.

### Not a consent management system
The project is not primarily responsible for managing acceptance/consent.

### Not a runtime behavior monitor
The project primarily analyzes declared privacy information and functional expectations rather than claiming to observe actual runtime behavior.

### Not a legal compliance certification system
The system provides analytical results and should not be presented as a legal determination.

### Not simply a privacy-score generator
The score is a downstream result. The core contribution is the semantic representation and functional analysis behind it.

---

# 39. Research Contribution Structure

```text
Layer 1
NATURAL LANGUAGE UNDERSTANDING
        |
        v
Layer 2
FUNCTIONAL DATA ONTOLOGY
        |
        v
Layer 3
KNOWLEDGE GRAPH + REASONING
        |
        v
Layer 4
FUNCTIONAL DATA OVERREACH ANALYSIS
```

### Layer 1
Convert natural-language policies into structured candidate facts.

### Layer 2
Define a formal vocabulary and relationships.

### Layer 3
Represent and reason over the knowledge.

### Layer 4
Use the knowledge to detect functional mismatch and explain results.

---

# 40. Dataset / Benchmark

A practical benchmark can contain applications from:
- Communication;
- Social Media;
- Navigation;
- Banking/Finance;
- Shopping;
- Healthcare;
- Streaming;
- Productivity;
- Games;
- Utilities.

For every application, record:

```text
Application
Category
Description
Functions
Privacy Policy
Extracted Data
Expected Data
Purposes
Recipients
Retention
User Rights
FDO Label
Justification Label
Evidence Clause
```

A manually reviewed subset should act as the ground-truth benchmark.

---

# 41. Evaluation Plan

## NLP evaluation
Measure:
- Precision;
- Recall;
- F1-score.

For:
- data extraction;
- purpose extraction;
- recipient extraction;
- processing classification.

## Ontology evaluation
Evaluate:
- consistency;
- coverage;
- competency questions;
- relationship correctness.

## FDO detection evaluation
Use manually labeled expected/declared data and FDO classifications.

Measure:
- Accuracy;
- Precision;
- Recall;
- F1-score.

## Reasoning evaluation
Test whether the reasoning layer correctly derives expected relationships and identifies ontology inconsistencies.

## Explainability evaluation
Evaluate whether users can understand:
- why data was considered unexpected;
- which policy evidence supports the result;
- how the reasoning reached the conclusion.

---

# 42. Development Roadmap

## Phase 1
Application and policy data model.

## Phase 2
Policy extraction and clause segmentation.

## Phase 3
NLP/AI extraction.

## Phase 4
Initial FDO OWL/RDF ontology.

## Phase 5
Expected-data/function ontology.

## Phase 6
RDF knowledge graph and SPARQL queries.

## Phase 7
Neo4j graph visualization/storage where required.

## Phase 8
Reasoning using Apache Jena and evaluation of HermiT/Pellet where needed.

## Phase 9
FDO detection and policy justification.

## Phase 10
Explainable dashboard and comparison.

## Phase 11
Benchmark evaluation and research analysis.

---

# 43. Recommended Minimum Viable Research System

If implementation time is limited, prioritize:

```text
Privacy Policy
      |
      v
NLP / LLM Extraction
      |
      v
FDO OWL/RDF Ontology
      |
      v
Expected Data Mapping
      |
      v
Knowledge Graph
      |
      v
SPARQL
      |
      v
FDO Detection
      |
      v
Explainable Report
```

Advanced Neo4j visualization, advanced reasoning, and comparison can be added after the core semantic pipeline works.

The core research contribution should not be sacrificed merely to include more technologies.

---

# 44. One-Line Explanation

> **FDO Privacy converts natural-language privacy policies into machine-readable semantic knowledge and uses application functionality, ontology relationships, graph queries, and reasoning to analyze whether data practices match their functional purpose and to explain potential Functional Data Overreach.**

---

# 45. One-Minute Viva Explanation

> "Our project addresses the problem that privacy information is usually available as long natural-language policies. These policies are difficult not only for users to understand but also for machines to interpret and reason about.
>
> We propose a Functional Data Ontology, or FDO, to represent privacy information in a structured form. We use NLP and an AI API to extract information such as what data is collected, why it is collected, how it is processed, who it is shared with, how long it is retained, and what rights the user has.
>
> At the same time, we analyze the application's functionality to determine what data is reasonably expected for that functionality. We represent both functional requirements and privacy-policy information using OWL/RDF and a knowledge graph.
>
> Using SPARQL and reasoning, we can query and derive relationships from this knowledge. This enables Functional Data Overreach analysis by comparing expected data with declared data and then checking whether unexpected collection is justified or disclosed.
>
> Finally, the system provides an explainable report showing the data involved, its purpose, relevant policy evidence, detected mismatch, and reasoning behind the result.
>
> So our project is not simply a privacy-policy summarizer. The main idea is to convert privacy information from unstructured text into structured semantic knowledge that both humans and machines can understand, query, compare, and reason about."

---

# 46. Final Concept

```text
                    PRIVACY POLICY
                          |
                          v
                  NATURAL LANGUAGE
                          |
                          v
                    NLP + AI API
                          |
                          v
                  PRIVACY FACTS
                          |
                          v
                FDO ONTOLOGY
                  OWL + RDF
                          |
                          v
                KNOWLEDGE GRAPH
                Neo4j / RDF Store
                          |
              +-----------+-----------+
              |                       |
              v                       v
          SPARQL                 REASONING
              |                       |
              +-----------+-----------+
                          |
                          v
             FUNCTIONAL ANALYSIS
                          |
              +-----------+-----------+
              |                       |
              v                       v
       EXPECTED DATA            DECLARED DATA
              |                       |
              +-----------+-----------+
                          |
                          v
                  FDO DETECTION
                          |
                          v
              POLICY JUSTIFICATION
                          |
                          v
                EXPLAINABLE RESULT
                          |
                          v
                USER UNDERSTANDING
```

## Central message

> **Privacy information should not remain trapped inside lengthy natural-language documents. FDO Privacy converts that information into structured semantic knowledge, connects it with application functionality, and enables automated querying, reasoning, functional overreach detection, visualization, comparison, and explainable privacy analysis.**


---

# Part IV — Consolidated Gap Analysis and Remaining Work


# Master Gap & Remaining-Work Assessment

## Current reality

The supplied status document says the research package (Stages 1–7) is complete and the Stage 8 core backend is operational. The original idea, however, describes a broader semantic system involving OWL/RDF, a knowledge graph, SPARQL, reasoning, policy acquisition from PDF/URL, richer NLP, function extraction, a dashboard, comparison, and risk analysis.

Therefore, the project is **not finished overall**. The current implementation is the working backend foundation for the larger target system.

## Completed / operational

- Research design and literature foundation.
- Functional Data Ontology concept and expected-data baseline.
- Stage 3 privacy-policy evidence dataset and QA.
- Stage 4 manual FDO adjudication.
- Stage 5 benchmark.
- Stage 6 visualization/findings.
- Stage 7 final research report.
- Python backend.
- FastAPI.
- Uvicorn development server.
- SQLAlchemy.
- SQLite.
- Pydantic/Pydantic Settings.
- Application/function/expected-mapping database models.
- Policy and evidence persistence.
- Analysis pipeline.
- Exact canonical evidence matching.
- Deterministic FDO decision engine.
- Explanation persistence.
- Standard/rich reporting.
- Google Gemini extraction.
- Runtime AI policy/evidence ingestion.
- Canonical `DATA.*` data-type normalization.
- Live AI → database → FDO end-to-end validation.

## Remaining / not yet implemented in the current code

### A. Semantic ontology implementation
- Formal OWL ontology file.
- Formal RDF vocabulary/triples.
- Ontology constraints/restrictions.
- Machine-readable ontology versioning.
- Ontology validation/consistency checks.

### B. Semantic graph layer
- RDF graph/store.
- Knowledge-graph persistence.
- Neo4j integration if retained in the final design.
- Canonical-source-of-truth decision between RDF and Neo4j.
- Graph traversal/visualization.

### C. SPARQL
- Fuseki or another RDF/SPARQL server.
- Competency queries.
- Expected-vs-declared semantic queries.
- Queries for purpose, recipient, retention, rights, and sharing relationships.

### D. Reasoning
- Explicit semantic reasoning rules.
- Apache Jena reasoning and/or HermiT/Pellet evaluation.
- Derived-knowledge pipeline.
- Ontology consistency testing.
- Integration of reasoning results with FDO analysis.

### E. Policy acquisition
- PDF ingestion.
- URL retrieval.
- Robust document/text extraction.
- Section and heading extraction.
- Clause segmentation.
- Provenance preservation for externally retrieved policies.

### F. NLP / AI expansion
- More complete privacy-fact extraction.
- Processing-activity extraction.
- Recipient extraction.
- Retention extraction.
- Consent extraction.
- User-right extraction.
- Function extraction from application descriptions.
- Stronger validation of structured AI output.
- Retry/backoff/rate-limit handling.
- Broader AI regression tests.

### G. Purpose compatibility
The current backend has a working comparison layer, but semantic purpose matching is still an identified improvement area.

Needed:
- controlled purpose vocabulary and/or semantic similarity;
- compatible/incompatible/ambiguous handling;
- auditable evidence for the compatibility result;
- regression tests for semantically equivalent wording.

### H. Benchmark evaluation
Run the automated prototype against the 27-app analytical cohort and compare predictions with the manually adjudicated benchmark.

Measure:
- accuracy;
- precision;
- recall;
- F1;
- agreement;
- error categories;
- AI extraction errors versus decision-engine errors.

### I. Frontend
Build the intended user-facing dashboard:
- application selection;
- policy text/PDF/URL input;
- analysis trigger;
- extraction view;
- expected-vs-declared data view;
- FDO result view;
- evidence/explanation view;
- data-flow visualization;
- application comparison;
- report/export UI.

### J. Risk scoring and comparison
Implement these only after the semantic core is stable:
- explainable risk indicators;
- cross-application semantic comparison;
- privacy-attribute comparison;
- data-sharing/retention/user-right comparisons.

### K. Productionization
Later:
- PostgreSQL;
- Docker;
- deployment;
- API security;
- rate limiting;
- monitoring;
- logging;
- background jobs;
- production configuration.

## Recommended order

```text
Current working backend
        ↓
Regression and failure testing
        ↓
Semantic purpose compatibility
        ↓
Formal FDO OWL ontology
        ↓
RDF representation
        ↓
SPARQL / Fuseki
        ↓
Reasoning
        ↓
Integrate semantic results with FDO engine
        ↓
27-app benchmark evaluation
        ↓
Frontend
        ↓
Graph visualization / Neo4j if justified
        ↓
Production deployment
```

## Important scope warning

Do not claim that Neo4j, RDF, OWL, SPARQL, Fuseki, HermiT, or Pellet are already implemented merely because they occur in the original project idea. The supplied status material explicitly treats these as planned/not currently implemented.

Do not replace the current deterministic FDO adjudication with an LLM. The current project's strongest architectural boundary is:

```text
AI = evidence extraction
Deterministic rules = FDO adjudication
```

## Final position

The project currently has a functioning and validated Stage 8 backend core. The next major architectural milestone is to turn the current structured relational evidence pipeline into the semantic OWL/RDF + graph + SPARQL + reasoning system described by the original idea, then evaluate that complete system against the research benchmark and expose it through a user-facing dashboard.

