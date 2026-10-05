from rdflib import URIRef

from app.ontology.uri import (
    RESOURCE_BASE_URI,
    build_resource_uri,
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


def test_build_resource_uri():
    result = build_resource_uri("application", 123)

    assert isinstance(result, URIRef)
    assert str(result) == (
        f"{RESOURCE_BASE_URI}application/123"
    )


def test_resource_uri_is_stable():
    first = application_uri(1)
    second = application_uri(1)

    assert first == second


def test_different_entities_have_different_uris():
    first = application_uri(1)
    second = application_uri(2)

    assert first != second


def test_application_uri():
    assert str(application_uri(1)).endswith(
        "/application/1"
    )


def test_function_uri():
    assert str(function_uri(5)).endswith(
        "/function/5"
    )


def test_expected_data_uri():
    assert str(expected_data_uri(10)).endswith(
        "/expected-data/10"
    )


def test_declared_data_uri():
    assert str(declared_data_uri(11)).endswith(
        "/declared-data/11"
    )


def test_policy_uri():
    assert str(policy_uri(20)).endswith(
        "/policy/20"
    )


def test_policy_clause_uri():
    assert str(policy_clause_uri(21)).endswith(
        "/policy-clause/21"
    )


def test_personal_data_uri():
    assert str(personal_data_uri(30)).endswith(
        "/personal-data/30"
    )


def test_purpose_uri():
    assert str(purpose_uri(31)).endswith(
        "/purpose/31"
    )


def test_recipient_uri():
    assert str(recipient_uri(32)).endswith(
        "/recipient/32"
    )


def test_retention_policy_uri():
    assert str(retention_policy_uri(33)).endswith(
        "/retention-policy/33"
    )


def test_overreach_uri():
    assert str(overreach_uri(40)).endswith(
        "/overreach/40"
    )


def test_justification_uri():
    assert str(justification_uri(41)).endswith(
        "/justification/41"
    )


def test_risk_uri():
    assert str(risk_uri(42)).endswith(
        "/risk/42"
    )


def test_empty_entity_type_rejected():
    try:
        build_resource_uri("", 1)
        assert False
    except ValueError:
        assert True


def test_empty_entity_id_rejected():
    try:
        build_resource_uri("application", "")
        assert False
    except ValueError:
        assert True