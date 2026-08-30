# FDO-Privacy --- Stage 8 Master Architecture Document

**Version:** 1.0\
**Stage:** 8.1K --- Master Architecture\
**Project:** FDO-Privacy

------------------------------------------------------------------------

## 1. Purpose

This document consolidates the completed Stage 8.1 architecture
specifications into one master technical design for the FDO-Privacy
prototype.

It brings together:

-   project structure
-   system components
-   complete data flow
-   input/output contracts
-   data model
-   FDO decision logic
-   AI responsibilities
-   API requirements
-   technology direction
-   validation strategy

This document is the master reference for Stage 8 implementation.

------------------------------------------------------------------------

# 2. System Objective

The FDO-Privacy prototype operationalizes the project's research
methodology into an auditable software pipeline.

The system connects:

``` text
Application Functionality
        +
Expected Data Requirements
        +
Privacy Policy Evidence
        ↓
Functional Comparison
        ↓
FDO Reasoning
        ↓
Explainable Result
```

The prototype is intended to determine whether a data practice can be
established as functionally excessive, not merely whether a privacy
policy mentions a particular data type.

------------------------------------------------------------------------

# 3. Architectural Principles

The system follows these principles:

1.  **Evidence first**
2.  **Function-dependent analysis**
3.  **Explicit expected-data baseline**
4.  **Separation of AI extraction and FDO decision logic**
5.  **Three-way final classification**
6.  **Explicit uncertainty**
7.  **Evidence provenance**
8.  **Benchmark separation**
9.  **Explainable results**
10. **Incremental implementation**

------------------------------------------------------------------------

# 4. High-Level Architecture

``` text
                         USER
                           |
                           v
                 +-------------------+
                 |   FRONTEND / UI   |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 |   BACKEND API     |
                 |     FastAPI       |
                 +---------+---------+
                           |
              +------------+-------------+
              |                          |
              v                          v
       APPLICATION CONTEXT        POLICY PROCESSOR
              |                          |
              v                          v
       EXPECTED DATA ENGINE       AI POLICY EXTRACTION
              |                          |
              |                          v
              |                  NORMALIZATION
              |                          |
              +------------+-------------+
                           |
                           v
                 FUNCTIONAL COMPARISON
                           |
                           v
                 FDO DECISION ENGINE
                           |
                           v
                 EXPLANATION GENERATOR
                           |
                           v
                 RESULTS / REPORT
                           |
                           v
                         USER
```

------------------------------------------------------------------------

# 5. Project Structure

The current repository structure is:

``` text
C:\FDO
│
├── Backend
│   ├── app
│   │   ├── models
│   │   ├── rules
│   │   ├── services
│   │   └── utils
│   └── requirements.txt
│
├── DATA
│
├── Docs
│
├── Frontend
│   ├── public
│   └── src
│       ├── components
│       ├── pages
│       ├── services
│       ├── types
│       └── utils
│
└── existing research documents
```

The `Docs` directory contains the Stage 8 architecture specifications.

------------------------------------------------------------------------

# 6. System Components

## 6.1 User Interface

Collects application and privacy-policy input and presents analysis
results.

It does not make FDO decisions.

## 6.2 Application Information Manager

Represents:

``` text
Application
Function
Feature
```

This supplies functional context.

## 6.3 Privacy Policy Processor

Converts supplied policy documents/text into processable text while
preserving source information.

## 6.4 AI Policy Extraction

Extracts candidate:

``` text
Data Type
Purpose
Entity
Sharing
Retention
Evidence
Source Section
```

## 6.5 Data / Purpose Normalization

Maps equivalent expressions into controlled concepts while preserving
original wording.

## 6.6 Expected Data Engine

Retrieves function-specific expected mappings from the established
research model.

## 6.7 Policy Evidence Store

Preserves extracted policy evidence and provenance.

## 6.8 Functional Comparison Engine

Compares:

``` text
Expected vs Declared Data
Expected vs Declared Purpose
Data vs Function
```

## 6.9 FDO Decision Engine

Applies the explicit FDO rules and returns:

``` text
FDO
NOT_FDO
AMBIGUOUS
```

## 6.10 Explanation Generator

Creates evidence-backed human-readable explanations.

## 6.11 Results Dashboard

Displays item-level findings, evidence, explanations, and summaries.

------------------------------------------------------------------------

# 7. End-to-End Data Flow

``` text
1. User supplies application + policy
                ↓
2. Input validation
                ↓
3. Application/function context
                ↓
4. Policy processing
                ↓
5. AI extraction
                ↓
6. Data/purpose normalization
                ↓
7. Expected mapping lookup
                ↓
8. Functional comparison
                ↓
9. Necessity evaluation
                ↓
10. Purpose compatibility
                ↓
11. Functional justification
                ↓
12. FDO decision
                ↓
13. Evidence/provenance attachment
                ↓
14. Explanation generation
                ↓
15. Dashboard/report
```

------------------------------------------------------------------------

# 8. Input Contract

Main analysis request:

