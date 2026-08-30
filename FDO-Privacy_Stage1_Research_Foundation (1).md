# FDO-Privacy: An Explainable AI Framework for Detecting Functional Data Overreach in Privacy Policies

## Stage 1 — Research Foundation (Research & Problem Definition)

---

## Part 1. Problem Definition

### 1.1 The core problem

Privacy policies are the primary legal artifact through which organizations disclose what personal data they collect, why, and with whom it is shared. Large-scale empirical work shows that policies are long, legally dense, and poorly read: readability studies consistently place average privacy policies above a college reading level, and behavioral studies estimate that only a small fraction of users ever read them (commonly cited figures are in the low single digits of percent). This "notice-and-consent" model is widely regarded in the literature as failing in practice, which is precisely why the last decade has produced a large body of work on *automated* privacy-policy analysis (summarization, extraction, contradiction detection, risk scoring).

However, nearly all of this automated-analysis literature treats the privacy policy as a **closed, self-referential text**: the object of analysis is the policy alone (Is it readable? Is it internally consistent? Does it disclose category X? Does it match a taxonomy of "data practices"?). Very little of it asks a logically prior question: *given what the application actually does, how much of the disclosed collection is even plausible?* This is the gap FDO-Privacy targets.

### 1.2 Why summarization is insufficient

Automated summarization and information-extraction systems (e.g., readability/extraction toolsets, PI-Extract-style annotators, PolicyIE-based intent/slot classifiers) make policies shorter and more digestible, but they inherit the policy's own framing. A summary of "we collect location data to provide personalized services" is faithfully extracted regardless of whether the underlying app is a flashlight utility or a navigation app. Summarization improves *comprehension* of what is stated; it does not evaluate whether what is stated is *functionally justified*. This distinction — comprehension vs. justification — is central to the FDO-Privacy problem statement.

### 1.3 What is missing from existing approaches

Reviewing the major automated-analysis lineages (Part 4) reveals three structurally under-addressed questions:

1. **Cross-referencing declared collection against expected functional need.** Existing systems either analyze the policy text alone (readability, extraction, contradiction detection) or analyze app behavior alone (static/dynamic taint analysis of code), or cross-reference *behavior* against *disclosure* (flow-to-policy consistency, e.g., PoliCheck). None of the mainstream lines systematically ask whether the *category of application* justifies the *category of data* being collected, independent of whether that collection is disclosed or technically executed.
2. **Policy justification quality, not just presence.** Several systems detect whether a practice is disclosed (extraction) or whether disclosures are internally contradictory (PolicyLint) or inconsistent with observed flows (PoliCheck). Few systems evaluate whether a disclosed purpose statement is a *substantively adequate justification* for the specific data type, as opposed to a generic boilerplate purpose clause ("to improve our services").
3. **Explainable, decomposed reasoning over a single score.** A large family of privacy-scoring and privacy-rating systems (see Part 4.7) reduce a policy to a single numeric or categorical rating. This is useful for at-a-glance comparison but does not tell a user, developer, or auditor *which specific data item is problematic and why*.

### 1.4 Why functional necessity matters

Data-protection law itself is built around a similar idea: GDPR Article 5(1)(c) (data minimization) and Article 5(1)(b) (purpose limitation) require that personal data be "adequate, relevant and limited to what is necessary" for the stated purpose. Operationalizing these legal principles computationally is recognized in the literature as difficult and is only partially attempted — for example, prior design-science work on GDPR compliance in continuous-integration pipelines explicitly *declined* to operationalize purpose limitation because it was judged too subjective, while still attempting data minimization. Separately, information-retrieval research on personalization systems (Biega et al., SIGIR 2020) proposed formal operationalizations of data minimization for ranking/recommendation systems specifically, showing that "necessity" can be given a working definition in narrow domains, but this has not been generalized to arbitrary consumer applications and privacy-policy text. The mobile-security literature offers the closest structural analogue: WHYPER, AutoCog and their successors operationalize "does the app description justify the requested permission?" as a description-to-permission fidelity problem. FDO-Privacy generalizes this same intuition — comparing a functional specification of an application to its resource/data demands — from *coarse-grained OS permissions* to *fine-grained personal-data categories described in privacy policies*, and adds an explicit policy-justification layer on top.

### 1.5 Why explainability matters more than a single score

Numeric privacy-rating systems and privacy-risk-scoring frameworks (e.g., commercial-style automated rating patents, ML-based privacy indicator frameworks evaluated over tens of thousands of Play Store apps) demonstrate that scoring at scale is feasible, but the explainable-AI-for-privacy literature (e.g., work built around the PRISMe interactive assessment tool) argues that opaque scores do not build user trust or actionable understanding, and can be gamed by policy authors who optimize wording rather than practice once they know the scoring heuristics. For FDO-Privacy, whose stated purpose includes helping developers and reviewers understand *why* a specific data item is flagged, a single aggregate score is an inadequate deliverable; the framework needs per-item, per-claim explanations (Purpose–Collection Gap Analysis, Policy Justification Analysis) that a human can audit, which is also more consistent with regulator and auditor use cases described in the PolicyLint/PoliCheck line of work.

### 1.6 Research gap this project addresses

The research gap is not "no one analyzes privacy policies with NLP/LLMs" — that field is mature and crowded. The gap is specifically: **no widely validated framework systematically operationalizes functional necessity as a first-class analytical layer sitting between "what the app does" and "what the policy discloses," and pairs a resulting overreach detection with (a) a policy-justification classification and (b) explainable, item-level reasoning, rather than either a document-only analysis or a black-box score.** Part 4 and Part 6 substantiate this claim against the literature found.

### 1.7 Distinguishing key concepts

| Concept | Definition | Object of analysis |
|---|---|---|
| **Privacy policy transparency** | Whether a policy discloses its practices clearly and is findable/readable by users. | The text alone. |
| **Policy compliance** | Whether the policy (and/or organizational practice) satisfies a specific legal regime (GDPR, CCPA, COPPA, etc.). | The text and/or practice, against a legal standard. |
| **Runtime behavior** | What the application's code actually does at execution time (data flows, API calls, network transmissions). | The application binary/traffic, independent of any text. |
| **Data minimization** | The legal/ethical principle that only necessary data should be collected for a stated purpose. | A normative constraint, typically legally defined. |
| **Functional necessity** | Whether a specific data item is plausibly required to deliver a specific declared application function. | A relationship between app functionality and a data item — the analytical primitive FDO-Privacy introduces operational tooling for. |
| **Functional Data Overreach (FDO)** | The condition where declared/collected data exceeds what is functionally necessary for the app's primary functionality, evaluated together with whether that excess is adequately justified in the policy. | A derived judgment combining functional necessity assessment with policy justification assessment. |

