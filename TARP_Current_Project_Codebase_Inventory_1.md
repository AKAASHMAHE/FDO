# TARP / FDO-Privacy — Current Project Codebase Inventory

**Audit Date:** October 4, 2026  
**Project Name:** FDO-Privacy (Functional Data Ontology based Privacy Policy Analysis)  
**Project Root:** `D:\VIT\PROJECT\TARP`  
**Document Purpose:** Complete, up-to-date, empirical codebase inventory based strictly on the actual files and source code present in the repository.

---

## 1. Complete Directory Tree

Below is the complete directory and file tree of the actual repository, generated via recursive inspection of `D:\VIT\PROJECT\TARP`. Temporary directories (`.git`, `__pycache__`, `.pytest_cache`, `venv`) are omitted for clarity.

```text
TARP/
├── FDO-Privacy_Literature_Survey.docx
├── FDO-Privacy_Project_File_Inventory.md
├── FDO-Privacy_Project_Status.md
├── FDO-Privacy_Stage1_Research_Foundation (1).md
├── FDO-Privacy_Stage2_Functional_Data_Ontology.md
├── Backend/
│   ├── .env (contains environment variables including GEMINI_API_KEY)
│   ├── .gitignore
│   ├── fdo_privacy.db (SQLite database file)
│   ├── test_ai_extraction.py
│   ├── test_gemini.py
│   ├── test_purpose_fdo_integration.py
│   ├── test_purpose_normalization.py
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── init_db.py
│   │   ├── main.py
│   │   ├── requirements.txt (empty, 0 bytes)
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── analysis.py
│   │   │   ├── application.py
│   │   │   ├── base.py
│   │   │   ├── comparison.py
│   │   │   ├── expected_mapping.py
│   │   │   ├── explanation.py
│   │   │   ├── fdo_result.py
│   │   │   ├── function.py
│   │   │   ├── normalized_evidence.py
│   │   │   ├── policy_document.py
│   │   │   └── policy_evidence.py
│   │   ├── schemas/
│   │   │   ├── analysis.py
│   │   │   ├── analysis_result.py
│   │   │   ├── policy_extraction.py
│   │   │   └── rich_report.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── ai_service.py
│   │       ├── analysis_report_service.py
│   │       ├── analysis_result_service.py
│   │       ├── analysis_runner.py
│   │       ├── analysis_service.py
│   │       ├── application_service.py
│   │       ├── comparison_persistence_service.py
│   │       ├── comparison_service.py
│   │       ├── evidence_matcher.py
│   │       ├── evidence_service.py
│   │       ├── expected_mapping_service.py
│   │       ├── explanation_service.py
│   │       ├── fdo_decision_service.py
│   │       ├── function_service.py
│   │       ├── policy_extraction_service.py
│   │       ├── policy_ingestion_service.py
│   │       ├── policy_service.py
│   │       ├── result_service.py
│   │       └── rich_report_service.py
│   └── scripts/
│       ├── import_stage3.py
│       ├── persist_fdo_test.py
│       ├── test_failure_path.py
│       ├── validate_multi_app.py
│       ├── verify_fdo_decision.py
│       └── verify_services.py
├── DATA/
│   ├── FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx
│   ├── FDO-Privacy_Final_Stage3_Dataset_COMPLETE.xlsx
│   ├── FDO-Privacy_Stage2B_Agreement_Analysis_v1.0 (1).xlsx
│   ├── FDO-Privacy_Stage2B_Agreement_Analysis_v1.0.xlsx
│   ├── FDO-Privacy_Stage2B_AnnotatorA_Batch1.xlsx
│   ├── FDO-Privacy_Stage2B_AnnotatorA_Batch2.xlsx
│   ├── FDO-Privacy_Stage2B_AnnotatorA_Batch3.xlsx
│   ├── FDO-Privacy_Stage2B_AnnotatorA_Batch4.xlsx
│   ├── FDO-Privacy_Stage2B_AnnotatorB_All4Batches.xlsx
│   ├── FDO-Privacy_Stage2B_AnnotatorB_Batch01.xlsx
│   ├── FDO-Privacy_Stage2B_AnnotatorB_Batch02.xlsx
│   ├── FDO-Privacy_Stage2B_AnnotatorB_Batch03.xlsx
│   ├── FDO-Privacy_Stage2B_AnnotatorB_Batch04.xlsx
│   ├── FDO-Privacy_Stage2B_Pilot_v0.2_VerifiedBatch01.xlsx
│   ├── FDO-Privacy_Stage2B_Pilot_v0.3_Batch02.xlsx
│   ├── FDO-Privacy_Stage2B_Pilot_v0.4_Batch03.xlsx
│   ├── FDO-Privacy_Stage2B_Pilot_v0.5_Batch04.xlsx
│   ├── FDO-Privacy_Stage3A_Dataset_Schema_v1.0.xlsx
│   ├── FDO-Privacy_Stage3B_Policy_Extraction_Batch01.xlsx
│   ├── FDO-Privacy_Stage3B_Policy_Extraction_Batch01_Complete.xlsx
│   ├── FDO-Privacy_Stage3B_Policy_Extraction_Batch03.xlsx
│   ├── FDO-Privacy_Stage3B_Policy_Registry_Batch01.xlsx
│   ├── FDO-Privacy_Stage3B_Policy_Registry_Batch01_v2.xlsx
│   ├── FDO-Privacy_Stage3B_Policy_Registry_Extraction_Batch02.xlsx
│   ├── FDO-Privacy_Stage3C_Dataset_Freeze_v1.0.xlsx
│   ├── FDO-Privacy_Stage3C_Integration_QA_v1.0.xlsx
│   ├── FDO-Privacy_Stage3C_QA_Remediation_v1.1.xlsx
│   ├── FDO-Privacy_Stage3C_QA_Remediation_v1.2.xlsx
│   ├── FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.0.xlsx
│   ├── FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.1_FILLED.xlsx
│   ├── FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.2_ANNOTATED_BATCH.xlsx
│   ├── FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.3_ANNOTATED_BATCH.xlsx
│   ├── FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.4_ANNOTATED_BATCH.xlsx
│   ├── FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.5_ANNOTATED_BATCH.xlsx
│   ├── FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.6_FINAL_ANNOTATION.xlsx
│   ├── FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.7_COMPLETION_REVIEW.xlsx
│   ├── FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.8_EVIDENCE_REVIEW.xlsx
│   ├── FDO-Privacy_Stage3D_Policy_Evidence_Completion_v1.0.xlsx
│   ├── FDO-Privacy_Stage3D_Policy_Evidence_Completion_v1.1.xlsx
│   ├── FDO-Privacy_Stage3D_v1.9_STAGE3_FREEZE_AND_STAGE4_READY.xlsx
│   ├── FDO-Privacy_Stage4A_Expected_vs_Declared_Matching_v1.0.xlsx
│   ├── FDO-Privacy_Stage4A_FDO_Necessity_Analysis_v1.1.xlsx
│   ├── FDO-Privacy_Stage4B_Purpose_Compatibility_Review_v1.0.xlsx
│   ├── FDO-Privacy_Stage4B_Purpose_Compatibility_v1.0.xlsx
│   ├── FDO-Privacy_Stage4C_FDO_Candidate_Identification_v1.0.xlsx
│   ├── FDO-Privacy_Stage4C_FDO_Candidate_Screening_v1.0.xlsx
│   ├── FDO-Privacy_Stage4D_Detailed_Adjudication_v1.0.xlsx
│   ├── FDO-Privacy_Stage4D_FDO_Adjudication_v1.0.xlsx
│   ├── FDO-Privacy_Stage4E_Ambiguous_Case_Resolution_v1.0.xlsx
│   ├── FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx
│   └── FDO-Privacy_Stage7_Final_Research_Report_Package_v1.0.docx
└── Docs/
    ├── Batch-4_Review_1.docx
    ├── Batch-4_Review_1.pdf
    ├── before_ai_audit.md
    ├── FDO-Privacy_Complete_Project_Status_and_Remaining_Work.md
    ├── FDO-Privacy_Stage8_AI_Responsibilities_Specification_v1.0.md
    ├── FDO-Privacy_Stage8_API_Requirements_Specification_v1.0.md
    ├── FDO-Privacy_Stage8_Data_Flow_Specification_v1.0.md
    ├── FDO-Privacy_Stage8_Data_Model_Specification_v1.0.md
    ├── FDO-Privacy_Stage8_FDO_Decision_Logic_v1.0.md
    ├── FDO-Privacy_Stage8_Input_Output_Specification_v1.0.md
    ├── FDO-Privacy_Stage8_Master_Architecture_Document_v1.0.md
    ├── FDO-Privacy_Stage8_System_Components_v1.0.md
    ├── full idea.md
    └── LITERATURE SURVEY/
        ├── A privacy scoring framework Automation of privacy compliance and risk evaluation with standard indicators.pdf
        ├── A Systematic Mapping Study on Automated Analysis of Privacy Policies.pdf
        ├── A Systematic Review of Privacy Policy Literature.pdf
        ├── Actions Speak Louder than Words Entity-Sensitive Privacy Policy and Data Flow Analysis with PoliCheck.pdf
        ├── Android Permissions Demystified (Stowaway).pdf
        ├── AutoCog Measuring the Description-to-permission Fidelity in Android Applications.pdf
        ├── CompAi A Tool for GDPR Completeness Checking of Privacy Policies using Artificial Intelligence.pdf
        ├── Explainable AI in Usable Privacy and Security Challenges and Opportunities.pdf
        ├── GDPR Compliance in the Context of Continuous Integration.pdf
        ├── GraphCompliance Aligning Policy and Context Graphs for LLM-Based Regulatory Compliance.pdf
        ├── Harnessing Language Models to Analyze Android App Permission Fidelity.pdf
        ├── LADFA A Framework of Using Large Language Models and Retrieval-Augmented Generation for Personal Data Flow Analysis in Privacy Policies.pdf
        ├── Let's Measure the Elephant in the Room Facilitating Personalized Automated Analysis of Privacy Policies at Scale.pdf
        ├── Operationalizing the Legal Principle of Data Minimization for Personalization.pdf
        ├── policylint investigating internal privacy policy contradictions on google play.pdf
        ├── polygraph automated privacy policy analysis using knowledge graphs.pdf
        ├── PrivComp-KG  Leveraging Knowledge Graph and Large Language Models for Privacy Policy Compliance Verification.pdf
        ├── TKPERM Cross-platform Permission Knowledge Transfer to Detect Overprivileged Third-party Applications.pdf
        ├── Using LLMs for Automated Privacy Policy Analysis Prompt Engineering, Fine-Tuning and Explainability.pdf
        └── WHYPER Towards Automating Risk Assessment of Mobile Applications.pdf
```

