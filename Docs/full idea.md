# FDO Privacy — Full Project Idea

## 1. Project Title

**FDO Privacy: An Explainable Functional Data Ontology Framework for Semantic Privacy Analysis**

### Possible IEEE-style titles
- Functional Data Ontology for Explainable Privacy Policy Analysis
- Semantic Privacy Analysis Using Functional Data Ontology and Knowledge Graph Reasoning
- An Ontology-Driven Framework for Functional Data Overreach Detection in Privacy Policies
- FDO Privacy: An AI and Knowledge-Graph Framework for Machine-Readable Privacy Analysis

---

## 2. Executive Idea

The central problem addressed by FDO Privacy is that privacy information is mostly presented as natural-language privacy policies. These policies are difficult for ordinary users to understand and, more importantly for this project, difficult for machines to interpret, connect, compare, and reason about automatically.

The project proposes a **Functional Data Ontology (FDO)** that represents privacy information as structured, machine-readable knowledge.

Instead of keeping privacy information only as statements such as:

> "The application may collect location information to provide location-based services and may share information with service providers."

the system converts the meaning into structured relationships:

```text
Application
    -> performs -> Navigation
Navigation
    -> requires -> Location
Application
    -> collects -> Location
Location
    -> usedFor -> NavigationService
Application
    -> shares -> Location
Location
    -> sharedWith -> ServiceProvider
Location
    -> retainedFor -> RetentionPeriod
User
    -> hasRightTo -> DeleteData
```

This structured representation can then be stored in an RDF/OWL knowledge graph and queried using SPARQL.

A reasoning engine can derive information that was not explicitly written as a single sentence but follows logically from the ontology.

The central pipeline is:

```text
Natural-Language Privacy Information
                |
                v
        NLP / AI Extraction
                |
                v
      Structured Privacy Facts
                |
                v
       FDO Ontology (OWL/RDF)
                |
                v
       Knowledge Graph (Neo4j / RDF Store)
                |
                v
        SPARQL / Reasoning
                |
                v
 Semantic Privacy Analysis & FDO Detection
                |
                v
     Explainable Human Report
```

---

## 3. Problem We Are Solving

Privacy policies are usually:
- lengthy;
- written in natural language;
- legally or technically complex;
- inconsistent in terminology;
- difficult to compare;
- difficult for machines to reason over.

A privacy policy may mention a data type in one section, its purpose in another, its recipient somewhere else, and its retention period in another section.

A human may understand these statements by reading the document as a whole. A machine needs the relationships to be explicitly represented or computationally inferred.

### Research gap

Existing privacy systems may focus on:
- privacy-policy summarization;
- individual privacy-statement extraction;
- consent management;
- runtime compliance;
- privacy scoring.

FDO Privacy focuses on a semantic foundation:

> **Representing the functional meaning and relationships of privacy information as machine-readable knowledge so automated semantic analysis and reasoning become possible.**

Therefore, the project is not merely another privacy-policy summarizer.

---

## 4. Core Research Questions

### Main question

> **Can natural-language privacy information be transformed into a Functional Data Ontology that enables machines to represent, query, reason about, and detect inconsistencies or functional overreach in data practices?**

### Specific question

> **Can an application's functional requirements and its declared privacy practices be represented in a common semantic model and compared automatically to identify whether data usage matches declared functionality and purpose?**

---

## 5. Functional Data Ontology (FDO)

### 5.1 What is FDO?

FDO stands for **Functional Data Ontology**.

The ontology defines concepts and relationships needed to represent how personal data functions within an application ecosystem.

It describes relationships among:
- applications;
- application functions;
- personal data;
- processing activities;
- purposes;
- recipients;
- retention;
- consent;
- user rights;
- security;
- expected data requirements;
- privacy-policy evidence.

### 5.2 Why "functional"?

The project does not only ask:

> "What data is collected?"

It asks:

> **"What function does the application perform, what data does that function require, what processing occurs, why is the data processed, and does the declared data practice correspond to that function?"**

Example:

```text
Navigation Application
        |
        +-- performsFunction --> Navigation
                                  |
                                  +-- requiresData --> Location
```

If the policy also states that the application collects Contacts or Medical History, the semantic model provides a basis for asking whether these data types are required by the identified functionality.

---

## 6. Functional Data Overreach (FDO)

### Definition

Functional Data Overreach is:

> **Collection or processing of user data that exceeds the minimum data reasonably required for the application's identified primary functionality, subject to the stated purpose and available justification.**

### Example

Flashlight application:

