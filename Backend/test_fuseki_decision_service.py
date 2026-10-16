from app.ontology.fuseki_decision_service import FusekiDecisionService


def test_fuseki_semantic_finding_reaches_existing_decision_engine():
    service = FusekiDecisionService()

    decisions = service.evaluate()

    assert len(decisions) >= 1

    decision = decisions[0]

    assert decision.fdo_status == "FDO"
    assert decision.decision_confidence == 0.85
    assert decision.data_match_relation == "NARROWER_EVIDENCE"

    reason = decision.decision_reason.lower()

    assert "purpose is incompatible" in reason
    assert "matched via narrower type" in reason
    assert reason.count("matched via narrower type") == 1