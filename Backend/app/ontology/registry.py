"""
FDO Ontology Class Registry.

Provides a single registry of the semantic classes defined by FDO.
This registry will later be reused by the RDF/OWL serialization layer.
"""

from .classes import (
    Application,
    Consent,
    DeclaredData,
    ExpectedData,
    FDOEntity,
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
    SensitiveData,
    User,
    UserRight,
)


FDO_CLASSES = {
    "FDOEntity": FDOEntity,
    "Application": Application,
    "Function": Function,
    "PersonalData": PersonalData,
    "SensitiveData": SensitiveData,
    "ProcessingActivity": ProcessingActivity,
    "Purpose": Purpose,
    "Recipient": Recipient,
    "RetentionPolicy": RetentionPolicy,
    "User": User,
    "UserRight": UserRight,
    "Consent": Consent,
    "PrivacyPolicy": PrivacyPolicy,
    "PolicyClause": PolicyClause,
    "ExpectedData": ExpectedData,
    "DeclaredData": DeclaredData,
    "Justification": Justification,
    "Overreach": Overreach,
    "Risk": Risk,
}