```text
Function:
Turn flashlight ON/OFF

Expected:
Flash/camera capability

Declared:
Location
Contacts
Microphone
Device identifiers
```

The system identifies unexpected data as FDO candidates.

Importantly, an unexpected data type is **not automatically declared illegal, malicious, or wrong**. The system continues to examine:
- purpose;
- justification;
- disclosure;
- recipients;
- processing activity;
- retention;
- consent;
- policy consistency.

The result is an explainable analytical classification rather than a simplistic good/bad label.

---

## 7. Core Philosophy

FDO Privacy follows four principles:

### 7.1 Semantic Representation
Privacy information should be represented as structured knowledge rather than remaining only as text.

### 7.2 Functional Context
Data collection should be interpreted in relation to application functionality.

### 7.3 Machine Reasoning
The representation should support semantic queries and logical inference.

### 7.4 Explainability
Every detected issue should be traceable to policy evidence, ontology relationships, queries, and reasoning.

---

# 8. Overall System Architecture

```text
                         USER
                          |
                          v
                Web Application / UI
                          |
             +------------+------------+
             |                         |
             v                         v
      Privacy Policy Input       Application Input
       PDF / URL / Text       Name / Category / Description
             |                         |
             +------------+------------+
                          |
                          v
                 FastAPI Backend
                          |
                          v
                Policy Acquisition
                          |
                          v
                 Text Extraction
                          |
                          v
                 Clause Segmentation
                          |
                          v
                  NLP / AI Layer
                          |
             +------------+------------+
             |                         |
             v                         v
     Privacy Fact Extraction    Function Extraction
             |                         |
             v                         v
     Data / Purpose / Share      App Functions
     Retention / Rights         Expected Data
             |                         |
             +------------+------------+
                          |
                          v
                  FDO Mapping Layer
                          |
                          v
                    FDO Ontology
                     OWL + RDF
                          |
                          v
                  Knowledge Graph
                  Neo4j / RDF Store
                          |
             +------------+------------+
             |                         |
             v                         v
        SPARQL Queries          Reasoning Engine
                                      |
                                      v
                               Derived Knowledge
             |                         |
             +------------+------------+
                          |
                          v
                 FDO Analysis Engine
                          |
             +------------+------------+
             |                         |
             v                         v
     Functional Gap Analysis    Policy Justification
             |                         |
             +------------+------------+
                          |
                          v
                 Risk / Analysis Layer
                          |
                          v
                 Explainable Report
                          |
                          v
                    Dashboard
                          |
                          v
                         USER
```

---

# 9. End-to-End Project Flow

## Step 1 — User input

The user provides:
- Privacy Policy PDF;
- Privacy Policy URL;
- or Privacy Policy text.

Optional application metadata:
- name;
- category;
- description;
- functionality;
- store metadata.

## Step 2 — Policy acquisition

If a URL is supplied, the system retrieves the relevant policy.

If a PDF is supplied, the system extracts its text.

The result is normalized into machine-processable text.

## Step 3 — Text preprocessing

The NLP pipeline:
- removes irrelevant formatting;
- identifies headings;
- splits paragraphs;
- performs sentence segmentation;
- performs clause segmentation;
- normalizes terminology;
- identifies candidate privacy statements.

## Step 4 — NLP and AI extraction

The AI/NLP layer extracts candidate:
- data types;
- processing activities;
- purposes;
- recipients;
- retention;
- consent;
- user rights;
- security information.

## Step 5 — Application function analysis

The system analyzes the application description and identifies functions.

Example:

```text
"Provides turn-by-turn navigation,
route planning and nearby place discovery."

        ↓

Functions:
Navigation
Route Planning
Nearby Place Discovery
```

## Step 6 — Expected data identification

The FDO/Expected Data Ontology maps application functions to reasonably expected data.

Example:

```text
Navigation -> requires -> Location
```

## Step 7 — Ontology mapping

Extracted privacy facts and functional requirements are mapped into FDO concepts and relationships.

## Step 8 — RDF/OWL representation

The semantic facts are represented using RDF triples and the FDO OWL ontology.

## Step 9 — Knowledge graph

The resulting semantic knowledge is stored and/or synchronized into the graph layer.

## Step 10 — SPARQL and reasoning

SPARQL queries retrieve relevant relationships. A reasoning engine derives implicit relationships and checks ontology consistency where applicable.

## Step 11 — FDO detection

Expected data is compared with declared/collected data.

## Step 12 — Policy justification

For unexpected data, the system checks whether the policy provides a stated purpose or justification.

## Step 13 — Explainable analysis

