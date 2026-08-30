# FDO-Privacy --- Stage 8 API Requirements Specification

**Version:** 1.0\
**Stage:** 8.1J --- API Requirements\
**Project:** FDO-Privacy

------------------------------------------------------------------------

## 1. Purpose

This document defines the backend API contracts for the FDO-Privacy
prototype.

The API provides the communication layer between the frontend and the
analysis services.

The API must preserve the architecture defined in Stages 8.1D--8.1I:

``` text
Frontend
    |
    v
API
    |
    v
Backend Services
    |
    +--> Policy Processing
    +--> AI Extraction
    +--> Normalization
    +--> Expected Data
    +--> Functional Comparison
    +--> FDO Decision
    +--> Explanation
    |
    v
API Response
    |
    v
Frontend
```

------------------------------------------------------------------------

# 2. API Design Principles

The API should:

-   use structured JSON wherever practical
-   validate all incoming requests
-   return structured errors
-   preserve evidence and provenance
-   separate extraction from decision-making
-   expose `AMBIGUOUS` when evidence is insufficient
-   never silently overwrite benchmark data
-   return item-level explanations
-   keep AI-generated information distinguishable from source evidence

------------------------------------------------------------------------

# 3. Base API

Initial development base path:

``` text
/api/v1
```

Example:

``` text
POST /api/v1/analyze
```

The exact host and deployment URL are implementation details and are not
fixed at this architecture stage.

------------------------------------------------------------------------

# 4. Endpoint Inventory

  -----------------------------------------------------------------------------------------------------------
  Method                  Endpoint                                                    Purpose
  ----------------------- ----------------------------------------------------------- -----------------------
  POST                    `/api/v1/analyze`                                           Run complete FDO
                                                                                      analysis

  POST                    `/api/v1/extract-policy`                                    Extract structured
                                                                                      evidence from policy
                                                                                      text

  GET                     `/api/v1/applications`                                      List available
                                                                                      applications

  GET                     `/api/v1/applications/{application_id}`                     Retrieve an application

  GET                     `/api/v1/applications/{application_id}/expected-mappings`   Retrieve expected
                                                                                      mappings

  GET                     `/api/v1/analysis/{analysis_id}`                            Retrieve analysis
                                                                                      result

  GET                     `/api/v1/analysis/{analysis_id}/report`                     Retrieve report-ready
                                                                                      analysis

  GET                     `/api/v1/health`                                            Check backend
                                                                                      availability
  -----------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 5. POST `/api/v1/analyze`

## Purpose

Run the complete FDO-Privacy analysis pipeline.

## Request

``` json
{
  "application_name": "Example Navigation App",
  "category": "Navigation",
  "description": "Provides route planning and navigation",
  "policy_text": "Privacy policy text...",
  "policy_source": null
}
```

## Processing

``` text
Request
  ↓
Validation
  ↓
Application Context
  ↓
Policy Processing
  ↓
AI Extraction
  ↓
Normalization
  ↓
Expected Mapping Lookup
  ↓
Functional Comparison
  ↓
FDO Decision
  ↓
Explanation
  ↓
Response
```

## Success response

HTTP:

``` text
200 OK
```

Example:

``` json
{
  "analysis_id": "analysis_001",
  "application": {
    "application_id": "app_001",
    "application_name": "Example Navigation App"
  },
  "analysis_status": "COMPLETED",
  "summary": {
    "total_mappings": 10,
    "fdo": 1,
    "not_fdo": 7,
    "ambiguous": 2
  },
  "results": []
}
```

The numbers above are illustrative only.

## Partial response

If some mappings cannot be safely completed:

``` text
analysis_status = PARTIAL
```

The response should still expose completed results and identify
unresolved items.

------------------------------------------------------------------------

# 6. POST `/api/v1/extract-policy`

## Purpose

Run policy extraction without performing the complete FDO decision.

This endpoint is useful for testing and debugging the extraction layer.

## Request

``` json
{
  "policy_text": "Privacy policy text...",
  "application_name": "Example App"
}
```

## Response

