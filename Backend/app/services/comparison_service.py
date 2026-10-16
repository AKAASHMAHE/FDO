from dataclasses import dataclass

from app.services.data_type_hierarchy import data_type_relation

PURPOSE_CATEGORIES = {
    "NAVIGATION": {
        "navigation",
        "directions",
        "route planning",
        "route guidance",
        "turn by turn directions",
        "nearby search",
        "finding nearby places",
        "live trip tracking",
        "live delivery tracking",
        "real time traffic",
        "traffic road guidance",
        "pickup routing",
        "delivery address and shipping calculation",
        "determine user position and provide real time navigation",
        "automatic arrival check in",
        "real time traffic navigation",
        "route navigation",
    },
    "COMMUNICATION": {
        "messaging",
        "message",
        "calling",
        "calls",
        "communication",
        "contacting users",
        "chat",
        "core messaging",
        "direct messaging",
        "medical communication",
        "video call",
        "video calling",
        "video consultation",
        "video meeting",
        "video visit",
        "voice call",
        "voice command",
        "voice video calling",
        "communication collaboration",
        "recipient identification",
    },
    "SOCIAL_INTERACTION": {
        "social interaction",
        "sharing",
        "connecting with friends",
        "social networking",
        "friend team discovery",
        "contact discovery and connection",
        "content posting",
        "social posting",
        "commenting",
        "posting",
        "media sharing",
        "media file sharing",
        "location sharing",
        "social challenges",
    },
    "ACCOUNT_MANAGEMENT": {
        "account creation",
        "account management",
        "authentication",
        "login",
        "sign in",
        "user account",
        "one time authentication",
        "player account identification",
        "player identification matchmaking",
        "user identification and account management",
        "user authentication and profile management",
        "authenticate users and manage profile access",
        "user authentication for cross device sync services",
        "user authentication for cross device synchronization",
        "user authentication and profile synchronization",
    },
    "PAYMENT_PROCESSING": {
        "payments",
        "payment processing",
        "transactions",
        "purchases",
        "processing payments",
        "payment transaction",
        "bill payment",
        "purchase transaction",
        "shopping cart",
        "transaction",
        "payment processing and order settlement",
    },
    "MEDIA": {
        "media",
        "video",
        "videos",
        "func.com.video",
        "music",
        "playing media",
        "media content",
        "video playback",
        "offline viewing",
        "photo video management",
        "editing",
    },
    "SEARCH": {
        "search",
        "searching",
        "finding information",
        "querying content",
        "search discovery",
        "search organization",
        "search history and preferences",
        "browsing history and cache management",
        "managing browsing history cache and cookies",
        "browsing history",
        "search personalization",
        "localized search",
        "localized restaurant discovery",
        "provider discovery",
        "contextualize local search results",
        "fulfill website geolocation requests",
    },
    "SEARCH_LOCATION": {
        "localization",
        "localized",
        "location based",
        "search localization",
        "sync saved locations and preferences across devices",
    },
    "SECURITY": {
        "security",
        "fraud prevention",
        "abuse prevention",
        "protecting accounts",
        "account security",
        "security fraud protection",
        "security verification",
        "verification",
    },
    "SERVICE_OPERATION": {
        "providing the service",
        "service operation",
        "operating the application",
        "maintaining functionality",
        "service functionality",
        "local offline file access",
        "offline local file access",
        "device identification for rendering and network communication",
        "device identification for network requests and webpage rendering compatibility",
        "hardware and os identification for rendering and network requests",
        "appointment booking",
        "booking confirmation",
        "scheduling care",
        "delivery",
        "process user uploaded pdf and document files",
    },
    "ANALYTICS": {
        "analytics",
        "usage analysis",
        "measuring service performance",
        "service analytics",
        "analyzing usage",
    },
    "PERSONALIZATION": {
        "personalization",
        "personalized experience",
        "customized experience",
        "recommendations",
        "personalized recommendations",
        "personalization coaching",
    },
    "ADVERTISING": {
        "advertising",
        "targeted advertising",
        "ad delivery",
        "serving ads",
        "personalized ads",
    },
    "MARKETING": {
        "marketing",
        "promotional communications",
        "promotions",
        "promotional purposes",
    },
    "HEALTHCARE": {
        "health metrics",
        "view health information",
        "health care",
        "provider discovery",
        "medical communication",
    },
    "GAMING": {
        "gameplay",
        "player identification",
        "matchmaking",
    },
    "FILE_STORAGE_SYNC": {
        "file storage sync",
        "backup sync",
        "backup synchronization",
        "sync saved locations and preferences across devices",
    },
    "DEVICE_CONTROL": {
        "device control",
        "device orientation and hardware sensor integration",
    },
    "ACTIVITY_TRACKING": {
        "activity tracking",
        "gps activity tracking",
        "progress tracking",
        "learning activity",
        "assignment classwork",
    },
    "FITNESS_TRACKING": {
        "fitness tracking",
        "health metrics",
        "view health information",
    },
    "EDUCATION": {
        "assignment classwork",
        "learning activity",
        "lesson activity",
    },
}


