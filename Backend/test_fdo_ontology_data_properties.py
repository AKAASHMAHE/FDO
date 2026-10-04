from app.ontology import (
    Application,
    DataProperty,
    FDO_DATA_PROPERTIES,
    PersonalData,
    RetentionPolicy,
    Recipient,
    PrivacyPolicy,
    PolicyClause,
    ExpectedData,
    DeclaredData,
    Overreach,
    Risk,
)


def test_data_property_structure():
    prop = FDO_DATA_PROPERTIES["name"]

    assert isinstance(prop, DataProperty)
    assert prop.name == "name"
    assert prop.datatype == "string"


def test_application_name_property():
    prop = FDO_DATA_PROPERTIES["name"]

    assert prop.domain is Application
    assert prop.datatype == "string"


def test_application_category_property():
    prop = FDO_DATA_PROPERTIES["category"]

    assert prop.domain is Application
    assert prop.datatype == "string"


def test_personal_data_sensitive_property():
    prop = FDO_DATA_PROPERTIES["sensitive"]

    assert prop.domain is PersonalData
    assert prop.datatype == "boolean"


def test_personal_data_sensitivity_category():
    prop = FDO_DATA_PROPERTIES["sensitivityCategory"]

    assert prop.domain is PersonalData
    assert prop.datatype == "string"


def test_recipient_type_property():
    prop = FDO_DATA_PROPERTIES["recipientType"]

    assert prop.domain is Recipient
    assert prop.datatype == "string"


def test_retention_duration_property():
    prop = FDO_DATA_PROPERTIES["duration"]

    assert prop.domain is RetentionPolicy
    assert prop.datatype == "string"


def test_policy_source_property():
    prop = FDO_DATA_PROPERTIES["source"]

    assert prop.domain is PrivacyPolicy


def test_policy_version_property():
    prop = FDO_DATA_PROPERTIES["version"]

    assert prop.domain is PrivacyPolicy


def test_policy_clause_text_property():
    prop = FDO_DATA_PROPERTIES["text"]

    assert prop.domain is PolicyClause


def test_policy_clause_section_property():
    prop = FDO_DATA_PROPERTIES["section"]

    assert prop.domain is PolicyClause


def test_expected_data_type_property():
    prop = FDO_DATA_PROPERTIES["dataType"]

    assert prop.domain is ExpectedData


def test_expected_data_necessity_property():
    prop = FDO_DATA_PROPERTIES["necessity"]

    assert prop.domain is ExpectedData


def test_expected_data_purpose_property():
    prop = FDO_DATA_PROPERTIES["purpose"]

    assert prop.domain is ExpectedData


def test_declared_data_sharing_property():
    prop = FDO_DATA_PROPERTIES["sharing"]

    assert prop.domain is DeclaredData


def test_declared_data_retention_property():
    prop = FDO_DATA_PROPERTIES["retention"]

    assert prop.domain is DeclaredData


def test_overreach_confidence_property():
    prop = FDO_DATA_PROPERTIES["confidence"]

    assert prop.domain is Overreach
    assert prop.datatype == "float"


def test_overreach_reason_property():
    prop = FDO_DATA_PROPERTIES["reason"]

    assert prop.domain is Overreach
    assert prop.datatype == "string"


def test_risk_score_property():
    prop = FDO_DATA_PROPERTIES["score"]

    assert prop.domain is Risk
    assert prop.datatype == "float"


def test_risk_level_property():
    prop = FDO_DATA_PROPERTIES["level"]

    assert prop.domain is Risk
    assert prop.datatype == "string"


def test_all_properties_have_descriptions():
    for prop in FDO_DATA_PROPERTIES.values():
        assert prop.name
        assert prop.datatype
        assert prop.description


def test_required_data_properties_exist():
    expected = {
        "id",
        "name",
        "description",
        "category",
        "sensitive",
        "sensitivityCategory",
        "duration",
        "recipientType",
        "status",
        "source",
        "version",
        "text",
        "section",
        "dataType",
        "necessity",
        "purpose",
        "sharing",
        "retention",
        "justificationType",
        "reason",
        "confidence",
        "level",
        "score",
    }

    assert expected.issubset(FDO_DATA_PROPERTIES.keys())