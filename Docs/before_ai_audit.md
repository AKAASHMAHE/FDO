# FDO-Privacy Project — Pre-AI Audit

**Document:** `before_ai_audit.md`  
**Purpose:** Complete project baseline before integrating Gemini AI into the live backend pipeline.  
**Status:** Backend architecture and deterministic analysis pipeline implemented and verified; AI extraction component tested independently; full AI-to-database integration is the next major step.

---

## 1. Executive Summary

The FDO-Privacy project has two connected layers:

1. **Research / benchmark layer — Stages 1–7**
   - Defines the privacy-analysis problem.
   - Builds the expected-data ontology and application/function mappings.
   - Collects and annotates privacy-policy evidence.
   - Performs FDO adjudication.
   - Produces the research benchmark, findings, visualizations, and report.

2. **Software / productization layer — Stage 8**
   - Converts the research methodology into a reusable backend system.
   - Accepts an application and privacy-policy information.
   - Extracts and structures policy evidence.
   - Normalizes evidence.
   - Compares declared evidence against expected data mappings.
   - Applies deterministic FDO decision rules.
   - Stores explanations and results.
   - Exposes the pipeline through a FastAPI REST API.
   - Will eventually be connected to a frontend.

### Current implementation principle

**AI extracts evidence. Deterministic rules make the FDO decision.**

Gemini is not supposed to decide whether data is FDO, NOT_FDO, or AMBIGUOUS. The AI layer is responsible for extracting structured, policy-supported evidence. The deterministic FDO engine remains the decision authority.

---

# 2. Project Goal

The core objective is to determine whether data collected/declared by an application is functionally necessary for the application's stated function and purpose.

The project does **not** use simplistic rules such as:

- "The app collects it, therefore it is FDO."
- "The data is optional, therefore it is not FDO."
- "The data is unexpected, therefore it is FDO."

Instead, the analysis is function-specific and evidence-driven.

The conceptual chain is:

**Application → Category → Function → Feature → Data Type → Necessity → Purpose → Policy Evidence → Comparison → FDO Decision → Explanation**

Functional specificity is important because the same data type may be necessary for one function but unnecessary for another.

---

# 3. Research Stages Completed

## Stage 1 — Research Scope & Design

Completed as the research foundation.

Covered:

- Problem definition
- Research questions
- Research scope
- Methodology
- Application analysis framework
- FDO analysis concept

---

## Stage 2 — Expected Data Baseline / Ontology

Completed.

The expected-data model establishes what data is expected for application functions.

Important hierarchy:

- Application
- Category
- Function
- Feature
- Data Type
- Necessity
- Expected Purpose

The **function** is the main unit for necessity analysis.

The dataset contains:

- Applications
- Functions
- Expected data mappings
- Necessity
- Expected purpose

### Research pilot

- 30 original pilot applications
- 4 annotation batches
- Functional/application mappings created

---

## Stage 3 — Privacy Policy Evidence Annotation & QA

Completed.

Privacy-policy evidence was collected/annotated with provenance.

The analytical cohort was frozen at:

- **27 analytical applications**
- 3 policy exceptions

Policy exceptions:

- Instagram
- PUBG MOBILE
- WeChat

Evidence is represented with information such as:

- Data type
- Purpose
- Entity
- Sharing
- Retention
- Evidence text
- Source section
- Extraction status
- Confidence

---

## Stage 4 — FDO Analysis / Adjudication

Completed as the research analysis layer.

Sub-stages:

- 4A — Necessity
- 4B — Purpose Compatibility
- 4C — Candidate Screening
- 4D — Detailed Adjudication
- 4E — Ambiguous Resolution

The analysis considers:

1. Data match
2. Purpose compatibility
3. Functional relationship
4. Evidence availability/status

---

## Stage 5 — Final Mapping-Level Dataset / Statistics

Completed as the research benchmark layer.

Current benchmark documented by the research package:

| Metric | Benchmark |
|---|---:|
| Original pilot applications | 30 |
| Analytical applications | 27 |
| Expected mappings | 99 |
| Evidence-backed mappings | 93 |
| NOT_FDO | 60 |
| AMBIGUOUS | 33 |
| Established FDO | 0 |

These are **research benchmark values**, not values that should be hard-coded into the software.

---

## Stage 6 — Visualization / Findings

Completed in the research package.

The stage covers the analysis findings and visual representation of the research results.

---

## Stage 7 — Final Research Report Package

Completed as the research/reporting layer.

This provides the research context that the Stage 8 software implementation is based on.

---

# 4. Stage 8 — Software Architecture

Stage 8 turns the research methodology into a reusable software pipeline.

## High-Level Architecture

