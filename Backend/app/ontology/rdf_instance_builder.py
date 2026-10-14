"""
FDO RDF Instance Builder.

Converts FDO semantic/domain objects into RDF individuals.

Architecture:

    Database
        ↓
    DB Mapper
        ↓
    FDO Domain Objects
        ↓
    RDF Instance Builder
        ↓
    RDF Graph
"""

from typing import Iterable

from rdflib import Graph, Literal, RDF, RDFS, OWL, XSD

from .classes import (
    Application,
    Function,
    PersonalData,
    SensitiveData,
    Purpose,
    Recipient,
    RetentionPolicy,
    PrivacyPolicy,
    PolicyClause,
    ExpectedData,
    DeclaredData,
    Justification,
    Overreach,
    Risk,
    User,
    UserRight
)

from .namespace import FDO

from .uri import (
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
    expected_data_uri,
    declared_data_uri,
    personal_data_uri,
    processing_activity_uri,
)

from .db_rdf_mapper import (
    application_from_record,
    function_from_record,
    expected_data_from_record,
    declared_data_from_record,
)
from app.services.data_type_hierarchy import (
    canonical_data_type_code,
    hierarchy_edges,
)
from app.services.ancillary_baseline import is_ancillary_declaration
# ============================================================
# Helper
# ============================================================

def _add_literal(graph, subject, predicate, value, datatype=None):
    """
    Add a literal triple only when value is not None.
    """

    if value is None:
        return

    if datatype is not None:
        graph.add(
            (
                subject,
                predicate,
                Literal(value, datatype=datatype),
            )
        )
    else:
        graph.add(
            (
                subject,
                predicate,
                Literal(value),
            )
        )


def data_type_class_uri(data_type: str):
    canonical = canonical_data_type_code(data_type)
    return FDO[f"DataType_{canonical.replace('.', '_')}"]


def _taxonomy_class_uri(code: str):
    if code == "PersonalData":
        return FDO.PersonalData
    if code == "DataType":
        return FDO.DataType
    return FDO[f"DataType_{code.replace('.', '_')}"]


def add_data_type_taxonomy(graph: Graph) -> None:
    for child, parent in hierarchy_edges():
        child_uri = _taxonomy_class_uri(child)
        parent_uri = _taxonomy_class_uri(parent)
        graph.add((child_uri, RDF.type, OWL.Class))
        graph.add((parent_uri, RDF.type, OWL.Class))
        graph.add((child_uri, RDFS.subClassOf, parent_uri))
    graph.add((FDO.DataType, RDF.type, OWL.Class))
    graph.add((FDO.AncillaryData, RDF.type, OWL.Class))


# ============================================================
# Entity Builders
# ============================================================

def add_application(graph: Graph, application: Application):
    """
    Add an Application individual to the RDF graph.
    """

    subject = application_uri(application.id)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.Application,
        )
    )

    _add_literal(graph, subject, FDO.id, application.id)
    _add_literal(graph, subject, FDO.name, application.name)
    _add_literal(graph, subject, FDO.category, application.category)
    _add_literal(graph, subject, FDO.description, application.description)

    return subject


def add_function(graph: Graph, function: Function):
    """
    Add a Function individual to the RDF graph.
    """

    subject = function_uri(function.id)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.Function,
        )
    )

    _add_literal(graph, subject, FDO.id, function.id)
    _add_literal(graph, subject, FDO.name, function.name)
    _add_literal(graph, subject, FDO.description, function.description)

    return subject


def add_personal_data(
    graph: Graph,
    data: PersonalData,
    data_id=None,
):
    """
    Add a PersonalData or SensitiveData individual.
    """

    identifier = data_id or data.id

    subject = personal_data_uri(identifier)

    if isinstance(data, SensitiveData):
        graph.add(
            (
                subject,
                RDF.type,
                FDO.SensitiveData,
            )
        )
    else:
        graph.add(
            (
                subject,
                RDF.type,
                FDO.PersonalData,
            )
        )

    _add_literal(graph, subject, FDO.id, data.id)
    _add_literal(graph, subject, FDO.name, data.name)

    graph.add(
        (
            subject,
            FDO.sensitive,
            Literal(
                data.sensitive,
                datatype=XSD.boolean,
            ),
        )
    )

    if isinstance(data, SensitiveData):
        _add_literal(
            graph,
            subject,
            FDO.sensitivityCategory,
            data.sensitivity_category,
        )

    return subject