The system produces an evidence-backed explanation.

## Step 14 — Dashboard/report

The user receives:
- expected data;
- declared data;
- unexpected data;
- FDO classification;
- policy justification;
- data-flow relationships;
- risk indicators;
- evidence;
- recommendations;
- comparison information.

---

# 10. NLP Layer

The NLP layer converts unstructured privacy-policy language into candidate structured facts.

### Data entities
- Location
- Email
- Phone number
- Contacts
- Device ID
- IP address
- Transaction data

### Purpose entities
- Service delivery
- Analytics
- Personalization
- Advertising
- Security
- Fraud prevention

### Processing activities
- Collect
- Store
- Use
- Share
- Disclose
- Retain
- Delete

### Recipient entities
- Service provider
- Advertising partner
- Analytics provider
- Business partner
- Government authority

### User rights
- Access
- Correction
- Deletion
- Portability
- Withdrawal of consent

The NLP layer can use a combination of deterministic preprocessing, NLP libraries, embeddings, and LLM-based semantic extraction.

---

# 11. AI API Layer

An LLM API can be used for semantic extraction and classification from privacy-policy clauses.

Possible providers:
- OpenAI API;
- Google Gemini API;
- another compatible LLM service.

The LLM should not be treated as the final source of truth.

The architecture should be:

```text
Privacy Policy
      |
      v
LLM / NLP
      |
      v
Candidate Facts
      |
      v
Validation / Normalization
      |
      v
FDO Ontology Mapping
```

The AI performs language understanding. The ontology and reasoning layer provide formal structure and logical analysis.

### Example

Input:

```text
"We may collect your precise location to provide
navigation and improve our location-based services."
```

Structured output:

```json
{
  "data_type": "Location",
  "precision": "Precise",
  "activity": "Collect",
  "purpose": [
    "Navigation",
    "Service Improvement"
  ],
  "evidence": "original policy clause"
}
```

The extracted information is normalized and mapped to ontology concepts.

---

# 12. AI Output Schema

The LLM should preferably return controlled structured output rather than unrestricted prose.

Conceptually:

```text
Clause
 |
 +-- DataType
 +-- ProcessingActivity
 +-- Purpose
 +-- Recipient
 +-- Retention
 +-- Consent
 +-- UserRight
 +-- Evidence
 +-- Confidence
```

The backend validates the output before inserting it into the knowledge graph.

---

# 13. Application Function Analyzer

The second major AI/NLP task is understanding what the application does.

Example:

```text
Application description:
"Navigate, find nearby places and get
turn-by-turn directions."

        ↓

Functions:
Navigation
Location Search
Directions

        ↓

Expected Data:
Location
```

The functional model is then connected to the privacy model.

---

# 14. Expected Data Ontology

The Expected Data Ontology maps application functionality to data that is reasonably required or optionally useful.

Example:

| Application Function | Expected Data | Optional Data |
|---|---|---|
| Messaging | Phone / Contacts | Camera |
| Navigation | Location | Camera |
| Banking | Identity / Transaction data | Location |
| Streaming | Account / Device information | Location |
| Shopping | Account / Address / Payment data | Location |
| Flashlight | Device/flash capability | None |

This ontology establishes the baseline against which declared data practices can be evaluated.

---

# 15. FDO Ontology — OWL + RDF

The FDO ontology is the semantic backbone of the system.

## RDF

RDF represents information as triples:

```text
Subject -> Predicate -> Object
```

Example:

```text
NavigationApp -> performsFunction -> Navigation
Navigation -> requiresData -> Location
NavigationApp -> collectsData -> Location
Location -> usedFor -> NavigationService
NavigationApp -> sharesDataWith -> ServiceProvider
```

## OWL

OWL formally defines:
- classes;
- properties;
- restrictions;
- subclass relationships;
- equivalence;
- logical characteristics;
- semantic constraints.

Suggested classes:

```text
Application
Function
PersonalData
SensitiveData
ProcessingActivity
Purpose
Recipient
RetentionPolicy
User
UserRight
Consent
SecurityMeasure
PrivacyPolicy
PolicyClause
ExpectedData
DeclaredData
Overreach
Justification
Risk
```

Suggested relationships:

```text
performsFunction
requiresData
collectsData
usesDataFor
sharesDataWith
retainsDataFor
hasUserRight
hasPurpose
hasEvidence
hasJustification
```

---

# 16. RDF Representation Example

Conceptual representation:

