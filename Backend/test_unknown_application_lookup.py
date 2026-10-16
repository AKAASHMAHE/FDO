from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app import models
from app.models.application import Application
from app.models.base import Base
from app.models.expected_mapping import ExpectedMapping
from app.models.function import Function
from app.models.policy_evidence import PolicyEvidence
from app.models.policy_document import PolicyDocument
from app.models.overreach_candidate import OverreachCandidate
from app.models.comparison import Comparison
from app.models.fdo_result import FDOResult
from app.models.explanation import Explanation
from app.services.analysis_runner import run_analysis
from app.services.application_service import (
    find_application_by_name,
    get_or_create_application_for_analysis,
)
from app.services.evidence_matcher import find_best_matching_evidence
from app.services.comparison_service import (
    classify_purpose_compatibility,
)
from app.ontology.semantic_decision_adapter import (
    semantic_finding_to_decision_input,
)
from app.services.policy_ingestion_service import create_runtime_policy


def make_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    return SessionLocal()


def test_existing_application_lookup_still_works():
    session = make_session()
    session.add(
        Application(
            application_id="NAV-01",
            application_name="Google Maps",
            category="Navigation",
            description="Navigation app",
        )
    )
    session.commit()

    application = find_application_by_name(
        session,
        "Google Maps",
    )

    assert application is not None
    assert application.application_id == "NAV-01"


def test_application_lookup_is_case_insensitive_and_trimmed():
    session = make_session()
    session.add(
        Application(
            application_id="NAV-01",
            application_name="Google Maps",
            category="Navigation",
        )
    )
    session.commit()

    assert (
        find_application_by_name(
            session,
            "google maps",
        ).application_id
        == "NAV-01"
    )
    assert (
        find_application_by_name(
            session,
            "  GOOGLE   MAPS  ",
        ).application_id
        == "NAV-01"
    )


def test_unknown_application_can_be_created():
    session = make_session()

    application = get_or_create_application_for_analysis(
        session,
        "Instagram",
        "Social Media",
        "Photo and video sharing app",
    )

    assert application.application_id == "APP-INSTAGRAM"
    assert application.application_name == "Instagram"
    assert application.category == "Social Media"


def test_repeating_unknown_application_does_not_create_duplicate():
    session = make_session()

    first = get_or_create_application_for_analysis(
        session,
        "Instagram",
        "Social Media",
    )
    second = get_or_create_application_for_analysis(
        session,
        "  instagram  ",
        "Different Category",
    )

    applications = session.scalars(
        select(Application)
    ).all()

    assert first.application_id == second.application_id
    assert len(applications) == 1


def test_existing_application_category_is_not_overwritten():
    session = make_session()
    session.add(
        Application(
            application_id="COM-01",
            application_name="WhatsApp",
            category="Communication",
        )
    )
    session.commit()

    application = get_or_create_application_for_analysis(
        session,
        "whatsapp",
        "Social Media",
    )

    assert application.application_id == "COM-01"
    assert application.category == "Communication"


def test_unknown_application_without_expectations_is_ambiguous_not_fdo():
    session = make_session()
    application = get_or_create_application_for_analysis(
        session,
        "Some Random App",
        "Utility",
    )
    policy = create_runtime_policy(
        session,
        application_id=application.application_id,
        policy_text=(
            "We collect device and activity information "
            "to provide our services."
        ),
        policy_source="TEST",
        evidence=[
            {
                "data_type": "device_info",
                "purpose": "providing the service",
                "extraction_status": "EXTRACTED",
                "evidence_text": (
                    "We collect device and activity information "
                    "to provide our services."
                ),
            }
        ],
        analysis_id="ANALYSIS-APP-RANDOM-TEST",
    )

    analysis = run_analysis(
        session,
        "ANALYSIS-APP-RANDOM-TEST",
        application.application_id,
        policy_id=policy.policy_id,
    )

    assert analysis.analysis_status == "COMPLETED"
    assert analysis.total_mappings == 0
    assert analysis.fdo_count == 0
    assert analysis.not_fdo_count == 0
    assert analysis.ambiguous_count == 0


def add_expected_location_mapping(session):
    application = get_or_create_application_for_analysis(
        session,
        "Maps Demo",
        "Navigation",
    )
    function = Function(
        function_record_id="FUNC-MAPS-NAV",
        function_id="FUNC.NAVIGATION",
        application_id=application.application_id,
        function_name="Navigation",
    )
    session.add(function)
    mapping = ExpectedMapping(
        expected_id="EXP-MAPS-LOCATION",
        application_id=application.application_id,
        function_record_id=function.function_record_id,
        data_type="DATA.LOCATION",
        necessity="REQUIRED",
        expected_purpose="navigation",
        source_version="CURATED",
    )
    session.add(mapping)
    policy = PolicyDocument(
        policy_id="POL-MAPS",
        application_id=application.application_id,
        source_type="TEST",
        source_identifier="TEST",
        document_name="Test Policy",
        raw_text="Test policy",
        created_at="2026-10-07T00:00:00+00:00",
    )
    session.add(policy)
    session.flush()
    return mapping, policy


