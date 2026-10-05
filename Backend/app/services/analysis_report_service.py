from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.services.analysis_service import (
    get_analysis,
    get_comparisons_by_analysis,
    get_fdo_results_by_analysis,
)
from app.ontology.semantic_result_repository import (
    SemanticResultRepository,
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

    semantic_results = (
        SemanticResultRepository(session)
        .get_by_analysis_id(analysis_id)
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
    )