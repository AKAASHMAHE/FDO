from rdflib import Graph, RDF, RDFS, OWL
from rdflib import URIRef, Literal
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
    build_rdf_graph,
    connect_application_function,
    connect_function_expected_data,
    connect_application_declared_data,
    connect_declared_data_policy_clause,
    connect_policy_clause_policy,
    connect_overreach_data,
    connect_overreach_function,
    connect_overreach_justification,
    connect_overreach_risk,
)

from app.ontology.uri import (
    application_uri,
    function_uri,
    expected_data_uri,
    declared_data_uri,
    policy_uri,
    policy_clause_uri,
    personal_data_uri,
    overreach_uri,
)


def test_graph_is_rdflib_graph():
    graph = build_rdf_graph()

    assert isinstance(graph, Graph)


def test_fdo_namespace_is_bound():
    graph = build_rdf_graph()

    namespaces = dict(graph.namespaces())

    assert "fdo" in namespaces
    assert str(namespaces["fdo"]) == str(FDO)


def test_application_has_valid_rdf_type():
    graph = build_rdf_graph(
        applications=[
            Application(
                id="app-1",
                name="Test Application",
            )
        ]
    )

    subject = application_uri("app-1")

    assert (
        subject,
        RDF.type,
        FDO.Application,
    ) in graph


def test_function_has_valid_rdf_type():
    graph = build_rdf_graph(
        functions=[
            Function(
                id="fn-1",
                name="Test Function",
            )
        ]
    )

    subject = function_uri("fn-1")

    assert (
        subject,
        RDF.type,
        FDO.Function,
    ) in graph


def test_expected_data_has_valid_rdf_type():
    graph = build_rdf_graph(
        expected_data=[
            ExpectedData(
                id="exp-1",
                name="Location",
                data_type="location",
            )
        ]
    )

    subject = expected_data_uri("exp-1")

    assert (
        subject,
        RDF.type,
        FDO.ExpectedData,
    ) in graph


def test_declared_data_has_valid_rdf_type():
    graph = build_rdf_graph(
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Location",
                data_type="location",
            )
        ]
    )

    subject = declared_data_uri("decl-1")

    assert (
        subject,
        RDF.type,
        FDO.DeclaredData,
    ) in graph


def test_policy_has_valid_rdf_type():
    graph = build_rdf_graph(
        policies=[
            PrivacyPolicy(
                id="policy-1",
                name="Privacy Policy",
                source="policy.txt",
            )
        ]
    )

    subject = policy_uri("policy-1")

    assert (
        subject,
        RDF.type,
        FDO.PrivacyPolicy,
    ) in graph


def test_policy_clause_has_valid_rdf_type():
    graph = build_rdf_graph(
        policy_clauses=[
            PolicyClause(
                id="clause-1",
                name="Location Clause",
                text="We collect location data.",
            )
        ]
    )

    subject = policy_clause_uri("clause-1")

    assert (
        subject,
        RDF.type,
        FDO.PolicyClause,
    ) in graph


def test_overreach_has_valid_rdf_type():
    graph = build_rdf_graph(
        overreach_findings=[
            Overreach(
                id="fdo-1",
                name="FDO Finding",
                status="FDO",
                reason="Unnecessary data collection.",
                confidence=0.85,
            )
        ]
    )

    subject = overreach_uri("fdo-1")

    assert (
        subject,
        RDF.type,
        FDO.Overreach,
    ) in graph


def test_relationship_objects_are_uri_resources():
    graph = build_rdf_graph(
        applications=[
            Application(
                id="app-1",
                name="Test Application",
            )
        ],
        functions=[
            Function(
                id="fn-1",
                name="Navigation",
            )
        ],
    )

    connect_application_function(
        graph,
        "app-1",
        "fn-1",
    )

    subject, predicate, obj = next(
        graph.triples(
            (
                application_uri("app-1"),
                FDO.performsFunction,
                None,
            )
        )
    )

    assert subject == application_uri("app-1")
    assert predicate == FDO.performsFunction
    assert obj == function_uri("fn-1")

    assert str(obj).startswith(
        "http://example.org/fdo#resource/"
    )


