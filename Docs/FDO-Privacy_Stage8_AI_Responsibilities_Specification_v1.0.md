# FDO-Privacy --- Stage 8 AI Responsibilities Specification

**Version:** 1.0\
**Stage:** 8.1I --- AI Responsibilities\
**Project:** FDO-Privacy

------------------------------------------------------------------------

## 1. Purpose

This document defines the role of Artificial Intelligence in the
FDO-Privacy prototype.

The central architectural principle is:

``` text
AI assists the analysis
        ↓
Structured evidence
        ↓
Research-defined rules
        ↓
Final FDO decision
```

The AI component must not replace the project's functional-data model or
the deterministic FDO decision logic.

------------------------------------------------------------------------

# 2. AI Role in the System

The AI/NLP layer is responsible primarily for tasks involving
unstructured privacy-policy language.

Its main responsibilities are:

1.  Policy text extraction assistance
2.  Data-type identification
3.  Purpose identification
4.  Entity/sharing/retention extraction where supported
5.  Terminology normalization assistance
6.  Evidence organization
7.  Uncertainty identification
8.  Explanation drafting

The final FDO classification remains under the project's explicit
reasoning rules.

------------------------------------------------------------------------

# 3. What AI CAN Do

## 3.1 Extract Policy Information

AI may identify candidate statements about:

``` text
Data Type
Purpose
Entity
Sharing
Retention
Evidence Text
Source Section
```

Example:

``` text
Policy:
"We collect your precise location to provide
location-based services."

AI extraction:

Data Type = LOCATION
Purpose = LOCATION_BASED_SERVICES
Evidence = source sentence
```

The source text must remain available.

------------------------------------------------------------------------

## 3.2 Identify Data-Type Mentions

AI may identify different expressions referring to a data category.

Example:

``` text
GPS information
Precise location
Geolocation
Location information
```

Candidate normalized category:

``` text
LOCATION
```

The normalization must be supported by the source wording.

------------------------------------------------------------------------

## 3.3 Identify Declared Purposes

AI may extract the purpose associated with a data practice.

Examples:

``` text
navigation
route calculation
fraud prevention
account security
personalization
advertising
analytics
```

The system must preserve the original purpose wording in addition to any
normalized representation.

------------------------------------------------------------------------

## 3.4 Identify Entities and Sharing Information

Where the policy provides sufficient evidence, AI may extract:

``` text
First party
Service provider
Third party
Advertising partner
Analytics provider
Other recipient
```

This information is evidence about the policy declaration and is not
itself an FDO determination.

------------------------------------------------------------------------

## 3.5 Identify Retention Statements

AI may identify retention information when explicitly stated.

Example:

``` text
"We retain account information while your account
remains active."
```

Possible extraction:

``` text
Retention:
While account remains active
```

If retention is not stated, the system must not invent a retention
period.

------------------------------------------------------------------------

## 3.6 Normalize Terminology

AI may assist in mapping equivalent policy expressions to the project's
controlled vocabulary.

The system should preserve:

``` text
Original term
Normalized term
Normalization note
```

Example:

``` text
Original:
"GPS information"

Normalized:
LOCATION
```

------------------------------------------------------------------------

## 3.7 Detect Uncertainty

AI should be able to indicate when an extraction is uncertain.

Example:

``` text
Candidate Data Type:
DEVICE INFORMATION

Confidence:
Low

Status:
REVIEW_REQUIRED
```

Uncertainty must be preserved rather than hidden.

------------------------------------------------------------------------

## 3.8 Draft Explanations

AI may generate a human-readable explanation from structured inputs that
have already been established.

Example:

``` text
Location is functionally related to the application's
navigation function, and the available policy evidence
provides a compatible navigation-related purpose.
```

The generated explanation must be traceable to the structured evidence.

------------------------------------------------------------------------

# 4. What AI CANNOT Do

## 4.1 AI Cannot Invent Evidence

The AI must never create a policy statement that does not exist in the
supplied source.

``` text
Source evidence
      ≠
AI-generated assumption
```

Only source-supported information may be stored as policy evidence.

------------------------------------------------------------------------

## 4.2 AI Cannot Invent a Purpose

If the policy says:

``` text
"to improve our services"
```

the AI must not convert this into:

``` text
"to calculate routes"
```

unless the source and application context actually support that
interpretation.

------------------------------------------------------------------------

## 4.3 AI Cannot Automatically Declare FDO

The AI must not make the final decision simply because it predicts that
a data practice looks excessive.

``` text
LLM prediction
      ≠
Final FDO result
```

The FDO Decision Engine applies the project's rules.

------------------------------------------------------------------------

