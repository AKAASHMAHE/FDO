from __future__ import annotations

from uuid import uuid4

import pytest
import requests
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.models.application import Application
from app.models.base import Base
from app.models.comparison import Comparison
from app.models.expected_mapping import ExpectedMapping
from app.models.fdo_result import FDOResult
from app.models.function import Function
from app.models.overreach_candidate import OverreachCandidate
from app.models.policy_document import PolicyDocument
from app.models.policy_evidence import PolicyEvidence
from app.ontology.db_rdf_service import DBRDFService
from app.ontology.fuseki_semantic_detector import FusekiSemanticDetector
from app.ontology.semantic_decision_adapter import adapt_semantic_results
from app.ontology.db_semantic_repository import DBSemanticRepository
from app.ontology.fuseki_service import FusekiService
from app.services.analysis_runner import run_analysis


@pytest.fixture
def isolated_fuseki_service():
    base_url = "http://localhost:3030"
    try:
        response = requests.get(f"{base_url}/$/datasets", timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        pytest.skip(f"Fuseki is unavailable: {exc}")

    dataset = f"fdo-parity-{uuid4().hex[:12]}"
    created = requests.post(
        f"{base_url}/$/datasets",
        data={"dbType": "mem", "dbName": dataset},
        timeout=10,
    )
    created.raise_for_status()
    try:
        yield FusekiService(base_url=base_url, dataset=dataset)
    finally:
        deleted = requests.delete(
            f"{base_url}/$/datasets/{dataset}",
            timeout=10,
        )
        deleted.raise_for_status()


def _add_synthetic_app(
    session,
    case_id: str,
    expected_type: str,
    expected_purpose: str,
    evidence: list[dict],
):
    application_id = f"SYN-{case_id}"
    function_id = f"FUNC-{case_id}"
    expected_id = f"EXP-{case_id}"
    policy_id = f"POL-{case_id}"
    application = Application(
        application_id=application_id,
        application_name=f"Synthetic {case_id}",
        category="Synthetic",
        description="Synthetic parity fixture",
    )
    function = Function(
        function_record_id=function_id,
        function_id=f"FUNCTION.{case_id}",
        application_id=application_id,
        function_name=f"Feature {case_id}",
        description=f"Feature {case_id}",
    )
    expected = ExpectedMapping(
        expected_id=expected_id,
        application_id=application_id,
        function_record_id=function_id,
        data_type=expected_type,
        necessity="REQUIRED",
        expected_purpose=expected_purpose,
    )
    policy = PolicyDocument(
        policy_id=policy_id,
        application_id=application_id,
        source_type="TEST",
        source_identifier=policy_id,
        document_name=f"Synthetic {case_id} policy",
        raw_text="Synthetic policy text.",
        created_at="2026-10-14T00:00:00Z",
    )
    session.add_all([application, function, expected, policy])
    for index, item in enumerate(evidence, start=1):
        session.add(
            PolicyEvidence(
                evidence_id=f"EV-{case_id}-{index}",
                policy_id=policy_id,
                data_type=item["data_type"],
                purpose=item["purpose"],
                entity=item.get("entity"),
                evidence_text=item.get("text", ""),
                extraction_status=item.get("status", "EXTRACTED"),
                confidence=item.get("confidence", 0.8),
            )
        )
    return application_id, expected_id, policy_id


def test_semantic_and_relational_decisions_have_synthetic_parity(
    isolated_fuseki_service,
    tmp_path,
):
    cases = [
        (
            "exact",
            "DATA.LOCATION.PRECISE",
            "navigation",
            [
                {
                    "data_type": "DATA.LOCATION.PRECISE",
                    "purpose": "advertising",
                    "text": "Feature exact unrelated ad purpose.",
                },
                {
                    "data_type": "DATA.LOCATION.PRECISE",
                    "purpose": "navigation",
                    "text": "Feature exact provides navigation.",
                },
            ],
        ),
        (
            "broader",
            "DATA.LOCATION.PRECISE",
            "navigation",
            [{
                "data_type": "DATA.LOCATION",
                "purpose": "navigation",
                "text": "Feature broader provides navigation.",
            }],
        ),
        (
            "narrower",
            "DATA.LOCATION",
            "navigation",
            [{
                "data_type": "DATA.LOCATION.PRECISE",
                "purpose": "navigation",
                "text": "Feature narrower provides navigation.",
            }],
        ),
        (
            "sibling",
            "DATA.LOCATION.PRECISE",
            "navigation",
            [{
                "data_type": "DATA.LOCATION.APPROXIMATE",
                "purpose": "marketing",
                "text": "Marketing uses approximate location.",
            }],
        ),
        (
            "approximate-navigation",
            "DATA.LOCATION.PRECISE",
            "navigation",
            [{
                "data_type": "DATA.LOCATION.APPROXIMATE",
                "purpose": "navigation",
                "text": "Navigation uses approximate location.",
            }],
        ),
        (
            "unrelated",
            "DATA.LOCATION",
            "navigation",
            [{
                "data_type": "DATA.HEALTH.RECORD",
                "purpose": "marketing",
                "text": "Marketing uses health records.",
            }],
        ),
        (
            "contacts-advertising",
            "DATA.LOCATION",
            "navigation",
            [{
                "data_type": "DATA.CONTACT.PHONE",
                "purpose": "advertising",
                "text": "Advertising uses contact information.",
            }],
        ),
        (
            "ancillary",
            "DATA.LOCATION",
            "navigation",
            [{
                "data_type": "DATA.DEVICE.ID",
                "purpose": "security verification",
                "text": "Feature ancillary verifies account security.",
            }],
        ),
        (
            "unknown-purpose",
            "DATA.LOCATION",
            "mystery operation",
            [{
                "data_type": "DATA.LOCATION",
                "purpose": "mystery operation",
                "text": "A mysterious operation.",
            }],
        ),
        ("no-evidence", "DATA.LOCATION", "navigation", []),
    ]
    expected_outputs = {
        "exact": {
            "expected": ("NOT_FDO", 0.90),
            "uncovered": {},
        },
        "broader": {
            "expected": ("NOT_FDO", 0.75),
            "uncovered": {},
        },
        "narrower": {
            "expected": ("NOT_FDO", 0.90),
            "uncovered": {},
        },
        "sibling": {
            "expected": ("AMBIGUOUS", 0.30),
            "uncovered": {"FDO": "NO_MATCH"},
        },
        "approximate-navigation": {
            "expected": ("AMBIGUOUS", 0.30),
            "uncovered": {"AMBIGUOUS": "NO_MATCH"},
        },
        "unrelated": {
            "expected": ("AMBIGUOUS", 0.30),
            "uncovered": {"FDO": "NO_MATCH"},
        },
        "contacts-advertising": {
            "expected": ("AMBIGUOUS", 0.30),
            "uncovered": {"FDO": "NO_MATCH"},
        },
        "ancillary": {
            "expected": ("AMBIGUOUS", 0.30),
            "uncovered": {"NOT_FDO": "ANCILLARY"},
        },
        "unknown-purpose": {
            "expected": ("AMBIGUOUS", 0.40),
            "uncovered": {},
        },
        "no-evidence": {
            "expected": ("AMBIGUOUS", 0.30),
            "uncovered": {},
        },
    }

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine, autoflush=False)()
    records = {}
    for case_id, expected_type, purpose, evidence in cases:
        records[case_id] = _add_synthetic_app(
            session,
            case_id,
            expected_type,
            purpose,
            evidence,
        )
    session.flush()

    graph_service = DBRDFService()
    for case_id, _, _, _ in cases:
        application_id, _, policy_id = records[case_id]
        repository = DBSemanticRepository(session)
        graph = graph_service.build_graph(
            repository.get_application(application_id),
            repository.get_functions(application_id),
            repository.get_expected_mappings(application_id),
            repository.get_policy_evidence(policy_id),
        )
        graph_path = tmp_path / f"{case_id}.ttl"
        graph.serialize(destination=str(graph_path), format="turtle")
        isolated_fuseki_service.upload_rdf(graph_path)

    detector = FusekiSemanticDetector(isolated_fuseki_service)
    covered = detector.detect_covered()
    uncovered = detector.detect_uncovered()

    relational = {}
    for case_id, _, _, _ in cases:
        application_id, expected_id, policy_id = records[case_id]
        analysis_id = f"ANALYSIS-SYN-{case_id}"
        run_analysis(
            session,
            analysis_id,
            application_id,
            policy_id=policy_id,
        )
        comparison = session.scalar(
            select(Comparison).where(
                Comparison.analysis_id == analysis_id,
                Comparison.expected_id == expected_id,
            )
        )
        result = session.scalar(
            select(FDOResult).where(
                FDOResult.comparison_id == comparison.comparison_id
            )
        )
        candidate = session.scalars(
            select(OverreachCandidate).where(
                OverreachCandidate.analysis_id == analysis_id
            )
        ).all()
        relational[case_id] = (result.fdo_status, candidate)

    for case_id, _, _, _ in cases:
        application_id, expected_id, _ = records[case_id]
        expected = repository.get_expected_mappings(application_id)
        semantic = adapt_semantic_results(
            application_id,
            f"http://example.org/fdo#resource/application/{application_id}",
            expected,
            covered,
            uncovered,
        )
        semantic_expected = next(
            row for row in semantic if row["expected_data"] == expected_id
        )
        relational_expected, relational_candidates = relational[case_id]
        assert semantic_expected["fdo_status"] == relational_expected
        expected_status, expected_confidence = expected_outputs[case_id][
            "expected"
        ]
        assert relational_expected == expected_status
        assert semantic_expected["fdo_status"] == expected_status
        assert semantic_expected["confidence"] == expected_confidence
        if case_id == "ancillary":
            assert len(relational_candidates) == 1
            assert relational_candidates[0].fdo_status == "NOT_FDO"
            assert relational_candidates[0].data_match == "ANCILLARY"
        if case_id == "exact":
            assert semantic_expected["declared_data"] == "EV-exact-2"
            assert "Several (2)" in semantic_expected["reason"]
        if case_id == "broader":
            assert semantic_expected["data_match_relation"] == (
                "BROADER_EVIDENCE"
            )
            assert semantic_expected["confidence"] == 0.75

        semantic_uncovered = {
            row["declared_data"]: (row["fdo_status"], row["data_match"])
            for row in semantic
            if row["expected_data"].startswith("OVERREACH:")
        }
        relational_uncovered = {
            item.evidence_id: (item.fdo_status, item.data_match)
            for item in relational_candidates
        }
        assert semantic_uncovered == relational_uncovered
        expected_uncovered = expected_outputs[case_id]["uncovered"]
        assert {
            (status, data_match)
            for status, data_match in semantic_uncovered.values()
        } == {
            (status, data_match)
            for status, data_match in expected_uncovered.items()
        }
        if case_id == "approximate-navigation":
            assert "possible baseline gap" in next(
                row["reason"]
                for row in semantic
                if row["expected_data"].startswith("OVERREACH:")
            )
        if case_id in {"unrelated", "contacts-advertising"}:
            assert "incompatible with every expected purpose" in next(
                row["reason"]
                for row in semantic
                if row["expected_data"].startswith("OVERREACH:")
            )

    session.close()
    engine.dispose()
