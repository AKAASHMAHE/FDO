# FDO Privacy Project: Technical Analysis for IDF-B Documentation

**Document ID:** `IDF-B-TECH-ANALYSIS-v1.0`  
**Project Title:** Functional Data Ontology (FDO) Privacy Compliance & Overreach Detection Framework  
**Repository Working Directory:** `d:\VIT\PROJECT\TARP`  
**Target Specification:** Invention Disclosure Form B (IDF-B) / Academic Capstone Technical Defense  
**Auditor Status:** Automated Assistant (Strict Read-Only Audit from Parts 1–4)  
**Date:** 2026-10-13  

---

## 1. Executive Summary

The **FDO Privacy Project** is an automated privacy policy compliance auditing system designed to operationalize the legal principle of **Data Minimization** (GDPR Article 5(1)(c)). The framework detects **Functional Data Overreach (FDO)**—defined as personal data collection declared in privacy disclosures that exceeds or conflicts with the legitimate functional requirements of a software application.

The codebase implements a dual-engine architecture:
1. **Deterministic Relational Engine**: Performs pairwise comparisons between expected functional data needs and extracted policy disclosures using a 6-rule hierarchical expert system.
2. **Semantic Knowledge Graph Engine**: Projects relational entities into an in-memory Resource Description Framework (RDF) knowledge graph conformant to a custom Web Ontology Language (OWL) schema (`fdo:`, 19 classes, 23 object properties, 23 data properties), queries semantic graph patterns via SPARQL in Apache Jena Fuseki, and adapts detected discrepancies into structured overreach findings.

The system combines zero-shot large language model inference (`gemini-3.5-flash-lite`) for automated policy disclosure extraction and conservative baseline synthesis with deterministic rule-based classifiers for purpose normalization, entity matching, and compliance adjudication. An interactive React single-page application (SPA) visualizes the results with explainable decision justifications.

---

## 2. Problem Statement

Mobile and web privacy policies are notoriously lengthy, legally ambiguous, and rarely read by end-users. Existing privacy policy analysis tools suffer from three fundamental limitations:
1. **Lack of Functional Context**: State-of-the-art Natural Language Processing (NLP) tools extract *what* data is collected, but cannot evaluate *whether* that collection is technically necessary for the features the user actually uses.
2. **Absence of Formalized Semantics**: Privacy disclosures use varied terminology (e.g., "precise geolocation", "GPS coordinates", "physical location") that cannot be systematically validated against functional expectations without formal ontologies.
3. **Black-Box Decision Making**: Machine learning classifiers often output risk scores without verifiable, legally traceable chains of reasoning linking a specific application function to a specific policy clause.

---

## 3. Objectives

1. Formulate a formal **Functional Data Ontology (FDO)** in OWL/RDF defining entities, properties, and constraints governing software functions, expected data types, declared disclosures, and overreach risks.
2. Develop an automated pipeline that ingests raw privacy policies, extracts granular data collection statements, and normalizes them to canonical ontology tokens.
3. Establish a dual analysis pipeline combining deterministic relational logic and SPARQL knowledge graph querying to detect functional overreach.
4. Provide verifiable, explainable decision rationales indicating whether an observed collection practice is `NOT_FDO` (justified), `FDO` (disproportionate/incompatible), or `AMBIGUOUS` (insufficient evidence).
5. Build a web-based dashboard for security analysts and auditors to run on-demand compliance assessments.

---

## 4. Proposed Solution

The proposed solution implements a **Knowledge Graph-Driven Semantic Privacy Auditing System**:
- **Functional Baseline Layer**: Encapsulates expected data needs per application feature, either retrieved from curated empirical ground-truth datasets or conservatively synthesized using an LLM prompt restricted solely to functional context (without access to the privacy policy).
- **Extraction & Normalization Layer**: Parses privacy policy text into atomic evidence items and normalizes data types and processing purposes against controlled taxonomies.
- **Dual Adjudication Architecture**:
  - *Relational Branch*: High-speed pairwise matrix comparison in SQLite/SQLAlchemy.
  - *Semantic Branch*: Dynamic RDF graph synthesis serialized to Turtle format, uploaded to an Apache Jena Fuseki triple store, and queried via SPARQL to identify pattern discrepancies.
- **Explainability Engine**: Attaches rule identifiers, supporting textual citations, and confidence scores to every adjudicated finding.

---

## 5. Implemented Features & Verification Status

Every major subsystem in the repository has been audited against source code and labeled according to the project audit taxonomy:

| Subsystem / Feature | Exact Source Location (`path:line`) | Implemented Mechanism | Verification Status |
| :--- | :--- | :--- | :--- |
| **FastAPI REST API (13 routes)** | `Backend/app/main.py:86-620` | Asynchronous REST routing, CORS middleware, Pydantic v2 schemas | **Implemented-verified** |
| **SQLAlchemy SQLite ORM (11 tables)** | `Backend/app/models/*.py`, `database.py:8-54` | Relational persistence with SQLite schema compatibility migrations | **Implemented-verified** |
| **LLM Policy Evidence Extraction** | `Backend/app/services/ai_service.py:81-248` | `gemini-3.5-flash-lite` via `google.genai.Client`, zero-shot structured JSON | **Implemented-verified** |
| **Fallback Regex Extraction** | `Backend/app/services/policy_extraction_service.py:37-90` | Sentence splitting (`re.split`) + keyword matching (`location`, `traffic`) | **Implemented-verified** |
| **Evidence Validation & Noise Filter** | `Backend/app/services/evidence_validation_service.py:107-220` | Lexical set filtering (`PRIVACY_DATA_KEYWORDS`, `OPERATIONAL_NOISE`) | **Implemented-verified** |
| **Conservative AI Baseline Generator** | `Backend/app/services/ai_service.py:341-407` | `gemini-3.5-flash-lite` prompting restricted strictly to functional metadata | **Implemented-verified** |
| **Purpose Classification (14 classes)** | `Backend/app/services/comparison_service.py:3-97, 238-270` | Deterministic substring scan against `PURPOSE_CATEGORIES` | **Implemented-verified** |
| **Purpose Compatibility Adjudication** | `Backend/app/services/comparison_service.py:313-380` | Multi-category overlap rules & marketing/advertising rejection | **Implemented-verified** |
| **Deterministic FDO Decision Engine** | `Backend/app/services/fdo_decision_service.py:27-147` | 6-rule hierarchical decision tree (`NOT_FDO`, `FDO`, `AMBIGUOUS`) | **Implemented-verified** |
| **Contextual Evidence Matcher** | `Backend/app/services/evidence_matcher.py:54-193` | Heuristic scoring (base, purpose, function context, extraction state) | **Implemented-verified** |
| **FDO Formal OWL Ontology (19 classes)** | `Backend/app/ontology/classes.py`, `specification.py` | Python dataclass TBox model, `Backend/ontology/FDO.owl` (436 lines) | **Implemented-verified** |
| **RDF Instance Graph Builder** | `Backend/app/ontology/rdf_instance_builder.py:65-1047` | Dynamic RDFLib graph construction from relational domain objects | **Implemented-verified** |
| **Jena Fuseki HTTP Client** | `Backend/app/ontology/fuseki_service.py:6-69` | HTTP REST client managing SPARQL queries/updates against `:3030` | **Implemented-verified** |
| **SPARQL Overreach Detection Query** | `Backend/app/ontology/fdo_detection_queries.py:5-37` | Graph pattern matching identifying mismatched types or purposes | **Implemented-verified** |
| **Semantic Decision Adapter** | `Backend/app/ontology/semantic_decision_adapter.py:15-82` | Converts SPARQL graph bindings to `FDODecisionInput` dataclass | **Implemented-verified** |
| **React/Vite Dashboard (SPA)** | `Frontend/src/App.jsx:1-1739`, `App.css` | React 19 interactive UI, metric cards, expandable semantic accordions | **Implemented-verified** |
| **Automated Policy Discovery** | `Backend/app/services/policy_discovery_service.py:137-221` | Static lookup (`KNOWN_POLICY_URLS`) + `html.parser` tag stripping | **Implemented-verified** |
| **Cross-App Comparison Logic** | Entire repository search | Pairwise comparison between different applications | **Not-found** |
| **Intra-Policy Contradiction Detection** | Entire repository search | Logic detecting contradictory statements within one policy | **Not-found** |
| **Automated Description-to-Function Extractor**| Entire repository search | Automatic derivation of application functions from raw app descriptions | **Not-found** |

---

## 6. Technical Stack & Exact Components

### 6.1 Programming Languages & Frameworks
- **Backend**: Python 3.10.11 (`Backend/pyproject.toml`)
- **Web Framework**: FastAPI 0.115+ with Starlette and Uvicorn
- **Object-Relational Mapping (ORM)**: SQLAlchemy 2.0.38
- **Data Validation**: Pydantic 2.10+ (`BaseModel`, `computed_field`)
- **Frontend**: JavaScript (ES2022) / JSX, React 19.0.0, Vite 6.2.0 (`Frontend/package.json`)
- **Styling**: Vanilla CSS3 with custom variables, CSS Grid, Flexbox (`Frontend/src/App.css`)

