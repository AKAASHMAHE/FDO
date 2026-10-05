from rdflib import RDF

from app.ontology.namespace import FDO
from app.ontology.classes import ExpectedData, DeclaredData
from app.ontology.rdf_instance_builder import (
    build_rdf_graph,
    connect_expected_data_purpose,
    connect_declared_data_purpose,
)
from app.ontology.uri import (
    expected_data_uri,
    declared_data_uri,
    purpose_uri,
)


def test_expected_data_can_connect_to_purpose():
    graph = build_rdf_graph(
        expected_data=[
            ExpectedData(
                id="exp-1",
                name="Location",
                data_type="location",
                purpose="navigation",
            )
        ]
    )

    connect_expected_data_purpose(
        graph,
        "exp-1",
        "navigation",
    )

    assert (
        expected_data_uri("exp-1"),
        FDO.expectedDataPurpose,
        purpose_uri("navigation"),
    ) in graph


def test_declared_data_can_connect_to_purpose():
    graph = build_rdf_graph(
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Location",
                data_type="location",
                purpose="navigation",
            )
        ]
    )

    connect_declared_data_purpose(
        graph,
        "decl-1",
        "navigation",
    )

    assert (
        declared_data_uri("decl-1"),
        FDO.declaredDataPurpose,
        purpose_uri("navigation"),
    ) in graph


def test_purpose_uri_is_stable():
    first = purpose_uri("navigation")
    second = purpose_uri("navigation")

    assert first == second


def test_purpose_names_are_normalized():
    graph = build_rdf_graph(
        expected_data=[
            ExpectedData(
                id="exp-1",
                name="Location",
                data_type="location",
                purpose="navigation",
            )
        ]
    )

    connect_expected_data_purpose(
        graph,
        "exp-1",
        "Navigation",
    )

    assert (
        expected_data_uri("exp-1"),
        FDO.expectedDataPurpose,
        purpose_uri("navigation"),
    ) in graph


def test_different_purposes_remain_distinct():
    navigation = purpose_uri("navigation")
    advertising = purpose_uri("advertising")
    analytics = purpose_uri("analytics")

    assert navigation != advertising
    assert navigation != analytics
    assert advertising != analytics


def test_expected_and_declared_purpose_can_be_compared_semantically():
    graph = build_rdf_graph(
        expected_data=[
            ExpectedData(
                id="exp-1",
                name="Location",
                data_type="location",
                purpose="navigation",
            )
        ],
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Location",
                data_type="location",
                purpose="navigation",
            )
        ],
    )

    connect_expected_data_purpose(
        graph,
        "exp-1",
        "navigation",
    )

    connect_declared_data_purpose(
        graph,
        "decl-1",
        "navigation",
    )

    expected_purpose = list(
        graph.objects(
            expected_data_uri("exp-1"),
            FDO.expectedDataPurpose,
        )
    )

    declared_purpose = list(
        graph.objects(
            declared_data_uri("decl-1"),
            FDO.declaredDataPurpose,
        )
    )

    assert expected_purpose == [purpose_uri("navigation")]
    assert declared_purpose == [purpose_uri("navigation")]