from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.schemas.analysis import SemanticFDOResultResponse
from app.services.analysis_service import (
    get_analysis,
    get_comparisons_by_analysis,
    get_fdo_results_by_analysis,
)
from app.ontology.semantic_result_repository import (
    SemanticResultRepository,
)
from app.services.policy_analysis_service import (
    PolicyAnalysis,
    build_policy_analysis,
)
from app.models.function import Function
from app.services.expected_mapping_service import (
    get_expected_mappings_by_application,
)
from app.services.functional_baseline_service import (
    baseline_confidence_for_mapping,
    baseline_source_for_mapping,
    get_baseline_confidence,
    get_baseline_source,
)


@dataclass
class AnalysisReport:
    analysis_id: str
    application_id: str
    policy_id: str
    analysis_status: str

    total_mappings: int
    fdo_count: int
    not_fdo_count: int
    ambiguous_count: int

    comparisons: list
    fdo_results: list
    semantic_results: list
    policy_analysis: PolicyAnalysis
    has_expected_baseline: bool
    baseline_source: str | None
    baseline_confidence: float | None
    baseline_status: str
    functional_baseline: list


def build_analysis_report(
    session: Session,
    analysis_id: str,
) -> AnalysisReport | None:

    analysis = get_analysis(
        session,
        analysis_id,
    )

    if not analysis:
        return None

    comparisons = get_comparisons_by_analysis(
        session,
        analysis_id,
    )

    fdo_results = get_fdo_results_by_analysis(
        session,
        analysis_id,
    )

    raw_semantic_results = (
        SemanticResultRepository(session)
        .get_by_analysis_id(analysis_id)
    )
    semantic_results = [
        SemanticFDOResultResponse.model_validate(r)
        for r in raw_semantic_results
    ]

    policy_analysis = build_policy_analysis(
        session,
        analysis.policy_id,
    )

    expected_mappings = get_expected_mappings_by_application(
        session,
        analysis.application_id,
    )

    functional_baseline = []

    for mapping in expected_mappings:
        function = session.get(
            Function,
            mapping.function_record_id,
        )

        functional_baseline.append(
            {
                "expected_id": mapping.expected_id,
                "function_id": (
                    function.function_id if function else None
                ),
                "function_name": (
                    function.function_name
                    if function
                    else "Unknown Function"
                ),
                "expected_data_type": mapping.data_type,
                "necessity": mapping.necessity,
                "expected_purpose": mapping.expected_purpose,
                "baseline_source": baseline_source_for_mapping(
                    mapping
                ),
                "baseline_confidence": (
                    baseline_confidence_for_mapping(mapping)
                ),
                "baseline_justification": getattr(
                    mapping,
                    "baseline_justification",
                    None,
                ),
            }
        )

    baseline_source = get_baseline_source(expected_mappings)
    baseline_status = (
        "PROVISIONAL"
        if baseline_source == "AI_DERIVED"
        else ("AVAILABLE" if expected_mappings else "UNAVAILABLE")
    )

    return AnalysisReport(
        analysis_id=analysis.analysis_id,
        application_id=analysis.application_id,
        policy_id=analysis.policy_id,
        analysis_status=analysis.analysis_status,
        total_mappings=analysis.total_mappings,
        fdo_count=analysis.fdo_count,
        not_fdo_count=analysis.not_fdo_count,
        ambiguous_count=analysis.ambiguous_count,
        comparisons=comparisons,
        fdo_results=fdo_results,
        semantic_results=semantic_results,
        policy_analysis=policy_analysis,
        has_expected_baseline=analysis.total_mappings > 0,
        baseline_source=baseline_source,
        baseline_confidence=get_baseline_confidence(
            expected_mappings
        ),
        baseline_status=baseline_status,
        functional_baseline=functional_baseline,
    )