```text
fdo:NavigationApp
    fdo:performsFunction fdo:Navigation .

fdo:Navigation
    fdo:requiresData fdo:Location .

fdo:NavigationApp
    fdo:collectsData fdo:Location .

fdo:NavigationApp
    fdo:collectsData fdo:Contacts .

fdo:NavigationApp
    fdo:sharesDataWith fdo:ServiceProvider .

fdo:Location
    fdo:hasPurpose fdo:NavigationService .
```

The privacy policy is therefore transformed from a document into interconnected knowledge.

---

# 17. Knowledge Graph — Neo4j

Neo4j can be used for graph storage, traversal, and visualization.

Conceptual structure:

```text
             [Application]
                  |
        performsFunction
                  |
                  v
             [Function]
                  |
             requiresData
                  |
                  v
            [PersonalData]
             /                 hasPurpose     sharedWith
          /                        v                 v
   [Purpose]          [Recipient]
```

The graph can be used to visualize relationships between applications, data, purposes, recipients, functions, and processing activities.

### Important architectural distinction

RDF/OWL and Neo4j serve different roles.

- **OWL/RDF**: formal semantic representation.
- **Neo4j**: graph-oriented storage, traversal, visualization and graph analysis.

For standards-compliant RDF/SPARQL/reasoning, **Apache Jena Fuseki** can provide the RDF/SPARQL layer.

The project should avoid maintaining two unrelated sources of truth. A canonical representation and controlled synchronization/export strategy should be defined.

---

# 18. Apache Jena Fuseki

Apache Jena Fuseki can provide an RDF dataset and SPARQL endpoint.

Conceptually:

```text
FDO OWL Ontology
        |
        v
    RDF Triples
        |
        v
Apache Jena / Fuseki
        |
        +---- SPARQL Queries
        |
        +---- Dataset Access
        |
        +---- Reasoning Integration
```

Fuseki enables semantic questions to be asked against the RDF representation.

---

# 19. SPARQL Queries

SPARQL is used to query the semantic knowledge.

### Query: What data does an application collect?

```sparql
SELECT ?data
WHERE {
    fdo:NavigationApp fdo:collectsData ?data .
}
```

### Query: What data does a function require?

```sparql
SELECT ?data
WHERE {
    fdo:Navigation fdo:requiresData ?data .
}
```

### Query: What collected data is not explicitly expected?

Conceptually:

```sparql
SELECT ?data
WHERE {
    fdo:NavigationApp fdo:collectsData ?data .
    FILTER NOT EXISTS {
        fdo:Navigation fdo:requiresData ?data .
    }
}
```

This creates an FDO candidate set for further analysis.

---

# 20. Reasoning Engine

Some conclusions are not explicitly stored as individual facts.

A reasoning engine can derive knowledge from ontology semantics and rules.

Possible technologies:
- Apache Jena reasoning;
- HermiT;
- Pellet.

Their exact role should be selected according to the OWL profile and reasoning requirements.

### Example

Explicit facts:

```text
Navigation
    requiresData
Location

NavigationApp
    performsFunction
Navigation

NavigationApp
    collectsData
Contacts
```

A semantic rule/query can support the conclusion:

```text
NavigationApp
    collects
Contacts

Contacts
    not required by identified Navigation function
```

This becomes an FDO candidate, which is then checked for policy justification.

---

# 21. HermiT / Pellet

HermiT and Pellet can be considered for OWL reasoning, consistency checking, and inference.

Their role differs from the LLM:

```text
LLM
 |
 +-- understands natural language
 +-- extracts candidate facts

OWL Reasoner
 |
 +-- applies ontology semantics
 +-- derives logical relationships
 +-- checks consistency
```

The strongest design is:

```text
AI for Language Understanding
+
Ontology for Formal Representation
+
Reasoner for Logical Inference
+
SPARQL for Querying
```

---

# 22. FDO Detection Engine

The FDO engine combines:

1. application functionality;
2. expected data;
3. declared data;
4. purposes;
5. policy justification;
6. recipients;
7. retention;
8. reasoning results.

Core logic:

```text
                APPLICATION
                     |
          +----------+----------+
          |                     |
          v                     v
    FUNCTIONAL MODEL       PRIVACY POLICY
          |                     |
          v                     v
    EXPECTED DATA          DECLARED DATA
          |                     |
          +----------+----------+
                     |
                     v
                  COMPARE
                     |
                     v
           FUNCTIONAL DATA GAP
                     |
                     v
             FDO CANDIDATE
                     |
                     v
          POLICY JUSTIFICATION
                     |
          +----------+----------+
          |          |          |
          v          v          v
       Explained  Undisclosed  Contradiction
```