@dataclass
class ComparisonInput:
    expected_id: str
    application_id: str
    function_record_id: str
    expected_data_type: str
    expected_necessity: str
    expected_purpose: str

    declared_evidence_id: str | None
    declared_data_type: str | None
    declared_purpose: str | None
    declared_sharing: str | None
    declared_retention: str | None


@dataclass
class ComparisonOutput:
    expected_id: str
    declared_evidence_id: str | None

    data_match: str
    data_match_relation: str
    purpose_compatibility: str
    functional_relationship: str
    functional_justification: str
    evidence_status: str


def build_comparison_input(
    expected,
    evidence=None,
) -> ComparisonInput:
    return ComparisonInput(
        expected_id=expected.expected_id,
        application_id=expected.application_id,
        function_record_id=expected.function_record_id,
        expected_data_type=expected.data_type,
        expected_necessity=expected.necessity,
        expected_purpose=expected.expected_purpose,
        declared_evidence_id=(
            evidence.evidence_id if evidence else None
        ),
        declared_data_type=(
            evidence.data_type if evidence else None
        ),
        declared_purpose=(
            evidence.purpose if evidence else None
        ),
        declared_sharing=(
            evidence.sharing if evidence else None
        ),
        declared_retention=(
            evidence.retention if evidence else None
        ),
    )
def evaluate_data_match(
    expected_data_type: str,
    declared_data_type: str | None,
) -> str:
    """
    Compare the expected normalized data type with
    the declared normalized data type.

    Returns:
        EXACT_MATCH
        HIERARCHICAL_MATCH
        NO_MATCH
        NO_EVIDENCE
    """

    if not declared_data_type:
        return "NO_EVIDENCE"

    relation = data_type_relation(
        expected_data_type,
        declared_data_type,
    )
    if relation == "EXACT":
        return "EXACT_MATCH"
    if relation:
        return "HIERARCHICAL_MATCH"

    return "NO_MATCH"
def normalize_purpose(purpose: str | None) -> str:
    """
    Normalize a purpose statement for deterministic comparison.

    Stage 8.6.2:
    Removes superficial formatting differences while
    preserving the underlying purpose meaning.

    Returns:
        Normalized purpose string.
        Empty string when no usable purpose is provided.
    """

    if not purpose:
        return ""

    normalized = purpose.strip().lower()

    if not normalized:
        return ""

    # Normalize common separators.
    replacements = {
        "-": " ",
        "_": " ",
        "/": " ",
    }

    for old, new in replacements.items():
        normalized = normalized.replace(old, new)

    # Collapse repeated whitespace.
    normalized = " ".join(normalized.split())

    return normalized

def classify_purpose(purpose: str | None) -> str | None:
    """
    Classify a normalized purpose into one of the
    controlled purpose categories.

    Stage 8.6.3:
    Uses deterministic keyword/phrase matching.

    Returns:
        Purpose category name, or None if no category
        can be identified.
    """

    normalized = normalize_purpose(purpose)

    if not normalized:
        return None

    matches = [
        (len(phrase), -normalized.find(phrase), category)
        for category, phrases in PURPOSE_CATEGORIES.items()
        for phrase in phrases
        if phrase in normalized
    ]
    return max(matches)[2] if matches else None


def classify_purposes(purpose: str | None) -> list[str]:
    """
    Classify a purpose statement into all matching
    controlled purpose categories.

    Stage 8.6.4:
    Supports multiple purpose categories while
    avoiding generic substring overlaps.

    Categories are returned in the order their
    matched phrases appear in the purpose statement.

    Returns:
        List of matching purpose category names.
        Empty list when no category can be identified.
    """

    normalized = normalize_purpose(purpose)

    if not normalized:
        return []

    phrase_matches = []

    # Find every matching category/phrase.
    for category, phrases in PURPOSE_CATEGORIES.items():
        for phrase in phrases:
            position = normalized.find(phrase)

            if position != -1:
                phrase_matches.append(
                    (category, phrase, position)
                )

    # Process longer phrases first only for overlap resolution.
    phrase_matches.sort(
        key=lambda item: len(item[1]),
        reverse=True,
    )

    selected_matches = []

    for category, phrase, position in phrase_matches:

        # Ignore a generic phrase when it is already
        # contained inside a longer, more specific phrase.
        covered_by_specific_phrase = any(
            other_phrase != phrase
            and len(other_phrase) > len(phrase)
            and phrase in other_phrase
            for _, other_phrase, _ in phrase_matches
        )

        if covered_by_specific_phrase:
            continue

        selected_matches.append(
            (category, phrase, position)
        )

    # Restore the natural order in which purposes
    # appear in the original statement.
    selected_matches.sort(
        key=lambda item: item[2]
    )

    matched_categories = []

    for category, _, _ in selected_matches:
        if category not in matched_categories:
            matched_categories.append(category)

    return matched_categories