FDO-Privacy is explicitly scoped to the **declared-collection vs. expected-functional-need** relationship and the **quality of stated justification**, not to runtime verification or legal compliance determination (see Part 8, Scope).

---

## Part 2. Research Question

### 2.1 Evaluation of the proposed research question

> "Can AI automatically detect functionally unnecessary data collection by comparing an application's expected data requirements with its declared privacy practices and provide explainable privacy overreach analysis?"

This question is directionally sound and preserves the project's central idea, but as written it conflates three distinct sub-claims (feasibility of detection, feasibility of comparison, feasibility of explainability) into a single yes/no question, which is difficult to operationalize into a measurable research design. It also does not name the mechanism (LLM/NLP reasoning) or the evaluation criterion (against what ground truth?).

### 2.2 Refined Primary Research Question

> **To what extent can an AI-based framework automatically identify Functional Data Overreach — data collection that exceeds an application's inferred functional requirements — by jointly modeling expected data requirements derived from application functionality and declared data practices extracted from privacy policies, and produce explainable, per-item justifications for its determinations that are usable by end users, developers, and auditors?**

This preserves the original intent (comparison of expected vs. declared, explainability) while making the object of measurement explicit: detection accuracy against ground truth, and explanation quality against human judgment.

### 2.3 Secondary Research Questions

1. **(Data extraction)** How accurately can data-collection statements — data type, purpose, entity (first-/third-party), and sharing/retention conditions — be extracted from privacy-policy text using NLP/LLM pipelines, relative to existing extraction baselines (e.g., PoliGraph-er, PI-Extract, PolicyIE-based classifiers)?
2. **(Functional data requirements)** How can the "expected data" required for a given application's primary and secondary functions be systematically derived (e.g., from app descriptions, functional categories, feature taxonomies) with acceptable inter-annotator/inter-model agreement, given that "necessity" is inherently context-dependent?
3. **(FDO detection)** How effectively can a functional-necessity comparison model classify individual declared data items into overreach categories (expected / disclosed-overreach / undisclosed-overreach / contradiction), compared to human-annotated ground truth?
4. **(Policy justification)** How well can a classifier distinguish substantively adequate purpose justifications from generic/boilerplate justifications for a specific flagged data item?
5. **(Explainability & evaluation)** Do the framework's generated explanations improve human (user/developer/auditor) understanding of, trust in, and ability to act on FDO findings, relative to an unexplained score-only baseline, and how consistent/faithful are the explanations relative to the underlying classification?

---

## Part 3. Research Objectives

1. **Develop** a formal conceptual model of Functional Data Overreach that relates application functionality, expected data requirements, and declared/collected data.
2. **Design** an ontology/taxonomy for representing application functions, data types, purposes, and entities suitable for automated reasoning (extending, not duplicating, existing privacy-policy ontologies such as PoliGraph and CCPA-derived data taxonomies).
3. **Extract** structured data-practice statements (data type, purpose, entity, sharing, retention) from privacy-policy text using NLP/LLM techniques, benchmarked against existing extraction tools.
4. **Identify** the expected functional data requirements of a given application from its functional description/category, producing a machine-usable expected-data profile.
5. **Compare** expected data requirements against declared/collected data to compute a Purpose–Collection Gap for each data item.
6. **Classify** each flagged data item into an overreach category (expected, disclosed overreach, undisclosed overreach, policy contradiction) using a Policy Justification Analysis stage.
7. **Detect** FDO instances at the application level and produce a multi-dimensional, explainable privacy-risk representation (not a single opaque score).
8. **Evaluate** the framework's extraction accuracy, classification accuracy, and explanation quality against human-annotated ground truth and existing baselines, and report system performance/scalability.

---

## Part 4. Literature Review

The review below groups prior work into the streams named in the assignment. It is drawn from IEEE/ACM/USENIX/Springer/Elsevier/arXiv sources located during this stage; where only a single non-peer-reviewed or industry source was found, that is noted explicitly.

### 4.1 Privacy-policy analysis: field-level surveys

A 2024 ACM Computing Surveys systematic review of the privacy-policy literature found that a large share of the reviewed corpus (reported as roughly 42% of ~86 relevant papers in that review) uses ML/NLP/DL techniques for some form of automated analysis, spanning summarization, ontology extraction, and violation detection pipelines. The review describes a common architecture for automated violation-detection work: build/derive an ontology mapping policy phrases to data-practice tuples, extract policy-side tuples (entity, action, data type), separately extract code/traffic-side tuples via static or dynamic analysis, then compare the two tuple sets for inconsistency. This architecture is the closest existing structural template to FDO-Privacy's comparison step, but its two sides are *policy text* and *actual code behavior* — not *policy text* and *inferred functional necessity*. An earlier (2022) Springer systematic mapping study of automated privacy-policy analysis similarly finds the field organized around law compliance, system-behavior checking, and user-information goals, and explicitly notes (as of its writing) the absence of prior mapping studies at the intersection of privacy-policy analysis and text-analysis methods — indicating the field was still consolidating as of that survey.

### 4.2 Automated summarization and information extraction

