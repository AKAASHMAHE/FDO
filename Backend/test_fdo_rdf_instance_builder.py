from rdflib import RDF

from app.ontology.classes import (
    Application,
    Function,
    ExpectedData,
    DeclaredData,
    PrivacyPolicy,
    PolicyClause,
    Overreach,
)
from app.ontology.namespace import FDO

from app.ontology.rdf_instance_builder import (
    add_application,
    add_function,
    add_expected_data,
    add_declared_data,
    add_privacy_policy,
    add_policy_clause,
    add_overreach,
    connect_application_function,
    connect_function_expected_data,
    connect_application_declared_data,
    connect_declared_data_policy_clause,
    connect_policy_clause_policy,
    connect_data_purpose,
    connect_data_recipient,
    connect_data_retention,
    connect_overreach_data,
    connect_overreach_function,
    connect_overreach_justification,
    connect_overreach_risk,
    build_rdf_graph,
)

from app.ontology.uri import (
    application_uri,
    function_uri,
    expected_data_uri,
    declared_data_uri,
    policy_uri,
    policy_clause_uri,
    personal_data_uri,
    purpose_uri,
    recipient_uri,
    retention_policy_uri,
    overreach_uri,
    justification_uri,
    risk_uri,
)


def test_add_application():
    graph = build_rdf_graph(
        applications=[
            Application(
                id="1",
                name="Test Application",
                category="Communication",
                description="Test app",
            )
        ]
    )

    subject = application_uri("1")

    assert (subject, RDF.type, FDO.Application) in graph
    assert (subject, FDO.name, None) in graph


def test_add_function():
    graph = build_rdf_graph(
        functions=[
            Function(
                id="1",
                name="Messaging",
                description="Send messages",
            )
        ]
    )

    subject = function_uri("1")

    assert (subject, RDF.type, FDO.Function) in graph


def test_add_expected_data():
    graph = build_rdf_graph(
        expected_data=[
            ExpectedData(
                id="1",
                name="Expected Phone Number",
                data_type="phone_number",
                necessity="required",
                purpose="communication",
            )
        ]
    )

    subject = expected_data_uri("1")

    assert (subject, RDF.type, FDO.ExpectedData) in graph


def test_add_declared_data():
    graph = build_rdf_graph(
        declared_data=[
            DeclaredData(
                id="1",
                name="Declared Location",
                data_type="location",
                purpose="advertising",
                sharing="third_party",
                retention="90 days",
            )
        ]
    )

    subject = declared_data_uri("1")

    assert (subject, RDF.type, FDO.DeclaredData) in graph


def test_add_policy():
    graph = build_rdf_graph(
        policies=[
            PrivacyPolicy(
                id="1",
                name="Test Policy",
                source="test-policy.txt",
                version="1.0",
            )
        ]
    )

    subject = policy_uri("1")

    assert (subject, RDF.type, FDO.PrivacyPolicy) in graph


def test_add_policy_clause():
    graph = build_rdf_graph(
        policy_clauses=[
            PolicyClause(
                id="1",
                name="Clause 1",
                text="We collect location data.",
                source="policy",
                section="Data Collection",
            )
        ]
    )

    subject = policy_clause_uri("1")

    assert (subject, RDF.type, FDO.PolicyClause) in graph


def test_add_overreach():
    graph = build_rdf_graph(
        overreach_findings=[
            Overreach(
                id="1",
                name="FDO Finding 1",
                status="FDO",
                reason="Data exceeds functional requirement.",
                confidence=0.85,
            )
        ]
    )

    subject = overreach_uri("1")

    assert (subject, RDF.type, FDO.Overreach) in graph


def test_connect_application_function():
    graph = build_rdf_graph(
        applications=[
            Application(id="1", name="Test App")
        ],
        functions=[
            Function(id="2", name="Messaging")
        ],
    )

    connect_application_function(graph, "1", "2")

    assert (
        application_uri("1"),
        FDO.performsFunction,
        function_uri("2"),
    ) in graph