def test_relationships_do_not_use_literals_as_objects():
    graph = build_rdf_graph(
        applications=[
            Application(
                id="app-1",
                name="Test Application",
            )
        ],
        functions=[
            Function(
                id="fn-1",
                name="Navigation",
            )
        ],
    )

    connect_application_function(
        graph,
        "app-1",
        "fn-1",
    )

    objects = list(
        graph.objects(
            application_uri("app-1"),
            FDO.performsFunction,
        )
    )

    assert len(objects) == 1
    assert isinstance(objects[0], URIRef)
    assert not isinstance(objects[0], Literal)  


def test_complete_graph_contains_expected_relationships():
    graph = build_rdf_graph(
        applications=[
            Application(
                id="app-1",
                name="Navigation App",
            )
        ],
        functions=[
            Function(
                id="fn-1",
                name="Navigation",
            )
        ],
        expected_data=[
            ExpectedData(
                id="exp-1",
                name="Expected Location",
                data_type="location",
                necessity="required",
                purpose="navigation",
            )
        ],
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Declared Location",
                data_type="location",
                purpose="navigation",
            )
        ],
        policies=[
            PrivacyPolicy(
                id="policy-1",
                name="Privacy Policy",
                source="policy.txt",
            )
        ],
        policy_clauses=[
            PolicyClause(
                id="clause-1",
                name="Location Clause",
                text="Location is collected.",
            )
        ],
    )

    connect_application_function(
        graph,
        "app-1",
        "fn-1",
    )

    connect_function_expected_data(
        graph,
        "fn-1",
        "exp-1",
    )

    connect_application_declared_data(
        graph,
        "app-1",
        "decl-1",
    )

    connect_declared_data_policy_clause(
        graph,
        "decl-1",
        "clause-1",
    )

    connect_policy_clause_policy(
        graph,
        "clause-1",
        "policy-1",
    )

    assert (
        application_uri("app-1"),
        FDO.performsFunction,
        function_uri("fn-1"),
    ) in graph

    assert (
        function_uri("fn-1"),
        FDO.expectedData,
        expected_data_uri("exp-1"),
    ) in graph

    assert (
        application_uri("app-1"),
        FDO.declaredData,
        declared_data_uri("decl-1"),
    ) in graph

    assert (
        declared_data_uri("decl-1"),
        FDO.supportedByClause,
        policy_clause_uri("clause-1"),
    ) in graph

    assert (
        policy_clause_uri("clause-1"),
        FDO.supportedByPolicy,
        policy_uri("policy-1"),
    ) in graph


def test_graph_can_round_trip_through_turtle():
    graph = build_rdf_graph(
        applications=[
            Application(
                id="app-1",
                name="Navigation App",
            )
        ],
        functions=[
            Function(
                id="fn-1",
                name="Navigation",
            )
        ],
    )

    connect_application_function(
        graph,
        "app-1",
        "fn-1",
    )

    turtle_data = graph.serialize(format="turtle")

    assert turtle_data
    assert "fdo:Application" in turtle_data
    assert "fdo:Function" in turtle_data
    assert "fdo:performsFunction" in turtle_data

    restored_graph = Graph()
    restored_graph.parse(
        data=turtle_data,
        format="turtle",
    )

    assert len(restored_graph) == len(graph)

    assert (
        application_uri("app-1"),
        RDF.type,
        FDO.Application,
    ) in restored_graph

    assert (
        application_uri("app-1"),
        FDO.performsFunction,
        function_uri("fn-1"),
    ) in restored_graph


def test_graph_contains_no_blank_nodes():
    graph = build_rdf_graph(
        applications=[
            Application(
                id="app-1",
                name="Test Application",
            )
        ],
        functions=[
            Function(
                id="fn-1",
                name="Test Function",
            )
        ],
    )

    connect_application_function(
        graph,
        "app-1",
        "fn-1",
    )

    for subject, predicate, obj in graph:
        assert not subject.startswith("_:")
        assert not predicate.startswith("_:")
        assert not obj.startswith("_:") if hasattr(obj, "startswith") else True


def test_empty_graph_is_valid():
    graph = build_rdf_graph()

    assert isinstance(graph, Graph)
    assert len(graph) > 0
    assert any(graph.triples((None, RDFS.subClassOf, None)))
    assert not list(graph.subjects(RDF.type, FDO.Application))