```text
                    USER / FRONTEND
                          |
                          v
                    FASTAPI API
                          |
              +-----------+-----------+
              |                       |
              v                       v
       Application Context       Policy Input
              |                       |
              |                       v
              |                Policy Processor
              |                       |
              |                       v
              |                  GEMINI AI
              |                       |
              |                       v
              |              Structured Evidence
              |                       |
              +-----------+-----------+
                          |
                          v
                Evidence Normalization
                          |
                          v
              Expected Data / Policy Evidence
                          |
                          v
              Functional Comparison Engine
                          |
                          v
               Deterministic FDO Engine
                          |
              +-----------+-----------+
              |           |           |
              v           v           v
            FDO        NOT_FDO     AMBIGUOUS
              |           |           |
              +-----------+-----------+
                          |
                          v
                    Explanation
                          |
                          v
                 Persisted Results
                          |
                          v
                    REST API Report
                          |
                          v
                    FRONTEND / UI
```

---

# 5. Current Technology Stack

## Backend

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **SQLite**
- **Uvicorn** / FastAPI development server

## AI

- **Google Gemini API**
- Current tested model:
  - `gemini-3.5-flash-lite`

The project is intentionally using a **free-tier API approach**. Free-tier quotas/rate limits can change, so the implementation must handle AI failures gracefully.

## Environment

- Python virtual environment:
  - `Backend\.venv`
- Environment variables:
  - `.env`
- Gemini API key:
  - `GEMINI_API_KEY`

The API key must never be committed to Git or exposed in documentation.

## Future / optional technologies

These are architectural possibilities, not current implemented dependencies:

- React / Next.js frontend
- PostgreSQL for production
- Neo4j / graph layer if a graph representation is later justified

The current working database is SQLite.

---

# 6. Current Backend Folder Structure

```text
Backend/
│
├── .env
├── .gitignore
├── fdo_privacy.db
├── requirements.txt
│
├── app/
│   ├── config.py
│   ├── database.py
│   ├── init_db.py
│   ├── main.py
│   │
│   ├── models/
│   │   ├── analysis.py
│   │   ├── application.py
│   │   ├── base.py
│   │   ├── comparison.py
│   │   ├── expected_mapping.py
│   │   ├── explanation.py
│   │   ├── fdo_result.py
│   │   ├── function.py
│   │   ├── normalized_evidence.py
│   │   ├── policy_document.py
│   │   └── policy_evidence.py
│   │
│   ├── schemas/
│   │   ├── analysis.py
│   │   ├── analysis_result.py
│   │   ├── policy_extraction.py
│   │   └── rich_report.py
│   │
│   └── services/
│       ├── ai_service.py
│       ├── analysis_report_service.py
│       ├── analysis_result_service.py
│       ├── analysis_runner.py
│       ├── analysis_service.py
│       ├── application_service.py
│       ├── comparison_persistence_service.py
│       ├── comparison_service.py
│       ├── evidence_matcher.py
│       ├── evidence_service.py
│       ├── expected_mapping_service.py
│       ├── explanation_service.py
│       ├── fdo_decision_service.py
│       ├── function_service.py
│       ├── policy_extraction_service.py
│       ├── policy_service.py
│       ├── result_service.py
│       └── rich_report_service.py
│
├── scripts/
│   ├── import_stage3.py
│   ├── persist_fdo_test.py
│   ├── test_failure_path.py
│   ├── validate_multi_app.py
│   └── verify_fdo_decision.py
│
└── DATA/
    └── FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx
```

---

# 7. Database

## Current Database

```text
SQLite
fdo_privacy.db
```

Connection currently uses:

```text
sqlite:///./fdo_privacy.db
```

The database currently contains **10 tables**.

---

# 8. Database Schema

## 8.1 applications

Stores application-level information.

```text
applications
-----------------------------
application_id       PK
application_name
category
description
```

Relationships:

```text
Application
   |
   +---- Functions
   |
   +---- Expected Mappings
   |
   +---- Policy Documents
```

---

## 8.2 functions

Stores functional information for an application.

```text
functions
-----------------------------
function_record_id   PK
function_id
application_id       FK
function_name
feature
description
```

A function belongs to an application.

The project uses functions as an important unit for expected-data analysis.

---

## 8.3 expected_mappings

Stores expected data for a function.

```text
expected_mappings
-----------------------------
expected_id          PK
application_id       FK
function_record_id   FK
data_type
necessity
expected_purpose
source_version
```

This represents the expected side of the comparison.

---

## 8.4 policy_documents

Stores the application's privacy policy/document.

Conceptually:

```text
Application
     |
     v
Policy Document
     |
     v
Policy Evidence
```

