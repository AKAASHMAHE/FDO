# FDO Privacy Project: Part 2 - NLP, AI, and Data Pipeline Audit

**Project Path:** `C:\FDO`  
**Output Document:** `docs/part2_nlp_ai_data.md`  
**Audit Scope:** Natural Language Processing (NLP), Artificial Intelligence (AI) Models, Machine Learning (ML) Codebases, Data Engineering Pipelines, and Empirical Research Datasets  
**Timestamp:** 2026-10-12  
**Auditor Status:** Automated Assistant (Strict Read-Only Audit)

---

## 1. Inventory of ML / NLP / AI Components

Every computational technique performing language processing, evidence extraction, or classification in `C:\FDO` was inspected to distinguish between learned statistical/neural models and deterministic rule-based algorithms.

### 1.1 Machine Learning and Foundation Model Inventory

| Component / Task | Exact Model Name & Version | Library / SDK & Version | Hyperparameters & Configuration | Consuming Location (`path::function`) | Execution Mode & Training Status | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Privacy Policy Evidence Extraction** | `gemini-3.5-flash-lite` | `google-genai>=0.1.0` (`from google import genai`) | Default generation parameters (no custom `temperature`, `top_p`, or token limits passed; relies on API defaults) | `Backend/app/services/ai_service.py::extract_policy_evidence_with_ai` | **Inference Only (Zero-Shot Prompting).** Zero training, fine-tuning, or parameter optimization code exists in the repository. | `Backend/app/services/ai_service.py:6, 106-110, 208-211` |
| **Conservative Functional Baseline Generation** | `gemini-3.5-flash-lite` | `google-genai>=0.1.0` (`from google import genai`) | Default generation parameters (no custom `temperature`, `top_p`, or token limits passed; relies on API defaults) | `Backend/app/services/ai_service.py::generate_functional_baseline_with_ai` | **Inference Only (Zero-Shot Prompting).** Zero training, fine-tuning, or parameter optimization code exists in the repository. | `Backend/app/services/ai_service.py:6, 335-339, 409-412` |

### 1.2 Non-ML / Rule-Based NLP & Algorithmic Components

The repository contains **no local model weights, no vector embeddings, no Hugging Face transformers, no spaCy language models, no scikit-learn regressors/classifiers, and no PyTorch/TensorFlow code**. All non-Gemini NLP operations are deterministic expert systems:

| Task / Subsystem | Technique Used | Implementation Details | Consuming Location (`path::function`) | Execution Mode | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **HTML Policy Text Ingestion** | HTML Tag Stripping & Parsing | Standard library `html.parser.HTMLParser` (`_TextExtractor`) filtering `<script>`, `<style>`, and `<noscript>` elements; whitespace collapse | `Backend/app/services/policy_discovery_service.py::_TextExtractor` | Deterministic Rule-Based | `Backend/app/services/policy_discovery_service.py:36-59` |
| **Fallback Policy Evidence Extraction** | Regex Sentence Splitting & Keyword Matching | `re.split(r"(?<=[.!?])\s+", text)` with case-insensitive keyword scanning (`location`, `navigation`, `traffic`, `personalization`) | `Backend/app/services/policy_extraction_service.py::extract_policy_evidence` | Deterministic Rule-Based Fallback | `Backend/app/services/policy_extraction_service.py:39-90` |
| **Evidence Quality & Noise Filtering** | Lexical Intersect Validation | Word set intersection against `PRIVACY_DATA_KEYWORDS` (27 items), `PROCESSING_KEYWORDS` (9 items), and `OPERATIONAL_NOISE` (11 phrases) | `Backend/app/services/evidence_validation_service.py::_looks_like_privacy_evidence` | Deterministic Rule-Based Filter | `Backend/app/services/evidence_validation_service.py:107-124` |
| **Purpose Classification** | Lexical Phrase Matching | Multi-phrase substring matching against `PURPOSE_CATEGORIES` (14 controlled taxonomic categories) | `Backend/app/services/comparison_service.py::classify_purposes` | Deterministic Rule-Based Taxonomy | `Backend/app/services/comparison_service.py:3-97, 238-270` |
| **Purpose Compatibility Adjudication** | Matrix Lookup / Equality Rules | Case-insensitive string equality, category containment rules, and promotional purpose rejection | `Backend/app/services/comparison_service.py::classify_purpose_compatibility` | Deterministic Rule-Based Comparator | `Backend/app/services/comparison_service.py:272-380` |
| **Contextual Function Matching** | String Normalization & In-Text Substring Search | Lowercase punctuation stripping (`normalize_purpose`), matching function names/features against evidence purpose/quote | `Backend/app/services/evidence_matcher.py::_text_contains_function_context` | Deterministic Rule-Based Matcher | `Backend/app/services/evidence_matcher.py:21-52` |
| **FDO Compliance Decision Engine** | 6-Rule Decision Tree | Hierarchical Boolean logic checking `evidence_status`, `data_match`, and `purpose_compatibility` | `Backend/app/services/fdo_decision_service.py::evaluate_fdo_decision` | Deterministic Expert System | `Backend/app/services/fdo_decision_service.py:27-147` |
| **Semantic Overreach Detection** | SPARQL Graph Pattern Matching | W3C SPARQL query (`FDO_DETECTION_QUERY`) filtering graph triples where `STR(?expectedType) != STR(?declaredType) || STR(?expectedPurpose) != STR(?declaredPurpose)` | `Backend/app/ontology/fdo_detection_queries.py` & `fuseki_semantic_detector.py::detect_fdo` | Deterministic Semantic Graph Query | `Backend/app/ontology/fdo_detection_queries.py:5-37`, `fuseki_semantic_detector.py:22-52` |

