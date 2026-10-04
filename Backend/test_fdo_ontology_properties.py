from app.ontology import (
    Application,
    Consent,
    DeclaredData,
    ExpectedData,
    FDO_OBJECT_PROPERTIES,
    Function,
    Justification,
    ObjectProperty,
    Overreach,
    PersonalData,
    PolicyClause,
    PrivacyPolicy,
    ProcessingActivity,
    Purpose,
    Recipient,
    RetentionPolicy,
    Risk,
    User,
    UserRight,
)


def test_object_property_structure():
    prop = FDO_OBJECT_PROPERTIES["performsFunction"]

    assert isinstance(prop, ObjectProperty)
    assert prop.name == "performsFunction"
    assert prop.domain is Application
    assert prop.range is Function


def test_application_performs_function():
    prop = FDO_OBJECT_PROPERTIES["performsFunction"]

    assert prop.domain is Application
    assert prop.range is Function


def test_function_requires_data():
    prop = FDO_OBJECT_PROPERTIES["requiresData"]

    assert prop.domain is Function
    assert prop.range is PersonalData


def test_application_collects_data():
    prop = FDO_OBJECT_PROPERTIES["collectsData"]

    assert prop.domain is Application
    assert prop.range is PersonalData


def test_application_declared_data():
    prop = FDO_OBJECT_PROPERTIES["declaredData"]

    assert prop.domain is Application
    assert prop.range is DeclaredData


def test_function_expected_data():
    prop = FDO_OBJECT_PROPERTIES["expectedData"]

    assert prop.domain is Function
    assert prop.range is ExpectedData


def test_expected_data_function_relationship():
    prop = FDO_OBJECT_PROPERTIES["expectedForFunction"]

    assert prop.domain is ExpectedData
    assert prop.range is Function


def test_declared_data_application_relationship():
    prop = FDO_OBJECT_PROPERTIES["declaredByApplication"]

    assert prop.domain is DeclaredData
    assert prop.range is Application


def test_data_purpose_relationship():
    prop = FDO_OBJECT_PROPERTIES["usedForPurpose"]

    assert prop.domain is PersonalData
    assert prop.range is Purpose


def test_data_processing_relationship():
    prop = FDO_OBJECT_PROPERTIES["processedBy"]

    assert prop.domain is PersonalData
    assert prop.range is ProcessingActivity


def test_data_recipient_relationship():
    prop = FDO_OBJECT_PROPERTIES["sharedWith"]

    assert prop.domain is PersonalData
    assert prop.range is Recipient


def test_data_retention_relationship():
    prop = FDO_OBJECT_PROPERTIES["hasRetentionPolicy"]

    assert prop.domain is PersonalData
    assert prop.range is RetentionPolicy


def test_declared_data_policy_evidence():
    prop = FDO_OBJECT_PROPERTIES["supportedByClause"]

    assert prop.domain is DeclaredData
    assert prop.range is PolicyClause


def test_clause_policy_relationship():
    prop = FDO_OBJECT_PROPERTIES["supportedByPolicy"]

    assert prop.domain is PolicyClause
    assert prop.range is PrivacyPolicy


def test_policy_user_right_relationship():
    prop = FDO_OBJECT_PROPERTIES["hasUserRight"]

    assert prop.domain is PrivacyPolicy
    assert prop.range is UserRight


def test_application_consent_relationship():
    prop = FDO_OBJECT_PROPERTIES["hasConsent"]

    assert prop.domain is Application
    assert prop.range is Consent


def test_overreach_justification_relationship():
    prop = FDO_OBJECT_PROPERTIES["hasJustification"]

    assert prop.domain is Overreach
    assert prop.range is Justification


def test_overreach_data_relationship():
    prop = FDO_OBJECT_PROPERTIES["concernsData"]

    assert prop.domain is Overreach
    assert prop.range is PersonalData


def test_overreach_function_relationship():
    prop = FDO_OBJECT_PROPERTIES["concernsFunction"]

    assert prop.domain is Overreach
    assert prop.range is Function


def test_overreach_risk_relationship():
    prop = FDO_OBJECT_PROPERTIES["hasRisk"]

    assert prop.domain is Overreach
    assert prop.range is Risk


def test_application_user_relationship():
    prop = FDO_OBJECT_PROPERTIES["hasUser"]

    assert prop.domain is Application
    assert prop.range is User


def test_all_required_properties_exist():
    expected_properties = {
        "performsFunction",
        "requiresData",
        "collectsData",
        "declaredData",
        "expectedData",
        "expectedForFunction",
        "declaredByApplication",
        "usedForPurpose",
        "processedBy",
        "sharedWith",
        "hasRetentionPolicy",
        "supportedByClause",
        "supportedByPolicy",
        "hasUserRight",
        "hasConsent",
        "hasJustification",
        "concernsData",
        "concernsFunction",
        "hasRisk",
        "hasUser",
    }

    assert expected_properties.issubset(FDO_OBJECT_PROPERTIES.keys())


def test_all_properties_have_descriptions():
    for prop in FDO_OBJECT_PROPERTIES.values():
        assert prop.description
        assert prop.name
        assert prop.domain
        assert prop.range