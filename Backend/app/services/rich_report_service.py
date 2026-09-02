from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.application import Application
from app.models.comparison import Comparison
from app.models.expected_mapping import ExpectedMapping
from app.models.fdo_result import FDOResult
from app.models.function import Function
from app.models.policy_evidence import PolicyEvidence
from app.models.explanation import Explanation


def build_rich_analysis_report(
    session: Session,
    analysis_id: str,
) -> dict | None:

    analysis = session.get(
        Analysis,
        analysis_id,
    )

    if analysis is None:
        return None

    application = session.get(
        Application,
        analysis.application_id,
    )

    if application is None:
        return None

    statement = (
        select(
            Comparison,
            ExpectedMapping,
            Function,
            PolicyEvidence,
            FDOResult,
            Explanation,
        )
        .join(
            ExpectedMapping,
            ExpectedMapping.expected_id
            == Comparison.expected_id,
        )
        .join(
            Function,
            Function.function_record_id
            == ExpectedMapping.function_record_id,
        )
        .outerjoin(
            PolicyEvidence,
            PolicyEvidence.evidence_id
            == Comparison.evidence_id,
        )
        .join(
            FDOResult,
            FDOResult.comparison_id
            == Comparison.comparison_id,
        )
        .outerjoin(
            Explanation,
            Explanation.result_id
            == FDOResult.result_id,
        )
        .where(
            Comparison.analysis_id
            == analysis_id,
        )
        .order_by(
            Comparison.expected_id,
        )
    )

    rows = session.execute(statement).all()

    results = []

    for (
        comparison,
        expected_mapping,
        function,
        evidence,
        fdo_result,
        explanation,
    ) in rows:

        results.append(
            {
                "expected_id": expected_mapping.expected_id,

                "function": {
                    "function_id": function.function_id,
                    "function_name": function.function_name,
                    "feature": function.feature,
                },

                "expected_data": expected_mapping.data_type,

                "declared_data": (
                    evidence.data_type
                    if evidence
                    else None
                ),

                "necessity": expected_mapping.necessity,

                "expected_purpose": (
                    expected_mapping.expected_purpose
                ),

                "declared_purpose": (
                    evidence.purpose
                    if evidence
                    else None
                ),

                "data_match": comparison.data_match,

                "purpose_compatibility": (
                    comparison.purpose_compatibility
                ),

                "functional_relationship": (
                    comparison.functional_relationship
                ),

                "functional_justification": (
                    comparison.functional_justification
                ),

                "evidence_status": comparison.evidence_status,

                "fdo_status": fdo_result.fdo_status,

                "evidence": (
                    {
                        "evidence_id": evidence.evidence_id,
                        "data_type": evidence.data_type,
                        "purpose": evidence.purpose,
                        "evidence_text": evidence.evidence_text,
                        "source_section": evidence.source_section,
                        "extraction_status": (
                            evidence.extraction_status
                        ),
                        "confidence": evidence.confidence,
                    }
                    if evidence
                    else None
                ),

                "explanation": (
                    explanation.explanation_text
                    if explanation
                    else None
                ),

                "decision_confidence": (
                    fdo_result.decision_confidence
                ),
            }
        )

    return {
        "analysis_id": analysis.analysis_id,

        "application": {
            "application_id": application.application_id,
            "application_name": application.application_name,
            "category": application.category,
            "description": application.description,
        },

        "analysis_status": analysis.analysis_status,

        "summary": {
            "total_mappings": analysis.total_mappings,
            "fdo": analysis.fdo_count,
            "not_fdo": analysis.not_fdo_count,
            "ambiguous": analysis.ambiguous_count,
        },

        "results": results,
    }