# FDO-Privacy --- Stage 8 Data Model Specification

**Version:** 1.0\
**Stage:** 8.1G --- Data Model\
**Project:** FDO-Privacy

------------------------------------------------------------------------

## 1. Purpose

This document defines the logical data model for the FDO-Privacy
prototype.

It converts the objects defined in Stage 8.1F into persistent entities
and relationships that can later be implemented in SQLite or another
relational database.

The model is designed to preserve:

-   application/function context
-   expected-data mappings
-   policy documents
-   policy evidence
-   normalized evidence
-   comparison results
-   FDO decisions
-   explanations
-   provenance
-   benchmark separation

------------------------------------------------------------------------

# 2. High-Level Entity Relationship

``` text
APPLICATION
    |
    +------< FUNCTION
    |           |
    |           +------< EXPECTED_MAPPING
    |
    +------< POLICY_DOCUMENT
                    |
                    +------< POLICY_EVIDENCE
                                      |
                                      +------< NORMALIZED_EVIDENCE

EXPECTED_MAPPING
        |
        +------< COMPARISON >------ POLICY_EVIDENCE
                    |
                    v
                FDO_RESULT
                    |
                    v
               EXPLANATION

ANALYSIS
    |
    +------< COMPARISON
```

`<` indicates a one-to-many relationship.

------------------------------------------------------------------------

# 3. Core Entities

The initial database should contain these core entities:

1.  `applications`
2.  `functions`
3.  `expected_mappings`
4.  `policy_documents`
5.  `policy_evidence`
6.  `normalized_evidence`
7.  `analyses`
8.  `comparisons`
9.  `fdo_results`
10. `explanations`

Optional benchmark tables can be added later without mixing benchmark
records with live prototype analyses.

------------------------------------------------------------------------

# 4. Applications

## Table: `applications`

Stores the application being analyzed.

  Field              Type        Key   Required   Description
  ------------------ ----------- ----- ---------- -------------------------------
  application_id     TEXT        PK    Yes        Unique application identifier
  application_name   TEXT              Yes        Application name
  category           TEXT              Yes        Application category
  description        TEXT              No         Functional description
  created_at         TIMESTAMP         Yes        Record creation time
  updated_at         TIMESTAMP         Yes        Last update time

### Example

``` text
application_id = app_001
application_name = Example Navigation App
category = Navigation
```

------------------------------------------------------------------------

# 5. Functions

## Table: `functions`

Stores functions/features associated with an application.

  Field            Type   Key   Required   Description
  ---------------- ------ ----- ---------- ----------------------------------
  function_id      TEXT   PK    Yes        Unique function identifier
  application_id   TEXT   FK    Yes        Parent application
  function_name    TEXT         Yes        Function name
  feature          TEXT         No         Feature associated with function
  description      TEXT         No         Additional functional context

### Relationship

``` text
applications.application_id
        |
        +----< functions.application_id
```

One application can have many functions.

------------------------------------------------------------------------

# 6. Expected Mappings

## Table: `expected_mappings`

Stores the function-specific expected-data baseline.

  Field              Type   Key   Required   Description
  ------------------ ------ ----- ---------- -----------------------------
  expected_id        TEXT   PK    Yes        Unique expected mapping
  application_id     TEXT   FK    Yes        Application
  function_id        TEXT   FK    Yes        Function
  data_type          TEXT         Yes        Expected data type
  necessity          TEXT         Yes        Existing necessity category
  expected_purpose   TEXT         Yes        Expected purpose
  source_version     TEXT         No         Dataset/model version

### Relationship

``` text
FUNCTION
   |
   +----< EXPECTED_MAPPING
```

The prototype must preserve compatibility with the existing Stage-2
expected-data model.

------------------------------------------------------------------------

# 7. Policy Documents

## Table: `policy_documents`

Stores the source policy supplied for analysis.

  Field               Type        Key   Required   Description
  ------------------- ----------- ----- ---------- --------------------------------
  policy_id           TEXT        PK    Yes        Unique policy identifier
  application_id      TEXT        FK    Yes        Associated application
  source_type         TEXT              Yes        PDF, TXT, pasted text, etc.
  source_identifier   TEXT              No         URL or source identifier
  document_name       TEXT              No         Original filename/title
  raw_text            TEXT              Yes        Extracted/original policy text
  retrieved_at        TIMESTAMP         No         Retrieval timestamp
  created_at          TIMESTAMP         Yes        Record creation time

### Important rule

The original policy text should be preserved where possible.

------------------------------------------------------------------------

# 8. Policy Evidence

## Table: `policy_evidence`