---

## 2. File-by-File Description

### File
`Backend/app/main.py`
- **Type:** Python Source (FastAPI Application & Router Entry Point)
- **Purpose:** Exposes HTTP REST API endpoints for application querying, policy evidence extraction, runtime FDO analysis execution, and report generation.
- **Main Components:** FastAPI app instance `app`, endpoints: `get_expected_mappings_endpoint`, `health_check`, `get_applications`, `get_application_detail_endpoint`, `get_application_readiness_endpoint`, `extract_policy_endpoint`, `analyze_endpoint`, `get_analysis_results_endpoint`, `get_analysis_report_endpoint`, `get_analysis_endpoint`, `create_analysis_endpoint`.
- **Inputs:** HTTP GET/POST requests containing JSON payloads (e.g. `AnalyzeRequest`, `PolicyExtractionRequest`, `AnalysisCreateRequest`) or path parameters (`application_id`, `analysis_id`).
- **Outputs:** Standardized JSON responses matching Pydantic schemas (`AnalysisReportResponse`, `RichAnalysisReportResponse`, `PolicyExtractionResponse`, etc.).
- **Dependencies:** `fastapi`, `sqlalchemy.orm`, `app.config`, `app.database`, `app.services.*`, `app.schemas.*`.
- **Used By:** External clients, frontend interface, curl/HTTP clients.
- **Project Role:** Core REST API entry point of the software backend.

---

### File
`Backend/app/config.py`
- **Type:** Python Source (Configuration Module)
- **Purpose:** Manages application configuration settings loaded from environment variables and `.env` files.
- **Main Components:** Class `Settings(BaseSettings)` with attributes `app_name`, `app_version`, `environment`, `database_url`; instance `settings`.
- **Inputs:** Environment variables and `Backend/.env` file.
- **Outputs:** Configured `settings` singleton instance.
- **Dependencies:** `pydantic_settings`.
- **Used By:** `Backend/app/database.py`, `Backend/app/main.py`.
- **Project Role:** Central configuration provider.

---

### File
`Backend/app/database.py`
- **Type:** Python Source (Database Connection Manager)
- **Purpose:** Configures SQLAlchemy database engine and session factory for SQLite database interaction.
- **Main Components:** `engine`, `SessionLocal`, dependency function `get_db()`.
- **Inputs:** `settings.database_url` (`sqlite:///./fdo_privacy.db`).
- **Outputs:** SQLAlchemy `Engine`, `sessionmaker` instance, and generator yielding `Session`.
- **Dependencies:** `sqlalchemy`, `app.config`.
- **Used By:** `app/main.py`, `app/init_db.py`, `scripts/import_stage3.py`, `scripts/*.py`.
- **Project Role:** ORM database connection layer.

---

### File
`Backend/app/init_db.py`
- **Type:** Python Source (Database Table Initializer)
- **Purpose:** Creates all database tables defined in SQLAlchemy ORM models if they do not exist.
- **Main Components:** Function `init_db()`.
- **Inputs:** SQLAlchemy `Base.metadata` and `engine`.
- **Outputs:** Creates SQLite tables in `fdo_privacy.db`.
- **Dependencies:** `app.database`, `app.models.base`, `app.models`.
- **Used By:** Command line execution during database setup.
- **Project Role:** Database schema initializer.

---

### File
`Backend/app/services/ai_service.py`
- **Type:** Python Source (AI / Gemini Evidence Extraction Service)
- **Purpose:** Integrates with Google GenAI SDK (`gemini-3.5-flash-lite`) to extract structured privacy policy evidence quotes and canonical data types from raw text.
- **Main Components:** Constants `MODEL_NAME`, `ALLOWED_DATA_TYPES`, `DATA_TYPE_NORMALIZATION`; helper functions `_load_env_file()`, `_normalize_data_type()`; main function `extract_policy_evidence_with_ai(policy_text, application_name)`.
- **Inputs:** `policy_text` (string), `application_name` (string), `GEMINI_API_KEY` from environment.
- **Outputs:** List of extracted evidence dictionaries containing `data_type`, `purpose`, `entity`, `sharing`, `retention`, `evidence_text`, `source_section`, `confidence`.
- **Dependencies:** `google.genai`, `json`, `os`, `pathlib`.
- **Used By:** `app/services/policy_extraction_service.py`.
- **Project Role:** Natural language evidence extraction engine powered by LLM.

---