---

# 23. Policy Justification Analysis

An unexpected data type should not automatically be labeled a privacy violation.

For every FDO candidate, examine whether the policy provides a purpose or justification.

Possible classifications:

### Expected
The data is reasonably associated with the application's identified functionality.

### Disclosed Overreach
The data appears unnecessary for the identified functionality, but the policy explicitly provides a purpose.

### Undisclosed Overreach
The data appears functionally unnecessary and the policy does not adequately explain why it is collected.

### Policy Contradiction
The structured evidence conflicts with another policy statement.

All classifications should retain the relevant policy evidence.

---

# 24. Explainable AI

The system should not only output:

```text
Privacy Risk = 81
```

Instead it should explain the result.

Example:

```text
Potential Functional Data Overreach Detected

Data:
Contacts

Application Function:
Navigation

Expected Requirement:
Location

Reason:
Contacts are not associated with the identified
primary navigation functionality.

Policy:
The policy declares collection of contacts.

Justification:
No clear purpose identified for navigation.

Classification:
Potential Undisclosed Functional Data Overreach

Risk:
High
```

The user should be able to trace the result to the relevant policy clause and semantic relationships.

---

# 25. Explainability Pipeline

```text
Policy Clause
     |
     v
Extracted Fact
     |
     v
Ontology Relationship
     |
     v
SPARQL / Reasoning Result
     |
     v
FDO Detection
     |
     v
Explanation Generator
     |
     v
Human-readable Explanation
```

---

# 26. Privacy Risk Scoring

Scoring is a downstream component, not the core contribution.

Possible dimensions:

```text
Functional Necessity
Transparency
Purpose Alignment
Third-party Sharing
Retention
User Control
Policy Consistency
```

The score should be described as:

> **An explainable analytical indicator derived from the project's defined criteria.**

It should not be presented as a legal certification or definitive judgment.

---

# 27. Data-Flow Visualization

The semantic graph can be used to visualize how data moves.

Example:

```text
USER
 |
 | provides
 v
[Location]
 |
 | collected by
 v
[Navigation App]
 |
 | used for
 v
[Navigation]
 |
 | shared with
 v
[Service Provider]
 |
 | retained for
 v
[Retention Period]
```

This makes privacy relationships understandable to users.

---

# 28. Application Comparison

Comparison is a secondary feature built on the common semantic model.

Instead of comparing raw privacy-policy text, the system compares structured privacy knowledge.

```text
                 PRIVACY COMPARISON
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
     APPLICATION A APPLICATION B APPLICATION C
          |             |             |
          +-------------+-------------+
                        |
                        v
              COMMON FDO ATTRIBUTES
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
   Data Collection  Data Sharing   User Rights
        |
        v
 Functional Necessity
        |
        v
 FDO / Risk Comparison
        |
        v
 COMPARISON REPORT
```

Because all applications are represented using the same ontology, their privacy information can be compared consistently.

---

# 29. Backend / API Architecture

The backend coordinates the system:

```text
Frontend
   |
   v
FastAPI
   |
   +-- Policy API
   +-- Application API
   +-- Analysis API
   +-- Ontology API
   +-- Knowledge Graph API
   +-- SPARQL Query API
   +-- Comparison API
   +-- Report API
```

Overall backend flow:

```text
Input
  |
  v
NLP / AI
  |
  v
Ontology Mapping
  |
  v
Knowledge Graph
  |
  v
SPARQL / Reasoning
  |
  v
FDO Analysis
  |
  v
Response
```

---

# 30. Suggested API Modules

## Policy API
- accepts PDF/URL/text;
- extracts policy text;
- stores policy metadata.

## NLP API
- clause segmentation;
- entity extraction;
- privacy fact extraction;
- purpose extraction;
- recipient extraction.

## Application Function API
- application classification;
- function extraction;
- expected data identification.

## Ontology API
- maps extracted concepts;
- validates ontology data;
- generates RDF/OWL representation.

## Knowledge Graph API
- stores graph information;
- retrieves relationships;
- supports graph traversal.

## SPARQL API
- semantic queries;
- expected-vs-declared data queries;
- privacy relationship queries.

## Reasoning API
- ontology inference;
- consistency checking;
- derived semantic relationships.

## FDO Analysis API
- functional gap detection;
- overreach classification;
- policy justification;
- risk generation.

## Comparison API
- application comparison;
- privacy attribute comparison;
- FDO comparison.

## Report API
- creates structured human-readable results.

---

# 31. Complete Technology Stack

