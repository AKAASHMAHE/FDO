from rdflib import RDF

from app.ontology.namespace import FDO
from app.ontology.rdf_instance_builder import (
    build_rdf_graph,
    add_overreach,
    connect_overreach_data,
    connect_overreach_function,
    connect_overreach_justification,
    connect_overreach_risk,
)
from app.ontology.classes import Overreach

from app.ontology.uri import (
    overreach_uri,
    personal_data_uri,
    function_uri,
    justification_uri,
    risk_uri,
)


def test_overreach_is_created_as_overreach_class():
    graph = build_rdf_graph()

    add_overreach(
    graph,
    Overreach(
        id="overreach-1",
        name="Excessive Location Collection",
        status="FDO",
        reason="Data collection exceeds functional necessity",
        confidence=0.85,
    ),
)

    assert (
        overreach_uri("overreach-1"),
        RDF.type,
        FDO.Overreach,
    ) in graph


def test_overreach_can_reference_personal_data():
    graph = build_rdf_graph()

    add_overreach(
    graph,
    Overreach(
        id="overreach-1",
        name="Excessive Location Collection",
        status="FDO",
        reason="Data collection exceeds functional necessity",
        confidence=0.85,
    ),
)

    connect_overreach_data(
        graph,
        "overreach-1",
        "location",
    )

    assert (
        overreach_uri("overreach-1"),
        FDO.concernsData,
        personal_data_uri("location"),
    ) in graph


def test_overreach_can_reference_function():
    graph = build_rdf_graph()

    add_overreach(
    graph,
    Overreach(
        id="overreach-1",
        name="Excessive Location Collection",
        status="FDO",
        reason="Data collection exceeds functional necessity",
        confidence=0.85,
    ),
)

    connect_overreach_function(
        graph,
        "overreach-1",
        "navigation",
    )

    assert (
        overreach_uri("overreach-1"),
        FDO.concernsFunction,
        function_uri("navigation"),
    ) in graph


def test_overreach_can_have_justification():
    graph = build_rdf_graph()

    add_overreach(
    graph,
    Overreach(
        id="overreach-1",
        name="Excessive Location Collection",
        status="FDO",
        reason="Data collection exceeds functional necessity",
        confidence=0.85,
    ),
)

    connect_overreach_justification(
        graph,
        "overreach-1",
        "justification-1",
    )

    assert (
        overreach_uri("overreach-1"),
        FDO.hasJustification,
        justification_uri("justification-1"),
    ) in graph


def test_overreach_can_have_risk():
    graph = build_rdf_graph()

    add_overreach(
    graph,
    Overreach(
        id="overreach-1",
        name="Excessive Location Collection",
        status="FDO",
        reason="Data collection exceeds functional necessity",
        confidence=0.85,
    ),
)

    connect_overreach_risk(
        graph,
        "overreach-1",
        "risk-1",
    )

    assert (
        overreach_uri("overreach-1"),
        FDO.hasRisk,
        risk_uri("risk-1"),
    ) in graph


def test_complete_overreach_relationship_structure():
    graph = build_rdf_graph()

    add_overreach(
    graph,
    Overreach(
        id="overreach-1",
        name="Excessive Location Collection",
        status="FDO",
        reason="Data collection exceeds functional necessity",
        confidence=0.85,
    ),
)

    connect_overreach_data(
        graph,
        "overreach-1",
        "location",
    )

    connect_overreach_function(
        graph,
        "overreach-1",
        "navigation",
    )

    connect_overreach_justification(
        graph,
        "overreach-1",
        "justification-1",
    )

    connect_overreach_risk(
        graph,
        "overreach-1",
        "risk-1",
    )

    subject = overreach_uri("overreach-1")

    assert (subject, RDF.type, FDO.Overreach) in graph
    assert (subject, FDO.concernsData, personal_data_uri("location")) in graph
    assert (subject, FDO.concernsFunction, function_uri("navigation")) in graph
    assert (
        subject,
        FDO.hasJustification,
        justification_uri("justification-1"),
    ) in graph
    assert (
        subject,
        FDO.hasRisk,
        risk_uri("risk-1"),
    ) in graph