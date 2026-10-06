from app.ontology.db_semantic_result_service import (
    deduplicate_semantic_results,
    group_semantic_result_purposes,
)
from app.ontology.semantic_decision_adapter import (
    decide_semantic_finding,
)
from app.schemas.analysis import SemanticFDOResultResponse
from app.services.evidence_validation_service import (
    is_semantic_finding_usable,
    validate_policy_evidence,
)
from app.services.policy_discovery_service import (
    PolicyDiscoveryResult,
    discover_privacy_policy,
)
from app.services.policy_extraction_service import (
    extract_policy_evidence,
)
from app.services.policy_analysis_service import (
    build_policy_analysis,
)
from app.services.expected_mapping_service import (
    get_expected_mappings_by_application,
)


def test_irrelevant_operational_evidence_is_rejected():
    evidence = validate_policy_evidence(
        [
            {
                "data_type": "DATA.OTHER",
                "purpose": "delivery is retried",
                "evidence_text": "Delivery is retried when infrastructure fails.",
                "confidence": 0.8,
            }
        ]
    )

    assert evidence == []


def test_valid_privacy_evidence_is_preserved():
    evidence = validate_policy_evidence(
        [
            {
                "data_type": "DATA.DEVICE",
                "purpose": "providing the service",
                "evidence_text": (
                    "We collect device information to provide "
                    "and secure our services."
                ),
                "confidence": 0.8,
            }
        ]
    )

    assert len(evidence) == 1
    assert evidence[0]["data_type"] == "DATA.DEVICE"


def test_extraction_filters_bad_ai_output(monkeypatch):
    monkeypatch.setattr(
        "app.services.policy_extraction_service.extract_policy_evidence_with_ai",
        lambda policy_text, application_name: [
            {
                "data_type": "DATA.OTHER",
                "purpose": "delivery is retried",
                "evidence_text": "Delivery is retried when needed.",
                "confidence": 0.9,
            },
            {
                "data_type": "DATA.LOCATION",
                "purpose": "navigation",
                "evidence_text": (
                    "We collect location information to provide "
                    "navigation features."
                ),
                "confidence": 0.9,
            },
        ],
    )

    evidence = extract_policy_evidence(
        (
            "Delivery is retried when needed. We collect "
            "location information to provide navigation features."
        ),
        "Maps App",
    )

    assert len(evidence) == 1
    assert evidence[0]["data_type"] == "DATA.LOCATION"


def test_policy_discovery_success_from_known_url(monkeypatch):
    class Response:
        encoding = "utf-8"
        content = (
            b"<html><body><h1>Privacy Policy</h1>"
            b"We collect personal information and device data "
            b"to provide services. " * 30
            + b"</body></html>"
        )

        def raise_for_status(self):
            return None

    monkeypatch.setattr(
        "app.services.policy_discovery_service.requests.get",
        lambda *args, **kwargs: Response(),
    )

    result = discover_privacy_policy("Instagram")

    assert result.success is True
    assert result.source_url
    assert "personal information" in result.policy_text.lower()


