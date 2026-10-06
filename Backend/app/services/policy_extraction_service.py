import re
from uuid import uuid4
from app.services.ai_service import extract_policy_evidence_with_ai
from app.services.evidence_validation_service import (
    validate_policy_evidence,
)

def extract_policy_evidence(
    policy_text: str,
    application_name: str,
) -> list[dict]:
    text = policy_text.strip()

    if not text:
        return []
    try:
        ai_evidence = extract_policy_evidence_with_ai(
            text,
            application_name,
        )

        validated_ai_evidence = validate_policy_evidence(
            ai_evidence
        )

        if validated_ai_evidence:
            for item in validated_ai_evidence:
                item["evidence_id"] = (
                    f"AI-{uuid4().hex[:8]}"
                )

            return validated_ai_evidence

    except Exception:
        pass

    evidence = []

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text,
    )

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        lower = sentence.lower()

        data_type = None
        purpose = None

        if "precise location" in lower or "exact location" in lower:
            data_type = "LOCATION.PRECISE"
        elif "approximate location" in lower or "coarse location" in lower:
            data_type = "LOCATION.APPROXIMATE"
        elif "location" in lower:
            data_type = "LOCATION"

        if "navigation" in lower or "directions" in lower:
            purpose = "NAVIGATION"
        elif "nearby" in lower or "local" in lower:
            purpose = "LOCATION_BASED_SERVICES"
        elif "traffic" in lower:
            purpose = "TRAFFIC"
        elif "personalization" in lower:
            purpose = "PERSONALIZATION"

        if data_type is None:
            continue

        evidence.append(
            {
                "evidence_id": (
                    f"EXTRACTED-{uuid4().hex[:8]}"
                ),
                "data_type": data_type,
                "purpose": purpose,
                "entity": application_name,
                "sharing": None,
                "retention": None,
                "evidence_text": sentence,
                "source_section": None,
                "extraction_status": "EXTRACTED",
                "confidence": 0.80,
            }
        )

    return validate_policy_evidence(evidence)