def add_expected_data(graph: Graph, expected: ExpectedData):
    """
    Add an ExpectedData individual.
    """

    subject = expected_data_uri(expected.id)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.ExpectedData,
        )
    )

    _add_literal(graph, subject, FDO.id, expected.id)
    _add_literal(graph, subject, FDO.name, expected.name)
    _add_literal(graph, subject, FDO.dataType, expected.data_type)
    if expected.data_type:
        graph.add(
            (
                subject,
                FDO.dataTypeClass,
                data_type_class_uri(expected.data_type),
            )
        )
    _add_literal(graph, subject, FDO.necessity, expected.necessity)
    _add_literal(graph, subject, FDO.purpose, expected.purpose)

    return subject


def add_declared_data(graph: Graph, declared: DeclaredData):
    """
    Add a DeclaredData individual.
    """

    subject = declared_data_uri(declared.id)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.DeclaredData,
        )
    )

    _add_literal(graph, subject, FDO.id, declared.id)
    _add_literal(graph, subject, FDO.name, declared.name)
    _add_literal(graph, subject, FDO.dataType, declared.data_type)
    if declared.data_type:
        graph.add(
            (
                subject,
                FDO.dataTypeClass,
                data_type_class_uri(declared.data_type),
            )
        )
    _add_literal(graph, subject, FDO.purpose, declared.purpose)
    _add_literal(graph, subject, FDO.sharing, declared.sharing)
    _add_literal(graph, subject, FDO.retention, declared.retention)
    _add_literal(graph, subject, FDO.extractionStatus, declared.extraction_status)
    _add_literal(graph, subject, FDO.confidence, declared.confidence, XSD.float)
    _add_literal(graph, subject, FDO.text, declared.evidence_text)
    _add_literal(graph, subject, FDO.entity, declared.entity)

    if is_ancillary_declaration(
        declared.data_type,
        declared.purpose,
    ):
        graph.add((subject, RDF.type, FDO.AncillaryData))

    return subject


def add_privacy_policy(graph: Graph, policy: PrivacyPolicy):
    """
    Add a PrivacyPolicy individual.
    """

    subject = policy_uri(policy.id)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.PrivacyPolicy,
        )
    )

    _add_literal(graph, subject, FDO.id, policy.id)
    _add_literal(graph, subject, FDO.name, policy.name)
    _add_literal(graph, subject, FDO.source, policy.source)
    _add_literal(graph, subject, FDO.version, policy.version)

    return subject


def add_policy_clause(graph: Graph, clause: PolicyClause):
    """
    Add a PolicyClause individual.
    """

    subject = policy_clause_uri(clause.id)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.PolicyClause,
        )
    )

    _add_literal(graph, subject, FDO.id, clause.id)
    _add_literal(graph, subject, FDO.name, clause.name)
    _add_literal(graph, subject, FDO.text, clause.text)
    _add_literal(graph, subject, FDO.source, clause.source)
    _add_literal(graph, subject, FDO.section, clause.section)

    return subject


def add_overreach(graph: Graph, overreach: Overreach):
    """
    Add an Overreach/FDO finding individual.
    """

    subject = overreach_uri(overreach.id)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.Overreach,
        )
    )

    _add_literal(graph, subject, FDO.id, overreach.id)
    _add_literal(graph, subject, FDO.name, overreach.name)
    _add_literal(graph, subject, FDO.status, overreach.status)
    _add_literal(graph, subject, FDO.reason, overreach.reason)

    if overreach.confidence is not None:
        _add_literal(
            graph,
            subject,
            FDO.confidence,
            overreach.confidence,
            XSD.float,
        )

    return subject


def add_purpose(
    graph: Graph,
    purpose: Purpose,
    purpose_id=None,
):
    """
    Add a Purpose individual.
    """

    identifier = purpose_id or purpose.id

    subject = purpose_uri(identifier)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.Purpose,
        )
    )

    _add_literal(graph, subject, FDO.id, purpose.id)
    _add_literal(graph, subject, FDO.name, purpose.name)
    _add_literal(graph, subject, FDO.description, purpose.description)

    return subject