| Layer | Technology | Role |
|---|---|---|
| Frontend | React / Next.js | User interface |
| UI | Tailwind CSS | Interface styling |
| Backend | Python | Core application logic |
| API | FastAPI | REST API |
| NLP | spaCy / Transformers | Text processing |
| AI | OpenAI API / Gemini API | Semantic extraction/classification |
| Embeddings | Sentence Transformers | Semantic similarity where required |
| Ontology | OWL | Formal semantic model |
| Knowledge Representation | RDF | Machine-readable triples |
| Semantic Query | SPARQL | Semantic querying |
| Graph Database | Neo4j | Graph storage/visualization |
| RDF/SPARQL Server | Apache Jena Fuseki | RDF dataset and SPARQL endpoint |
| Reasoning | Apache Jena / HermiT / Pellet | Inference and consistency |
| Relational DB | SQLite / PostgreSQL | Application/system records |
| ORM | SQLAlchemy | Relational database access |
| Visualization | React graph/chart libraries | Dashboard |
| Deployment | Docker | Environment/deployment consistency |

---

# 32. Storage Architecture

A practical system can use two storage layers.

## Relational database

SQLite/PostgreSQL can store:
- applications;
- analysis jobs;
- policy metadata;
- processing status;
- reports;
- system configuration.

## Semantic/graph layer

RDF/Neo4j can represent:
- applications;
- functions;
- personal data;
- purposes;
- processing;
- recipients;
- retention;
- rights;
- ontology relationships;
- derived knowledge.

This separates operational records from semantic knowledge.

---

# 33. Complete Working Example

Consider a navigation application.

### Application information

```text
Application:
Navigation App

Functions:
- Route planning
- Turn-by-turn navigation
- Nearby place discovery
```

### Expected data

```text
Location
```

### Privacy policy declares

```text
Collects:
- Location
- Device ID
- Contacts

Uses location for:
- Navigation
- Service improvement

Shares certain information with:
- Service providers
```

### NLP extracts

```text
Location -> Collect
Device ID -> Collect
Contacts -> Collect

Location -> Purpose -> Navigation
Location -> Purpose -> Service Improvement

Application -> SharesWith -> Service Provider
```

### Ontology representation

```text
NavigationApp
    performsFunction
        Navigation

Navigation
    requiresData
        Location

NavigationApp
    collectsData
        Location

NavigationApp
    collectsData
        DeviceID

NavigationApp
    collectsData
        Contacts
```

### FDO analysis

```text
Expected:
Location

Declared:
Location
Device ID
Contacts

Unexpected:
Device ID
Contacts
```

Suppose the policy explains Device ID for security but gives no clear purpose for Contacts.

Then:

```text
Device ID
    -> Additional collection with stated purpose

Contacts
    -> Potential Undisclosed Functional Data Overreach
```

The final report explains the evidence and reasoning.

---

# 34. Full End-to-End Architecture

```text
                         USER
                          |
                          v
              Upload Policy / Enter URL
                          |
                          v
                   FASTAPI BACKEND
                          |
                          v
                 POLICY EXTRACTION
                          |
                          v
                 CLAUSE SEGMENTATION
                          |
                          v
                  NLP + AI ANALYSIS
                          |
              +-----------+-----------+
              |                       |
              v                       v
       PRIVACY FACTS            APP FUNCTIONS
              |                       |
              v                       v
      DATA / PURPOSE /          EXPECTED DATA
      SHARING / RETENTION
              |                       |
              +-----------+-----------+
                          |
                          v
                    FDO MAPPING
                          |
                          v
                 OWL + RDF ONTOLOGY
                          |
                          v
                SEMANTIC KNOWLEDGE
                          |
             +------------+------------+
             |                         |
             v                         v
       JENA FUSEKI                 NEO4J
             |                         |
             v                         v
        SPARQL QUERIES          GRAPH ANALYSIS
             |                         |
             +------------+------------+
                          |
                          v
                  REASONING ENGINE
                          |
                          v
               FDO DETECTION ENGINE
                          |
                          v
              POLICY JUSTIFICATION
                          |
                          v
                 RISK / EXPLANATION
                          |
                          v
                 REPORT / DASHBOARD
                          |
                          v
                         USER
```

---

# 35. Major Project Modules

## Module 1 — Policy Acquisition
Input:
- PDF;
- URL;
- text.

Output:
- normalized policy text.

## Module 2 — NLP Processing
Output:
- clauses;
- entities;
- candidate privacy facts.

