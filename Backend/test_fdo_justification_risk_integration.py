from rdflib import RDF

from app.ontology.classes import Justification, Risk
from app.ontology.namespace import FDO
from app.ontology.rdf_instance_builder import (
    build_rdf_graph,
    add_justification,
    add_risk,
)
from app.ontology.uri import (
    justification_uri,
    risk_uri,
)


def test_justification_is_created_as_justification_class():
    graph = build_rdf_graph()

    add_justification(
        graph,
        Justification(
            id="justification-1",
            name="Functional necessity",
            justification_type="functional",
            
        ),
    )

    assert (
        justification_uri("justification-1"),
        RDF.type,
        FDO.Justification,
    ) in graph





def test_justification_preserves_type():
    graph = build_rdf_graph()

    add_justification(
        graph,
        Justification(
            id="justification-1",
            name="Functional necessity",
            justification_type="functional",
        ),
    )

    value = graph.value(
        justification_uri("justification-1"),
        FDO.justificationType,
    )

    assert str(value) == "functional"


def test_risk_is_created_as_risk_class():
    graph = build_rdf_graph()

    add_risk(
        graph,
        Risk(
            id="risk-1",
            name="Privacy overcollection risk",
            level="high",
            score=0.85,
        ),
    )

    assert (
        risk_uri("risk-1"),
        RDF.type,
        FDO.Risk,
    ) in graph


def test_risk_preserves_level():
    graph = build_rdf_graph()

    add_risk(
        graph,
        Risk(
            id="risk-1",
            name="Privacy overcollection risk",
            level="high",
            score=0.85,
        ),
    )

    value = graph.value(
        risk_uri("risk-1"),
        FDO.level,
    )

    assert str(value) == "high"


def test_risk_preserves_score():
    graph = build_rdf_graph()

    add_risk(
        graph,
        Risk(
            id="risk-1",
            name="Privacy overcollection risk",
            level="high",
            score=0.85,
        ),
    )

    value = graph.value(
        risk_uri("risk-1"),
        FDO.score,
    )

    assert value.toPython() == 0.85


def test_justification_and_risk_are_distinct_resources():
    graph = build_rdf_graph()

    add_justification(
        graph,
        Justification(
            id="justification-1",
            name="Functional necessity",
        ),
    )

    add_risk(
        graph,
        Risk(
            id="risk-1",
            name="Privacy risk",
        ),
    )

    assert justification_uri("justification-1") != risk_uri("risk-1")

    assert (
        justification_uri("justification-1"),
        RDF.type,
        FDO.Justification,
    ) in graph

    assert (
        risk_uri("risk-1"),
        RDF.type,
        FDO.Risk,
    ) in graph