def add_recipient(graph: Graph, recipient: Recipient):
    """
    Add a Recipient individual.
    """

    subject = recipient_uri(recipient.id)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.Recipient,
        )
    )

    _add_literal(graph, subject, FDO.id, recipient.id)
    _add_literal(graph, subject, FDO.name, recipient.name)
    _add_literal(
        graph,
        subject,
        FDO.recipientType,
        recipient.recipient_type,
    )

    return subject


def add_retention_policy(
    graph: Graph,
    retention: RetentionPolicy,
):
    """
    Add a RetentionPolicy individual.
    """

    subject = retention_policy_uri(retention.id)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.RetentionPolicy,
        )
    )

    _add_literal(graph, subject, FDO.id, retention.id)
    _add_literal(graph, subject, FDO.name, retention.name)
    _add_literal(graph, subject, FDO.duration, retention.duration)
    _add_literal(
        graph,
        subject,
        FDO.description,
        retention.description,
    )

    return subject


def add_justification(
    graph: Graph,
    justification: Justification,
):
    """
    Add a Justification individual.
    """

    subject = justification_uri(justification.id)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.Justification,
        )
    )

    _add_literal(graph, subject, FDO.id, justification.id)
    _add_literal(graph, subject, FDO.name, justification.name)
    _add_literal(graph, subject, FDO.text, justification.text)
    _add_literal(
        graph,
        subject,
        FDO.justificationType,
        justification.justification_type,
    )

    return subject


def add_risk(graph: Graph, risk: Risk):
    """
    Add a Risk individual.
    """

    subject = risk_uri(risk.id)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.Risk,
        )
    )

    _add_literal(graph, subject, FDO.id, risk.id)
    _add_literal(graph, subject, FDO.name, risk.name)
    _add_literal(graph, subject, FDO.level, risk.level)

    if risk.score is not None:
        _add_literal(
            graph,
            subject,
            FDO.score,
            risk.score,
            XSD.float,
        )

    _add_literal(graph, subject, FDO.reason, risk.reason)

    return subject


# ============================================================
# Relationships
# ============================================================

def connect_application_function(
    graph: Graph,
    application_id,
    function_id,
):
    """
    Application performs Function.
    """

    graph.add(
        (
            application_uri(application_id),
            FDO.performsFunction,
            function_uri(function_id),
        )
    )


def connect_function_expected_data(
    graph: Graph,
    function_id,
    expected_id,
):
    """
    Function has expected data.
    """

    graph.add(
        (
            function_uri(function_id),
            FDO.expectedData,
            expected_data_uri(expected_id),
        )
    )

    graph.add(
        (
            expected_data_uri(expected_id),
            FDO.expectedForFunction,
            function_uri(function_id),
        )
    )


def connect_application_declared_data(
    graph: Graph,
    application_id,
    declared_id,
):
    """
    Application has declared data.
    """

    graph.add(
        (
            application_uri(application_id),
            FDO.declaredData,
            declared_data_uri(declared_id),
        )
    )

    graph.add(
        (
            declared_data_uri(declared_id),
            FDO.declaredByApplication,
            application_uri(application_id),
        )
    )


def connect_declared_data_policy_clause(
    graph: Graph,
    declared_id,
    clause_id,
):
    """
    Connect declared data to supporting policy evidence.
    """

    graph.add(
        (
            declared_data_uri(declared_id),
            FDO.supportedByClause,
            policy_clause_uri(clause_id),
        )
    )


def connect_policy_clause_policy(
    graph: Graph,
    clause_id,
    policy_id,
):
    """
    Connect policy clause to its source policy.
    """

    graph.add(
        (
            policy_clause_uri(clause_id),
            FDO.supportedByPolicy,
            policy_uri(policy_id),
        )
    )


def connect_data_purpose(
    graph: Graph,
    data_id,
    purpose_id,
):
    """
    Connect personal data to its purpose.
    """

    graph.add(
        (
            personal_data_uri(data_id),
            FDO.usedForPurpose,
            purpose_uri(purpose_id),
        )
    )


def connect_data_recipient(
    graph: Graph,
    data_id,
    recipient_id,
):
    """
    Connect personal data to a recipient.
    """

    graph.add(
        (
            personal_data_uri(data_id),
            FDO.sharedWith,
            recipient_uri(recipient_id),
        )
    )


