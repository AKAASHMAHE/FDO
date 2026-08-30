# FDO-Privacy --- Stage 8 Data Flow Specification

**Version:** 1.0\
**Stage:** 8.1E --- Complete Data Flow\
**Project:** FDO-Privacy

------------------------------------------------------------------------

## 1. Purpose

This document defines how information moves through the FDO-Privacy
prototype.

The purpose is to establish a precise flow from user input through
policy processing, AI-assisted extraction, expected-data lookup,
functional comparison, FDO decision-making, explanation generation, and
final presentation.

This specification is a design artifact. It does not modify or replace
the Stage 1--7 research benchmark.

------------------------------------------------------------------------

## 2. Complete System Flow

``` text
USER
  |
  | Application information + Privacy Policy
  v
INPUT VALIDATION
  |
  v
APPLICATION / FUNCTION CONTEXT
  |
  +-----------------------------+
  |                             |
  v                             v
PRIVACY POLICY PROCESSOR     EXPECTED DATA ENGINE
  |                             |
  v                             |
CLEAN POLICY TEXT               |
  |                             |
  v                             |
AI POLICY EXTRACTION            |
  |                             |
  v                             |
NORMALIZED POLICY EVIDENCE      |
  |                             |
  +-------------+---------------+
                |
                v
       FUNCTIONAL COMPARISON
                |
                v
          NECESSITY TEST
                |
                v
       PURPOSE COMPATIBILITY
                |
                v
   FUNCTIONAL JUSTIFICATION
                |
                v
         FDO DECISION ENGINE
                |
        +-------+-------+
        |       |       |
        v       v       v
       FDO   NOT_FDO  AMBIGUOUS
        |       |       |
        +-------+-------+
                |
                v
       EXPLANATION GENERATOR
                |
                v
        RESULTS / DASHBOARD
                |
                v
             USER
```

------------------------------------------------------------------------

# 3. Flow Step 1 --- User Input

## Input

The prototype accepts:

``` text
Application Name
Application Category
Application Description
Privacy Policy
```

The policy may eventually be supplied as:

``` text
PDF
TXT
Pasted Text
```

## Output

A validated analysis request.

Example:

``` json
{
  "application_name": "Example App",
  "category": "Navigation",
  "description": "Provides navigation and route planning",
  "policy_text": "..."
}
```

------------------------------------------------------------------------

# 4. Flow Step 2 --- Input Validation

The backend validates:

-   application name exists
-   application description is available where required
-   policy input is not empty
-   supported policy format is provided
-   text can be processed

Invalid input should return an understandable error rather than entering
the analysis pipeline.

## Output

``` text
Validated Analysis Request
```

------------------------------------------------------------------------

# 5. Flow Step 3 --- Application / Function Context

The system establishes the functional context of the application.

Conceptually:

``` text
Application
    |
    +-- Category
    |
    +-- Function
          |
          +-- Feature
```

Example:

``` text
Application:
Navigation App

Function:
Turn-by-turn Navigation

Feature:
Route Calculation
```

This context is necessary because the FDO question is
function-dependent.

## Output

``` text
Application Context
Function Context
Feature Context
```

------------------------------------------------------------------------

# 6. Flow Step 4 --- Privacy Policy Processing

The policy processor converts the supplied policy into clean,
processable text.

## Input

``` text
PDF / TXT / Policy Text
```

## Processing

-   extract text
-   clean unnecessary formatting
-   preserve sections where possible
-   retain source information
-   prepare text for extraction

## Output

``` text
Clean Policy Text
+
Policy Metadata
```

------------------------------------------------------------------------

# 7. Flow Step 5 --- AI Policy Extraction

The AI/NLP layer analyzes the policy text.

## Candidate extraction fields

``` text
Data Type
Purpose
Entity
Sharing
Retention
Evidence Text
Source Section
```

## Example

Input:

``` text
"We collect your precise location to provide
location-based services."
```

Structured candidate:

``` json
{
  "data_type": "LOCATION",
  "purpose": "LOCATION_BASED_SERVICES",
  "evidence_text": "We collect your precise location...",
  "source_section": "Location Information"
}
```

## Important rule

The AI output is **candidate evidence**, not automatically validated
ground truth.

The original evidence must remain available.

------------------------------------------------------------------------

# 8. Flow Step 6 --- Data / Purpose Normalization

Different policy terms may refer to the same conceptual category.

Example:

``` text
GPS information
Precise location
Location information
Geolocation
```

may normalize to:

``` text
LOCATION
```

The same principle can be applied to purpose categories when supported
by the evidence.

