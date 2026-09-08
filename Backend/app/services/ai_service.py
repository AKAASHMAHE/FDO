import json
import os
from pathlib import Path

from google import genai


MODEL_NAME = "gemini-3.5-flash-lite"


ALLOWED_DATA_TYPES = {
    "DATA.LOCATION.PRECISE",
    "DATA.LOCATION.APPROXIMATE",
    "DATA.LOCATION",
    "DATA.CONTACTS",
    "DATA.DEVICE",
    "DATA.ACCOUNT",
    "DATA.FINANCIAL",
    "DATA.HEALTH",
    "DATA.MEDIA",
    "DATA.USAGE",
    "DATA.OTHER",
}


DATA_TYPE_NORMALIZATION = {
    "LOCATION.PRECISE": "DATA.LOCATION.PRECISE",
    "LOCATION.APPROXIMATE": "DATA.LOCATION.APPROXIMATE",
    "LOCATION": "DATA.LOCATION",
    "CONTACTS": "DATA.CONTACTS",
    "DEVICE": "DATA.DEVICE",
    "ACCOUNT": "DATA.ACCOUNT",
    "FINANCIAL": "DATA.FINANCIAL",
    "HEALTH": "DATA.HEALTH",
    "MEDIA": "DATA.MEDIA",
    "USAGE": "DATA.USAGE",
    "OTHER": "DATA.OTHER",
}


def _load_env_file() -> None:
    env_path = Path(".env")

    if not env_path.exists():
        return

    for line in env_path.read_text(
        encoding="utf-8"
    ).splitlines():

        line = line.strip()

        if (
            not line
            or line.startswith("#")
            or "=" not in line
        ):
            continue

        key, value = line.split("=", 1)

        if key.strip() not in os.environ:
            os.environ[key.strip()] = value.strip()


def _normalize_data_type(
    data_type: str | None,
) -> str | None:
    if data_type is None:
        return None

    value = str(data_type).strip().upper()

    if value in ALLOWED_DATA_TYPES:
        return value

    if value in DATA_TYPE_NORMALIZATION:
        return DATA_TYPE_NORMALIZATION[value]

    return None


def extract_policy_evidence_with_ai(
    policy_text: str,
    application_name: str,
) -> list[dict]:
    """
    Use Gemini to extract structured privacy-policy evidence.

    Gemini is only responsible for evidence extraction.
    It does not make an FDO decision.
    """

    text = policy_text.strip()

    if not text:
        return []

    _load_env_file()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured"
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
You are a privacy-policy evidence extraction assistant
for the FDO-Privacy project.

Application:
{application_name}

Extract ONLY information explicitly supported by the
privacy-policy text below.

Do NOT infer information that is not stated.
Do NOT decide whether something is FDO, NOT_FDO,
or AMBIGUOUS.

Return ONLY valid JSON in this exact structure:

{{
  "evidence": [
    {{
      "data_type": "string or null",
      "purpose": "string or null",
      "entity": "string or null",
      "sharing": "string or null",
      "retention": "string or null",
      "evidence_text": "exact supporting sentence or phrase",
      "source_section": "string or null",
      "confidence": 0.0
    }}
  ]
}}

IMPORTANT:
The data_type MUST use the canonical FDO-Privacy ontology
identifiers listed below.

Allowed canonical data_type values:

- DATA.LOCATION.PRECISE
- DATA.LOCATION.APPROXIMATE
- DATA.LOCATION
- DATA.CONTACTS
- DATA.DEVICE
- DATA.ACCOUNT
- DATA.FINANCIAL
- DATA.HEALTH
- DATA.MEDIA
- DATA.USAGE
- DATA.OTHER

Do NOT remove the DATA. prefix.

Examples:

Correct:
"DATA.LOCATION.PRECISE"

Correct:
"DATA.LOCATION.APPROXIMATE"

Incorrect:
"LOCATION.PRECISE"

Incorrect:
"LOCATION"

If the policy does not provide enough information to
identify a supported data type, use null rather than
inventing a data type.

The evidence_text must contain the exact supporting
sentence or phrase from the policy text.

The confidence must be between 0.0 and 1.0.

Privacy-policy text:
{text}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    raw_text = (
        response.text or ""
    ).strip()

    if not raw_text:
        return []

    try:
        if raw_text.startswith("```"):
            raw_text = raw_text.strip()

            lines = raw_text.splitlines()

            if (
                lines
                and lines[0].startswith("```")
            ):
                lines = lines[1:]

            if (
                lines
                and lines[-1].strip() == "```"
            ):
                lines = lines[:-1]

            raw_text = "\n".join(
                lines
            ).strip()

        parsed = json.loads(
            raw_text
        )

    except json.JSONDecodeError:
        return []

    evidence = parsed.get(
        "evidence",
        [],
    )

    if not isinstance(
        evidence,
        list,
    ):
        return []

    results = []

    for item in evidence:

        if not isinstance(
            item,
            dict,
        ):
            continue

        normalized_data_type = (
            _normalize_data_type(
                item.get("data_type")
            )
        )

        if (
            item.get("data_type") is not None
            and normalized_data_type is None
        ):
            continue

        results.append(
            {
                "data_type": normalized_data_type,
                "purpose": item.get(
                    "purpose"
                ),
                "entity": item.get(
                    "entity"
                ),
                "sharing": item.get(
                    "sharing"
                ),
                "retention": item.get(
                    "retention"
                ),
                "evidence_text": item.get(
                    "evidence_text"
                ),
                "source_section": item.get(
                    "source_section"
                ),
                "extraction_status": "EXTRACTED",
                "confidence": item.get(
                    "confidence"
                ),
            }
        )

    return results