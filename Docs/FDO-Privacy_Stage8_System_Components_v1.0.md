# FDO-Privacy --- Stage 8 System Components Specification

**Version:** 1.0\
**Stage:** 8.1D --- System Components\
**Project:** FDO-Privacy

------------------------------------------------------------------------

## 1. Purpose

This document formally defines the major software components of the
FDO-Privacy prototype.

The Stage 8 implementation converts the research workflow developed in
Stages 1--7 into a working prototype. The system should connect
application functionality, expected data requirements, privacy-policy
evidence, functional comparison, FDO reasoning, and explainable results.

The implementation must preserve the project's evidence-first
methodology:

-   AI may extract and normalize policy information.
-   AI-generated information is evidence/candidate information, not
    automatic ground truth.
-   FDO decisions must be based on explicit research rules and available
    evidence.
-   Ambiguous cases must remain `AMBIGUOUS`.
-   Missing evidence must not automatically become `NOT_DECLARED`.
-   Declaration of a data type does not automatically make it FDO.
-   Optional or secondary data does not automatically make it FDO.

------------------------------------------------------------------------

## 2. High-Level Component Architecture

``` text
                         USER
                           |
                           v
                 +-------------------+
                 |   User Interface  |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Application Input |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Policy Processor  |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | AI Policy         |
                 | Extraction        |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Data / Purpose    |
                 | Normalization     |
                 +---------+---------+
                           |
             +-------------+-------------+
             |                           |
             v                           v
   +-------------------+       +-------------------+
   | Expected Data     |       | Policy Evidence   |
   | Engine            |       | Store             |
   +---------+---------+       +---------+---------+
             |                           |
             +-------------+-------------+
                           |
                           v
                 +-------------------+
                 | Functional        |
                 | Comparison Engine  |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | FDO Decision      |
                 | Engine            |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Explanation       |
                 | Generator         |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Results / Report  |
                 | Dashboard         |
                 +-------------------+
```

------------------------------------------------------------------------

## 3. Component Inventory

  -----------------------------------------------------------------------
  \#                      Component               Main Responsibility
  ----------------------- ----------------------- -----------------------
  1                       User Interface          Collect
                                                  application/policy
                                                  input and display
                                                  results

  2                       Application Information Represent what the
                          Manager                 application does and
                                                  its functions

  3                       Privacy Policy          Accept and clean policy
                          Processor               documents/text

  4                       AI Policy Extraction    Extract data types,
                                                  purposes and related
                                                  policy evidence

  5                       Data / Purpose          Convert different
                          Normalization           policy terms into a
                                                  controlled vocabulary

  6                       Expected Data Engine    Retrieve
                                                  function-specific
                                                  expected data
                                                  requirements

  7                       Policy Evidence Store   Preserve extracted
                                                  evidence and provenance

  8                       Functional Comparison   Compare expected and
                          Engine                  declared data/purposes

  9                       FDO Decision Engine     Apply the explicit FDO
                                                  reasoning rules

  10                      Explanation Generator   Produce evidence-backed
                                                  human-readable
                                                  explanations

  11                      Results / Report        Present item-level
                          Dashboard               results and summaries
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 4. Component Specifications

## 4.1 User Interface

### Purpose

Provide the user-facing entry point to the FDO-Privacy system.

### Inputs

The interface should eventually accept:

-   Application name
-   Application category
-   Application description
-   Privacy policy

The privacy policy may eventually be provided as:

-   PDF
-   TXT
-   pasted text

### Outputs

The interface displays:

-   analyzed application
-   identified functions
-   data items
-   expected status
-   declared status
-   necessity
-   purpose compatibility
-   evidence
-   FDO status
-   explanation

### Responsibility

The UI is responsible for presentation and input collection. It does not
make FDO decisions.

------------------------------------------------------------------------

## 4.2 Application Information Manager

### Purpose

Represent the functionality of the application being analyzed.

### Core concepts

``` text
Application
    |
    +-- Category
    |
    +-- Function
          |
          +-- Feature
```

### Example

``` text
Application: Navigation App

Function: Turn-by-turn Navigation

Feature: Route Calculation
```

### Responsibility

Provide the functional context required for determining whether a
particular data type has a plausible relationship with an application
function.

------------------------------------------------------------------------

## 4.3 Privacy Policy Processor

### Purpose

Convert the supplied privacy policy into processable text.

### Input

``` text
PDF / TXT / policy text
```

### Processing

-   document reading
-   text extraction
-   basic cleaning
-   section preservation where possible
-   preparation for AI extraction

### Output

Clean policy text and associated document metadata.

### Responsibility

This component prepares evidence. It does not decide whether processing
is excessive.

------------------------------------------------------------------------

## 4.4 AI Policy Extraction

### Purpose