## Important constraint

Normalization must not change the meaning of the source policy.

## Output

``` text
Normalized Policy Evidence
```

------------------------------------------------------------------------

# 9. Flow Step 7 --- Expected Data Lookup

The Expected Data Engine retrieves the relevant function-specific
baseline from the project's expected-data model.

## Input

``` text
Application
Function
Feature
```

## Output

``` text
Expected Data Type
Expected Necessity
Expected Purpose
```

Example:

``` json
{
  "function": "Route Calculation",
  "data_type": "LOCATION",
  "necessity": "L1_REQUIRED",
  "expected_purpose": "Route calculation"
}
```

The existing Stage-2 expected-data model is the conceptual baseline for
this component.

------------------------------------------------------------------------

# 10. Flow Step 8 --- Functional Comparison

The system now brings together:

``` text
Expected Data
+
Declared Policy Evidence
+
Application Function
```

Three major comparisons are performed.

## 8.1 Data Comparison

``` text
Expected Data
       vs
Declared Data
```

## 8.2 Purpose Comparison

``` text
Expected Purpose
       vs
Declared Purpose
```

## 8.3 Functional Relationship

``` text
Data Type
    |
    v
Application Function
```

The result is a structured comparison record.

------------------------------------------------------------------------

# 11. Flow Step 9 --- Necessity Test

The system evaluates the declared data against the expected necessity
baseline.

Conceptually:

``` text
L1_REQUIRED
L2_SUPPORTIVE
L3_OPTIONAL
L4_SECONDARY
L5_NO_PLAUSIBLE_LINK
```

The exact controlled vocabulary must remain aligned with the existing
Stage-2 dataset.

## Important rule

A non-L1 category does **not automatically mean FDO**.

Necessity is one part of the decision.

------------------------------------------------------------------------

# 12. Flow Step 10 --- Purpose Compatibility Test

The expected purpose is compared with the policy-supported declared
purpose.

Example:

``` text
Expected:
Route calculation

Declared:
Provide navigation and route services

Result:
Potentially compatible
```

If the evidence only says:

``` text
Improve our services
```

and does not provide enough context, the system should not invent a
specific functional purpose.

Result:

``` text
AMBIGUOUS / REVIEW
```

------------------------------------------------------------------------

# 13. Flow Step 11 --- Functional Justification Test

The system asks:

> Is there evidence supporting why this data processing is functionally
> justified?

The test uses:

``` text
Application Function
+
Data Type
+
Expected Necessity
+
Expected Purpose
+
Declared Purpose
+
Policy Evidence
```

## Possible outcomes

``` text
Supported
Not established
Unresolved
```

A lack of evidence is not automatically treated as proof of excess.

------------------------------------------------------------------------

# 14. Flow Step 12 --- FDO Decision Engine

The decision engine combines the outputs of the previous tests.

``` text
Necessity
   +
Purpose Compatibility
   +
Functional Justification
   +
Evidence
   |
   v
FDO Decision
```

Possible classifications:

``` text
FDO
NOT_FDO
AMBIGUOUS
```

## Decision principles

### Principle 1

``` text
Declared ≠ automatically FDO
```

### Principle 2

``` text
Optional ≠ automatically FDO
```

### Principle 3

``` text
Missing evidence ≠ NOT_DECLARED
```

### Principle 4

``` text
Unclear evidence → AMBIGUOUS
```

### Principle 5

A final FDO requires evidence of functional excess or purpose
incompatibility.

------------------------------------------------------------------------

# 15. Flow Step 13 --- Evidence and Provenance

Every important decision should retain its supporting evidence.

The analysis record should be able to trace:

``` text
FDO Result
    |
    +-- Decision inputs
    |
    +-- Policy evidence
    |
    +-- Source section
    |
    +-- Expected mapping
    |
    +-- Function
    |
    +-- Purpose
```

This creates an auditable chain.

------------------------------------------------------------------------

# 16. Flow Step 14 --- Explanation Generation

The explanation generator receives the structured decision.

It should generate a concise explanation based only on available
evidence.

Example:

``` text
Result: NOT_FDO

Explanation:
Location has an identifiable relationship to the
navigation function, and the available policy evidence
describes a compatible navigation-related purpose.
```

For uncertainty:

``` text
Result: AMBIGUOUS

Explanation:
The available policy evidence does not provide enough
information to establish a function-specific purpose
or functional necessity.
```

## Important rule

The explanation generator must not invent:

-   policy statements
-   purposes
-   data types
-   evidence
-   functional relationships

------------------------------------------------------------------------

# 17. Flow Step 15 --- Results Dashboard