Stores evidence extracted from the policy.

  Field               Type   Key   Required   Description
  ------------------- ------ ----- ---------- -----------------------------
  evidence_id         TEXT   PK    Yes        Unique evidence record
  policy_id           TEXT   FK    Yes        Source policy
  data_type           TEXT         Yes        Extracted data type
  purpose             TEXT         No         Declared purpose
  entity              TEXT         No         Processing entity
  sharing             TEXT         No         Sharing information
  retention           TEXT         No         Retention information
  raw_term            TEXT         No         Original policy wording
  evidence_text       TEXT         Yes        Source evidence
  source_section      TEXT         No         Policy section
  source_location     TEXT         No         Page/paragraph/location
  extraction_status   TEXT         Yes        Extraction state
  confidence          REAL         No         Model/extraction confidence

### Provenance

Every evidence record belongs to a source policy.

``` text
POLICY_DOCUMENT
       |
       +----< POLICY_EVIDENCE
```

------------------------------------------------------------------------

# 9. Normalized Evidence

## Table: `normalized_evidence`

Stores the normalized representation without replacing the original
evidence.

  Field                  Type   Key   Required   Description
  ---------------------- ------ ----- ---------- ------------------------------
  normalized_id          TEXT   PK    Yes        Unique normalized record
  evidence_id            TEXT   FK    Yes        Original evidence
  normalized_data_type   TEXT         Yes        Controlled data type
  normalized_purpose     TEXT         No         Controlled purpose
  original_data_type     TEXT         No         Extracted/original value
  original_purpose       TEXT         No         Extracted/original purpose
  normalization_note     TEXT         No         Explanation of normalization

### Important rule

Normalization does not overwrite source evidence.

``` text
Original Evidence
       |
       +----> Normalized Representation
```

------------------------------------------------------------------------

# 10. Analyses

## Table: `analyses`

Represents one prototype analysis session.

  ---------------------------------------------------------------------------------
  Field             Type           Key            Required       Description
  ----------------- -------------- -------------- -------------- ------------------
  analysis_id       TEXT           PK             Yes            Unique analysis
                                                                 identifier

  application_id    TEXT           FK             Yes            Application
                                                                 analyzed

  policy_id         TEXT           FK             Yes            Policy analyzed

  analysis_status   TEXT                          Yes            COMPLETED,
                                                                 PARTIAL,
                                                                 REVIEW_REQUIRED,
                                                                 FAILED

  started_at        TIMESTAMP                     Yes            Start time

  completed_at      TIMESTAMP                     No             Completion time

  system_version    TEXT                          Yes            Prototype version
  ---------------------------------------------------------------------------------

### Relationship

``` text
APPLICATION
     |
     +----< ANALYSIS >---- POLICY_DOCUMENT
```

------------------------------------------------------------------------

# 11. Comparisons

## Table: `comparisons`

Stores the structured comparison before final FDO classification.

  Field                      Type   Key   Required   Description
  -------------------------- ------ ----- ---------- ----------------------------
  comparison_id              TEXT   PK    Yes        Unique comparison
  analysis_id                TEXT   FK    Yes        Analysis session
  expected_id                TEXT   FK    Yes        Expected mapping
  evidence_id                TEXT   FK    No         Supporting policy evidence
  data_match                 TEXT   Yes   Yes        MATCH, NO_MATCH, UNCERTAIN
  purpose_compatibility      TEXT         Yes        Compatibility result
  functional_relationship    TEXT         Yes        Functional relationship
  necessity_assessment       TEXT         Yes        Necessity result
  functional_justification   TEXT         Yes        Justification result
  evidence_sufficiency       TEXT         Yes        Sufficiency state

### Relationship

``` text
ANALYSIS
   |
   +----< COMPARISON >---- EXPECTED_MAPPING
               |
               +---------- POLICY_EVIDENCE
```

------------------------------------------------------------------------

# 12. FDO Results

## Table: `fdo_results`

Stores the final classification for a comparison.

  ----------------------------------------------------------------------------------------------
  Field                             Type           Key            Required       Description
  --------------------------------- -------------- -------------- -------------- ---------------
  result_id                         TEXT           PK             Yes            Unique result

  comparison_id                     TEXT           FK             Yes            Comparison

  application_id                    TEXT           FK             Yes            Application

  data_type                         TEXT                          Yes            Data item

  necessity_result                  TEXT                          Yes            Necessity
                                                                                 result

  purpose_result                    TEXT                          Yes            Purpose result

  functional_justification_result   TEXT                          Yes            Functional
                                                                                 justification

  evidence_status                   TEXT                          Yes            Evidence state

  classification                    TEXT                          Yes            FDO, NOT_FDO,
                                                                                 AMBIGUOUS

  created_at                        TIMESTAMP                     Yes            Result creation
                                                                                 time
  ----------------------------------------------------------------------------------------------

### Classification constraint

``` text
FDO
NOT_FDO
AMBIGUOUS
```