### File
`Backend/app/services/comparison_service.py`
- **Type:** Python Source (Core Comparison & Purpose Taxonomy Service)
- **Purpose:** Implements deterministic normalization of purpose strings, classification into 13 controlled categories, evaluation of data matching, purpose compatibility, and functional relationships.
- **Main Components:** Constant dict `PURPOSE_CATEGORIES` (13 categories); dataclasses `ComparisonInput`, `ComparisonOutput`; functions `evaluate_data_match`, `normalize_purpose`, `classify_purpose`, `classify_purposes`, `evaluate_purpose_compatibility`, `evaluate_functional_relationship`, `evaluate_evidence_status`, `build_comparison`.
- **Inputs:** `ExpectedMapping` object, `PolicyEvidence` object (or simple namespaces).
- **Outputs:** `ComparisonOutput` dataclass instance containing `data_match`, `purpose_compatibility`, `functional_relationship`, `functional_justification`, `evidence_status`.
- **Dependencies:** `dataclasses`.
- **Used By:** `app/services/analysis_runner.py`, `scripts/verify_fdo_decision.py`, `scripts/persist_fdo_test.py`, `test_purpose_normalization.py`, `test_purpose_fdo_integration.py`.
- **Project Role:** Central comparison and purpose-taxonomy logic module.

---

### File
`Backend/app/services/fdo_decision_service.py`
- **Type:** Python Source (Deterministic FDO Decision Engine)
- **Purpose:** Evaluates comparison inputs against 5 deterministic rules to render final FDO status (`FDO`, `NOT_FDO`, `AMBIGUOUS`).
- **Main Components:** Dataclasses `FDODecisionInput`, `FDODecisionOutput`; main decision function `evaluate_fdo_decision(comparison)`.
- **Inputs:** `FDODecisionInput` object.
- **Outputs:** `FDODecisionOutput` containing `fdo_status`, `decision_reason`, `decision_confidence`.
- **Dependencies:** `dataclasses`.
- **Used By:** `app/services/analysis_runner.py`, `scripts/verify_fdo_decision.py`, `scripts/persist_fdo_test.py`, `test_purpose_fdo_integration.py`.
- **Project Role:** Core deterministic adjudication engine for Functional Data Overreach.

---

### File
`Backend/app/services/analysis_runner.py`
- **Type:** Python Source (End-to-End Analysis Pipeline Executor)
- **Purpose:** Coordinates the complete analysis workflow for an application: retrieves mappings and policy evidence, builds comparisons, evaluates FDO decisions, and persists results to the database.
- **Main Components:** Function `run_analysis(session, analysis_id, application_id, policy_id=None)`.
- **Inputs:** SQLAlchemy `Session`, `analysis_id` (str), `application_id` (str), optional `policy_id` (str).
- **Outputs:** Persisted `Analysis` ORM model instance with updated aggregate counters (`fdo_count`, `not_fdo_count`, `ambiguous_count`).
- **Dependencies:** `sqlalchemy.orm`, `app.models.*`, `app.services.*`.
- **Used By:** `app/main.py` (`/api/v1/analyze`, `/api/v1/analyses`), `scripts/validate_multi_app.py`, `scripts/test_failure_path.py`.
- **Project Role:** Pipeline orchestrator connecting input data, comparison engine, decision logic, and database persistence.

---

### File
`Backend/app/services/evidence_matcher.py`
- **Type:** Python Source (Evidence Matching Service)
- **Purpose:** Queries database to locate declared policy evidence matching an expected data type for a given policy document.
- **Main Components:** Function `find_matching_evidence(session, policy_id, expected_data_type)`.
- **Inputs:** SQLAlchemy `Session`, `policy_id`, `expected_data_type`.
- **Outputs:** `PolicyEvidence` model instance or `None`.
- **Dependencies:** `sqlalchemy.orm`, `app.models.policy_evidence.PolicyEvidence`.
- **Used By:** `app/services/analysis_runner.py`.
- **Project Role:** Evidence retrieval and mapping lookup component.

---

### File
`Backend/app/services/policy_ingestion_service.py`
- **Type:** Python Source (Runtime Policy Ingestion Service)
- **Purpose:** Persists runtime user-submitted privacy policies and AI-extracted evidence as runtime records in the database without modifying frozen benchmark data.
- **Main Components:** Function `create_runtime_policy(session, application_id, policy_text, policy_source, evidence, analysis_id)`.
- **Inputs:** `application_id`, `policy_text`, `policy_source`, list of evidence dicts, `analysis_id`.
- **Outputs:** Persisted `PolicyDocument` ORM record and associated `PolicyEvidence` records.
- **Dependencies:** `datetime`, `uuid`, `sqlalchemy.orm`, `app.models.policy_document`, `app.models.policy_evidence`.
- **Used By:** `app/main.py` (`/api/v1/analyze`).
- **Project Role:** Runtime policy and evidence database persistence handler.

---

### File
`Backend/app/services/policy_extraction_service.py`
- **Type:** Python Source (Policy Extraction Orchestrator & Fallback)
- **Purpose:** Orchestrates policy evidence extraction: calls AI extraction service (`ai_service.py`) first, and falls back to regex sentence splitting if AI extraction fails or returns empty.
- **Main Components:** Function `extract_policy_evidence(policy_text, application_name)`.
- **Inputs:** `policy_text`, `application_name`.
- **Outputs:** List of evidence dictionaries formatted for API output or database insertion.
- **Dependencies:** `re`, `uuid`, `app.services.ai_service`.
- **Used By:** `app/main.py` (`/api/v1/extract-policy`, `/api/v1/analyze`).
- **Project Role:** Evidence extraction facade with graceful fallback.

---

### File
`Backend/app/services/rich_report_service.py`
- **Type:** Python Source (Rich Report Generator)
- **Purpose:** Executes a 6-table SQL join to compile full hierarchical analysis reports including function details, expected data, declared evidence, decision justifications, and explanations.
- **Main Components:** Function `build_rich_analysis_report(session, analysis_id)`.
- **Inputs:** SQLAlchemy `Session`, `analysis_id`.
- **Outputs:** Dict matching `RichAnalysisReportResponse` schema or `None`.
- **Dependencies:** `sqlalchemy.select`, `sqlalchemy.orm`, `app.models.*`.
- **Used By:** `app/main.py` (`/api/v1/analysis/{analysis_id}/report`).
- **Project Role:** Deep report builder for frontend and detailed inspection.

---

### File
`Backend/app/services/analysis_report_service.py`
- **Type:** Python Source (Standard Analysis Report Service)
- **Purpose:** Compiles standard analysis reports containing high-level summary counters, comparisons, and FDO results.
- **Main Components:** Dataclass `AnalysisReport`, function `build_analysis_report(session, analysis_id)`.
- **Inputs:** SQLAlchemy `Session`, `analysis_id`.
- **Outputs:** `AnalysisReport` object or `None`.
- **Dependencies:** `dataclasses`, `sqlalchemy.orm`, `app.services.analysis_service`.
- **Used By:** `app/main.py`.
- **Project Role:** Summary report builder.

---

### File
`Backend/app/services/analysis_result_service.py`
- **Type:** Python Source (Flattened Result Service)
- **Purpose:** Queries and formats flattened analysis results for detailed table display in API endpoints.
- **Main Components:** Function `get_analysis_results(session, analysis_id)`.
- **Inputs:** SQLAlchemy `Session`, `analysis_id`.
- **Outputs:** List of dictionaries matching `AnalysisResultResponse`.
- **Dependencies:** `sqlalchemy.select`, `sqlalchemy.orm`, `app.models.*`.
- **Used By:** `app/main.py` (`/api/v1/analyses/{analysis_id}/results`).
- **Project Role:** Table-oriented result formatter.

---

