# FDO-Privacy --- Stage 8 Input / Output Specification

**Version:** 1.0\
**Stage:** 8.1F --- Input / Output Specification\
**Project:** FDO-Privacy

------------------------------------------------------------------------

## 1. Purpose

This document defines the structured inputs and outputs exchanged by the
FDO-Privacy prototype.

These schemas are implementation contracts. They will later guide the
backend data models, API request/response objects, frontend types, and
validation logic.

The schemas preserve the project's evidence-first approach and
explicitly separate policy evidence from final FDO decisions.

------------------------------------------------------------------------

## 2. Core Data Flow

``` text
AnalysisRequest
      |
      v
ApplicationContext
      |
      +--------------------+
      |                    |
      v                    v
PolicyEvidence       ExpectedMapping
      |                    |
      +---------+----------+
                |
                v
       ComparisonResult
                |
                v
           FDOResult
                |
                v
           Explanation
                |
                v
        AnalysisResponse
```

------------------------------------------------------------------------

# 3. Analysis Request

## Purpose

Represents the request submitted by the user.

### Schema

``` json
{
  "application_name": "string",
  "category": "string",
  "description": "string",
  "policy_text": "string",
  "policy_source": "string|null"
}
```

### Required fields

  Field              Type               Required Description
  ------------------ ------------- ------------- ------------------------------------
  application_name   string                  Yes Name of application being analyzed
  category           string                  Yes Application category
  description        string          Recommended Functional description
  policy_text        string                  Yes Policy text supplied for analysis
  policy_source      string/null              No Source URL or source identifier

------------------------------------------------------------------------

# 4. Application Context

## Purpose

Represents the functional context used during analysis.

### Schema

``` json
{
  "application_id": "string",
  "application_name": "string",
  "category": "string",
  "description": "string",
  "functions": [
    {
      "function_id": "string",
      "function_name": "string",
      "feature": "string|null"
    }
  ]
}
```

### Function object

  Field           Type          Description
  --------------- ------------- -----------------------------------
  function_id     string        Internal function identifier
  function_name   string        Function performed by application
  feature         string/null   Specific feature when available

------------------------------------------------------------------------

# 5. Policy Evidence

## Purpose

Represents information extracted from the privacy policy.

### Schema

``` json
{
  "evidence_id": "string",
  "application_id": "string",
  "data_type": "string",
  "purpose": "string|null",
  "entity": "string|null",
  "sharing": "string|null",
  "retention": "string|null",
  "raw_term": "string|null",
  "evidence_text": "string",
  "source_section": "string|null",
  "source_location": "string|null",
  "extraction_status": "string",
  "confidence": 0.0
}
```

### Important distinction

`evidence_text` is the source-supported policy evidence.

`confidence` represents extraction/model confidence and must not be
treated as proof of correctness.

### Extraction status

Possible states may include:

``` text
EXTRACTED
REVIEW_REQUIRED
SOURCE_INSUFFICIENT
```

The exact status vocabulary must remain consistent with the
implementation and research dataset.

------------------------------------------------------------------------

# 6. Normalized Policy Evidence

## Purpose

Represents policy evidence after controlled normalization.

### Schema

``` json
{
  "evidence_id": "string",
  "normalized_data_type": "string",
  "normalized_purpose": "string|null",
  "original_data_type": "string|null",
  "original_purpose": "string|null",
  "normalization_note": "string|null",
  "evidence_text": "string"
}
```

### Rule

Normalization may standardize terminology but must not introduce
unsupported meaning.

Example:

``` text
"GPS information"
"precise location"
"geolocation"
```

may normalize to:

``` text
LOCATION
```

when supported by the source text.

------------------------------------------------------------------------

# 7. Expected Mapping

## Purpose

Represents the expected-data baseline for an application function.

### Schema

``` json
{
  "expected_id": "string",
  "application_id": "string",
  "function_id": "string",
  "function": "string",
  "data_type": "string",
  "necessity": "string",
  "expected_purpose": "string"
}
```

### Necessity

The implementation should use the project's established necessity
vocabulary rather than inventing a new scale.

The existing project model uses graded necessity concepts such as:

``` text
L1_REQUIRED
L2_SUPPORTIVE
L3_OPTIONAL
L4_SECONDARY
L5_NO_PLAUSIBLE_LINK
```

The exact labels must remain aligned with the frozen research dataset.

------------------------------------------------------------------------

# 8. Comparison Result

## Purpose

Represents the structured comparison before the final FDO
classification.

### Schema

``` json
{
  "expected_id": "string",
  "evidence_id": "string|null",
  "data_match": "string",
  "purpose_compatibility": "string",
  "functional_relationship": "string",
  "necessity_assessment": "string",
  "functional_justification": "string",
  "evidence_sufficiency": "string"
}
```

### Suggested controlled values

`data_match`:

``` text
MATCH
NO_MATCH
UNCERTAIN
```

`purpose_compatibility`:

``` text
COMPATIBLE
INCOMPATIBLE
UNCERTAIN
NOT_ESTABLISHED
```

`functional_relationship`:

``` text
SUPPORTED
NOT_SUPPORTED
UNCERTAIN
```

`evidence_sufficiency`:

``` text
SUFFICIENT
INSUFFICIENT
UNCERTAIN
```

The implementation must not force an uncertain source into a binary
value.

------------------------------------------------------------------------

# 9. FDO Result

## Purpose

Represents the final item-level classification.

### Schema

``` json
{
  "result_id": "string",
  "expected_id": "string",
  "application_id": "string",
  "data_type": "string",
  "classification": "NOT_FDO",
  "necessity_result": "string",
  "purpose_result": "string",
  "functional_justification_result": "string",
  "evidence_status": "string"
}
```

### Classification

The primary prototype classification vocabulary is:

``` text
FDO
NOT_FDO
AMBIGUOUS
```

### Rules

``` text
Insufficient evidence
        ↓
AMBIGUOUS

Supported functional relationship
+
compatible purpose
+
no established functional excess
        ↓
NOT_FDO

Evidence establishes functional excess
or purpose incompatibility under the
project's adopted rules
        ↓
FDO
```

These are conceptual decision paths. The final deterministic rule
implementation must be specified separately in Stage 8.1H.

------------------------------------------------------------------------

# 10. Explanation

## Purpose

Provides a human-readable explanation for the result.

### Schema

``` json
{
  "explanation_id": "string",
  "result_id": "string",
  "summary": "string",
  "reasoning_points": [
    "string"
  ],
  "evidence_references": [
    "string"
  ],
  "limitations": [
    "string"
  ]
}
```

### Example

``` json
{
  "summary": "Location is functionally related to navigation.",
  "reasoning_points": [
    "Location is expected for route calculation.",
    "The policy provides a navigation-related purpose."
  ],
  "evidence_references": [
    "evidence_001"
  ],
  "limitations": []
}
```

------------------------------------------------------------------------

# 11. Complete Analysis Response

## Purpose

Represents the complete response returned by the backend to the
frontend.

### Schema

``` json
{
  "analysis_id": "string",
  "application": {},
  "policy_status": "string",
  "results": [],
  "summary": {
    "total_mappings": 0,
    "fdo": 0,
    "not_fdo": 0,
    "ambiguous": 0
  },
  "analysis_status": "string"
}
```

### Analysis status

Suggested values:

``` text
COMPLETED
PARTIAL
REVIEW_REQUIRED
FAILED
```

`PARTIAL` or `REVIEW_REQUIRED` should be used when the system cannot
safely complete all mappings.

------------------------------------------------------------------------

# 12. Evidence Provenance Object

For auditable results, an evidence reference should be traceable.

### Schema

``` json
{
  "evidence_id": "string",
  "source_type": "string",
  "source_identifier": "string|null",
  "source_section": "string|null",
  "evidence_text": "string",
  "retrieved_at": "string|null"
}
```

The system should preserve the source location whenever available.

------------------------------------------------------------------------

# 13. Error Response

Invalid requests should produce structured errors.

### Schema

``` json
{
  "error": {
    "code": "string",
    "message": "string",
    "field": "string|null"
  }
}
```

### Example