Use an AI/NLP model to identify structured privacy-policy information.

### Candidate fields

``` text
Data Type
Purpose
Entity
Sharing
Retention
Evidence Text
Source Section
```

### Example

Policy text:

``` text
"We collect your precise location to provide
location-based services."
```

Possible structured extraction:

``` text
Data Type: LOCATION
Purpose: LOCATION_BASED_SERVICE
Evidence: exact policy statement
```

### Important constraint

AI extraction is not automatically ground truth.

The extracted result must retain:

-   source evidence
-   provenance
-   confidence/uncertainty where applicable

Human or rule-based validation can be applied before a result becomes an
accepted analytical record.

------------------------------------------------------------------------

## 4.5 Data / Purpose Normalization

### Purpose

Normalize different expressions that refer to the same conceptual
category.

### Example

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

Similarly, different purpose descriptions may be mapped to controlled
purpose categories when the evidence supports doing so.

### Responsibility

Create a consistent representation for comparison.

### Constraint

Normalization must not change the meaning of the source evidence.

------------------------------------------------------------------------

## 4.6 Expected Data Engine

### Purpose

Provide the expected data requirement for the relevant
application/function.

The expected-data model developed during earlier project stages is the
research baseline.

### Core mapping

``` text
Application
    +
Function
    +
Data Type
    +
Necessity
    +
Expected Purpose
```

### Example

``` text
Function:
Navigation

Data Type:
Precise Location

Necessity:
L1_REQUIRED

Expected Purpose:
Route calculation
```

### Responsibility

Provide the expected baseline against which declared policy practices
are compared.

------------------------------------------------------------------------

## 4.7 Policy Evidence Store

### Purpose

Preserve extracted policy evidence and provenance.

### Candidate fields

``` text
Application
Data Type
Purpose
Entity
Sharing
Retention
Raw Policy Term
Evidence Text
Official Source
Source Section
Extraction Status
```

### Responsibility

Maintain the evidence trail.

### Important rule

A missing record or unresolved extraction must not automatically be
interpreted as proof that an application does not collect the data.

------------------------------------------------------------------------

## 4.8 Functional Comparison Engine

### Purpose

Compare the expected data model with policy-declared data.

### Main comparisons

#### Comparison 1 --- Expected vs Declared

``` text
Expected Data
       vs
Declared Data
```

#### Comparison 2 --- Expected Purpose vs Declared Purpose

``` text
Expected Purpose
       vs
Declared Purpose
```

#### Comparison 3 --- Necessity vs Functional Relationship

``` text
Expected Necessity
       vs
Application Function
```

### Output

A structured comparison record that is passed to the FDO Decision
Engine.

------------------------------------------------------------------------

## 4.9 FDO Decision Engine

### Purpose

Apply the project's explicit FDO reasoning rules.

### Core inputs

``` text
Expected Data
Declared Data
Expected Necessity
Expected Purpose
Declared Purpose
Functional Context
Policy Evidence
```

### Core tests

``` text
1. Necessity Test
2. Purpose Compatibility Test
3. Functional Justification Test
```

### Possible outputs

``` text
FDO
NOT_FDO
AMBIGUOUS
```

### Decision principles

#### Principle 1

``` text
Declared data ≠ automatically FDO
```

#### Principle 2

``` text
Optional data ≠ automatically FDO
```

#### Principle 3

``` text
Missing evidence ≠ NOT_DECLARED
```

#### Principle 4

``` text
Unclear evidence → AMBIGUOUS
```

#### Principle 5

A final FDO requires evidence of functional excess or purpose
incompatibility.

### Separation from AI

The LLM should not directly override the FDO rules.

The decision engine receives structured evidence and applies the defined
research logic.

------------------------------------------------------------------------

## 4.10 Explanation Generator

### Purpose

Convert the structured decision and supporting evidence into a
human-readable explanation.

### Example output

``` text
Data Type: Location

Result: NOT_FDO

Explanation:
Location has an identifiable relationship to the
application's navigation functionality, and the
available policy evidence provides a compatible
service purpose.
```

For unresolved evidence:

``` text
Data Type: Contacts

Result: AMBIGUOUS

Explanation:
The available policy evidence does not provide
enough information to establish a function-specific
purpose or functional necessity.
```

### Constraint

The explanation generator must not invent policy evidence.

Explanations must be derived from structured evidence already available
to the system.

------------------------------------------------------------------------

## 4.11 Results / Report Dashboard

### Purpose

Present the analysis in an understandable and auditable form.

### Item-level result

Each analyzed data item should expose:

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

### Summary-level result

The dashboard may additionally show:

-   number of analyzed data items
-   FDO count
-   NOT_FDO count
-   AMBIGUOUS count
-   evidence coverage
-   application-level summaries

A single opaque privacy score must not replace the item-level
explanation.

