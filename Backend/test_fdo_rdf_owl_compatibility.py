from pathlib import Path

from rdflib import Graph, RDF, RDFS, OWL

from app.ontology.namespace import FDO
from app.ontology.rdf_instance_builder import (
    build_rdf_graph,
    connect_application_function,
    connect_function_expected_data,
    connect_application_declared_data,
    connect_declared_data_policy_clause,
    connect_policy_clause_policy,
)

from app.ontology.classes import (
    Application,
    Function,
    ExpectedData,
    DeclaredData,
    PrivacyPolicy,
    PolicyClause,
)

from app.ontology.uri import (
    application_uri,
    function_uri,
    expected_data_uri,
    declared_data_uri,
    policy_uri,
    policy_clause_uri,
)


# ============================================================
# Helpers
# ============================================================

def load_fdo_ontology():
    """
    Load the generated FDO OWL ontology.

    The committed ontology is expected at:

        Backend/ontology/FDO.owl

    If it is not there, the test also checks:

        Backend/app/ontology/FDO.owl
    """

    backend_root = Path(__file__).resolve().parent

    candidates = [
        backend_root / "ontology" / "FDO.owl",
        backend_root / "app" / "ontology" / "FDO.owl",
    ]

    ontology_path = next(
        (path for path in candidates if path.exists()),
        None,
    )

    assert ontology_path is not None, (
        "FDO.owl was not found in either "
        "Backend/ontology/FDO.owl or "
        "Backend/app/ontology/FDO.owl"
    )

    graph = Graph()
    graph.parse(
        ontology_path,
        format="xml",
    )

    return graph


# ============================================================
# Ontology Loading
# ============================================================

def test_fdo_owl_can_be_loaded():
    ontology = load_fdo_ontology()

    assert isinstance(ontology, Graph)
    assert len(ontology) > 0


def test_fdo_ontology_declaration_exists():
    ontology = load_fdo_ontology()

    assert (
        FDO.Ontology,
        RDF.type,
        OWL.Ontology,
    ) in ontology


# ============================================================
# Class Compatibility
# ============================================================

def test_core_fdo_classes_exist():
    ontology = load_fdo_ontology()

    expected_classes = [
        FDO.Application,
        FDO.Function,
        FDO.PersonalData,
        FDO.SensitiveData,
        FDO.ProcessingActivity,
        FDO.Purpose,
        FDO.Recipient,
        FDO.RetentionPolicy,
        FDO.User,
        FDO.UserRight,
        FDO.Consent,
        FDO.PrivacyPolicy,
        FDO.PolicyClause,
        FDO.ExpectedData,
        FDO.DeclaredData,
        FDO.Overreach,
        FDO.Justification,
        FDO.Risk,
    ]

    for class_uri in expected_classes:
        assert (
            class_uri,
            RDF.type,
            OWL.Class,
        ) in ontology


# ============================================================
# Object Property Compatibility
# ============================================================

def test_core_object_properties_exist():
    ontology = load_fdo_ontology()

    expected_properties = [
        FDO.performsFunction,
        FDO.requiresData,
        FDO.collectsData,
        FDO.declaredData,
        FDO.expectedData,
        FDO.expectedForFunction,
        FDO.declaredByApplication,
        FDO.usedForPurpose,
        FDO.processedBy,
        FDO.sharedWith,
        FDO.hasRetentionPolicy,
        FDO.supportedByClause,
        FDO.supportedByPolicy,
        FDO.hasUserRight,
        FDO.hasConsent,
        FDO.hasJustification,
        FDO.concernsData,
        FDO.concernsFunction,
        FDO.hasRisk,
        FDO.hasUser,
    ]

    for property_uri in expected_properties:
        assert (
            property_uri,
            RDF.type,
            OWL.ObjectProperty,
        ) in ontology


# ============================================================
# Domain / Range Compatibility
# ============================================================

def test_performs_function_domain_and_range():
    ontology = load_fdo_ontology()

    assert (
        FDO.performsFunction,
        RDFS.domain,
        FDO.Application,
    ) in ontology

    assert (
        FDO.performsFunction,
        RDFS.range,
        FDO.Function,
    ) in ontology


def test_expected_data_domain_and_range():
    ontology = load_fdo_ontology()

    assert (
        FDO.expectedData,
        RDFS.domain,
        FDO.Function,
    ) in ontology

    assert (
        FDO.expectedData,
        RDFS.range,
        FDO.ExpectedData,
    ) in ontology


def test_declared_data_domain_and_range():
    ontology = load_fdo_ontology()

    assert (
        FDO.declaredData,
        RDFS.domain,
        FDO.Application,
    ) in ontology

    assert (
        FDO.declaredData,
        RDFS.range,
        FDO.DeclaredData,
    ) in ontology


