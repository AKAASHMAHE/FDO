from app.ontology.namespace import FDO
from app.ontology.classes import PersonalData
from app.ontology.rdf_instance_builder import (
    build_rdf_graph,
    connect_data_processing_activity,
)
from app.ontology.uri import (
    personal_data_uri,
    processing_activity_uri,
)


def test_personal_data_can_connect_to_processing_activity():
    graph = build_rdf_graph(
        personal_data=[
            PersonalData(
                id="location",
                name="Location",
            )
        ]
    )

    connect_data_processing_activity(
        graph,
        "location",
        "collect-location",
    )

    assert (
        personal_data_uri("location"),
        FDO.processedBy,
        processing_activity_uri("collect-location"),
    ) in graph


def test_processing_activity_uri_is_stable():
    first = processing_activity_uri("collect-location")
    second = processing_activity_uri("collect-location")

    assert first == second


def test_processing_activity_names_are_normalized():
    graph = build_rdf_graph(
        personal_data=[
            PersonalData(
                id="location",
                name="Location",
            )
        ]
    )

    connect_data_processing_activity(
        graph,
        "location",
        "Collect-Location",
    )

    assert (
        personal_data_uri("location"),
        FDO.processedBy,
        processing_activity_uri("collect-location"),
    ) in graph


def test_collect_processing_activity():
    graph = build_rdf_graph(
        personal_data=[
            PersonalData(
                id="location",
                name="Location",
            )
        ]
    )

    connect_data_processing_activity(
        graph,
        "location",
        "collect-location",
    )

    assert (
        personal_data_uri("location"),
        FDO.processedBy,
        processing_activity_uri("collect-location"),
    ) in graph


def test_store_processing_activity():
    graph = build_rdf_graph(
        personal_data=[
            PersonalData(
                id="email",
                name="Email",
            )
        ]
    )

    connect_data_processing_activity(
        graph,
        "email",
        "store-email",
    )

    assert (
        personal_data_uri("email"),
        FDO.processedBy,
        processing_activity_uri("store-email"),
    ) in graph


def test_use_processing_activity():
    graph = build_rdf_graph(
        personal_data=[
            PersonalData(
                id="email",
                name="Email",
            )
        ]
    )

    connect_data_processing_activity(
        graph,
        "email",
        "use-email",
    )

    assert (
        personal_data_uri("email"),
        FDO.processedBy,
        processing_activity_uri("use-email"),
    ) in graph


def test_share_processing_activity():
    graph = build_rdf_graph(
        personal_data=[
            PersonalData(
                id="contacts",
                name="Contacts",
            )
        ]
    )

    connect_data_processing_activity(
        graph,
        "contacts",
        "share-contacts",
    )

    assert (
        personal_data_uri("contacts"),
        FDO.processedBy,
        processing_activity_uri("share-contacts"),
    ) in graph


def test_disclose_processing_activity():
    graph = build_rdf_graph(
        personal_data=[
            PersonalData(
                id="email",
                name="Email",
            )
        ]
    )

    connect_data_processing_activity(
        graph,
        "email",
        "disclose-email",
    )

    assert (
        personal_data_uri("email"),
        FDO.processedBy,
        processing_activity_uri("disclose-email"),
    ) in graph


def test_retain_processing_activity():
    graph = build_rdf_graph(
        personal_data=[
            PersonalData(
                id="location",
                name="Location",
            )
        ]
    )

    connect_data_processing_activity(
        graph,
        "location",
        "retain-location",
    )

    assert (
        personal_data_uri("location"),
        FDO.processedBy,
        processing_activity_uri("retain-location"),
    ) in graph


def test_delete_processing_activity():
    graph = build_rdf_graph(
        personal_data=[
            PersonalData(
                id="location",
                name="Location",
            )
        ]
    )

    connect_data_processing_activity(
        graph,
        "location",
        "delete-location",
    )

    assert (
        personal_data_uri("location"),
        FDO.processedBy,
        processing_activity_uri("delete-location"),
    ) in graph


def test_multiple_processing_activities_are_distinct():
    collect = processing_activity_uri("collect-location")
    store = processing_activity_uri("store-location")
    share = processing_activity_uri("share-location")

    assert collect != store
    assert collect != share
    assert store != share


def test_personal_data_can_have_multiple_processing_activities():
    graph = build_rdf_graph(
        personal_data=[
            PersonalData(
                id="location",
                name="Location",
            )
        ]
    )

    connect_data_processing_activity(
        graph,
        "location",
        "collect-location",
    )

    connect_data_processing_activity(
        graph,
        "location",
        "store-location",
    )

    connect_data_processing_activity(
        graph,
        "location",
        "share-location",
    )

    activities = list(
        graph.objects(
            personal_data_uri("location"),
            FDO.processedBy,
        )
    )

    assert set(activities) == {
        processing_activity_uri("collect-location"),
        processing_activity_uri("store-location"),
        processing_activity_uri("share-location"),
    }