``` json
{
  "application_name": "string",
  "category": "string",
  "description": "string",
  "policy_text": "string",
  "policy_source": "string|null"
}
```

Required:

``` text
application_name
category
policy_text
```

------------------------------------------------------------------------

# 9. Core Output Contract

Each item-level result should contain:

``` json
{
  "data_type": "LOCATION",
  "expected_necessity": "L1_REQUIRED",
  "expected_purpose": "Route calculation",
  "declared_purpose": "Location-based services",
  "purpose_compatibility": "COMPATIBLE",
  "functional_relationship": "SUPPORTED",
  "functional_justification": "SUPPORTED",
  "evidence_status": "SUFFICIENT",
  "fdo_status": "NOT_FDO",
  "explanation": "..."
}
```

Final classification:

``` text
FDO
NOT_FDO
AMBIGUOUS
```

------------------------------------------------------------------------

# 10. Data Model

Core entities:

``` text
Application
Function
ExpectedMapping
PolicyDocument
PolicyEvidence
NormalizedEvidence
Analysis
Comparison
FDOResult
Explanation
```

Relationship:

``` text
APPLICATION
│
├──< FUNCTION
│      │
│      └──< EXPECTED_MAPPING
│
├──< POLICY_DOCUMENT
│      │
│      └──< POLICY_EVIDENCE
│               │
│               └──< NORMALIZED_EVIDENCE
│
└──< ANALYSIS
        │
        └──< COMPARISON
                 │
                 ├── EXPECTED_MAPPING
                 └── POLICY_EVIDENCE
                         |
                         v
                    FDO_RESULT
                         |
                         v
                    EXPLANATION
```

The model preserves source evidence separately from normalized data and
generated explanations.

------------------------------------------------------------------------

# 11. FDO Decision Logic

The decision process is:

``` text
Evidence Sufficiency
        ↓
Necessity
        ↓
Purpose Compatibility
        ↓
Functional Relationship
        ↓
Functional Justification
        ↓
FDO Decision
```

## FDO

Use `FDO` when available evidence establishes functional excess or
purpose incompatibility under the adopted project rules.

## NOT_FDO

Use `NOT_FDO` when sufficient evidence supports the functional
relationship and does not establish functional excess or purpose
incompatibility.

## AMBIGUOUS

Use `AMBIGUOUS` when evidence is insufficient, unclear, or conflicting
such that a defensible binary decision cannot be made.

------------------------------------------------------------------------

# 12. Important Decision Rules

``` text
Declared data ≠ automatically FDO
Optional data ≠ automatically FDO
Missing evidence ≠ NOT_DECLARED
Unclear evidence → AMBIGUOUS
AI prediction ≠ final FDO decision
```

The system must not create certainty where the evidence does not support
it.

------------------------------------------------------------------------

# 13. AI Architecture Boundary

The AI layer is responsible for:

``` text
Policy extraction
Data-type identification
Purpose identification
Entity/sharing/retention extraction
Normalization assistance
Uncertainty detection
Explanation drafting
```

The deterministic research layer is responsible for:

``` text
Expected data
Necessity
Functional relationship
Purpose compatibility
Functional justification
Final FDO classification
```

Architecture:

``` text
AI
 |
 v
Structured Evidence
 |
 v
Comparison / Research Rules
 |
 v
FDO Decision
```

------------------------------------------------------------------------

# 14. AI Safety / Reliability Rules

The AI must not:

-   invent policy evidence
-   invent purposes
-   treat assumptions as evidence
-   convert missing evidence into proof of non-collection
-   force uncertain cases into a binary classification
-   independently override the FDO rules

AI confidence is model/extraction confidence, not factual truth.

------------------------------------------------------------------------

# 15. Evidence and Provenance

Important analytical records should retain:

``` text
Evidence ID
Source Policy
Source Section
Source Location
Evidence Text
Extraction Status
Confidence
```

A decision should be traceable through:

``` text
Application
    ↓
Function
    ↓
Expected Mapping
    ↓
Policy Evidence
    ↓
Comparison
    ↓
FDO Result
    ↓
Explanation
```

------------------------------------------------------------------------

# 16. API Architecture

Base path:

``` text
/api/v1
```

Main endpoints:

``` text
POST /api/v1/analyze
POST /api/v1/extract-policy

GET /api/v1/applications
GET /api/v1/applications/{application_id}
GET /api/v1/applications/{application_id}/expected-mappings

GET /api/v1/analysis/{analysis_id}
GET /api/v1/analysis/{analysis_id}/report

GET /api/v1/health
```

The API uses structured JSON responses and structured error objects.

------------------------------------------------------------------------

# 17. Main Analysis API Flow

``` text
POST /api/v1/analyze
        |
        v
Validate
        |
        v
Process Policy
        |
        v
Extract Evidence
        |
        v
Normalize
        |
        v
Load Expected Data
        |
        v
Compare
        |
        v
Apply FDO Rules
        |
        v
Generate Explanation
        |
        v
Return AnalysisResponse
```

------------------------------------------------------------------------

# 18. Error Handling

Errors use:

