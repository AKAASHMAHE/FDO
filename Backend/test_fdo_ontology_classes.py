from app.ontology import (
    Application,
    Consent,
    DeclaredData,
    ExpectedData,
    FDO_CLASSES,
    Function,
    Justification,
    Overreach,
    PersonalData,
    PolicyClause,
    PrivacyPolicy,
    ProcessingActivity,
    Purpose,
    Recipient,
    RetentionPolicy,
    Risk,
    SensitiveData,
    User,
    UserRight,
)


def test_application_class():
    app = Application(
        id="app_001",
        name="Navigation App",
        category="Navigation",
        description="Provides turn-by-turn navigation.",
    )

    assert app.id == "app_001"
    assert app.name == "Navigation App"
    assert app.category == "Navigation"


def test_function_class():
    function = Function(
        id="fn_001",
        name="Navigation",
        description="Turn-by-turn route navigation.",
    )

    assert function.name == "Navigation"


def test_personal_data_class():
    data = PersonalData(
        id="data_001",
        name="Location",
    )

    assert data.name == "Location"
    assert data.sensitive is False


def test_sensitive_data_is_personal_data():
    data = SensitiveData(
        id="data_002",
        name="Health Information",
        sensitivity_category="Health",
    )

    assert isinstance(data, PersonalData)
    assert data.sensitivity_category == "Health"


def test_processing_activity_class():
    activity = ProcessingActivity(
        id="activity_001",
        name="Collect",
    )

    assert activity.name == "Collect"


def test_purpose_class():
    purpose = Purpose(
        id="purpose_001",
        name="Navigation",
    )

    assert purpose.name == "Navigation"


def test_recipient_class():
    recipient = Recipient(
        id="recipient_001",
        name="Service Provider",
        recipient_type="Service Provider",
    )

    assert recipient.recipient_type == "Service Provider"


def test_retention_policy_class():
    retention = RetentionPolicy(
        id="retention_001",
        name="30 Days",
        duration="30 days",
    )

    assert retention.duration == "30 days"


def test_user_right_class():
    right = UserRight(
        id="right_001",
        name="Deletion",
    )

    assert right.name == "Deletion"


def test_consent_class():
    consent = Consent(
        id="consent_001",
        name="Location Consent",
        status="granted",
    )

    assert consent.status == "granted"


def test_privacy_policy_class():
    policy = PrivacyPolicy(
        id="policy_001",
        name="Navigation Privacy Policy",
        source="policy.pdf",
    )

    assert policy.source == "policy.pdf"


def test_policy_clause_class():
    clause = PolicyClause(
        id="clause_001",
        name="Location Collection Clause",
        text="We collect precise location information.",
        section="Information We Collect",
    )

    assert "precise location" in clause.text.lower()


def test_expected_data_class():
    expected = ExpectedData(
        id="expected_001",
        name="Expected Location",
        data_type="Location",
        necessity="required",
        purpose="Navigation",
    )

    assert expected.data_type == "Location"
    assert expected.necessity == "required"


def test_declared_data_class():
    declared = DeclaredData(
        id="declared_001",
        name="Declared Contacts",
        data_type="Contacts",
        purpose="Service functionality",
        sharing="Service Provider",
        retention="30 days",
    )

    assert declared.data_type == "Contacts"
    assert declared.sharing == "Service Provider"


def test_justification_class():
    justification = Justification(
        id="justification_001",
        name="Security Justification",
        text="Used to prevent fraud.",
        justification_type="Security",
    )

    assert justification.justification_type == "Security"


def test_overreach_class():
    finding = Overreach(
        id="overreach_001",
        name="Contacts Overreach",
        status="Potential Undisclosed Overreach",
        reason="Contacts are not expected for navigation.",
        confidence=0.85,
    )

    assert finding.status == "Potential Undisclosed Overreach"
    assert finding.confidence == 0.85


def test_risk_class():
    risk = Risk(
        id="risk_001",
        name="Contacts Risk",
        level="High",
        score=0.85,
    )

    assert risk.level == "High"
    assert risk.score == 0.85


def test_all_fdo_classes_registered():
    expected_classes = {
        "Application",
        "Function",
        "PersonalData",
        "SensitiveData",
        "ProcessingActivity",
        "Purpose",
        "Recipient",
        "RetentionPolicy",
        "User",
        "UserRight",
        "Consent",
        "PrivacyPolicy",
        "PolicyClause",
        "ExpectedData",
        "DeclaredData",
        "Justification",
        "Overreach",
        "Risk",
    }

    assert expected_classes.issubset(FDO_CLASSES.keys())