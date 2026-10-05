"""
Stable URI strategy for FDO RDF individuals.

Ontology vocabulary:
    http://example.org/fdo#

Individual resources:
    http://example.org/fdo/resource/<type>/<id>

Keeping the URI generation centralized ensures that the same
database entity always maps to the same RDF resource.
"""

from rdflib import URIRef

from .namespace import FDO_NAMESPACE_URI


RESOURCE_BASE_URI = f"{FDO_NAMESPACE_URI}resource/"


def build_resource_uri(entity_type: str, entity_id) -> URIRef:
    """
    Build a stable URI for an FDO individual.

    Example:
        build_resource_uri("application", 1)

    Returns:
        http://example.org/fdo#resource/application/1
    """

    normalized_type = str(entity_type).strip().lower()
    normalized_id = str(entity_id).strip()

    if not normalized_type:
        raise ValueError("entity_type cannot be empty")

    if not normalized_id:
        raise ValueError("entity_id cannot be empty")

    return URIRef(
        f"{RESOURCE_BASE_URI}{normalized_type}/{normalized_id}"
    )


def application_uri(application_id) -> URIRef:
    return build_resource_uri("application", application_id)


def function_uri(function_id) -> URIRef:
    return build_resource_uri("function", function_id)


def expected_data_uri(expected_id) -> URIRef:
    return build_resource_uri("expected-data", expected_id)


def declared_data_uri(declared_id) -> URIRef:
    return build_resource_uri("declared-data", declared_id)


def policy_uri(policy_id) -> URIRef:
    return build_resource_uri("policy", policy_id)


def policy_clause_uri(clause_id) -> URIRef:
    return build_resource_uri("policy-clause", clause_id)


def personal_data_uri(data_id) -> URIRef:
    return build_resource_uri("personal-data", data_id)


def purpose_uri(purpose_id) -> URIRef:
    return build_resource_uri("purpose", purpose_id)


def recipient_uri(recipient_id) -> URIRef:
    return build_resource_uri("recipient", recipient_id)


def retention_policy_uri(retention_id) -> URIRef:
    return build_resource_uri("retention-policy", retention_id)


def overreach_uri(overreach_id) -> URIRef:
    return build_resource_uri("overreach", overreach_id)


def justification_uri(justification_id) -> URIRef:
    return build_resource_uri("justification", justification_id)


def risk_uri(risk_id) -> URIRef:
    return build_resource_uri("risk", risk_id)
def processing_activity_uri(processing_activity_id):
    return build_resource_uri(
        "processing-activity",
        processing_activity_id,
    )