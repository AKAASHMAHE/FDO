from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.expected_mapping import ExpectedMapping
from app.models.function import Function
from app.services.ai_service import (
    ALLOWED_DATA_TYPES,
    generate_functional_baseline_with_ai,
)
from app.services.expected_mapping_service import (
    get_expected_mappings_by_application,
)


BASELINE_CURATED = "CURATED"
BASELINE_AI_DERIVED = "AI_DERIVED"
AI_SOURCE_PREFIX = "AI_DERIVED"

ALLOWED_NECESSITY = {
    "REQUIRED",
    "OPTIONAL",
    "NOT_REQUIRED",
}


@dataclass
class BaselineGenerationResult:
    source: str | None
    available: bool
    generated: bool
    confidence: float | None
    status: str


def _slug(value: str) -> str:
    normalized = re.sub(
        r"[^A-Z0-9]+",
        "-",
        value.strip().upper(),
    ).strip("-")

    return normalized or "FUNCTION"


def _stable_suffix(*parts: str) -> str:
    value = "|".join(parts)
    return hashlib.sha1(
        value.encode("utf-8")
    ).hexdigest()[:10].upper()


def _source_version(
    confidence: float | None,
) -> str:
    if confidence is None:
        return AI_SOURCE_PREFIX

    return f"{AI_SOURCE_PREFIX}:confidence={confidence:.2f}"


def baseline_source_for_mapping(
    mapping: ExpectedMapping,
) -> str:
    source_version = (
        mapping.source_version or ""
    ).upper()

    if source_version.startswith(AI_SOURCE_PREFIX):
        return BASELINE_AI_DERIVED

    return BASELINE_CURATED


def baseline_confidence_for_mapping(
    mapping: ExpectedMapping,
) -> float | None:
    source_version = mapping.source_version or ""

    match = re.search(
        r"confidence=([0-9]*\.?[0-9]+)",
        source_version,
        flags=re.I,
    )

    if not match:
        return None

    value = float(match.group(1))
    return max(0.0, min(1.0, value))


def get_baseline_source(
    mappings: list[ExpectedMapping],
) -> str | None:
    if not mappings:
        return None

    if any(
        baseline_source_for_mapping(mapping) == BASELINE_CURATED
        for mapping in mappings
    ):
        return BASELINE_CURATED

    return BASELINE_AI_DERIVED


def get_baseline_confidence(
    mappings: list[ExpectedMapping],
) -> float | None:
    values = [
        baseline_confidence_for_mapping(mapping)
        for mapping in mappings
        if baseline_source_for_mapping(mapping)
        == BASELINE_AI_DERIVED
    ]
    values = [
        value for value in values if value is not None
    ]

    if not values:
        return None

    return sum(values) / len(values)


def _clamp_confidence(value) -> float | None:
    if value is None:
        return None

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    return max(0.0, min(1.0, number))


def _validate_payload(payload: dict | None) -> list[dict]:
    if not isinstance(payload, dict):
        return []

    functions = payload.get("functions")

    if not isinstance(functions, list):
        return []

    validated = []

    for function in functions:
        if not isinstance(function, dict):
            continue

        function_name = str(
            function.get("function_name") or ""
        ).strip()

        if not function_name:
            continue

        expected_data = function.get("expected_data")

        if not isinstance(expected_data, list):
            continue

        validated_data = []

        for item in expected_data:
            if not isinstance(item, dict):
                continue

            data_type = str(
                item.get("data_type") or ""
            ).strip().upper()

            if data_type not in ALLOWED_DATA_TYPES:
                continue

            necessity = str(
                item.get("necessity") or ""
            ).strip().upper()

            if necessity not in ALLOWED_NECESSITY:
                continue

            if necessity == "NOT_REQUIRED":
                continue

            purpose = str(
                item.get("purpose") or ""
            ).strip()

            if not purpose:
                continue

            validated_data.append(
                {
                    "data_type": data_type,
                    "necessity": necessity,
                    "purpose": purpose[:500],
                    "justification": str(
                        item.get("justification") or ""
                    ).strip()[:1000]
                    or None,
                    "confidence": _clamp_confidence(
                        item.get("confidence")
                    ),
                }
            )

        if validated_data:
            validated.append(
                {
                    "function_name": function_name[:255],
                    "description": str(
                        function.get("description") or ""
                    ).strip()[:1000]
                    or None,
                    "expected_data": validated_data,
                }
            )

    return validated