def connect_data_retention(
    graph: Graph,
    data_id,
    retention_id,
):
    """
    Connect personal data to its retention policy.
    """

    graph.add(
        (
            personal_data_uri(data_id),
            FDO.hasRetentionPolicy,
            retention_policy_uri(retention_id),
        )
    )


def connect_overreach_data(
    graph: Graph,
    overreach_id,
    data_id,
):
    """
    Connect FDO finding to affected data.
    """

    graph.add(
        (
            overreach_uri(overreach_id),
            FDO.concernsData,
            personal_data_uri(data_id),
        )
    )


def connect_overreach_function(
    graph: Graph,
    overreach_id,
    function_id,
):
    """
    Connect FDO finding to affected function.
    """

    graph.add(
        (
            overreach_uri(overreach_id),
            FDO.concernsFunction,
            function_uri(function_id),
        )
    )


def connect_overreach_justification(
    graph: Graph,
    overreach_id,
    justification_id,
):
    """
    Connect FDO finding to its justification.
    """

    graph.add(
        (
            overreach_uri(overreach_id),
            FDO.hasJustification,
            justification_uri(justification_id),
        )
    )


def connect_overreach_risk(
    graph: Graph,
    overreach_id,
    risk_id,
):
    """
    Connect FDO finding to its risk assessment.
    """

    graph.add(
        (
            overreach_uri(overreach_id),
            FDO.hasRisk,
            risk_uri(risk_id),
        )
    )
def _convert_application_record(record):
    if not isinstance(record, dict):
        return record

    if "application_id" in record:
        return application_from_record(record)

    return Application(
        id=str(record.get("id", "")),
        name=str(record.get("name", "")),
        category=record.get("category"),
        description=record.get("description"),
    )


def _convert_function_record(record):
    if not isinstance(record, dict):
        return record

    if "function_record_id" in record:
        return function_from_record(record)

    return Function(
        id=str(record.get("id", "")),
        name=str(record.get("name", "")),
        description=record.get("description"),
    )


def _convert_expected_data_record(record):
    if not isinstance(record, dict):
        return record

    if "expected_id" in record:
        return expected_data_from_record(record)

    return ExpectedData(
        id=str(record.get("id", "")),
        name=str(record.get("name", "")),
        data_type=record.get("data_type"),
        necessity=record.get("necessity"),
        purpose=record.get("purpose"),
    )


def _convert_declared_data_record(record):
    if not isinstance(record, dict):
        return record

    if "evidence_id" in record:
        return declared_data_from_record(record)

    return DeclaredData(
        id=str(record.get("id", "")),
        name=str(record.get("name", "")),
        data_type=record.get("data_type"),
        purpose=record.get("purpose"),
        sharing=record.get("sharing"),
        retention=record.get("retention"),
    )

# ============================================================
# Graph Builder
# ============================================================