## 4.4 AI Cannot Convert Missing Evidence into Negative Evidence

The following are different:

``` text
No evidence extracted
```

and:

``` text
Policy explicitly states the data is not collected
```

The first is not proof of the second.

Therefore:

``` text
Extraction failure
      ≠
NOT_DECLARED
```

------------------------------------------------------------------------

## 4.5 AI Cannot Force Binary Decisions

When the evidence is insufficient or contradictory, the system should
preserve uncertainty.

``` text
Uncertain evidence
      ↓
AMBIGUOUS / REVIEW
```

The AI should not force:

``` text
FDO
```

or:

``` text
NOT_FDO
```

just to complete the output.

------------------------------------------------------------------------

# 5. AI Confidence

AI confidence is an indication of extraction/model confidence.

It is not equivalent to factual truth.

Example:

``` json
{
  "data_type": "LOCATION",
  "confidence": 0.91
}
```

The value `0.91` means the model is confident in its extraction; it does
not prove that the policy statement is correct.

Source evidence remains the authority for what the policy actually
states.

------------------------------------------------------------------------

# 6. Evidence-First AI Output

AI extraction should produce structured records such as:

``` json
{
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
```

The exact field implementation will follow the Stage 8.1F input/output
specification.

------------------------------------------------------------------------

# 7. AI Validation Boundary

The prototype should use the following boundary:

``` text
                  POLICY
                    |
                    v
             AI EXTRACTION
                    |
                    v
           CANDIDATE EVIDENCE
                    |
                    v
       STRUCTURE / NORMALIZATION
                    |
                    v
        EVIDENCE VALIDATION
                    |
                    v
         ACCEPTED STRUCTURED
              EVIDENCE
                    |
                    v
           FDO RULE ENGINE
```

The AI therefore supports the evidence preparation stage.

------------------------------------------------------------------------

# 8. AI and Expected Data

The AI should not independently create the project's expected-data
baseline.

Expected data comes from the established functional-data model.

``` text
Application Function
        |
        v
Expected Data Model
        |
        v
Expected Mapping
```

AI may assist in interpreting application descriptions or policy
terminology, but the authoritative expected mapping remains the
research-defined model.

------------------------------------------------------------------------

# 9. AI and FDO Decision Logic

The final decision boundary is:

``` text
AI
 |
 | extracts / normalizes / assists
 v
Structured Evidence
 |
 v
Functional Comparison
 |
 v
FDO Decision Rules
 |
 +----> FDO
 +----> NOT_FDO
 +----> AMBIGUOUS
```

The AI does not bypass the decision engine.

------------------------------------------------------------------------

# 10. Hallucination Control

The prototype should reduce unsupported AI output through:

### 10.1 Source Evidence Requirement

Important extracted claims should retain source text.

### 10.2 Structured Output

The model should return predefined fields rather than unrestricted prose
wherever possible.

### 10.3 Controlled Vocabulary

Data types and other normalized concepts should use the project's
defined vocabulary.

### 10.4 Uncertainty State

Uncertain extraction should be explicitly marked.

### 10.5 Rule-Based Final Decision

The FDO result should be produced by the defined decision logic rather
than unrestricted model generation.

------------------------------------------------------------------------

# 11. Explanation Generation Rules

The AI may draft explanations only from structured analysis results.

An explanation should contain:

``` text
What data was analyzed
Relevant function
Expected requirement
Policy-supported purpose
Decision
Reason
Evidence reference
Limitations where applicable
```

The AI must not add facts that are absent from the analysis record.

------------------------------------------------------------------------

# 12. Ambiguity Handling

AI uncertainty can occur at several levels:

``` text
Data-type uncertainty
Purpose uncertainty
Entity uncertainty
Functional relationship uncertainty
Evidence uncertainty
```

When uncertainty materially affects the FDO decision:

``` text
AMBIGUOUS
```

should be available as the final classification.

This is preferable to unsupported certainty.

------------------------------------------------------------------------

# 13. Contradictory Policy Statements

If the AI identifies conflicting policy statements:

``` text
Statement A:
Data used for purpose X

Statement B:
Data used for purpose Y
```

the system should preserve both pieces of evidence.

It should not silently select one.

Possible result:

``` text
Evidence Status = CONFLICTING
Decision = AMBIGUOUS
```

unless another validated rule or evidence resolves the conflict.

------------------------------------------------------------------------

# 14. Human Review Boundary

The architecture should allow human review for cases such as:

``` text
Low extraction confidence
Conflicting evidence
Unclear purpose
Unclear data type
Unclear functional relationship
Unsupported normalization
```