``` json
{
  "extraction_status": "COMPLETED",
  "evidence": [
    {
      "evidence_id": "evidence_001",
      "data_type": "LOCATION",
      "purpose": "LOCATION_BASED_SERVICES",
      "entity": null,
      "sharing": null,
      "retention": null,
      "evidence_text": "We collect your precise location...",
      "source_section": "Location Information",
      "extraction_status": "EXTRACTED",
      "confidence": 0.91
    }
  ]
}
```

The confidence value is model/extraction confidence, not proof of
factual correctness.

------------------------------------------------------------------------

# 7. GET `/api/v1/applications`

## Purpose

Return applications available to the prototype.

## Response

HTTP:

``` text
200 OK
```

Example:

``` json
{
  "applications": [
    {
      "application_id": "app_001",
      "application_name": "Example App",
      "category": "Navigation"
    }
  ]
}
```

------------------------------------------------------------------------

# 8. GET `/api/v1/applications/{application_id}`

## Purpose

Return one application's information and functional context.

## Response

``` json
{
  "application_id": "app_001",
  "application_name": "Example Navigation App",
  "category": "Navigation",
  "description": "Provides route planning and navigation",
  "functions": [
    {
      "function_id": "func_001",
      "function_name": "Route Calculation",
      "feature": "Route Planning"
    }
  ]
}
```

------------------------------------------------------------------------

# 9. GET `/api/v1/applications/{application_id}/expected-mappings`

## Purpose

Return the expected-data baseline for an application.

## Response

``` json
{
  "application_id": "app_001",
  "expected_mappings": [
    {
      "expected_id": "exp_001",
      "function_id": "func_001",
      "data_type": "LOCATION",
      "necessity": "L1_REQUIRED",
      "expected_purpose": "Route calculation"
    }
  ]
}
```

The expected mapping must come from the project's established
expected-data model.

------------------------------------------------------------------------

# 10. GET `/api/v1/analysis/{analysis_id}`

## Purpose

Retrieve a previously completed analysis.

## Response

``` json
{
  "analysis_id": "analysis_001",
  "application": {},
  "analysis_status": "COMPLETED",
  "summary": {},
  "results": []
}
```

The response should preserve the item-level analysis information.

------------------------------------------------------------------------

# 11. GET `/api/v1/analysis/{analysis_id}/report`

## Purpose

Return a report-ready representation of the analysis.

The report response should include:

``` text
Application
Function
Expected Data
Declared Data
Necessity
Expected Purpose
Declared Purpose
Purpose Compatibility
Functional Justification
FDO Classification
Evidence
Explanation
```

Example:

``` json
{
  "analysis_id": "analysis_001",
  "report": {
    "application": "Example Navigation App",
    "items": [
      {
        "data_type": "LOCATION",
        "fdo_status": "NOT_FDO",
        "explanation": "Location is functionally related to route calculation."
      }
    ]
  }
}
```

------------------------------------------------------------------------

# 12. GET `/api/v1/health`

## Purpose

Verify that the backend service is available.

## Response

``` json
{
  "status": "ok",
  "service": "fdo-privacy-backend"
}
```

HTTP:

``` text
200 OK
```

------------------------------------------------------------------------

# 13. Error Response Format

All API errors should use a consistent structure.

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

# 14. HTTP Status Codes

The initial API should use:

  Status   Meaning
  -------- ------------------------------------------------
  200      Successful request
  201      Resource successfully created, when applicable
  400      Invalid request
  404      Resource not found
  422      Validation error
  500      Unexpected server error
  503      Service temporarily unavailable

A domain-level result such as `AMBIGUOUS` is **not** an HTTP error.

------------------------------------------------------------------------

# 15. Validation Rules

## Analysis request

Required:

``` text
application_name
category
policy_text
```

Recommended:

``` text
description
```

## Policy text

Must not be empty.

## Application ID

Must refer to an existing application when an existing application is
requested.

## Analysis ID

Must refer to an existing analysis for retrieval endpoints.

------------------------------------------------------------------------

# 16. FDO Result Contract

