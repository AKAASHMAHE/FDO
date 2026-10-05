"""
FDO Ontology - Object Property Definitions

Defines semantic relationships between FDO ontology classes.

These relationships will later be serialized into OWL/RDF and used
by the knowledge graph, SPARQL queries, and reasoning layer.
"""

from dataclasses import dataclass
from typing import Type


@dataclass(frozen=True)
class ObjectProperty:
    """
    Represents an FDO semantic relationship.

    Example:
        Application --performsFunction--> Function
    """

    name: str
    domain: Type
    range: Type
    description: str


# Import ontology classes
from .classes import (
    Application,
    Consent,
    DeclaredData,
    ExpectedData,
    Function,
    Justification,
    Overreach,
    PersonalData,
    PolicyClause,
    PrivacyPolicy,
    ProcessingActivity,
    Purpose,
    Recipient,
    RetentionPolicy,
    Risk,
    User,
    UserRight,
)


FDO_OBJECT_PROPERTIES = {
    "performsFunction": ObjectProperty(
        name="performsFunction",
        domain=Application,
        range=Function,
        description="Connects an application to a function it performs.",
    ),

    "requiresData": ObjectProperty(
        name="requiresData",
        domain=Function,
        range=PersonalData,
        description="Connects a function to data reasonably required for that function.",
    ),

    "collectsData": ObjectProperty(
        name="collectsData",
        domain=Application,
        range=PersonalData,
        description="Connects an application to personal data it collects.",
    ),

    "declaredData": ObjectProperty(
        name="declaredData",
        domain=Application,
        range=DeclaredData,
        description="Connects an application to data declared in its privacy policy.",
    ),

    "expectedData": ObjectProperty(
        name="expectedData",
        domain=Function,
        range=ExpectedData,
        description="Connects a function to expected data requirements.",
    ),

    "expectedForFunction": ObjectProperty(
        name="expectedForFunction",
        domain=ExpectedData,
        range=Function,
        description="Connects expected data to the function for which it is expected.",
    ),

    "declaredByApplication": ObjectProperty(
        name="declaredByApplication",
        domain=DeclaredData,
        range=Application,
        description="Connects declared data to the application declaring it.",
    ),

    "usedForPurpose": ObjectProperty(
        name="usedForPurpose",
        domain=PersonalData,
        range=Purpose,
        description="Connects personal data to its stated processing purpose.",
    ),

    "processedBy": ObjectProperty(
        name="processedBy",
        domain=PersonalData,
        range=ProcessingActivity,
        description="Connects personal data to the processing activity applied to it.",
    ),

    "sharedWith": ObjectProperty(
        name="sharedWith",
        domain=PersonalData,
        range=Recipient,
        description="Connects personal data to recipients with whom it is shared.",
    ),

    "hasRetentionPolicy": ObjectProperty(
        name="hasRetentionPolicy",
        domain=PersonalData,
        range=RetentionPolicy,
        description="Connects personal data to its retention policy.",
    ),

    "supportedByClause": ObjectProperty(
        name="supportedByClause",
        domain=DeclaredData,
        range=PolicyClause,
        description="Connects a declared data fact to policy evidence supporting it.",
    ),

    "supportedByPolicy": ObjectProperty(
        name="supportedByPolicy",
        domain=PolicyClause,
        range=PrivacyPolicy,
        description="Connects a policy clause to its source privacy policy.",
    ),

    "hasUserRight": ObjectProperty(
        name="hasUserRight",
        domain=PrivacyPolicy,
        range=UserRight,
        description="Connects a privacy policy to user rights it provides.",
    ),

    "hasConsent": ObjectProperty(
        name="hasConsent",
        domain=Application,
        range=Consent,
        description="Connects an application to a consent record.",
    ),

    "hasJustification": ObjectProperty(
        name="hasJustification",
        domain=Overreach,
        range=Justification,
        description="Connects an overreach finding to its justification.",
    ),

    "concernsData": ObjectProperty(
        name="concernsData",
        domain=Overreach,
        range=PersonalData,
        description="Connects an overreach finding to the data involved.",
    ),

    "concernsFunction": ObjectProperty(
        name="concernsFunction",
        domain=Overreach,
        range=Function,
        description="Connects an overreach finding to the affected function.",
    ),

    "hasRisk": ObjectProperty(
        name="hasRisk",
        domain=Overreach,
        range=Risk,
        description="Connects an overreach finding to an associated privacy risk.",
    ),

    "hasUser": ObjectProperty(
        name="hasUser",
        domain=Application,
        range=User,
        description="Connects an application to its user context.",
    ),
    "expectedDataType": ObjectProperty(
    name="expectedDataType",
    domain=ExpectedData,
    range=PersonalData,
    description="Connects expected data to the semantic personal data concept it represents.",
),

"declaredDataType": ObjectProperty(
    name="declaredDataType",
    domain=DeclaredData,
    range=PersonalData,
    description="Connects declared data to the semantic personal data concept it represents.",
),
"expectedDataPurpose": ObjectProperty(
    name="expectedDataPurpose",
    domain=ExpectedData,
    range=Purpose,
    description="Connects expected data to its semantic processing purpose.",
),

"declaredDataPurpose": ObjectProperty(
    name="declaredDataPurpose",
    domain=DeclaredData,
    range=Purpose,
    description="Connects declared data to its semantic processing purpose.",
),
}