Human review is especially important when automated evidence could
materially change the final classification.

------------------------------------------------------------------------

# 15. AI Audit Information

For reproducibility, the prototype should retain where practical:

``` text
Model/provider identifier
Model version
Extraction status
Confidence
Source evidence
Normalized result
Timestamp
Prompt/template version
```

This supports later evaluation and debugging.

------------------------------------------------------------------------

# 16. AI Failure Modes

The prototype should explicitly consider:

  -----------------------------------------------------------------------
  Failure mode            Risk                    Mitigation
  ----------------------- ----------------------- -----------------------
  Hallucinated evidence   False policy claim      Require source evidence

  Wrong data              Incorrect comparison    Preserve original term
  normalization                                   

  Purpose                 False justification     Keep original purpose
  over-interpretation                             

  Missing extraction      False negative          Preserve uncertainty

  Overconfident           Hidden errors           Confidence + review
  extraction                                      

  Conflicting statements  Incorrect choice        Preserve both

  FDO overprediction      False positives         Rule-based decision
                                                  engine

  FDO underprediction     False negatives         Benchmark evaluation

  Explanation invention   Misleading user         Generate only from
                                                  structured record
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 17. AI Output States

The extraction layer may use:

``` text
EXTRACTED
REVIEW_REQUIRED
SOURCE_INSUFFICIENT
```

These are extraction/evidence states.

They must not be confused with final FDO classifications:

``` text
FDO
NOT_FDO
AMBIGUOUS
```

------------------------------------------------------------------------

# 18. Separation of Responsibilities

## AI Layer

``` text
Read policy
Extract information
Normalize terminology
Identify uncertainty
Draft explanation
```

## Research Logic Layer

``` text
Expected data
Necessity
Functional relationship
Purpose compatibility
Functional justification
```

## Decision Layer

``` text
FDO
NOT_FDO
AMBIGUOUS
```

This three-layer separation is a core design requirement.

------------------------------------------------------------------------

# 19. Example End-to-End AI Interaction

### Policy

``` text
"We collect precise location information to
provide navigation and route services."
```

### AI extraction

``` text
Data Type:
LOCATION

Purpose:
NAVIGATION / ROUTE SERVICES

Evidence:
Original policy sentence

Status:
EXTRACTED
```

### Expected-data engine

``` text
Function:
Route Calculation

Expected:
LOCATION

Necessity:
L1_REQUIRED

Expected Purpose:
Route calculation
```

### Rule engine

``` text
Data relationship:
Supported

Purpose:
Compatible

Functional excess:
Not established

Result:
NOT_FDO
```

### AI explanation

``` text
Location is functionally related to route calculation,
and the policy states a navigation-related purpose.
```

The AI assists the process but does not determine the result
independently.

------------------------------------------------------------------------

# 20. Example of Correct Uncertainty

### Policy

``` text
"We may collect information about your device
to improve our services."
```

If the exact data type or functional purpose cannot be established:

``` text
Data Type:
UNCERTAIN

Purpose:
IMPROVE_SERVICES

Evidence:
Source sentence

Status:
REVIEW_REQUIRED
```

The final system may return:

``` text
AMBIGUOUS
```

if this uncertainty prevents a defensible FDO decision.

------------------------------------------------------------------------

# 21. AI Governance Principle

The prototype follows:

``` text
Evidence > Model assumption
Research rule > Model opinion
Traceability > Unexplained prediction
Explicit uncertainty > False certainty
```

------------------------------------------------------------------------

# 22. Stage 8.1I Completion Criteria

Stage 8.1I is complete when the project has formally defined:

-   [x] AI responsibilities
-   [x] Policy extraction role
-   [x] Data-type identification
-   [x] Purpose identification
-   [x] Entity/sharing/retention extraction
-   [x] Normalization assistance
-   [x] Uncertainty handling
-   [x] Confidence interpretation
-   [x] Evidence requirements
-   [x] Hallucination controls
-   [x] AI decision boundary
-   [x] Expected-data boundary
-   [x] FDO decision boundary
-   [x] Explanation rules
-   [x] Contradiction handling
-   [x] Human review boundary
-   [x] Audit information
-   [x] AI failure modes
-   [x] AI output states

**Status: COMPLETE**

------------------------------------------------------------------------

# 23. Next Stage

**Stage 8.1J --- API Requirements Specification**

The next step will formally define the backend API contracts, including:

``` text
POST /analyze
POST /extract-policy
GET /applications
GET /analysis/{analysis_id}
GET /analysis/{analysis_id}/report
```

For each endpoint we will specify:

-   request
-   response
-   validation
-   errors
-   status codes
-   relationship to the data model