---

## 2. Stage-by-Stage NLP Pipeline Trace

The NLP pipeline transforms raw privacy policy text into structured, normalized, and validated evidence items before feeding the downstream deterministic comparison engine.

```
Raw Policy Input (URL or Text)
          │
          ▼
[ Stage 1: Ingestion & Discovery ]
          │  HTML text stripping / static URL lookup
          ▼
[ Stage 2: Pre-Processing & Cleaning ]
          │  Whitespace normalization, length truncation (1 MB max)
          ▼
[ Stage 3: Sentence Segmentation & Routing ]
          │  Tries Gemini LLM; falls back to regex sentence splitter
          ▼
[ Stage 4: Entity, Purpose & Action Extraction ]
          │  Extracts: data_type, purpose, sharing, retention, quote
          ▼
[ Stage 5: Evidence Validation & Noise Filtering ]
          │  Filters operational noise; requires privacy + processing terms
          ▼
[ Stage 6: Normalization & Ontology Mapping ]
          │  Maps to canonical DATA.* identifiers and PURPOSE_CATEGORIES
          ▼
[ Stage 7: Contextual Evidence Matching ]
          │  Pairs evidence with expected functional mappings
          ▼
Output to Deterministic Comparison Layer
```

### Detailed Pipeline Stages

| Stage Number & Name | Implementing Function (`path::function`) | Input Structure | Output Structure | Method Type | Failure & Error Handling Strategy | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Policy Ingestion & Discovery** | `Backend/app/services/policy_discovery_service.py::discover_privacy_policy` | `application_name: str` | `PolicyDiscoveryResult(success: bool, policy_text: str \| None, source_url: str \| None, error: str \| None)` | Rule-based (static dictionary `KNOWN_POLICY_URLS` for 10 apps + HTTP GET) | Catches `requests.RequestException`; falls back to HTTP status 422 if no policy text is discoverable and none provided by user. | `Backend/app/services/policy_discovery_service.py:137-221` |
| **2. HTML Stripping & Text Extraction** | `Backend/app/services/policy_discovery_service.py::_TextExtractor` | Raw HTML byte stream / string from HTTP response | Clean text string, whitespace normalized, max 1,000,000 bytes | Rule-based (`html.parser.HTMLParser` state machine ignoring `<script>`, `<style>`, `<noscript>`) | Ignores malformed HTML tags gracefully via standard library parser; caps output at `MAX_POLICY_BYTES = 1_000_000`. | `Backend/app/services/policy_discovery_service.py:10, 36-59` |
| **3. Segmentation & Dual-Mode Routing** | `Backend/app/services/policy_extraction_service.py::extract_policy_evidence` | Raw policy text (`str`), `application_name: str` | Dispatched to LLM extractor or fallback regex extractor | Dual-mode router (LLM primary, Rule-based regex fallback) | Wraps Gemini call in `try...except Exception: pass`. If API key missing, quota exceeded, or network fails, immediately diverts to Stage 4B regex fallback. | `Backend/app/services/policy_extraction_service.py:8-36` |
| **4A. Primary LLM Extraction** | `Backend/app/services/ai_service.py::extract_policy_evidence_with_ai` | Policy text (`str`), `application_name: str` | Structured list of candidate evidence dicts (`data_type`, `purpose`, `sharing`, `retention`, `evidence_text`, `confidence`) | LLM Inference (`gemini-3.5-flash-lite` via `google.genai.Client`) | Strips Markdown code blocks; `json.loads` parsing wrapped in `try...except json.JSONDecodeError` returning empty list on malformed JSON. | `Backend/app/services/ai_service.py:81-248` |
| **4B. Fallback Regex Extraction** | `Backend/app/services/policy_extraction_service.py::extract_policy_evidence` (lines 37-90) | Policy text (`str`), `application_name: str` | List of candidate evidence dicts matching regex keywords | Rule-based regex (`re.split(r"(?<=[.!?])\s+", text)`) | Skips blank sentences; assigns fallback confidence = 0.50. | `Backend/app/services/policy_extraction_service.py:37-90` |
| **5. Evidence Validation & Noise Filtering** | `Backend/app/services/evidence_validation_service.py::validate_policy_evidence` | Raw candidate evidence dict list | Filtered list of validated evidence dicts | Rule-based lexical filter | Rejects items matching `OPERATIONAL_NOISE` (11 phrases); rejects items lacking both `PRIVACY_DATA_KEYWORDS` and `PROCESSING_KEYWORDS`; drops invalid confidence scores. | `Backend/app/services/evidence_validation_service.py:107-220` |
| **6. Ontology Term Normalization** | `Backend/app/services/ai_service.py::_normalize_data_type` & `Backend/app/services/comparison_service.py::normalize_purpose` | Raw strings (e.g., `"LOCATION.PRECISE"`, `"turn_by_turn"`) | Canonical ontology identifiers (e.g., `"DATA.LOCATION.PRECISE"`, `"NAVIGATION"`) | Rule-based dictionary lookup & regex normalization | Strips separators (`-`, `_`, `/`), collapses whitespace. Unrecognized data types converted to `None` and dropped; unknown purposes return `None`. | `Backend/app/services/ai_service.py:24-79`, `comparison_service.py:186-210` |
| **7. Functional Baseline Resolution** | `Backend/app/services/functional_baseline_service.py::ensure_functional_baseline` | `Application` ORM object | `BaselineGenerationResult(source='CURATED'\|'AI_DERIVED', available=True, ...)` | Hybrid: SQL query for curated mappings; on cache-miss, invokes `ai_service.py::generate_functional_baseline_with_ai` | If Gemini fails or returns empty functions, marks `available=False`, `status='FAILED'`; downstream analysis skips semantic pass gracefully. | `Backend/app/services/functional_baseline_service.py:160-265` |
| **8. Contextual Evidence Matching** | `Backend/app/services/evidence_matcher.py::find_best_matching_evidence` | Session, policy ID, `ExpectedMapping` | `EvidenceMatch(evidence=PolicyEvidence, status='EXTRACTED'\|'NO_EVIDENCE', reason=str)` | Rule-based SQL selection + purpose keyword overlap search | If no matching data type exists, returns `status='NO_EVIDENCE'`. | `Backend/app/services/evidence_matcher.py:54-193` |
| **9. Purpose Compatibility Evaluation** | `Backend/app/services/comparison_service.py::evaluate_comparison` | `ComparisonInput` | `ComparisonOutput(data_match, purpose_compatibility, functional_relationship, functional_justification)` | Rule-based 14-category taxonomy matching | If declared purpose is absent, marks compatibility as `UNKNOWN` and functional relationship as `UNRELATED`. | `Backend/app/services/comparison_service.py:421-481` |