### File
`Backend/app/services/application_service.py`
- **Type:** Python Source (Application Repository Service)
- **Purpose:** Provides database CRUD and query methods for Application entities and readiness checks.
- **Main Components:** Functions `get_all_applications`, `get_application`, `get_application_readiness`, `find_application_by_name_and_category`.
- **Inputs:** SQLAlchemy `Session`, `application_id`, `application_name`, `category`.
- **Outputs:** `Application` ORM model instances or readiness dicts.
- **Dependencies:** `sqlalchemy.select`, `sqlalchemy.orm`, `app.models.*`.
- **Used By:** `app/main.py`, `app/services/analysis_runner.py`, `scripts/verify_services.py`.
- **Project Role:** Application data access layer.

---

### File
`Backend/app/services/comparison_persistence_service.py`
- **Type:** Python Source (Comparison Persistence Service)
- **Purpose:** Saves calculated comparison results into the `comparisons` database table.
- **Main Components:** Function `save_comparison(session, comparison_id, analysis_id, expected_id, evidence_id, comparison)`.
- **Inputs:** `session`, `comparison_id`, `analysis_id`, `expected_id`, `evidence_id`, `comparison` object.
- **Outputs:** Persisted `Comparison` ORM instance.
- **Dependencies:** `app.models.comparison.Comparison`.
- **Used By:** `app/services/analysis_runner.py`, `scripts/persist_fdo_test.py`.
- **Project Role:** Comparison database persistence layer.

---

### File
`Backend/app/services/evidence_service.py`
- **Type:** Python Source (Evidence Repository Service)
- **Purpose:** Provides query methods for retrieving policy evidence records by policy, data type, or ID.
- **Main Components:** Functions `get_all_evidence`, `get_evidence_by_policy`, `get_evidence_by_data_type`, `get_evidence`.
- **Inputs:** SQLAlchemy `Session`, `policy_id`, `data_type`, `evidence_id`.
- **Outputs:** `PolicyEvidence` ORM instances or lists.
- **Dependencies:** `sqlalchemy.select`, `app.models.policy_evidence.PolicyEvidence`.
- **Used By:** `scripts/verify_services.py`, `scripts/persist_fdo_test.py`, `scripts/verify_fdo_decision.py`.
- **Project Role:** Evidence data access layer.

---

### File
`Backend/app/services/expected_mapping_service.py`
- **Type:** Python Source (Expected Mapping Repository Service)
- **Purpose:** Provides query methods for expected data mappings by application, function, or ID.
- **Main Components:** Functions `get_all_expected_mappings`, `get_expected_mappings_by_application`, `get_expected_mappings_by_function`, `get_expected_mapping`.
- **Inputs:** SQLAlchemy `Session`, `application_id`, `function_record_id`, `expected_id`.
- **Outputs:** `ExpectedMapping` ORM instances or lists.
- **Dependencies:** `sqlalchemy.select`, `app.models.expected_mapping.ExpectedMapping`.
- **Used By:** `app/main.py`, `app/services/analysis_runner.py`, `scripts/verify_services.py`, `scripts/persist_fdo_test.py`.
- **Project Role:** Expected mappings data access layer.

---

### File
`Backend/app/services/explanation_service.py`
- **Type:** Python Source (Explanation Persistence Service)
- **Purpose:** Generates and saves human-readable decision explanations to the `explanations` table.
- **Main Components:** Function `save_explanation(session, result_id, decision, evidence_summary=None, limitations=None)`.
- **Inputs:** `session`, `result_id`, `decision` object.
- **Outputs:** Persisted `Explanation` ORM instance.
- **Dependencies:** `datetime`, `app.models.explanation.Explanation`.
- **Used By:** `app/services/analysis_runner.py`.
- **Project Role:** Explanation persistence layer.

---

### File
`Backend/app/services/function_service.py`
- **Type:** Python Source (Function Repository Service)
- **Purpose:** Provides query methods for application function records.
- **Main Components:** Functions `get_all_functions`, `get_functions_by_application`, `get_function`.
- **Inputs:** SQLAlchemy `Session`, `application_id`, `function_record_id`.
- **Outputs:** `Function` ORM instances or lists.
- **Dependencies:** `sqlalchemy.select`, `app.models.function.Function`.
- **Used By:** `app/main.py`, `scripts/verify_services.py`.
- **Project Role:** Application function data access layer.

---

### File
`Backend/app/services/policy_service.py`
- **Type:** Python Source (Policy Repository Service)
- **Purpose:** Provides query methods for privacy policy documents.
- **Main Components:** Functions `get_all_policy_documents`, `get_policy_documents_by_application`, `get_policy_document`.
- **Inputs:** SQLAlchemy `Session`, `application_id`, `policy_id`.
- **Outputs:** `PolicyDocument` ORM instances or lists.
- **Dependencies:** `sqlalchemy.select`, `app.models.policy_document.PolicyDocument`.
- **Used By:** `app/services/analysis_runner.py`, `scripts/verify_services.py`.
- **Project Role:** Privacy document data access layer.

---

### File
`Backend/app/services/result_service.py`
- **Type:** Python Source (FDO Result Persistence Service)
- **Purpose:** Saves calculated FDO decisions to the `fdo_results` table.
- **Main Components:** Function `save_fdo_result(session, comparison_id, decision)`.
- **Inputs:** `session`, `comparison_id`, `decision` object.
- **Outputs:** Persisted `FDOResult` ORM instance.
- **Dependencies:** `datetime`, `app.models.fdo_result.FDOResult`.
- **Used By:** `app/services/analysis_runner.py`, `scripts/persist_fdo_test.py`.
- **Project Role:** FDO result database persistence layer.

---

### Models Subdirectory (`Backend/app/models/`)
- **`base.py`:** Defines SQLAlchemy `Base(DeclarativeBase)`.
- **`application.py`:** Table `applications` (`application_id` PK, `application_name`, `category`, `description`).
- **`function.py`:** Table `functions` (`function_record_id` PK, `function_id`, `application_id` FK, `function_name`, `feature`, `description`).
- **`expected_mapping.py`:** Table `expected_mappings` (`expected_id` PK, `application_id` FK, `function_record_id` FK, `data_type`, `necessity`, `expected_purpose`, `source_version`).
- **`policy_document.py`:** Table `policy_documents` (`policy_id` PK, `application_id` FK, `source_type`, `source_identifier`, `document_name`, `raw_text`, `retrieved_at`, `created_at`).
- **`policy_evidence.py`:** Table `policy_evidence` (`evidence_id` PK, `policy_id` FK, `data_type`, `purpose`, `entity`, `sharing`, `retention`, `evidence_text`, `source_section`, `extraction_status`, `confidence`).
- **`analysis.py`:** Table `analyses` (`analysis_id` PK, `application_id` FK, `policy_id` FK, `analysis_status`, `total_mappings`, `fdo_count`, `not_fdo_count`, `ambiguous_count`, `created_at`).
- **`comparison.py`:** Table `comparisons` (`comparison_id` PK, `analysis_id` FK, `expected_id` FK, `evidence_id` FK, `data_match`, `purpose_compatibility`, `functional_relationship`, `functional_justification`, `evidence_status`).
- **`fdo_result.py`:** Table `fdo_results` (`result_id` PK, `comparison_id` FK, `fdo_status`, `decision_reason`, `decision_confidence`, `created_at`).
- **`explanation.py`:** Table `explanations` (`explanation_id` PK, `result_id` FK, `explanation_text`, `evidence_summary`, `limitations`, `created_at`).
- **`normalized_evidence.py`:** Table `normalized_evidence` (`normalized_id` PK, `evidence_id` FK, `normalized_data_type`, `normalized_purpose`, `normalization_note`, `normalization_status`).

---

