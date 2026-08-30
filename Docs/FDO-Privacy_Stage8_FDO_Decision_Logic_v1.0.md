# FDO-Privacy --- Stage 8 FDO Decision Logic Specification

**Version:** 1.0\
**Stage:** 8.1H --- FDO Decision Logic\
**Project:** FDO-Privacy

------------------------------------------------------------------------

## 1. Purpose

This document formally defines the decision logic that the FDO-Privacy
prototype will use to classify an analyzed data practice as:

``` text
FDO
NOT_FDO
AMBIGUOUS
```

The purpose is to convert the research methodology developed in Stages
1--7 into an explicit, auditable software rule set.

The system must not make an FDO decision solely from the presence of a
data type in a privacy policy.

------------------------------------------------------------------------

# 2. Decision Inputs

The FDO Decision Engine receives:

``` text
Application
Function
Feature
Expected Data Type
Expected Necessity
Expected Purpose
Declared Data Type
Declared Purpose
Policy Evidence
Purpose Compatibility
Functional Relationship
Functional Justification
Evidence Sufficiency
```

These inputs originate from the earlier components defined in Stage
8.1D--8.1G.

------------------------------------------------------------------------

# 3. Core Decision Principle

The prototype follows this reasoning:

``` text
EXPECTED REQUIREMENT
          +
DECLARED PRACTICE
          +
FUNCTIONAL CONTEXT
          +
POLICY EVIDENCE
          |
          v
     EVALUATION
          |
          v
  FDO / NOT_FDO / AMBIGUOUS
```

The classification is based on the evidence available for the specific
application function and data item.

------------------------------------------------------------------------

# 4. Three-Way Classification

## 4.1 FDO

Use `FDO` only when the available evidence establishes a functionally
excessive or purpose-incompatible practice under the project's adopted
rules.

Conceptually:

``` text
Evidence sufficient
        AND
Functional excess established
        OR
Purpose incompatibility established
        AND
The conclusion is supported by the expected-data model
and functional context
        ↓
FDO
```

An FDO classification must be explainable using the underlying evidence.

------------------------------------------------------------------------

## 4.2 NOT_FDO

Use `NOT_FDO` when the available evidence supports a plausible
functional relationship and does not establish functional excess or
purpose incompatibility.

Conceptually:

``` text
Evidence sufficient
        AND
Functional relationship supported
        AND
Purpose compatible or otherwise justified
        AND
No functional excess established
        ↓
NOT_FDO
```

`NOT_FDO` means that an FDO was not established for that analyzed
mapping under the available evidence and rules.

It does **not** mean that the application has been proven to collect no
excessive data outside the analyzed evidence.

------------------------------------------------------------------------

## 4.3 AMBIGUOUS

Use `AMBIGUOUS` when the available evidence is insufficient to make a
defensible binary classification.

Conceptually:

``` text
Evidence insufficient
        OR
Purpose unclear
        OR
Functional relationship unclear
        OR
Conflicting evidence
        ↓
AMBIGUOUS
```

Ambiguous cases must remain visible for review.

They must not be silently converted into `FDO` or `NOT_FDO`.

------------------------------------------------------------------------

# 5. Decision Pipeline

The decision engine should evaluate the following stages in order.

``` text
START
  |
  v
Is sufficient evidence available?
  |
  +---- NO ----> AMBIGUOUS
  |
 YES
  |
  v
Is the data/function relationship evaluated?
  |
  +---- NO ----> AMBIGUOUS
  |
 YES
  |
  v
Evaluate necessity
  |
  v
Evaluate purpose compatibility
  |
  v
Evaluate functional justification
  |
  v
Is functional excess or purpose incompatibility established?
  |
  +---- YES ---> FDO
  |
  NO
  |
  v
Is the functional relationship/purpose sufficiently supported?
  |
  +---- YES ---> NOT_FDO
  |
  NO
  |
  v
AMBIGUOUS
```

------------------------------------------------------------------------

# 6. Evidence Sufficiency Gate

Evidence sufficiency is evaluated before making a strong binary claim.

### Sufficient evidence

Evidence is sufficient when the available records provide enough
information to evaluate the relevant data/function relationship and
purpose.

### Insufficient evidence

Evidence is insufficient when important information needed for the
decision is unavailable, unresolved, or too generic.

### Rule

``` text
Insufficient evidence
        ↓
AMBIGUOUS
```

This prevents unsupported FDO or NOT_FDO classifications.

------------------------------------------------------------------------

# 7. Necessity Test

The system compares the declared data practice with the expected
necessity baseline.

The existing project vocabulary includes:

``` text
L1_REQUIRED
L2_SUPPORTIVE
L3_OPTIONAL
L4_SECONDARY
L5_NO_PLAUSIBLE_LINK
```

The implementation must use the frozen project's established labels.

## Important rule

Necessity alone does not determine FDO.

For example:

``` text
L3_OPTIONAL
      ≠
FDO
```