def test_policy_discovery_failure_returns_manual_fallback(monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("network unavailable")

    monkeypatch.setattr(
        "app.services.policy_discovery_service.requests.get",
        fail,
    )

    result = discover_privacy_policy("Unknown Application")

    assert result.success is False
    assert "paste the policy manually" in result.error


def test_semantic_results_are_deduplicated_conservatively():
    result = {
        "application_id": "APP",
        "function": "FUNC",
        "expected_data": "EXP",
        "declared_data": "DEC",
        "expected_type": "DATA.DEVICE",
        "declared_type": "DATA.USAGE",
        "expected_purpose": "service",
        "declared_purpose": "ads",
        "fdo_status": "FDO",
    }

    distinct = {
        **result,
        "declared_purpose": "analytics",
    }

    deduplicated = deduplicate_semantic_results(
        [result, dict(result), distinct]
    )

    assert deduplicated == [result, distinct]


def test_valid_semantic_not_fdo_still_works():
    decision = decide_semantic_finding(
        {
            "expected_data": "EXP-003",
            "declared_data": "AI-camera",
            "expected_type": "DATA.MEDIA.CAMERA",
            "declared_type": "DATA.MEDIA.CAMERA",
            "expected_purpose": "FUNC.COM.VIDEO",
            "declared_purpose": "FUNC.COM.VIDEO",
        }
    )

    assert decision.fdo_status == "NOT_FDO"


def test_valid_semantic_fdo_still_works():
    decision = decide_semantic_finding(
        {
            "expected_data": "EXP-003",
            "declared_data": "AI-location",
            "expected_type": "DATA.MEDIA.CAMERA",
            "declared_type": "DATA.LOCATION",
            "expected_purpose": "FUNC.COM.VIDEO",
            "declared_purpose": "advertising",
        }
    )

    assert decision.fdo_status == "FDO"


def test_operational_semantic_finding_is_not_usable():
    finding = {
        "expected_type": "DATA.MEDIA.CAMERA",
        "declared_type": "DATA.OTHER",
        "declared_data": "AI-delivery-retry",
        "declared_purpose": "delivery is retried",
    }

    assert is_semantic_finding_usable(finding) is False


def test_unclear_semantic_evidence_is_not_confident_fdo():
    finding = {
        "expected_type": "DATA.MEDIA.CAMERA",
        "declared_type": "DATA.OTHER",
        "declared_data": "AI-unclear",
        "declared_purpose": "security",
    }

    assert is_semantic_finding_usable(finding) is False


def test_semantic_response_includes_human_readable_labels():
    response = SemanticFDOResultResponse(
        semantic_result_id="SEM-1",
        application_id="APP",
        application="http://example.org/fdo#resource/application/APP",
        function=(
            "http://example.org/fdo#resource/function/"
            "COM-01:FUNC.COM.VIDEO"
        ),
        expected_data=(
            "http://example.org/fdo#resource/expected-data/EXP-003"
        ),
        declared_data=(
            "http://example.org/fdo#resource/declared-data/AI-camera"
        ),
        expected_type="DATA.MEDIA.CAMERA",
        declared_type="DATA.OTHER",
        expected_purpose="FUNC.COM.VIDEO",
        declared_purpose="delivery is retried",
        fdo_status="AMBIGUOUS",
        confidence=0.4,
        reason="Insufficient evidence.",
    )

    payload = response.model_dump()

    assert payload["function_label"] == "Communication Video"
    assert payload["expected_data_label"] == "Camera"
    assert payload["declared_data_label"] == "Other / Unclear Data"


def test_multiple_purposes_for_same_semantic_relationship_are_grouped():
    base = {
        "application_id": "APP",
        "application": "APP",
        "function": "FUNC.COM.VIDEO",
        "expected_data": "EXP-LOCATION",
        "declared_data": "AI-location",
        "expected_type": "DATA.LOCATION",
        "declared_type": "DATA.LOCATION",
        "expected_purpose": "FUNC.COM.VIDEO",
        "fdo_status": "FDO",
        "confidence": 0.8,
        "reason": "Purpose differs.",
    }

    grouped = group_semantic_result_purposes(
        [
            {
                **base,
                "declared_purpose": "estimate general location",
            },
            {
                **base,
                "declared_purpose": "create an account",
            },
        ]
    )

    assert len(grouped) == 1
    assert grouped[0]["declared_purposes"] == [
        "estimate general location",
        "create an account",
    ]


def test_different_semantic_relationships_remain_separate_when_grouping():
    base = {
        "application_id": "APP",
        "application": "APP",
        "function": "FUNC.COM.VIDEO",
        "expected_data": "EXP-LOCATION",
        "declared_data": "AI-location",
        "expected_type": "DATA.LOCATION",
        "expected_purpose": "FUNC.COM.VIDEO",
        "fdo_status": "FDO",
        "confidence": 0.8,
        "reason": "Purpose differs.",
    }

    grouped = group_semantic_result_purposes(
        [
            {
                **base,
                "declared_type": "DATA.LOCATION",
                "declared_purpose": "estimate location",
            },
            {
                **base,
                "declared_data": "AI-camera",
                "declared_type": "DATA.MEDIA.CAMERA",
                "declared_purpose": "video calling",
            },
        ]
    )

    assert len(grouped) == 2


def test_policy_analysis_available_without_expected_baseline():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from app.models.base import Base
    from app.models.application import Application
    from app.services.policy_ingestion_service import (
        create_runtime_policy,
    )

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()

    session.add(
        Application(
            application_id="APP-NEW",
            application_name="New App",
            category="Other",
        )
    )

    policy = create_runtime_policy(
        session,
        application_id="APP-NEW",
        policy_text="We collect location to estimate your city.",
        policy_source="https://example.com/privacy",
        analysis_id="ANALYSIS-APP-NEW-TEST",
        evidence=[
            {
                "data_type": "DATA.LOCATION",
                "purpose": "estimate your general location",
                "entity": "location services",
                "evidence_text": (
                    "We collect location to estimate your city."
                ),
                "extraction_status": "EXTRACTED",
                "confidence": 0.9,
            }
        ],
    )

    policy_analysis = build_policy_analysis(
        session,
        policy.policy_id,
    )

    assert policy_analysis.available is True
    assert policy_analysis.policy_source == "https://example.com/privacy"
    assert policy_analysis.findings[0].data_label == "Location"
    assert policy_analysis.findings[0].purposes == [
        "estimate your general location"
    ]
    assert (
        get_expected_mappings_by_application(session, "APP-NEW")
        == []
    )