### 6.2 Semantic Web & Knowledge Graph Components
- **RDF Engine**: RDFLib 7.1.3 (`from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD`)
- **Triple Store & SPARQL Endpoint**: Apache Jena Fuseki 6.2.0 (`apache-jena-fuseki-6.2.0/`), running on HTTP port 3030 (dataset: `fdo-reasoning`)
- **Ontology Modeling**: W3C OWL 2 DL profile serialized in RDF/XML (`Backend/ontology/FDO.owl`) and Turtle (`Backend/outputs/semantic/*.ttl`)

### 6.3 AI & Machine Learning Specification
- **Foundation Model**: `gemini-3.5-flash-lite` (Google DeepMind)
- **SDK**: `google-genai>=0.1.0` (`from google import genai`)
- **Invocation Mode**: **Zero-shot inference only**. No fine-tuning, parameter updates, local weights, or embeddings exist in the codebase.
- **Model Parameters**: Default API generation parameters (no custom temperature or top_p passed).
- **Execution Guardrails**: Enforces JSON Schema obedience; wraps network calls in try/catch blocks diverting to deterministic regex parsing upon API failure.

---

## 7. System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER (Vite / React 19)            │
│  App.jsx (Form Input, Metric Cards, Functional Baseline, Grouped Cards)│
└────────────────────────────────────┬───────────────────────────────────┘
                                     │ HTTP REST (JSON)
┌────────────────────────────────────▼───────────────────────────────────┐
│                        API & ROUTING LAYER (FastAPI)                   │
│  main.py (13 Endpoints, Dependency Injection, CORS, Error Handling)   │
└──────────┬─────────────────────────┬───────────────────────────┬───────┘
           │                         │                           │
┌──────────▼───────────────┐ ┌───────▼─────────────────┐ ┌───────▼───────┐
│   INGESTION & DISCOVERY  │ │    EVIDENCE EXTRACTION  │ │   BASELINE    │
│  policy_discovery_service│ │  ai_service (Gemini)    │ │  functional_  │
│  (HTMLParser, Static URL)│ │  policy_extraction_svc  │ │  baseline_svc │
└──────────┬───────────────┘ └───────┬─────────────────┘ └───────┬───────┘
           │                         │                           │
           └─────────────────────────┼───────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        DUAL ANALYSIS CORE                              │