### Schemas Subdirectory (`Backend/app/schemas/`)
- **`analysis.py`:** Defines API Pydantic schemas: `AnalysisCreateRequest`, `ComparisonResponse`, `FDOResultResponse`, `AnalysisReportResponse`, `ApplicationResponse`, `ApplicationReadinessResponse`, `FunctionResponse`, `ApplicationDetailResponse`, `ExpectedMappingResponse`, `ExpectedMappingsResponse`, `AnalyzeRequest`.
- **`analysis_result.py`:** Schema `AnalysisResultResponse` for flat result list output.
- **`policy_extraction.py`:** Schemas `PolicyExtractionRequest`, `PolicyEvidenceResponse`, `PolicyExtractionResponse`.
- **`rich_report.py`:** Schemas `RichApplicationResponse`, `RichFunctionResponse`, `RichEvidenceResponse`, `RichAnalysisResultResponse`, `RichAnalysisSummaryResponse`, `RichAnalysisReportResponse`.

---

### Scripts Subdirectory (`Backend/scripts/`)
- **`import_stage3.py`:** Imports Stage 3 benchmark Excel dataset (`FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx`) into SQLite database (`fdo_privacy.db`), inserting 27 applications, 88 functions, 99 expected mappings, 27 policy documents, and 93 evidence records.
- **`persist_fdo_test.py`:** Integration script testing database transaction commits for analyses, comparisons, and results.
- **`test_failure_path.py`:** Integration test verifying that invalid application requests trigger database transaction rollbacks.
- **`validate_multi_app.py`:** Validation script running full analysis across 4 applications (`AMB-01`, `EDU-02`, `FIT-01`, `FOD-01`) and confirming mathematical equality of counters (`total_mappings == fdo_count + not_fdo_count + ambiguous_count`).
- **`verify_fdo_decision.py`:** Diagnostic script testing single decision execution on real database records (`EXP-099` & `DEC-101`).
- **`verify_services.py`:** Integration script verifying data access service loading across applications, functions, mappings, policies, and evidence.

---

### Root Test Files (`Backend/`)
- **`test_purpose_normalization.py`:** Unit test file containing 42 test functions covering purpose normalization, single-category classification, multi-category classification, and semantic compatibility.
- **`test_purpose_fdo_integration.py`:** Integration test file containing 4 test functions verifying that purpose compatibility outputs properly drive FDO decision engine status (`FDO` vs `NOT_FDO`).
- **`test_ai_extraction.py`:** Script testing live AI evidence extraction using `extract_policy_evidence_with_ai`.
- **`test_gemini.py`:** API verification script testing raw Google GenAI API connection to `gemini-3.5-flash-lite`.

---

## 3. Backend Architecture

### Architecture Flow
The actual backend architecture follows a strict decoupled, 10-step flow from user input to persistent database storage and structured JSON output:

```text
User Input (Policy Text + App Name / Category)
  │
  ▼
API Endpoint (`POST /api/v1/analyze`) [Backend/app/main.py]
  │
  ▼
AI Evidence Extraction [Backend/app/services/ai_service.py via policy_extraction_service.py]
  ├─ Provider: Google GenAI SDK (`google.genai`)
  ├─ Model: `gemini-3.5-flash-lite`
  └─ Output: JSON Array of structured evidence quotes & canonical data types
  │
  ▼
Runtime Policy & Evidence Ingestion [Backend/app/services/policy_ingestion_service.py]
  └─ Writes isolated `AI-POL-*` policy and `AI-*` evidence records into SQLite DB
  │
  ▼
Analysis Pipeline Orchestration [Backend/app/services/analysis_runner.py]
  │
  ├─► Evidence Matching [Backend/app/services/evidence_matcher.py]
  │     └─ Matches expected data type against declared policy evidence records
  │
  ├─► Comparison Engine [Backend/app/services/comparison_service.py]
  │     ├─ Data Matching (`evaluate_data_match`: EXACT_MATCH / NO_MATCH / NO_EVIDENCE)
  │     ├─ Purpose Normalization (`normalize_purpose`: lowercases, strips hyphens/slashes)
  │     ├─ Purpose Classification (`classify_purposes`: matches into 13 controlled taxonomy categories)
  │     ├─ Purpose Compatibility (`evaluate_purpose_compatibility`: COMPATIBLE / INCOMPATIBLE / NO_EVIDENCE)
  │     └─ Evidence Status (`evaluate_evidence_status`: EXTRACTED / INSUFFICIENT / NO_EVIDENCE)
  │
  ├─► Deterministic FDO Decision Engine [Backend/app/services/fdo_decision_service.py]
  │     └─ Applies 5 deterministic rules -> `NOT_FDO` / `FDO` / `AMBIGUOUS` with confidence score
  │
  └─► Database Persistence & Explanations
        ├─ Saves `Comparison` records [comparison_persistence_service.py]
        ├─ Saves `FDOResult` records [result_service.py]
        └─ Saves `Explanation` text [explanation_service.py]
  │
  ▼
Database Transaction Commit [Backend/app/database.py -> fdo_privacy.db]
  │
  ▼
Rich Report Builder [Backend/app/services/rich_report_service.py]
  └─ Executes SQL joins across 6 tables to structure hierarchical response
  │
  ▼
JSON API Response (`RichAnalysisReportResponse`)
```

---

## 4. Test Suite Analysis

### Discovered Test Files
1. `Backend/test_purpose_normalization.py` (42 unit test functions)
2. `Backend/test_purpose_fdo_integration.py` (4 integration test functions)
3. `Backend/test_ai_extraction.py` (Manual AI test script)
4. `Backend/test_gemini.py` (Gemini API diagnostic script)

### Production Files Exercised
- `Backend/app/services/comparison_service.py` (`normalize_purpose`, `classify_purpose`, `classify_purposes`, `evaluate_purpose_compatibility`, `build_comparison`)
- `Backend/app/services/fdo_decision_service.py` (`FDODecisionInput`, `evaluate_fdo_decision`)
- `Backend/app/services/ai_service.py` (`extract_policy_evidence_with_ai`)

### Test Execution Results
- **Command Executed:** Python test discovery runner loading functions from test files
- **Python Version:** 3.10.11 (Windows)
- **Total Discovered Tests:** 46
- **Results:**
  - `test_purpose_normalization.py`: **42 passed**, 0 failed
  - `test_purpose_fdo_integration.py`: **4 passed**, 0 failed
  - **Overall Total:** **46 PASSED**, **0 FAILING**, **0 SKIPPED**

*Note on test runner:* `pytest` CLI tool was not pre-installed in the default global Windows Python path, but running all 46 test functions directly via Python confirmed 100% pass rate.

---

## 5. Current Implementation Status

### IMPLEMENTED
- **Deterministic FDO Decision Engine:** Complete 5-rule decision logic in `fdo_decision_service.py`.
- **Purpose Normalization & Classification:** String normalization and 13-category phrase matching in `comparison_service.py`.
- **Multi-Purpose & Semantic Compatibility:** Evaluating multi-phrase declarations against expected functional purpose categories.
- **AI Policy Evidence Extraction:** Live Gemini API integration using `gemini-3.5-flash-lite` in `ai_service.py`.
- **SQLite Database Layer:** 10 SQLAlchemy ORM tables initialized in `fdo_privacy.db`.
- **Benchmark Data Import:** Automated Excel importer in `scripts/import_stage3.py` for Stage 3 benchmark dataset.
- **FastAPI REST API:** 10 endpoints implemented in `app/main.py`.
- **Rich Analysis Reporting:** Hierarchical report generator with 6-table join in `rich_report_service.py`.
- **Unit Test Suite:** 46 passing unit tests.

### PARTIALLY IMPLEMENTED
- **Fallback Regex Policy Extraction:** Basic sentence splitting in `policy_extraction_service.py` when AI API is unavailable.

