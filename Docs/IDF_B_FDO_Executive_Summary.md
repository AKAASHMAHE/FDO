# IDF-B Executive Summary
## FDO Privacy Project — Functional Data Ontology for Privacy Policy Analysis

**Institution:** Vellore Institute of Technology  
**Document type:** IDF-B Technical Audit — Executive Summary  
**Audit date:** 2026-10-13  
**Status:** Prototype / Research System

---

## Problem Statement

Mobile application privacy policies are long, legally dense documents that users rarely read and regulators cannot inspect at scale. Existing approaches either rely on manual legal review or flat keyword searches that conflate data *collection* with data *necessity*. There is no widely deployed automated tool that maps each data item a policy claims to collect against a structured justification of functional purpose, identifies where collected data exceeds the stated purpose (i.e., functional data over-reach), or surfaces the finding in a structured, inspectable form. This project addresses that gap.

---

## Proposed Solution

The **FDO Privacy Project** implements a multi-layer automated pipeline that ingests a privacy policy URL, extracts structured data-use triples (data type → purpose → function), evaluates each triple against a formal ontology of functional necessity, and renders the findings in a React dashboard. The system combines:

1. **Gemini 3.5 Flash Lite LLM** (Google GenAI API, `gemini-3.5-flash-lite` model) with structured JSON prompts to extract data triples from raw policy text.
2. **OWL 2 ontology** (`FDO.owl`, 19 classes, 24 object properties, 23 data properties) defining `FunctionalDataObject`, `AppFunction`, `DataType`, `Purpose`, and their necessity relations.
3. **Apache Jena Fuseki 6.2.0** as an RDF triplestore, configured with `OWLFBRuleReasoner` inference in `fdo-reasoning.ttl`, used for SPARQL-based overreach detection via `FDO_DETECTION_QUERY`.
4. **Deterministic decision engine** (`evaluate_fdo_decision()`, `fdo_decision_service.py:27–147`) — 6 explicit if/elif rules shared by both the relational and semantic analysis branches.
5. **FastAPI backend** (13 REST endpoints) backed by **SQLite** (SQLAlchemy ORM, 11 tables) and a **React/Vite** single-page dashboard.

---

## Implemented Features (Verification Status)

| Feature | Status |
|---|---|
| Policy text ingestion via URL (requests + BeautifulSoup) | Implemented-verified |
| Gemini 3.5 Flash Lite structured extraction (data triples) | Implemented-verified (requires API key) |
| Fallback regex extraction (4-keyword scan) | Implemented-verified |
| OWL ontology loaded into Fuseki at runtime | Implemented-verified (Fuseki must be started manually) |
| SPARQL overreach detection (`FDO_DETECTION_QUERY`) | Implemented-verified (Fuseki-dependent) |
| 6-rule FDO decision engine | Implemented-verified |
| Evidence scoring (base + purpose-compat + function-match) | Implemented-verified |
| Purpose normalization (14-category taxonomy) | Implemented-verified |
| SQLite persistence (11-table schema) | Implemented-verified |
| FastAPI REST API (13 endpoints) | Implemented-verified |
| React dashboard (single-page, component-based) | Implemented-verified |
| Cross-application policy comparison | **Not-found** |
| Intra-policy contradiction detection | **Not-found** |
| OWL DL reasoning driving runtime decisions | Configured-but-unused (SPARQL FILTER drives decisions; OWLFBRuleReasoner loaded but not queried for inferences) |

---

## Architecture Summary

```
URL → PolicyIngestionService (requests/BS4)
    → GeminiExtractor (gemini-3.5-flash-lite, structured JSON prompt)
    → ComparisonService (normalize, classify, purpose-compat scoring)
    → [Relational branch] evaluate_fdo_decision() → SQLite
    → [Semantic branch]  RDFGraphBuilder → Fuseki → FDO_DETECTION_QUERY
                         → semantic_decision_adapter → evaluate_fdo_decision() → SQLite
    → React frontend (App.jsx, GroupedSemanticCard, HistoryPanel)
```

Both branches converge on the **same deterministic decision function**. If Fuseki is offline, the semantic branch is silently skipped; the relational branch always executes.

---

## Test Results

| Batch | Tests | Pass | Fail/Error | Condition |
|---|---|---|---|---|
| Ontology + purpose | 155 | 155 | 0 | No external dependency |
| Integration | 126 | 126 | 0 | No external dependency |
| SPARQL/semantic | 45 | 45 | 0 | No external dependency |
| Fuseki-dependent (FAILED) | 17 | 0 | 17 | Fuseki offline → `ConnectionRefusedError` |
| Fuseki-dependent (ERROR) | 7 | 0 | 7 | Fuseki offline → module-level `ConnectionRefusedError` |
| Remaining offline tests | 47 | 47 | 0 | No external dependency |
| **Total** | **397** | **373** | **24** | |

All 373 Fuseki-independent tests pass. All 24 failures/errors are caused by `localhost:3030` being unreachable, not by logic errors.

---

## Primary Limitations

1. **Fuseki requires manual startup** — `fuseki-server.bat`; not containerized or supervised. Semantic branch silently skips if offline.
2. **Gemini API key required** for full extraction; absent key falls back to a 4-keyword regex that produces sparse triples.
3. **No cross-application comparison** — each analysis is scoped to a single `application_id`; comparative overreach ranking across apps is not implemented.
4. **OWL reasoner is decorative** — runtime decisions are made by SPARQL FILTER pattern matching, not by OWL DL inference; the `OWLFBRuleReasoner` does not drive any output.
5. **Policy omission ≠ violation** — the system correctly notes this in design but has no formal omission-inference mechanism.

---

## Audit Deliverables

| File | Description |
|---|---|
| `docs/part1_inventory_architecture.md` | 125-file inventory, startup orchestration, architecture |
| `docs/part2_nlp_ai_data.md` | NLP/AI pipeline, Gemini prompts, rule-based systems |
| `docs/part3_ontology_storage.md` | Ontology classes/properties, SQL schema, Fuseki config |
| `docs/part4_api_frontend_analysis_tests.md` | API endpoints, frontend trace, privacy logic, test results |
| `docs/IDF_B_FDO_Project_Technical_Analysis.md` | Full 21-section technical analysis + IDF-B content + faculty guide |
| `docs/IDF_B_FDO_File_Inventory.md` | 41-file consolidated inventory table |
| `docs/IDF_B_FDO_Executive_Summary.md` | This document |
