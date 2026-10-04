"""
FDO Ontology - Final Semantic Specification

This module provides the single formal specification of the
Functional Data Ontology (FDO) semantic model.

It combines:

    1. FDO classes
    2. Object properties
    3. Data properties
    4. Cardinality constraints
    5. Required-property constraints
    6. Competency questions

This module is intentionally independent of RDF/OWL serialization.

The RDF/OWL implementation will consume this specification
in the next stage.
"""

from dataclasses import dataclass
from typing import Dict, List

from .registry import FDO_CLASSES
from .properties import FDO_OBJECT_PROPERTIES
from .data_properties import FDO_DATA_PROPERTIES
from .constraints import (
    FDO_CARDINALITY_CONSTRAINTS,
    FDO_REQUIRED_PROPERTY_CONSTRAINTS,
)
from .competency_questions import FDO_COMPETENCY_QUESTIONS


@dataclass(frozen=True)
class FDOSpecification:
    """
    Complete semantic specification of the FDO ontology.
    """

    classes: Dict
    object_properties: Dict
    data_properties: Dict
    cardinality_constraints: List
    required_property_constraints: List
    competency_questions: List


FDO_SPECIFICATION = FDOSpecification(
    classes=FDO_CLASSES,
    object_properties=FDO_OBJECT_PROPERTIES,
    data_properties=FDO_DATA_PROPERTIES,
    cardinality_constraints=FDO_CARDINALITY_CONSTRAINTS,
    required_property_constraints=FDO_REQUIRED_PROPERTY_CONSTRAINTS,
    competency_questions=FDO_COMPETENCY_QUESTIONS,
)


def get_fdo_specification() -> FDOSpecification:
    """
    Return the complete FDO semantic specification.
    """
    return FDO_SPECIFICATION


def list_fdo_classes() -> List[str]:
    """
    Return all registered FDO class names.
    """
    return list(FDO_CLASSES.keys())


def list_fdo_object_properties() -> List[str]:
    """
    Return all registered FDO object-property names.
    """
    return list(FDO_OBJECT_PROPERTIES.keys())


def list_fdo_data_properties() -> List[str]:
    """
    Return all registered FDO data-property names.
    """
    return list(FDO_DATA_PROPERTIES.keys())


def list_fdo_competency_questions() -> List[str]:
    """
    Return all registered competency-question IDs.
    """
    return [
        question.id
        for question in FDO_COMPETENCY_QUESTIONS
    ]


def get_fdo_summary() -> Dict[str, int]:
    """
    Return a compact summary of the ontology specification.
    """
    return {
        "classes": len(FDO_CLASSES),
        "object_properties": len(FDO_OBJECT_PROPERTIES),
        "data_properties": len(FDO_DATA_PROPERTIES),
        "cardinality_constraints": len(
            FDO_CARDINALITY_CONSTRAINTS
        ),
        "required_property_constraints": len(
            FDO_REQUIRED_PROPERTY_CONSTRAINTS
        ),
        "competency_questions": len(
            FDO_COMPETENCY_QUESTIONS
        ),
    }