### PLACEHOLDER / STUB
- **`Backend/app/requirements.txt`:** Currently an empty file (0 bytes).

### NOT FOUND
- **OWL / RDF / SPARQL Files:** No `.owl`, `.ttl`, `.rdf`, or `.sparql` files exist in the code repository.
- **Graph Database / Reasoners:** No Neo4j, Apache Jena, Fuseki, or Pellet integration exists in code.
- **Frontend UI:** No web frontend codebase (React/Vue/HTML) is present in the repository.

---

## 6. Data Directory

The `DATA/` directory contains 46 Excel files (`.xlsx`) and 1 Word document (`.docx`) representing research datasets across project stages:

| Dataset / File | Rows / Size | Format | Content / Purpose | Used By Component | Category |
|---|---|---|---|---|---|
| `FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx` | 4 sheets, ~100 rows | XLSX | Cleaned Stage 3 benchmark dataset (Apps, Expected Data, Policy Registry, Declared Data) | `scripts/import_stage3.py` | Benchmark Dataset |
| `FDO-Privacy_Final_Stage3_Dataset_COMPLETE.xlsx` | 4 sheets, ~100 rows | XLSX | Complete Stage 3 benchmark dataset with raw notes | Historical Research | Benchmark Dataset |
| `FDO-Privacy_Stage2B_Agreement_Analysis_v1.0 (1).xlsx` | ~50 rows | XLSX | Annotator inter-rater agreement calculation | Historical Research | Pilot / Annotations |
| `FDO-Privacy_Stage2B_AnnotatorA_Batch1.xlsx` - `Batch4.xlsx` | 4 files, ~25 rows each | XLSX | Annotator A pilot mappings | Historical Research | Pilot Annotations |
| `FDO-Privacy_Stage2B_AnnotatorB_Batch01.xlsx` - `Batch04.xlsx` | 5 files | XLSX | Annotator B pilot mappings | Historical Research | Pilot Annotations |
| `FDO-Privacy_Stage3A_Dataset_Schema_v1.0.xlsx` | ~30 rows | XLSX | Dataset schema specifications | Historical Research | Schema Spec |
| `FDO-Privacy_Stage3B_Policy_Registry_Batch01.xlsx` - `Batch03` | 6 files | XLSX | Raw policy text extraction and URL registry | Historical Research | Policy Registry |
| `FDO-Privacy_Stage3C_Dataset_Freeze_v1.0.xlsx` | ~99 rows | XLSX | Dataset freeze state prior to adjudication | Historical Research | Benchmark Freeze |
| `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.0` - `v1.8` | 9 files | XLSX | Iterative annotation matrices for declared evidence | Historical Research | Evidence Annotation |
| `FDO-Privacy_Stage3D_v1.9_STAGE3_FREEZE_AND_STAGE4_READY.xlsx` | ~145 KB | XLSX | Final Stage 3 freeze matrix ready for Stage 4 | Historical Research | Benchmark Freeze |
| `FDO-Privacy_Stage4A_Expected_vs_Declared_Matching_v1.0.xlsx` | ~70 KB | XLSX | Stage 4A expected vs declared data matching results | Historical Research | Adjudication Data |
| `FDO-Privacy_Stage4A_FDO_Necessity_Analysis_v1.1.xlsx` | ~162 KB | XLSX | Stage 4A functional necessity evaluations | Historical Research | Adjudication Data |
| `FDO-Privacy_Stage4B_Purpose_Compatibility_Review_v1.0.xlsx` | 2 files | XLSX | Stage 4B purpose compatibility evaluations | Historical Research | Adjudication Data |
| `FDO-Privacy_Stage4C_FDO_Candidate_Identification` & `Screening` | 2 files | XLSX | Candidate identification and screening queues | Historical Research | Adjudication Data |
| `FDO-Privacy_Stage4D_Detailed_Adjudication_v1.0.xlsx` | ~209 KB | XLSX | Multi-test FDO manual adjudication records | Historical Research | Adjudication Data |
| `FDO-Privacy_Stage4E_Ambiguous_Case_Resolution_v1.0.xlsx` | ~224 KB | XLSX | Detailed resolution of ambiguous policy cases | Historical Research | Adjudication Data |
| `FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx` | ~247 KB | XLSX | Research findings and chart data | Historical Research | Visualization Data |
| `FDO-Privacy_Stage7_Final_Research_Report_Package_v1.0.docx` | ~40 KB | DOCX | Final research report text | Historical Research | Final Research Paper |

---

## 7. Ontology / Knowledge Graph

### Search Findings
A repository-wide search for `.owl`, `.ttl`, `.rdf`, `.sparql`, `rdflib`, `owlready2`, `neo4j`, `pyfuseki`, and `jena` revealed **zero** ontology/graph implementation files.

### Actual Code Implementation
In the active codebase, "Ontology" refers to:
1. **Canonical Data Type Identifiers:** Standardized strings (`DATA.LOCATION.PRECISE`, `DATA.LOCATION.APPROXIMATE`, `DATA.LOCATION`, `DATA.CONTACTS`, `DATA.DEVICE`, `DATA.ACCOUNT`, `DATA.FINANCIAL`, `DATA.HEALTH`, `DATA.MEDIA`, `DATA.USAGE`, `DATA.OTHER`) enforced in `ai_service.py` and stored in SQLite database under `expected_mappings.source_version`.
2. **Controlled Purpose Categories:** A python dictionary `PURPOSE_CATEGORIES` in `app/services/comparison_service.py` containing keyword/phrase sets for 13 purpose categories (`NAVIGATION`, `COMMUNICATION`, `SOCIAL_INTERACTION`, `ACCOUNT_MANAGEMENT`, `PAYMENT_PROCESSING`, `MEDIA`, `SEARCH`, `SECURITY`, `SERVICE_OPERATION`, `ANALYTICS`, `PERSONALIZATION`, `ADVERTISING`, `MARKETING`).

Semantic reasoning is executed via Python comparison logic, not OWL Description Logic reasoners or SPARQL query engines.

---

## 8. AI / NLP Components

### Implementation Details
- **Provider:** Google GenAI SDK (`google.genai`)
- **Model:** `gemini-3.5-flash-lite`
- **Source File:** `Backend/app/services/ai_service.py`
- **Role:** AI is strictly scoped to evidence extraction (`extract_policy_evidence_with_ai`). It extracts structured JSON containing evidence text, source sections, data types, and purposes.
- **Strict Guardrails:** The prompt explicitly instructs Gemini: *"Do NOT decide whether something is FDO, NOT_FDO, or AMBIGUOUS."*
- **Fallback Mechanism:** `policy_extraction_service.py` falls back to regex sentence splitting if Gemini fails or returns invalid JSON.
- **Secrets Management:** `Backend/.env` contains `GEMINI_API_KEY`. (File is present locally; secret values are kept private).

---

## 9. Database

### Implementation Details
- **Database Engine:** SQLite 3 (`Backend/fdo_privacy.db`)
- **ORM Layer:** SQLAlchemy 2.0 (`DeclarativeBase`)
- **Configuration File:** `Backend/app/database.py`
- **Initialization File:** `Backend/app/init_db.py`

### Table Definitions & Relationships