The policy document acts as the parent/source for extracted evidence.

---

## 8.5 policy_evidence

Stores structured evidence extracted from policy text.

```text
policy_evidence
-----------------------------
evidence_id          PK
policy_id            FK
data_type
purpose
entity
sharing
retention
evidence_text
source_section
extraction_status
confidence
```

This is one of the most important tables for AI integration.

---

## 8.6 normalized_evidence

Stores normalized representations of raw policy evidence.

```text
normalized_evidence
-----------------------------
normalized_id        PK
evidence_id          FK
normalized_data_type
normalized_purpose
normalization_note
normalization_status
```

Purpose:

```text
Raw policy evidence
        |
        v
Normalization
        |
        v
Comparable representation
```

---

## 8.7 analyses

Stores an analysis execution.

Conceptually:

```text
Analysis
  |
  +--- Application
  +--- Policy
  +--- Comparisons
  +--- FDO Results
```

The analysis starts with a CREATED state and is updated as the analysis pipeline runs.

---

## 8.8 comparisons

Stores comparison-level results between expected mappings and available evidence.

Current response-level comparison fields include:

```text
comparison_id
analysis_id
expected_id
evidence_id
data_match
purpose_compatibility
functional_relationship
functional_justification
evidence_status
```

This is the bridge between:

**Expected data ↔ Policy evidence**

---

## 8.9 fdo_results

Stores the deterministic FDO decision.

```text
fdo_results
-----------------------------
result_id
comparison_id
fdo_status
decision_reason
decision_confidence
created_at
```

Possible status values include:

```text
FDO
NOT_FDO
AMBIGUOUS
```

The FDO result is generated by deterministic project rules, not directly by Gemini.

---

## 8.10 explanations

Stores the explanation associated with an FDO result.

```text
explanations
-----------------------------
explanation_id
result_id
explanation_text
evidence_summary
limitations
created_at
```

This provides an auditable reason for the final result.

---

# 9. Data Flow

## Existing / Target Complete Flow

```text
1. Application selected
        |
        v
2. Application context loaded
        |
        +--> category
        +--> functions
        +--> features
        +--> expected mappings
        |
        v
3. Privacy policy supplied
        |
        v
4. Policy document stored
        |
        v
5. Gemini extracts explicit policy evidence
        |
        v
6. AI output validated
        |
        v
7. Policy evidence persisted
        |
        v
8. Evidence normalized
        |
        v
9. Expected mappings loaded
        |
        v
10. Evidence matched to expected mappings
        |
        v
11. Comparison generated
        |
        +--> data match
        +--> purpose compatibility
        +--> functional relationship
        +--> evidence status
        |
        v
12. Deterministic FDO decision
        |
        +--> FDO
        +--> NOT_FDO
        +--> AMBIGUOUS
        |
        v
13. Explanation generated/stored
        |
        v
14. Analysis/report persisted
        |
        v
15. API returns frontend-ready report
```

---

# 10. API Layer

Base path:

```text
/api/v1
```

Current routes:

## Health

```http
GET /api/v1/health
```

Verified:

```json
{
  "status": "ok",
  "service": "fdo-privacy-backend"
}
```

---

## Applications

```http
GET /api/v1/applications
GET /api/v1/applications/{application_id}
GET /api/v1/applications/{application_id}/readiness
GET /api/v1/applications/{application_id}/expected-mappings
```

These provide application context, readiness and expected mappings.

---

## Policy extraction

```http
POST /api/v1/extract-policy
```

This endpoint is intended to transform privacy-policy text into structured evidence.

Current AI extraction component has been tested separately.

---

## Analysis creation

```http
POST /api/v1/analyses
```

Creates/runs analysis using a stored application context.

---

## Direct analysis

```http
POST /api/v1/analyze
```

Accepts application/policy information for analysis.

---

## Analysis retrieval

```http
GET /api/v1/analyses/{analysis_id}
GET /api/v1/analysis/{analysis_id}
```

Both valid and invalid analysis retrieval paths have been tested.

---

## Analysis results

```http
GET /api/v1/analyses/{analysis_id}/results
```

Returns detailed mapping-level analysis results.

---

## Analysis report

```http
GET /api/v1/analysis/{analysis_id}/report
```

The current implementation returns a frontend-ready rich report.

The report contains:

```text
Application
Analysis status
Summary
Results
Function
Expected data
Declared data
Necessity
Expected purpose
Declared purpose
Data match
Purpose compatibility
Functional relationship
Functional justification
Evidence
Explanation
Decision confidence
FDO status
```

---

# 11. Deterministic FDO Decision Engine

The decision engine is implemented in:

```text
app/services/fdo_decision_service.py
```

