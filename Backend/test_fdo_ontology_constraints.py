from app.ontology import (
    Application,
    CardinalityConstraint,
    DeclaredData,
    ExpectedData,
    FDO_CARDINALITY_CONSTRAINTS,
    FDO_REQUIRED_PROPERTY_CONSTRAINTS,
    Function,
    Overreach,
    PersonalData,
    PolicyClause,
    PrivacyPolicy,
    RequiredPropertyConstraint,
)


def test_cardinality_constraint_structure():
    constraint = FDO_CARDINALITY_CONSTRAINTS[0]

    assert isinstance(constraint, CardinalityConstraint)
    assert constraint.property_name
    assert constraint.domain


def test_application_requires_function():
    constraints = [
        c
        for c in FDO_CARDINALITY_CONSTRAINTS
        if c.property_name == "performsFunction"
    ]

    assert len(constraints) == 1
    assert constraints[0].domain is Application
    assert constraints[0].min_count == 1


def test_function_requires_data_is_optional():
    constraint = next(
        c for c in FDO_CARDINALITY_CONSTRAINTS
        if c.property_name == "requiresData"
    )

    assert constraint.domain is Function
    assert constraint.min_count == 0


def test_application_collects_data_is_optional():
    constraint = next(
        c for c in FDO_CARDINALITY_CONSTRAINTS
        if c.property_name == "collectsData"
    )

    assert constraint.domain is Application
    assert constraint.min_count == 0


def test_retention_policy_has_maximum_one():
    constraint = next(
        c for c in FDO_CARDINALITY_CONSTRAINTS
        if c.property_name == "hasRetentionPolicy"
    )

    assert constraint.domain is PersonalData
    assert constraint.max_count == 1


def test_overreach_concerns_exactly_one_data():
    constraint = next(
        c for c in FDO_CARDINALITY_CONSTRAINTS
        if c.property_name == "concernsData"
    )

    assert constraint.domain is Overreach
    assert constraint.min_count == 1
    assert constraint.max_count == 1


def test_overreach_function_is_optional():
    constraint = next(
        c for c in FDO_CARDINALITY_CONSTRAINTS
        if c.property_name == "concernsFunction"
    )

    assert constraint.domain is Overreach
    assert constraint.min_count == 0
    assert constraint.max_count == 1


def test_overreach_justification_is_optional():
    constraint = next(
        c for c in FDO_CARDINALITY_CONSTRAINTS
        if c.property_name == "hasJustification"
    )

    assert constraint.domain is Overreach
    assert constraint.max_count == 1


def test_overreach_risk_is_optional():
    constraint = next(
        c for c in FDO_CARDINALITY_CONSTRAINTS
        if c.property_name == "hasRisk"
    )

    assert constraint.domain is Overreach
    assert constraint.max_count == 1


def test_required_property_structure():
    constraint = FDO_REQUIRED_PROPERTY_CONSTRAINTS[0]

    assert isinstance(constraint, RequiredPropertyConstraint)
    assert constraint.property_name
    assert constraint.domain


def test_application_name_required():
    constraint = next(
        c for c in FDO_REQUIRED_PROPERTY_CONSTRAINTS
        if c.property_name == "name" and c.domain is Application
    )

    assert constraint


def test_function_name_required():
    constraint = next(
        c for c in FDO_REQUIRED_PROPERTY_CONSTRAINTS
        if c.property_name == "name" and c.domain is Function
    )

    assert constraint


def test_personal_data_name_required():
    constraint = next(
        c for c in FDO_REQUIRED_PROPERTY_CONSTRAINTS
        if c.property_name == "name" and c.domain is PersonalData
    )

    assert constraint


def test_expected_data_type_required():
    constraint = next(
        c for c in FDO_REQUIRED_PROPERTY_CONSTRAINTS
        if c.property_name == "dataType"
        and c.domain is ExpectedData
    )

    assert constraint


def test_declared_data_type_required():
    constraint = next(
        c for c in FDO_REQUIRED_PROPERTY_CONSTRAINTS
        if c.property_name == "dataType"
        and c.domain is DeclaredData
    )

    assert constraint


def test_policy_clause_text_required():
    constraint = next(
        c for c in FDO_REQUIRED_PROPERTY_CONSTRAINTS
        if c.property_name == "text"
    )

    assert constraint.domain is PolicyClause


def test_policy_source_required():
    constraint = next(
        c for c in FDO_REQUIRED_PROPERTY_CONSTRAINTS
        if c.property_name == "source"
    )

    assert constraint.domain is PrivacyPolicy


def test_overreach_reason_required():
    constraint = next(
        c for c in FDO_REQUIRED_PROPERTY_CONSTRAINTS
        if c.property_name == "reason"
    )

    assert constraint.domain is Overreach


def test_all_constraints_have_descriptions():
    for constraint in FDO_CARDINALITY_CONSTRAINTS:
        assert constraint.description

    for constraint in FDO_REQUIRED_PROPERTY_CONSTRAINTS:
        assert constraint.description


def test_constraint_property_names_are_not_empty():
    for constraint in FDO_CARDINALITY_CONSTRAINTS:
        assert constraint.property_name

    for constraint in FDO_REQUIRED_PROPERTY_CONSTRAINTS:
        assert constraint.property_name