---

## 3. LLM Integration Specification

The system utilizes Google Gemini (`gemini-3.5-flash-lite`) strictly as a stateless, zero-shot structured text extraction assistant and functional baseline proposer.

### 3.1 Prompt Engineering & Templates

#### Prompt 1: Privacy Policy Evidence Extraction
- **Location:** `Backend/app/services/ai_service.py:112-206`
- **Function:** `extract_policy_evidence_with_ai(policy_text: str, application_name: str) -> list[dict]`
- **System Role / Persona:** *"You are a privacy-policy evidence extraction assistant for the FDO-Privacy project."*
- **Context Injected:** `application_name: str`, raw `policy_text: str`.
- **Negative Constraints (Safety Guardrails):**
  1. *"Extract ONLY actual privacy evidence explicitly supported by the privacy-policy text below."*
  2. *"Do NOT infer information that is not stated."*
  3. *"Do NOT decide whether something is FDO, NOT_FDO, or AMBIGUOUS."*
  4. *"Do NOT extract arbitrary operational statements unless they explicitly describe personal-data collection, use, processing, storage, retention, or sharing."*
- **Ontology Alignment Constraint:** Explicitly mandates output `data_type` must match one of the 11 canonical ontology identifiers: `DATA.LOCATION.PRECISE`, `DATA.LOCATION.APPROXIMATE`, `DATA.LOCATION`, `DATA.CONTACTS`, `DATA.DEVICE`, `DATA.ACCOUNT`, `DATA.FINANCIAL`, `DATA.HEALTH`, `DATA.MEDIA`, `DATA.USAGE`, `DATA.OTHER`. Forbids omitting the `DATA.` prefix.
- **Operational Noise Rejection Instruction:** Specifically lists phrases to reject: *"delivery is retried"*, *"infrastructure reliability"*, *"service availability"*, *"server uptime"*, *"generic system maintenance"*, *"generic technical operation"*.
- **Target JSON Schema:**
  ```json
  {
    "evidence": [
      {
        "data_type": "string or null",
        "purpose": "string or null",
        "entity": "string or null",
        "sharing": "string or null",
        "retention": "string or null",
        "evidence_text": "exact supporting sentence or phrase",
        "source_section": "string or null",
        "confidence": 0.0
      }
    ]
  }
  ```

#### Prompt 2: Conservative Functional Baseline Generation
- **Location:** `Backend/app/services/ai_service.py:341-407`
- **Function:** `generate_functional_baseline_with_ai(application_name: str, category: str, description: str \| None) -> dict \| None`
- **System Role / Persona:** *"You are generating a conservative functional-data baseline for the FDO-Privacy project."*
- **Context Injected:** `application_name`, `category`, `description`. **Crucially, privacy policy text is never passed to this prompt.**
- **Negative Constraints:**
  1. *"Use ONLY the application identity and functional context below."*
  2. *"Do NOT use privacy-policy text."*
  3. *"Do NOT decide FDO, NOT_FDO, or AMBIGUOUS."*
  4. *"Do NOT list every possible personal-data type."*
  5. *"Only include data reasonably necessary for primary application functionality."*