The purpose and functional relationship must also be evaluated.

------------------------------------------------------------------------

# 8. Purpose Compatibility Test

The system compares:

``` text
Expected Purpose
       vs
Declared Purpose
```

### Compatible

The declared purpose has a plausible relationship to the expected
application function.

### Incompatible

The available evidence establishes a purpose that conflicts with the
expected function-specific justification.

### Unclear

The policy wording is too broad or incomplete to establish
compatibility.

Example:

``` text
Expected:
Route calculation

Declared:
Improve services
```

If the available context cannot establish whether this purpose is
functionally related:

``` text
Purpose = UNCERTAIN
        ↓
Potential AMBIGUOUS
```

The system must not invent a more specific purpose.

------------------------------------------------------------------------

# 9. Functional Relationship Test

The system evaluates:

``` text
Data Type
     +
Application Function
```

### Supported relationship

There is evidence that the data is plausibly needed or useful for the
identified function.

### Unsupported relationship

The evidence does not establish a plausible functional relationship.

### Unclear relationship

The available evidence does not allow a reliable determination.

An unclear relationship should generally result in `AMBIGUOUS` unless
another explicit project rule establishes a defensible classification.

------------------------------------------------------------------------

# 10. Functional Justification Test

The system asks:

> Is there sufficient evidence explaining why the application processes
> this data in relation to its function or stated purpose?

Inputs:

``` text
Application Function
Expected Data
Necessity
Expected Purpose
Declared Purpose
Policy Evidence
```

Possible states:

``` text
SUPPORTED
NOT_ESTABLISHED
UNCERTAIN
```

### Important principle

`NOT_ESTABLISHED` does not automatically mean `FDO`.

If the evidence is insufficient to establish either excess or legitimate
functional justification, the result may be:

``` text
AMBIGUOUS
```

------------------------------------------------------------------------

# 11. Decision Matrix

The following matrix defines the high-level classification behavior.

  -----------------------------------------------------------------------------
  Evidence       Functional     Purpose        Functional Excess Result
                 Relationship                  / Incompatibility 
  -------------- -------------- -------------- ----------------- --------------
  Sufficient     Supported      Compatible     Not established   NOT_FDO

  Sufficient     Supported      Compatible     Established       FDO

  Sufficient     Unsupported    Incompatible   Established       FDO

  Sufficient     Unsupported    Unclear        Not established   AMBIGUOUS

  Insufficient   Any            Any            Not established   AMBIGUOUS

  Sufficient     Unclear        Unclear        Not established   AMBIGUOUS

  Conflicting    Any            Any            Cannot establish  AMBIGUOUS
                                               safely            
  -----------------------------------------------------------------------------

This matrix is a design-level rule and will be translated into
deterministic backend logic during implementation.

------------------------------------------------------------------------

# 12. Missing Evidence Rules

The system must distinguish:

``` text
Missing Evidence
```

from:

``` text
Explicit Non-Declaration
```

Therefore:

``` text
Missing extraction
      ≠
NOT_DECLARED
```

and:

``` text
No evidence found
      ≠
Proof of no collection
```

If missing evidence prevents a reliable FDO decision:

``` text
AMBIGUOUS
```

------------------------------------------------------------------------

# 13. Optional Data Rule

The presence of an optional or secondary data practice is not sufficient
by itself to establish FDO.

For example:

``` text
Necessity = L3_OPTIONAL
```

does not automatically produce:

``` text
FDO
```

The decision must still evaluate:

``` text
Purpose
Functional relationship
Justification
Evidence
```

------------------------------------------------------------------------

# 14. AI Decision Boundary

The AI/NLP layer may provide:

``` text
Extracted Data
Extracted Purpose
Normalized Terms
Candidate Functional Relationship
Draft Explanation
```

But the AI must not independently make the final FDO classification.

The architecture is:

``` text
AI Extraction
      |
      v
Structured Evidence
      |
      v
Deterministic FDO Rules
      |
      v
Final Classification
```

If AI confidence is low or evidence is unclear, the system should
preserve uncertainty rather than force a classification.

------------------------------------------------------------------------

# 15. Contradiction Handling

If policy evidence contains contradictory statements:

``` text
Evidence A → Purpose X

Evidence B → Purpose Y
```

the system should not arbitrarily choose one.

Instead:

``` text
Conflicting evidence
        ↓
Review / AMBIGUOUS
```

unless additional evidence resolves the contradiction.

------------------------------------------------------------------------

# 16. Explanation Requirement

Every final classification must have an explanation.

## FDO

The explanation must identify:

-   relevant function
-   data type
-   expected requirement
-   conflicting/excessive evidence
-   reason for FDO

## NOT_FDO

The explanation must identify:

-   relevant function
-   expected data requirement
-   declared purpose
-   functional relationship
-   why excess was not established

## AMBIGUOUS

The explanation must identify:

-   what evidence is available
-   what evidence is missing or unclear
-   why a binary decision cannot safely be made

