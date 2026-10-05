"""
FDO Ontology - Data Property Definitions

Defines literal-valued properties of FDO ontology entities.

Object properties connect ontology entities to other entities.
Data properties connect ontology entities to literal values such as
strings, booleans, integers, and floating-point numbers.
"""

from dataclasses import dataclass
from typing import Type


@dataclass(frozen=True)
class DataProperty:
    """
    Represents a semantic data property.

    Example:
        Application --name--> "Google Maps"
    """

    name: str
    domain: Type
    datatype: str
    description: str


from .classes import (
    Application,
    Consent,
    DeclaredData,
    ExpectedData,
    Function,
    FDOEntity,
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


FDO_DATA_PROPERTIES = {

    "id": DataProperty(
        name="id",
        domain=FDOEntity,
        datatype="string",
        description="Unique identifier of an ontology entity.",
    ),

    "name": DataProperty(
        name="name",
        domain=Application,
        datatype="string",
        description="Human-readable name of an ontology entity.",
    ),

    "description": DataProperty(
        name="description",
        domain=FDOEntity,
        datatype="string",
        description="Human-readable description of an ontology entity.",
    ),

    "category": DataProperty(
        name="category",
        domain=Application,
        datatype="string",
        description="Category of an application.",
    ),

    "sensitive": DataProperty(
        name="sensitive",
        domain=PersonalData,
        datatype="boolean",
        description="Indicates whether a data type is sensitive.",
    ),

    "sensitivityCategory": DataProperty(
        name="sensitivityCategory",
        domain=PersonalData,
        datatype="string",
        description="Category describing the sensitivity of personal data.",
    ),

    "duration": DataProperty(
        name="duration",
        domain=RetentionPolicy,
        datatype="string",
        description="Retention duration associated with personal data.",
    ),

    "recipientType": DataProperty(
        name="recipientType",
        domain=Recipient,
        datatype="string",
        description="Type of recipient receiving personal data.",
    ),

    "status": DataProperty(
        name="status",
        domain=Consent,
        datatype="string",
        description="Status of consent or an FDO finding.",
    ),

    "source": DataProperty(
        name="source",
        domain=PrivacyPolicy,
        datatype="string",
        description="Source document or source location.",
    ),

    "version": DataProperty(
        name="version",
        domain=PrivacyPolicy,
        datatype="string",
        description="Version of the privacy policy.",
    ),

    "text": DataProperty(
        name="text",
        domain=PolicyClause,
        datatype="string",
        description="Text of a policy clause or justification.",
    ),

    "section": DataProperty(
        name="section",
        domain=PolicyClause,
        datatype="string",
        description="Policy section containing the clause.",
    ),

    "dataType": DataProperty(
        name="dataType",
        domain=ExpectedData,
        datatype="string",
        description="Type of personal data.",
    ),

    "necessity": DataProperty(
        name="necessity",
        domain=ExpectedData,
        datatype="string",
        description="Necessity level of expected data.",
    ),

    "purpose": DataProperty(
        name="purpose",
        domain=ExpectedData,
        datatype="string",
        description="Purpose associated with expected data.",
    ),

    "sharing": DataProperty(
        name="sharing",
        domain=DeclaredData,
        datatype="string",
        description="Sharing information associated with declared data.",
    ),

    "retention": DataProperty(
        name="retention",
        domain=DeclaredData,
        datatype="string",
        description="Retention information associated with declared data.",
    ),

    "justificationType": DataProperty(
        name="justificationType",
        domain=Justification,
        datatype="string",
        description="Type of justification supporting an FDO finding.",
    ),

    "reason": DataProperty(
        name="reason",
        domain=Overreach,
        datatype="string",
        description="Reason explaining an FDO finding.",
    ),

    "confidence": DataProperty(
        name="confidence",
        domain=Overreach,
        datatype="float",
        description="Confidence associated with an FDO finding.",
    ),

    "level": DataProperty(
        name="level",
        domain=Risk,
        datatype="string",
        description="Risk level associated with an FDO finding.",
    ),

    "score": DataProperty(
        name="score",
        domain=Risk,
        datatype="float",
        description="Numerical risk score.",
    ),
}