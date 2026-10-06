import re


PRIVACY_DATA_KEYWORDS = {
    "account",
    "activity",
    "advertising id",
    "biometric",
    "browsing",
    "camera",
    "contact",
    "cookie",
    "device",
    "email",
    "financial",
    "health",
    "identifier",
    "ip address",
    "location",
    "microphone",
    "name",
    "payment",
    "personal data",
    "personal information",
    "phone",
    "photo",
    "precise location",
    "profile",
    "usage",
    "user id",
}


PROCESSING_KEYWORDS = {
    "collect",
    "disclose",
    "gather",
    "process",
    "receive",
    "retain",
    "share",
    "store",
    "use",
}


OPERATIONAL_NOISE = {
    "delivery is retried",
    "delivery retry",
    "generic platform operations",
    "infrastructure improvements",
    "infrastructure reliability",
    "reliability",
    "security improvements",
    "server uptime",
    "service availability",
    "software behavior",
    "system maintenance",
}


GENERIC_OPERATIONAL_PURPOSES = {
    "delivery is retried",
    "infrastructure improvements",
    "infrastructure reliability",
    "platform operations",
    "reliability",
    "security",
    "service availability",
    "system maintenance",
}


VALID_DATA_TYPES = {
    "DATA.LOCATION.PRECISE",
    "DATA.LOCATION.APPROXIMATE",
    "DATA.LOCATION",
    "DATA.CONTACTS",
    "DATA.DEVICE",
    "DATA.ACCOUNT",
    "DATA.FINANCIAL",
    "DATA.HEALTH",
    "DATA.MEDIA",
    "DATA.MEDIA.CAMERA",
    "DATA.MEDIA.MICROPHONE",
    "DATA.MEDIA.PHOTO",
    "DATA.MEDIA.VIDEO",
    "DATA.USAGE",
    "DATA.OTHER",
    "LOCATION.PRECISE",
    "LOCATION.APPROXIMATE",
    "LOCATION",
}


def _normalize_text(value: str | None) -> str:
    if not value:
        return ""

    return " ".join(str(value).strip().lower().split())


def _has_phrase(text: str, phrases: set[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def _looks_like_privacy_evidence(
    evidence_text: str,
    purpose: str | None,
) -> bool:
    text = _normalize_text(evidence_text)
    purpose_text = _normalize_text(purpose)
    combined = f"{text} {purpose_text}".strip()

    if not combined:
        return False

    if _has_phrase(combined, OPERATIONAL_NOISE):
        return False

    has_data = _has_phrase(combined, PRIVACY_DATA_KEYWORDS)
    has_processing = _has_phrase(combined, PROCESSING_KEYWORDS)

    return has_data and has_processing


def _valid_confidence(value) -> float | None:
    if value is None:
        return None

    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return None

    if confidence < 0.0 or confidence > 1.0:
        return None

    return confidence


def validate_policy_evidence_item(
    item: dict,
) -> dict | None:
    data_type = item.get("data_type")

    if not data_type:
        return None

    data_type = str(data_type).strip().upper()

    if data_type not in VALID_DATA_TYPES:
        return None

    evidence_text = item.get("evidence_text")

    if not evidence_text or not str(evidence_text).strip():
        return None

    if not _looks_like_privacy_evidence(
        str(evidence_text),
        item.get("purpose"),
    ):
        return None

    if data_type == "DATA.OTHER":
        normalized = _normalize_text(evidence_text)

        if not _has_phrase(
            normalized,
            PRIVACY_DATA_KEYWORDS,
        ):
            return None

    validated = dict(item)
    validated["data_type"] = data_type
    validated["evidence_text"] = re.sub(
        r"\s+",
        " ",
        str(evidence_text).strip(),
    )
    validated["extraction_status"] = (
        validated.get("extraction_status") or "EXTRACTED"
    )
    validated["confidence"] = _valid_confidence(
        validated.get("confidence")
    )

    return validated


def validate_policy_evidence(
    evidence: list[dict],
) -> list[dict]:
    validated = []
    seen = set()

    for item in evidence:
        if not isinstance(item, dict):
            continue

        valid_item = validate_policy_evidence_item(item)

        if valid_item is None:
            continue

        key = (
            valid_item.get("data_type"),
            _normalize_text(valid_item.get("purpose")),
            _normalize_text(valid_item.get("evidence_text")),
        )

        if key in seen:
            continue

        seen.add(key)
        validated.append(valid_item)

    return validated


def is_semantic_finding_usable(
    finding: dict,
) -> bool:
    declared_type = str(
        finding.get("declared_type") or ""
    ).strip().upper()

    expected_type = str(
        finding.get("expected_type") or ""
    ).strip().upper()

    declared_purpose = _normalize_text(
        finding.get("declared_purpose")
    )

    declared_data = _normalize_text(
        finding.get("declared_data")
    )

    combined = (
        f"{declared_type} {declared_purpose} {declared_data}"
        .strip()
        .lower()
    )

    if not declared_type or not expected_type:
        return False

    if declared_type not in VALID_DATA_TYPES:
        return False

    if _has_phrase(combined, OPERATIONAL_NOISE):
        return False

    if _has_phrase(declared_purpose, GENERIC_OPERATIONAL_PURPOSES):
        return False

    if declared_type == "DATA.OTHER":
        return False

    if not declared_purpose:
        return False

    return True