Current decision logic:

### Case 1 — No evidence

```text
No evidence
    ↓
AMBIGUOUS
confidence = 0.30
```

Reason:

Missing evidence is not proof that data is not collected.

---

### Case 2 — Insufficient / unknown evidence

```text
INSUFFICIENT / UNKNOWN
    ↓
AMBIGUOUS
confidence = 0.40
```

---

### Case 3 — Evidence extraction not completed

```text
non-EXTRACTED
    ↓
AMBIGUOUS
confidence = 0.40
```

---

### Case 4 — Exact match + compatible purpose + related function

```text
EXACT_MATCH
+
COMPATIBLE
+
RELATED
        ↓
NOT_FDO
confidence = 0.90
```

---

### Case 5 — Exact match + incompatible purpose + related function

```text
EXACT_MATCH
+
INCOMPATIBLE
+
RELATED
        ↓
FDO
confidence = 0.85
```

---

### Case 6 — No exact data match but functionally related

```text
NO_MATCH
+
RELATED
        ↓
FDO
confidence = 0.80
```

---

### Fallback

```text
Anything unresolved
        ↓
AMBIGUOUS
confidence = 0.50
```

This keeps uncertainty explicit instead of forcing a binary answer.

---

# 12. Explanation Layer

The project does not stop at:

```text
FDO = YES
```

Every result should be explainable.

The explanation layer stores:

- Decision reason
- Evidence summary
- Limitations
- Explanation text

The current runner persists an explanation after creating the FDO result.

Verified behavior:

```text
Analysis
   ↓
Comparison
   ↓
FDO Result
   ↓
Explanation
```

---

# 13. AI Layer — Current Status

## Gemini API setup

Completed.

The project uses:

```text
Google Gemini API
```

Current tested model:

```text
gemini-3.5-flash-lite
```

A Gemini API key has been configured through:

```text
.env
```

with:

```text
GEMINI_API_KEY=...
```

The actual key must remain private.

---

## Independent Gemini test

Completed successfully.

Gemini successfully extracted:

```text
LOCATION.PRECISE
```

with a purpose related to:

```text
directions and nearby search
```

It also returned:

- entity
- evidence text
- confidence

This proves that the API key, SDK, model access and basic extraction prompt work.

---

# 14. AI Service

Current file:

```text
app/services/ai_service.py
```

The AI service is responsible for:

1. Loading the Gemini API key.
2. Sending policy text to Gemini.
3. Asking Gemini for structured evidence.
4. Requesting JSON output.
5. Returning evidence fields such as:
   - data_type
   - purpose
   - entity
   - sharing
   - retention
   - evidence_text
   - source_section
   - extraction_status
   - confidence

The prompt explicitly tells Gemini:

- Extract only information supported by the policy.
- Do not infer unsupported data.
- Do not decide FDO status.
- Return structured evidence.
- Do not invent a data type when evidence is insufficient.

---

# 15. Critical AI Boundary

This boundary must remain fixed unless the research methodology is intentionally changed.

```text
                 GEMINI AI
                    |
                    v
         Policy Evidence Extraction
                    |
                    v
          Structured Evidence
                    |
                    X
             NO FDO DECISION
                    |
                    v
       Deterministic Rule Engine
                    |
          +---------+---------+
          |         |         |
          v         v         v
         FDO     NOT_FDO   AMBIGUOUS
```

### AI is allowed to:

- Read policy text.
- Identify explicit data collection statements.
- Identify stated purposes.
- Identify entities.
- Identify sharing/retention statements.
- Provide confidence.
- Structure evidence.

### AI must not:

- Decide FDO by itself.
- Invent evidence.
- Treat missing evidence as non-collection.
- Override deterministic research rules.
- Change expected-data mappings.
- Manufacture functional necessity.

---

# 16. What Has Already Been Verified

## Database

Verified:

```text
Database OK: sqlite:///./fdo_privacy.db
Table count: 10
```

All 10 expected tables exist.

---

## Application data

Verified:

- 30 applications exist.
- Each of the 30 applications has exactly one policy.

---

## Readiness

Examples verified:

```text
NAV-01
policy_count = 1
evidence_count = 3
ready = true
```

```text
COM-01
policy_count = 1
evidence_count = 0
ready = false
```

This proves the system can distinguish analysis-ready and evidence-incomplete applications.

---

# 17. Failure Path Verification

An invalid application was tested.

Expected:

```text
ValueError
```

Observed:

```text
Application not found: INVALID-APP
```

Database integrity check:

```text
Analysis records after failure: 0
```

This proves the failure path does not incorrectly create an analysis record.

---

# 18. Multi-Application Verification