- **Necessity Constraints:** Mandates `necessity` levels as `REQUIRED`, `OPTIONAL`, or `NOT_REQUIRED`. *"Prefer REQUIRED only when the data is clearly needed for primary functionality. Use OPTIONAL for feature-dependent data."*
- **Target JSON Schema:**
  ```json
  {
    "functions": [
      {
        "function_name": "string",
        "description": "string",
        "expected_data": [
          {
            "data_type": "DATA.ACCOUNT",
            "necessity": "REQUIRED",
            "purpose": "short functional purpose",
            "justification": "short justification",
            "confidence": 0.0
          }
        ]
      }
    ]
  }
  ```

### 3.2 Response Parsing & Sanitization Workflow

The Gemini API client returns text responses that may include Markdown formatting or whitespace artifacts. The parsing pipeline (`Backend/app/services/ai_service.py:220-258, 421-440`) enforces:
1. **Markdown Fence Stripping:** Checks whether `raw_text` begins with ` ``` ` or ` ```json `. If present, strips the opening fence line and matching closing ` ``` ` line.
2. **JSON Deserialization:** Passes stripped string to `json.loads(raw_text)`.
3. **Parsing Failure Graceful Recovery:** In `extract_policy_evidence_with_ai`, caught `json.JSONDecodeError` returns `[]`; in `generate_functional_baseline_with_ai`, it returns `None`.
4. **Root Object Verification:** Checks that parsed JSON is a dictionary containing the required root key (`"evidence"` or `"functions"`).

### 3.3 What is Model Output vs What is Independently Validated

The FDO Privacy platform adheres to an **Architectural Isolation Contract**: the LLM is treated as an untrusted candidate generator, and all downstream legal decisions rely on deterministic validation.

| Extracted Field | Status in LLM Response | Independent Validation Performed by Codebase | Validation Function & Location |
| :--- | :--- | :--- | :--- |
| `data_type` | Proposed by model | **Strict Set Validation & Canonical Remapping**: Validated against `VALID_DATA_TYPES` (18 canonical terms). Prefixes like `LOCATION.PRECISE` are forcibly normalized to `DATA.LOCATION.PRECISE`. Any unrecognized data type is rejected and dropped. If `DATA.OTHER`, the text must independently trigger privacy keywords. | `evidence_validation_service.py:145-174`, `ai_service.py:24-36` |
| `evidence_text` | Proposed quote | **Non-Empty & Dual Lexical Intersection Check**: Must not be empty. Combined text and purpose must contain at least one term from `PRIVACY_DATA_KEYWORDS` (27 terms) AND at least one term from `PROCESSING_KEYWORDS` (9 terms). If either is missing, the entire evidence item is discarded. | `evidence_validation_service.py:107-124, 155-164` |
| Operational Noise | Model may hallucinate | **Active Negative Lexical Filter**: If the combined quote and purpose contains any phrase from `OPERATIONAL_NOISE` (11 phrases: *"delivery is retried"*, *"service availability"*, *"system maintenance"*, etc.), the item is stripped. | `evidence_validation_service.py:47-59, 118-120` |
| `confidence` | Numeric float from model | **Range Verification**: Validated by `_valid_confidence()` to ensure `0.0 <= confidence <= 1.0`. Any non-float or out-of-bounds value is set to `None`. | `evidence_validation_service.py:127-140` |
| Evidence Uniqueness | Multiple duplicate items | **Tuple Deduplication**: Items with identical `(data_type, normalized_purpose, normalized_evidence_text)` tuples are deduplicated. | `evidence_validation_service.py:192-219` |
| `purpose` | Proposed text | **Controlled Taxonomy Classification**: Raw text is categorized into 14 controlled classes (`PURPOSE_CATEGORIES`) via deterministic substring matching; the LLM's raw string is never used directly for decision logic. | `comparison_service.py:212-270` |
| **FDO Compliance Decision** | **Excluded from prompt** | **100% Deterministic Code Execution**: The LLM is explicitly forbidden from generating FDO decisions. All classifications (`FDO`, `NOT_FDO`, `AMBIGUOUS`) are calculated by the 6-rule decision tree. | `fdo_decision_service.py:27-147` |

---

## 4. Dataset Inventory & Research Artifacts

The `C:\FDO\DATA` directory contains **51 empirical research datasets** representing the multi-stage research and development lifecycle from initial annotator agreement studies to the frozen master dataset.

### 4.1 Master Ground Truth Datasets (Consumed by Runtime/ETL)

| Dataset File Name | Format | Documented Source | Structure (Rows x Columns) | Core Schema / Entity Attributes | Quality Issues & Anomalies | Consuming Code Location | Operational Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx` | Excel (.xlsx, 56 KB) | Empirical privacy policy curation across 30 mobile applications | **12 sheets**: Stage 3 Dataset (133r x 18c), Applications (31r x 6c), Expected Data (100r x 6c), Policy Registry (31r x 6c), Declared Data (35r x 6c), Evidence (31r x 6c), Exceptions (4r x 6c), QA Freeze (10r x 3c) | `App ID`, `Application`, `Category`, `Function ID`, `Function`, `Expected ID`, `Expected Data Type`, `Necessity`, `Declared ID`, `Raw Policy Term`, `Normalized Data Type ID`, `Policy URL` | In sheet `Stage 4 Input – Blank`, the em-dash in sheet name is rendered as a replacement character `Stage 4 Input  Blank` on Windows CP1252. | `Backend/scripts/import_stage3.py:14-37` | **Primary Ground Truth Seed.** Ingested into SQLite DB as reference vocabulary and application baselines. |
| `FDO-Privacy_Final_Stage3_Dataset_COMPLETE.xlsx` | Excel (.xlsx, 58 KB) | Extended version of Stage 3 Cleaned Dataset with full notes | 12 sheets mirroring Cleaned dataset with additional annotations | Same schema as Cleaned, plus extended audit rationale columns | Minor column padding differences vs Cleaned version | Manual verification | Reference ground truth archive. |