def evaluate_purpose_compatibility(
    expected_purpose: str,
    declared_purpose: str | None,
) -> str:
    """
    Evaluate whether the declared purpose is compatible
    with the expected purpose.

    Stage 8.6.4:
    Supports multiple declared purpose categories.

    Returns:
        COMPATIBLE, INCOMPATIBLE, UNKNOWN, or NO_EVIDENCE.
    """

    if not declared_purpose:
        return "NO_EVIDENCE"

    expected = normalize_purpose(expected_purpose)
    declared = normalize_purpose(declared_purpose)

    if not expected or not declared:
        return "NO_EVIDENCE"

    expected_categories = classify_purposes(expected)

    # Classify all declared purposes.
    declared_categories = classify_purposes(declared)

    # If either side cannot be classified, compatibility is unknown.
    if not expected_categories or not declared_categories:
        return "UNKNOWN"

    # Preserve exact-match behavior after confirming both purposes are known.
    if expected == declared:
        return "COMPATIBLE"

    # Multi-purpose compatibility:
    # at least one declared purpose category matching
    # the expected purpose category is sufficient.
    if any(
        category in declared_categories
        for category in expected_categories
    ):
        return "COMPATIBLE"

    return "INCOMPATIBLE"


def classify_purpose_compatibility(
    expected_purpose: str | None,
    declared_purpose: str | None,
) -> str:
    """
    Canonical purpose compatibility helper shared by relational and
    semantic decision paths.
    """

    result = evaluate_purpose_compatibility(
        expected_purpose or "",
        declared_purpose,
    )

    if result == "NO_EVIDENCE":
        return "UNKNOWN"

    return result

def evaluate_functional_relationship(
    declared_evidence_id: str | None,
) -> str:
    """
    Determine whether declared evidence is available for
    functional relationship analysis.

    This is only an evidence-presence baseline.
    It does not make the final FDO decision.

    Returns:
        RELATED
        NO_EVIDENCE
    """

    if not declared_evidence_id:
        return "NO_EVIDENCE"

    return "RELATED"
def evaluate_evidence_status(
    declared_evidence_id: str | None,
    extraction_status: str | None,
) -> str:
    """
    Classify the availability and extraction state of
    declared evidence.

    Returns:
        NO_EVIDENCE
        EXTRACTED
        INSUFFICIENT
        UNKNOWN
    """

    if not declared_evidence_id:
        return "NO_EVIDENCE"

    if not extraction_status:
        return "UNKNOWN"

    status = extraction_status.strip().upper()

    if status == "EXTRACTED":
        return "EXTRACTED"

    if status == "INSUFFICIENT":
        return "INSUFFICIENT"

    return "UNKNOWN"
def build_comparison(
    expected,
    evidence=None,
) -> ComparisonOutput:
    """
    Build a deterministic comparison result from an
    expected mapping and optional declared evidence.

    This function does NOT make the final FDO decision.
    """

    data_match = evaluate_data_match(
        expected.data_type,
        evidence.data_type if evidence else None,
    )
    relation = data_type_relation(
        expected.data_type,
        evidence.data_type if evidence else None,
    )

    purpose_compatibility = evaluate_purpose_compatibility(
        expected.expected_purpose,
        evidence.purpose if evidence else None,
    )

    functional_relationship = evaluate_functional_relationship(
        evidence.evidence_id if evidence else None,
    )

    evidence_status = evaluate_evidence_status(
        evidence.evidence_id if evidence else None,
        evidence.extraction_status if evidence else None,
    )

    if not evidence:
        justification = (
            "No declared evidence is available for comparison."
        )
    else:
        justification = (
            "Declared evidence is available for "
            "data, purpose, and functional analysis."
        )

    return ComparisonOutput(
        expected_id=expected.expected_id,
        declared_evidence_id=(
            evidence.evidence_id if evidence else None
        ),
        data_match=data_match,
        data_match_relation=relation or "NONE",
        purpose_compatibility=purpose_compatibility,
        functional_relationship=functional_relationship,
        functional_justification=justification,
        evidence_status=evidence_status,
    )