Every item-level result returned by the API should expose:

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
  "explanation": "Location is functionally related to route calculation."
}
```

The final status must be one of:

``` text
FDO
NOT_FDO
AMBIGUOUS
```

------------------------------------------------------------------------

# 17. API and AI Boundary

The API must not expose an architecture in which the frontend sends:

``` text
"Is this FDO?"
```

directly to an unrestricted LLM and accepts the answer.

Instead:

``` text
Frontend
   ↓
Backend API
   ↓
Structured Evidence
   ↓
Comparison
   ↓
FDO Rules
   ↓
Final Result
```

AI remains an internal supporting service.

------------------------------------------------------------------------

# 18. API and Evidence Provenance

Where policy evidence is returned, the API should preserve:

``` text
evidence_id
source policy
source section
source location
evidence text
extraction status
confidence
```

This allows the frontend to display or retrieve supporting evidence.

------------------------------------------------------------------------

# 19. API and Benchmark Separation

The live API must not modify the research benchmark.

The benchmark should be accessed only through a controlled evaluation
workflow.

Conceptually:

``` text
Research Benchmark
       |
       | read-only
       v
Evaluation Module
       |
       +---- Prototype API
       |
       v
Comparison Metrics
```

------------------------------------------------------------------------

# 20. Security Requirements

The API should eventually include:

-   input validation
-   upload/type validation
-   request size limits
-   safe document processing
-   error sanitization
-   logging without unnecessary sensitive policy content
-   access control when deployed beyond local development

These are implementation requirements and may be expanded during backend
development.

------------------------------------------------------------------------

# 21. API Versioning

The initial API uses:

``` text
/api/v1
```

Breaking changes should use a new version rather than silently changing
an existing contract.

Example:

``` text
/api/v2
```

------------------------------------------------------------------------

# 22. Frontend Integration

The frontend will primarily use:

``` text
POST /api/v1/analyze
```

for the main workflow.

It can use:

``` text
GET /api/v1/analysis/{analysis_id}
```

to retrieve results and:

``` text
GET /api/v1/analysis/{analysis_id}/report
```

to retrieve the report-ready representation.

------------------------------------------------------------------------

# 23. Example Main Workflow

``` text
User opens application
        |
        v
Frontend collects policy
        |
        v
POST /api/v1/analyze
        |
        v
Backend validates request
        |
        v
Analysis pipeline executes
        |
        v
FDO result generated
        |
        v
JSON response
        |
        v
Frontend renders:
    - data item
    - expected requirement
    - policy evidence
    - FDO status
    - explanation
```

------------------------------------------------------------------------

# 24. API Non-Goals

The API should not:

-   make the LLM the final FDO authority
-   hide uncertainty
-   treat missing evidence as proof of non-collection
-   overwrite the benchmark
-   return unsupported claims as verified evidence
-   reduce every analysis to a single opaque privacy score

------------------------------------------------------------------------

# 25. Stage 8.1J Completion Criteria

Stage 8.1J is complete when the project has defined:

-   [x] API base path
-   [x] Main analysis endpoint
-   [x] Policy extraction endpoint
-   [x] Application endpoints
-   [x] Expected-mapping endpoint
-   [x] Analysis retrieval endpoint
-   [x] Report endpoint
-   [x] Health endpoint
-   [x] Request schemas
-   [x] Response schemas
-   [x] Error schema
-   [x] HTTP status codes
-   [x] Validation requirements
-   [x] FDO result contract
-   [x] AI/API boundary
-   [x] Evidence provenance requirements
-   [x] Benchmark separation
-   [x] Initial security requirements
-   [x] API versioning

**Status: COMPLETE**

------------------------------------------------------------------------

# 26. Next Stage

**Stage 8.1K --- Master Architecture Document**

The next step will consolidate the completed Stage 8.1 design artifacts
into one master technical architecture document covering:

``` text
Project Structure
System Components
Data Flow
Input/Output Contracts
Data Model
FDO Decision Logic
AI Responsibilities
API Requirements
Technology Direction
Validation Strategy
```

After 8.1K is completed, Stage 8.1L will perform the final verification
gate.