### 4.2 Stage 2B Annotator Agreement Study (15 Files)

| Dataset Group / File | Format | Documented Source | Structure | Schema & Content | Quality Issues | Consuming Code | Operational Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FDO-Privacy_Stage2B_Agreement_Analysis_v1.0.xlsx` & `(1).xlsx` | Excel (.xlsx, 16 KB each) | Independent dual-coder privacy policy annotation study | Agreement Analysis (100r x 14c), Metrics (20r x 2c), Disagreements (2r x 7c), Ontology Revision (4r x 3c) | `App ID`, `Function`, `Data Type`, `Annotator A Code`, `Annotator B Code`, `Agreement (Y/N)`, `Disagreement Category` | `FDO-Privacy_Stage2B_Agreement_Analysis_v1.0 (1).xlsx` is an identical duplicate copy created during file download. | Research documentation | Inter-annotator reliability benchmark (Cohen's Kappa calculation for concept stability). |
| `FDO-Privacy_Stage2B_AnnotatorA_Batch1-4.xlsx` (4 files) | Excel (.xlsx, 8-9 KB each) | Primary Annotator A coding passes | Batches 1 to 4: 25 to 27 rows x 11 columns each; Instructions (6r x 2c) | `Case ID`, `App ID`, `Function ID`, `Declared Data`, `Purpose`, `Coding Decision` | Clean, complete annotation sheets | Research documentation | Raw Annotator A empirical coding records. |
| `FDO-Privacy_Stage2B_AnnotatorB_Batch01-04.xlsx` & `All4Batches.xlsx` (5 files) | Excel (.xlsx, 10-23 KB each) | Secondary Annotator B independent coding passes | `All4Batches`: 100r x 15c; Individual batches: 25 to 27r x 15c each | `Case ID`, `App ID`, `Function ID`, `Declared Data`, `Purpose`, `Coding Decision`, `Rationale` | None | Research documentation | Raw Annotator B empirical coding records. |
| `FDO-Privacy_Stage2B_Pilot_v0.2_VerifiedBatch01` to `v0.5_Batch04.xlsx` (4 files) | Excel (.xlsx, 9 KB each) | Pilot adjudication and verified batch calibration | Batches 01 to 04: 25 to 27r x 12c each; Research Notes (6r x 2c) | `App ID`, `Function`, `Data Type`, `Pilot Code`, `Consensus Code`, `Rule Refinement Notes` | None | Research documentation | Pilot calibration establishing coding guidelines. |

### 4.3 Stage 3 Policy Extraction & Curation History (18 Files)

| Dataset Group / File | Format | Documented Source | Structure | Schema & Content | Quality Issues | Consuming Code | Operational Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FDO-Privacy_Stage3A_Dataset_Schema_v1.0.xlsx` | Excel (.xlsx, 30 KB) | Initial Stage 3 data model specification | Applications (31r x 12c), Expected Data (100r x 15c), Policy Documents (31r x 12c), Declared Data (31r x 16c) | Entity-relationship tables defining relational columns, foreign keys, data dictionaries | Replaced by Stage 3C and Cleaned freeze | Reference documentation | Initial schema baseline for Stage 3. |
| `FDO-Privacy_Stage3B_Policy_Extraction_Batch01-03.xlsx` & `Registry_*.xlsx` (6 files) | Excel (.xlsx, 8-11 KB each) | Batchwise policy scraping and extraction registry | Batches 1 to 3: 9 to 27r x 7 to 13c | `Policy ID`, `App ID`, `Policy URL`, `Effective Date`, `Raw Policy Text`, `Extracted Data Type` | Incremental intermediate batches | Manual verification | Audit trail of raw policy extraction. |
| `FDO-Privacy_Stage3C_Dataset_Freeze_v1.0.xlsx`, `Integration_QA_v1.0.xlsx`, `QA_Remediation_v1.1-1.2.xlsx` (4 files) | Excel (.xlsx, 8-11 KB each) | Quality assurance, integration verification, and freeze gate | 5 to 31r x 2 to 11c | `QA Check`, `Result`, `Issue Description`, `Remediation Action`, `Verified Web Evidence` | Documents edge cases (e.g. Waze navigation evidence remediation) | Manual verification | QA audit trail verifying ground truth consistency. |
| `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.0` to `v1.9_STAGE3_FREEZE_AND_STAGE4_READY.xlsx` (7 files) | Excel (.xlsx, 107-145 KB each) | Multi-pass policy annotation matrix evolving to Stage 4 input readiness | 100r x 17c matrix, plus 3D Official Evidence (21r x 9c), 4D Adjudication (12r x 15c), 4C FDO Candidates (12r x 14c) | `App ID`, `Function ID`, `Expected Data Type`, `Expected Necessity`, `Declared Evidence ID`, `Declared Data Type`, `Declared Purpose`, `Purpose Compatibility`, `FDO Candidate Flag` | Iterative version freeze; v1.9 is the finalized Stage 4 ready version | Research documentation | Pre-adjudication master evidence matrix. |