The analysis pipeline has been tested across multiple applications.

Verified examples:

### AMB-01

```text
Status: COMPLETED
Total: 5
FDO: 3
NOT_FDO: 0
AMBIGUOUS: 2
Counter: true
```

### EDU-02

```text
Status: COMPLETED
Total: 2
FDO: 0
NOT_FDO: 0
AMBIGUOUS: 2
Counter: true
```

### FIT-01

```text
Status: COMPLETED
Total: 4
FDO: 1
NOT_FDO: 0
AMBIGUOUS: 3
Counter: true
```

### FOD-01

```text
Status: COMPLETED
Total: 4
FDO: 0
NOT_FDO: 0
AMBIGUOUS: 4
Counter: true
```

This confirms that the analysis counter remains consistent across different applications.

---

# 19. Rich Report Verification

A complete report was successfully produced for:

```text
ANALYSIS-NAV-01-67bfa44f
```

Verified:

- 3 results
- all FDO
- evidence available
- explanations present
- application information
- function information
- expected data
- declared data
- decision fields

The rich report is intended to be directly usable by a frontend.

---

# 20. API Verification Status

The following have been tested successfully:

- Health endpoint
- Application list
- Application detail
- Expected mappings
- Application readiness
- Policy extraction success path
- Policy extraction empty-input failure path
- Analysis creation
- Analysis retrieval
- Results retrieval
- Rich report retrieval
- Invalid application path
- Invalid analysis path
- Invalid results path
- Invalid report path

---

# 21. Evidence Availability Reality

The current database intentionally contains different evidence levels.

Examples:

```text
AMB-01  -> 2 evidence records
AMB-02  -> 1
COM-01  -> 0
COM-02  -> 0
ECO-01  -> 0
ECO-02  -> 0
EDU-01  -> 0
EDU-02  -> 1
FIN-01  -> 0
FIN-02  -> 0
FIT-01  -> 5
FIT-02  -> 3
FOD-01  -> 2
FOD-02  -> 1
GAM-01  -> 2
GAM-02  -> 1
HEA-01  -> 0
HEA-02  -> 2
NAV-01  -> 3
NAV-02  -> 0
PRO-01  -> 1
PRO-02  -> 1
SOC-01  -> 1
SOC-02  -> 0
STR-01  -> 1
STR-02  -> 0
TRV-01  -> 1
TRV-02  -> 1
UTL-01  -> 1
UTL-02  -> 4
```

This variation is useful for testing:

- Successful evidence extraction
- Missing evidence
- Ambiguity
- Partial evidence
- FDO decisions

---

# 22. Important Ambiguous Cases

Known expected mappings without matching evidence include examples such as:

### AMB-01

```text
EXP-092
DATA.CONTACT.EMAIL
Purpose: Recipient identification

EXP-093
DATA.DEVICE.STORAGE
Purpose: Backup/sync
```

Available evidence is instead related to:

```text
DATA.MEDIA.PHOTOS_VIDEOS
```

---

### EDU-02

```text
EXP-044
DATA.USAGE.LESSON_ACTIVITY

EXP-045
DATA.USAGE.PROGRESS_RECORDS
```

Available evidence:

```text
DATA.USAGE.ACTIVITY_LOGS
```

---

### FIT-01

Expected examples include:

```text
DATA.LOCATION.PRECISE
DATA.CONTACTS.LIST
DATA.USAGE.ACTIVITY_HISTORY
```

Available evidence includes:

```text
DATA.ACCOUNT.PERSONAL_INFO
DATA.HEALTH.ACTIVITY
DATA.HEALTH.HEART_RATE
DATA.DEVICE.ID
DATA.FINANCIAL.PAYMENT
```

---

### FOD-01

Expected examples include:

```text
DATA.LOCATION.APPROXIMATE
DATA.CONTACT.ADDRESS
DATA.FINANCIAL.PAYMENT
DATA.LOCATION.PRECISE
```

Available evidence includes:

```text
DATA.ACCOUNT.PERSONAL_INFO
DATA.USAGE.TRIP_DETAILS
```

These cases are valuable for validating that the system does not automatically force every expected mapping into an FDO/non-FDO decision.

---

# 23. What Is NOT Yet Fully Integrated

The biggest current gap is:

```text
Gemini extraction
        ↓
LIVE policy extraction service
        ↓
evidence persistence
        ↓
normalization
        ↓
comparison
        ↓
FDO analysis
```

The Gemini component has been independently tested, but the complete AI-powered path still needs to be integrated and validated end-to-end.

This is the reason for this audit document.

---

# 24. Remaining Work — Exact Order

## Phase A — AI Integration

### A1. Inspect current policy extraction service