def test_policy_traceability_domain_and_range():
    ontology = load_fdo_ontology()

    assert (
        FDO.supportedByClause,
        RDFS.domain,
        FDO.DeclaredData,
    ) in ontology

    assert (
        FDO.supportedByClause,
        RDFS.range,
        FDO.PolicyClause,
    ) in ontology

    assert (
        FDO.supportedByPolicy,
        RDFS.domain,
        FDO.PolicyClause,
    ) in ontology

    assert (
        FDO.supportedByPolicy,
        RDFS.range,
        FDO.PrivacyPolicy,
    ) in ontology


# ============================================================
# Generated RDF Instance Compatibility
# ============================================================

def test_generated_application_instance_uses_declared_class():
    ontology = load_fdo_ontology()

    graph = build_rdf_graph(
        applications=[
            Application(
                id="app-1",
                name="Navigation App",
            )
        ]
    )

    instance = application_uri("app-1")

    assert (
        instance,
        RDF.type,
        FDO.Application,
    ) in graph

    assert (
        FDO.Application,
        RDF.type,
        OWL.Class,
    ) in ontology


def test_generated_function_instance_uses_declared_class():
    ontology = load_fdo_ontology()

    graph = build_rdf_graph(
        functions=[
            Function(
                id="fn-1",
                name="Navigation",
            )
        ]
    )

    instance = function_uri("fn-1")

    assert (
        instance,
        RDF.type,
        FDO.Function,
    ) in graph

    assert (
        FDO.Function,
        RDF.type,
        OWL.Class,
    ) in ontology


def test_generated_expected_data_instance_uses_declared_class():
    ontology = load_fdo_ontology()

    graph = build_rdf_graph(
        expected_data=[
            ExpectedData(
                id="exp-1",
                name="Location",
                data_type="location",
            )
        ]
    )

    instance = expected_data_uri("exp-1")

    assert (
        instance,
        RDF.type,
        FDO.ExpectedData,
    ) in graph

    assert (
        FDO.ExpectedData,
        RDF.type,
        OWL.Class,
    ) in ontology


def test_generated_declared_data_instance_uses_declared_class():
    ontology = load_fdo_ontology()

    graph = build_rdf_graph(
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Location",
                data_type="location",
            )
        ]
    )

    instance = declared_data_uri("decl-1")

    assert (
        instance,
        RDF.type,
        FDO.DeclaredData,
    ) in graph

    assert (
        FDO.DeclaredData,
        RDF.type,
        OWL.Class,
    ) in ontology


# ============================================================
# Generated Relationship Compatibility
# ============================================================

def test_generated_application_function_relationship_matches_owl():
    ontology = load_fdo_ontology()

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

    assert (
        application_uri("app-1"),
        FDO.performsFunction,
        function_uri("fn-1"),
    ) in graph

    assert (
        FDO.performsFunction,
        RDF.type,
        OWL.ObjectProperty,
    ) in ontology


def test_generated_expected_data_relationship_matches_owl():
    ontology = load_fdo_ontology()

    graph = build_rdf_graph(
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
    )

    connect_function_expected_data(
        graph,
        "fn-1",
        "exp-1",
    )

    assert (
        function_uri("fn-1"),
        FDO.expectedData,
        expected_data_uri("exp-1"),
    ) in graph

    assert (
        FDO.expectedData,
        RDF.type,
        OWL.ObjectProperty,
    ) in ontology


def test_generated_declared_data_relationship_matches_owl():
    ontology = load_fdo_ontology()

    graph = build_rdf_graph(
        applications=[
            Application(
                id="app-1",
                name="Navigation App",
            )
        ],
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Location",
                data_type="location",
            )
        ],
    )

    connect_application_declared_data(
        graph,
        "app-1",
        "decl-1",
    )

    assert (
        application_uri("app-1"),
        FDO.declaredData,
        declared_data_uri("decl-1"),
    ) in graph

    assert (
        FDO.declaredData,
        RDF.type,
        OWL.ObjectProperty,
    ) in ontology


def test_generated_policy_traceability_relationships_match_owl():
    ontology = load_fdo_ontology()

    graph = build_rdf_graph(
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
        declared_data_uri("decl-1"),
        FDO.supportedByClause,
        policy_clause_uri("clause-1"),
    ) in graph

    assert (
        policy_clause_uri("clause-1"),
        FDO.supportedByPolicy,
        policy_uri("policy-1"),
    ) in graph

    assert (
        FDO.supportedByClause,
        RDF.type,
        OWL.ObjectProperty,
    ) in ontology

    assert (
        FDO.supportedByPolicy,
        RDF.type,
        OWL.ObjectProperty,
    ) in ontology