### 4.4 Stage 4 Empirical Adjudication Ground Truth (9 Files)

| Dataset File Name | Format | Documented Source | Structure | Schema & Content | Quality Issues | Consuming Code | Operational Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FDO-Privacy_Stage4A_Expected_vs_Declared_Matching_v1.0.xlsx` & `FDO_Necessity_Analysis_v1.1.xlsx` (2 files) | Excel (.xlsx, 71 KB & 162 KB) | Systematic pairwise matching of functional necessity against declarations | 94 to 100r x 17c | `App ID`, `Function ID`, `Expected Data Type`, `Necessity Level`, `Declared Data Type`, `Data Match Result (Exact/No Match)` | Contains intermediate working sheets | Research documentation | Ground truth for Stage 4A data-match rules. |
| `FDO-Privacy_Stage4B_Purpose_Compatibility_Review_v1.0.xlsx` & `Purpose_Compatibility_v1.0.xlsx` (2 files) | Excel (.xlsx, 88 KB & 178 KB) | Evaluation of declared collection purposes against functional necessity | 94 to 100r x 15-16c | `App ID`, `Function ID`, `Expected Purpose`, `Declared Purpose`, `Purpose Compatibility (Compatible/Incompatible)`, `Compatibility Rationale` | None | Research documentation | Ground truth for Stage 4B purpose compatibility matrix. |
| `FDO-Privacy_Stage4C_FDO_Candidate_Identification_v1.0.xlsx` & `Candidate_Screening_v1.0.xlsx` (2 files) | Excel (.xlsx, 94 KB & 192 KB) | Screening of potential overreach instances across 30 applications | 12 candidates x 14c; Full screening 94r x 15c | `App ID`, `Application`, `Function`, `Data Type`, `Overreach Type (Purpose/Data/Unnecessary)`, `Candidate Justification` | None | Research documentation | Candidate screening identifying overprivileged features. |
| `FDO-Privacy_Stage4D_Detailed_Adjudication_v1.0.xlsx` & `FDO_Adjudication_v1.0.xlsx` (2 files) | Excel (.xlsx, 209 KB & 101 KB) | Final human expert adjudication of FDO compliance decisions | Detailed: 94r x 18c; Summary: 12r x 15c | `App ID`, `Function ID`, `Expected Data`, `Declared Data`, `Final FDO Decision (FDO / NOT_FDO / AMBIGUOUS)`, `Legal Rationale`, `GDPR Art. 5(1)(c) Compliance Note` | Authoritative human benchmark | Research documentation | **Master Adjudication Benchmark.** Direct ground truth against which automated FDO rules are evaluated. |
| `FDO-Privacy_Stage4E_Ambiguous_Case_Resolution_v1.0.xlsx` | Excel (.xlsx, 224 KB) | Analysis and formal resolution criteria for ambiguous edge cases | 94r x 17c | `App ID`, `Function ID`, `Ambiguity Source`, `Conservative Default Assignment`, `Resolution Condition` | None | Research documentation | Ground truth defining conservative default handling. |

### 4.5 Stage 6 Visualization & Stage 7 Reporting (2 Files)

| Dataset File Name | Format | Documented Source | Structure | Schema & Content | Quality Issues | Consuming Code | Operational Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx` | Excel (.xlsx, 247 KB) | Aggregated empirical results, descriptive statistics, and charts | Stage 6 Findings (6r x 5c), Stage 5 Final Mapping (94r x 17c), Stage 4E Resolution (94r x 17c) | `Metric Category`, `FDO Count`, `NOT_FDO Count`, `Ambiguous Count`, `Percentage Distribution`, `Cross-Category Overreach Frequencies` | Includes embedded Excel charts and pivot tables | Final documentation | Evidentiary tables and figures for patent disclosure and research publication. |
| `FDO-Privacy_Stage7_Final_Research_Report_Package_v1.0.docx` | Word Document (.docx, 40 KB) | Comprehensive research narrative synthesis | Formatted text document (18 pages) | Introduction, Methodology, Stage 1-6 Results, Legal Synthesis, Conclusion | Non-tabular document | Research documentation | Narrative research report. |

---

## 5. End-to-End Data Pipeline Trace

This section traces data from raw external input to final stored representation, explicitly flagging where steps are operational vs **ABSENT**.