------------------------------------------------------------------------

# 17. Evidence Traceability

Every FDO decision should be traceable to:

``` text
Application
   ↓
Function
   ↓
Expected Mapping
   ↓
Policy Evidence
   ↓
Comparison
   ↓
Decision
   ↓
Explanation
```

The result must never depend solely on an unexplained model-generated
statement.

------------------------------------------------------------------------

# 18. Pseudocode

The initial deterministic logic can be represented as:

``` text
function classify(mapping, evidence, comparison):

    if evidence is insufficient:
        return AMBIGUOUS

    if functional relationship is unclear:
        return AMBIGUOUS

    if purpose compatibility is unclear
       and no other evidence resolves it:
        return AMBIGUOUS

    if functional excess is established:
        return FDO

    if purpose incompatibility is established:
        return FDO

    if functional relationship is supported
       and purpose is compatible
       and no excess is established:
        return NOT_FDO

    return AMBIGUOUS
```

This is intentionally conservative.

The exact implementation thresholds and controlled values will be
encoded in the backend after this specification is reviewed.

------------------------------------------------------------------------

# 19. Example --- NOT_FDO

``` text
Application:
Navigation App

Function:
Route Calculation

Expected Data:
Location

Necessity:
L1_REQUIRED

Expected Purpose:
Route calculation

Declared Data:
Location

Declared Purpose:
Location-based services

Functional Relationship:
Supported

Purpose Compatibility:
Compatible

Functional Excess:
Not established

Result:
NOT_FDO
```

### Explanation

Location has an identifiable relationship to the navigation function,
and the available policy evidence supports a compatible service purpose.

------------------------------------------------------------------------

# 20. Example --- FDO

``` text
Application:
Example Utility

Function:
Basic Calculator

Expected Data:
Calculator input

Declared Data:
Contacts

Declared Purpose:
Contact-based advertising

Functional Relationship:
Unsupported

Purpose:
Incompatible with identified calculator function

Functional Excess:
Established

Result:
FDO
```

This is a conceptual example of how an FDO could be established; it is
not a result from the existing benchmark.

------------------------------------------------------------------------

# 21. Example --- AMBIGUOUS

``` text
Application:
Example App

Function:
Core Service

Expected Data:
Contacts

Declared Data:
Contacts

Declared Purpose:
Improve services

Functional Relationship:
Unclear

Evidence:
Policy wording is generic

Result:
AMBIGUOUS
```

### Explanation

The available evidence does not establish enough information to
determine functional necessity or a specific compatible purpose.

------------------------------------------------------------------------

# 22. Relationship to Existing Stage 5 Results

The current research benchmark contains:

``` text
Evidence-backed mappings: 93
NOT_FDO: 60
AMBIGUOUS: 33
FDO established: 0
```

The Stage 8 prototype must not hard-code these values as its decision
logic.

Instead:

``` text
Decision Rules
      ↓
Prototype Prediction
      ↓
Compare with Benchmark
```

The benchmark remains a validation reference.

------------------------------------------------------------------------

# 23. Conservative Classification Principle

The prototype should prefer:

``` text
AMBIGUOUS
```

over an unsupported binary decision.

This is especially important for:

-   generic policy language
-   incomplete policy evidence
-   conflicting evidence
-   uncertain function identification
-   uncertain purpose mapping
-   low-confidence extraction

The purpose is to avoid false certainty.

------------------------------------------------------------------------

# 24. Audit Record

Each decision should retain enough information to reconstruct the
classification.

Minimum audit fields:

``` text
analysis_id
application_id
function_id
expected_id
evidence_id
necessity_result
purpose_result
functional_relationship
functional_justification
evidence_sufficiency
classification
explanation
```

------------------------------------------------------------------------

# 25. Stage 8.1H Completion Criteria

Stage 8.1H is complete when the project has formally defined:

-   [x] FDO definition boundary
-   [x] NOT_FDO definition boundary
-   [x] AMBIGUOUS definition boundary
-   [x] Evidence sufficiency gate
-   [x] Necessity test
-   [x] Purpose compatibility test
-   [x] Functional relationship test
-   [x] Functional justification test
-   [x] Decision matrix
-   [x] Missing evidence handling
-   [x] Optional-data handling
-   [x] AI decision boundary
-   [x] Contradiction handling
-   [x] Explanation requirements
-   [x] Evidence traceability
-   [x] Decision pseudocode
-   [x] Benchmark relationship
-   [x] Audit requirements

**Status: COMPLETE**

------------------------------------------------------------------------

# 26. Next Stage

**Stage 8.1I --- AI Responsibilities Specification**

The next step will formally define exactly what the AI is allowed to do,
including:

-   policy extraction
-   data-type identification
-   purpose identification
-   normalization assistance
-   uncertainty handling
-   evidence citation
-   explanation drafting
-   AI confidence
-   human/rule validation boundaries

The AI will remain an assisting component, not the final FDO authority.