```text
applications (application_id [PK], application_name, category, description)
  │
  ├──► functions (function_record_id [PK], function_id, application_id [FK], function_name, feature, description)
  │      │
  │      └──► expected_mappings (expected_id [PK], application_id [FK], function_record_id [FK], data_type, necessity, expected_purpose, source_version)
  │             │
  │             └──► comparisons (comparison_id [PK], analysis_id [FK], expected_id [FK], evidence_id [FK], data_match, purpose_compatibility, functional_relationship, functional_justification, evidence_status)
  │                    │
  │                    └──► fdo_results (result_id [PK], comparison_id [FK], fdo_status, decision_reason, decision_confidence, created_at)
  │                           │
  │                           └──► explanations (explanation_id [PK], result_id [FK], explanation_text, evidence_summary, limitations, created_at)
  │
  └──► policy_documents (policy_id [PK], application_id [FK], source_type, source_identifier, document_name, raw_text, retrieved_at, created_at)
         │
         └──► policy_evidence (evidence_id [PK], policy_id [FK], data_type, purpose, entity, sharing, retention, evidence_text, source_section, extraction_status, confidence)
                │
                └──► normalized_evidence (normalized_id [PK], evidence_id [FK], normalized_data_type, normalized_purpose, normalization_note, normalization_status)

analyses (analysis_id [PK], application_id [FK], policy_id [FK], analysis_status, total_mappings, fdo_count, not_fdo_count, ambiguous_count, created_at)
```

---

## 10. Configuration / Environment