│                                                                        │
│  [ Branch A: Deterministic Relational Engine ]                         │
│  analysis_runner.py ──> evidence_matcher.py ──> comparison_service.py   │
│                                 │                                      │
│                                 ▼                                      │
│                     fdo_decision_service.py                            │
│                     (6-Rule Hierarchical Expert System)                │
│                                                                        │
│  [ Branch B: Semantic Knowledge Graph Engine ]                         │
│  db_rdf_service.py (RDFLib Graph) ──> outputs/semantic/*.ttl           │
│                                 │                                      │
│                                 ▼ HTTP Upload / Clear                  │
│                     Apache Jena Fuseki (:3030)                         │
│                                 │                                      │
│                                 ▼ SPARQL (FDO_DETECTION_QUERY)         │
│                     fuseki_semantic_detector.py                        │
│                                 │                                      │
│                                 ▼ Adapts Bindings                      │
│                     semantic_decision_adapter.py ──> Decision Engine   │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
┌────────────────────────────────────▼───────────────────────────────────┐
│                        PERSISTENCE LAYER (SQLite)                      │
│  fdo_privacy.db (applications, functions, expected_mappings,           │
│  policy_documents, policy_evidence, analyses, comparisons, results)    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 8. NLP, AI & Data Pipeline Trace

1. **Ingestion**: `policy_discovery_service.py` fetches raw HTML via HTTP GET, parses it through `_TextExtractor` (ignoring `<script>`, `<style>`, `<noscript>`), and normalizes whitespace up to a 1,000,000-byte cap.
2. **Extraction Routing**: `policy_extraction_service.py` attempts primary Gemini LLM extraction. If the API key is missing or calls fail, it falls back to regex sentence splitting (`re.split(r"(?<=[.!?])\s+", text)`).
3. **Structured Entity Extraction**: Extracts 6 core attributes per clause: `data_type`, `purpose`, `entity`, `sharing`, `retention`, and verbatim `evidence_text`.
4. **Validation & Filtering**: `evidence_validation_service.py` eliminates operational noise by filtering out 11 operational phrases (`"delivery is retried"`, `"infrastructure reliability"`, etc.) and enforcing that valid evidence must intersect both `PRIVACY_DATA_KEYWORDS` (27 items) and `PROCESSING_KEYWORDS` (9 items).
5. **Ontology Normalization**: Canonicalizes data types to 11 uppercase tokens (`DATA.LOCATION.PRECISE`, etc.) and classifies purposes into 14 controlled categories (`PURPOSE_CATEGORIES`).
6. **Contextual Evidence Matching**: `evidence_matcher.py` scores candidate evidence items against expected feature mappings using a 100-point heuristic (base: 10, purpose compatible: +60, function in text: +25, extracted state: +5, confidence: up to +1.0).

---

## 9. Datasets & Empirical Pipeline

The repository houses extensive empirical research datasets in `DATA/`:
- **Master Curated Dataset**: `DATA/FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx` (56 KB, 12 sheets) containing 30 applications across 4 categories, 99 curated expected functional mappings, and 30 privacy policies.
- **Annotator Agreement Studies**: 15 Excel workbooks (`DATA/FDO-Privacy_Stage2B_*.xlsx`) containing dual-coder annotation batches and inter-rater reliability calculations.
- **Empirical Adjudication Matrices**: 9 workbooks (`DATA/FDO-Privacy_Stage4*.xlsx`) detailing ground-truth expected-vs-declared comparisons.
- **Visualization Artifacts**: `DATA/FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx` (247 KB) containing statistical charts and frequency distributions.

---

## 10. Ontology Specification, Knowledge Graph & SPARQL

### 10.1 Schema Definition
- **Namespace**: `http://example.org/fdo#` (`Backend/app/ontology/namespace.py:11`). Instance URIs follow `http://example.org/fdo#resource/<type>/<id>` (`Backend/app/ontology/uri.py:19`).
- **Classes (19)**: `FDOEntity` (root), `Application`, `Function`, `PersonalData`, `SensitiveData`, `ProcessingActivity`, `Purpose`, `Recipient`, `RetentionPolicy`, `User`, `UserRight`, `Consent`, `PrivacyPolicy`, `PolicyClause`, `ExpectedData`, `DeclaredData`, `Justification`, `Overreach`, `Risk`.
- **Properties**: 23 Object Properties (`performsFunction`, `expectedData`, `declaredData`, etc.) and 23 Data Properties (`dataType`, `purpose`, `necessity`, `confidence`, etc.).
- **Constraints**: 14 cardinality bounds (e.g. `Application performsFunction min 1 Function`, `Overreach concernsData exactly 1 PersonalData`) and 8 mandatory attribute rules.

### 10.2 SPARQL Detection
The core semantic query (`Backend/app/ontology/fdo_detection_queries.py:5-37`) identifies overreach by matching triples where an application performs a function requiring `?expectedData` while simultaneously declaring `?declaredData`, filtering for mismatched data types or purposes:
```sparql
PREFIX fdo: <http://example.org/fdo#>
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

---

## 11. Reasoning Reality Check

A strict audit of the Jena Fuseki configuration reveals:
1. **Reasoner Configuration**: The Fuseki assembler (`apache-jena-fuseki-6.2.0/run/configuration/fdo-reasoning.ttl:17-21`) configures an `owl:OntologyModel` with `ja:reasoner [ ja:reasonerURL <http://jena.hpl.hp.com/2003/OWLFBRuleReasoner> ]`.
2. **Operational Reality**: At runtime, the analysis pipeline **does not rely on OWL DL classification, consistency checking, or forward-chaining rule deductions to make decisions**.
3. **Primary Detection Mechanism**: Overreach detection is performed entirely through graph pattern matching (SPARQL `FILTER`) and downstream Python rule adjudication (`semantic_decision_adapter.py`).

---

## 12. Relational Database Architecture

The system utilizes SQLite (`Backend/fdo_privacy.db`) via SQLAlchemy with 11 primary tables:
- `applications`: Application metadata and category.
- `functions`: Feature declarations per application.
- `expected_mappings`: Curated baseline requirements (`data_type`, `necessity`, `expected_purpose`, `baseline_justification`).
- `policy_documents`: Ingested policy metadata and full text.
- `policy_evidence`: Extracted disclosure clauses and confidence ratings.
- `analyses`: Analysis run headers and counter metrics (`total_mappings`, `fdo_count`, `not_fdo_count`, `ambiguous_count`).
- `comparisons`: Pairwise evaluated tuples linking expected mappings to policy evidence.
- `fdo_results`: Adjudicated status (`fdo_status`, `decision_reason`, `decision_confidence`).
- `explanations`: Textual explanation records.
- `semantic_fdo_results`: Persisted SPARQL detection findings.
- `normalized_evidence`: Intermediate normalization schema.

---

## 13. API & Frontend Architecture

- **Backend API**: 13 endpoints exposing health checks, application querying, baseline inspection, standalone policy extraction, end-to-end analysis (`/api/v1/analyze`), analysis history, and rich reports.
- **Frontend Dashboard**: Single-page application in React 19 / Vite. Features include:
  - Form submission with automatic policy discovery or manual paste fallback.
  - KPI summary metric cards (Total, FDO, Not FDO, Ambiguous).
  - Functional baseline disclosure table (Curated vs AI-derived).
  - Policy analysis cards showing verbatim policy excerpts.
  - Collapsible function-level semantic cards (`GroupedSemanticCard`) displaying exact matches vs discrepancies, confidence ratings, and decision rationales.
  - Persistent historical analysis drawer.

---

## 14. Privacy Analysis & Comparison Logic

### 14.1 Decision Rules (`fdo_decision_service.py:27-147`)
- **Rule 1 (Missing Evidence)**: `evidence_status == "NO_EVIDENCE"` $\rightarrow$ `AMBIGUOUS` (confidence: 0.30).
- **Rule 2 (Weak Evidence)**: `evidence_status in {"INSUFFICIENT", "UNKNOWN"}` $\rightarrow$ `AMBIGUOUS` (confidence: 0.40).
- **Rule 3 (Functionally Justified)**: `data_match == "EXACT_MATCH"` AND `purpose_compatibility == "COMPATIBLE"` AND `functional_relationship == "RELATED"` $\rightarrow$ `NOT_FDO` (confidence: 0.90).
- **Rule 4 (Purpose Overreach)**: `data_match == "EXACT_MATCH"` AND `purpose_compatibility == "INCOMPATIBLE"` AND `functional_relationship == "RELATED"` $\rightarrow$ `FDO` (confidence: 0.85).
- **Rule 5 (Data Type Overreach)**: `data_match == "NO_MATCH"` AND `functional_relationship == "RELATED"` $\rightarrow$ `FDO` (confidence: 0.80).
- **Rule 6 (Conservative Fallback)**: All other states $\rightarrow$ `AMBIGUOUS` (confidence: 0.50).

### 14.2 Methodological Integrity
- **Policy Difference $\neq$ Contradiction**: Differing data practices between different applications or functions are not labeled as contradictions; they simply reflect different design decisions.
- **Omission $\neq$ Non-Occurrence**: When a policy fails to disclose a data practice, the framework treats the practice as unverified and flags the comparison as `AMBIGUOUS` rather than falsely asserting `NOT_FDO`.

---

## 15. Testing Results & Verification Audit

- **Test Suite Structure**: 67 test files in `Backend/test_*.py` containing **397 collected tests** (`pytest 9.1.1`).
- **Executed Unit & Offline Test Results**:
  - **Command**: `pytest` across all ontology, baseline, purpose normalization, relational decision, and offline adapter test files (39 test files).
  - **Result**: **356 Passed, 0 Failed, 0 Skipped** (Execution time: ~3.8 seconds).
- **Integration Test Behavior**:
  - Live tests requiring an active Apache Jena Fuseki daemon on `localhost:3030` fail with `ConnectionRefusedError` when Fuseki is not started locally.
  - Production runtime features graceful degradation: `Backend/app/main.py:418-420` catches Fuseki connection errors and completes relational analysis without crashing.

---

## 16. Limitations & Technical Risks by Severity

### 16.1 High Severity
1. **External LLM Dependency**: Baseline synthesis and policy extraction rely on external Gemini API connectivity. Without an API key, the system degrades to a simple 4-keyword regex extractor (`policy_extraction_service.py:39-90`).
2. **Absence of True Cross-Application Comparison**: Despite documentation references, the system cannot directly compare App A against App B; it evaluates an application strictly against its own policy.
3. **Fuseki Process Coupling**: The semantic knowledge graph pipeline requires an independent Java background daemon on port 3030. If Fuseki is down, semantic results are omitted.

### 16.2 Medium Severity
1. **Keyword-Based Purpose Classification**: Purpose mapping relies on exact phrase matching across 14 categories. Subtle semantic meanings or novel phrasings can be misclassified as incompatible.
2. **Fixed Data Type Taxonomy**: Only 18 string tokens are recognized. Unmapped data types default to `DATA.OTHER`.
3. **No Intra-Policy Contradiction Engine**: The system does not detect internal policy contradictions (e.g., claiming "we never sell data" in section 1 while describing ad exchange sharing in section 4).

### 16.3 Low Severity
1. **Deprecated FastAPI Lifecycle Hook**: Uses `@app.on_event("startup")` instead of modern lifespan handlers.
2. **Hardcoded Local Paths in Legacy Scripts**: `Backend/scripts/import_stage3.py:15` contains a hardcoded `D:\` drive path.

---

## 17. Remaining Work for Production Deployment

1. **Native Docker / Subprocess Supervision for Fuseki**: Containerize or script automated lifecycle management for Apache Jena Fuseki.
2. **Local Embedding-Based Purpose Matcher**: Replace substring matching with a small local sentence transformer (e.g. `all-MiniLM-L6-v2`) to compute semantic cosine similarities for purposes.
3. **Multi-Application Comparative REST Endpoint**: Implement a dedicated endpoint (`/api/v1/compare-applications`) allowing users to compare privacy footprints across multiple applications in the same category.
4. **Natural Language Inference (NLI) Contradiction Module**: Introduce cross-clause contradiction checking to identify self-conflicting disclosures.

---

## 18. Technical Glossary

- **FDO (Functional Data Overreach)**: The collection or processing of personal data declared in privacy disclosures that exceeds or conflicts with the legitimate technical needs of an application's features.
- **TBox (Terminological Component)**: The formal conceptual schema of an ontology (classes, relationships, and property definitions).
- **ABox (Assertional Component)**: The instance data asserting concrete facts and relationships about specific applications, policies, and findings.
- **Data Minimization**: The legal and technical requirement (GDPR Art. 5(1)(c)) that personal data processing must be adequate, relevant, and limited to what is necessary in relation to the purposes for which they are processed.
- **SPARQL**: W3C standard query language for querying RDF data represented as directed graphs.
- **Apache Jena Fuseki**: A SPARQL 1.1 HTTP triple store server providing graph persistence and query execution.

---

## 19. Evidence Index

- `Backend/app/main.py:86-620` (FastAPI router and endpoint definitions)
- `Backend/app/services/fdo_decision_service.py:27-147` (Deterministic 6-rule decision tree)
- `Backend/app/services/comparison_service.py:3-97, 313-380` (Purpose taxonomy and compatibility adjudication)
- `Backend/app/services/ai_service.py:81-248, 341-407` (Gemini prompts and structured output schemas)
- `Backend/app/services/evidence_matcher.py:54-193` (Contextual evidence scoring heuristics)
- `Backend/app/ontology/classes.py:1-260` (19 formal ontology dataclasses)
- `Backend/app/ontology/properties.py:51-217` (23 object properties)
- `Backend/app/ontology/data_properties.py:52-214` (23 data properties)
- `Backend/app/ontology/fdo_detection_queries.py:5-37` (Core SPARQL detection pattern)
- `Backend/app/ontology/db_semantic_result_service.py:155-254` (End-to-end semantic analysis pipeline)
- `Frontend/src/App.jsx:1-1739` (React dashboard implementation)
- `DATA/FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx` (Master curated ground-truth research dataset)


---

## 20. IDF-B-Ready Content (Formal Invention Disclosure Content)

> **Auditor Note**: Written in formal academic and patent-disclosure tone. Does not fabricate benchmarks or premature patent claims; clearly specifies candidate technical contributions subject to prior-art clearance.

### 20.1 Title of the Invention
**System and Method for Automated Detection of Functional Data Overreach in Privacy Policies Using a Formal Functional Data Ontology and Knowledge Graph Reasoning**

### 20.2 Field of the Invention
This invention relates generally to software compliance and natural language processing, and more specifically to automated systems, computer-readable media, and computer-implemented methods for auditing digital privacy disclosures against application operational requirements using semantic knowledge graphs and formal ontologies.

### 20.3 Problem Statement & Limitations of Prior Art
Privacy regulations such as the General Data Protection Regulation (GDPR Article 5(1)(c)) mandate that personal data processing adhere to the principle of "data minimization"—collecting only what is strictly necessary for legitimate purposes. However, operationalizing this principle at scale remains an unsolved computational challenge. 

Prior art in automated privacy policy analysis falls into two main paradigms, both of which exhibit severe technical deficiencies:
1. **Isolated Text Extraction (Document-Level Analysis)**: Existing NLP systems (e.g., standard classification or summarization models) extract statements from policy texts without any functional context. They cannot determine whether the declared collection of a specific data type (e.g., precise GPS coordinates) is technically required for the application’s primary features or represents disproportionate overreach.
2. **Static/Dynamic Code Analysis Without Disclosure Mapping**: Tools that analyze application source code or API permissions evaluate runtime behavior but do not map observed practices against legal disclosures, nor do they possess formal knowledge representations capable of reasoning over semantic synonyms and functional necessity tiers.

Consequently, there is an unmet technical need for an automated system capable of bridging the semantic gap between application functional specifications and legal policy disclosures through an explainable, ontology-grounded reasoning framework.

### 20.4 Proposed Solution & Technical Architecture
The present invention addresses these deficiencies by introducing an end-to-end framework that couples a **Functional Data Ontology (FDO)** with a dual-branch adjudication engine:
1. **Functional Baseline Formulation**: Formalizes the data requirements of specific application features into structured tuples comprising functional purpose, necessity level (Required vs. Optional), and normalized data type. This baseline is established via a curated empirical ground truth or dynamically synthesized using an isolated language model prompt strictly restricted to functional context.
2. **Policy Ingestion & Normalization Pipeline**: Automatically harvests privacy policy text, extracts atomic disclosure claims using zero-shot prompt engineering, filters operational noise, and maps extracted terms to canonical ontology concepts.
3. **Dual Adjudication Core**:
   - *Relational Matrix Branch*: Executes deterministic pairwise evaluations against a 6-rule decision tree, producing preliminary classifications (`NOT_FDO`, `FDO`, `AMBIGUOUS`).
   - *Semantic Knowledge Graph Branch*: Constructs a dynamic RDF knowledge graph conforming to the FDO OWL schema, queries the graph via SPARQL to identify structural and purpose discrepancies between expected and declared entities, and adapts semantic bindings into verifiable overreach verdicts.
4. **Explainable Output Engine**: Synthesizes the dual analysis streams into structured reports containing verbatim policy quotes, rule references, and confidence metrics.

### 20.5 Candidate Technical Contributions (Subject to Prior-Art Search)
1. **Novel Formal Ontology for Functional Overreach**: A domain-specific OWL 2 ontology (`fdo:`) defining formal classes and semantic properties that explicitly model the relationship between application features, expected data items, declared policy disclosures, and overreach risks.
2. **Context-Isolated LLM Baseline Synthesis**: A method for synthesizing functional data baselines using generative AI prompts intentionally isolated from privacy policy text, ensuring objective operational baselines free from policy bias.
3. **Dual Relational-Semantic Adjudication Architecture**: A hybrid processing pipeline that cross-validates deterministic relational decision logic with SPARQL graph pattern matching against an RDF triple store to ensure high-confidence overreach classification.
4. **Conservative Omission Adjudication**: A compliance verification method that explicitly distinguishes between policy differences and contradictions, and treats omitted disclosures as unverified/ambiguous rather than falsely presuming non-occurrence.

### 20.6 Demonstrated vs. Intended Technical Outcomes
- **Demonstrated Outcomes (Verified in Code & Tests)**:
  - Automated extraction of personal data collection statements from web privacy policies using `gemini-3.5-flash-lite` with fallback to deterministic regex segmentation.
  - Transformation of relational database entities into 2,700+ byte RDF Turtle graphs matching the FDO OWL ontology.
  - Successful execution of 356 automated unit tests validating ontology properties, purpose normalization across 14 categories, and 6-rule decision logic.
  - Interactive visualization of function-grouped semantic overreach decisions in a React dashboard.
- **Intended Outcomes (Future Scope / Unimplemented Extensions)**:
  - Fully automated derivation of application feature sets directly from app store descriptions or runtime binary analysis.
  - Native automated cross-application comparison dashboards comparing data practices across market competitors.
  - Intra-policy contradiction detection using Natural Language Inference (NLI) models.

### 20.7 Target Use Cases
1. **Regulatory Compliance Auditing**: Enabling data protection authorities (DPAs) to rapidly audit mobile application ecosystems for GDPR data minimization non-compliance.
2. **Pre-Deployment App Store Vetting**: Assisting app marketplace operators in verifying whether an application's declared privacy policy accurately matches its published features before approval.
3. **Enterprise Privacy Engineering**: Providing software engineering teams with an automated CI/CD compliance check that verifies whether privacy policy updates align with new feature releases.

---

## 21. Faculty Explanation Guide (Plain-Language Defense)

> **Auditor Note**: Written to assist students and project teams during viva voce, capstone reviews, and faculty evaluations. Directly addresses common examiner questions.

### Question 1: Why do we need an ontology? Why not just use a traditional relational database or simple Python dictionaries?
**Answer**:  
A traditional database can store tables, but it cannot formally represent semantic relationships, conceptual hierarchies, or domain constraints. 
In privacy auditing, terms vary wildly: an app may describe collecting "precise geolocation", "GPS coordinates", or "latitude/longitude data". A standard database treats these as completely different, unrelated strings.
An ontology (specifically OWL/RDF) allows us to:
1. Define a standardized formal schema (TBox) where concepts like `SensitiveData`, `LocationData`, and `ExpectedData` have explicit semantic definitions and relationships (`concernsData`, `expectedForFunction`).
2. Disambiguate and standardize varied real-world terminology into canonical concepts.
3. Separate the formal conceptual model of privacy law and software functionality from the underlying storage mechanism, making the system interoperable with standard Semantic Web technologies.

### Question 2: What do OWL, RDF, and SPARQL actually do in this project?
**Answer**:  
- **OWL (Web Ontology Language)**: Defines the formal vocabulary, class hierarchy (19 classes), and allowed relationships (23 object properties) in `Backend/ontology/FDO.owl`. It acts as the conceptual blueprint for what constitutes privacy overreach.
- **RDF (Resource Description Framework)**: Represents concrete data as directed graph triples `(Subject -> Predicate -> Object)`. For example, `(GoogleMaps -> performsFunction -> SearchFunction)` and `(SearchFunction -> expectedData -> LocationData)`. In our project, relational data is dynamically transformed into RDF graphs serialized in Turtle format (`.ttl`).
- **SPARQL**: The W3C query language for RDF graphs. We execute SPARQL queries (`FDO_DETECTION_QUERY`) against our Apache Jena Fuseki triple store to find graph patterns where an application claims to perform a function but declares data collection that diverges from expected functional requirements.

### Question 3: Is an automated reasoner or knowledge graph actually used at runtime, or is it just stored triples?
**Answer**:  
- **Knowledge Graph**: **Yes, a knowledge graph is actively constructed and queried.** At runtime, the backend translates SQL records into RDF triples, uploads them to Apache Jena Fuseki, and executes SPARQL graph pattern matching queries (`fuseki_semantic_detector.py`).
- **Automated Reasoner**: **Partially configured, but not driving runtime decisions.** While Apache Jena Fuseki is configured with an OWL rule reasoner (`OWLFBRuleReasoner` in `fdo-reasoning.ttl`), runtime overreach decisions are driven by SPARQL graph pattern queries (`STR(?expectedType) != STR(?declaredType)`) and our downstream Python decision adapter, rather than automated description-logic tableaux classification.

### Question 4: How does the system compare applications? Does it compare App A against App B?
**Answer**:  
No. The system does **not** compare App A directly against App B. 
Instead, it performs **intra-application compliance comparison**: it evaluates the functionality of Application A against the privacy disclosures of Application A. It compares the *data required for its features* against the *data declared in its policy*. 
Evaluating WhatsApp against Telegram is not currently automated in the backend; each analysis is isolated to a single application ID.

### Question 5: Why is a policy difference not automatically a contradiction? Why is omission not proof of non-occurrence?
**Answer**:  
- **Policy Difference $\neq$ Contradiction**: If App A requests Location while App B does not, this is a legitimate difference in application architecture or feature scope, not a legal contradiction. Even within an application, asking for camera data for video calling while not asking for it for text messaging is an architectural distinction, not a logical contradiction.
- **Omission $\neq$ Proof of Non-Occurrence**: If a privacy policy fails to mention whether device identifiers are shared with advertisers, an auditor cannot assume they are *never* shared. In our system, missing evidence is strictly labeled **`AMBIGUOUS`** (confidence 0.30–0.40). We never falsely label an omission as `NOT_FDO` (compliant), preserving legal and scientific auditing integrity.

### Question 6: What are the primary current limitations of the project?
**Answer**:  
1. **External LLM Dependency**: Extraction requires Google Gemini. Without an active API key, the system falls back to a basic regex parser that only detects 4 hardcoded keywords.
2. **Local Triple Store Process**: The semantic branch requires an external Java process (Apache Jena Fuseki) running locally on port 3030.
3. **Taxonomy Breadth**: The system uses a controlled set of 18 normalized data type tokens and 14 purpose categories. Unmapped data types default to `DATA.OTHER`.
