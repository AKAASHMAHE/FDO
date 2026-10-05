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
    justification_uri,
    risk_uri,
)


def test_complete_application_function_data_chain():
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

    assert (
        application_uri("app-1"),
        RDF.type,
        FDO.Application,
    ) in graph

    assert (
        function_uri("fn-1"),
        RDF.type,
        FDO.Function,
    ) in graph

    assert (
        expected_data_uri("exp-1"),
        RDF.type,
        FDO.ExpectedData,
    ) in graph

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
        expected_data_uri("exp-1"),
        FDO.expectedForFunction,
        function_uri("fn-1"),
    ) in graph


def test_complete_policy_traceability_chain():
    graph = build_rdf_graph(
        applications=[
            Application(
                id="app-1",
                name="Test App",
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
                source="privacy-policy.txt",
                version="1.0",
            )
        ],
        policy_clauses=[
            PolicyClause(
                id="clause-1",
                name="Location Clause",
                text="We collect location data.",
                source="privacy-policy.txt",
                section="Data Collection",
            )
        ],
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
        FDO.declaredData,
        declared_data_uri("decl-1"),
    ) in graph

    assert (
        declared_data_uri("decl-1"),
        FDO.declaredByApplication,
        application_uri("app-1"),
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


def test_complete_fdo_finding_chain():
    graph = build_rdf_graph(
        applications=[
            Application(
                id="app-1",
                name="Test App",
            )
        ],
        functions=[
            Function(
                id="fn-1",
                name="Navigation",
            )
        ],
        overreach_findings=[
            Overreach(
                id="fdo-1",
                name="FDO Finding",
                status="FDO",
                reason="Location is used for an unrelated purpose.",
                confidence=0.85,
            )
        ],
    )

    connect_overreach_data(
        graph,
        "fdo-1",
        "location",
    )

    connect_overreach_function(
        graph,
        "fdo-1",
        "fn-1",
    )

    connect_overreach_justification(
        graph,
        "fdo-1",
        "justification-1",
    )

    connect_overreach_risk(
        graph,
        "fdo-1",
        "risk-1",
    )

    assert (
        overreach_uri("fdo-1"),
        RDF.type,
        FDO.Overreach,
    ) in graph

    assert (
        overreach_uri("fdo-1"),
        FDO.concernsData,
        personal_data_uri("location"),
    ) in graph

    assert (
        overreach_uri("fdo-1"),
        FDO.concernsFunction,
        function_uri("fn-1"),
    ) in graph

    assert (
        overreach_uri("fdo-1"),
        FDO.hasJustification,
        justification_uri("justification-1"),
    ) in graph

    assert (
        overreach_uri("fdo-1"),
        FDO.hasRisk,
        risk_uri("risk-1"),
    ) in graph


def test_multiple_applications_remain_separate():
    graph = build_rdf_graph(
        applications=[
            Application(
                id="app-1",
                name="Navigation App",
            ),
            Application(
                id="app-2",
                name="Messaging App",
            ),
        ],
        functions=[
            Function(
                id="fn-1",
                name="Navigation",
            ),
            Function(
                id="fn-2",
                name="Messaging",
            ),
        ],
    )

    connect_application_function(
        graph,
        "app-1",
        "fn-1",
    )

    connect_application_function(
        graph,
        "app-2",
        "fn-2",
    )

    assert (
        application_uri("app-1"),
        FDO.performsFunction,
        function_uri("fn-1"),
    ) in graph

    assert (
        application_uri("app-2"),
        FDO.performsFunction,
        function_uri("fn-2"),
    ) in graph

    assert (
        application_uri("app-1"),
        FDO.performsFunction,
        function_uri("fn-2"),
    ) not in graph

    assert (
        application_uri("app-2"),
        FDO.performsFunction,
        function_uri("fn-1"),
    ) not in graph


def test_graph_contains_all_relationships():
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
                name="Location",
                data_type="location",
            )
        ],
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Location",
                data_type="location",
            )
        ],
        policies=[
            PrivacyPolicy(
                id="policy-1",
                name="Policy",
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

    connect_application_function(graph, "app-1", "fn-1")
    connect_function_expected_data(graph, "fn-1", "exp-1")
    connect_application_declared_data(graph, "app-1", "decl-1")
    connect_declared_data_policy_clause(graph, "decl-1", "clause-1")
    connect_policy_clause_policy(graph, "clause-1", "policy-1")

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