``` json
{
  "error": {
    "code": "POLICY_EMPTY",
    "message": "Privacy policy text is required.",
    "field": "policy_text"
  }
}
```

------------------------------------------------------------------------

# 14. Frontend Result Type

The frontend should receive a simplified item-level object suitable for
rendering.

``` json
{
  "data_type": "LOCATION",
  "expected_necessity": "L1_REQUIRED",
  "expected_purpose": "Route calculation",
  "declared_purpose": "Location-based services",
  "purpose_compatibility": "COMPATIBLE",
  "fdo_status": "NOT_FDO",
  "explanation": "Location has an identifiable relationship to the navigation function.",
  "evidence_available": true
}
```

------------------------------------------------------------------------

# 15. Database-Level Core Entities

The initial implementation should be able to represent at least these
entities:

``` text
Application
Function
ExpectedMapping
PolicyDocument
PolicyEvidence
NormalizedEvidence
Comparison
FDOResult
Explanation
Analysis
```

The exact relational schema will be finalized during the backend design
stage.

------------------------------------------------------------------------

# 16. Input / Output Validation Rules

## Application

-   name must not be empty
-   category should be provided
-   description should be available when required for function
    identification

## Policy

-   policy input must not be empty
-   unsupported formats should be rejected or converted before analysis
-   original evidence should be retained

## Evidence

-   evidence text should be linked to a source where possible
-   extracted evidence must be distinguishable from generated text

## FDO Result

-   classification must be one of the controlled result states
-   an ambiguous case must not be silently converted to FDO or NOT_FDO

## Explanation

-   must reference the underlying structured analysis
-   must not invent unsupported evidence

------------------------------------------------------------------------

# 17. Separation of Data Types

The system should keep these concepts separate:

``` text
Policy Evidence
       ≠
Expected Mapping
       ≠
Comparison Result
       ≠
FDO Result
       ≠
Explanation
```

This separation allows every final decision to be traced back to the
underlying evidence and expected-data baseline.

------------------------------------------------------------------------

# 18. Benchmark Compatibility

The prototype's result schema must be capable of representing the
existing research benchmark.

The current benchmark contains:

``` text
Expected mappings: 99
Evidence-backed mappings: 93
NOT_FDO: 60
AMBIGUOUS: 33
FDO established: 0
```

These values are benchmark results, not default values for every future
analysis.

The prototype must generate its own predictions and later be evaluated
against the benchmark.

------------------------------------------------------------------------

# 19. Example Complete Object

``` json
{
  "analysis_id": "analysis_001",
  "application": {
    "application_id": "app_001",
    "application_name": "Example Navigation App",
    "category": "Navigation"
  },
  "result": {
    "expected_id": "exp_001",
    "data_type": "LOCATION",
    "expected_necessity": "L1_REQUIRED",
    "expected_purpose": "Route calculation",
    "declared_purpose": "Location-based services",
    "purpose_compatibility": "COMPATIBLE",
    "functional_justification": "SUPPORTED",
    "fdo_status": "NOT_FDO"
  },
  "explanation": {
    "summary": "Location is functionally related to route calculation.",
    "evidence_references": [
      "evidence_001"
    ]
  }
}
```

------------------------------------------------------------------------

# 20. Stage 8.1F Completion Criteria

Stage 8.1F is complete when the project has formally defined:

-   [x] Analysis request
-   [x] Application context
-   [x] Policy evidence
-   [x] Normalized evidence
-   [x] Expected mapping
-   [x] Comparison result
-   [x] FDO result
-   [x] Explanation
-   [x] Complete analysis response
-   [x] Evidence provenance
-   [x] Error response
-   [x] Frontend result type
-   [x] Core database entities
-   [x] Validation rules
-   [x] Benchmark compatibility

**Status: COMPLETE**

------------------------------------------------------------------------

# 21. Next Stage

**Stage 8.1G --- Data Model Specification**

The next step will convert these logical objects into the actual
persistent data model, including:

-   entity relationships
-   primary keys
-   foreign keys
-   database tables
-   field types
-   indexes
-   provenance relationships
-   benchmark separation

This will prepare the project for backend implementation without mixing
implementation code into the architecture stage.
