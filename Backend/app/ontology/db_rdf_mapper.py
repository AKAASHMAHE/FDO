"""
Adapter for converting DB/ORM records into FDO ontology objects.
"""

from .classes import (
    Application,
    Function,
    ExpectedData,
    DeclaredData,
)


def _get(record, field, default=None):
    """
    Read a field from either a dictionary or an ORM object.
    """
    if isinstance(record, dict):
        return record.get(field, default)

    return getattr(record, field, default)


def application_from_record(record) -> Application:
    """
    Convert an Application ORM/dict record
    into an FDO Application.
    """
    return Application(
        id=str(_get(record, "application_id", "")),
        name=str(_get(record, "application_name", "")),
        category=_get(record, "category"),
        description=_get(record, "description"),
    )


def function_from_record(record) -> Function:
    """
    Convert a Function ORM/dict record
    into an FDO Function.

    function_record_id is used as the semantic
    resource identity because ExpectedMapping
    references this value.
    """
    return Function(
        id=str(_get(record, "function_record_id", "")),
        name=str(_get(record, "function_name", "")),
        description=_get(record, "description"),
    )


def expected_data_from_record(record) -> ExpectedData:
    """
    Convert an ExpectedMapping ORM/dict record
    into an FDO ExpectedData object.
    """
    return ExpectedData(
        id=str(_get(record, "expected_id", "")),
        name=str(_get(record, "data_type", "")),
        data_type=_get(record, "data_type"),
        necessity=_get(record, "necessity"),
        purpose=_get(record, "expected_purpose"),
    )


def declared_data_from_record(record) -> DeclaredData:
    """
    Convert a PolicyEvidence ORM/dict record
    into an FDO DeclaredData object.
    """
    return DeclaredData(
        id=str(_get(record, "evidence_id", "")),
        name=str(_get(record, "data_type", "")),
        data_type=_get(record, "data_type"),
        purpose=_get(record, "purpose"),
        sharing=_get(record, "sharing"),
        retention=_get(record, "retention"),
        extraction_status=_get(record, "extraction_status"),
        confidence=_get(record, "confidence"),
        evidence_text=_get(record, "evidence_text"),
        entity=_get(record, "entity"),
    )