# Stage 2 — Functional Data Ontology for FDO-Privacy

**Project:** FDO-Privacy: An Explainable AI Framework for Detecting Functional Data Overreach in Privacy Policies
**Stage:** 2 of N — Ontology Design & Validation (no implementation, no detector, no full KG)

---

## PART 1 — Purpose of the Ontology

FDO-Privacy's central claim — that an app's declared data collection can "exceed" functional necessity — is only meaningful if "functional necessity" is defined in a way that is explicit, inspectable, and reproducible. Without a shared ontology, any judgment of overreach collapses into an unstructured LLM opinion: unfalsifiable, inconsistent across runs, and impossible to audit. The ontology is the artifact that makes the research question answerable rather than merely askable.

The ontology supplies the controlled vocabulary and relational structure connecting:

```
Application → Application Category → Application Function → Functional Feature
→ Data Type → Necessity Level → Purpose → Evidence/Rationale
```

Each link in this chain is a claim that must be independently defensible. An application belongs to a category (contextual prior, not proof); a category typically implements certain functions (a taxonomy, not a mandate — not every navigation app has traffic monitoring); a function decomposes into features (some core, some optional); each feature is associated with data types at varying necessity levels; each data-type/function pairing serves a purpose; and every pairing must cite the evidence used to justify it. This chain is what later lets the system compute an **Expected Data Profile** for an app, which is compared against the **Declared Data Profile** extracted from its privacy policy. The mismatch is a **Functional Gap**, and only gaps that survive the necessity/purpose/evidence filters become **FDO candidates** — not raw mismatches.

```
Expected Data (from ontology + declared functions)
        ↓
Declared Data (from privacy-policy extraction)
        ↓
Functional Gap = Declared − Expected, annotated with necessity/purpose context
        ↓
FDO Detection = Gap items with no defensible functional or secondary-purpose justification
```

### Key distinctions

| Concept | Definition | Key property |
|---|---|---|
| **Application category** | A coarse market/domain grouping (e.g., Navigation, Banking) | Weak prior; not determinative |
| **Application function** | A discrete capability the app performs (e.g., turn-by-turn navigation) | Unit of necessity analysis |
| **Feature** | A concrete implementation detail or sub-capability of a function (e.g., voice-guided turns) | May be core or optional |
| **Data type** | A standardized category of personal/device data | Drawn from the data-type taxonomy |
| **Purpose** | The declared or inferred reason data is used | Independent axis from necessity |
| **Functional necessity** | How tightly a data type is coupled to a function/feature operating at all | Graded, not binary |
| **Optional data** | Data required only if a non-default, opt-in feature is enabled | Necessity is conditional on feature adoption |
| **Context-dependent data** | Data whose necessity varies by deployment context (device type, region, account tier) | Necessity is a function of context, not fixed |
| **Unexpected data** | Data with no evidentiary link to any identified function or declared secondary purpose | Necessary but not sufficient condition for FDO |

---

## PART 2 — Ontology Design Principles

1. **Functional specificity** — Mappings are anchored to a named function/feature, never to "the app" as a whole. "Navigation apps need location" is too coarse; "turn-by-turn navigation requires precise real-time location" is auditable.
2. **Explainability** — Every edge in the ontology carries a rationale string. An edge without a rationale is not admissible to the ontology, only to a "candidate/unvalidated" holding area.
3. **Machine readability** — All entities and relations are expressed in a structured schema (Part 14) so the future detector can traverse the graph programmatically rather than re-parsing prose.
4. **Extensibility** — New categories, functions, features, and data types must be addable without breaking existing mappings — additive schema, versioned identifiers, no hard-coded enums where a controlled vocabulary can grow.
5. **Domain independence** — The ontology's structural rules (function→feature→data→necessity→purpose→evidence) apply uniformly whether the domain is Banking or Gaming; category-specific content lives in populated instances, not in the schema itself.
6. **Evidence grounding** — No mapping exists purely because an LLM asserted it; every mapping traces to at least one evidence category (Part 11), and LLM inference is explicitly tagged as such and weighted lowest.
7. **Handling of optional features** — Optional features get their own necessity tier (Level 3) so that data tied to an opt-in capability is never conflated with data the core function needs.
8. **Handling of secondary functions** — Analytics, fraud prevention, personalization, and advertising are modeled as first-class functions with their own expected-data mappings, not folded into the primary function's requirements or dismissed as automatically illegitimate.
9. **Handling of third-party services** — SDKs/embedded services (e.g., payment processors, ad networks, crash reporters) are modeled as attributed sub-collectors with their own purpose tags, so a data flow to a third party is traceable and not silently merged into "the app's" own necessity profile.
10. **Handling of ambiguity** — A dedicated "Ambiguous / Insufficient Evidence" state exists so the ontology does not force a confident label when the evidence doesn't support one; ambiguity is a valid, explicit output.
11. **Versioning** — Every entity, mapping, and schema release is versioned; mappings can be deprecated/superseded without deleting history, preserving auditability and enabling longitudinal study of how norms shift.
12. **Human validation** — LLM-proposed mappings are draft-status until reviewed by an annotator; the annotation protocol (Part 12) is the gate between "candidate ontology" and "validated ontology."