Verify exactly how:

```text
policy_extraction_service.py
```

currently works.

Do not overwrite working behavior blindly.

---

### A2. Connect Gemini to policy extraction

Target:

```text
POST /api/v1/extract-policy
```

Flow:

```text
Request
  ↓
Policy extraction service
  ↓
Gemini
  ↓
Structured evidence
  ↓
Validation
  ↓
Response
```

---

### A3. Preserve fallback behavior

If Gemini:

- fails
- times out
- returns invalid JSON
- exceeds quota
- is unavailable

the system should fail safely.

A deterministic extraction fallback can remain available where appropriate.

The final behavior must never silently manufacture evidence.

---

### A4. Validate AI output

Every AI response should be checked for:

- valid JSON
- correct top-level structure
- valid evidence list
- allowed data-type values
- valid confidence range
- non-empty evidence text where evidence is claimed
- no unsupported inference
- extraction status

---

# 25. Phase B — AI Evidence Persistence

After extraction:

```text
AI evidence
    ↓
PolicyEvidence
    ↓
Database
```

Every persisted evidence item needs:

- unique evidence ID
- policy ID
- evidence text
- structured data type
- purpose
- provenance/source section
- extraction status
- confidence

The original evidence text must remain available for auditability.

---

# 26. Phase C — Normalization

After raw evidence persistence:

```text
Policy Evidence
      ↓
Normalized Evidence
```

Normalization should map semantically similar policy language into the project's controlled data taxonomy without inventing facts.

Examples conceptually:

```text
"GPS location"
        ↓
LOCATION.PRECISE
```

or

```text
"approximate location"
        ↓
LOCATION.APPROXIMATE
```

Normalization should be separately testable from AI extraction.

---

# 27. Phase D — Evidence Matching

The matcher should connect:

```text
Expected Mapping
        ↕
Policy Evidence
```

using:

- data-type compatibility
- purpose compatibility
- functional relationship

The matcher must preserve evidence provenance.

---

# 28. Phase E — Complete AI-Powered Analysis

Target flow:

```text
Application
    ↓
Expected mappings
    ↓
Privacy policy
    ↓
Gemini
    ↓
Policy evidence
    ↓
Normalization
    ↓
Evidence matching
    ↓
Comparison
    ↓
Deterministic FDO engine
    ↓
Explanation
    ↓
Persisted analysis
    ↓
Rich report
```

This is the major milestone after the current audit.

---

# 29. Phase F — Test Matrix

The integrated system should be tested against at least these categories.

## Test 1 — Clear evidence

Policy explicitly says:

```text
precise location for navigation
```

Expected:

```text
AI extracts evidence
→ normalized evidence
→ comparison
→ deterministic decision
```

---

## Test 2 — No evidence

Policy does not mention the expected data.

Expected:

```text
AMBIGUOUS
```

Not:

```text
NOT_FDO
```

---

## Test 3 — Purpose mismatch

Policy explicitly states collection, but purpose is unrelated to the expected function.

Expected deterministic rules should evaluate compatibility and relationship.

---

## Test 4 — Ambiguous wording

Policy statement is insufficient to confidently identify the data.

Expected:

```text
AMBIGUOUS
```

---

## Test 5 — AI failure

Simulate:

- missing API key
- invalid API response
- quota/rate limit
- empty response

Expected:

```text
safe failure or controlled fallback
```

No corrupt FDO result should be created.

---

## Test 6 — Invalid application

Already tested successfully.

Must remain:

```text
404 / controlled error
```

with no incorrect analysis persistence.

---

# 30. Phase G — AI vs Existing Benchmark Comparison

Once the AI pipeline works:

Run the same applications through:

```text
Existing research evidence
```

and

```text
AI-extracted evidence
```

Compare:

- evidence extraction
- data-type mapping
- purpose mapping
- functional relationship
- FDO result
- ambiguity rate

Important:

The research benchmark remains the benchmark.

The AI system must be evaluated against it rather than changing the benchmark to fit AI output.

---

# 31. Phase H — Backend Lock

Before frontend work:

- Freeze database schema.
- Freeze API contracts.
- Freeze FDO decision logic.
- Freeze evidence fields.
- Freeze result statuses.
- Add error handling.
- Add logging.
- Add reproducibility information where useful.
- Ensure secrets are excluded from Git.
- Run all regression tests.

---

# 32. Phase I — Frontend

After backend stabilization:

```text
React / Next.js
        ↓
FastAPI
        ↓
FDO analysis backend
```

Potential screens:

1. Home / project introduction
2. Application selection
3. Privacy-policy input
4. Analysis processing
5. Analysis summary
6. Mapping-level results
7. Evidence viewer
8. FDO explanation
9. Ambiguous cases
10. Application history/report

