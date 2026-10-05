"""
Adapter for converting DB-shaped records into FDO ontology objects.
"""

from .classes import (
    Application,
    Function,
    ExpectedData,
    DeclaredData,
)


def _get(record, field, default=None):
    if isinstance(record, dict):
        return record.get(field, default)

    return getattr(record, field, default)


def application_from_record(record) -> Application:
    return Application(
        id=str(_get(record, "id")),
        name=str(_get(record, "name", "")),
    )


def function_from_record(record) -> Function:
    return Function(
        id=str(_get(record, "id")),
        name=str(_get(record, "name", "")),
    )


def expected_data_from_record(record) -> ExpectedData:
    return ExpectedData(
        id=str(_get(record, "id")),
        name=str(_get(record, "name", "")),
        data_type=_get(record, "data_type"),
        necessity=_get(record, "necessity"),
        purpose=_get(record, "purpose"),
    )


def declared_data_from_record(record) -> DeclaredData:
    return DeclaredData(
        id=str(_get(record, "id")),
        name=str(_get(record, "name", "")),
        data_type=_get(record, "data_type"),
        purpose=_get(record, "purpose"),
    )