Each principle exists to block a specific known failure mode: (1)/(5) block over-generalization; (2)/(6) block black-box authority; (3)/(4)/(11) block brittleness; (7)/(8)/(9) block false-positive FDO findings; (10) blocks false confidence; (12) blocks LLM self-certification.

---

## PART 3 — Application Function Taxonomy (preliminary)

```
Communication
├── Text messaging
├── Voice calling
├── Video calling
├── Contact discovery
├── File sharing
└── Group communication

Social Media
├── Content posting
├── Content feed/discovery
├── Direct messaging
├── Social graph management (follow/friend)
├── Content reaction (like/comment)
└── Live streaming

Navigation
├── Route calculation
├── Turn-by-turn navigation
├── Traffic monitoring
├── Location search
├── Saved places
└── Location sharing

Finance / Banking
├── Account balance & statements
├── Fund transfer
├── Bill pay
├── Mobile check deposit
├── Card management
└── Fraud/security monitoring

Shopping / E-commerce
├── Product browsing/search
├── Cart & checkout
├── Payment processing
├── Order tracking
├── Reviews/ratings
└── Personalized recommendations

Healthcare
├── Appointment scheduling
├── Telehealth video visits
├── Health record access
├── Medication tracking
└── Symptom checking

Education
├── Course content delivery
├── Assignment submission
├── Progress tracking
└── Discussion/collaboration

Entertainment / Streaming
├── Content playback
├── Content search/discovery
├── Watchlists/favorites
├── Recommendations
└── Offline download

Productivity
├── Document editing
├── Task/project management
├── Calendar/scheduling
├── File storage/sync
└── Collaboration

Utilities
├── Device management
├── System diagnostics
└── Notifications

Travel
├── Booking (flights/hotels)
├── Itinerary management
├── Check-in
└── Real-time trip updates

Food Delivery
├── Restaurant/menu browsing
├── Order placement
├── Payment
├── Delivery tracking
└── Ratings/reviews

Fitness
├── Activity tracking
├── Workout logging
├── Health metric tracking (HR, sleep)
├── Social/challenge features
└── Coaching/recommendations

Gaming
├── Core gameplay
├── Multiplayer/matchmaking
├── In-app purchases
├── Leaderboards/social
└── Push notifications/re-engagement
```

The taxonomy is stored as a controlled vocabulary with stable IDs (e.g., `CAT.NAV`, `FUNC.NAV.TURNBYTURN`) so new categories/functions append without renumbering existing ones.

---

## PART 4 — Data-Type Taxonomy

The starting hierarchy in the prompt is retained as the working skeleton, refined and cross-mapped rather than reinvented:

```
Personal Data
├── Identity Data: Name, Date of Birth, Government ID, Profile Information, Demographic Data
├── Contact Data: Email, Phone Number, Address, Emergency Contact
├── Location Data: Precise Location, Approximate Location, Location History
├── Communication Data: Messages, Call Metadata, Call Content, Contacts List
├── Financial Data: Payment Instrument, Transaction History, Bank Account/Routing, Credit Data
├── Device Data: Device Identifier, IP Address, Advertising ID, Device/OS Characteristics, Network Info
├── Media Data: Photos, Videos, Audio Recordings, Camera Stream, Microphone Stream
├── Usage/Behavioral Data: In-App Activity Logs, Clickstream, Session Data, Search History
└── Sensitive Data: Health Data, Biometric Data, Genetic Data, Precise Geolocation of Minors,
                     Religious/Political/Sexual-Orientation Data, Government ID Numbers
```

**Reuse vs. new vocabulary.** FDO-Privacy should *not* invent a competing personal-data taxonomy. Recommended mapping strategy:

- **Reuse directly**: GDPR Art. 4/9 categories for the Identity/Sensitive split (Art. 9 special categories map onto our "Sensitive Data" branch); CCPA/CPRA §1798.140 categories for the overall personal-information list (map closely to Identity/Contact/Financial/Device/Usage branches); Google Play Data Safety categories (Location, Personal Info, Financial Info, Health & Fitness, Messages, Photos/Videos, App Activity, Device/Other IDs) as a near-1:1 crosswalk since many target apps are mobile and already self-declare in this schema; existing mobile-privacy taxonomies from academic permission-mapping literature (e.g., work correlating Android permissions to data categories) for the Device/Media branches.
- **FDO-Privacy adds**: a *functional-necessity axis* orthogonal to these existing taxonomies (none of GDPR/CCPA/Play Data Safety encode "how functionally necessary is this to function X" — they encode *what* data and *broad purpose category*, not fine-grained necessity-to-function coupling). This is the ontology's actual novel layer, not the data taxonomy itself.
- Each data-type node stores a `crosswalk` field: `{ "gdpr": "...", "ccpa": "...", "play_data_safety": "..." }` so downstream policy-extraction (which will likely encounter policies using any of these vocabularies) can normalize into our internal IDs.

---

## PART 5 — Necessity Levels