Frontend should not duplicate FDO decision logic.

The backend remains the source of truth.

---

# 33. Phase J — Full-System Integration

Final application flow:

```text
USER
 |
 v
Select Application
 |
 v
Provide / Load Privacy Policy
 |
 v
Submit Analysis
 |
 v
FastAPI
 |
 v
Gemini Evidence Extraction
 |
 v
Evidence Validation
 |
 v
Normalization
 |
 v
Functional Matching
 |
 v
Deterministic FDO Decision
 |
 v
Explanation
 |
 v
Database
 |
 v
Report API
 |
 v
Frontend Dashboard
```

---

# 34. Security Requirements

The project must protect:

### API key

```text
GEMINI_API_KEY
```

Must remain in `.env`.

`.env` must remain in `.gitignore`.

### Privacy policy text

Treat policy input as application data.

Do not log sensitive raw content unnecessarily.

### AI output

Never trust model output directly.

Always validate before persistence.

### FDO decision

Never allow arbitrary AI output to directly become:

```text
FDO
NOT_FDO
AMBIGUOUS
```

The deterministic decision layer should remain authoritative.

---

# 35. Error-Handling Architecture

Recommended structure:

```text
AI unavailable
      ↓
Controlled error / fallback
      ↓
No fabricated evidence
      ↓
Analysis either:
   - safely continues with known evidence, or
   - returns controlled failure
```

Database transaction behavior should ensure partially failed analyses do not leave misleading records.

The already-tested failure path is a baseline that must continue passing.

---

# 36. Reproducibility / Auditability

Each analysis should be traceable through:

```text
Analysis ID
    ↓
Application
    ↓
Policy
    ↓
Evidence ID
    ↓
Expected Mapping ID
    ↓
Comparison ID
    ↓
FDO Result ID
    ↓
Explanation ID
```

This is essential for research defensibility.

A final FDO result should be explainable back to the underlying evidence and expected mapping.

---

# 37. Important Design Rules

These rules should not be violated accidentally during implementation.

### Rule 1

**Declared data ≠ automatically FDO.**

### Rule 2

**Optional/context-dependent data ≠ automatically FDO.**

### Rule 3

**Unexpected data ≠ automatically FDO.**

### Rule 4

**Missing evidence ≠ proof of non-collection.**

### Rule 5

**Function matters more than broad application category.**

### Rule 6

**AI extracts evidence; deterministic logic decides FDO.**

### Rule 7

**Ambiguity must remain visible.**

### Rule 8

**Research benchmark values must not be hard-coded as software outputs.**

### Rule 9

**Every decision should be traceable to comparison and evidence.**

### Rule 10

**AI output must be validated before entering the database.**

---

# 38. Current Status Snapshot

```text
RESEARCH
--------------------------------
Stage 1  ██████████  COMPLETE
Stage 2  ██████████  COMPLETE
Stage 3  ██████████  COMPLETE
Stage 4  ██████████  COMPLETE
Stage 5  ██████████  COMPLETE
Stage 6  ██████████  COMPLETE
Stage 7  ██████████  COMPLETE


BACKEND / STAGE 8
--------------------------------
Database                  COMPLETE
Models                    COMPLETE
Services                  COMPLETE
Expected mappings         COMPLETE
Evidence storage          COMPLETE
Deterministic FDO engine  COMPLETE
Explanation storage       COMPLETE
Rich report               COMPLETE
API                       COMPLETE
Failure-path testing      COMPLETE
Multi-app testing         COMPLETE

AI
--------------------------------
Gemini account/key        COMPLETE
Gemini model access       COMPLETE
Independent extraction    COMPLETE
AI service                IMPLEMENTED
Live pipeline integration NEXT
AI validation             NEXT
AI persistence validation NEXT
AI end-to-end testing     NEXT

FRONTEND
--------------------------------
Frontend                  NOT STARTED
Backend/frontend wiring   NOT STARTED
Dashboard                 NOT STARTED
```

---

# 39. Where We Are Right Now

The project is **not at the beginning**.

The research foundation is complete through Stage 7.

The backend already has:

- database
- models
- services
- expected-data mappings
- policy evidence
- comparison engine
- deterministic FDO decision engine
- explanations
- rich reports
- REST APIs
- error handling
- multi-application tests

Gemini API access is also proven independently.

Therefore, the next task is **not** to redesign the project.

The next task is:

> **Integrate the already-tested Gemini extraction component into the existing policy-extraction → evidence → normalization → comparison → deterministic FDO → explanation → report pipeline, without breaking the verified backend behavior.**