```
[1. Policy Ingestion]
   ├── Manual text input (Frontend Form) ──> OPERATIONAL
   └── Automated URL fetch (10 static apps) ──> OPERATIONAL
   └── Automated search engine for unlisted apps ──> ABSENT
          │
          ▼
[2. HTML Sanitization]
   ├── HTML tag stripping (_TextExtractor) ──> OPERATIONAL
   └── 1 MB buffer limit truncation ──> OPERATIONAL
          │
          ▼
[3. Extraction Routing]
   ├── Primary: Gemini 3.5 Flash Lite zero-shot ──> OPERATIONAL
   ├── Fallback: Regex sentence splitting ──> OPERATIONAL
   └── Local embedding / semantic search ──> ABSENT
          │
          ▼
[4. Evidence Cleansing & Filtering]
   ├── Valid data type verification (18 types) ──> OPERATIONAL
   ├── Operational noise stripping (11 phrases) ──> OPERATIONAL
   └── Privacy keyword dual intersection ──> OPERATIONAL
          │
          ▼
[5. Relational Policy Ingestion]
   ├── Persist PolicyDocument in SQLite ──> OPERATIONAL
   └── Persist PolicyEvidence rows in SQLite ──> OPERATIONAL
          │
          ▼
[6. Functional Baseline Resolution]
   ├── Query curated ExpectedMapping (Stage 3 seed) ──> OPERATIONAL
   ├── On-demand Gemini baseline for new app ──> OPERATIONAL
   └── Dynamic API manifest permission ingestion ──> ABSENT
          │
          ▼
[7. Pairwise Matching & Classification]
   ├── Contextual function matching ──> OPERATIONAL
   ├── 14-category purpose classification ──> OPERATIONAL
   └── Compatibility matrix evaluation ──> OPERATIONAL
          │
          ▼
[8. Deterministic Decision Engine]
   ├── 6-rule hierarchical decision tree ──> OPERATIONAL
   └── Persist Comparison, FDOResult, Explanation ──> OPERATIONAL
          │
          ▼
[9. Semantic Knowledge Graph Processing]
   ├── ORM-to-RDF mapping (DBRDFService) ──> OPERATIONAL (requires rdflib)
   ├── RDF individual generation (RDFInstanceBuilder) ──> OPERATIONAL (requires rdflib)
   ├── Serialize Turtle file to disk (.ttl cache) ──> OPERATIONAL
   ├── Clear & upload to Apache Jena Fuseki ──> OPERATIONAL (if Fuseki live)
   ├── Execute SPARQL FDO detection query ──> OPERATIONAL (if Fuseki live)
   └── Persist SemanticFDOResult in SQLite ──> OPERATIONAL
          │
          ▼
[10. Reporting & UI Presentation]
   ├── SQL multi-table joined query ──> OPERATIONAL
   └── JSON payload to React dashboard ──> OPERATIONAL
```

### Detailed Trace of Pipeline Stages

