from app.ontology import (
    Application,
    DeclaredData,
    ExpectedData,
    Function,
    Overreach,
    PolicyClause,
    PrivacyPolicy,
    map_application,
    map_declared_data,
    map_expected_mapping,
    map_fdo_result,
    map_function,
    map_policy_document,
    map_policy_evidence,
    map_records,
)


def test_map_application_from_dict():
    record = {
        "id": 1,
        "name": "Google Maps",
        "category": "Navigation",
        "description": "Navigation application",
    }

    result = map_application(record)

    assert isinstance(result, Application)
    assert result.id == "1"
    assert result.name == "Google Maps"
    assert result.category == "Navigation"


def test_map_application_fallback_name():
    record = {
        "id": 2,
        "app_name": "WhatsApp",
    }

    result = map_application(record)

    assert result.name == "WhatsApp"


def test_map_function():
    record = {
        "id": 10,
        "name": "Navigation",
        "description": "Route planning",
    }

    result = map_function(record)

    assert isinstance(result, Function)
    assert result.id == "10"
    assert result.name == "Navigation"


def test_map_expected_mapping():
    record = {
        "id": 20,
        "data_type": "Location",
        "necessity": "required",
        "purpose": "Navigation",
    }

    result = map_expected_mapping(record)

    assert isinstance(result, ExpectedData)
    assert result.id == "20"
    assert result.data_type == "Location"
    assert result.necessity == "required"
    assert result.purpose == "Navigation"


def test_map_expected_mapping_alternate_field():
    record = {
        "id": 21,
        "expected_data_type": "Contacts",
        "necessity": "optional",
        "purpose": "Communication",
    }

    result = map_expected_mapping(record)

    assert result.data_type == "Contacts"


def test_map_policy_document():
    record = {
        "id": 30,
        "name": "Privacy Policy",
        "source": "policy.txt",
        "version": "1.0",
    }

    result = map_policy_document(record)

    assert isinstance(result, PrivacyPolicy)
    assert result.name == "Privacy Policy"
    assert result.source == "policy.txt"
    assert result.version == "1.0"


def test_map_policy_evidence():
    record = {
        "id": 40,
        "text": "We collect precise location information.",
        "source": "policy.txt",
        "section": "Information We Collect",
    }

    result = map_policy_evidence(record)

    assert isinstance(result, PolicyClause)
    assert "precise location" in result.text.lower()
    assert result.section == "Information We Collect"


def test_map_declared_data():
    record = {
        "id": 50,
        "data_type": "Location",
        "purpose": "Navigation",
        "sharing": "Service Provider",
        "retention": "30 days",
    }

    result = map_declared_data(record)

    assert isinstance(result, DeclaredData)
    assert result.data_type == "Location"
    assert result.purpose == "Navigation"
    assert result.sharing == "Service Provider"
    assert result.retention == "30 days"


def test_map_declared_data_alternate_field():
    record = {
        "id": 51,
        "declared_data_type": "Contacts",
        "purpose": "Communication",
    }

    result = map_declared_data(record)

    assert result.data_type == "Contacts"


def test_map_fdo_result():
    record = {
        "id": 60,
        "fdo_status": "FDO",
        "decision_reason": "Data is unrelated to function.",
        "decision_confidence": 0.85,
    }

    result = map_fdo_result(record)

    assert isinstance(result, Overreach)
    assert result.status == "FDO"
    assert result.reason == "Data is unrelated to function."
    assert result.confidence == 0.85


def test_map_fdo_result_alternate_fields():
    record = {
        "id": 61,
        "status": "AMBIGUOUS",
        "reason": "Insufficient evidence.",
        "confidence": 0.40,
    }

    result = map_fdo_result(record)

    assert result.status == "AMBIGUOUS"
    assert result.reason == "Insufficient evidence."
    assert result.confidence == 0.40


def test_map_records():
    result = map_records(
        applications=[
            {
                "id": 1,
                "name": "Maps",
            }
        ],
        functions=[
            {
                "id": 2,
                "name": "Navigation",
            }
        ],
        expected_mappings=[
            {
                "id": 3,
                "data_type": "Location",
            }
        ],
        policy_documents=[
            {
                "id": 4,
                "name": "Policy",
            }
        ],
        policy_evidence=[
            {
                "id": 5,
                "text": "We collect location.",
            }
        ],
        declared_data=[
            {
                "id": 6,
                "data_type": "Location",
            }
        ],
        fdo_results=[
            {
                "id": 7,
                "status": "FDO",
            }
        ],
    )

    assert len(result["applications"]) == 1
    assert len(result["functions"]) == 1
    assert len(result["expected_data"]) == 1
    assert len(result["privacy_policies"]) == 1
    assert len(result["policy_clauses"]) == 1
    assert len(result["declared_data"]) == 1
    assert len(result["overreach"]) == 1


def test_map_records_empty():
    result = map_records()

    assert result["applications"] == []
    assert result["functions"] == []
    assert result["expected_data"] == []
    assert result["privacy_policies"] == []
    assert result["policy_clauses"] == []
    assert result["declared_data"] == []
    assert result["overreach"] == []