def build_rdf_graph(
    applications: Iterable[Application] = (),
    functions: Iterable[Function] = (),
    expected_data: Iterable[ExpectedData] = (),
    declared_data: Iterable[DeclaredData] = (),
    policies: Iterable[PrivacyPolicy] = (),
    policy_clauses: Iterable[PolicyClause] = (),
    overreach_findings: Iterable[Overreach] = (),
    personal_data=None,
) -> Graph:
    """
    Build an RDF graph from FDO domain objects.

    Supports both:
    1. FDO domain objects
    2. Legacy DB-shaped dictionaries
    3. Actual ORM-shaped dictionaries
    """

    graph = Graph()

    graph.bind("fdo", FDO)
    graph.bind("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
    add_data_type_taxonomy(graph)

    for application in applications or []:
        application = _convert_application_record(
            application
        )
        add_application(graph, application)

    for function in functions or []:
        function = _convert_function_record(
            function
        )
        add_function(graph, function)

    for expected in expected_data or []:
        expected = _convert_expected_data_record(
            expected
        )
        add_expected_data(graph, expected)

    for declared in declared_data or []:
        declared = _convert_declared_data_record(
            declared
        )
        add_declared_data(graph, declared)

    for policy in policies or []:
        add_privacy_policy(graph, policy)

    for clause in policy_clauses or []:
        add_policy_clause(graph, clause)

    for finding in overreach_findings or []:
        add_overreach(graph, finding)

    for item in personal_data or []:
        add_personal_data(graph, item)

    return graph
# ============================================================
# Serialization
# ============================================================

def serialize_rdf_graph(
    graph: Graph,
    output_path: str,
    format: str = "turtle",
) -> str:
    """
    Serialize an RDF graph to a file.
    """

    graph.serialize(
        destination=output_path,
        format=format,
    )

    return output_path
def connect_expected_data_personal_data(
    graph: Graph,
    expected_data_id,
    personal_data_id,
) -> None:
    """
    Connect an ExpectedData individual to its semantic PersonalData concept.
    """
    graph.add(
        (
            expected_data_uri(expected_data_id),
            FDO.expectedDataType,
            personal_data_uri(str(personal_data_id).strip().lower()),
        )
    )


def connect_declared_data_personal_data(
    graph: Graph,
    declared_data_id,
    personal_data_id,
) -> None:
    """
    Connect a DeclaredData individual to its semantic PersonalData concept.
    """
    graph.add(
        (
            declared_data_uri(declared_data_id),
            FDO.declaredDataType,
            personal_data_uri(str(personal_data_id).strip().lower()),
        )
    )
def connect_expected_data_purpose(
    graph: Graph,
    expected_data_id,
    purpose_id,
) -> None:
    """
    Connect an ExpectedData individual to its semantic Purpose concept.
    """
    normalized_purpose = str(purpose_id).strip().lower()

    graph.add(
        (
            expected_data_uri(expected_data_id),
            FDO.expectedDataPurpose,
            purpose_uri(normalized_purpose),
        )
    )


def connect_declared_data_purpose(
    graph: Graph,
    declared_data_id,
    purpose_id,
) -> None:
    """
    Connect a DeclaredData individual to its semantic Purpose concept.
    """
    normalized_purpose = str(purpose_id).strip().lower()

    graph.add(
        (
            declared_data_uri(declared_data_id),
            FDO.declaredDataPurpose,
            purpose_uri(normalized_purpose),
        )
    )
def connect_declared_data_recipient(
    graph: Graph,
    declared_data_id,
    recipient_id,
) -> None:
    """
    Connect DeclaredData to a semantic Recipient.
    """
    normalized_recipient = str(recipient_id).strip().lower()

    graph.add(
        (
            declared_data_uri(declared_data_id),
            FDO.sharedWith,
            recipient_uri(normalized_recipient),
        )
    )


def connect_declared_data_retention(
    graph: Graph,
    declared_data_id,
    retention_id,
) -> None:
    """
    Connect DeclaredData to a semantic RetentionPolicy.
    """
    normalized_retention = str(retention_id).strip().lower()

    graph.add(
        (
            declared_data_uri(declared_data_id),
            FDO.hasRetentionPolicy,
            retention_policy_uri(normalized_retention),
        )
    )
def connect_data_processing_activity(
    graph: Graph,
    personal_data_id,
    processing_activity_id,
) -> None:
    """
    Connect PersonalData to a semantic ProcessingActivity.
    """
    normalized_activity = str(
        processing_activity_id
    ).strip().lower()

    graph.add(
        (
            personal_data_uri(personal_data_id),
            FDO.processedBy,
            processing_activity_uri(normalized_activity),
        )
    )
def add_sensitive_data(
    graph: Graph,
    data: SensitiveData,
) -> None:
    """
    Add a SensitiveData individual to the RDF graph.

    SensitiveData is represented as both:
        fdo:SensitiveData
        fdo:PersonalData

    because SensitiveData is a specialization of PersonalData.
    """

    subject = personal_data_uri(data.id)

    graph.add(
        (
            subject,
            RDF.type,
            FDO.PersonalData,
        )
    )

    graph.add(
        (
            subject,
            RDF.type,
            FDO.SensitiveData,
        )
    )

    graph.add(
        (
            subject,
            FDO.id,
            Literal(data.id),
        )
    )

    graph.add(
        (
            subject,
            FDO.name,
            Literal(data.name),
        )
    )

    graph.add(
        (
            subject,
            FDO.sensitive,
            Literal(True),
        )
    )

    if data.sensitivity_category:
        graph.add(
            (
                subject,
                FDO.sensitivityCategory,
                Literal(
                    data.sensitivity_category.strip().lower()
                ),
            )
        )