def ensure_functional_baseline(
    session: Session,
    application: Application,
) -> BaselineGenerationResult:
    existing_mappings = get_expected_mappings_by_application(
        session,
        application.application_id,
    )

    if existing_mappings:
        return BaselineGenerationResult(
            source=get_baseline_source(existing_mappings),
            available=True,
            generated=False,
            confidence=get_baseline_confidence(
                existing_mappings
            ),
            status=(
                "PROVISIONAL"
                if get_baseline_source(existing_mappings)
                == BASELINE_AI_DERIVED
                else "AVAILABLE"
            ),
        )

    try:
        payload = generate_functional_baseline_with_ai(
            application_name=application.application_name,
            category=application.category,
            description=application.description,
        )
    except Exception:
        return BaselineGenerationResult(
            source=None,
            available=False,
            generated=False,
            confidence=None,
            status="FAILED",
        )

    functions = _validate_payload(payload)

    if not functions:
        return BaselineGenerationResult(
            source=None,
            available=False,
            generated=False,
            confidence=None,
            status="UNAVAILABLE",
        )

    confidence_values = []

    for function_index, function in enumerate(
        functions,
        start=1,
    ):
        function_id = (
            f"AI-FUNC-{_slug(function['function_name'])}"
        )[:100]
        function_record_id = (
            f"{application.application_id}:"
            f"{function_id}:AI"
        )[:150]

        function_record = session.get(
            Function,
            function_record_id,
        )

        if function_record is None:
            function_record = Function(
                function_record_id=function_record_id,
                function_id=function_id,
                application_id=application.application_id,
                function_name=function["function_name"],
                feature=BASELINE_AI_DERIVED,
                description=function["description"],
            )
            session.add(function_record)

        for item_index, item in enumerate(
            function["expected_data"],
            start=1,
        ):
            suffix = _stable_suffix(
                application.application_id,
                function["function_name"],
                item["data_type"],
                item["purpose"],
            )
            expected_id = (
                f"AI-EXP-{application.application_id}-"
                f"{function_index:02d}-{item_index:02d}-"
                f"{suffix}"
            )[:100]

            if session.get(ExpectedMapping, expected_id):
                continue

            existing_statement = select(
                ExpectedMapping
            ).where(
                ExpectedMapping.application_id
                == application.application_id,
                ExpectedMapping.function_record_id
                == function_record_id,
                ExpectedMapping.data_type
                == item["data_type"],
                ExpectedMapping.expected_purpose
                == item["purpose"],
            )

            if session.scalars(existing_statement).first():
                continue

            confidence = item["confidence"]

            if confidence is not None:
                confidence_values.append(confidence)

            session.add(
                ExpectedMapping(
                    expected_id=expected_id,
                    application_id=application.application_id,
                    function_record_id=function_record_id,
                    data_type=item["data_type"],
                    necessity=item["necessity"],
                    expected_purpose=item["purpose"],
                    source_version=_source_version(confidence),
                    baseline_justification=item.get(
                        "justification"
                    ),
                )
            )

    session.flush()

    persisted_mappings = get_expected_mappings_by_application(
        session,
        application.application_id,
    )

    return BaselineGenerationResult(
        source=BASELINE_AI_DERIVED,
        available=bool(persisted_mappings),
        generated=bool(persisted_mappings),
        confidence=(
            sum(confidence_values) / len(confidence_values)
            if confidence_values
            else get_baseline_confidence(persisted_mappings)
        ),
        status=(
            "PROVISIONAL"
            if persisted_mappings
            else "UNAVAILABLE"
        ),
    )