def test_connect_function_expected_data():
    graph = build_rdf_graph(
        functions=[
            Function(id="1", name="Messaging")
        ],
        expected_data=[
            ExpectedData(
                id="2",
                name="Phone Number",
                data_type="phone_number",
            )
        ],
    )

    connect_function_expected_data(graph, "1", "2")

    assert (
        function_uri("1"),
        FDO.expectedData,
        expected_data_uri("2"),
    ) in graph

    assert (
        expected_data_uri("2"),
        FDO.expectedForFunction,
        function_uri("1"),
    ) in graph


def test_connect_application_declared_data():
    graph = build_rdf_graph(
        applications=[
            Application(id="1", name="Test App")
        ],
        declared_data=[
            DeclaredData(
                id="2",
                name="Location",
                data_type="location",
            )
        ],
    )

    connect_application_declared_data(graph, "1", "2")

    assert (
        application_uri("1"),
        FDO.declaredData,
        declared_data_uri("2"),
    ) in graph

    assert (
        declared_data_uri("2"),
        FDO.declaredByApplication,
        application_uri("1"),
    ) in graph


def test_policy_traceability_relationships():
    graph = build_rdf_graph()

    connect_declared_data_policy_clause(graph, "1", "2")
    connect_policy_clause_policy(graph, "2", "3")

    assert (
        declared_data_uri("1"),
        FDO.supportedByClause,
        policy_clause_uri("2"),
    ) in graph

    assert (
        policy_clause_uri("2"),
        FDO.supportedByPolicy,
        policy_uri("3"),
    ) in graph


def test_purpose_relationship():
    graph = build_rdf_graph()

    connect_data_purpose(graph, "1", "2")

    assert (
        personal_data_uri("1"),
        FDO.usedForPurpose,
        purpose_uri("2"),
    ) in graph


def test_recipient_relationship():
    graph = build_rdf_graph()

    connect_data_recipient(graph, "1", "2")

    assert (
        personal_data_uri("1"),
        FDO.sharedWith,
        recipient_uri("2"),
    ) in graph


def test_retention_relationship():
    graph = build_rdf_graph()

    connect_data_retention(graph, "1", "2")

    assert (
        personal_data_uri("1"),
        FDO.hasRetentionPolicy,
        retention_policy_uri("2"),
    ) in graph


def test_overreach_relationships():
    graph = build_rdf_graph()

    connect_overreach_data(graph, "1", "2")
    connect_overreach_function(graph, "1", "3")
    connect_overreach_justification(graph, "1", "4")
    connect_overreach_risk(graph, "1", "5")

    assert (
        overreach_uri("1"),
        FDO.concernsData,
        personal_data_uri("2"),
    ) in graph

    assert (
        overreach_uri("1"),
        FDO.concernsFunction,
        function_uri("3"),
    ) in graph

    assert (
        overreach_uri("1"),
        FDO.hasJustification,
        justification_uri("4"),
    ) in graph

    assert (
        overreach_uri("1"),
        FDO.hasRisk,
        risk_uri("5"),
    ) in graph


def test_build_multiple_entities():
    graph = build_rdf_graph(
        applications=[
            Application(id="1", name="App A"),
            Application(id="2", name="App B"),
        ],
        functions=[
            Function(id="1", name="Function A"),
            Function(id="2", name="Function B"),
        ],
        expected_data=[
            ExpectedData(
                id="1",
                name="Expected Data",
                data_type="location",
            )
        ],
        declared_data=[
            DeclaredData(
                id="1",
                name="Declared Data",
                data_type="location",
            )
        ],
    )

    assert len(graph) > 0

    assert (
        application_uri("1"),
        RDF.type,
        FDO.Application,
    ) in graph

    assert (
        application_uri("2"),
        RDF.type,
        FDO.Application,
    ) in graph

    assert (
        function_uri("1"),
        RDF.type,
        FDO.Function,
    ) in graph

    assert (
        function_uri("2"),
        RDF.type,
        FDO.Function,
    ) in graph


def test_rdf_graph_can_serialize():
    graph = build_rdf_graph(
        applications=[
            Application(
                id="1",
                name="Test Application",
            )
        ]
    )

    turtle = graph.serialize(format="turtle")

    assert "fdo:Application" in turtle
    assert "fdo:name" in turtle