Binary Required/Not-Required is rejected — it cannot represent optionality, secondary purposes, or evidentiary uncertainty, all of which are central to avoiding false positives. The graded model in the prompt is adopted with one refinement: **Level 4 (Secondary-Purpose)** is split into a **sub-typed enum** rather than a flat label, because "analytics" and "advertising" have very different legitimacy profiles under most regulatory frameworks and should not be scored identically downstream.

| Level | Label | Definition |
|---|---|---|
| 1 | Functionally Required | Function cannot operate at all without this data |
| 2 | Functionally Supportive | Function operates without it, but is materially degraded |
| 3 | Optional-Feature Data | Required only if a specific, non-default feature is enabled |
| 4 | Secondary-Purpose Data | Used for a declared purpose distinct from core function (sub-typed: analytics / advertising / personalization / fraud-security / crash-diagnostics / service-improvement / legal-compliance) |
| 5 | No Functional Evidence | No plausible link to any identified function or declared secondary purpose |
| 6 | Ambiguous | Evidence is insufficient to assign 1–5 confidently |

This is a **defensible but not objective** model — it is a structured way of representing expert/annotator judgment, not a physical law. Its purpose is reproducibility of *reasoning*, not elimination of judgment calls.

---

## PART 6 — Function → Data Mapping (illustrative)

| Function | Data | Necessity | Purpose | Rationale | Confidence |
|---|---|---|---|---|---|
| Turn-by-turn navigation | Precise Location | L1 Required | Route calculation | Cannot compute current position/route without it | High |
| Turn-by-turn navigation | Contacts | L5 No Evidence | — | No functional link to routing | High |
| Turn-by-turn navigation | Camera | L3 Optional | Visual/AR navigation | Only if AR-overlay feature exists | Medium |
| Turn-by-turn navigation | Device ID | L4 Secondary (analytics) | Usage analytics | Not needed for routing itself | Medium |
| Messaging | Contacts | L1 Required | Contact discovery | Core to finding/starting conversations | High |
| Messaging | Camera | L3 Optional | Image messaging | Only if in-app photo capture exists | Medium |
| Messaging | Precise Location | L4 Secondary or L5 | Location sharing (if feature exists) / else no evidence | Depends on whether location-sharing is a declared feature | Medium |
| Banking | Government ID | L1 Required | Identity verification / KYC | Regulatory requirement for account opening | High |
| Banking | Precise Location | L4 Secondary (fraud-security) | Fraud detection | Not required for a transaction to execute, but a recognized security practice | Medium |
| Fitness Tracking | Health Data (HR) | L1 Required | Activity/metric tracking | Core purpose of the app | High |

---

## PART 7 — Ten Detailed Function Profiles

Each profile below uses the schema: Function / Description / Required / Supportive / Optional / Secondary / Usually Unexpected / Rationale / Confidence / Evidence Type.

**1. Messaging (text)**
- *Required*: Contacts (for recipient selection), Message Content (transiently, for delivery)
- *Supportive*: Phone Number/Email (as account identifier)
- *Optional*: Camera/Photos (image messaging), Microphone (voice notes)
- *Secondary*: Device ID (analytics), Usage Logs (service improvement)
- *Unexpected*: Precise Location (unless location-sharing declared), Health Data, Financial Data
- *Rationale*: Text delivery requires addressing (contacts) and content; everything else is feature-conditional or purpose-conditional.
- *Confidence*: High (core), Medium (secondary items)
- *Evidence*: Domain reasoning, app-store descriptions

**2. Voice Calling**
- *Required*: Microphone Audio (transiently), Phone Number or Account ID (call routing)
- *Supportive*: Contacts (caller ID/lookup)
- *Optional*: Call Recording storage (if feature exists)
- *Secondary*: Call Metadata (fraud/quality analytics)
- *Unexpected*: Camera, Photos, Precise Location
- *Rationale*: Real-time audio transport is the core function; anything visual/locational is extraneous absent a stated feature.
- *Confidence*: High
- *Evidence*: Domain reasoning, telecom functional standards

**3. Video Calling**
- *Required*: Camera Stream, Microphone Audio (transiently)
- *Supportive*: Contacts
- *Optional*: Screen sharing (Screen Content), Virtual backgrounds (Photos, for custom bg)
- *Secondary*: Device Characteristics (quality/analytics), Device ID
- *Unexpected*: Precise Location, Financial Data, Health Data
- *Rationale*: Visual+audio streams are intrinsic; location/financial data have no coupling.
- *Confidence*: High
- *Evidence*: Domain reasoning

**4. Navigation (route/turn-by-turn)**
- *Required*: Precise Location
- *Supportive*: Location History (traffic prediction), Saved Places
- *Optional*: Camera (AR overlay), Location Sharing (contacts, if "share ETA" exists)
- *Secondary*: Device ID/IP (analytics/ads)
- *Unexpected*: Contacts (absent share feature), Financial Data, Health Data
- *Rationale*: Positioning is intrinsic to routing; everything else is either feature-gated or purpose-gated.
- *Confidence*: High
- *Evidence*: Domain reasoning, published API docs of mapping SDKs

