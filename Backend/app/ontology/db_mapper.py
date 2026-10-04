"""
FDO Ontology - Database Mapping Layer

Maps existing relational database records into the FDO semantic model.

Important:
    The relational database remains the operational source of truth.
    This layer creates semantic/domain objects from those records.
"""

from typing import Any, Dict, List

from .classes import (
    Application,
    DeclaredData,
    ExpectedData,
    Function,
    Overreach,
    PolicyClause,
    PrivacyPolicy,
)


def _get(record: Any, field: str, default=None):
    """
    Safely read a field from either an ORM object or dictionary.
    """

    if isinstance(record, dict):
        return record.get(field, default)

    return getattr(record, field, default)


def map_application(record: Any) -> Application:
    """
    Map an applications database record to an FDO Application.
    """

    return Application(
        id=str(_get(record, "id")),
        name=str(
            _get(record, "name")
            or _get(record, "app_name")
            or "Unnamed Application"
        ),
        category=_get(record, "category"),
        description=_get(record, "description"),
    )


def map_function(record: Any) -> Function:
    """
    Map a functions database record to an FDO Function.
    """

    return Function(
        id=str(_get(record, "id")),
        name=str(
            _get(record, "name")
            or _get(record, "function_name")
            or "Unnamed Function"
        ),
        description=_get(record, "description"),
    )


def map_expected_mapping(record: Any) -> ExpectedData:
    """
    Map an expected_mappings record to FDO ExpectedData.
    """

    data_type = (
        _get(record, "data_type")
        or _get(record, "expected_data_type")
        or ""
    )

    return ExpectedData(
        id=str(_get(record, "id")),
        name=f"Expected {data_type}".strip(),
        data_type=str(data_type),
        necessity=_get(record, "necessity"),
        purpose=_get(record, "purpose"),
    )


def map_policy_document(record: Any) -> PrivacyPolicy:
    """
    Map a policy_documents record to FDO PrivacyPolicy.
    """

    return PrivacyPolicy(
        id=str(_get(record, "id")),
        name=str(
            _get(record, "name")
            or _get(record, "title")
            or "Privacy Policy"
        ),
        source=_get(record, "source"),
        version=_get(record, "version"),
    )


def map_policy_evidence(record: Any) -> PolicyClause:
    """
    Map policy evidence into an FDO PolicyClause.
    """

    text = (
        _get(record, "text")
        or _get(record, "evidence_text")
        or _get(record, "clause_text")
        or ""
    )

    return PolicyClause(
        id=str(_get(record, "id")),
        name=f"Policy Clause {_get(record, 'id')}",
        text=str(text),
        source=_get(record, "source"),
        section=_get(record, "section"),
    )


def map_declared_data(record: Any) -> DeclaredData:
    """
    Map normalized/declared evidence into FDO DeclaredData.
    """

    data_type = (
        _get(record, "data_type")
        or _get(record, "declared_data_type")
        or ""
    )

    return DeclaredData(
        id=str(_get(record, "id")),
        name=f"Declared {data_type}".strip(),
        data_type=str(data_type),
        purpose=_get(record, "purpose"),
        sharing=_get(record, "sharing"),
        retention=_get(record, "retention"),
    )


def map_fdo_result(record: Any) -> Overreach:
    """
    Map an existing FDO result into an FDO Overreach object.

    This preserves the existing deterministic FDO engine result.
    """

    return Overreach(
        id=str(_get(record, "id")),
        name=f"FDO Finding {_get(record, 'id')}",
        status=_get(record, "fdo_status") or _get(record, "status"),
        reason=_get(record, "decision_reason") or _get(record, "reason"),
        confidence=_get(record, "decision_confidence")
        or _get(record, "confidence"),
    )


def map_records(
    *,
    applications=None,
    functions=None,
    expected_mappings=None,
    policy_documents=None,
    policy_evidence=None,
    declared_data=None,
    fdo_results=None,
) -> Dict[str, List[Any]]:
    """
    Convert collections of database records into semantic FDO objects.
    """

    return {
        "applications": [
            map_application(record)
            for record in (applications or [])
        ],
        "functions": [
            map_function(record)
            for record in (functions or [])
        ],
        "expected_data": [
            map_expected_mapping(record)
            for record in (expected_mappings or [])
        ],
        "privacy_policies": [
            map_policy_document(record)
            for record in (policy_documents or [])
        ],
        "policy_clauses": [
            map_policy_evidence(record)
            for record in (policy_evidence or [])
        ],
        "declared_data": [
            map_declared_data(record)
            for record in (declared_data or [])
        ],
        "overreach": [
            map_fdo_result(record)
            for record in (fdo_results or [])
        ],
    }