The final structured result is sent to the frontend.

## Item-level output

``` text
Application
Function
Data Type
Expected Necessity
Expected Purpose
Declared Data
Declared Purpose
Evidence
Purpose Compatibility
Functional Justification
FDO Status
Explanation
```

## Summary output

``` text
Total analyzed mappings
FDO
NOT_FDO
AMBIGUOUS
Evidence coverage
```

The item-level explanation remains the primary research output.

------------------------------------------------------------------------

# 18. End-to-End Example

``` text
USER
 |
 | "Navigation App" + Privacy Policy
 v
INPUT VALIDATION
 |
 v
FUNCTION CONTEXT
 |
 | Function = Route Calculation
 v
POLICY PROCESSOR
 |
 v
AI EXTRACTION
 |
 | Data = Precise Location
 | Purpose = Location-based services
 v
NORMALIZATION
 |
 | LOCATION
 v
EXPECTED DATA ENGINE
 |
 | Expected = LOCATION
 | Necessity = L1_REQUIRED
 | Purpose = Route calculation
 v
COMPARISON
 |
 | Expected data matches declared data
 | Purpose appears functionally compatible
 v
FDO ENGINE
 |
 v
NOT_FDO
 |
 v
EXPLANATION
 |
 v
DASHBOARD
```

------------------------------------------------------------------------

# 19. Ambiguous Example

``` text
USER
 |
 v
POLICY
 |
 v
AI EXTRACTION
 |
 | Data = Contacts
 | Purpose = "Improve services"
 v
NORMALIZATION
 |
 v
EXPECTED DATA
 |
 | No clear function-specific requirement
 v
COMPARISON
 |
 | Purpose too generic
 v
FDO ENGINE
 |
 v
AMBIGUOUS
 |
 v
EXPLANATION
 |
 v
"Available evidence is insufficient to establish
functional necessity or a specific compatible purpose."
```

The system must not automatically label this case FDO merely because the
expected requirement is unclear.

------------------------------------------------------------------------

# 20. Error / Uncertainty Flow

``` text
                  EVIDENCE PROBLEM
                       |
             +---------+---------+
             |                   |
             v                   v
       Missing Evidence    Unclear Purpose
             |                   |
             +---------+---------+
                       |
                       v
                  AMBIGUOUS
```

The system should preserve the uncertainty and identify what evidence is
needed to resolve it.

------------------------------------------------------------------------

# 21. Relationship to Existing Benchmark

The Stage-1--7 research dataset remains separate from the automated
pipeline.

The benchmark is used for evaluation:

``` text
Existing Manual Benchmark
          |
          v
     Run Prototype
          |
          v
 Prototype Prediction
          |
          v
 Compare
          |
          v
Evaluation Metrics
```

A disagreement between the prototype and benchmark is an evaluation
result. It must not silently modify the benchmark.

------------------------------------------------------------------------

# 22. Data States Through the Pipeline

The prototype should preserve the distinction between:

``` text
RAW_POLICY
      ↓
EXTRACTED_CANDIDATE
      ↓
NORMALIZED_EVIDENCE
      ↓
COMPARISON_RECORD
      ↓
FDO_DECISION
      ↓
EXPLANATION
```

And decision states:

``` text
FDO
NOT_FDO
AMBIGUOUS
```

Earlier annotation states such as:

``` text
DECLARED
NOT_DECLARED
SOURCE_INSUFFICIENT
```

belong to the policy-evidence/annotation layer and should not be
confused with the final FDO classification.

------------------------------------------------------------------------

# 23. Stage 8.1E Completion Criteria

Stage 8.1E is complete when the project has defined:

-   [x] User input flow
-   [x] Input validation
-   [x] Application/function context
-   [x] Policy processing
-   [x] AI extraction flow
-   [x] Normalization flow
-   [x] Expected-data lookup
-   [x] Functional comparison
-   [x] Necessity test
-   [x] Purpose compatibility test
-   [x] Functional justification test
-   [x] FDO decision flow
-   [x] Evidence/provenance flow
-   [x] Explanation flow
-   [x] Dashboard flow
-   [x] Error/ambiguity handling
-   [x] Benchmark validation relationship

**Status: COMPLETE**

------------------------------------------------------------------------

# 24. Next Stage

The next architecture task is:

**Stage 8.1F --- Input / Output Specification**

This will define the exact schemas for:

-   analysis request
-   application
-   function
-   expected mapping
-   policy evidence
-   comparison result
-   FDO result
-   explanation
-   final API response

These schemas will later become the backend data models and API
contracts.