**5. Banking**
- *Required*: Government ID/SSN (KYC), Bank Account Info, Authentication Credentials
- *Supportive*: Device ID (fraud correlation), Transaction History (statements)
- *Optional*: Camera (mobile check deposit, biometric login)
- *Secondary*: Precise Location (fraud detection), Biometric Data (auth convenience)
- *Unexpected*: Contacts, Microphone, Camera-roll Photos (absent check-deposit feature)
- *Rationale*: Regulatory KYC drives required tier; fraud-prevention data is legitimate secondary use, not automatically FDO.
- *Confidence*: High (required), Medium (secondary)
- *Evidence*: Regulatory principle (KYC/AML), domain reasoning

**6. E-commerce (browse/checkout)**
- *Required*: Payment Information (at checkout), Shipping Address
- *Supportive*: Order History, Account Email
- *Optional*: Camera (visual search/AR try-on), Precise Location (store locator)
- *Secondary*: Advertising ID, Behavioral/Usage Data (personalization/ads)
- *Unexpected*: Contacts, Health Data, Microphone
- *Rationale*: Transacting requires payment+shipping; recommendation/ads data is a distinct, declarable secondary purpose.
- *Confidence*: High
- *Evidence*: Domain reasoning, app-store descriptions

**7. Food Delivery**
- *Required*: Delivery Address, Payment Information
- *Supportive*: Precise Location (live courier tracking), Phone Number (delivery coordination)
- *Optional*: Photos (delivery-instruction images)
- *Secondary*: Device ID, Behavioral Data (personalization/ads)
- *Unexpected*: Contacts, Health Data, Camera (absent optional feature)
- *Rationale*: Real-time delivery tracking materially depends on live location, distinguishing it from static-checkout e-commerce.
- *Confidence*: High
- *Evidence*: Domain reasoning

**8. Video Streaming**
- *Required*: none beyond an account identifier to authorize playback
- *Supportive*: Watch History (recommendations, resume-playback), Device Characteristics (bitrate/DRM)
- *Optional*: Profile/Household data (multi-profile features)
- *Secondary*: Advertising ID, Behavioral Data
- *Unexpected*: Precise Location (beyond coarse licensing-region check), Contacts, Financial Data (beyond billing)
- *Rationale*: Playback itself needs almost nothing personal; most collection here is secondary-purpose, which must be evaluated on its own terms, not assumed necessary.
- *Confidence*: Medium-High
- *Evidence*: Domain reasoning, DRM/licensing standards

**9. Fitness Tracking**
- *Required*: Health/Activity Data (HR, steps, GPS-based distance)
- *Supportive*: Precise Location (route mapping), Sleep Data
- *Optional*: Camera (progress photos), Social/Contacts (challenges)
- *Secondary*: Advertising ID, Demographic Data (personalization)
- *Unexpected*: Financial Data, Call/Message Content
- *Rationale*: The core value proposition *is* biometric/activity data, making this one of the few domains where sensitive-data collection is squarely L1.
- *Confidence*: High
- *Evidence*: Domain reasoning, existing app documentation

**10. Photo Editing**
- *Required*: Photo Library Access (to select/edit an image), or Camera (to capture one)
- *Supportive*: none beyond required
- *Optional*: Precise Location (geotag stamping feature), Cloud Storage sync
- *Secondary*: Device ID, Usage Data (analytics)
- *Unexpected*: Contacts, Microphone, Financial Data, Health Data
- *Rationale*: Editing requires image access as a baseline; most other data categories have no functional coupling.
- *Confidence*: High
- *Evidence*: Domain reasoning, app-store descriptions

---

## PART 8 — Avoiding False Positives: "Unexpected ≠ Overreach"

A data item lacking a core-functional link may still be legitimately collected for a **declared, evaluable secondary purpose**. The ontology therefore keeps "unexpected relative to core function" and "unjustified overall" as *separate* judgments — only the latter is eligible to be flagged as FDO.

- **Location → Navigation** (Example 1): L1, expected, no ambiguity.
- **Location → Advertising** (Example 2): unexpected *for the core function*, but legitimate as a declared L4 secondary purpose. FDO only if declared without disclosure, or disclosed with no plausible purpose match.
- **Camera → Image messaging** (Example 3): L3 optional, expected *conditional on the feature being real* — the ontology requires evidence the feature exists (app-store description, UI documentation) before granting L3 status.
- **Camera → No identified feature** (Example 4): L5, no functional or secondary-purpose anchor found — this is the pattern that should raise an FDO flag.
- **Location → Fraud detection (Banking)** (Example 5): L4 secondary-purpose, legitimate security rationale, not L1 for the transaction itself. FDO analysis should note it as "collected beyond core-transaction necessity but for a recognized security purpose," not as overreach, unless the declared purpose is implausible for the app's actual behavior (e.g., a static informational banking-rate-calculator app claiming "fraud detection" for constant background location).

