"""
FDO Ontology - Constraint Definitions

Defines structural constraints for the FDO ontology.

These constraints describe cardinality and required-property rules.
They will later be translated into OWL restrictions / SHACL constraints.
"""

from dataclasses import dataclass
from typing import Optional, Type


@dataclass(frozen=True)
class CardinalityConstraint:
    """
    Defines a minimum/maximum cardinality restriction.
    """

    property_name: str
    domain: Type
    min_count: int = 0
    max_count: Optional[int] = None
    description: str = ""


@dataclass(frozen=True)
class RequiredPropertyConstraint:
    """
    Defines a property that must be present on an entity.
    """

    property_name: str
    domain: Type
    description: str = ""


from .classes import (
    Application,
    DeclaredData,
    ExpectedData,
    Function,
    Overreach,
    PersonalData,
    PolicyClause,
    PrivacyPolicy,
)


FDO_CARDINALITY_CONSTRAINTS = [

    CardinalityConstraint(
        property_name="performsFunction",
        domain=Application,
        min_count=1,
        description="Every application should perform at least one function.",
    ),

    CardinalityConstraint(
        property_name="requiresData",
        domain=Function,
        min_count=0,
        description="A function may require zero or more data types.",
    ),

    CardinalityConstraint(
        property_name="collectsData",
        domain=Application,
        min_count=0,
        description="An application may collect zero or more data types.",
    ),

    CardinalityConstraint(
        property_name="declaredData",
        domain=Application,
        min_count=0,
        description="An application may have zero or more declared data records.",
    ),

    CardinalityConstraint(
        property_name="expectedData",
        domain=Function,
        min_count=0,
        description="A function may have zero or more expected data mappings.",
    ),

    CardinalityConstraint(
        property_name="usedForPurpose",
        domain=PersonalData,
        min_count=0,
        description="Personal data may have zero or more purposes.",
    ),

    CardinalityConstraint(
        property_name="processedBy",
        domain=PersonalData,
        min_count=0,
        description="Personal data may be associated with zero or more processing activities.",
    ),

    CardinalityConstraint(
        property_name="sharedWith",
        domain=PersonalData,
        min_count=0,
        description="Personal data may be shared with zero or more recipients.",
    ),

    CardinalityConstraint(
        property_name="hasRetentionPolicy",
        domain=PersonalData,
        min_count=0,
        max_count=1,
        description="Personal data may have at most one primary retention policy.",
    ),

    CardinalityConstraint(
        property_name="supportedByClause",
        domain=DeclaredData,
        min_count=0,
        description="Declared data may be supported by zero or more policy clauses.",
    ),

    CardinalityConstraint(
        property_name="hasJustification",
        domain=Overreach,
        min_count=0,
        max_count=1,
        description="An overreach finding may have at most one primary justification.",
    ),

    CardinalityConstraint(
        property_name="concernsData",
        domain=Overreach,
        min_count=1,
        max_count=1,
        description="An overreach finding concerns exactly one primary data type.",
    ),

    CardinalityConstraint(
        property_name="concernsFunction",
        domain=Overreach,
        min_count=0,
        max_count=1,
        description="An overreach finding may concern one primary function.",
    ),

    CardinalityConstraint(
        property_name="hasRisk",
        domain=Overreach,
        min_count=0,
        max_count=1,
        description="An overreach finding may have one primary risk assessment.",
    ),
]


FDO_REQUIRED_PROPERTY_CONSTRAINTS = [

    RequiredPropertyConstraint(
        property_name="name",
        domain=Application,
        description="Every application must have a name.",
    ),

    RequiredPropertyConstraint(
        property_name="name",
        domain=Function,
        description="Every function must have a name.",
    ),

    RequiredPropertyConstraint(
        property_name="name",
        domain=PersonalData,
        description="Every personal data concept must have a name.",
    ),

    RequiredPropertyConstraint(
        property_name="dataType",
        domain=ExpectedData,
        description="Every expected data record must identify its data type.",
    ),

    RequiredPropertyConstraint(
        property_name="dataType",
        domain=DeclaredData,
        description="Every declared data record must identify its data type.",
    ),

    RequiredPropertyConstraint(
        property_name="text",
        domain=PolicyClause,
        description="Every policy clause must contain policy text.",
    ),

    RequiredPropertyConstraint(
        property_name="source",
        domain=PrivacyPolicy,
        description="Every privacy policy should identify its source.",
    ),

    RequiredPropertyConstraint(
        property_name="reason",
        domain=Overreach,
        description="Every overreach finding must contain an explanation reason.",
    ),
]