def test_purpose_aware_evidence_prefers_compatible_purpose():
    session = make_session()
    mapping, policy = add_expected_location_mapping(session)
    session.add_all(
        [
            PolicyEvidence(
                evidence_id="EV-ADS",
                policy_id=policy.policy_id,
                data_type="DATA.LOCATION",
                purpose="advertising",
                evidence_text=(
                    "We collect location information for advertising."
                ),
                extraction_status="EXTRACTED",
                confidence=0.95,
            ),
            PolicyEvidence(
                evidence_id="EV-NAV",
                policy_id=policy.policy_id,
                data_type="DATA.LOCATION",
                purpose="navigation and directions",
                evidence_text=(
                    "We collect location information to provide "
                    "navigation and directions."
                ),
                extraction_status="EXTRACTED",
                confidence=0.70,
            ),
        ]
    )
    session.flush()

    match = find_best_matching_evidence(
        session,
        policy.policy_id,
        mapping,
    )

    assert match.evidence.evidence_id == "EV-NAV"


def test_purpose_aware_evidence_marks_equal_matches_ambiguous():
    session = make_session()
    mapping, policy = add_expected_location_mapping(session)
    session.add_all(
        [
            PolicyEvidence(
                evidence_id="EV-1",
                policy_id=policy.policy_id,
                data_type="DATA.LOCATION",
                purpose="location services",
                evidence_text="We collect location for location services.",
                extraction_status="EXTRACTED",
                confidence=0.5,
            ),
            PolicyEvidence(
                evidence_id="EV-2",
                policy_id=policy.policy_id,
                data_type="DATA.LOCATION",
                purpose="location services",
                evidence_text="We use location for location services.",
                extraction_status="EXTRACTED",
                confidence=0.5,
            ),
        ]
    )
    session.flush()

    match = find_best_matching_evidence(
        session,
        policy.policy_id,
        mapping,
    )

    assert match.evidence is None
    assert match.status == "AMBIGUOUS"


def test_semantic_and_relational_purpose_logic_match():
    relational = classify_purpose_compatibility(
        "navigation",
        "navigation and directions",
    )
    semantic = semantic_finding_to_decision_input(
        {
            "expected_data": "EXP",
            "declared_data": "DEC",
            "expected_type": "DATA.LOCATION",
            "declared_type": "DATA.LOCATION",
            "expected_purpose": "navigation",
            "declared_purpose": "navigation and directions",
        }
    )

    assert relational == "COMPATIBLE"
    assert semantic.purpose_compatibility == relational


def test_reverse_scan_persists_unrelated_type_as_fdo_candidate():
    session = make_session()
    mapping, policy = add_expected_location_mapping(session)
    session.add(
        PolicyEvidence(
            evidence_id="EV-HEALTH-OVERREACH",
            policy_id=policy.policy_id,
            data_type="DATA.HEALTH",
            purpose="marketing",
            evidence_text="We collect health information for marketing.",
            extraction_status="EXTRACTED",
            confidence=0.9,
        )
    )
    session.flush()

    analysis = run_analysis(
        session,
        "ANALYSIS-HEALTH-OVERREACH",
        mapping.application_id,
        policy_id=policy.policy_id,
    )

    candidate = session.get(
        OverreachCandidate,
        "ANALYSIS-HEALTH-OVERREACH:OVERREACH:EV-HEALTH-OVERREACH",
    )
    assert analysis.total_mappings == 1
    assert candidate is not None
    assert candidate.data_type == "DATA.HEALTH"
    assert candidate.data_match == "NO_MATCH"
    assert candidate.functional_relationship == "RELATED"
    assert candidate.purpose_compatibility == "INCOMPATIBLE"
    assert candidate.fdo_status == "FDO"
    assert candidate.decision_confidence == 0.8


def test_reverse_scan_does_not_candidate_type_covered_by_expected():
    session = make_session()
    mapping, policy = add_expected_location_mapping(session)
    session.add(
        PolicyEvidence(
            evidence_id="EV-PRECISE-LOCATION",
            policy_id=policy.policy_id,
            data_type="DATA.LOCATION.PRECISE",
            purpose="navigation",
            evidence_text="We collect precise location for navigation.",
            extraction_status="EXTRACTED",
            confidence=0.9,
        )
    )
    session.flush()

    run_analysis(
        session,
        "ANALYSIS-COVERED-TYPE",
        mapping.application_id,
        policy_id=policy.policy_id,
    )

    assert session.scalars(
        select(OverreachCandidate).where(
            OverreachCandidate.analysis_id == "ANALYSIS-COVERED-TYPE"
        )
    ).all() == []
    comparison = session.get(
        Comparison,
        "ANALYSIS-COVERED-TYPE:EXP-MAPS-LOCATION",
    )
    assert comparison.data_match == "HIERARCHICAL_MATCH"
    assert comparison.data_match_relation == "NARROWER_EVIDENCE"
    result = session.get(
        FDOResult,
        f"RESULT-{comparison.comparison_id}",
    )
    assert result.fdo_status == "NOT_FDO"
    explanation = session.get(
        Explanation,
        f"EXPLANATION-{result.result_id}",
    )
    assert explanation.data_match_relation == "NARROWER_EVIDENCE"
    assert "Data-type relation: NARROWER_EVIDENCE" in (
        explanation.explanation_text
    )