## Module 3 — AI Semantic Extraction
Output:
- data;
- purpose;
- processing;
- recipients;
- retention;
- rights;
- consent;
- evidence.

## Module 4 — Application Function Analysis
Output:
- application category;
- functions;
- expected data.

## Module 5 — FDO Ontology
Defines the semantic vocabulary and relationships.

## Module 6 — RDF/OWL Representation
Converts extracted facts into machine-readable semantic triples.

## Module 7 — Knowledge Graph
Stores and visualizes connected privacy information.

## Module 8 — SPARQL Query Layer
Answers semantic questions from the graph.

## Module 9 — Reasoning Engine
Derives implicit information and checks consistency.

## Module 10 — FDO Detection Engine
Compares expected and declared data.

## Module 11 — Policy Justification Engine
Determines whether unexpected processing is explained.

## Module 12 — Explainable Risk Engine
Produces evidence-backed privacy analysis.

## Module 13 — Comparison Engine
Compares applications using the common ontology.

## Module 14 — Dashboard
Displays:
- privacy data;
- data flow;
- expected data;
- declared data;
- FDO candidates;
- explanations;
- comparison;
- recommendations.

---

# 36. What the User Ultimately Sees

The complicated technical pipeline stays behind the scenes.

Example:

```text
APPLICATION: Navigation App

FUNCTION:
Navigation

EXPECTED DATA:
✓ Location

DECLARED DATA:
✓ Location
✓ Device ID
⚠ Contacts

FUNCTIONAL DATA OVERREACH:
Contacts

WHY?
Contacts are not associated with the identified
primary navigation function.

POLICY JUSTIFICATION:
No clear purpose identified.

CLASSIFICATION:
Potential Undisclosed Overreach

EVIDENCE:
Relevant privacy-policy clause

RISK:
High

RECOMMENDATION:
Review whether contact collection is necessary
for the stated navigation functionality.
```

---

# 37. What Makes the Project Innovative

The project should not claim that privacy policies, LLMs, or knowledge graphs have never been used before.

The proposed contribution is the combination of:

### 1. Functional perspective
Relating data collection to application functionality.

### 2. Formal semantic representation
Defining an FDO ontology using OWL/RDF.

### 3. AI-to-ontology pipeline
Using NLP/LLMs to transform natural-language privacy statements into structured semantic facts.

### 4. Knowledge graph representation
Connecting data, purposes, processing, recipients, retention and rights.

### 5. Machine reasoning
Using SPARQL and ontology reasoning to query and derive privacy knowledge.

### 6. Functional Data Overreach detection
Comparing expected data requirements against declared data practices.

### 7. Explainability
Providing the evidence and reasoning behind detected overreach instead of an unexplained score.

---

# 38. What the Project Is NOT

### Not simply a privacy-policy summarizer
A summarizer tells users what the policy says. FDO Privacy additionally models relationships and performs semantic analysis.

### Not a consent management system
The project is not primarily responsible for managing acceptance/consent.

### Not a runtime behavior monitor
The project primarily analyzes declared privacy information and functional expectations rather than claiming to observe actual runtime behavior.

### Not a legal compliance certification system
The system provides analytical results and should not be presented as a legal determination.

### Not simply a privacy-score generator
The score is a downstream result. The core contribution is the semantic representation and functional analysis behind it.

---

# 39. Research Contribution Structure

```text
Layer 1
NATURAL LANGUAGE UNDERSTANDING
        |
        v
Layer 2
FUNCTIONAL DATA ONTOLOGY
        |
        v
Layer 3
KNOWLEDGE GRAPH + REASONING
        |
        v
Layer 4
FUNCTIONAL DATA OVERREACH ANALYSIS
```

### Layer 1
Convert natural-language policies into structured candidate facts.

### Layer 2
Define a formal vocabulary and relationships.

### Layer 3
Represent and reason over the knowledge.

### Layer 4
Use the knowledge to detect functional mismatch and explain results.

---

# 40. Dataset / Benchmark

A practical benchmark can contain applications from:
- Communication;
- Social Media;
- Navigation;
- Banking/Finance;
- Shopping;
- Healthcare;
- Streaming;
- Productivity;
- Games;
- Utilities.

For every application, record:

```text
Application
Category
Description
Functions
Privacy Policy
Extracted Data
Expected Data
Purposes
Recipients
Retention
User Rights
FDO Label
Justification Label
Evidence Clause
```

A manually reviewed subset should act as the ground-truth benchmark.

---

# 41. Evaluation Plan

## NLP evaluation
Measure:
- Precision;
- Recall;
- F1-score.

