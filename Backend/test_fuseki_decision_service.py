from app.ontology.fuseki_decision_service import FusekiDecisionService


def test_fuseki_semantic_finding_reaches_existing_decision_engine():
    service = FusekiDecisionService()

    decisions = service.evaluate()

    assert len(decisions) >= 1

    decision = decisions[0]

    assert decision.fdo_status == "FDO"
    assert decision.decision_confidence == 0.80

    reason = decision.decision_reason.lower()

    assert "declared data type" in reason
    assert "expected functional data type" in reason
    assert "evaluated function" in reason