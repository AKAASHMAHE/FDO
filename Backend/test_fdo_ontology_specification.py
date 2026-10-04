from app.ontology.specification import (
    FDOSpecification,
    FDO_SPECIFICATION,
    get_fdo_specification,
    list_fdo_classes,
    list_fdo_object_properties,
    list_fdo_data_properties,
    list_fdo_competency_questions,
    get_fdo_summary,
)


def test_fdo_specification_is_valid():
    assert isinstance(FDO_SPECIFICATION, FDOSpecification)


def test_get_fdo_specification_returns_canonical_specification():
    specification = get_fdo_specification()

    assert specification is FDO_SPECIFICATION


def test_specification_contains_classes():
    specification = get_fdo_specification()

    assert specification.classes
    assert "Application" in specification.classes
    assert "Function" in specification.classes
    assert "PersonalData" in specification.classes
    assert "Overreach" in specification.classes


def test_specification_contains_object_properties():
    specification = get_fdo_specification()

    assert specification.object_properties
    assert "performsFunction" in specification.object_properties
    assert "requiresData" in specification.object_properties
    assert "collectsData" in specification.object_properties
    assert "hasJustification" in specification.object_properties


def test_specification_contains_data_properties():
    specification = get_fdo_specification()

    assert specification.data_properties
    assert "id" in specification.data_properties
    assert "name" in specification.data_properties
    assert "dataType" in specification.data_properties
    assert "confidence" in specification.data_properties


def test_specification_contains_cardinality_constraints():
    specification = get_fdo_specification()

    assert specification.cardinality_constraints

    property_names = {
        constraint.property_name
        for constraint in specification.cardinality_constraints
    }

    assert "performsFunction" in property_names
    assert "concernsData" in property_names
    assert "hasJustification" in property_names


def test_specification_contains_required_property_constraints():
    specification = get_fdo_specification()

    assert specification.required_property_constraints

    property_names = {
        constraint.property_name
        for constraint in specification.required_property_constraints
    }

    assert "name" in property_names
    assert "dataType" in property_names
    assert "text" in property_names
    assert "reason" in property_names


def test_specification_contains_competency_questions():
    specification = get_fdo_specification()

    assert len(specification.competency_questions) == 20

    question_ids = {
        question.id
        for question in specification.competency_questions
    }

    assert "CQ01" in question_ids
    assert "CQ05" in question_ids
    assert "CQ14" in question_ids
    assert "CQ20" in question_ids


def test_list_fdo_classes():
    classes = list_fdo_classes()

    assert "Application" in classes
    assert "Function" in classes
    assert "PersonalData" in classes
    assert "PrivacyPolicy" in classes
    assert "Overreach" in classes


def test_list_fdo_object_properties():
    properties = list_fdo_object_properties()

    assert "performsFunction" in properties
    assert "requiresData" in properties
    assert "expectedData" in properties
    assert "hasRisk" in properties


def test_list_fdo_data_properties():
    properties = list_fdo_data_properties()

    assert "id" in properties
    assert "name" in properties
    assert "dataType" in properties
    assert "necessity" in properties
    assert "purpose" in properties
    assert "confidence" in properties


def test_list_fdo_competency_questions():
    questions = list_fdo_competency_questions()

    assert len(questions) == 20
    assert "CQ01" in questions
    assert "CQ10" in questions
    assert "CQ20" in questions


def test_fdo_summary():
    summary = get_fdo_summary()

    assert summary["classes"] == len(FDO_SPECIFICATION.classes)
    assert summary["object_properties"] == len(
        FDO_SPECIFICATION.object_properties
    )
    assert summary["data_properties"] == len(
        FDO_SPECIFICATION.data_properties
    )
    assert summary["cardinality_constraints"] == len(
        FDO_SPECIFICATION.cardinality_constraints
    )
    assert summary["required_property_constraints"] == len(
        FDO_SPECIFICATION.required_property_constraints
    )
    assert summary["competency_questions"] == len(
        FDO_SPECIFICATION.competency_questions
    )


def test_fdo_specification_is_complete():
    specification = get_fdo_specification()

    assert specification.classes
    assert specification.object_properties
    assert specification.data_properties
    assert specification.cardinality_constraints
    assert specification.required_property_constraints
    assert specification.competency_questions