No other final FDO classification should be silently introduced.

------------------------------------------------------------------------

# 13. Explanations

## Table: `explanations`

Stores the human-readable explanation associated with a result.

  Field                 Type   Key   Required   Description
  --------------------- ------ ----- ---------- --------------------------------
  explanation_id        TEXT   PK    Yes        Unique explanation
  result_id             TEXT   FK    Yes        FDO result
  summary               TEXT   Yes   Yes        Short explanation
  reasoning_points      TEXT         No         Structured/list representation
  evidence_references   TEXT         No         Evidence IDs
  limitations           TEXT         No         Known limitations

### Relationship

``` text
FDO_RESULT
    |
    +----< EXPLANATION
```

------------------------------------------------------------------------

# 14. Complete Relationship Map

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
                 │
                 └── POLICY_EVIDENCE
                         |
                         v
                    FDO_RESULT
                         |
                         v
                    EXPLANATION
```

------------------------------------------------------------------------

# 15. Primary and Foreign Key Rules

The prototype should enforce these relationships:

``` text
functions.application_id
    → applications.application_id

expected_mappings.application_id
    → applications.application_id

expected_mappings.function_id
    → functions.function_id

policy_documents.application_id
    → applications.application_id

policy_evidence.policy_id
    → policy_documents.policy_id

normalized_evidence.evidence_id
    → policy_evidence.evidence_id

analyses.application_id
    → applications.application_id

analyses.policy_id
    → policy_documents.policy_id

comparisons.analysis_id
    → analyses.analysis_id

comparisons.expected_id
    → expected_mappings.expected_id

comparisons.evidence_id
    → policy_evidence.evidence_id

fdo_results.comparison_id
    → comparisons.comparison_id

fdo_results.application_id
    → applications.application_id

explanations.result_id
    → fdo_results.result_id
```

------------------------------------------------------------------------

# 16. Indexing Strategy

At minimum, indexes should later be created for:

``` text
applications.application_name
functions.application_id
expected_mappings.application_id
expected_mappings.function_id
policy_documents.application_id
policy_evidence.policy_id
policy_evidence.data_type
normalized_evidence.evidence_id
analyses.application_id
comparisons.analysis_id
comparisons.expected_id
fdo_results.application_id
fdo_results.classification
explanations.result_id
```

These support common lookups without prematurely optimizing the
prototype.

------------------------------------------------------------------------

# 17. Benchmark Separation

The existing manually adjudicated research benchmark must not be mixed
with live prototype results.

Conceptually:

``` text
RESEARCH BENCHMARK
        |
        | read-only reference
        v
PROTOTYPE
        |
        v
PREDICTIONS
        |
        v
EVALUATION
```

If benchmark tables are added later, they should have an explicit
namespace or table prefix such as:

``` text
benchmark_applications
benchmark_mappings
benchmark_results
```

or equivalent separation.

The prototype must never silently overwrite benchmark records.

------------------------------------------------------------------------

# 18. Data Integrity Rules

The database should enforce:

1.  Every expected mapping belongs to an application and function.
2.  Every policy evidence record belongs to a policy document.
3.  Normalized evidence must reference original evidence.
4.  Every comparison belongs to an analysis.
5.  A comparison references an expected mapping.
6.  A comparison may reference supporting evidence when available.
7.  Every FDO result belongs to a comparison.
8.  Every explanation belongs to a result.
9.  Final classification is controlled.
10. Source evidence is preserved separately from generated explanations.

------------------------------------------------------------------------

# 19. Recommended Initial Database

For the first prototype:

``` text
SQLite
```

Reason:

-   lightweight
-   local
-   easy to develop
-   no separate database server required
-   sufficient for the first prototype

A larger database such as PostgreSQL can be introduced later if
deployment or scale requires it.

------------------------------------------------------------------------

# 20. Stage 8.1G Completion Criteria

Stage 8.1G is complete when the project has defined:

-   [x] Core entities
-   [x] Entity relationships
-   [x] Primary keys
-   [x] Foreign keys
-   [x] Core fields
-   [x] Classification constraints
-   [x] Provenance relationships
-   [x] Indexing strategy
-   [x] Benchmark separation
-   [x] Data integrity rules
-   [x] Initial database direction

**Status: COMPLETE**

------------------------------------------------------------------------

# 21. Next Stage

**Stage 8.1H --- FDO Decision Logic Specification**

The next step will formally define the deterministic decision logic used
by the prototype to convert:

``` text
Expected Mapping
+
Policy Evidence
+
Necessity
+
Purpose Compatibility
+
Functional Justification
+
Evidence Sufficiency
```

into:

``` text
FDO
NOT_FDO
AMBIGUOUS
```

No backend code will be written until that logic is formally specified.
