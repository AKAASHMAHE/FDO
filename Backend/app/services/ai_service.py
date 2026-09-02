import json
import os
from pathlib import Path

from google import genai


MODEL_NAME = "gemini-3.5-flash-lite"


def _load_env_file() -> None:
    env_path = Path(".env")

    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)

        if key.strip() not in os.environ:
            os.environ[key.strip()] = value.strip()


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
        raise RuntimeError("GEMINI_API_KEY is not configured")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a privacy-policy evidence extraction assistant for the
FDO-Privacy project.

Application:
{application_name}

Extract ONLY information explicitly supported by the privacy-policy
text below.

Do NOT infer information that is not stated.
Do NOT decide whether something is FDO, NOT_FDO, or AMBIGUOUS.

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

Allowed data_type values include:
- LOCATION.PRECISE
- LOCATION.APPROXIMATE
- LOCATION
- CONTACTS
- DEVICE
- ACCOUNT
- FINANCIAL
- HEALTH
- MEDIA
- USAGE
- OTHER

If the policy does not provide enough information to identify a
supported data type, do not invent one.

The confidence must be between 0.0 and 1.0.

Privacy-policy text:
{text}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    raw_text = (response.text or "").strip()

    print("\n===== RAW GEMINI RESPONSE =====")
    print(raw_text)
    print("===== END RAW RESPONSE =====\n")

    if not raw_text:
        return []

    try:
        if raw_text.startswith("```"):
            raw_text = raw_text.strip()
            lines = raw_text.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            raw_text = "\n".join(lines).strip()

        parsed = json.loads(raw_text)

    except json.JSONDecodeError:
        print("Gemini returned invalid JSON.")
        return []

    evidence = parsed.get("evidence", [])

    if not isinstance(evidence, list):
        return []

    results = []

    for item in evidence:
        if not isinstance(item, dict):
            continue

        results.append(
            {
                "data_type": item.get("data_type"),
                "purpose": item.get("purpose"),
                "entity": item.get("entity"),
                "sharing": item.get("sharing"),
                "retention": item.get("retention"),
                "evidence_text": item.get("evidence_text"),
                "source_section": item.get("source_section"),
                "extraction_status": "EXTRACTED",
                "confidence": item.get("confidence"),
            }
        )

    return results