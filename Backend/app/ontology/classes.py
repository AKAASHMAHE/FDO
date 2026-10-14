"""
FDO Ontology - Core Class Definitions

This module defines the conceptual classes of the Functional Data
Ontology (FDO) in Python.

Important:
    This is the semantic/domain model only.
    RDF/OWL serialization will be implemented in a later stage.

The classes are based on the FDO project specification:
    Application
    Function
    PersonalData
    SensitiveData
    ProcessingActivity
    Purpose
    Recipient
    RetentionPolicy
    User
    UserRight
    Consent
    PrivacyPolicy
    PolicyClause
    ExpectedData
    DeclaredData
    Overreach
    Justification
    Risk
"""

from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Base Entity
# ---------------------------------------------------------------------------

@dataclass
class FDOEntity:
    """
    Base class for all FDO semantic entities.

    Every semantic entity has:
        id   -> unique identifier
        name -> human-readable name
    """

    id: str
    name: str


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

@dataclass
class Application(FDOEntity):
    """
    Represents an application being analyzed.

    Examples:
        Navigation App
        Banking App
        Messaging App
        Flashlight App
    """

    category: Optional[str] = None
    description: Optional[str] = None


# ---------------------------------------------------------------------------
# Function
# ---------------------------------------------------------------------------

@dataclass
class Function(FDOEntity):
    """
    Represents a function performed by an application.

    Examples:
        Navigation
        Route Planning
        Messaging
        Payment Processing
    """

    description: Optional[str] = None


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

@dataclass
class PersonalData(FDOEntity):
    """
    Represents a type of personal data.

    Examples:
        Location
        Email
        Phone Number
        Contacts
        Device ID
        IP Address
    """

    sensitive: bool = False


@dataclass
class SensitiveData(PersonalData):
    """
    Represents a sensitive category of personal data.

    SensitiveData is a specialization of PersonalData.
    """

    sensitivity_category: Optional[str] = None


# ---------------------------------------------------------------------------
# Processing Activity
# ---------------------------------------------------------------------------

@dataclass
class ProcessingActivity(FDOEntity):
    """
    Represents an operation performed on data.

    Examples:
        Collect
        Store
        Use
        Share
        Disclose
        Retain
        Delete
    """

    description: Optional[str] = None


# ---------------------------------------------------------------------------
# Purpose
# ---------------------------------------------------------------------------

@dataclass
class Purpose(FDOEntity):
    """
    Represents why personal data is processed.

    Examples:
        Navigation
        Service Delivery
        Analytics
        Personalization
        Advertising
        Security
        Fraud Prevention
    """

    description: Optional[str] = None


# ---------------------------------------------------------------------------
# Recipient
# ---------------------------------------------------------------------------

@dataclass
class Recipient(FDOEntity):
    """
    Represents an entity with which data may be shared.

    Examples:
        Service Provider
        Advertising Partner
        Analytics Provider
        Business Partner
        Government Authority
    """

    recipient_type: Optional[str] = None


# ---------------------------------------------------------------------------
# Retention Policy
# ---------------------------------------------------------------------------

@dataclass
class RetentionPolicy(FDOEntity):
    """
    Represents how long or under what rule data is retained.

    Examples:
        30 days
        Until account deletion
        As long as necessary
    """

    duration: Optional[str] = None
    description: Optional[str] = None


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

@dataclass
class User(FDOEntity):
    """
    Represents a user involved in the privacy model.

    The ontology can later connect users with:
        consent
        rights
        personal data
    """

    description: Optional[str] = None


# ---------------------------------------------------------------------------
# User Right
# ---------------------------------------------------------------------------

@dataclass
class UserRight(FDOEntity):
    """
    Represents a privacy-related right available to the user.

    Examples:
        Access
        Correction
        Deletion
        Portability
        Withdrawal of Consent
    """

    description: Optional[str] = None


# ---------------------------------------------------------------------------
# Consent
# ---------------------------------------------------------------------------

@dataclass
class Consent(FDOEntity):
    """
    Represents a user's consent related to data processing.
    """

    status: Optional[str] = None
    description: Optional[str] = None


# ---------------------------------------------------------------------------
# Privacy Policy
# ---------------------------------------------------------------------------

@dataclass
class PrivacyPolicy(FDOEntity):
    """
    Represents a privacy policy associated with an application.
    """

    source: Optional[str] = None
    version: Optional[str] = None


# ---------------------------------------------------------------------------
# Policy Clause
# ---------------------------------------------------------------------------

@dataclass
class PolicyClause(FDOEntity):
    """
    Represents an individual policy statement or evidence clause.

    The clause is important for explainability because semantic
    conclusions should remain traceable to policy evidence.
    """

    text: str = ""
    source: Optional[str] = None
    section: Optional[str] = None


# ---------------------------------------------------------------------------
# Expected Data
# ---------------------------------------------------------------------------

@dataclass
class ExpectedData(FDOEntity):
    """
    Represents data reasonably expected or required by an
    application's identified functionality.

    Example:

        Navigation -> requiresData -> Location
    """

    data_type: str = ""
    necessity: Optional[str] = None
    purpose: Optional[str] = None


# ---------------------------------------------------------------------------
# Declared Data
# ---------------------------------------------------------------------------

@dataclass
class DeclaredData(FDOEntity):
    """
    Represents data declared in a privacy policy.

    Example:

        NavigationApp -> collectsData -> Contacts
    """

    data_type: str = ""
    purpose: Optional[str] = None
    sharing: Optional[str] = None
    retention: Optional[str] = None
    extraction_status: Optional[str] = None
    confidence: Optional[float] = None
    evidence_text: Optional[str] = None
    entity: Optional[str] = None


# ---------------------------------------------------------------------------
# Justification
# ---------------------------------------------------------------------------

@dataclass
class Justification(FDOEntity):
    """
    Represents the stated reason or explanation for data processing.

    An unexpected data type is not automatically considered
    functional overreach. The policy justification must also
    be examined.
    """

    text: str = ""
    justification_type: Optional[str] = None


# ---------------------------------------------------------------------------
# Overreach
# ---------------------------------------------------------------------------

@dataclass
class Overreach(FDOEntity):
    """
    Represents a Functional Data Overreach finding/candidate.

    The finding should retain enough information to explain:
        - what data was involved
        - why it was unexpected
        - what policy evidence supports it
        - whether justification exists
    """

    status: Optional[str] = None
    reason: Optional[str] = None
    confidence: Optional[float] = None


# ---------------------------------------------------------------------------
# Risk
# ---------------------------------------------------------------------------

@dataclass
class Risk(FDOEntity):
    """
    Represents an analytical privacy-risk indicator.

    Risk is a downstream analytical concept and is not itself
    the fundamental definition of FDO.
    """

    level: Optional[str] = None
    score: Optional[float] = None
    reason: Optional[str] = None