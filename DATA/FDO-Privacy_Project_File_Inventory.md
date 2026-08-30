# FDO-Privacy Project — Complete File Inventory

## 1. Project Context

The **FDO-Privacy** research project investigates whether application data collection practices can be systematically evaluated against expected, function-specific data requirements and privacy-policy evidence to identify potentially **Functionally Excessive Data (FDO)**.

Privacy policies often describe data collection using broad or ambiguous categories, making it difficult to discern whether collected data types are strictly necessary for core application features or functionally excessive. The FDO-Privacy framework addresses this challenge by establishing an empirical, auditable pipeline that maps expected data necessity to empirical policy declarations and subjects them to rigorous necessity, purpose compatibility, candidate screening, and detailed adjudication tests.

The project was executed through an iterative 7-stage workflow:
- **Stage 1 (Research Scope & Design)**: Defined the problem statement, core research questions, analytical scope, and initial methodology.
- **Stage 2 (Expected-Data Baseline & Pilot)**: Built the expected-data baseline model mapping applications and core functions to data types, expected necessity, and expected purposes. Executed a 30-application pilot across 4 annotation batches.
- **Stage 3 (Policy Evidence Annotation & QA)**: Prepared canonical schemas, extracted privacy policy evidence, established provenance, conducted integration QA, remediated defect gaps, and frozen the Stage 3 dataset across 27 analytical applications (excluding 3 policy exceptions).
- **Stage 4 (FDO Analysis & Adjudication)**: Performed 5-tier FDO analysis (Stage 4A Necessity Analysis, Stage 4B Purpose Compatibility, Stage 4C Candidate Screening, Stage 4D Detailed Adjudication, Stage 4E Ambiguous Resolution). FDO labels were strictly reserved for this stage.
- **Stage 5 (Final Mapping-Level Dataset & Statistics)**: Generated final mapping-level dataset statistics across 99 expected mappings and 93 evidence-backed mappings.
- **Stage 6 (Results Visualization & Findings)**: Constructed interactive dashboards, comparative charts, master consolidated workbooks, and core research findings.
- **Stage 7 (Final Research Report Package)**: Consolidated methodology, empirical findings, validity threats, roadmap, and presentation deliverables into a formal research report package in DOCX format.

## 2. Project Status Snapshot

Below are the verified, empirical project counts supported directly by the project files:

- **Original Pilot Applications**: 30 applications (evaluated during Stage 2B pilot annotations)
- **Analytical Applications**: 27 applications (Stage 3 through Stage 7 analytical cohort)
- **Expected Mappings**: 99 mappings (defined in Stage 2 expected-data model)
- **Evidence-Backed Mappings**: 93 mappings (entered Stage 4/5 analysis after Stage 3 freeze; 6 mappings lacked complete policy evidence)
- **NOT_FDO Mappings**: 60 mappings (64.5% of evidence-backed mappings; zero functional excess established)
- **AMBIGUOUS Mappings**: 33 mappings (35.5% of evidence-backed mappings; evidence insufficient or unresolved)
- **FDO Mappings Established**: 0 mappings (0.0% resolved-case FDO rate)
- **Policy Exceptions**: 3 applications (**Instagram**, **PUBG MOBILE**, and **WeChat** — documented as policy exceptions due to unparseable, regional, or unresolvable policy structures)
- **Current Project Stage / Status**: **Stage 7 Complete** (Final Research Report Package finalized in DOCX)

## 3. File Inventory

| # | File Name | File Type | Version | Project Stage | Main Purpose | Contains Detailed Data? | Primary Use |
|---|---|---|---|---|---|---|---|
| 1 | `FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx` | XLSX | v1.0 Cleaned | Stage 3 (Final) | Consolidated cleaned Stage 3 dataset without extra staging metadata | Yes | Final Stage 3 Artifact |
| 2 | `FDO-Privacy_Final_Stage3_Dataset_COMPLETE.xlsx` | XLSX | v1.0 Complete | Stage 3 (Final) | Complete Stage 3 master dataset including all columns and full metadata | Yes | Final Stage 3 Artifact |
| 3 | `FDO-Privacy_Stage2B_Agreement_Analysis_v1.0 (1).xlsx` | XLSX | v1.0 | Stage 2B | Inter-annotator agreement analysis (duplicate file) | Yes | Audit / QA Artifact |
| 4 | `FDO-Privacy_Stage2B_Agreement_Analysis_v1.0.xlsx` | XLSX | v1.0 | Stage 2B | Inter-annotator agreement analysis, metric calculation, and ontology revision tracking | Yes | Audit / QA Artifact |
| 5 | `FDO-Privacy_Stage2B_AnnotatorA_Batch1.xlsx` | XLSX | v0.2 | Stage 2B | Annotator A independent pilot annotations for Batch 1 | Yes | Annotation Artifact |
| 6 | `FDO-Privacy_Stage2B_AnnotatorA_Batch2.xlsx` | XLSX | v0.3 | Stage 2B | Annotator A independent pilot annotations for Batch 2 | Yes | Annotation Artifact |
| 7 | `FDO-Privacy_Stage2B_AnnotatorA_Batch3.xlsx` | XLSX | v0.4 | Stage 2B | Annotator A independent pilot annotations for Batch 3 | Yes | Annotation Artifact |
| 8 | `FDO-Privacy_Stage2B_AnnotatorA_Batch4.xlsx` | XLSX | v0.5 | Stage 2B | Annotator A independent pilot annotations for Batch 4 | Yes | Annotation Artifact |
| 9 | `FDO-Privacy_Stage2B_AnnotatorB_All4Batches.xlsx` | XLSX | v0.5 Complete | Stage 2B | Consolidated Annotator B pilot annotations across all 4 batches | Yes | Annotation Artifact |
| 10 | `FDO-Privacy_Stage2B_AnnotatorB_Batch01.xlsx` | XLSX | v0.2 | Stage 2B | Annotator B independent pilot annotations for Batch 1 | Yes | Annotation Artifact |
| 11 | `FDO-Privacy_Stage2B_AnnotatorB_Batch02.xlsx` | XLSX | v0.3 | Stage 2B | Annotator B independent pilot annotations for Batch 2 | Yes | Annotation Artifact |
| 12 | `FDO-Privacy_Stage2B_AnnotatorB_Batch03.xlsx` | XLSX | v0.4 | Stage 2B | Annotator B independent pilot annotations for Batch 3 | Yes | Annotation Artifact |
| 13 | `FDO-Privacy_Stage2B_AnnotatorB_Batch04.xlsx` | XLSX | v0.5 | Stage 2B | Annotator B independent pilot annotations for Batch 4 | Yes | Annotation Artifact |
| 14 | `FDO-Privacy_Stage2B_Pilot_v0.2_VerifiedBatch01.xlsx` | XLSX | v0.2 | Stage 2B | Adjudicated and verified consensus annotations for Pilot Batch 1 | Yes | Annotation / QA Artifact |
| 15 | `FDO-Privacy_Stage2B_Pilot_v0.3_Batch02.xlsx` | XLSX | v0.3 | Stage 2B | Adjudicated consensus annotations for Pilot Batch 2 | Yes | Annotation / QA Artifact |
| 16 | `FDO-Privacy_Stage2B_Pilot_v0.4_Batch03.xlsx` | XLSX | v0.4 | Stage 2B | Adjudicated consensus annotations for Pilot Batch 3 | Yes | Annotation / QA Artifact |
| 17 | `FDO-Privacy_Stage2B_Pilot_v0.5_Batch04.xlsx` | XLSX | v0.5 | Stage 2B | Adjudicated consensus annotations for Pilot Batch 4 | Yes | Annotation / QA Artifact |
| 18 | `FDO-Privacy_Stage3A_Dataset_Schema_v1.0.xlsx` | XLSX | v1.0 | Stage 3A | Defines canonical schema, data dictionary, application metadata, and expected mappings | Yes | Input / Design Artifact |
| 19 | `FDO-Privacy_Stage3B_Policy_Extraction_Batch01.xlsx` | XLSX | v1.0 Batch 1 | Stage 3B | Initial policy text extraction for Batch 1 applications | Yes | Extraction Artifact |
| 20 | `FDO-Privacy_Stage3B_Policy_Extraction_Batch01_Complete.xlsx` | XLSX | v1.1 Batch 1 | Stage 3B | Completed policy text extraction for Batch 1 applications | Yes | Extraction Artifact |
| 21 | `FDO-Privacy_Stage3B_Policy_Extraction_Batch03.xlsx` | XLSX | v1.0 Batch 3 | Stage 3B | Policy text extractions and annotations for Batch 3 applications | Yes | Extraction Artifact |
| 22 | `FDO-Privacy_Stage3B_Policy_Registry_Batch01.xlsx` | XLSX | v1.0 Batch 1 | Stage 3B | Initial policy registry metadata for Batch 1 (URLs, effective dates) | Yes | Registry Artifact |
| 23 | `FDO-Privacy_Stage3B_Policy_Registry_Batch01_v2.xlsx` | XLSX | v1.1 Batch 1 | Stage 3B | Updated policy registry metadata for Batch 1 | Yes | Registry Artifact |
| 24 | `FDO-Privacy_Stage3B_Policy_Registry_Extraction_Batch02.xlsx` | XLSX | v1.0 Batch 2 | Stage 3B | Combined policy registry metadata and extractions for Batch 2 | Yes | Registry / Extraction Artifact |
| 25 | `FDO-Privacy_Stage3C_Dataset_Freeze_v1.0.xlsx` | XLSX | v1.0 | Stage 3C | Initial dataset freeze combining extractions across all batches | Yes | Integration Artifact |
| 26 | `FDO-Privacy_Stage3C_Integration_QA_v1.0.xlsx` | XLSX | v1.0 | Stage 3C | Initial QA review identifying missing evidence, formatting issues, and discrepancies | Yes | Audit / QA Artifact |
| 27 | `FDO-Privacy_Stage3C_QA_Remediation_v1.1.xlsx` | XLSX | v1.1 | Stage 3C | First round of QA remediation fixing identified extraction defects | Yes | Audit / QA Artifact |
| 28 | `FDO-Privacy_Stage3C_QA_Remediation_v1.2.xlsx` | XLSX | v1.2 | Stage 3C | Finalized QA remediation establishing clean dataset freeze | Yes | Audit / QA Artifact |
| 29 | `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.0.xlsx` | XLSX | v1.0 | Stage 3D | Initial unpopulated Policy Annotation Matrix structure | Yes | Annotation Matrix |
| 30 | `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.1_FILLED.xlsx` | XLSX | v1.1 | Stage 3D | Populated annotation matrix with initial policy declarations | Yes | Annotation Matrix |
| 31 | `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.2_ANNOTATED_BATCH.xlsx` | XLSX | v1.2 | Stage 3D | Incremental annotation matrix after Batch 1 processing | Yes | Annotation Matrix |
| 32 | `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.3_ANNOTATED_BATCH.xlsx` | XLSX | v1.3 | Stage 3D | Incremental annotation matrix after Batch 2 processing | Yes | Annotation Matrix |
| 33 | `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.4_ANNOTATED_BATCH.xlsx` | XLSX | v1.4 | Stage 3D | Incremental annotation matrix after Batch 3 processing | Yes | Annotation Matrix |
| 34 | `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.5_ANNOTATED_BATCH.xlsx` | XLSX | v1.5 | Stage 3D | Incremental annotation matrix completing full 30-app annotation pass | Yes | Annotation Matrix |
| 35 | `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.6_FINAL_ANNOTATION.xlsx` | XLSX | v1.6 | Stage 3D | Finalized primary annotations prior to completion/evidence review | Yes | Annotation Matrix |
| 36 | `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.7_COMPLETION_REVIEW.xlsx` | XLSX | v1.7 | Stage 3D | Audit review tracking missing fields and evidence gaps | Yes | Audit / Review Matrix |
| 37 | `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.8_EVIDENCE_REVIEW.xlsx` | XLSX | v1.8 | Stage 3D | Review matrix validating policy evidence quotes and provenance | Yes | Audit / Review Matrix |
| 38 | `FDO-Privacy_Stage3D_Policy_Evidence_Completion_v1.0.xlsx` | XLSX | v1.0 Evidence | Stage 3D | Dedicated workflow file for filling evidence gaps identified in v1.7 | Yes | Remediation Artifact |
| 39 | `FDO-Privacy_Stage3D_Policy_Evidence_Completion_v1.1.xlsx` | XLSX | v1.1 Evidence | Stage 3D | Finalized evidence completion workbook establishing complete quotes | Yes | Remediation Artifact |
| 40 | `FDO-Privacy_Stage3D_v1.9_STAGE3_FREEZE_AND_STAGE4_READY.xlsx` | XLSX | v1.9 Freeze | Stage 3D | Final frozen Stage 3 dataset ready for Stage 4 FDO analysis | Yes | Stage 3 Master Freeze |
| 41 | `FDO-Privacy_Stage4A_Expected_vs_Declared_Matching_v1.0.xlsx` | XLSX | v1.0 | Stage 4A | Initial matching of expected necessity against declared data | Yes | Analysis Artifact |
| 42 | `FDO-Privacy_Stage4A_FDO_Necessity_Analysis_v1.1.xlsx` | XLSX | v1.1 | Stage 4A | Final necessity analysis evaluating data necessity alignment | Yes | Analysis Artifact |
| 43 | `FDO-Privacy_Stage4B_Purpose_Compatibility_Review_v1.0.xlsx` | XLSX | v1.0 Review | Stage 4B | Preliminary review queue for purpose compatibility testing | Yes | Analysis Artifact |
| 44 | `FDO-Privacy_Stage4B_Purpose_Compatibility_v1.0.xlsx` | XLSX | v1.0 Final | Stage 4B | Comprehensive purpose compatibility assessment against policy evidence | Yes | Analysis Artifact |
| 45 | `FDO-Privacy_Stage4C_FDO_Candidate_Identification_v1.0.xlsx` | XLSX | v1.0 Ident | Stage 4C | Initial candidate identification list for potential FDO cases | Yes | Analysis Artifact |
| 46 | `FDO-Privacy_Stage4C_FDO_Candidate_Screening_v1.0.xlsx` | XLSX | v1.0 Final | Stage 4C | Formal screening filtering non-candidates from true adjudication queue | Yes | Analysis Artifact |
| 47 | `FDO-Privacy_Stage4D_Detailed_Adjudication_v1.0.xlsx` | XLSX | v1.0 Final | Stage 4D | Master adjudication workbook applying multi-test FDO rules | Yes | Analysis Artifact |
| 48 | `FDO-Privacy_Stage4D_FDO_Adjudication_v1.0.xlsx` | XLSX | v1.0 Subset | Stage 4D | Focused adjudication subset workbook for candidate cases | Yes | Analysis Artifact |
| 49 | `FDO-Privacy_Stage4E_Ambiguous_Case_Resolution_v1.0.xlsx` | XLSX | v1.0 Final | Stage 4E | Final Stage 4 resolution of ambiguous cases and freeze of final FDO labels | Yes | Analysis Artifact |
| 50 | `FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx` | XLSX | v1.0 Final | Stage 6 | Consolidated results workbook with dashboards, statistics, charts, and master sheets | Yes | Visualization / Summary Artifact |
| 51 | `FDO-Privacy_Stage7_Final_Research_Report_Package_v1.0.docx` | DOCX | v1.0 Final | Stage 7 | Comprehensive final research report package consolidating all project findings | Yes (Text/Report) | Final Research Report |