------------------------------------------------------------------------

# 5. AI Responsibilities vs Rule Responsibilities

This separation is fundamental to the architecture.

## AI / NLP Layer

AI can assist with:

``` text
Policy text extraction
Data-type identification
Purpose identification
Term normalization
Evidence summarization
Explanation drafting
```

## Research / Rule Layer

The deterministic research layer handles:

``` text
Expected-data lookup
Necessity comparison
Purpose compatibility
Functional justification
FDO classification
Ambiguity handling
```

### Architecture principle

``` text
AI
 |
 | extracts / structures
 v
Structured Evidence
 |
 v
Research Rules
 |
 v
FDO Decision
```

This prevents the prototype from becoming an opaque "LLM says FDO"
system.

------------------------------------------------------------------------

# 6. Component Interaction

The intended interaction sequence is:

``` text
1. User supplies application + policy
2. Policy Processor extracts/cleans policy text
3. AI Extraction identifies candidate data/purpose evidence
4. Normalization converts evidence to controlled concepts
5. Expected Data Engine retrieves the expected mapping
6. Functional Comparison compares expected and declared information
7. FDO Decision Engine applies necessity/purpose/justification tests
8. Explanation Generator creates the evidence-backed explanation
9. Dashboard presents the result
```

------------------------------------------------------------------------

# 7. Relationship to Existing Research Artifacts

The prototype must reuse the research artifacts already produced rather
than creating a disconnected dataset.

``` text
Stage 1
Research Foundation
        |
        v
Stage 2
Expected Data Model
        |
        v
Stage 3
Policy Evidence / Annotation
        |
        v
Stage 4
FDO Analysis
        |
        v
Stage 5
Final Mapping Dataset
        |
        v
Stage 6
Results / Findings
        |
        v
Stage 7
Research Report
        |
        v
Stage 8
Working Prototype
```

The existing benchmark should be preserved as a reference for later
prototype evaluation.

------------------------------------------------------------------------

# 8. Prototype Validation Principle

The manually adjudicated project dataset is the benchmark for evaluating
the automated prototype.

The intended process is:

``` text
Existing Research Benchmark
             |
             v
      Run Prototype
             |
             v
     Prototype Results
             |
             v
      Compare Results
             |
             v
Evaluation Metrics
```

The prototype must not rewrite the benchmark simply because an automated
prediction differs from the manually adjudicated result.

Differences become evaluation results.

------------------------------------------------------------------------

# 9. Initial Implementation Boundary

Stage 8 should begin with a minimal working prototype.

### Version 0.1

``` text
Policy Text
    ↓
AI Extraction
    ↓
Structured Evidence
    ↓
Expected Data Lookup
    ↓
FDO Rule Engine
    ↓
Explanation
    ↓
JSON Result
```

Later versions can add:

-   PDF upload
-   database persistence
-   web dashboard
-   benchmark evaluation
-   advanced NLP
-   knowledge graph / GraphRAG if justified

Complex infrastructure should not be introduced before the basic FDO
pipeline works.

------------------------------------------------------------------------

# 10. Technology Direction

The planned implementation can use:

``` text
Frontend:
React / Next.js

Backend:
Python + FastAPI

AI / NLP:
LLM + NLP utilities

Data:
SQLite initially
PostgreSQL if needed later

Visualization:
Charting library

Optional future knowledge representation:
Neo4j / graph-based layer
```

Technology choices may be refined during implementation if the prototype
requirements justify a change.

------------------------------------------------------------------------

# 11. Security and Evidence Principles

The implementation should:

-   preserve source evidence
-   avoid silently modifying source policy text
-   distinguish extracted evidence from model-generated explanations
-   retain uncertainty
-   avoid unsupported negative claims
-   maintain provenance for important analytical decisions
-   prevent AI-generated text from becoming unverified evidence

------------------------------------------------------------------------

# 12. Stage 8.1D Completion Criteria

Stage 8.1D is complete when the project has formally defined:

-   [x] User Interface
-   [x] Application Information Manager
-   [x] Privacy Policy Processor
-   [x] AI Policy Extraction
-   [x] Data / Purpose Normalization
-   [x] Expected Data Engine
-   [x] Policy Evidence Store
-   [x] Functional Comparison Engine
-   [x] FDO Decision Engine
-   [x] Explanation Generator
-   [x] Results / Report Dashboard
-   [x] AI vs rule-engine responsibility
-   [x] Component interaction
-   [x] Prototype validation relationship

**Status: COMPLETE**

------------------------------------------------------------------------

# 13. Next Stage

After completing Stage 8.1D, continue with:

**Stage 8.1E --- Complete Data Flow Specification**

This will define the exact information passed between components,
including the structured input/output objects that will later become the
backend data models and API contracts.
