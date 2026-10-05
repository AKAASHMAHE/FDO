from app.ontology.db_rdf_mapper import (
    application_from_record,
    function_from_record,
    expected_data_from_record,
    declared_data_from_record,
)


def test_application_from_orm_style_record():

    record = {
        "application_id": "app-001",
        "application_name": "Navigation App",
        "category": "Navigation",
        "description": "Navigation application",
    }

    result = application_from_record(record)

    assert result.id == "app-001"
    assert result.name == "Navigation App"
    assert result.category == "Navigation"
    assert result.description == "Navigation application"


def test_function_from_orm_style_record():

    record = {
        "function_record_id": "func-record-001",
        "function_id": "navigation",
        "application_id": "app-001",
        "function_name": "Navigation",
        "description": "Navigation feature",
    }

    result = function_from_record(record)

    assert result.id == "func-record-001"
    assert result.name == "Navigation"
    assert result.description == "Navigation feature"


def test_expected_data_from_orm_style_record():

    record = {
        "expected_id": "expected-001",
        "application_id": "app-001",
        "function_record_id": "func-record-001",
        "data_type": "location",
        "necessity": "required",
        "expected_purpose": "navigation",
    }

    result = expected_data_from_record(record)

    assert result.id == "expected-001"
    assert result.data_type == "location"
    assert result.necessity == "required"
    assert result.purpose == "navigation"


def test_declared_data_from_orm_style_record():

    record = {
        "evidence_id": "evidence-001",
        "policy_id": "policy-001",
        "data_type": "precise_location",
        "purpose": "advertising",
        "sharing": "third parties",
        "retention": "30 days",
    }

    result = declared_data_from_record(record)

    assert result.id == "evidence-001"
    assert result.data_type == "precise_location"
    assert result.purpose == "advertising"
    assert result.sharing == "third parties"
    assert result.retention == "30 days"