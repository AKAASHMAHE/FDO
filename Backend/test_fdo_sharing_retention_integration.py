from app.ontology.namespace import FDO
from app.ontology.classes import DeclaredData
from app.ontology.rdf_instance_builder import (
    build_rdf_graph,
    connect_declared_data_recipient,
    connect_declared_data_retention,
)
from app.ontology.uri import (
    declared_data_uri,
    recipient_uri,
    retention_policy_uri,
)


def test_declared_data_can_connect_to_recipient():
    graph = build_rdf_graph(
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Location",
                data_type="location",
                sharing="third-party analytics",
            )
        ]
    )

    connect_declared_data_recipient(
        graph,
        "decl-1",
        "third-party-analytics",
    )

    assert (
        declared_data_uri("decl-1"),
        FDO.sharedWith,
        recipient_uri("third-party-analytics"),
    ) in graph


def test_declared_data_can_connect_to_retention_policy():
    graph = build_rdf_graph(
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Location",
                data_type="location",
                retention="30 days",
            )
        ]
    )

    connect_declared_data_retention(
        graph,
        "decl-1",
        "retention-30-days",
    )

    assert (
        declared_data_uri("decl-1"),
        FDO.hasRetentionPolicy,
        retention_policy_uri("retention-30-days"),
    ) in graph


def test_recipient_uri_is_stable():
    first = recipient_uri("third-party-analytics")
    second = recipient_uri("third-party-analytics")

    assert first == second


def test_retention_uri_is_stable():
    first = retention_policy_uri("retention-30-days")
    second = retention_policy_uri("retention-30-days")

    assert first == second


def test_recipient_names_are_normalized():
    graph = build_rdf_graph(
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Location",
                data_type="location",
            )
        ]
    )

    connect_declared_data_recipient(
        graph,
        "decl-1",
        "Third-Party-Analytics",
    )

    assert (
        declared_data_uri("decl-1"),
        FDO.sharedWith,
        recipient_uri("third-party-analytics"),
    ) in graph


def test_retention_names_are_normalized():
    graph = build_rdf_graph(
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Location",
                data_type="location",
            )
        ]
    )

    connect_declared_data_retention(
        graph,
        "decl-1",
        "Retention-30-Days",
    )

    assert (
        declared_data_uri("decl-1"),
        FDO.hasRetentionPolicy,
        retention_policy_uri("retention-30-days"),
    ) in graph


def test_multiple_recipients_remain_distinct():
    first = recipient_uri("service-provider")
    second = recipient_uri("advertising-partner")

    assert first != second


def test_multiple_retention_policies_remain_distinct():
    first = retention_policy_uri("30-days")
    second = retention_policy_uri("90-days")

    assert first != second


def test_declared_data_can_have_both_sharing_and_retention():
    graph = build_rdf_graph(
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Location",
                data_type="location",
                sharing="third-party analytics",
                retention="30 days",
            )
        ]
    )

    connect_declared_data_recipient(
        graph,
        "decl-1",
        "third-party-analytics",
    )

    connect_declared_data_retention(
        graph,
        "decl-1",
        "retention-30-days",
    )

    assert (
        declared_data_uri("decl-1"),
        FDO.sharedWith,
        recipient_uri("third-party-analytics"),
    ) in graph

    assert (
        declared_data_uri("decl-1"),
        FDO.hasRetentionPolicy,
        retention_policy_uri("retention-30-days"),
    ) in graph