---

# 40. Immediate Next Step

Before editing code:

1. Inspect the actual current `app/services/ai_service.py`.
2. Inspect the actual current `app/services/policy_extraction_service.py`.
3. Inspect the actual `/api/v1/extract-policy` implementation in `app/main.py`.
4. Identify whether JSON-fence handling is already present.
5. Identify the current deterministic extraction/fallback path.
6. Integrate Gemini with the smallest safe change.
7. Run:
   - compile test
   - extraction endpoint test
   - persistence test
   - full analysis test
   - failure-path test
   - ambiguous/no-evidence test
8. Compare AI-backed results with the existing verified deterministic behavior.
9. Only after all backend tests pass, proceed toward frontend.

---

# 41. Final Architecture — Target State

```text
┌──────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│              React / Next.js (future)                        │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             v
┌──────────────────────────────────────────────────────────────┐
│                         FASTAPI                              │
│                       /api/v1                                │
└────────────────────────────┬─────────────────────────────────┘
                             │
             ┌───────────────┴────────────────┐
             │                                │
             v                                v
┌──────────────────────────┐      ┌───────────────────────────┐
│ Application Context      │      │ Privacy Policy Input      │
│                          │      │                           │
│ Application              │      │ Raw Policy Text           │
│ Category                 │      └─────────────┬─────────────┘
│ Functions                │                    │
│ Features                │                    v
│ Expected Mappings        │      ┌───────────────────────────┐
└─────────────┬────────────┘      │       Gemini AI           │
              │                   │ Evidence Extraction       │
              │                   └─────────────┬─────────────┘
              │                                 │
              │                                 v
              │                   ┌───────────────────────────┐
              │                   │ AI Output Validation       │
              │                   └─────────────┬─────────────┘
              │                                 │
              └────────────────┬────────────────┘
                               v
                 ┌─────────────────────────────┐
                 │     Policy Evidence         │
                 │                             │
                 │ Data Type                   │
                 │ Purpose                     │
                 │ Entity                      │
                 │ Sharing                     │
                 │ Retention                   │
                 │ Evidence Text               │
                 │ Source Section              │
                 │ Confidence                  │
                 └──────────────┬──────────────┘
                                │
                                v
                 ┌─────────────────────────────┐
                 │ Evidence Normalization      │
                 └──────────────┬──────────────┘
                                │
                                v
                 ┌─────────────────────────────┐
                 │ Functional Evidence Matcher │
                 └──────────────┬──────────────┘
                                │
                                v
                 ┌─────────────────────────────┐
                 │ Functional Comparison       │
                 │                             │
                 │ Data Match                  │
                 │ Purpose Compatibility       │
                 │ Functional Relationship     │
                 │ Evidence Status             │
                 └──────────────┬──────────────┘
                                │
                                v
                 ┌─────────────────────────────┐
                 │ Deterministic FDO Engine    │
                 │                             │
                 │ FDO / NOT_FDO / AMBIGUOUS   │
                 └──────────────┬──────────────┘
                                │
                                v
                 ┌─────────────────────────────┐
                 │ Explanation Service         │
                 └──────────────┬──────────────┘
                                │
                                v
                 ┌─────────────────────────────┐
                 │         SQLite DB           │
                 │                             │
                 │ Applications                │
                 │ Functions                   │
                 │ Expected Mappings           │
                 │ Policy Documents            │
                 │ Policy Evidence             │
                 │ Normalized Evidence         │
                 │ Analyses                    │
                 │ Comparisons                 │
                 │ FDO Results                 │
                 │ Explanations                │
                 └──────────────┬──────────────┘
                                │
                                v
                 ┌─────────────────────────────┐
                 │ Rich Report / REST API      │
                 └─────────────────────────────┘
```

---

# 42. One-Line Project Definition

> **FDO-Privacy is an evidence-driven, function-aware privacy analysis system that uses Gemini to extract explicit privacy-policy evidence and deterministic research rules to determine FDO, NOT_FDO, or AMBIGUOUS outcomes with traceable explanations.**

---

## Audit Conclusion

**Before AI integration, the project has a functioning research foundation and a substantially implemented backend.**

The critical remaining backend milestone is not AI experimentation itself; Gemini access has already been proven.

The critical milestone is **safe integration of AI evidence extraction into the existing verified pipeline while preserving deterministic FDO logic, provenance, ambiguity handling, database integrity, and reproducibility.**

After that:

```text
AI integration
    ↓
End-to-end backend validation
    ↓
Backend freeze
    ↓
Frontend
    ↓
Full integration
    ↓
Evaluation against research benchmark
    ↓
Final testing/demo
    ↓
Final project/report
```