## 4. Detailed File-by-File Explanation

### `FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx`

**What this file contains**
Consolidated cleaned Stage 3 dataset without extra staging metadata

**Worksheets / Sections**
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.

**Important data/counts**
- Primary worksheet (`Stage 3 Dataset`) contains **134 rows** across 12 total worksheet(s).

**Use case**
Serves as the cleaned baseline of policy declarations and evidence after removing preliminary annotation metadata.

**Where it fits in the workflow**
Feeds into Stage 4 analysis after Stage 3D freeze.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Final Artifact (Stage 3)**

**Relationship to other files**
- Stage: Stage 3 (Final). Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Final_Stage3_Dataset_COMPLETE.xlsx`

**What this file contains**
Complete Stage 3 master dataset including all columns and full metadata

**Worksheets / Sections**
- **Sheet `MASTER — ALL DATA`**: Contains 134 non-empty rows (134 max rows, 22 max cols). Primary columns include: `Record Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 11 non-empty rows (11 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 9 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.

**Important data/counts**
- Primary worksheet (`MASTER — ALL DATA`) contains **134 rows** across 12 total worksheet(s).

**Use case**
Provides the exhaustive master record for Stage 3 including all 22 attributes and complete provenance.

**Where it fits in the workflow**
Created alongside CLEANED dataset at the conclusion of Stage 3.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Final Artifact (Stage 3)**

**Relationship to other files**
- Stage: Stage 3 (Final). Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_Agreement_Analysis_v1.0 (1).xlsx`

**What this file contains**
Inter-annotator agreement analysis (duplicate file)

**Worksheets / Sections**
- **Sheet `Agreement Analysis`**: Contains 100 non-empty rows (100 max rows, 14 max cols). Primary columns include: `Application`, `Function`, `Data Type ID`, `A Necessity`, `B Necessity`, `Exact?`.
- **Sheet `Metrics`**: Contains 20 non-empty rows (20 max rows, 2 max cols). Primary columns include: `Total mappings`, `99`.
- **Sheet `Disagreements`**: Contains 2 non-empty rows (2 max rows, 7 max cols). Primary columns include: `Application`, `Function`, `Data Type`, `A`, `B`, `Issue`.
- **Sheet `Ontology Revision`**: Contains 4 non-empty rows (4 max rows, 3 max cols). Primary columns include: `Revision candidate`, `Clarify L2 vs L4`, `A data type can support a core function while ALSO serving a secondary purpose. Necessity level should describe the function-data relationship; purpose should be recorded separately.`.
- **Sheet `Research Caveat`**: Contains 3 non-empty rows (3 max rows, 2 max cols). Primary columns include: `Important`, `The uploaded Annotator B workbooks retain the original A/draft columns and show one necessity disagreement across 99 mappings. This analysis therefore reports observed agreement, not proof that two independent human annotators participated.`.

**Important data/counts**
- Primary worksheet (`Agreement Analysis`) contains **100 rows** across 5 total worksheet(s).

**Use case**
Filesystem duplicate of FDO-Privacy_Stage2B_Agreement_Analysis_v1.0.xlsx.

**Where it fits in the workflow**
Identical content to original v1.0.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate / Duplicate Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_Agreement_Analysis_v1.0.xlsx`

**What this file contains**
Inter-annotator agreement analysis, metric calculation, and ontology revision tracking

**Worksheets / Sections**
- **Sheet `Agreement Analysis`**: Contains 100 non-empty rows (100 max rows, 14 max cols). Primary columns include: `Application`, `Function`, `Data Type ID`, `A Necessity`, `B Necessity`, `Exact?`.
- **Sheet `Metrics`**: Contains 20 non-empty rows (20 max rows, 2 max cols). Primary columns include: `Total mappings`, `99`.
- **Sheet `Disagreements`**: Contains 2 non-empty rows (2 max rows, 7 max cols). Primary columns include: `Application`, `Function`, `Data Type`, `A`, `B`, `Issue`.
- **Sheet `Ontology Revision`**: Contains 4 non-empty rows (4 max rows, 3 max cols). Primary columns include: `Revision candidate`, `Clarify L2 vs L4`, `A data type can support a core function while ALSO serving a secondary purpose. Necessity level should describe the function-data relationship; purpose should be recorded separately.`.
- **Sheet `Research Caveat`**: Contains 3 non-empty rows (3 max rows, 2 max cols). Primary columns include: `Important`, `The uploaded Annotator B workbooks retain the original A/draft columns and show one necessity disagreement across 99 mappings. This analysis therefore reports observed agreement, not proof that two independent human annotators participated.`.

**Important data/counts**
- Primary worksheet (`Agreement Analysis`) contains **100 rows** across 5 total worksheet(s).

**Use case**
Evaluates agreement metrics between Annotator A and Annotator B across pilot batches.

**Where it fits in the workflow**
Created after pilot annotation batches to refine annotation rules for Stage 3.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Audit / QA Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_AnnotatorA_Batch1.xlsx`

**What this file contains**
Annotator A independent pilot annotations for Batch 1

**Worksheets / Sections**
- **Sheet `Annotator A Batch 1`**: Contains 26 non-empty rows (26 max rows, 11 max cols). Primary columns include: `Application`, `Function`, `Data Type ID`, `Necessity (A)`, `Purpose (A)`, `Rationale (A)`.
- **Sheet `A Instructions`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Annotator`, `A — model/researcher annotation prepared for pilot analysis.`.

**Important data/counts**
- Primary worksheet (`Annotator A Batch 1`) contains **26 rows** across 2 total worksheet(s).

**Use case**
Captures raw pilot policy annotations by Annotator A for Batch 1.

**Where it fits in the workflow**
Feeds into Stage 2B Agreement Analysis.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Annotation Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_AnnotatorA_Batch2.xlsx`

**What this file contains**
Annotator A independent pilot annotations for Batch 2

**Worksheets / Sections**
- **Sheet `Annotator A Batch 2`**: Contains 27 non-empty rows (27 max rows, 11 max cols). Primary columns include: `Application`, `Function`, `Data Type ID`, `Necessity (A)`, `Purpose (A)`, `Rationale (A)`.
- **Sheet `A Instructions`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Annotator`, `A — model/researcher annotation prepared for pilot analysis.`.

**Important data/counts**
- Primary worksheet (`Annotator A Batch 2`) contains **27 rows** across 2 total worksheet(s).

**Use case**
Captures raw pilot policy annotations by Annotator A for Batch 2.

**Where it fits in the workflow**
Feeds into Stage 2B Agreement Analysis.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Annotation Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_AnnotatorA_Batch3.xlsx`

**What this file contains**
Annotator A independent pilot annotations for Batch 3

**Worksheets / Sections**
- **Sheet `Annotator A Batch 3`**: Contains 25 non-empty rows (25 max rows, 11 max cols). Primary columns include: `Application`, `Function`, `Data Type ID`, `Necessity (A)`, `Purpose (A)`, `Rationale (A)`.
- **Sheet `A Instructions`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Annotator`, `A — model/researcher annotation prepared for pilot analysis.`.

**Important data/counts**
- Primary worksheet (`Annotator A Batch 3`) contains **25 rows** across 2 total worksheet(s).

**Use case**
Captures raw pilot policy annotations by Annotator A for Batch 3.

**Where it fits in the workflow**
Feeds into Stage 2B Agreement Analysis.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Annotation Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_AnnotatorA_Batch4.xlsx`

**What this file contains**
Annotator A independent pilot annotations for Batch 4

**Worksheets / Sections**
- **Sheet `Annotator A Batch 4`**: Contains 25 non-empty rows (25 max rows, 11 max cols). Primary columns include: `Application`, `Function`, `Data Type ID`, `Necessity (A)`, `Purpose (A)`, `Rationale (A)`.
- **Sheet `A Instructions`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Annotator`, `A — model/researcher annotation prepared for pilot analysis.`.

**Important data/counts**
- Primary worksheet (`Annotator A Batch 4`) contains **25 rows** across 2 total worksheet(s).

**Use case**
Captures raw pilot policy annotations by Annotator A for Batch 4.

**Where it fits in the workflow**
Feeds into Stage 2B Agreement Analysis.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Annotation Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_AnnotatorB_All4Batches.xlsx`

**What this file contains**
Consolidated Annotator B pilot annotations across all 4 batches

**Worksheets / Sections**
- **Sheet `Sheet1`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Application`, `Function`, `Data Type ID`, `Necessity (A)`, `Purpose (A)`, `Rationale (A)`.

**Important data/counts**
- Primary worksheet (`Sheet1`) contains **100 rows** across 1 total worksheet(s).

**Use case**
Aggregates Annotator B's annotations across Batches 1 through 4 into a single workbook.

**Where it fits in the workflow**
Consolidates individual Annotator B batch files.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Annotation Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_AnnotatorB_Batch01.xlsx`

**What this file contains**
Annotator B independent pilot annotations for Batch 1

**Worksheets / Sections**
- **Sheet `Sheet1`**: Contains 26 non-empty rows (26 max rows, 15 max cols). Primary columns include: `Application`, `Function`, `Data Type ID`, `Necessity (A)`, `Purpose (A)`, `Rationale (A)`.

**Important data/counts**
- Primary worksheet (`Sheet1`) contains **26 rows** across 1 total worksheet(s).

**Use case**
Captures raw pilot policy annotations by Annotator B for Batch 1.

**Where it fits in the workflow**
Feeds into AnnotatorB_All4Batches and Agreement Analysis.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Annotation Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_AnnotatorB_Batch02.xlsx`

**What this file contains**
Annotator B independent pilot annotations for Batch 2

**Worksheets / Sections**
- **Sheet `Sheet1`**: Contains 27 non-empty rows (27 max rows, 15 max cols). Primary columns include: `Application`, `Function`, `Data Type ID`, `Necessity (A)`, `Purpose (A)`, `Rationale (A)`.

**Important data/counts**
- Primary worksheet (`Sheet1`) contains **27 rows** across 1 total worksheet(s).

**Use case**
Captures raw pilot policy annotations by Annotator B for Batch 2.

**Where it fits in the workflow**
Feeds into AnnotatorB_All4Batches and Agreement Analysis.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Annotation Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_AnnotatorB_Batch03.xlsx`

**What this file contains**
Annotator B independent pilot annotations for Batch 3

**Worksheets / Sections**
- **Sheet `Sheet1`**: Contains 25 non-empty rows (25 max rows, 15 max cols). Primary columns include: `Application`, `Function`, `Data Type ID`, `Necessity (A)`, `Purpose (A)`, `Rationale (A)`.

**Important data/counts**
- Primary worksheet (`Sheet1`) contains **25 rows** across 1 total worksheet(s).

**Use case**
Captures raw pilot policy annotations by Annotator B for Batch 3.

**Where it fits in the workflow**
Feeds into AnnotatorB_All4Batches and Agreement Analysis.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Annotation Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_AnnotatorB_Batch04.xlsx`

**What this file contains**
Annotator B independent pilot annotations for Batch 4

**Worksheets / Sections**
- **Sheet `Sheet1`**: Contains 25 non-empty rows (25 max rows, 15 max cols). Primary columns include: `Application`, `Function`, `Data Type ID`, `Necessity (A)`, `Purpose (A)`, `Rationale (A)`.

**Important data/counts**
- Primary worksheet (`Sheet1`) contains **25 rows** across 1 total worksheet(s).

**Use case**
Captures raw pilot policy annotations by Annotator B for Batch 4.

**Where it fits in the workflow**
Feeds into AnnotatorB_All4Batches and Agreement Analysis.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Annotation Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_Pilot_v0.2_VerifiedBatch01.xlsx`

**What this file contains**
Adjudicated and verified consensus annotations for Pilot Batch 1

**Worksheets / Sections**
- **Sheet `Verified Batch 01`**: Contains 26 non-empty rows (26 max rows, 12 max cols). Primary columns include: `App ID`, `Application`, `Function ID`, `Function`, `Data Type ID`, `Necessity`.
- **Sheet `Research Notes`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Status`, `This is a researcher-draft annotation batch, not validated ground truth.`.

**Important data/counts**
- Primary worksheet (`Verified Batch 01`) contains **26 rows** across 2 total worksheet(s).

**Use case**
Establishes verified consensus annotations for Batch 1 after reconciling Annotator A and B.

**Where it fits in the workflow**
Follows individual Batch 1 annotations, feeds into pilot baseline.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate / QA Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_Pilot_v0.3_Batch02.xlsx`

**What this file contains**
Adjudicated consensus annotations for Pilot Batch 2

**Worksheets / Sections**
- **Sheet `Batch 02 Draft`**: Contains 27 non-empty rows (27 max rows, 12 max cols). Primary columns include: `App ID`, `Application`, `Function ID`, `Function`, `Data Type ID`, `Necessity`.
- **Sheet `Batch Notes`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Item`, `Note`.

**Important data/counts**
- Primary worksheet (`Batch 02 Draft`) contains **27 rows** across 2 total worksheet(s).

**Use case**
Establishes verified consensus annotations for Batch 2.

**Where it fits in the workflow**
Follows individual Batch 2 annotations.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate / QA Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_Pilot_v0.4_Batch03.xlsx`

**What this file contains**
Adjudicated consensus annotations for Pilot Batch 3

**Worksheets / Sections**
- **Sheet `Batch 03 Draft`**: Contains 25 non-empty rows (25 max rows, 12 max cols). Primary columns include: `App ID`, `Application`, `Function ID`, `Function`, `Data Type ID`, `Necessity`.
- **Sheet `Research Notes`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Topic`, `Note`.

**Important data/counts**
- Primary worksheet (`Batch 03 Draft`) contains **25 rows** across 2 total worksheet(s).

**Use case**
Establishes verified consensus annotations for Batch 3.

**Where it fits in the workflow**
Follows individual Batch 3 annotations.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate / QA Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage2B_Pilot_v0.5_Batch04.xlsx`

**What this file contains**
Adjudicated consensus annotations for Pilot Batch 4

**Worksheets / Sections**
- **Sheet `Batch 04 Draft`**: Contains 25 non-empty rows (25 max rows, 12 max cols). Primary columns include: `App ID`, `Application`, `Function ID`, `Function`, `Data Type ID`, `Necessity`.
- **Sheet `Batch Notes`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Topic`, `Note`.

**Important data/counts**
- Primary worksheet (`Batch 04 Draft`) contains **25 rows** across 2 total worksheet(s).

**Use case**
Establishes verified consensus annotations for Batch 4 completing the 30-app pilot.

**Where it fits in the workflow**
Completes Stage 2B pilot phase.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate / QA Artifact**

**Relationship to other files**
- Stage: Stage 2B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3A_Dataset_Schema_v1.0.xlsx`

**What this file contains**
Defines canonical schema, data dictionary, application metadata, and expected mappings

**Worksheets / Sections**
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 12 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Official App/Feature URL`, `Privacy Policy URL`, `Policy Version/Date`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Documents`**: Contains 31 non-empty rows (31 max rows, 12 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL`, `Policy Title`, `Effective/Updated Date`.
- **Sheet `Declared Data`**: Contains 31 non-empty rows (31 max rows, 16 max cols). Primary columns include: `Declared ID`, `Policy ID`, `App ID`, `Data Type ID`, `Normalized Data Type`, `Raw Policy Term`.
- **Sheet `Purposes`**: Contains 1 non-empty rows (1 max rows, 10 max cols). Primary columns include: `Purpose ID`, `Policy ID`, `App ID`, `Purpose Category`, `Raw Purpose Phrase`, `Normalized Purpose`.
- **Sheet `Sharing`**: Contains 1 non-empty rows (1 max rows, 12 max cols). Primary columns include: `Sharing ID`, `Policy ID`, `App ID`, `Data Type ID`, `Recipient Category`, `Recipient Name/Raw Term`.
- **Sheet `Retention`**: Contains 1 non-empty rows (1 max rows, 11 max cols). Primary columns include: `Retention ID`, `Policy ID`, `App ID`, `Data Type ID`, `Retention Period Raw`, `Normalized Retention`.
- **Sheet `Evidence`**: Contains 1 non-empty rows (1 max rows, 12 max cols). Primary columns include: `Evidence ID`, `Policy ID`, `App ID`, `Evidence Type`, `Source URL`, `Section/Heading`.
- **Sheet `Ground Truth - Later`**: Contains 2 non-empty rows (2 max rows, 12 max cols). Primary columns include: `GT ID`, `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`.
- **Sheet `Data Dictionary`**: Contains 11 non-empty rows (11 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `QA Checklist`**: Contains 10 non-empty rows (10 max rows, 2 max cols). Primary columns include: `QA Item`, `Requirement`.

**Important data/counts**
- Primary worksheet (`Applications`) contains **31 rows** across 11 total worksheet(s).

**Use case**
Establishes the foundational Stage 3 data structure, expected 99 mappings, and application registry.

**Where it fits in the workflow**
Forms the input for Stage 3B policy extraction and registry construction.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Input / Design Artifact**

**Relationship to other files**
- Stage: Stage 3A. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3B_Policy_Extraction_Batch01.xlsx`

**What this file contains**
Initial policy text extraction for Batch 1 applications

**Worksheets / Sections**
- **Sheet `Declared Data Batch 01`**: Contains 27 non-empty rows (27 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Extraction Coverage`**: Contains 11 non-empty rows (11 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Policy extraction status`, `Records extracted`, `Evidence quality`, `Next action`.

**Important data/counts**
- Primary worksheet (`Declared Data Batch 01`) contains **27 rows** across 2 total worksheet(s).

**Use case**
Stores raw extracted policy text snippets for Batch 1.

**Where it fits in the workflow**
Superseded by Batch01_Complete.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Extraction Artifact**

**Relationship to other files**
- Stage: Stage 3B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3B_Policy_Extraction_Batch01_Complete.xlsx`

**What this file contains**
Completed policy text extraction for Batch 1 applications

**Worksheets / Sections**
- **Sheet `Policy Extraction Batch 01B`**: Contains 13 non-empty rows (13 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Research Notes`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Topic`, `Note`.

**Important data/counts**
- Primary worksheet (`Policy Extraction Batch 01B`) contains **13 rows** across 2 total worksheet(s).

**Use case**
Contains finalized raw policy text extractions and coverage checks for Batch 1.

**Where it fits in the workflow**
Replaces initial Batch 01 extraction file.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Extraction Artifact**

**Relationship to other files**
- Stage: Stage 3B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3B_Policy_Extraction_Batch03.xlsx`

**What this file contains**
Policy text extractions and annotations for Batch 3 applications

**Worksheets / Sections**
- **Sheet `Batch 03 Policy Registry`**: Contains 9 non-empty rows (9 max rows, 7 max cols). Primary columns include: `App ID`, `Application`, `Official Source`, `Effective/Updated`, `Scope`, `Status`.
- **Sheet `Policy Extraction`**: Contains 21 non-empty rows (21 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy/Data Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Research Notes`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Topic`, `Note`.

**Important data/counts**
- Primary worksheet (`Batch 03 Policy Registry`) contains **9 rows** across 3 total worksheet(s).

**Use case**
Stores raw policy extractions and preliminary annotations for Batch 3.

**Where it fits in the workflow**
Feeds into Stage 3C integration.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Extraction Artifact**

**Relationship to other files**
- Stage: Stage 3B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3B_Policy_Registry_Batch01.xlsx`

**What this file contains**
Initial policy registry metadata for Batch 1 (URLs, effective dates)

**Worksheets / Sections**
- **Sheet `Policy Registry Batch 01`**: Contains 11 non-empty rows (11 max rows, 11 max cols). Primary columns include: `App ID`, `Application`, `Policy URL`, `Policy Title`, `Effective/Updated Date`, `Region/Scope`.
- **Sheet `Extraction Plan`**: Contains 11 non-empty rows (11 max rows, 3 max cols). Primary columns include: `Step`, `Task`, `Rule`.
- **Sheet `Scope Caveats`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Issue`, `Rule`.

**Important data/counts**
- Primary worksheet (`Policy Registry Batch 01`) contains **11 rows** across 3 total worksheet(s).

**Use case**
Tracks policy source links, dates, and access timestamps for Batch 1.

**Where it fits in the workflow**
Superseded by Batch01_v2.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Registry Artifact**

**Relationship to other files**
- Stage: Stage 3B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3B_Policy_Registry_Batch01_v2.xlsx`

**What this file contains**
Updated policy registry metadata for Batch 1

**Worksheets / Sections**
- **Sheet `Policy Registry Batch 01`**: Contains 11 non-empty rows (11 max rows, 12 max cols). Primary columns include: `App ID`, `Application`, `Policy URL`, `Policy Title`, `Effective/Updated Date`, `Region/Scope`.
- **Sheet `Extraction Plan`**: Contains 11 non-empty rows (11 max rows, 3 max cols). Primary columns include: `Step`, `Task`, `Rule`.
- **Sheet `Scope Caveats`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Issue`, `Rule`.
- **Sheet `Verified Sources`**: Contains 11 non-empty rows (11 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Official Source`, `What It Supports`, `Verification Note`.

**Important data/counts**
- Primary worksheet (`Policy Registry Batch 01`) contains **11 rows** across 4 total worksheet(s).

**Use case**
Refines policy metadata, URL provenance, and validation status for Batch 1.

**Where it fits in the workflow**
Replaces original Batch 01 registry file.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Registry Artifact**

**Relationship to other files**
- Stage: Stage 3B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3B_Policy_Registry_Extraction_Batch02.xlsx`

**What this file contains**
Combined policy registry metadata and extractions for Batch 2

**Worksheets / Sections**
- **Sheet `Batch 02 Policy Registry`**: Contains 11 non-empty rows (11 max rows, 8 max cols). Primary columns include: `App ID`, `Application`, `Policy/Privacy Source`, `Effective/Updated`, `Region/Scope`, `Source Evidence`.
- **Sheet `Batch 02 Extracted Data`**: Contains 15 non-empty rows (15 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy/Data Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Research Notes`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Issue`, `Decision`.

**Important data/counts**
- Primary worksheet (`Batch 02 Policy Registry`) contains **11 rows** across 3 total worksheet(s).

**Use case**
Consolidates policy URLs and text extractions for Batch 2 applications.

**Where it fits in the workflow**
Feeds into Stage 3C integration.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Extraction Artifact**

**Relationship to other files**
- Stage: Stage 3B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3C_Dataset_Freeze_v1.0.xlsx`

**What this file contains**
Initial dataset freeze combining extractions across all batches

**Worksheets / Sections**
- **Sheet `Stage 3C Freeze Report`**: Contains 10 non-empty rows (10 max rows, 2 max cols). Primary columns include: `FDO-Privacy Stage 3C Dataset Freeze Report`, `v1.0`.
- **Sheet `Analysis Set`**: Contains 31 non-empty rows (31 max rows, 4 max cols). Primary columns include: `App ID`, `Application`, `Included in Stage 4?`, `Reason`.
- **Sheet `Freeze Checklist`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Evidence/Rule`.
- **Sheet `Stage 4 Input Rules`**: Contains 8 non-empty rows (8 max rows, 2 max cols). Primary columns include: `Rule`, `Instruction`.

**Important data/counts**
- Primary worksheet (`Stage 3C Freeze Report`) contains **10 rows** across 4 total worksheet(s).

**Use case**
Freezes integrated extractions before formal QA.

**Where it fits in the workflow**
Feeds into Stage 3C Integration QA.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Freeze Artifact**

**Relationship to other files**
- Stage: Stage 3C. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3C_Integration_QA_v1.0.xlsx`

**What this file contains**
Initial QA review identifying missing evidence, formatting issues, and discrepancies

**Worksheets / Sections**
- **Sheet `Integrated App QA`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `App ID`, `Application`, `Policy Source Status`, `Extraction Status`, `Evidence Status`, `Regional Variant Status`.
- **Sheet `QA Issue Register`**: Contains 12 non-empty rows (12 max rows, 8 max cols). Primary columns include: `Issue ID`, `App ID`, `Issue Type`, `Severity`, `Description`, `Required Action`.
- **Sheet `Integration Schema`**: Contains 7 non-empty rows (7 max rows, 5 max cols). Primary columns include: `Layer`, `Source`, `Join Key`, `Output`, `Rule`.
- **Sheet `Stage 3C Gate`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Gate`, `Requirement`, `Current Result`, `Decision`.

**Important data/counts**
- Primary worksheet (`Integrated App QA`) contains **31 rows** across 4 total worksheet(s).

**Use case**
Audits integrated dataset and flags items needing remediation.

**Where it fits in the workflow**
Triggers QA remediation v1.1.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Audit / QA Artifact**

**Relationship to other files**
- Stage: Stage 3C. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3C_QA_Remediation_v1.1.xlsx`

**What this file contains**
First round of QA remediation fixing identified extraction defects

**Worksheets / Sections**
- **Sheet `QA Remediation`**: Contains 12 non-empty rows (12 max rows, 9 max cols). Primary columns include: `Issue ID`, `App ID`, `Application`, `Previous Status`, `Remediation Result`, `Official Source / Evidence`.
- **Sheet `Updated Freeze Gate`**: Contains 12 non-empty rows (12 max rows, 4 max cols). Primary columns include: `Gate`, `Requirement`, `Result`, `Decision`.
- **Sheet `Verified Web Evidence`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `App`, `Evidence`, `Why It Matters`, `Source Ref`.

**Important data/counts**
- Primary worksheet (`QA Remediation`) contains **12 rows** across 3 total worksheet(s).

**Use case**
Applies fixes to policy extractions and provenance metadata.

**Where it fits in the workflow**
Superseded by v1.2.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate QA Artifact**

**Relationship to other files**
- Stage: Stage 3C. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3C_QA_Remediation_v1.2.xlsx`

**What this file contains**
Finalized QA remediation establishing clean dataset freeze

**Worksheets / Sections**
- **Sheet `Final Remediation Pass`**: Contains 5 non-empty rows (5 max rows, 7 max cols). Primary columns include: `Issue ID`, `App ID`, `Application`, `Result`, `Evidence`, `Dataset Action`.
- **Sheet `Waze Extracted Records`**: Contains 7 non-empty rows (7 max rows, 7 max cols). Primary columns include: `Declared ID`, `App ID`, `Raw Policy Term`, `Normalized Data Type ID`, `Purpose`, `Evidence Location`.
- **Sheet `Freeze Gate v1.2`**: Contains 12 non-empty rows (12 max rows, 4 max cols). Primary columns include: `Gate`, `Requirement`, `Result`, `Decision`.

**Important data/counts**
- Primary worksheet (`Final Remediation Pass`) contains **5 rows** across 3 total worksheet(s).

**Use case**
Completes Stage 3C QA remediation and approves dataset for matrix filling.

**Where it fits in the workflow**
Feeds directly into Stage 3D Matrix v1.0.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate QA Artifact**

**Relationship to other files**
- Stage: Stage 3C. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.0.xlsx`

**What this file contains**
Initial unpopulated Policy Annotation Matrix structure

**Worksheets / Sections**
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.

**Important data/counts**
- Primary worksheet (`3D Full Annotation Matrix`) contains **100 rows** across 31 total worksheet(s).

**Use case**
Provides blank annotation matrix initialized with expected mappings.

**Where it fits in the workflow**
Feeds into v1.1 FILLED.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Matrix Artifact**

**Relationship to other files**
- Stage: Stage 3D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.1_FILLED.xlsx`

**What this file contains**
Populated annotation matrix with initial policy declarations

**Worksheets / Sections**
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Annotation Audit`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Remaining Annotation Queue`**: Contains 86 non-empty rows (86 max rows, 10 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function ID`, `Data Type ID`, `Data Type`.

**Important data/counts**
- Primary worksheet (`3D Full Annotation Matrix`) contains **100 rows** across 33 total worksheet(s).

**Use case**
Initial population of declaration codes across expected mappings.

**Where it fits in the workflow**
Feeds into batch annotation process (v1.2).

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Matrix Artifact**

**Relationship to other files**
- Stage: Stage 3D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.2_ANNOTATED_BATCH.xlsx`

**What this file contains**
Incremental annotation matrix after Batch 1 processing

**Worksheets / Sections**
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Remaining Annotation Queue`**: Contains 78 non-empty rows (78 max rows, 10 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function ID`, `Data Type ID`, `Data Type`.
- **Sheet `3D Annotation Audit`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.

**Important data/counts**
- Primary worksheet (`3D Full Annotation Matrix`) contains **100 rows** across 33 total worksheet(s).

**Use case**
Records policy annotations and evidence text for Batch 1.

**Where it fits in the workflow**
Progresses to v1.3.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Matrix Artifact**

**Relationship to other files**
- Stage: Stage 3D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.3_ANNOTATED_BATCH.xlsx`

**What this file contains**
Incremental annotation matrix after Batch 2 processing

**Worksheets / Sections**
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Remaining Annotation Queue`**: Contains 60 non-empty rows (60 max rows, 10 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function ID`, `Data Type ID`, `Data Type`.
- **Sheet `3D Annotation Audit`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.

**Important data/counts**
- Primary worksheet (`3D Full Annotation Matrix`) contains **100 rows** across 34 total worksheet(s).

**Use case**
Records policy annotations and evidence text for Batch 2.

**Where it fits in the workflow**
Progresses to v1.4.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Matrix Artifact**

**Relationship to other files**
- Stage: Stage 3D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.4_ANNOTATED_BATCH.xlsx`

**What this file contains**
Incremental annotation matrix after Batch 3 processing

**Worksheets / Sections**
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Remaining Annotation Queue`**: Contains 46 non-empty rows (46 max rows, 10 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function ID`, `Data Type ID`, `Data Type`.
- **Sheet `3D Annotation Audit`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.

**Important data/counts**
- Primary worksheet (`3D Full Annotation Matrix`) contains **100 rows** across 34 total worksheet(s).

**Use case**
Records policy annotations and evidence text for Batch 3.

**Where it fits in the workflow**
Progresses to v1.5.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Matrix Artifact**

**Relationship to other files**
- Stage: Stage 3D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.5_ANNOTATED_BATCH.xlsx`

**What this file contains**
Incremental annotation matrix completing full 30-app annotation pass

**Worksheets / Sections**
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Remaining Annotation Queue`**: Contains 32 non-empty rows (32 max rows, 10 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function ID`, `Data Type ID`, `Data Type`.
- **Sheet `3D Annotation Audit`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.

**Important data/counts**
- Primary worksheet (`3D Full Annotation Matrix`) contains **100 rows** across 34 total worksheet(s).

**Use case**
Completes initial annotation pass across all applications.

**Where it fits in the workflow**
Progresses to v1.6 FINAL.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Matrix Artifact**

**Relationship to other files**
- Stage: Stage 3D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.6_FINAL_ANNOTATION.xlsx`

**What this file contains**
Finalized primary annotations prior to completion/evidence review

**Worksheets / Sections**
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.
- **Sheet `3D Remaining Annotation Queue`**: Contains 24 non-empty rows (24 max rows, 10 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function ID`, `Data Type ID`, `Data Type`.
- **Sheet `3D Annotation Audit`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Final Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Item`, `Value`, `Status`.

**Important data/counts**
- Primary worksheet (`3D Full Annotation Matrix`) contains **100 rows** across 35 total worksheet(s).

**Use case**
Consolidates primary annotation pass across all 99 mappings.

**Where it fits in the workflow**
Progresses to v1.7 COMPLETION REVIEW.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Matrix Artifact**

**Relationship to other files**
- Stage: Stage 3D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.7_COMPLETION_REVIEW.xlsx`

**What this file contains**
Audit review tracking missing fields and evidence gaps

**Worksheets / Sections**
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.
- **Sheet `3D Final Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Item`, `Value`, `Status`.
- **Sheet `3D v1.7 Review Tracker`**: Contains 24 non-empty rows (24 max rows, 9 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Status`.
- **Sheet `3D v1.7 Audit`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.

**Important data/counts**
- Primary worksheet (`3D Full Annotation Matrix`) contains **100 rows** across 35 total worksheet(s).

**Use case**
Identifies incomplete annotations and missing text evidence.

**Where it fits in the workflow**
Triggers Evidence Completion files and v1.8.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Audit / Review Matrix**

**Relationship to other files**
- Stage: Stage 3D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3D_Policy_Annotation_Matrix_v1.8_EVIDENCE_REVIEW.xlsx`

**What this file contains**
Review matrix validating policy evidence quotes and provenance

**Worksheets / Sections**
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.
- **Sheet `3D Final Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Item`, `Value`, `Status`.
- **Sheet `3D v1.8 Review Tracker`**: Contains 7 non-empty rows (7 max rows, 8 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Status`.
- **Sheet `3D v1.8 Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.

**Important data/counts**
- Primary worksheet (`3D Full Annotation Matrix`) contains **100 rows** across 35 total worksheet(s).

**Use case**
Verifies exact text quotes against policy registry URLs.

**Where it fits in the workflow**
Progresses to v1.9 STAGE3 FREEZE.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Audit / Review Matrix**

**Relationship to other files**
- Stage: Stage 3D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3D_Policy_Evidence_Completion_v1.0.xlsx`

**What this file contains**
Dedicated workflow file for filling evidence gaps identified in v1.7

**Worksheets / Sections**
- **Sheet `3D Official Evidence`**: Contains 11 non-empty rows (11 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.

**Important data/counts**
- Primary worksheet (`3D Official Evidence`) contains **11 rows** across 28 total worksheet(s).

**Use case**
Gathers missing policy text quotes and re-evaluates ambiguous mappings.

**Where it fits in the workflow**
Superseded by v1.1.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Remediation Artifact**

**Relationship to other files**
- Stage: Stage 3D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3D_Policy_Evidence_Completion_v1.1.xlsx`

**What this file contains**
Finalized evidence completion workbook establishing complete quotes

**Worksheets / Sections**
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.

**Important data/counts**
- Primary worksheet (`3D Official Evidence`) contains **21 rows** across 28 total worksheet(s).

**Use case**
Completes text evidence insertion for remaining incomplete mappings.

**Where it fits in the workflow**
Integrated into Stage 3D v1.9 Freeze.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Remediation Artifact**

**Relationship to other files**
- Stage: Stage 3D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage3D_v1.9_STAGE3_FREEZE_AND_STAGE4_READY.xlsx`

**What this file contains**
Final frozen Stage 3 dataset ready for Stage 4 FDO analysis

**Worksheets / Sections**
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.
- **Sheet `3D Final Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Item`, `Value`, `Status`.
- **Sheet `3D v1.8 Review Tracker`**: Contains 7 non-empty rows (7 max rows, 8 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Status`.
- **Sheet `3D v1.8 Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D v1.9 Final Review`**: Contains 7 non-empty rows (7 max rows, 7 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Current Status`, `Resolution`, `Evidence Requirement`.
- **Sheet `Stage 3 Freeze`**: Contains 13 non-empty rows (13 max rows, 2 max cols). Primary columns include: `Field`, `Value`.
- **Sheet `Stage 4 Ready Dataset`**: Contains 94 non-empty rows (94 max rows, 13 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.

**Important data/counts**
- Primary worksheet (`3D Full Annotation Matrix`) contains **100 rows** across 38 total worksheet(s).

**Use case**
Establishes frozen evidence-backed set (93 mappings) and documents policy exceptions.

**Where it fits in the workflow**
Feeds directly into Stage 4A Necessity Analysis.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Final Stage 3 Freeze Artifact**

**Relationship to other files**
- Stage: Stage 3D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage4A_Expected_vs_Declared_Matching_v1.0.xlsx`

**What this file contains**
Initial matching of expected necessity against declared data

**Worksheets / Sections**
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.

**Important data/counts**
- Primary worksheet (`4A Expected vs Declared`) contains **100 rows** across 15 total worksheet(s).

**Use case**
Initial comparison of expected baseline against policy declarations.

**Where it fits in the workflow**
Superseded by FDO_Necessity_Analysis_v1.1.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Analysis Artifact**

**Relationship to other files**
- Stage: Stage 4A. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage4A_FDO_Necessity_Analysis_v1.1.xlsx`

**What this file contains**
Final necessity analysis evaluating data necessity alignment

**Worksheets / Sections**
- **Sheet `Stage 4A Necessity Analysis`**: Contains 94 non-empty rows (94 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.
- **Sheet `3D Final Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Item`, `Value`, `Status`.
- **Sheet `3D v1.8 Review Tracker`**: Contains 7 non-empty rows (7 max rows, 8 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Status`.
- **Sheet `3D v1.8 Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D v1.9 Final Review`**: Contains 7 non-empty rows (7 max rows, 7 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Current Status`, `Resolution`, `Evidence Requirement`.
- **Sheet `Stage 3 Freeze`**: Contains 13 non-empty rows (13 max rows, 2 max cols). Primary columns include: `Field`, `Value`.
- **Sheet `Stage 4 Ready Dataset`**: Contains 94 non-empty rows (94 max rows, 13 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4A Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4A Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.

**Important data/counts**
- Primary worksheet (`Stage 4A Necessity Analysis`) contains **94 rows** across 41 total worksheet(s).

**Use case**
Classifies mappings by necessity tier and identifies candidates needing purpose review.

**Where it fits in the workflow**
Feeds into Stage 4B Purpose Compatibility.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Analysis Artifact (Stage 4A)**

**Relationship to other files**
- Stage: Stage 4A. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage4B_Purpose_Compatibility_Review_v1.0.xlsx`

**What this file contains**
Preliminary review queue for purpose compatibility testing

**Worksheets / Sections**
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.

**Important data/counts**
- Primary worksheet (`4B Purpose Compatibility`) contains **100 rows** across 18 total worksheet(s).

**Use case**
Filters necessity findings into preliminary purpose evaluation queues.

**Where it fits in the workflow**
Superseded by Purpose_Compatibility_v1.0.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Analysis Artifact**

**Relationship to other files**
- Stage: Stage 4B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage4B_Purpose_Compatibility_v1.0.xlsx`

**What this file contains**
Comprehensive purpose compatibility assessment against policy evidence

**Worksheets / Sections**
- **Sheet `Stage 4B Purpose Compatibility`**: Contains 94 non-empty rows (94 max rows, 16 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4A Necessity Analysis`**: Contains 94 non-empty rows (94 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.
- **Sheet `3D Final Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Item`, `Value`, `Status`.
- **Sheet `3D v1.8 Review Tracker`**: Contains 7 non-empty rows (7 max rows, 8 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Status`.
- **Sheet `3D v1.8 Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D v1.9 Final Review`**: Contains 7 non-empty rows (7 max rows, 7 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Current Status`, `Resolution`, `Evidence Requirement`.
- **Sheet `Stage 3 Freeze`**: Contains 13 non-empty rows (13 max rows, 2 max cols). Primary columns include: `Field`, `Value`.
- **Sheet `Stage 4 Ready Dataset`**: Contains 94 non-empty rows (94 max rows, 13 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4A Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4A Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 4B Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4B Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.

**Important data/counts**
- Primary worksheet (`Stage 4B Purpose Compatibility`) contains **94 rows** across 44 total worksheet(s).

**Use case**
Evaluates whether declared collection purposes match expected functional necessity.

**Where it fits in the workflow**
Feeds into Stage 4C Candidate Screening.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Analysis Artifact (Stage 4B)**

**Relationship to other files**
- Stage: Stage 4B. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage4C_FDO_Candidate_Identification_v1.0.xlsx`

**What this file contains**
Initial candidate identification list for potential FDO cases

**Worksheets / Sections**
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.

**Important data/counts**
- Primary worksheet (`4C FDO Candidates`) contains **12 rows** across 21 total worksheet(s).

**Use case**
Drafts potential FDO candidates based on necessity/purpose mismatches.

**Where it fits in the workflow**
Superseded by Candidate_Screening_v1.0.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Analysis Artifact**

**Relationship to other files**
- Stage: Stage 4C. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage4C_FDO_Candidate_Screening_v1.0.xlsx`

**What this file contains**
Formal screening filtering non-candidates from true adjudication queue

**Worksheets / Sections**
- **Sheet `Stage 4C Candidate Screening`**: Contains 94 non-empty rows (94 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4B Purpose Compatibility`**: Contains 94 non-empty rows (94 max rows, 16 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4A Necessity Analysis`**: Contains 94 non-empty rows (94 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.
- **Sheet `3D Final Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Item`, `Value`, `Status`.
- **Sheet `3D v1.8 Review Tracker`**: Contains 7 non-empty rows (7 max rows, 8 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Status`.
- **Sheet `3D v1.8 Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D v1.9 Final Review`**: Contains 7 non-empty rows (7 max rows, 7 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Current Status`, `Resolution`, `Evidence Requirement`.
- **Sheet `Stage 3 Freeze`**: Contains 13 non-empty rows (13 max rows, 2 max cols). Primary columns include: `Field`, `Value`.
- **Sheet `Stage 4 Ready Dataset`**: Contains 94 non-empty rows (94 max rows, 13 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4A Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4A Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 4B Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4B Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 4C Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4C Decision Rules`**: Contains 5 non-empty rows (5 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.

**Important data/counts**
- Primary worksheet (`Stage 4C Candidate Screening`) contains **94 rows** across 47 total worksheet(s).

**Use case**
Applies screening rules to separate non-candidates from adjudication candidates.

**Where it fits in the workflow**
Feeds into Stage 4D Detailed Adjudication.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Analysis Artifact (Stage 4C)**

**Relationship to other files**
- Stage: Stage 4C. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage4D_Detailed_Adjudication_v1.0.xlsx`

**What this file contains**
Master adjudication workbook applying multi-test FDO rules

**Worksheets / Sections**
- **Sheet `Stage 4D Detailed Adjudication`**: Contains 94 non-empty rows (94 max rows, 18 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4C Candidate Screening`**: Contains 94 non-empty rows (94 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4B Purpose Compatibility`**: Contains 94 non-empty rows (94 max rows, 16 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4A Necessity Analysis`**: Contains 94 non-empty rows (94 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.
- **Sheet `3D Final Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Item`, `Value`, `Status`.
- **Sheet `3D v1.8 Review Tracker`**: Contains 7 non-empty rows (7 max rows, 8 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Status`.
- **Sheet `3D v1.8 Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D v1.9 Final Review`**: Contains 7 non-empty rows (7 max rows, 7 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Current Status`, `Resolution`, `Evidence Requirement`.
- **Sheet `Stage 3 Freeze`**: Contains 13 non-empty rows (13 max rows, 2 max cols). Primary columns include: `Field`, `Value`.
- **Sheet `Stage 4 Ready Dataset`**: Contains 94 non-empty rows (94 max rows, 13 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4A Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4A Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 4B Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4B Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 4C Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4C Decision Rules`**: Contains 5 non-empty rows (5 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Test`, `Rule`.

**Important data/counts**
- Primary worksheet (`Stage 4D Detailed Adjudication`) contains **94 rows** across 50 total worksheet(s).

**Use case**
Applies necessity, purpose, and functional justification tests to candidate mappings.

**Where it fits in the workflow**
Feeds into Stage 4E Ambiguous Case Resolution.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Analysis Artifact (Stage 4D)**

**Relationship to other files**
- Stage: Stage 4D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage4D_FDO_Adjudication_v1.0.xlsx`

**What this file contains**
Focused adjudication subset workbook for candidate cases

**Worksheets / Sections**
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.

**Important data/counts**
- Primary worksheet (`4D Adjudication`) contains **12 rows** across 25 total worksheet(s).

**Use case**
Contains concentrated adjudication notes for the candidate subset.

**Where it fits in the workflow**
Complements Detailed Adjudication v1.0.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Intermediate Analysis Artifact**

**Relationship to other files**
- Stage: Stage 4D. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage4E_Ambiguous_Case_Resolution_v1.0.xlsx`

**What this file contains**
Final Stage 4 resolution of ambiguous cases and freeze of final FDO labels

**Worksheets / Sections**
- **Sheet `Stage 4E Ambiguous Resolution`**: Contains 94 non-empty rows (94 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4D Detailed Adjudication`**: Contains 94 non-empty rows (94 max rows, 18 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4C Candidate Screening`**: Contains 94 non-empty rows (94 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4B Purpose Compatibility`**: Contains 94 non-empty rows (94 max rows, 16 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4A Necessity Analysis`**: Contains 94 non-empty rows (94 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.
- **Sheet `3D Final Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Item`, `Value`, `Status`.
- **Sheet `3D v1.8 Review Tracker`**: Contains 7 non-empty rows (7 max rows, 8 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Status`.
- **Sheet `3D v1.8 Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D v1.9 Final Review`**: Contains 7 non-empty rows (7 max rows, 7 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Current Status`, `Resolution`, `Evidence Requirement`.
- **Sheet `Stage 3 Freeze`**: Contains 13 non-empty rows (13 max rows, 2 max cols). Primary columns include: `Field`, `Value`.
- **Sheet `Stage 4 Ready Dataset`**: Contains 94 non-empty rows (94 max rows, 13 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4A Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4A Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 4B Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4B Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 4C Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4C Decision Rules`**: Contains 5 non-empty rows (5 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Test`, `Rule`.
- **Sheet `Stage 4E Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4E Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.

**Important data/counts**
- Primary worksheet (`Stage 4E Ambiguous Resolution`) contains **94 rows** across 53 total worksheet(s).

**Use case**
Resolves borderline cases, preserves explicit AMBIGUOUS state, and sets final Stage 5 labels.

**Where it fits in the workflow**
Feeds directly into Stage 5/6 Visualization.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Final Stage 4 Analysis Artifact**

**Relationship to other files**
- Stage: Stage 4E. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx`

**What this file contains**
Consolidated results workbook with dashboards, statistics, charts, and master sheets

**Worksheets / Sections**
- **Sheet `Stage 6 Findings`**: Contains 6 non-empty rows (6 max rows, 5 max cols). Primary columns include: `Finding ID`, `Finding`, `Result`, `Interpretation`, `Caution`.
- **Sheet `Stage 5 Final Mapping Dataset`**: Contains 94 non-empty rows (94 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4E Ambiguous Resolution`**: Contains 94 non-empty rows (94 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4D Detailed Adjudication`**: Contains 94 non-empty rows (94 max rows, 18 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4C Candidate Screening`**: Contains 94 non-empty rows (94 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4B Purpose Compatibility`**: Contains 94 non-empty rows (94 max rows, 16 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4A Necessity Analysis`**: Contains 94 non-empty rows (94 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Full Annotation Matrix`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `3D Official Evidence`**: Contains 21 non-empty rows (21 max rows, 9 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Policy/Data Area`, `Declared Data Supported`, `Purpose / Use Supported`.
- **Sheet `4D Adjudication`**: Contains 12 non-empty rows (12 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4C FDO Candidates`**: Contains 12 non-empty rows (12 max rows, 14 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4B Purpose Compatibility`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `4A Expected vs Declared`**: Contains 100 non-empty rows (100 max rows, 17 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 3 Dataset`**: Contains 134 non-empty rows (134 max rows, 18 max cols). Primary columns include: `Layer`, `Record ID`, `App ID`, `Application`, `Function ID`, `Function`.
- **Sheet `README`**: Contains 12 non-empty rows (12 max rows, 2 max cols). Primary columns include: `FDO-Privacy Final Stage 3 Dataset`, `v1.1 FULL`.
- **Sheet `Applications`**: Contains 31 non-empty rows (31 max rows, 6 max cols). Primary columns include: `App ID`, `Application`, `Category`, `Stage 4 Inclusion`, `Policy Exception`, `Notes`.
- **Sheet `Expected Data`**: Contains 100 non-empty rows (100 max rows, 15 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Feature ID`, `Feature`.
- **Sheet `Policy Registry`**: Contains 31 non-empty rows (31 max rows, 11 max cols). Primary columns include: `Policy ID`, `App ID`, `Application`, `Policy URL/Source`, `Policy Title`, `Effective/Updated`.
- **Sheet `Declared Data`**: Contains 35 non-empty rows (35 max rows, 13 max cols). Primary columns include: `Declared ID`, `App ID`, `Application`, `Raw Policy Term`, `Normalized Data Type ID`, `Collection Mode`.
- **Sheet `Evidence`**: Contains 31 non-empty rows (31 max rows, 8 max cols). Primary columns include: `Evidence ID`, `App ID`, `Application`, `Evidence Type`, `Source Ref`, `Evidence Strength`.
- **Sheet `Exceptions`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Exception ID`, `App ID`, `Application`, `Reason`, `Current Handling`, `Resolution Condition`.
- **Sheet `QA Freeze`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `Check`, `Result`, `Details`.
- **Sheet `Data Dictionary`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Meaning`.
- **Sheet `Record Count Audit`**: Contains 8 non-empty rows (8 max rows, 4 max cols). Primary columns include: `Dataset Component`, `Count`, `Source Sheet`, `Meaning`.
- **Sheet `Stage 4 Input — Blank`**: Contains 28 non-empty rows (28 max rows, 8 max cols). Primary columns include: `App ID`, `Function ID`, `Data Type ID`, `Expected Necessity`, `Declared Presence`, `Purpose Compatibility`.
- **Sheet `4A Declared-Only Review`**: Contains 23 non-empty rows (23 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4A Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `4B Adjudication Queue`**: Contains 89 non-empty rows (89 max rows, 8 max cols). Primary columns include: `Queue ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Match Status`.
- **Sheet `4B Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4C Declared-Only Candidates`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4C Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Declared-Only Adjudication`**: Contains 20 non-empty rows (20 max rows, 10 max cols). Primary columns include: `App ID`, `Declared ID`, `Declared Data Type ID`, `Raw Policy Term`, `Declared Purpose`, `Evidence Ref`.
- **Sheet `4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `3D Completion Queue`**: Contains 31 non-empty rows (31 max rows, 5 max cols). Primary columns include: `App ID`, `Application`, `Current Stage-3 Policy Evidence State`, `Next Required Action`, `Stage-4 Ready?`.
- **Sheet `3D Summary`**: Contains 7 non-empty rows (7 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `3D Annotation Guide`**: Contains 9 non-empty rows (9 max rows, 2 max cols). Primary columns include: `Field`, `Allowed values / instruction`.
- **Sheet `3D Coverage Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D Batch Summary`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Item`, `Value`.
- **Sheet `3D Final Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Item`, `Value`, `Status`.
- **Sheet `3D v1.8 Review Tracker`**: Contains 7 non-empty rows (7 max rows, 8 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Function`, `Data Type`, `Current Status`.
- **Sheet `3D v1.8 Status`**: Contains 8 non-empty rows (8 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Meaning`.
- **Sheet `3D v1.9 Final Review`**: Contains 7 non-empty rows (7 max rows, 7 max cols). Primary columns include: `Review ID`, `Expected ID`, `App ID`, `Current Status`, `Resolution`, `Evidence Requirement`.
- **Sheet `Stage 3 Freeze`**: Contains 13 non-empty rows (13 max rows, 2 max cols). Primary columns include: `Field`, `Value`.
- **Sheet `Stage 4 Ready Dataset`**: Contains 94 non-empty rows (94 max rows, 13 max cols). Primary columns include: `Expected ID`, `App ID`, `Function ID`, `Function`, `Data Type ID`, `Data Type`.
- **Sheet `Stage 4A Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4A Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 4B Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4B Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 4C Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4C Decision Rules`**: Contains 5 non-empty rows (5 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 4D Summary`**: Contains 6 non-empty rows (6 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4D Decision Rules`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Test`, `Rule`.
- **Sheet `Stage 4E Summary`**: Contains 5 non-empty rows (5 max rows, 3 max cols). Primary columns include: `Metric`, `Count`, `Interpretation`.
- **Sheet `Stage 4E Decision Rules`**: Contains 6 non-empty rows (6 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 5 App Summary`**: Contains 30 non-empty rows (30 max rows, 7 max cols). Primary columns include: `App ID`, `Total Mappings in Final Dataset`, `NOT_FDO`, `AMBIGUOUS`, `FDO`, `FDO Rate*`.
- **Sheet `Stage 5 Overall Statistics`**: Contains 12 non-empty rows (12 max rows, 3 max cols). Primary columns include: `Metric`, `Value`, `Interpretation`.
- **Sheet `Stage 5 Methodology`**: Contains 7 non-empty rows (7 max rows, 2 max cols). Primary columns include: `Rule`, `Application`.
- **Sheet `Stage 6 Results Dashboard`**: Contains 10 non-empty rows (10 max rows, 3 max cols). Primary columns include: `FDO-Privacy — Stage 6 Results Dashboard`, `Value`, `Notes`.
- **Sheet `Stage 6 Charts`**: Contains 4 non-empty rows (4 max rows, 6 max cols). Primary columns include: `Outcome`, `Count`, ``, ``, `Stage-5 Resolved Outcome`.

**Important data/counts**
- Primary worksheet (`Stage 6 Findings`) contains **6 rows** across 60 total worksheet(s).

**Use case**
Provides complete analytical statistics (60 NOT_FDO, 33 AMBIGUOUS, 0 FDO), charts, and multi-stage consolidations.

**Where it fits in the workflow**
Serves as the primary quantitative source for the Stage 7 Report.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Final Results & Visualization Artifact**

**Relationship to other files**
- Stage: Stage 6. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

### `FDO-Privacy_Stage7_Final_Research_Report_Package_v1.0.docx`

**What this file contains**
Comprehensive final research report package consolidating all project findings

**Worksheets / Sections**
- Contains **70 paragraphs** and **1 table(s)**.
- **Major Headings / Document Structure**:
  - `1. Executive Summary` (Heading 1)
  - `2. Research Problem` (Heading 1)
  - `3. Project Objective` (Heading 1)
  - `4. Innovation / Novelty` (Heading 1)
  - `5. Dataset and Scope` (Heading 1)
  - `6. Methodology` (Heading 1)
  - `6.1 Expected-data modelling` (Heading 2)
  - `6.2 Policy evidence annotation` (Heading 2)
  - `6.3 Stage 4A — Necessity analysis` (Heading 2)
  - `6.4 Stage 4B — Purpose compatibility` (Heading 2)
  - `6.5 Stage 4C–4E — Candidate screening and adjudication` (Heading 2)
  - `7. Results` (Heading 1)
  - `8. Key Research Finding` (Heading 1)
  - `9. Limitations and Threats to Validity` (Heading 1)
  - `10. Conclusion` (Heading 1)
  - `11. Future Work` (Heading 1)
  - `12. Project Implementation Roadmap` (Heading 1)
  - `13. Presentation-Ready Result` (Heading 1)
  - `14. Source Artifact` (Heading 1)

**Important data/counts**
- Document spans 14 major numbered sections and 5 subsections consolidating the complete research project.

**Use case**
Consolidates project methodology, findings, limitations, roadmap, and presentation-ready executive statements.

**Where it fits in the workflow**
Final output deliverable of the FDO-Privacy research project.

**Is it an input, intermediate, final, audit, or reporting artifact?**
- Classified as: **Final Research Deliverable**

**Relationship to other files**
- Stage: Stage 7. Interlinks with preceding and succeeding files in the Stage 1 → Stage 7 pipeline.

---

## 5. Version / Evolution History

| Version / File | What changed | Why it matters | Status |
|---|---|---|---|
| `Stage2B_Pilot_v0.2` → `v0.5` | Incremental batch annotation across Pilot Batches 01 to 04 | Built initial 30-app pilot annotation dataset | Intermediate / Superseded |
| `Stage2B_AnnotatorA` / `AnnotatorB` | Dual independent annotation passes across 4 batches | Enabled inter-annotator agreement metrics | Audit / Annotation |
| `Stage2B_Agreement_Analysis_v1.0` | Calculated agreement metrics and logged ontology revisions | Standardized annotation rules for Stage 3 | Active Audit Baseline |
| `Stage2B_Agreement_Analysis_v1.0 (1)` | Exact duplicate creation in filesystem | Unintended file duplicate | Superseded Duplicate |
| `Stage3A_Dataset_Schema_v1.0` | Formalized canonical dataset schema and expected 99 mappings | Established fixed baseline for Stage 3 policy extraction | Active Baseline Schema |
| `Stage3B_Policy_Extraction_Batch01` → `Complete` | Expanded text extractions for Batch 1 applications | Replaced partial extractions with complete quotes | Superseded by Complete |
| `Stage3B_Policy_Registry_Batch01` → `v2` | Updated policy URLs, retrieval dates, and provenance links | Corrected broken policy links and dates | Superseded by v2 |
| `Stage3C_Integration_QA_v1.0` → `v1.2` | Identified defect gaps and performed two remediation rounds | Corrected extraction formatting and evidence gaps | Superseded by v1.2 |
| `Stage3D_Policy_Annotation_Matrix_v1.0` → `v1.6` | Filled matrix incrementally from v1.0 blank to v1.6 full annotation | Completed primary policy declaration pass | Superseded by v1.9 |
| `Stage3D_Policy_Annotation_Matrix_v1.7` → `v1.8` | Added completion review queues and evidence quote verification | Ensured 100% text quote coverage for declared items | Superseded by v1.9 |
| `Stage3D_Policy_Evidence_Completion_v1.0` → `v1.1` | Isolated incomplete evidence rows and added missing text quotes | Resolved missing quote defects prior to freeze | Superseded by v1.1 |
| `Stage3D_v1.9_STAGE3_FREEZE` | Integrated evidence completion into frozen master matrix | Established 93 evidence-backed mapping freeze | Active Stage 3 Freeze |
| `Final_Stage3_Dataset_CLEANED` vs `COMPLETE` | Separated clean user view (18 cols) from master view (22 cols) | Provided lightweight analytical set alongside full master | Both Active (Final Stage 3) |
| `Stage4A_Matching_v1.0` → `Necessity_Analysis_v1.1` | Refined expected vs declared matching into formal necessity tiers | Formed initial necessity input for Stage 4B | Active Stage 4A Baseline |
| `Stage4B_Review_v1.0` → `Purpose_Compatibility_v1.0` | Expanded purpose review queue into complete compatibility matrix | Evaluated purpose alignment against expected function | Active Stage 4B Baseline |
| `Stage4C_Identification_v1.0` → `Screening_v1.0` | Formalized candidate screening rules and candidate queues | Filtered non-candidates from true adjudication queue | Active Stage 4C Baseline |
| `Stage4D_Detailed_Adjudication_v1.0` & `FDO_Adjudication_v1.0` | Applied multi-test FDO rules to candidate mappings | Established preliminary FDO decision justifications | Active Stage 4D Baseline |
| `Stage4E_Ambiguous_Case_Resolution_v1.0` | Resolved borderline cases and locked final Stage 5 labels | Locked 60 NOT_FDO, 33 AMBIGUOUS, 0 FDO | Active Stage 4 Freeze |
| `Stage6_Results_Visualization_v1.0` | Built master consolidated workbook with 60 sheets and dashboards | Provided single source of truth for charts and stats | Active Stage 6 Baseline |
| `Stage7_Final_Research_Report_Package_v1.0.docx` | Drafted formal 14-section research paper deliverable | Consolidated complete project for publication/presentation | Final Deliverable |


## 6. Stage-by-Stage Artifact Map

| Stage | Main Goal | Files Used / Produced | Output |
|---|---|---|---|
| **Stage 1** | Define research scope, problem statement, and evaluation framework | Initial design specifications | Research Framework & Scope |
| **Stage 2** | Build expected-data model and execute 30-app pilot annotation | `Stage2B_Pilot_v0.2`-`v0.5`, `Stage2B_AnnotatorA/B` files, `Stage2B_Agreement_Analysis_v1.0` | 99 Expected Mappings & Pilot Agreement Metrics |
| **Stage 3** | Extract policy evidence, conduct QA remediation, and freeze Stage 3 dataset | `Stage3A_Schema_v1.0`, `Stage3B_Extraction/Registry` files, `Stage3C_QA_v1.0`-`v1.2`, `Stage3D_Matrix_v1.0`-`v1.9`, `Final_Stage3_Dataset_CLEANED/COMPLETE` | 93 Evidence-Backed Mappings & Frozen Stage 3 Master |
| **Stage 4** | Perform 5-tier FDO analysis (Necessity, Purpose, Screening, Adjudication, Ambiguity Resolution) | `Stage4A_Necessity_Analysis_v1.1`, `Stage4B_Purpose_Compatibility_v1.0`, `Stage4C_Candidate_Screening_v1.0`, `Stage4D_Detailed_Adjudication_v1.0`, `Stage4E_Ambiguous_Case_Resolution_v1.0` | Adjudicated FDO Labels (60 NOT_FDO, 33 AMBIGUOUS, 0 FDO) |
| **Stage 5** | Consolidate mapping-level dataset and calculate empirical statistics | Derived inside `Stage4E` and `Stage6` workbooks | Final Mapping-Level Dataset & Statistics |
| **Stage 6** | Build interactive dashboards, visualization charts, and research summary | `Stage6_Results_Visualization_and_Findings_v1.0.xlsx` | Results Dashboard & 60-Sheet Master Workbook |
| **Stage 7** | Synthesize research methodology, findings, validity threats, and roadmap into report package | `Stage7_Final_Research_Report_Package_v1.0.docx` | Comprehensive 14-Section DOCX Research Report |


## 7. Dataset Lineage

The data lineage flows sequentially through the 7 project stages as depicted below:

```
Original Pilot Application Roster (30 Apps)
  ↓ [Stage2B Pilot Files & Agreement Analysis]
Expected-Data Model Baseline (99 Expected Mappings across 30 Apps)
  ↓ [Stage3A Schema v1.0]
Policy Evidence Extraction & Registry Construction (Batches 01–03)
  ↓ [Stage3B Policy Extraction & Registry Files]
Integration & QA Remediation (Defect Fixes & Quote Standardization)
  ↓ [Stage3C QA Remediation v1.1 / v1.2]
Policy Annotation Matrix Iteration (v1.0 Blank → v1.6 Final Annotation)
  ↓ [Stage3D Matrix v1.0–v1.6]
Evidence Completion & Provenance Review (100% Text Quote Coverage)
  ↓ [Stage3D Evidence Completion v1.0 / v1.1 & Matrix v1.7 / v1.8]
Stage 3 Dataset Freeze (93 Evidence-Backed Mappings; 27 Analytical Apps; 3 Policy Exceptions)
  ↓ [Stage3D v1.9 Freeze & Final Stage 3 CLEANED / COMPLETE]
Stage 4A: FDO Necessity Analysis (Expected vs Declared Matching)
  ↓ [Stage4A Necessity Analysis v1.1]
Stage 4B: Expected-Purpose vs Declared-Purpose Compatibility Assessment
  ↓ [Stage4B Purpose Compatibility v1.0]
Stage 4C: FDO Candidate Screening (Filtering Non-Candidates)
  ↓ [Stage4C Candidate Screening v1.0]
Stage 4D: Detailed FDO Adjudication (Necessity, Purpose & Functional Justification Tests)
  ↓ [Stage4D Detailed Adjudication v1.0]
Stage 4E: Ambiguous-Case Resolution & Final FDO Label Freeze
  ↓ [Stage4E Ambiguous Case Resolution v1.0]
Stage 5/6: Final FDO Dataset Consolidation & Results Visualization
  ↓ [Stage6 Results Visualization and Findings v1.0]
Stage 7: Final Research Report Package Synthesis
  ↓ [Stage7 Final Research Report Package v1.0.docx]
```

### Transition Highlights & Primary Artifacts:
1. **Pilot → Expected Baseline**: `Stage2B_Pilot_v0.5_Batch04.xlsx` and `Stage2B_Agreement_Analysis_v1.0.xlsx` established the 99 expected mappings across 30 pilot applications.
2. **Expected Baseline → Extraction**: `Stage3A_Dataset_Schema_v1.0.xlsx` defined the schema for `Stage3B_Policy_Extraction_Batch01_Complete.xlsx` and registry files.
3. **Extraction → Integration QA**: Extractions were frozen in `Stage3C_Dataset_Freeze_v1.0.xlsx`, audited in `Stage3C_Integration_QA_v1.0.xlsx`, and remediated in `Stage3C_QA_Remediation_v1.2.xlsx`.
4. **QA → Matrix Annotations**: Clean extractions populated `Stage3D_Policy_Annotation_Matrix_v1.1_FILLED.xlsx`, progressing through `v1.6_FINAL_ANNOTATION.xlsx`.
5. **Annotations → Stage 3 Freeze**: Evidence gaps were resolved in `Stage3D_Policy_Evidence_Completion_v1.1.xlsx` and locked in `Stage3D_v1.9_STAGE3_FREEZE_AND_STAGE4_READY.xlsx` (and `Final_Stage3_Dataset_CLEANED/COMPLETE.xlsx`). This established the 27-app analytical cohort (excluding Instagram, PUBG MOBILE, WeChat).
6. **Stage 3 Freeze → Stage 4 Pipeline**: Sequential execution of `Stage4A_FDO_Necessity_Analysis_v1.1.xlsx` → `Stage4B_Purpose_Compatibility_v1.0.xlsx` → `Stage4C_FDO_Candidate_Screening_v1.0.xlsx` → `Stage4D_Detailed_Adjudication_v1.0.xlsx` → `Stage4E_Ambiguous_Case_Resolution_v1.0.xlsx`.
7. **Stage 4 Freeze → Results & Report**: `Stage4E` locked the final dataset (60 NOT_FDO, 33 AMBIGUOUS, 0 FDO), which was visualized in `Stage6_Results_Visualization_and_Findings_v1.0.xlsx` and reported in `Stage7_Final_Research_Report_Package_v1.0.docx`.

## 8. Final Research Result

Based **EXCLUSIVELY** on the supplied project artifacts, the current empirical results of the FDO-Privacy research project are as follows:

- **Expected Mappings Evaluated**: 99 mappings across 27 analytical applications.
- **Evidence-Backed Mappings**: 93 mappings (6 mappings lacked sufficient policy extraction evidence).
- **NOT_FDO Mappings**: **60 mappings** (64.5% of evidence-backed mappings).
- **AMBIGUOUS Mappings**: **33 mappings** (35.5% of evidence-backed mappings).
- **FDO Mappings Established**: **0 mappings** (0.0% resolved-case FDO rate).

### CRITICAL METHODOLOGICAL DISTINCTION:
> [!IMPORTANT]
> **"0 FDO established" DOES NOT mean that we have proven that no FDO exists in the evaluated applications.**
> 
> Rather, it means that **no FDO was established from the currently available policy evidence and adopted adjudication rules**.
> 
> Furthermore, **33 mappings (35.5%) remain explicitly AMBIGUOUS** due to broad, generic, or incomplete privacy policy language. These ambiguous cases are intentionally retained in the findings and are **NOT** silently converted into negative (NOT_FDO) or positive (FDO) conclusions. The primary resolved-case FDO rate (0%) is strictly conditional on the 60 resolved cases.

## 9. Important Methodological Rules

The project files enforce several fundamental methodological rules governing privacy policy evidence annotation and FDO adjudication:

1. **Missing Policy / Extraction Evidence MUST NOT automatically be treated as "NOT_DECLARED"**:
   - If policy text for a specific function/data-type mapping is absent or unextracted, it must be classified as `SOURCE_INSUFFICIENT` or `AMBIGUOUS`, never assumed to be undeclared.

2. **Ambiguity MUST be preserved explicitly**:
   - Borderline or vaguely worded policy declarations must remain labeled as `AMBIGUOUS`. They must not be forced into binary `FDO` or `NOT_FDO` decisions.

3. **Policy Declaration DOES NOT equal FDO**:
   - The mere fact that an application declares collecting a data type in its privacy policy does not constitute Functionally Excessive Data. FDO requires empirical proof of functional excess or purpose incompatibility.

4. **Optional or Supportive Data Processing is NOT automatically FDO**:
   - Data collected to support optional features, security, analytics, or user choice is evaluated under functional justification rules and is not categorized as FDO merely because it is not strictly required for core app operations (L1).

5. **FDO requires clear evidence of Functional Excess or Purpose Incompatibility**:
   - To assign an `FDO` label, the evidence must prove that the collected data type has no plausible functional necessity and its declared purpose is incompatible with the core feature.

6. **FDO labels are strictly reserved for Stage 4**:
   - Annotators in Stage 2 and Stage 3 record empirical policy declarations (`DECLARED`, `NOT_DECLARED`, `AMBIGUOUS`) and text quotes. FDO decision labels (`FDO`, `NOT_FDO`) are assigned exclusively during Stage 4 adjudication.

## 10. Recommended File to Use for Each Task

| If you want to... | Use this file | Why |
|---|---|---|
| Inspect original expected-data baseline & schema | `FDO-Privacy_Stage3A_Dataset_Schema_v1.0.xlsx` | Contains canonical expected mappings (99), application list, and data dictionary. |
| Inspect raw pilot annotations & agreement metrics | `FDO-Privacy_Stage2B_Agreement_Analysis_v1.0.xlsx` | Evaluates Annotator A/B agreement across pilot batches and tracks ontology revisions. |
| Inspect frozen Stage 3 policy declarations & quotes | `FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx` | Clean, 18-column master sheet of evidence-backed policy declarations for 27 apps. |
| Inspect exhaustive Stage 3 master dataset with full metadata | `FDO-Privacy_Final_Stage3_Dataset_COMPLETE.xlsx` | Complete 22-column master record including full provenance, QA freeze audit, and dictionary. |
| Inspect Stage 4A necessity tier analysis | `FDO-Privacy_Stage4A_FDO_Necessity_Analysis_v1.1.xlsx` | Details expected vs declared necessity matching across L1/L2/L3 tiers. |
| Inspect Stage 4B purpose compatibility evaluations | `FDO-Privacy_Stage4B_Purpose_Compatibility_v1.0.xlsx` | Contains full purpose compatibility reviews matching policy wording to expected purposes. |
| Inspect Stage 4C candidate screening decisions | `FDO-Privacy_Stage4C_FDO_Candidate_Screening_v1.0.xlsx` | Shows candidate screening rules and separation of non-candidates from candidate queues. |
| Inspect Stage 4D detailed adjudication test results | `FDO-Privacy_Stage4D_Detailed_Adjudication_v1.0.xlsx` | Master adjudication matrix applying necessity, purpose, and functional justification tests. |
| Inspect final frozen Stage 4/5 dataset & ambiguity resolution | `FDO-Privacy_Stage4E_Ambiguous_Case_Resolution_v1.0.xlsx` | Locked dataset resolving ambiguous cases and establishing final 60 NOT_FDO / 33 AMBIGUOUS counts. |
| Inspect complete empirical statistics, dashboards & charts | `FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx` | Master 60-sheet consolidated workbook with interactive dashboards, app summaries, and charts. |
| Read the complete, publication-ready research report | `FDO-Privacy_Stage7_Final_Research_Report_Package_v1.0.docx` | Comprehensive 14-section formal report synthesizing methodology, findings, validity threats, and roadmap. |


## 11. Files That Should NOT Be Treated as Final

The following files represent intermediate, superseded, partial, review, or duplicate artifacts and **MUST NOT** be mistaken for the final project dataset or report:

1. **`FDO-Privacy_Stage2B_Agreement_Analysis_v1.0 (1).xlsx`**:
   - *Reason*: Exact filesystem duplicate of `Stage2B_Agreement_Analysis_v1.0.xlsx`.
2. **`Stage2B Pilot Files` (`v0.2`–`v0.5`) & `AnnotatorA/B Batch Files`**:
   - *Reason*: Preliminary pilot annotation batches covering 30 pilot applications prior to Stage 3 schema formalization and cohort freezing.
3. **`Stage3B Partial Extraction & Registry Files` (`Extraction_Batch01`, `Registry_Batch01`)**:
   - *Reason*: Superseded by `Extraction_Batch01_Complete` and `Registry_Batch01_v2`.
4. **`Stage3C QA Remediation v1.1` & `Dataset Freeze v1.0`**:
   - *Reason*: Intermediate QA drafts superseded by `Stage3C_QA_Remediation_v1.2.xlsx`.
5. **`Stage3D Matrix Versions v1.0` through `v1.8`**:
   - *Reason*: Incremental annotation iterations. Superseded by `Stage3D_v1.9_STAGE3_FREEZE_AND_STAGE4_READY.xlsx`.
6. **`Stage3D Policy Evidence Completion v1.0`**:
   - *Reason*: Intermediate evidence completion draft superseded by `v1.1`.
7. **`Stage4 Initial Draft Files` (`Stage4A_Matching_v1.0`, `Stage4B_Review_v1.0`, `Stage4C_Identification_v1.0`, `Stage4D_FDO_Adjudication_v1.0`)**:
   - *Reason*: Preliminary analysis working files superseded by their respective final Stage 4 counterparts (`Stage4A v1.1`, `Stage4B v1.0`, `Stage4C Screening v1.0`, `Stage4D Detailed Adjudication v1.0`, and `Stage4E v1.0`).

## 12. Recommended Project Folder Structure

To maintain a clean, logical organization without modifying or moving existing files, we recommend structuring future project iterations as follows:

```
FDO-Privacy_Project/
├── 01_Project_Design/
│   ├── FDO-Privacy_Stage3A_Dataset_Schema_v1.0.xlsx
├── 02_Expected_Data_&_Pilot/
│   ├── FDO-Privacy_Stage2B_Agreement_Analysis_v1.0.xlsx
│   ├── FDO-Privacy_Stage2B_AnnotatorA_Batch1.xlsx to Batch4.xlsx
│   ├── FDO-Privacy_Stage2B_AnnotatorB_All4Batches.xlsx
│   └── FDO-Privacy_Stage2B_Pilot_v0.2_VerifiedBatch01.xlsx to v0.5_Batch04.xlsx
├── 03_Policy_Annotation_&_QA/
│   ├── FDO-Privacy_Stage3B_Policy_Extraction_Batch01_Complete.xlsx
│   ├── FDO-Privacy_Stage3B_Policy_Registry_Batch01_v2.xlsx
│   ├── FDO-Privacy_Stage3C_QA_Remediation_v1.2.xlsx
│   ├── FDO-Privacy_Stage3D_Policy_Evidence_Completion_v1.1.xlsx
│   └── FDO-Privacy_Stage3D_v1.9_STAGE3_FREEZE_AND_STAGE4_READY.xlsx
├── 04_FDO_Analysis/
│   ├── FDO-Privacy_Stage4A_FDO_Necessity_Analysis_v1.1.xlsx
│   ├── FDO-Privacy_Stage4B_Purpose_Compatibility_v1.0.xlsx
│   ├── FDO-Privacy_Stage4C_FDO_Candidate_Screening_v1.0.xlsx
│   ├── FDO-Privacy_Stage4D_Detailed_Adjudication_v1.0.xlsx
│   └── FDO-Privacy_Stage4E_Ambiguous_Case_Resolution_v1.0.xlsx
├── 05_Final_Dataset/
│   ├── FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx
│   └── FDO-Privacy_Final_Stage3_Dataset_COMPLETE.xlsx
├── 06_Results_&_Visualization/
│   └── FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx
└── 07_Report_&_Deliverables/
    └── FDO-Privacy_Stage7_Final_Research_Report_Package_v1.0.docx
```

## 13. Final Project Artifact Map

```
[ DESIGN ]
   └── FDO-Privacy_Stage3A_Dataset_Schema_v1.0.xlsx
        ↓
[ EXPECTED DATA MODEL & PILOT ]
   ├── FDO-Privacy_Stage2B_Pilot_v0.2_VerifiedBatch01.xlsx to v0.5_Batch04.xlsx
   └── FDO-Privacy_Stage2B_Agreement_Analysis_v1.0.xlsx
        ↓
[ POLICY EVIDENCE & EXTRACTION ]
   ├── FDO-Privacy_Stage3B_Policy_Extraction_Batch01_Complete.xlsx
   └── FDO-Privacy_Stage3B_Policy_Registry_Batch01_v2.xlsx
        ↓
[ ANNOTATION & STAGE 3 FREEZE ]
   ├── FDO-Privacy_Stage3C_QA_Remediation_v1.2.xlsx
   ├── FDO-Privacy_Stage3D_v1.9_STAGE3_FREEZE_AND_STAGE4_READY.xlsx
   ├── FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx
   └── FDO-Privacy_Final_Stage3_Dataset_COMPLETE.xlsx
        ↓
[ FDO ANALYSIS & ADJUDICATION ]
   ├── FDO-Privacy_Stage4A_FDO_Necessity_Analysis_v1.1.xlsx
   ├── FDO-Privacy_Stage4B_Purpose_Compatibility_v1.0.xlsx
   ├── FDO-Privacy_Stage4C_FDO_Candidate_Screening_v1.0.xlsx
   ├── FDO-Privacy_Stage4D_Detailed_Adjudication_v1.0.xlsx
   └── FDO-Privacy_Stage4E_Ambiguous_Case_Resolution_v1.0.xlsx
        ↓
[ FINAL DATASET & VISUALIZATION ]
   └── FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx
        ↓
[ FINAL RESEARCH REPORT ]
   └── FDO-Privacy_Stage7_Final_Research_Report_Package_v1.0.docx
```