``` json
{
  "error": {
    "code": "POLICY_EMPTY",
    "message": "Privacy policy text is required.",
    "field": "policy_text"
  }
}
```

Initial HTTP statuses:

``` text
200 OK
201 Created
400 Bad Request
404 Not Found
422 Validation Error
500 Internal Server Error
503 Service Unavailable
```

`AMBIGUOUS` is a domain result, not an HTTP error.

------------------------------------------------------------------------

# 19. Technology Direction

Initial implementation direction:

``` text
Frontend:
React / Next.js

Backend:
Python + FastAPI

AI / NLP:
LLM + NLP utilities

Database:
SQLite initially

Optional future database:
PostgreSQL

Optional future graph layer:
Neo4j / graph representation
```

Technology choices may be refined during implementation if justified by
the prototype requirements.

------------------------------------------------------------------------

# 20. Initial Implementation Boundary

The first working implementation should remain simple:

``` text
Policy Text
    ↓
AI Extraction
    ↓
Structured Evidence
    ↓
Expected Mapping Lookup
    ↓
FDO Rule Engine
    ↓
Explanation
    ↓
JSON
```

Advanced infrastructure should not be introduced before the basic
pipeline works.

------------------------------------------------------------------------

# 21. Benchmark and Evaluation Architecture

The manually adjudicated research benchmark remains separate from
prototype predictions.

``` text
Existing Research Benchmark
          |
          | read-only reference
          v
       Evaluation
          |
          +---- Prototype
          |
          v
       Comparison
          |
          v
      Metrics / Findings
```

Prototype disagreement with the benchmark becomes an evaluation result
rather than a reason to overwrite the benchmark.

------------------------------------------------------------------------

# 22. Existing Research Baseline

The Stage 8 prototype is intended to build on the research artifacts
produced in earlier stages.

The benchmark currently documented for evaluation contains:

``` text
Expected mappings: 99
Evidence-backed mappings: 93
NOT_FDO: 60
AMBIGUOUS: 33
FDO established: 0
```

These are benchmark values and must not be hard-coded as prototype
outputs.

------------------------------------------------------------------------

# 23. Explainability Requirement

Every final result should expose:

``` text
Data Item
Function
Expected Requirement
Declared Practice
Policy Evidence
Purpose Compatibility
Functional Justification
FDO Classification
Explanation
```

The system should prioritize item-level explanations over an opaque
single privacy score.

------------------------------------------------------------------------

# 24. Security and Integrity

The prototype should:

-   validate user input
-   validate document types
-   limit unsafe uploads
-   preserve original evidence
-   distinguish source evidence from generated text
-   avoid unnecessary exposure of sensitive content in logs
-   prevent benchmark overwrite
-   maintain provenance
-   support controlled access when deployed

------------------------------------------------------------------------

# 25. Implementation Sequence

After Stage 8.1 is formally closed, implementation should proceed
incrementally:

``` text
8.2 Backend Foundation
        ↓
8.3 Policy Processing
        ↓
8.4 Expected Data Integration
        ↓
8.5 FDO Engine
        ↓
8.6 Explanation / Reporting
        ↓
8.7 Frontend
        ↓
8.8 Integration
        ↓
8.9 Testing
        ↓
8.10 Benchmark Evaluation
        ↓
8.11 Results
```

The exact Stage 8.2+ numbering can be refined when implementation
begins, but the architecture should remain consistent with this
sequence.

------------------------------------------------------------------------

# 26. Stage 8.1K Completion Criteria

The master architecture is complete when it consolidates:

-   [x] Project structure
-   [x] System components
-   [x] Complete data flow
-   [x] Input/output contracts
-   [x] Data model
-   [x] FDO decision logic
-   [x] AI responsibilities
-   [x] API requirements
-   [x] Technology direction
-   [x] Evidence/provenance
-   [x] Benchmark separation
-   [x] Validation strategy
-   [x] Security/integrity principles
-   [x] Implementation boundary

**Status: COMPLETE**

------------------------------------------------------------------------

# 27. Final Architecture Principle

The complete FDO-Privacy prototype can be summarized as:

``` text
                APPLICATION
                     |
              WHAT IT DOES
                     |
                     v
              EXPECTED DATA
                     |
                     |
PRIVACY POLICY ---> POLICY EVIDENCE
                     |
                     v
              FUNCTIONAL
              COMPARISON
                     |
                     v
              FDO RULE ENGINE
                     |
          +----------+----------+
          |          |          |
          v          v          v
         FDO      NOT_FDO   AMBIGUOUS
          |          |          |
          +----------+----------+
                     |
                     v
                EXPLANATION
                     |
                     v
                  USER
```

The central architectural rule is:

``` text
AI extracts and assists.
Research rules decide.
Evidence explains.
```

------------------------------------------------------------------------

# 28. Next Stage

**Stage 8.1L --- Final Architecture Verification**

The next step is the final gate check of all Stage 8.1 deliverables.

Only after every required item passes verification will Stage 8.1 be
marked:

``` text
COMPLETE
```

and implementation Stage 8.2 can begin.