- **Python Environment:** Python 3.10
- **Configuration Module:** `Backend/app/config.py` using `pydantic-settings`
- **Environment File:** `Backend/.env` present
- **Key Dependencies:** `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `pydantic-settings`, `google-genai`, `pandas`, `openpyxl`
- **Dependency File Status:** `Backend/app/requirements.txt` exists but is currently 0 bytes.

---

## 11. Documentation Inventory & Discrepancy Analysis

### Documentation Files Inspected
1. `FDO-Privacy_Project_Status.md` (Root status document)
2. `Docs/FDO-Privacy_Complete_Project_Status_and_Remaining_Work.md`
3. `Docs/FDO-Privacy_Stage8_Master_Architecture_Document_v1.0.md`
4. `Docs/FDO-Privacy_Stage8_System_Components_v1.0.md`
5. `Docs/FDO-Privacy_Stage8_FDO_Decision_Logic_v1.0.md`
6. `Docs/before_ai_audit.md`
7. `Docs/full idea.md`

### Discrepancy Analysis: Documentation vs. Actual Code

#### Discrepancy 1: Graph Database / Knowledge Graph
- **DOCUMENTATION SAYS:** System architecture uses a Knowledge Graph (Neo4j / Apache Jena) and RDF triples for ontology reasoning (`FDO-Privacy_Stage8_Master_Architecture_Document_v1.0.md`).
- **ACTUAL CODE SHOWS:** SQLite relational database with SQLAlchemy ORM and Python dictionary rule engine (`app/database.py`, `comparison_service.py`). No Neo4j or Jena integration exists.

#### Discrepancy 2: OWL Reasoner
- **DOCUMENTATION SAYS:** Ontology reasoning is performed using OWL DL reasoners (Pellet / HermiT) to deduce classification (`FDO-Privacy_Stage2_Functional_Data_Ontology.md`).
- **ACTUAL CODE SHOWS:** Purpose normalization, classification, and compatibility are executed in pure Python in `Backend/app/services/comparison_service.py`. No `.owl` files or OWL reasoners are present.

#### Discrepancy 3: Requirements File
- **DOCUMENTATION SAYS:** Package dependencies are pinned in `Backend/app/requirements.txt`.
- **ACTUAL CODE SHOWS:** `Backend/app/requirements.txt` is an empty 0-byte file.

---

## 12. Dependency Map

The diagram below illustrates module-level dependency relationships confirmed from actual import statements in the codebase:

```text
FastAPI Router [app/main.py]
  │
  ├──► Policy Extraction Service [app/services/policy_extraction_service.py]
  │      └──► AI Service [app/services/ai_service.py]
  │             └──► Google GenAI Client (`google.genai`)
  │
  ├──► Policy Ingestion Service [app/services/policy_ingestion_service.py]
  │      └──► Policy & Evidence Models [app/models/policy_document.py, policy_evidence.py]
  │
  ├──► Analysis Runner [app/services/analysis_runner.py]
  │      ├──► Evidence Matcher [app/services/evidence_matcher.py]
  │      ├──► Comparison Service [app/services/comparison_service.py]
  │      ├──► FDO Decision Service [app/services/fdo_decision_service.py]
  │      ├──► Comparison Persistence Service [app/services/comparison_persistence_service.py]
  │      ├──► Result Service [app/services/result_service.py]
  │      └──► Explanation Service [app/services/explanation_service.py]
  │
  ├──► Rich Report Service [app/services/rich_report_service.py]
  │      └──► SQLAlchemy Models [app/models/*]
  │
  └──► Database Engine [app/database.py]
         └──► Configuration Settings [app/config.py]
```

---

## 13. End-to-End Current Flow

1. **Input Reception:** Request arrives at `POST /api/v1/analyze` in `app/main.py` with `application_name`, `category`, and `policy_text`.
2. **Application Resolution:** `find_application_by_name_and_category` matches app against `applications` table in SQLite.
3. **AI Evidence Extraction:** `extract_policy_evidence` calls `extract_policy_evidence_with_ai` (`ai_service.py`), passing prompt to Gemini API (`gemini-3.5-flash-lite`).
4. **Evidence Parsing:** Gemini returns JSON containing quotes and canonical data types (`DATA.LOCATION.PRECISE`, etc.).
5. **Runtime Ingestion:** `create_runtime_policy` (`policy_ingestion_service.py`) writes `AI-POL-*` document and `AI-*` evidence records into SQLite database.
6. **Expected Mappings Retrieval:** `run_analysis` (`analysis_runner.py`) loads baseline expected mappings for the application.
7. **Comparison Execution:** `build_comparison` (`comparison_service.py`) evaluates expected vs declared data match, normalizes purposes, classifies into taxonomy categories, and checks purpose compatibility.
8. **Deterministic Adjudication:** `evaluate_fdo_decision` (`fdo_decision_service.py`) evaluates the comparison against 5 rules, returning `NOT_FDO`, `FDO`, or `AMBIGUOUS` with confidence score.
9. **Result Persistence:** Comparison, result, and explanation records are written to SQLite and committed via database transaction.
10. **Report Delivery:** `build_analysis_report` / `build_rich_analysis_report` constructs response JSON returned to client.

---

## 14. Important Current FDO Logic

| Rule / Step | Logic / Condition | Decision Output | Source File & Function |
|---|---|---|---|
| **Data Match** | `expected_data_type == declared_data_type` | `EXACT_MATCH` / `NO_MATCH` / `NO_EVIDENCE` | `comparison_service.py` -> `evaluate_data_match()` |
| **Purpose Normalization** | Lowercase, strip punctuation (`-`, `_`, `/`), collapse spaces | Normalized string | `comparison_service.py` -> `normalize_purpose()` |
| **Purpose Classification** | Match normalized string against 13 `PURPOSE_CATEGORIES` | List of category strings | `comparison_service.py` -> `classify_purposes()` |
| **Purpose Compatibility** | `expected_category in declared_categories` | `COMPATIBLE` / `INCOMPATIBLE` / `NO_EVIDENCE` | `comparison_service.py` -> `evaluate_purpose_compatibility()` |
| **Rule 1: No Evidence** | `evidence_status == "NO_EVIDENCE"` | `AMBIGUOUS` (Conf: 0.30) | `fdo_decision_service.py` -> `evaluate_fdo_decision()` |
| **Rule 2: Insufficient Evidence** | `evidence_status in {"INSUFFICIENT", "UNKNOWN"}` | `AMBIGUOUS` (Conf: 0.40) | `fdo_decision_service.py` -> `evaluate_fdo_decision()` |
| **Rule 3: Compatible Purpose** | `EXACT_MATCH` + `COMPATIBLE` + `RELATED` + `EXTRACTED` | `NOT_FDO` (Conf: 0.90) | `fdo_decision_service.py` -> `evaluate_fdo_decision()` |
| **Rule 4: Incompatible Purpose**| `EXACT_MATCH` + `INCOMPATIBLE` + `RELATED` + `EXTRACTED` | `FDO` (Conf: 0.85) | `fdo_decision_service.py` -> `evaluate_fdo_decision()` |
| **Rule 5: Mismatched Data** | `NO_MATCH` + `RELATED` + `EXTRACTED` | `FDO` (Conf: 0.80) | `fdo_decision_service.py` -> `evaluate_fdo_decision()` |
| **Fallback Rule** | No rule matched | `AMBIGUOUS` (Conf: 0.50) | `fdo_decision_service.py` -> `evaluate_fdo_decision()` |

---

## 15. Current Test Health

- **Execution Command:** Python test discovery runner executing functions in test modules
- **Test Results Summary:**
  - Total unit tests executed: **46**
  - Total passed: **46**
  - Total failed: **0**
  - Total skipped: **0**
- **Specific Test Categories Verified:**
  - Purpose normalization & whitespace handling: **Passed**
  - Single-category & multi-category classification: **Passed**
  - Semantic purpose compatibility (e.g. "navigation" vs "directions"): **Passed**
  - Purpose FDO decision integration (e.g. compatible -> `NOT_FDO`, incompatible -> `FDO`): **Passed**

---

## 16. Project Completion Matrix

| Component | Status | Source Files | Tests | Notes |
|---|---|---|---|---|
| **Purpose Normalization** | IMPLEMENTED | `app/services/comparison_service.py` | `test_purpose_normalization.py` | Normalizes text, hyphens, slashes, whitespace |
| **Purpose Classification** | IMPLEMENTED | `app/services/comparison_service.py` | `test_purpose_normalization.py` | 13 controlled purpose categories |
| **Multi-Purpose Compatibility**| IMPLEMENTED | `app/services/comparison_service.py` | `test_purpose_normalization.py` | Resolves multi-phrase purpose statements |
| **FDO Decision Engine** | IMPLEMENTED | `app/services/fdo_decision_service.py` | `test_purpose_fdo_integration.py` | 5 deterministic rules with confidence scoring |
| **NLP Evidence Extraction** | IMPLEMENTED | `app/services/policy_extraction_service.py` | Manual / Fallback regex | AI extraction with regex fallback |
| **AI Integration** | IMPLEMENTED | `app/services/ai_service.py` | `test_ai_extraction.py`, `test_gemini.py` | Google GenAI `gemini-3.5-flash-lite` |
| **Ontology (Canonical Types)** | IMPLEMENTED | `app/services/ai_service.py`, `comparison_service.py` | Indirectly via services | Canonical strings & purpose dict; no OWL files |
| **Knowledge Graph** | NOT FOUND | None | None | Planned/documented only; no Neo4j/Jena code |
| **Reasoning Engine** | IMPLEMENTED | `app/services/fdo_decision_service.py` | Unit test suite | Pure Python rule engine |
| **Database Layer** | IMPLEMENTED | `app/database.py`, `app/models/*` | `scripts/persist_fdo_test.py` | SQLite DB with 10 SQLAlchemy ORM tables |
| **API Layer** | IMPLEMENTED | `app/main.py`, `app/schemas/*` | `scripts/validate_multi_app.py` | 10 FastAPI HTTP REST endpoints |
| **Frontend UI** | NOT FOUND | None | None | No web UI present in repository |

---

## 17. Remaining Work

### Critical
1. **Populate Dependencies File:** Fill `Backend/app/requirements.txt` with exact package dependencies (`fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `pydantic-settings`, `google-genai`, `pandas`, `openpyxl`, `pytest`).
   - *Why needed:* Standardized deployment and CI environment reproducibility.
   - *Files involved:* `Backend/app/requirements.txt`.
2. **Configure pytest Setup:** Add `pyproject.toml` or `pytest.ini` to configure pytest discovery path so `python -m pytest` runs seamlessly without custom scripts.
   - *Files involved:* `Backend/pyproject.toml`.

### Important
1. **Interactive Web Frontend UI:** Build a simple web dashboard (React, Vue, or HTML/JS) to interact with `/api/v1/analyze` and display rich reports visually.
   - *Why needed:* Demonstrating system capabilities to non-technical users and reviewers.
   - *Files involved:* New `Frontend/` directory.
2. **Expand Purpose Taxonomy:** Expand `PURPOSE_CATEGORIES` dictionary in `comparison_service.py` to cover additional domain-specific privacy terms.

### Optional / Enhancement
1. **RDF/OWL Export Utility:** If required for research presentation, create an exporter script converting SQLite database records into RDF Turtle (`.ttl`) format.

---

## 18. Next Best Action

## Recommended Next Step

**Populate `Backend/app/requirements.txt` and add pytest configuration.**

- **Why this should be done next:** `Backend/app/requirements.txt` is currently an empty 0-byte file, and running `python -m pytest` failed due to unconfigured test runner dependencies. Completing this ensures environment reproducibility and standard CI testing.
- **Files to modify/create:**
  - `Backend/app/requirements.txt`
  - `Backend/pyproject.toml`
- **What should be added to `requirements.txt`:**
  ```text
  fastapi>=0.110.0
  uvicorn>=0.30.0
  sqlalchemy>=2.0.0
  pydantic>=2.0.0
  pydantic-settings>=2.0.0
  google-genai>=0.1.0
  pandas>=2.0.0
  openpyxl>=3.1.0
  pytest>=8.0.0
  ```
- **Verification Command:**
  ```powershell
  cd D:\VIT\PROJECT\TARP\Backend
  python -m pytest -v
  ```

---

## 19. Final Summary

## TARP CURRENT STATE SUMMARY

- **Project Purpose:** Automated detection of Functional Data Overreach (FDO) by comparing expected functional data requirements against privacy policy disclosures using LLM evidence extraction and deterministic rule adjudication.
- **Current Architecture:** Decoupled FastAPI backend connected to an SQLite database (`fdo_privacy.db`) using SQLAlchemy 2.0 ORM. Evidence extraction is performed by Google Gemini (`gemini-3.5-flash-lite`), while FDO decisions are governed strictly by a 5-rule Python decision engine.
- **Technology Stack:** Python 3.10, FastAPI, SQLAlchemy 2.0, SQLite 3, Pydantic v2, Google GenAI SDK, Pandas, OpenPyXL.
- **Current Backend Status:** Operational. All 10 REST API endpoints are functional, supporting benchmark queries and live runtime policy analysis.
- **AI/NLP Status:** Operational. Live evidence extraction via `gemini-3.5-flash-lite` with regex fallback.
- **Ontology Status:** Operational via canonical data type string identifiers and controlled purpose categories in code; no OWL/RDF files present.
- **Knowledge Graph & Reasoning Status:** No graph database (Neo4j/Jena) exists. Reasoning is executed deterministically in pure Python code.
- **Database Status:** Operational. 10 SQLAlchemy ORM tables populated with Stage 3 benchmark data (27 apps, 88 functions, 99 mappings, 93 evidence records).
- **Test Status:** 46 unit & integration tests passing (100% pass rate).
- **Completed Functionality:** Purpose normalization & classification, multi-purpose compatibility, 5-rule FDO decision engine, AI evidence extraction, benchmark importer, database persistence, REST API, rich report generation.
- **Incomplete Functionality:** Empty `requirements.txt` file, missing frontend UI, lack of RDF/OWL export scripts.
- **Immediate Next Step:** Populate `Backend/app/requirements.txt` and configure `pyproject.toml` for standard pytest execution.
