from dataclasses import dataclass

PURPOSE_CATEGORIES = {
    "NAVIGATION": {
        "navigation",
        "directions",
        "route planning",
        "route guidance",
        "turn by turn directions",
        "nearby search",
        "finding nearby places",
    },
    "COMMUNICATION": {
        "messaging",
        "message",
        "calling",
        "calls",
        "communication",
        "contacting users",
    },
    "SOCIAL_INTERACTION": {
        "social interaction",
        "sharing",
        "connecting with friends",
        "social networking",
    },
    "ACCOUNT_MANAGEMENT": {
        "account creation",
        "account management",
        "authentication",
        "login",
        "sign in",
        "user account",
    },
    "PAYMENT_PROCESSING": {
        "payments",
        "payment processing",
        "transactions",
        "purchases",
        "processing payments",
    },
    "MEDIA": {
        "media",
        "video",
        "videos",
        "music",
        "playing media",
        "media content",
    },
    "SEARCH": {
        "search",
        "searching",
        "finding information",
        "querying content",
    },
    "SECURITY": {
        "security",
        "fraud prevention",
        "abuse prevention",
        "protecting accounts",
        "account security",
    },
    "SERVICE_OPERATION": {
        "providing the service",
        "service operation",
        "operating the application",
        "maintaining functionality",
        "service functionality",
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
        NO_MATCH
        NO_EVIDENCE
    """

    if not declared_data_type:
        return "NO_EVIDENCE"

    if expected_data_type == declared_data_type:
        return "EXACT_MATCH"

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

    for category, phrases in PURPOSE_CATEGORIES.items():
        for phrase in phrases:
            if phrase in normalized:
                return category

    return None


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
        COMPATIBLE
        INCOMPATIBLE
        NO_EVIDENCE
    """

    if not declared_purpose:
        return "NO_EVIDENCE"

    expected = normalize_purpose(expected_purpose)
    declared = normalize_purpose(declared_purpose)

    if not expected or not declared:
        return "NO_EVIDENCE"

    # Preserve exact-match behavior.
    if expected == declared:
        return "COMPATIBLE"

    # Classify the expected purpose.
    expected_category = classify_purpose(expected)

    # Classify all declared purposes.
    declared_categories = classify_purposes(declared)

    # If either side cannot be classified,
    # remain conservative.
    if not expected_category or not declared_categories:
        return "INCOMPATIBLE"

    # Multi-purpose compatibility:
    # at least one declared purpose category matching
    # the expected purpose category is sufficient.
    if expected_category in declared_categories:
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
        purpose_compatibility=purpose_compatibility,
        functional_relationship=functional_relationship,
        functional_justification=justification,
        evidence_status=evidence_status,
    )