1. **Input Acquisition:**
   - User inputs application name, category, and description via React web UI ([`Frontend/src/App.jsx:1049-1070`](file:///C:/FDO/Frontend/src/App.jsx#L1049-L1070)).
   - Policy text is either pasted directly or discovered via [`policy_discovery_service.py`](file:///C:/FDO/Backend/app/services/policy_discovery_service.py).
   - **ABSENT:** An automated Google/Bing search engine or app store crawler for discovering policy URLs of apps outside the 10 static entries in `KNOWN_POLICY_URLS`.
2. **Text Preprocessing:**
   - Policy HTML is stripped of tags via `_TextExtractor` ([`policy_discovery_service.py:36-59`](file:///C:/FDO/Backend/app/services/policy_discovery_service.py#L36-L59)), collapsing whitespace and enforcing a 1 MB limit.
   - **ABSENT:** Language detection, translation, PDF OCR parsing, or boilerplate header/footer heuristic removal.
3. **Extraction & Routing:**
   - Dispatches text to `extract_policy_evidence_with_ai` using `gemini-3.5-flash-lite` ([`ai_service.py:81-248`](file:///C:/FDO/Backend/app/services/ai_service.py#L81-L248)).
   - If the API fails or key is missing, automatically diverts to the rule-based regex sentence splitter ([`policy_extraction_service.py:37-90`](file:///C:/FDO/Backend/app/services/policy_extraction_service.py#L37-L90)).
   - **ABSENT:** Embedding generation, vector database indexing (no FAISS, Chroma, Pinecone), or dense retrieval.
4. **Validation & Normalization:**
   - Candidate evidence items are strictly filtered by [`evidence_validation_service.py`](file:///C:/FDO/Backend/app/services/evidence_validation_service.py): data types must be in `VALID_DATA_TYPES`, operational noise phrases are stripped, privacy/processing keywords must be present, and duplicate triples are pruned.
5. **Relational Storage:**
   - `create_runtime_policy` ([`policy_ingestion_service.py:16-62`](file:///C:/FDO/Backend/app/services/policy_ingestion_service.py#L16-L62)) inserts records into `policy_documents` and `policy_evidence` tables with generated UUIDs.
6. **Functional Baseline Resolution:**
   - `ensure_functional_baseline` ([`functional_baseline_service.py:160-265`](file:///C:/FDO/Backend/app/services/functional_baseline_service.py#L160-L265)) checks for existing curated mappings. For new applications, invokes Gemini with functional context to generate baseline functions and expected data, storing them in SQLite with prefix `AI_DERIVED:confidence=0.85`.
   - **ABSENT:** Automatic ingestion of real Android `AndroidManifest.xml` permissions or iOS `Info.plist` usage descriptions.
7. **Pairwise Comparison:**
   - `run_analysis` ([`analysis_runner.py:25-257`](file:///C:/FDO/Backend/app/services/analysis_runner.py#L25-L257)) loops through each expected mapping, calls `find_best_matching_evidence` to retrieve matching policy evidence, and calls `evaluate_comparison` ([`comparison_service.py:421-481`](file:///C:/FDO/Backend/app/services/comparison_service.py#L421-L481)) to classify purpose into 14 categories and determine compatibility. Records are persisted in `comparisons`.
8. **Deterministic Adjudication:**
   - `evaluate_fdo_decision` ([`fdo_decision_service.py:27-147`](file:///C:/FDO/Backend/app/services/fdo_decision_service.py#L27-L147)) evaluates the 6-rule decision tree, producing `FDODecisionOutput` (`FDO`, `NOT_FDO`, or `AMBIGUOUS`). Records are stored in `fdo_results` and `explanations`.
   - **ABSENT:** An active-learning feedback loop where human edits retrain a model or automatically modify prompt exemplars.
9. **Semantic Knowledge Graph Transformation & SPARQL Detection:**
   - If functional baseline is available, `DBSemanticResultService` ([`db_semantic_result_service.py:155-253`](file:///C:/FDO/Backend/app/ontology/db_semantic_result_service.py#L155-L253)) queries relational tables via `DBSemanticRepository`, constructs an RDFLib `Graph` via `DBRDFService`, writes a `.ttl` file to `Backend/outputs/semantic/ANALYSIS-{id}.ttl`, uploads the graph to Apache Jena Fuseki on `http://localhost:3030/fdo`, runs `FDO_DETECTION_QUERY`, and stores results in `semantic_fdo_results`.
   - **ABSENT / GRACEFUL:** If Fuseki is offline or RDFLib fails, the error is caught and semantic results default to empty without interrupting the deterministic report.
10. **Report Assembly:**
    - `build_analysis_report` ([`analysis_report_service.py:24-122`](file:///C:/FDO/Backend/app/services/analysis_report_service.py#L24-L122)) executes multi-table SQL joins, combines comparisons, decisions, explanations, and semantic results, returning a validated `AnalysisReportResponse` payload to the React client.

---

## 6. Handoff Notes

### 6.1 Key Findings for IDF-B Preparation
1. **Zero-Training Architectural Novelty:** There is zero neural network training, fine-tuning, or embedding computation in the project. The patent disclosure should focus on the **novel multi-tier architecture** that couples zero-shot LLM evidence extraction with a dual-engine adjudication core (a deterministic taxonomic expert system + an OWL/RDF SPARQL semantic reasoner).
2. **Defensive LLM Isolation:** The LLM prompt design enforces strict negative boundaries: the LLM is explicitly forbidden from making legal compliance determinations or accessing policy text during baseline generation. Downstream Python code performs independent lexical validation and noise filtering before any LLM output touches the decision engine.
3. **Dataset Lineage & Role:** All 51 datasets in `DATA/` represent empirical human research artifacts (inter-annotator reliability studies, Stage 3 curation, and Stage 4 ground truth adjudications). No dataset trains a model; the master dataset (`FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx`) seeds the SQLite relational database via `Backend/scripts/import_stage3.py`.
4. **Implementation Vulnerabilities for Remediation:**
   - `Backend/scripts/import_stage3.py:14-16` hardcodes `D:\VIT\PROJECT\TARP\DATA\...` and must be updated to reference `C:\FDO\DATA\...`.
   - `rdflib>=7.0.0` must be installed in `Backend/.venv` to enable the 38 semantic test files to pass during automated validation.
   - `KNOWN_POLICY_URLS` in `policy_discovery_service.py` is hardcoded to 10 applications; other apps require manual policy text input.

### 6.2 Master Dataset Summary

- **Total Research Dataset Workbooks:** 51 files in `DATA/`.
- **Master Frozen Dataset:** `DATA/FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx` (12 sheets, 30 apps, 99 expected mappings, 30 policies, 34 declared data items).
- **Master Adjudication Benchmark:** `DATA/FDO-Privacy_Stage4D_Detailed_Adjudication_v1.0.xlsx` (94 rows x 18 columns, containing authoritative human compliance decisions).
- **Statistical Findings Summary:** `DATA/FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx` (94 rows x 17 columns).

### 6.3 Open Questions for Part 3 (Ontology, SPARQL & Reasoning Audit)
1. **OWL Reasoner Configuration:** Does the Apache Jena Fuseki setup utilize a generic rule reasoner (`jena:GenericRuleReasoner`), an OWL micro reasoner (`OWL_MEM_MICRO_RULE_INF`), or standard RDFS reasoning when executing `inspect-fdo.rq` and `reasoning-test.rq`?
2. **SPARQL Overreach Query Precision:** Does `FDO_DETECTION_QUERY` in `fdo_detection_queries.py:5-37` produce false positives when an application declares multiple compatible purposes for a single data type before `deduplicate_semantic_results` is called?
3. **Ontology Triples Traceability:** How do the 17 domain classes in `Backend/app/ontology/classes.py` and the object properties in `properties.py` guarantee 100% mathematical mapping to the relational schema in `Backend/app/models/`?