**General rule the ontology encodes:** FDO requires *(unexpected relative to core function) AND (no credible secondary-purpose anchor, or an anchor contradicted by other evidence)*. A single unmet condition blocks the FDO label and routes the item to "Secondary-Purpose — Unverified" for human review instead.

---

## PART 9 — Primary vs. Secondary Functions

```
Application
├── Primary Function(s)
└── Secondary Functions
    ├── Optional Feature
    ├── Security Function
    ├── Analytics Function
    ├── Personalization
    └── Advertising
```

The Stage 1 model `E(F) = ∪ E(fᵢ)` (expected data = union across all functions' expected sets) **loses information that FDO detection needs**: a flat union cannot represent "Data D is required for f₁ but has no relation to f₂," which matters because the *purpose claimed for D in the privacy policy* must match against the *specific function that actually needs it*, not against the app's undifferentiated functional surface.

**Proposed replacement — a keyed/attributed expected-data structure:**

```
E(F) = { (D, f, necessity(D,f), purpose(D,f)) : f ∈ functions(F), D ∈ data_types }
```

i.e., expected data is a set of **(data type, function, necessity, purpose)** tuples, not a flat set of data types. Two consequences:
1. A data type can appear multiple times with different necessity levels attached to different functions (e.g., Location is L1 for Navigation's route-calc but L4-secondary for the same app's ad function) — the union no longer silently collapses these into one entry.
2. When comparing against declared data, the detector can ask "is this declared collection justified *by any function*, and if so which, and does the declared purpose match that function's purpose?" rather than a purposeless set-membership check.

---

## PART 10 — Contextual Necessity

| Data | Function | Purpose | Context | Necessity Assessment |
|---|---|---|---|---|
| Precise vs. Approximate Location | Navigation | Routing | Turn-by-turn requires precise; "nearby city weather" only needs approximate | L1 precise for turn-by-turn; L1 *approximate only* for coarse features — collecting precise where approximate suffices is itself a candidate finding |
| Camera | AR features | Visual overlay | Only if AR mode exists and is user-invoked | L3, conditional on feature existing and being active |
| Contacts | Contact discovery | Find friends already using the app | Only relevant for social/communication apps | L1 for that function; L5 for apps without any discovery feature |
| Device ID | Fraud prevention | Cross-session fraud correlation | More justifiable in Banking/Finance than in, e.g., a flashlight app | L4, strength of justification is category- and risk-dependent |
| Phone Number | Account authentication | 2FA/verification | Justifiable across almost all categories as a security control | L2 (supportive) generally, sometimes L1 if it's the sole login method |
| Date of Birth | Age verification | Legal compliance (COPPA etc.) | Required where age-gated content/services exist | L1 for age-gated functions; L5 otherwise |
| Health Data | Fitness tracking | Core metric delivery | Central to the app's value proposition | L1 |
| Payment Information | Purchases | Transaction processing | Only at point of purchase, not for browsing | L1 at checkout; L5/unexpected if collected before any purchase intent |

The ontology represents this as a 4-tuple **(Data, Function, Purpose, Context) → Necessity**, so necessity is always computed relative to a specific context rather than assigned globally to a data type.

---

## PART 11 — Evidence Model

**Evidence categories** (ordered roughly by strength, though strength is evaluated per-case, not by category alone):

1. Regulatory principle (e.g., KYC/AML mandates, COPPA age-verification requirements)
2. Established taxonomy / prior academic research
3. Official application documentation (developer docs, API specs)
4. App-store description / published feature list
5. Domain expert judgment (annotator with relevant subject-matter background)
6. Human annotation (trained annotator following the protocol, without specialist domain expertise)
7. Domain reasoning (generalizable, widely-accepted functional logic, e.g., "video calling requires a camera stream")
8. LLM inference (model-generated candidate mapping)

**Critical separation:** LLM inference (category 8) is *always* a candidate, never a finalized mapping. Every LLM-proposed mapping is stored with `status: "draft"` and a `source: "llm_inference"` tag; it can only transition to `status: "validated"` after passing the annotation protocol (Part 12). This prevents the system from quietly using its own generative output as ground truth — a specific, named risk in Rule 3.

Example record:
```
Mapping: Navigation → Precise Location
Necessity: L1 Required
Evidence: [domain_reasoning, appstore_description]
LLM-proposed: true
Status: validated (2 annotators, κ agreement = 0.91)
Confidence: High
```

---

## PART 12 — Annotation Protocol

**Annotator qualifications**: no formal credential is mandated, but annotators should have (a) basic familiarity with mobile/web app functional design, and (b) training on this protocol document + a calibration set of 10 pre-labeled examples with worked rationale, passed before annotating pilot data. For Banking/Healthcare categories, at least one annotator with relevant domain exposure (finance/health background) should review, given regulatory-driven necessity claims (KYC, COPPA, HIPAA-adjacent).

**Annotation unit**: a single tuple `(Application, Function, Data Type, Context) → Necessity Level + Purpose + Rationale`. Annotators do not label whole apps at once; each function–data pairing is a separate judgment.

**Annotation labels**: the six-level necessity scale from Part 5, plus a free-text rationale field and a purpose tag (for L4, the sub-typed purpose enum) that is mandatory for every non-L5 label.

**Instructions (decision procedure)**:
1. Can the function operate *at all* without this data? No → L1.
2. Can it operate, but is materially worse/limited without it? → L2.
3. Is the data only needed if a specific non-default feature is turned on? → L3 (must cite the feature).
4. Is the data tied to a purpose distinct from making the function work (analytics, ads, fraud, personalization, crash reporting, compliance)? → L4 (must select purpose sub-type).
5. If none of the above apply and no plausible link exists → L5.
6. If the annotator cannot confidently choose among the above given available evidence → L6 (must state what additional evidence would resolve it).

**Disagreement resolution**: each item is labeled independently by ≥2 annotators. Exact agreement stands. Disagreement of one level apart (e.g., L1 vs. L2) is resolved by discussion and consensus; disagreement of two+ levels apart, or any disagreement involving L5 vs. anything else, is escalated to a third adjudicating annotator and, for Banking/Healthcare, the domain-background reviewer.

**Inter-annotator agreement statistic**: **Krippendorff's Alpha** is recommended over Cohen's/Fleiss' Kappa because (a) the necessity scale is ordinal, not nominal, and Alpha handles ordinal weighting cleanly; (b) not every item will have exactly the same number of annotators (missing/incomplete labels are common in pilot rounds), which Alpha tolerates and Kappa-family statistics do not handle natively; (c) Alpha generalizes to >2 annotators without the pairwise-averaging awkwardness of Cohen's Kappa. Report Alpha per necessity dimension and per purpose-tag dimension separately.

---

## PART 13 — Pilot Dataset Specification (20–50 apps)

**Coverage target**: at least 2 apps per category from Part 3 (aim ~30 apps for adequate per-category signal without overloading Stage 2). Include a deliberate mix of simple single-function apps (flashlight, calculator) and complex multi-function apps (super-apps with messaging+payments+social) to stress-test the taxonomy's handling of primary/secondary function separation.

**Per-application record**:
```
Application ID
Application Category
Application Description (source: app-store listing, summarized)
Primary Functions [list of Function IDs]
Secondary Functions [list, tagged: optional/security/analytics/personalization/advertising]
Function Evidence [evidence category + source citation, per function]
Expected Data [(data_type, function, necessity, purpose, rationale, confidence)]
Annotator IDs [≥2]
Agreement [Krippendorff's Alpha per item / per app]
Notes on ambiguity or disputed items
```

This pilot dataset's purpose is **ontology validation**, not FDO detection — no privacy-policy text or declared-data comparison happens in Stage 2. That belongs to a later stage once the Expected Data side is validated.

---

## PART 14 — Machine-Readable Schema

```json
{
  "schema_version": "0.2.0",
  "application": {
    "app_id": "string",
    "name": "string",
    "category": "CAT.NAV",
    "description_source": "string (citation)"
  },
  "functions": [
    {
      "function_id": "FUNC.NAV.TURNBYTURN",
      "name": "Turn-by-turn navigation",
      "type": "primary",
      "features": [
        {
          "feature_id": "FEAT.NAV.AR_OVERLAY",
          "name": "AR visual overlay",
          "optional": true
        }
      ],
      "evidence": [
        {"category": "appstore_description", "citation": "string", "confidence": "High"}
      ],
      "expected_data": [
        {
          "data_type_id": "DATA.LOCATION.PRECISE",
          "necessity": "L1_REQUIRED",
          "purpose": "route_calculation",
          "context": "core_operation",
          "confidence": 0.95,
          "rationale": "string",
          "evidence": [
            {"category": "domain_reasoning", "source": "string"}
          ],
          "llm_proposed": true,
          "status": "validated",
          "annotators": ["A1", "A2"],
          "agreement_alpha": 0.91,
          "version": "1.0.0",
          "superseded_by": null
        }
      ]
    }
  ],
  "secondary_purposes": [
    {
      "purpose_type": "advertising",
      "data_type_id": "DATA.DEVICE.ADID",
      "necessity": "L4_SECONDARY",
      "declared_by_app": true,
      "evidence": [{"category": "privacy_policy_reference", "source": "string"}]
    }
  ]
}
```

**Representation for the eventual full system**: JSON is right for Stage 2 (human-editable, tool-agnostic, matches the annotation workflow). For the eventual production knowledge graph, a **property graph in Neo4j** (or equivalent) is recommended over RDF/OWL: the relationships here are richer in edge-attributes (necessity, purpose, confidence, evidence, version) than clean class/subclass hierarchies, which property graphs represent naturally via edge properties, whereas OWL/RDF would require extensive reification to attach the same attributes to relationships. RDF/OWL becomes worthwhile only if formal ontological reasoning (e.g., automated consistency-checking via a reasoner, or public Linked-Data interoperability) becomes a project goal — not currently in scope. JSON-LD is a reasonable middle ground for external interoperability/publication later, generated from the graph rather than authored directly. **This is a recommendation only; no implementation occurs in Stage 2.**

---

## PART 15 — Ontology Validation Plan

| Dimension | Criterion | Measurement |
|---|---|---|
| Coverage | Every pilot app's stated functions map to ≥1 taxonomy function; no more than a small residual "uncategorized" rate | % of functions successfully mapped to existing taxonomy nodes (target ≥90%; below that signals taxonomy gaps, not app weirdness) |
| Consistency | Same data type + same function + same context yields same necessity across annotators/apps | Krippendorff's Alpha ≥ 0.7 treated as acceptable; 0.6–0.7 flagged for protocol revision; <0.6 blocks validation |
| Agreement | Annotators converge without excessive adjudication | % of items requiring third-annotator escalation (target <15%) |
| Extensibility | New function/data type addable without modifying existing validated mappings | Structural test: add 3 novel functions post-hoc, confirm zero edits to existing nodes required |
| Explainability | Every validated mapping has a non-empty rationale + ≥1 evidence citation | Automated schema check: 100% required (this is a hard gate, not a target) |
| Robustness | Ambiguous/edge-case apps (multi-function super-apps, niche utility apps) don't break the model | Qualitative review of ≥5 deliberately hard pilot cases; document unresolved cases rather than forcing a label |

---

## PART 16 — Connection to Future FDO Detection (Stage 6)

```
Application Description
        ↓  (function-extraction, using this taxonomy as the target label space)
Function Extraction
        ↓
Functional Data Ontology  (this Stage-2 artifact — the lookup structure)
        ↓  (per identified function, retrieve validated expected_data tuples)
Expected Data Profile  (attributed per-function, not a flat union — see Part 9)
        ↓
Privacy Policy Extraction  (separate NLP task — declared data + declared purposes)
        ↓
Declared Data Profile
        ↓
Functional Comparison  (per data item: is it in Expected Data for *some* identified function,
                         with matching or plausible purpose? or is it L4-justifiable? or neither?)
        ↓
FDO Classification  (only "neither" cases, per Part 8's AND rule, become FDO candidates —
                      routed with full evidence trail for explainability, not a bare flag)
```

For every expected-data mapping, the future engine consumes: `(data_type, function, necessity, purpose, confidence, evidence[])`. The detector's core comparison logic is essentially: for each declared-data item, search the Expected Data Profile for a matching function+purpose entry; absence of a match at necessity ≥ L4 (i.e., no required/supportive/optional/secondary anchor) is what triggers an FDO candidate, subject to human/threshold review given confidence and ambiguity flags.

---

## PART 17 — Research Contribution Analysis

- **Existing knowledge (reused, not claimed as novel)**: the underlying personal-data category taxonomy (GDPR/CCPA/Play Data Safety-derived); the general idea that apps have "functions" that can be enumerated; basic privacy-by-design/data-minimization principle (data minimization itself is an established regulatory concept, not new here).
- **Adaptation**: restructuring existing data taxonomies into a machine-traversable, versioned, evidence-tagged schema tuned specifically for function-level (not app-level) granularity; adapting standard annotation/IAA methodology (Krippendorff's Alpha, adjudication) to this specific labeling task.
- **Potential genuine contribution**: the **explicit, graded, evidence-linked coupling between (function, feature, context) and (data type, necessity, purpose)** as a queryable structure — i.e., not just "what data does a banking app collect" (descriptive, already done by prior privacy-policy NLP work) but "what data does *this specific function under this context* actually require, with what confidence and evidence, distinguishable from secondary-purpose collection." The attributed (non-union) expected-data model in Part 9, and the AND-gated FDO-eligibility rule in Part 8 (unexpected-for-function AND no secondary-purpose anchor) are the most defensible candidates for a genuine methodological contribution, *if* validated empirically against real annotator agreement and shown to reduce false-positive overreach flags compared to a naive "data not obviously needed = flag it" baseline. A simple function→data table alone is descriptive cataloguing and should not be presented as the paper's contribution.

---

## PART 18 — Critical Challenge (skeptical pass)

1. **Who decides what data is necessary?** Trained annotators following a documented protocol, with domain-expert review for regulated categories — not a single author's intuition, and not the LLM alone. Mitigation: multi-annotator IAA reporting is mandatory, not optional.
2. **Can two experts reasonably disagree?** Yes, especially at the L1/L2 boundary and around secondary-purpose plausibility. Mitigation: L6 (Ambiguous) exists precisely to make disagreement visible rather than papered over; disputed items are retained in the dataset with disagreement documented, not silently resolved by majority vote alone.
3. **Can an LLM hallucinate expected data?** Yes — an LLM can confidently invent a plausible-sounding function-data link with no real basis. Mitigation: all LLM output is `status: draft` until validated (Part 11); no draft mapping feeds Expected Data Profiles used for FDO scoring.
4. **Can secondary purposes create false FDO findings?** Yes, if secondary-purpose collection is under-recognized. Mitigation: Part 8's explicit AND-rule and the dedicated L4 sub-typed tier exist specifically to prevent this; "Secondary-Purpose — Unverified" is a routing state distinct from "FDO."
5. **Can optional features create false positives?** Yes, if a feature's existence isn't verified. Mitigation: L3 requires citing evidence the optional feature actually exists (app-store description, documentation) — not simply "this data *could* support some feature."
6. **Can different implementations of the same function require different data?** Yes (e.g., two navigation apps, one with AR, one without). Mitigation: features are modeled separately from functions precisely so implementation variance doesn't get baked into the function-level mapping; per-app instantiation records which features are actually present.
7. **Can application categories be too broad?** Yes — "Productivity" spans note apps to full office suites. Mitigation: category is explicitly downgraded to a "weak prior, not determinative" (Part 1); actual necessity judgments happen at the function level, where the taxonomy is far more granular.
8. **Can privacy policies omit legitimate purposes?** Yes, and that's arguably itself a compliance issue, not an ontology flaw — but it risks the detector flagging FDO where the real problem is *policy vagueness*, not *overreach*. Mitigation: this is flagged as a distinct output category ("declared without matched purpose — possible omission or possible overreach") rather than collapsed into FDO, deferred to the policy-extraction stage to disambiguate.
9. **Can one data type serve multiple purposes?** Yes, routinely (e.g., location for both navigation and fraud detection). Mitigation: the attributed tuple model (Part 9) allows the same data type to have multiple (function, purpose, necessity) entries simultaneously rather than one global necessity score.
10. **Can the ontology become too subjective to evaluate?** Risk is real if IAA is low. Mitigation: Part 15's hard gates (explainability 100%, Alpha ≥0.7 for validated status) mean low-agreement mappings simply don't graduate to "validated" — subjectivity is bounded by making non-agreement a blocking condition rather than an accepted noise floor.

---

## PART 19 — Final Stage-2 Deliverables Summary

- **A.** Functional Data Ontology Specification — Parts 1–2, 9–11
- **B.** Application Function Taxonomy — Part 3
- **C.** Data-Type Taxonomy (with crosswalks to GDPR/CCPA/Play Data Safety) — Part 4
- **D.** Necessity Model (six-level graded scale) — Part 5
- **E.** Function–Data Mapping Table + 10 detailed profiles — Parts 6–7
- **F.** Evidence Model (LLM inference explicitly subordinate to validated evidence) — Part 11
- **G.** Annotation Protocol (Krippendorff's Alpha-based IAA) — Part 12
- **H.** Pilot Dataset Specification (20–50 apps) — Part 13
- **I.** Machine-Readable Schema (JSON now; Neo4j property graph recommended for production) — Part 14
- **J.** Validation Plan (coverage/consistency/agreement/extensibility/explainability/robustness) — Part 15
- **K.** FDO Integration Specification — Part 16

---

## FINAL STAGE-2 DECISION

1. **Is the ontology sufficiently rigorous?** Structurally yes — it has graded necessity, mandatory evidence, explicit ambiguity handling, and a validation gate. It is *not yet empirically validated*; rigor of the design must still be confirmed against real inter-annotator agreement data from the pilot.
2. **Is the necessity model defensible?** Yes, as a *reproducible representation of expert judgment* — it does not claim objectivity, which is itself the defensible position given Rule 1.
3. **Which mappings are high-confidence?** Core L1/L5 mappings for well-understood, narrow functions (navigation→precise location; video calling→camera; voice calling→microphone) — these rest on domain reasoning strong enough to need minimal annotation overhead.
4. **Which mappings require human/domain-expert validation?** Nearly all L4 secondary-purpose mappings (especially fraud/security and advertising), and any regulatory-driven L1 claims in Banking/Healthcare (KYC, HIPAA-adjacent), plus every LLM-proposed draft mapping before it can be used downstream.
5. **What ambiguity remains?** Category boundary cases (super-apps, multi-purpose utility apps); the line between L2 (supportive) and L3 (optional-feature) when a "feature" is not cleanly separable from the core function; how strictly to weight app-store descriptions vs. actual observed behavior (not analyzed until a later, behavioral-analysis stage).
6. **Is the ontology suitable for automated FDO detection?** As a *lookup and comparison structure*, yes, provided it only supplies validated (not draft) mappings to the detector, and the AND-gated FDO-eligibility rule from Part 8 is implemented faithfully — a naive difference-of-sets approach on this ontology would still generate false positives.
7. **What must be changed before Stage 3?** Nothing structural is blocking; the pilot dataset must actually be annotated and its Krippendorff's Alpha measured before claiming validation status — Stage 2 as designed here is the *specification*, and Stage 3 (or a Stage 2b) must execute the pilot annotation round and report real agreement numbers before the ontology is called "validated" rather than "candidate."
8. **What exact artifacts should Stage 3 produce?** (a) Executed pilot annotation results with measured Krippendorff's Alpha per dimension; (b) a revised/finalized necessity model if agreement is low on any tier; (c) the function-extraction methodology for turning arbitrary app descriptions into taxonomy function IDs (not yet designed here); (d) the privacy-policy declared-data extraction methodology (separate NLP pipeline); (e) a first draft of the Functional Comparison / FDO-eligibility algorithm operating on the validated ontology, still without building the full production knowledge graph or detector.