For:
- data extraction;
- purpose extraction;
- recipient extraction;
- processing classification.

## Ontology evaluation
Evaluate:
- consistency;
- coverage;
- competency questions;
- relationship correctness.

## FDO detection evaluation
Use manually labeled expected/declared data and FDO classifications.

Measure:
- Accuracy;
- Precision;
- Recall;
- F1-score.

## Reasoning evaluation
Test whether the reasoning layer correctly derives expected relationships and identifies ontology inconsistencies.

## Explainability evaluation
Evaluate whether users can understand:
- why data was considered unexpected;
- which policy evidence supports the result;
- how the reasoning reached the conclusion.

---

# 42. Development Roadmap

## Phase 1
Application and policy data model.

## Phase 2
Policy extraction and clause segmentation.

## Phase 3
NLP/AI extraction.

## Phase 4
Initial FDO OWL/RDF ontology.

## Phase 5
Expected-data/function ontology.

## Phase 6
RDF knowledge graph and SPARQL queries.

## Phase 7
Neo4j graph visualization/storage where required.

## Phase 8
Reasoning using Apache Jena and evaluation of HermiT/Pellet where needed.

## Phase 9
FDO detection and policy justification.

## Phase 10
Explainable dashboard and comparison.

## Phase 11
Benchmark evaluation and research analysis.

---

# 43. Recommended Minimum Viable Research System

If implementation time is limited, prioritize:

```text
Privacy Policy
      |
      v
NLP / LLM Extraction
      |
      v
FDO OWL/RDF Ontology
      |
      v
Expected Data Mapping
      |
      v
Knowledge Graph
      |
      v
SPARQL
      |
      v
FDO Detection
      |
      v
Explainable Report
```

Advanced Neo4j visualization, advanced reasoning, and comparison can be added after the core semantic pipeline works.

The core research contribution should not be sacrificed merely to include more technologies.

---

# 44. One-Line Explanation

> **FDO Privacy converts natural-language privacy policies into machine-readable semantic knowledge and uses application functionality, ontology relationships, graph queries, and reasoning to analyze whether data practices match their functional purpose and to explain potential Functional Data Overreach.**

---

# 45. One-Minute Viva Explanation

> "Our project addresses the problem that privacy information is usually available as long natural-language policies. These policies are difficult not only for users to understand but also for machines to interpret and reason about.
>
> We propose a Functional Data Ontology, or FDO, to represent privacy information in a structured form. We use NLP and an AI API to extract information such as what data is collected, why it is collected, how it is processed, who it is shared with, how long it is retained, and what rights the user has.
>
> At the same time, we analyze the application's functionality to determine what data is reasonably expected for that functionality. We represent both functional requirements and privacy-policy information using OWL/RDF and a knowledge graph.
>
> Using SPARQL and reasoning, we can query and derive relationships from this knowledge. This enables Functional Data Overreach analysis by comparing expected data with declared data and then checking whether unexpected collection is justified or disclosed.
>
> Finally, the system provides an explainable report showing the data involved, its purpose, relevant policy evidence, detected mismatch, and reasoning behind the result.
>
> So our project is not simply a privacy-policy summarizer. The main idea is to convert privacy information from unstructured text into structured semantic knowledge that both humans and machines can understand, query, compare, and reason about."

---

# 46. Final Concept

```text
                    PRIVACY POLICY
                          |
                          v
                  NATURAL LANGUAGE
                          |
                          v
                    NLP + AI API
                          |
                          v
                  PRIVACY FACTS
                          |
                          v
                FDO ONTOLOGY
                  OWL + RDF
                          |
                          v
                KNOWLEDGE GRAPH
                Neo4j / RDF Store
                          |
              +-----------+-----------+
              |                       |
              v                       v
          SPARQL                 REASONING
              |                       |
              +-----------+-----------+
                          |
                          v
             FUNCTIONAL ANALYSIS
                          |
              +-----------+-----------+
              |                       |
              v                       v
       EXPECTED DATA            DECLARED DATA
              |                       |
              +-----------+-----------+
                          |
                          v
                  FDO DETECTION
                          |
                          v
              POLICY JUSTIFICATION
                          |
                          v
                EXPLAINABLE RESULT
                          |
                          v
                USER UNDERSTANDING
```

## Central message

> **Privacy information should not remain trapped inside lengthy natural-language documents. FDO Privacy converts that information into structured semantic knowledge, connects it with application functionality, and enables automated querying, reasoning, functional overreach detection, visualization, comparison, and explainable privacy analysis.**