Early large-scale readability work (e.g., Fabian et al.'s analysis of tens of thousands of policies using Flesch–Kincaid metrics) established the empirical motivation for automation: policies are reliably difficult to read. Extraction-focused systems such as PI-Extract use neural models to identify and annotate specific data-practice statements, with associated user studies showing that surfacing annotated practices improves reader comprehension. PolicyIE-derived work frames extraction as intent classification and slot filling over policy sentences. These systems answer "what does the policy say" with increasing structure and accuracy but do not evaluate the *plausibility* of what is said relative to the application's function.

### 4.3 Knowledge-graph representations of privacy policies

PoliGraph (Cui, Trimananda, Markopoulou & Jordan, USENIX Security 2023) is the most directly relevant knowledge-graph precedent. It represents an entire privacy policy — not isolated sentences — as a knowledge graph of relations between policy-text elements, built via the PoliGraph-er NLP pipeline, which the authors report identifies substantially more collection statements than prior sentence-level state of the art (a 40% increase in the reported evaluation) at high precision (~97%). PoliGraph's applications include revealing cross-policy patterns, checking term correctness, detecting internal contradictions (finding false alarms in prior contradiction-detection work), and analyzing consistency between the policy and observed network traffic. PoliGraph's methodology (whole-document graph construction, purpose-phrase classification) is directly reusable for FDO-Privacy's data-extraction and Privacy Knowledge Graph objectives, but PoliGraph does not model application functionality or evaluate functional necessity; its "consistency" analysis is policy-vs-traffic, not policy-vs-function.

### 4.4 Contradiction and flow-to-policy consistency analysis

PolicyLint (Andow et al., USENIX Security 2019) formalized detection of *internal* contradictions in a single policy by jointly modeling negation and semantic hierarchy of data objects/entities, applying automatically generated ontologies to a large corpus (over 11,000 apps), and finding a non-trivial fraction of policies (reported ~14%) contain apparent contradictions, many traced on manual review to misleading presentation or auto-generated boilerplate templates. PoliCheck (Andow et al., USENIX Security 2020) extended this line by formalizing an *entity-sensitive* flow-to-policy consistency model, correcting prior work's failure to distinguish first-party from third-party data recipients when comparing declared practices against actual observed data flows (obtained via dynamic/network analysis). Both systems are squarely about **disclosure correctness** (does the text contradict itself, does the text match observed behavior) rather than about whether the disclosed/observed collection is functionally warranted in the first place. FDO-Privacy's "Policy Contradiction" class (Part 10) is directly informed by PolicyLint's contradiction formalism, but is repositioned as one branch of a broader overreach taxonomy rather than the sole object of analysis.

### 4.5 Functional/description-to-permission fidelity (closest conceptual precedent)

This is the most important precedent for the FDO concept, even though it originates in mobile-security rather than privacy-policy research. WHYPER (Pandita et al., USENIX Security 2013) used NLP to find app-description sentences that justify a requested Android permission. AutoCog (Qu et al., ACM CCS 2014) formalized this as "description-to-permission fidelity," using learned models to flag permissions not evidenced by the app's natural-language description, reporting high precision/recall (~92–93%) across evaluated permissions and demonstrating the problem's severity at scale (tens of thousands of apps). Stowaway (Felt et al.) independently found roughly one-third of a studied app sample requested more permissions than used ("overprivileged"), establishing empirically that overreach is common. TKPERM extended this line with cross-platform knowledge transfer to generalize permission-necessity inference beyond hand-labeled permission/keyword sets, and recent (2025) work has begun applying LLMs directly to the permission-fidelity classification task, reporting improvements over the WHYPER/AutoCog/AC-Net baselines. **This entire line validates the core mechanic FDO-Privacy proposes — comparing a natural-language functional specification against a resource/data demand and flagging unjustified excess — but it operates over coarse, fixed OS permission categories (e.g., READ_CONTACTS) and app-store short descriptions, not over the fine-grained personal-data categories, purposes, and third-party sharing terms found in full privacy policies.** No system identified in this review extends description-to-permission-style fidelity checking to privacy-policy-declared data collection with an explicit functional-necessity model; this is a defensible, evidence-grounded piece of the research gap.

### 4.6 Data minimization and purpose limitation as computational targets

The GDPR's data-minimization (Art. 5(1)(c)) and purpose-limitation (Art. 5(1)(b)) principles are the closest legal analogues to "functional necessity," and multiple sources confirm these principles are recognized as legally central but difficult to operationalize. Design-science work on integrating GDPR checks into software CI pipelines explicitly chose to operationalize data minimization while *declining* to operationalize purpose limitation, citing its subjectivity — direct evidence that automated necessity/purpose reasoning is considered a hard, only partially solved problem in the requirements-engineering literature, not a settled one. In a narrower domain, Biega et al. (SIGIR 2020) formalized data minimization specifically for personalization/ranking systems, giving one of the few concrete computational operationalizations of "necessity" in the literature, but restricted to a single application class (recommenders), not general consumer apps or policy text. More recent (2025–2026) industry-oriented material on LLM/RAG privacy compliance discusses purpose limitation and minimization as design constraints on retrieval pipelines themselves (e.g., constraining RAG context to task-relevant data), which is a related but distinct problem — protecting data *used by* an LLM system, not evaluating whether an *arbitrary third-party app's declared collection* is necessary for its function. This confirms functional-necessity-of-collection (FDO-Privacy's target) is not the same problem as data-minimization-in-AI-pipelines (a currently more actively discussed but distinct 2025–2026 topic).

### 4.7 Privacy risk scoring and rating

Multiple lines produce a privacy score/rating from policy text: ML-based hierarchical classifiers producing standardized "privacy indicators" evaluated over 10,000+ Play Store apps and policies; risk-calculation approaches combining probability/consequence modeling with ontology-based policy analysis; and patented commercial methods that assign risk levels to detected keywords/phrases and difference them across policy versions to produce a rating and change-monitoring signal. These systems demonstrate feasibility of large-scale automated scoring but converge on a single aggregate output (a rating, a score, a risk level) rather than a decomposed, per-item, explainable judgment, and generally do not incorporate a functional-necessity comparison — they score what is disclosed, not whether it is warranted.

### 4.8 Explainable AI for privacy

The explainable-AI-for-privacy literature is comparatively young. PRISMe (discussed in a 2025 arXiv paper on explainable AI in usable privacy/security) is an interactive privacy-policy assessment tool using an LLM-as-judge architecture with a chat interface, evaluated in a 22-participant user study examining user understanding and awareness. This line explicitly identifies tensions this project must anticipate: (a) a trade-off between explanation transparency and adversarial robustness — if scoring heuristics are made fully transparent, policy authors can game wording without changing practice; and (b) a trade-off between explanation personalization and privacy (personalized explanations may themselves require processing sensitive user data). These are directly relevant threats to validity for FDO-Privacy's explainability objective (Part 14).

### 4.9 Knowledge graphs / GraphRAG for regulatory and privacy compliance

Recent (2024–2025/2026) work extends knowledge-graph and RAG techniques specifically to *regulatory compliance verification* rather than plain policy summarization: PrivComp-KG combines an LLM (via RAG) with a GDPR-derived knowledge graph to align policy text to specific GDPR articles and run rule-based (SWRL) compliance checks; GraphCompliance aligns a policy graph and a context graph for LLM-based regulatory compliance reasoning, explicitly noting that most prior systems operate on isolated text segments without cross-article reference tracking; related work links Android code behavior to privacy requirements, and other work benchmarks LLM-based extraction/conformance checking against GDPR text. Separately, PoliAnalyzer (2025) uses an LLM-driven NLP pipeline (built on the PolicyIE information schema) to convert privacy-policy text into a formal, queryable representation supporting personalized, user-preference-based analysis at scale. **This 2024–2026 cluster shows the field is actively moving toward LLM+KG/RAG architectures for structured privacy/compliance reasoning — methodologically supporting FDO-Privacy's proposed Privacy Knowledge Graph and GraphRAG-style approach — but all of it remains policy-text-centric (aligning text to regulation) rather than functionality-centric (aligning text to what the application needs to do).** This further supports, rather than undermines, the claimed gap.

### 4.10 Summary of the literature stream

Across all ten sub-areas, the review consistently finds: mature and increasingly LLM-based extraction/summarization; mature contradiction/consistency checking (policy-vs-policy, policy-vs-traffic); an established but narrow functional-fidelity precedent confined to OS permissions; partially solved computational treatments of data minimization limited to specific domains; mature but explainability-poor scoring systems; an emerging but small explainable-AI-for-privacy literature; and a fast-growing 2024–2026 cluster of KG/GraphRAG approaches applied to regulatory-text alignment rather than functional necessity. No system found integrates a functional-necessity comparison for privacy-policy-declared data with an explicit, multi-class policy-justification analysis and item-level explainability. This supports — with appropriate caution about the limits of any literature search — the claimed research gap.

---

## Part 5. Existing-System Comparison

| Existing Approach | Privacy Policy Analysis | Data Extraction | Functional Necessity | Overreach Detection | Policy Justification | Explainability | Knowledge Graph |
|---|---|---|---|---|---|---|---|
| WHYPER (2013) | No (app description, not full policy) | Partial (permission-relevant sentences) | **Yes** (description-to-permission) | Partial (permission mismatch) | No | Limited (sentence evidence) | No |
| AutoCog (2014) | No (app description) | Partial | **Yes** (description-to-permission fidelity) | **Yes** (flags unwarranted permissions) | No | Limited | No |
| TKPERM (2020) | No | Partial | **Yes** (transferable) | **Yes** | No | Limited | No |
| PolicyLint (2019) | **Yes** | **Yes** (entity/data/negation-aware) | No | Partial (contradiction ≠ overreach) | Partial (detects contradiction, not quality) | Limited | Ontology-based, not full graph |
| PoliCheck (2020) | **Yes** | **Yes** | No | Partial (flow-to-policy inconsistency only) | No | Limited | Ontology-based |
| PoliGraph / PoliGraph-er (2023) | **Yes** | **Yes** (whole-document, high precision) | No | No | No | Limited | **Yes** |
| PI-Extract | **Yes** | **Yes** | No | No | No | Partial (annotation aids comprehension) | No |
| PoliAnalyzer (2025) | **Yes** | **Yes** (LLM pipeline, PolicyIE-based) | No | No | Partial (user-preference matching) | Partial | Formal encoding, not graph-native |
| PrivComp-KG (2024) | **Yes** (GDPR-focused) | **Yes** | No | No | **Yes** (compliance verification) | Partial (SWRL rule trace) | **Yes** |
| GraphCompliance (2025) | **Yes** | **Yes** | No | No | **Yes** (regulatory) | Partial | **Yes** |
| ML privacy-indicator scoring frameworks | **Yes** | **Yes** (classifier-based) | No | No | No | No (single score) | No |
| PRISMe / XAI-privacy tools (2025) | **Yes** | Partial | No | No | Partial | **Yes** (LLM-as-judge, chat explanations) | No |
| **FDO-Privacy (proposed)** | **Yes** | **Yes** | **Yes** (generalized to full policy) | **Yes** | **Yes** (multi-class) | **Yes** (item-level) | **Yes** (proposed) |

This table is descriptive of the systems located during the review, not exhaustive of the field. It shows FDO-Privacy is not proposing a wholly new sub-field but a **novel combination and extension**: taking the functional-necessity mechanic proven at small scale in mobile-permission research, generalizing it to full privacy-policy text using extraction/KG techniques proven in PoliGraph-style work, and pairing it with a justification-quality classifier and explanation layer in the spirit of, but more granular than, the existing explainable-AI-for-privacy and KG-compliance clusters.

---

## Part 6. Proposed Research Gap

**Existing research can:**
- Extract structured data-practice statements from privacy-policy text with high precision (PoliGraph-er, PI-Extract, PolicyIE-based pipelines).
- Detect internal contradictions and flow-to-policy inconsistencies at scale (PolicyLint, PoliCheck).
- Determine whether a *coarse* natural-language app description justifies a *coarse* OS permission (WHYPER, AutoCog, TKPERM, and recent LLM-based extensions).
- Represent privacy-policy content as a structured knowledge graph (PoliGraph) and align policy text to specific regulatory articles using KG/RAG techniques (PrivComp-KG, GraphCompliance).
- Produce aggregate privacy risk scores/ratings at scale (ML privacy-indicator frameworks, risk-calculation methods).
- Generate LLM-based explanations of policy assessments in an interactive tool (PRISMe).

**Existing research commonly does not:**
- Systematically compare *full privacy-policy-declared collection* (fine-grained data types, purposes, third parties) against an *explicit model of the application's functional requirements* — the description-to-permission fidelity precedent exists only for coarse OS permissions against short app-store descriptions.
- Classify individual flagged data items by *justification quality* (adequate vs. boilerplate vs. absent), as distinct from mere presence/absence or contradiction of disclosure.
- Combine functional-necessity comparison, justification-quality classification, and item-level explainability within a single framework; each capability is found in different, largely non-overlapping literatures (mobile-permission analysis, policy-consistency analysis, KG-compliance analysis, XAI-privacy tools respectively).

**Therefore:**
A defensible, narrowly scoped gap exists at the intersection of (a) functional-necessity reasoning, (b) fine-grained privacy-policy analysis, and (c) explainable, decomposed (not single-score) output. This is a gap of *integration and generalization*, not a gap of "no one has studied privacy policies with AI."

**FDO-Privacy proposes:**
To generalize the description-to-permission fidelity mechanic from coarse OS permissions to fine-grained, policy-declared personal-data categories; to formalize this comparison as Purpose–Collection Gap Analysis; to add a Policy Justification Analysis stage classifying the adequacy of stated purposes for flagged items (informed by, but more granular than, PolicyLint's contradiction detection); to represent the resulting relationships in a Privacy Knowledge Graph (building on PoliGraph-style extraction); and to produce multi-dimensional, explainable, item-level privacy-risk output rather than a single opaque score (addressing the limitation identified in the scoring and XAI-privacy literatures).

---

## Part 7. Evaluation of Proposed Contributions

| Contribution | Category | Justification |
|---|---|---|
| **1. Functional Data Overreach Detection** | **Strong research contribution (conditional)** | The underlying mechanic (functional-necessity comparison) has precedent (WHYPER/AutoCog) but has not been demonstrated at the fine-grained, full-policy level. Novelty is in the generalization and the formal model (Part 9), not in "detecting overreach" as an idea per se. Requires empirical validation to substantiate as a genuine contribution rather than an engineering extension. |
| **2. Purpose–Collection Gap Analysis** | **Supporting/methodological contribution** | This is the operational mechanism realizing Contribution 1. Its novelty is the formal gap model (expected vs. collected data sets) applied at the policy-text level; the general idea of "gap analysis" between expectation and disclosure exists in adjacent forms (flow-to-policy consistency), so claims of gap analysis being unprecedented should be avoided — the novelty is the *functional* (not behavioral) comparison basis. |
| **3. Policy Justification Classification** | **Strong research contribution (conditional)** | No system reviewed performs a dedicated multi-class justification-adequacy classification of individual flagged items. This is closest to being genuinely novel, but requires a validated labeling scheme and demonstrated inter-annotator agreement before the novelty claim is defensible (see Part 13–14). |
| **4. Explainable Privacy Risk Analysis** | **Supporting contribution, engineering-adjacent** | Explainable, LLM-based privacy-policy assessment already exists (PRISMe and related XAI-privacy work). The contribution here is *specificity of explanation target* (per data-item FDO/justification reasoning) rather than the general idea of an LLM explaining a privacy assessment, which is not new. Should be framed as an application/extension of XAI-for-privacy methods to a new task, not as introducing explainability to privacy analysis. |
| **5. Privacy Knowledge Graph** | **Engineering/system contribution** | Privacy-policy knowledge graphs are an established technique (PoliGraph; PrivComp-KG; GraphCompliance). Building one for FDO-Privacy is necessary infrastructure and a legitimate system contribution, but should not be presented as a novel research contribution in itself; the novelty, if any, lies in the graph *schema* needed to represent functional-necessity and justification-quality relations, which existing schemas do not model. |

Overall: Contributions 1 and 3 are the project's strongest defensible research claims, contingent on empirical validation; Contribution 2 is the mechanism, not a separate contribution; Contributions 4 and 5 are valuable engineering contributions that should be described as applications/extensions of established techniques rather than novel introductions.

---

## Part 8. Scope Definition

### 8.1 FDO-Privacy WILL analyze:
- Declared privacy practices as stated in the privacy-policy text (data types, purposes, entities, sharing, retention).
- Application functionality as characterized by publicly available descriptions/functional categories (not source code).
- Functional necessity of each declared/collected data item relative to the described functionality.
- Adequacy of stated policy justifications for data items flagged as functionally non-obvious.
- Internal contradictions within the policy text relevant to flagged items (informed by, but not limited to, PolicyLint-style detection).
- Multi-dimensional, explainable privacy-risk characteristics derived from the above (not runtime data).

### 8.2 FDO-Privacy WILL NOT attempt to guarantee:
- That the analyzed application's **actual runtime behavior** matches its declared policy (this requires dynamic/static code or traffic analysis, as in PoliCheck-style work, which is out of scope for Stage 1–defined FDO-Privacy).
- **Legal compliance determination** under any specific regulation (GDPR, CCPA, COPPA, DPDP, etc.); FDO findings are not legal conclusions.
- That an organization is **legally violating** a specific law — only regulators/courts can make that determination.
- **Malicious intent** — flagged overreach may result from legitimate secondary purposes (analytics, fraud prevention, SDK dependencies), boilerplate policy generation, or legal caution, not necessarily bad faith.
- **Absolute, universal necessity thresholds** for every application — necessity is functionally and contextually determined, and the framework's judgments are defeasible, evidence-based estimates, not ground truth.

This distinction directly follows Rule 4 (Do Not Overclaim) and is essential for the project's academic and practical credibility, particularly because functional necessity is, per the literature (Part 4.6), explicitly recognized as a partially subjective determination.

---

## Part 9. FDO Conceptual Definition

### 9.1 Core definitions

- **Application functionality (F):** The set of discrete, user-facing capabilities an application provides, decomposable into a *primary function* (the app's core value proposition, e.g., "navigation") and zero or more *secondary functions* (e.g., "social sharing," "in-app purchases," "push notifications").
- **Expected data (E(f)):** For a given function *f*, the set of data types that are plausibly required to deliver that function, as would be assessed by a reasonable domain expert (analogous to WHYPER/AutoCog's "permission justified by description," generalized to arbitrary personal-data categories rather than OS permission constants).
- **Collected/declared data (D):** The set of data types the privacy policy states are collected, and (where extractable) the associated purpose, entity, and sharing/retention terms for each — obtainable via PoliGraph-style extraction.
- **Functional necessity:** A (possibly graded, not strictly binary) relation *necessary(d, f)* indicating whether data type *d* is plausibly required for function *f*.
- **Overreach:** A data item *d ∈ D* for which *d ∉ E(F)* — i.e., not necessary for any declared function of the application.
- **Justified overreach:** An overreach item for which the policy provides a *specific, substantive* purpose explanation tied to a legitimate secondary purpose (e.g., fraud prevention, legally mandated retention, ad personalization explicitly opted into).
- **Undisclosed overreach:** An overreach item for which the policy's stated purpose is absent, generic/boilerplate, or does not plausibly connect the data item to any stated purpose.
- **Policy contradiction:** A case where the policy's own statements about a data item are logically inconsistent (informed by PolicyLint's negation/entity-aware contradiction model) — a distinct failure mode from overreach, since a contradiction can occur even for functionally necessary data.

### 9.2 Formal model — revised

The prompt's proposed set-based formulation —

**Expected Data ∩ Collected Data** and **Collected Data − Expected Data**

— is a reasonable starting sketch but is too coarse as a final model for two reasons supported by the literature: (1) necessity is not binary in practice (the WHYPER/AutoCog line already treats fidelity as a graded, evidence-weighted judgment, not strict set membership); and (2) a single global "Expected Data" set ignores that different functions justify different data, and that an item can be expected for one function and unexpected for another within the same app (multi-function apps). A refined, still-implementable model:

```
For application A with functions F = {f1, f2, ..., fn}:
   E(F) = ∪ᵢ E(fᵢ)                     // union of per-function expected data
   D(A) = {(d, purpose, entity, ...)}   // extracted declared data items

   For each d in D(A):
       if d ∈ E(F):                     → Class 1: Expected
       elif d ∉ E(F) and purpose(d) is substantive and specific:
                                         → Class 2: Disclosed Overreach
       elif d ∉ E(F) and purpose(d) is absent/generic:
                                         → Class 3: Undisclosed Overreach
       if declared statements about d are internally contradictory:
                                         → Class 4: Policy Contradiction (orthogonal flag)
```

Necessity judgments (E(fᵢ)) should be produced as **graded confidence scores with rationale**, not hard boolean membership, to reflect the genuine ambiguity documented in the necessity/minimization literature (Part 4.6), and Class 4 is modeled as an orthogonal flag rather than a mutually exclusive class, since contradiction can co-occur with any necessity outcome.

### 9.3 Edge cases requiring explicit handling

- **Optional functionality:** Data required only for an optional feature (e.g., voice search) should be evaluated against that feature specifically, not treated as unnecessary for the "core" app, provided the feature is genuinely optional and separately disclosed.
- **Multiple application functions:** As modeled above via the union E(F); a single "primary function" framing (as in the original prompt) is too restrictive once secondary functions are legitimate.
- **Secondary purposes (analytics, fraud prevention, security):** These are recurring legitimate justifications in the literature (PolicyLint's own findings on contextual purpose phrases) and should be represented as a distinct, non-primary-function purpose category in E, not folded into "core functionality," to avoid mislabeling all analytics collection as overreach.
- **Advertising/personalization:** Ad-related data collection is common, disclosed, and often legally structured around consent; it should generally fall into Class 2 (Disclosed Overreach) when adequately explained, not be treated as inherently problematic.
- **Third-party SDKs:** Data collected via embedded SDKs (analytics, crash reporting, ad networks) complicates entity attribution; FDO-Privacy should, where possible, adopt PoliCheck's entity-sensitivity principle (first-party vs. third-party) when computing D(A).
- **Operationally useful but technically optional data:** Some data (e.g., precise vs. coarse location) may not be strictly "necessary" but materially improves the function it's tied to; graded necessity scoring (9.2) is intended specifically to avoid binary misclassification of such cases as outright overreach.

---

## Part 10. Preliminary Classification Framework — Evaluation

The four proposed classes (Expected / Disclosed Overreach / Undisclosed Overreach / Policy Contradiction) are a reasonable starting taxonomy and map cleanly onto the formal model in Part 9, but reviewing the literature suggests they are **not fully sufficient** as originally scoped:

1. **Contradiction should be orthogonal, not a fourth mutually exclusive class** (see 9.2) — PolicyLint's findings show contradictions can occur regardless of whether the underlying data is necessary, so folding it into a single four-way taxonomy risks losing information when both conditions co-occur.
2. **A fifth outcome — "Ambiguous / Insufficient Evidence" — should be added.** Given that functional necessity is explicitly recognized in the literature as partially subjective (Part 4.6, Part 9.3), some data items will not be confidently classifiable given only public app descriptions and policy text (e.g., unclear whether a "device identifier" is used for core functionality or purely for advertising). Forcing every item into one of four classes risks manufacturing false precision; an explicit low-confidence/ambiguous outcome, carried through to explanation output, is more defensible.
3. **Ambiguous cases to explicitly document:** items justified only by broad "improve our services" language (genuinely ambiguous between Disclosed and Undisclosed Overreach); data required for a function present in some but not all versions/tiers of the app; and data whose necessity depends on user-configurable settings not visible from the policy alone.

Recommended revised framework: **Expected / Disclosed Overreach / Undisclosed Overreach / Ambiguous**, with **Policy Contradiction** as an independent boolean flag attachable to any class.

---

## Part 11. Conceptual Research Framework

```
Application
      ↓  (functional description / category analysis)
Application Functions  (primary + secondary)
      ↓  (functional-necessity modeling, cf. WHYPER/AutoCog generalized)
Expected Data Requirements  — E(F)
      ↓
Privacy Policy  (raw text)
      ↓  (NLP/LLM extraction, cf. PoliGraph-er / PolicyIE)
Declared Data Collection  — D(A): {data type, purpose, entity, sharing, retention}
      ↓
Purpose / Sharing / Retention structuring
      ↓  (set/graded comparison of D(A) vs. E(F))
Functional Data Comparison  — Purpose–Collection Gap Analysis
      ↓
FDO Detection  (per-item classification: Expected / Disclosed / Undisclosed / Ambiguous)
      ↓  (justification-adequacy classification, cf. PolicyLint contradiction modeling extended)
Policy Justification Analysis
      ↓  (item-level rationale generation, cf. XAI-for-privacy / PRISMe-style explanation)
Explainable Privacy Risk  — multi-dimensional, per-item output
```

Each stage corresponds to an existing methodological precedent identified in Part 4, which both grounds the framework's feasibility and clarifies exactly which stage(s) constitute the project's actual novel contribution (principally the Functional Data Comparison and Policy Justification Analysis stages).

---

## Part 12. Research Methodology

**Recommended methodology: Design Science Research (DSR), combined with an experimental/empirical evaluation component.**

Justification: FDO-Privacy's core deliverable is an artifact (a framework/system) intended to solve a practically motivated problem, which is the canonical DSR use case (as also reflected in the GDPR/CI design-science precedent reviewed in Part 4.6). However, unlike pure DSR, the project also makes empirical claims (detection accuracy, explanation quality) that require controlled, measurable evaluation against ground truth and baselines — i.e., an experimental research component nested within the DSR build-evaluate cycle. A purely qualitative/system-oriented approach would be insufficient given Rule 6 (challenge the idea) and Rule 4 (do not overclaim), which require the project to substantiate, not merely assert, its detection and explainability claims.

**Proposed phases:**
1. **Literature review** (this Stage 1 document; to be extended/updated iteratively).
2. **Ontology/taxonomy construction** — application-function taxonomy, data-type taxonomy (drawing on CCPA/PoliGraph-style ontologies), purpose-category taxonomy.
3. **Dataset construction** — a corpus of (application description, privacy policy) pairs across diverse app categories, likely sampled similarly to PoliGraph/PolicyLint's Play Store-derived corpora for comparability.
4. **Ground-truth annotation** — human labeling of expected data per function and overreach class per data item, with a documented annotation protocol and inter-annotator agreement measurement (given the acknowledged subjectivity of necessity judgments).
5. **System development** — extraction pipeline, functional-necessity model, comparison/classification logic, knowledge-graph construction, explanation generation.
6. **Experimental evaluation** — extraction, classification, and detection metrics against ground truth and existing baselines (Part 13).
7. **Explainability evaluation** — human-subject study assessing explanation usefulness/trust/actionability, informed methodologically by the PRISMe user-study design.

---

## Part 13. Evaluation Plan

- **Privacy Policy Extraction:** Precision, Recall, F1 against manually annotated data-practice statements; compare against PoliGraph-er/PI-Extract-style baselines where feasible.
- **Data Classification** (data type / purpose / entity tagging): Precision, Recall, F1 per category.
- **FDO Detection:** Accuracy, Precision, Recall, F1 for the per-item overreach classification (Expected / Disclosed / Undisclosed / Ambiguous), evaluated against human-annotated ground truth.
- **Policy Justification Classification:** Accuracy, Precision, Recall, F1 for justification-adequacy labels, again against human ground truth.
- **Explainability:** Human evaluation / user study (not automatic metrics alone), assessing comprehension, trust, perceived usefulness, and decision-actionability, methodologically informed by the PRISMe 22-participant study design; should also assess *faithfulness* (does the explanation match the actual classification basis) given the adversarial-robustness concern raised in the XAI-for-privacy literature.
- **System Performance:** Processing time per policy/application and scalability across corpus size.

**Additional evaluation considerations:**
- **Baselines:** existing extraction tools (PoliGraph-er where reproducible), existing scoring frameworks (as a "single score" baseline to contrast against explainable multi-dimensional output), and a naive keyword-matching baseline for FDO detection.
- **Ground truth:** must be human-annotated given no existing FDO-labeled dataset was found in this review; annotation guidelines must explicitly address the ambiguous-necessity edge cases in Part 9.3.
- **Train/test split:** application category should be stratified across splits to avoid category-specific overfitting (e.g., all navigation apps in train only).
- **Inter-annotator agreement:** essential and should be reported (e.g., Cohen's/Fleiss' kappa) given the documented subjectivity of necessity judgments; low agreement on certain item types should itself be reported as a finding, not hidden.
- **Error analysis:** qualitative review of false positives/negatives, particularly around the "Ambiguous" boundary and multi-function apps.

No numerical results are asserted at this stage, consistent with the instruction not to invent experimental results.

---

## Part 14. Threats to Validity

| Threat | Mitigation |
|---|---|
| Ambiguity in determining functional necessity | Use graded confidence scores + an explicit "Ambiguous" class (Part 9–10); report inter-annotator agreement transparently rather than forcing consensus. |
| Subjectivity of expected-data labels | Multiple independent annotators per item; documented annotation protocol with worked examples for edge cases (Part 9.3). |
| LLM hallucination in extraction/classification/explanation | Ground extraction in retrieved policy spans (RAG-style grounding, cf. PoliAnalyzer/PrivComp-KG); require citation of the specific policy sentence(s) behind each classification; validate a sample against human review. |
| Privacy policies being incomplete or vague | Explicitly model "insufficient evidence" as a valid outcome rather than forcing a determination; flag low-information policies separately in evaluation. |
| Differences between declared and actual runtime behavior | Out of scope by design (Part 8); explicitly document that FDO-Privacy assesses *declared* practice only, not actual behavior — avoids overclaiming addressed by PoliCheck-style flow analysis, which is a separate, complementary research direction. |
| Application versions changing over time | Timestamp all analyzed policies/descriptions; treat each (app version, policy version) pair as a distinct unit of analysis. |
| Regional policy differences (GDPR vs. CCPA-oriented policies) | Stratify dataset by region/regulatory context where identifiable; avoid a single "universal" necessity threshold (consistent with Part 8's scope limits). |
| Ambiguous application descriptions | Where descriptions are too sparse to infer functions reliably, fall back to app-category taxonomies (e.g., store category) as a coarser functional proxy, and flag confidence accordingly. |
| Third-party SDK behavior conflated with first-party collection | Adopt entity-sensitive modeling (cf. PoliCheck) so third-party-attributed data isn't misattributed to the app's own primary functionality. |
| Dataset selection bias (e.g., overrepresentation of certain app categories or Play Store vs. other stores) | Stratified sampling across categories and (where feasible) platforms; report category distribution alongside results. |
| Human annotation bias | Multiple annotators, blind annotation where feasible, documented disagreement resolution process, and reporting of agreement statistics rather than a single "gold" label asserted without support. |
| Explanation gaming / adversarial robustness (policy authors optimizing wording, not practice, once heuristics are known) | Explicitly flagged in the XAI-for-privacy literature (Part 4.8) as a known risk for any transparent privacy-scoring system; mitigate via periodic re-validation against human judgment and avoiding publication of exact scoring thresholds as exploitable rules. |

---

## Part 15. Final Stage-1 Deliverable Summary

This document constitutes the Stage 1 deliverable and includes: (1) Final Problem Statement (Part 1), (2) Research Question (Part 2.2), (3) Secondary Research Questions (Part 2.3), (4) Research Objectives (Part 3), (5) Literature Review (Part 4), (6) Existing-System Comparison (Part 5), (7) Research Gap (Part 6), (8) Proposed Contributions evaluation (Part 7), (9) Scope and Limitations (Part 8), (10) Formal FDO Definition (Part 9), (11) FDO Classification Framework (Part 10), (12) Conceptual Framework (Part 11), (13) Research Methodology (Part 12), (14) Evaluation Methodology (Part 13), (15) Threats to Validity (Part 14).

---

## STAGE 1 DECISION

**1. Is the research problem sufficiently well-defined?**
Largely yes, after the refinements above. The original problem statement conflated several distinct analytical goals (comparison, detection, justification, explainability); this document decomposes them into an explicit multi-stage pipeline (Part 11) with named precedents for each stage, which makes the problem tractable and falsifiable rather than a vague aspiration.

**2. Is FDO sufficiently distinct from existing privacy-policy analysis concepts?**
Partially, and the distinction must be argued carefully rather than assumed. FDO is **not** distinct from *privacy-policy analysis broadly* (that field is mature). It **is** meaningfully distinct from the specific existing sub-concepts it most resembles: it is not policy-transparency analysis (concerned with readability/findability), not policy-compliance analysis (concerned with legal conformance), not flow-to-policy consistency analysis (concerned with disclosure-vs-behavior, e.g., PoliCheck), and not generic privacy-risk scoring (concerned with aggregate severity). Its closest true precedent — WHYPER/AutoCog-style description-to-permission fidelity — is real but has never been generalized from coarse OS permissions to fine-grained privacy-policy-declared data with an accompanying justification-quality layer. The distinctiveness claim should be framed exactly this way: **a novel generalization and integration**, not an unprecedented concept.

**3. Is the proposed research gap defensible?**
Yes, as scoped in Part 6, provided the project does not claim to be the first to apply AI/NLP/LLMs to privacy policies (false), the first to build a privacy knowledge graph (false — PoliGraph precedes it), or the first to produce explainable privacy assessments (false — PRISMe precedes it). The defensible claim is narrower and should be stated narrowly in any future paper: the first framework (found in this review) to combine functional-necessity comparison, policy-justification classification, and item-level explainability for full privacy-policy text.

**4. Which contributions are strongest?**
Functional Data Overreach Detection (Contribution 1) and Policy Justification Classification (Contribution 3) are the strongest and most original, conditional on empirical validation. Purpose–Collection Gap Analysis (Contribution 2) is the mechanism realizing Contribution 1, not an independent contribution. Explainable Privacy Risk Analysis (Contribution 4) and the Privacy Knowledge Graph (Contribution 5) are legitimate but should be presented as engineering/system contributions applying established techniques (PoliGraph, PRISMe-style XAI) to this new task, not as introducing knowledge graphs or explainability to privacy research.

**5. What must be changed before starting Stage 2?**
- Adopt the revised five-outcome classification (Expected / Disclosed Overreach / Undisclosed Overreach / Ambiguous, with Policy Contradiction as an orthogonal flag) instead of the original four rigid classes.
- Adopt graded (confidence-scored) necessity judgments rather than strict set membership.
- Explicitly scope novelty claims per Part 7's contribution table before any external-facing writing (proposal, paper) is drafted, to avoid overclaiming relative to PoliGraph, PolicyLint/PoliCheck, WHYPER/AutoCog, and PrivComp-KG/GraphCompliance.
- Commit to a human-annotation protocol with inter-annotator agreement reporting before any dataset construction begins, given the field's own acknowledgment that necessity/purpose-limitation judgments are subjective.

**6. What exact artifacts should Stage 2 produce?**
- A formal data-type / function / purpose ontology (extending, not duplicating, PoliGraph's and CCPA-derived ontologies).
- A small pilot corpus (e.g., 20–50 apps across diverse categories) with manually annotated expected-data profiles and overreach labels, including a documented annotation protocol and a pilot inter-annotator agreement measurement.
- A first-draft extraction pipeline design (not full implementation) mapping to the Part 11 framework's "Declared Data Collection" stage, with an explicit baseline comparison plan against PoliGraph-er-style extraction.
- A first-draft functional-necessity inference design mapping to the "Expected Data Requirements" stage, explicitly generalizing the WHYPER/AutoCog fidelity mechanic.
- A refined, testable version of the Part 13 evaluation plan with concrete metrics and a defined (even if small) ground-truth dataset target.

---

## Reference List (sources located during Stage 1 literature review)

- Cui, H., Trimananda, R., Markopoulou, A., & Jordan, S. (2023). *PoliGraph: Automated Privacy Policy Analysis using Knowledge Graphs.* USENIX Security 2023.
- Andow, B., Mahmud, S. Y., Wang, W., Whitaker, J., Enck, W., Reaves, B., Singh, K., & Xie, T. (2019). *PolicyLint: Investigating Internal Privacy Policy Contradictions on Google Play.* USENIX Security 2019.
- Andow, B., Mahmud, S. Y., Whitaker, J., Enck, W., Reaves, B., Singh, K., & Egelman, S. (2020). *Actions Speak Louder than Words: Entity-Sensitive Privacy Policy and Data Flow Analysis with PoliCheck.* USENIX Security 2020.
- Pandita, R., Xiao, X., Yang, W., Enck, W., & Xie, T. (2013). *WHYPER: Towards Automating Risk Assessment of Mobile Applications.* USENIX Security 2013.
- Qu, Z., Rastogi, V., Zhang, X., Chen, Y., Zhu, T., & Chen, Z. (2014). *AutoCog: Measuring the Description-to-permission Fidelity in Android Applications.* ACM CCS 2014.
- Felt, A. P., Chin, E., Hanna, S., Song, D., & Wagner, D. *Android Permissions Demystified* / Stowaway overprivilege study (cited via AutoCog/related literature).
- TKPERM: *Cross-platform Permission Knowledge Transfer to Detect Overprivileged Third-party Applications.* NDSS 2020.
- Harnessing Language Models to Analyze Android App Permission Fidelity (2025 workshop paper, PST'25).
- Biega, A. J., Potash, P., Daumé III, H., Diaz, F., & Finck, M. (2020). *Operationalizing the Legal Principle of Data Minimization for Personalization.* SIGIR 2020.
- ACM Computing Surveys (2024). *A Systematic Review of Privacy Policy Literature.*
- Springer, *Computing* (2022). *A systematic mapping study on automated analysis of privacy policies.*
- LADFA (2025/2026 arXiv). *Using LLMs and RAG for Personal Data Flow Analysis in Privacy Policies.*
- Freiberger, V. et al. (2025). *Explainable AI in Usable Privacy and Security: Challenges and Opportunities* (PRISMe tool discussion), arXiv.
- ScienceDirect (2023/2026). *A privacy scoring framework: Automation of privacy compliance and risk evaluation with standard indicators.*
- ScienceDirect (2025). *What are your privacy risks? Privacy risk assessment based on privacy policies analysis.*
- Garza, L., Elluri, L., Kotal, A., Piplai, A., Gupta, D., & Joshi, A. (2024). *PrivComp-KG: Leveraging Knowledge Graph and Large Language Models for Privacy Policy Compliance Verification.* arXiv:2404.19744.
- GraphCompliance: *Aligning Policy and Context Graphs for LLM-Based Regulatory Compliance* (2025, arXiv).
- Knowledge Graph Representations for LLM-Based Policy Compliance Reasoning (arXiv survey/reference compilation).
- PoliAnalyzer (2025 arXiv). *Let's Measure the Elephant in the Room: Facilitating Personalized Automated Analysis of Privacy Policies at Scale.*
- GDPR Compliance in the Context of Continuous Integration (design-science, arXiv:2002.06830).
- Messaging with Purpose Limitation — Privacy-Compliant Publish-Subscribe Systems (arXiv:2110.15150).

*Note: some sources were accessed via secondary aggregators (Semantic Scholar, ResearchGate, DeepDyve, GitHub mirrors); original venue/publication details are cited above where identifiable. A small number of 2025–2026 arXiv preprints referenced here are not yet peer-reviewed and should be re-verified before being cited in a formal thesis or paper.*
