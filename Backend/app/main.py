from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal

from app.models.function import Function

from app.services.analysis_report_service import build_analysis_report
from uuid import uuid4
from app.services.rich_report_service import (
    build_rich_analysis_report,
)
from app.services.application_service import (
    get_all_applications,
    get_application,
    get_application_readiness,
    find_application_by_name_and_category,
)
from app.services.function_service import (
    get_functions_by_application,
)
from app.schemas.analysis_result import AnalysisResultResponse

from app.services.analysis_result_service import get_analysis_results

from app.services.analysis_runner import run_analysis
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisReportResponse,
    ApplicationResponse,
    ApplicationReadinessResponse,
    ApplicationDetailResponse,
    ExpectedMappingsResponse,
    AnalyzeRequest,
)
from app.schemas.policy_extraction import (
    PolicyExtractionRequest,
    PolicyEvidenceResponse,
    PolicyExtractionResponse,
)
from app.schemas.rich_report import (
    RichAnalysisReportResponse,
)
from app.services.policy_extraction_service import (
    extract_policy_evidence,
)

from app.services.expected_mapping_service import (
    get_expected_mappings_by_application,
    get_expected_mapping,
)
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for the FDO-Privacy prototype.",
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get(
    "/api/v1/applications/{application_id}/expected-mappings",
    response_model=ExpectedMappingsResponse,
)
def get_expected_mappings_endpoint(
    application_id: str,
    db: Session = Depends(get_db),
):
    application = get_application(
        db,
        application_id,
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail=f"Application not found: {application_id}",
        )

    mappings = get_expected_mappings_by_application(
        db,
        application_id,
    )

    return {
        "application_id": application_id,
        "expected_mappings": [
            {
                "expected_id": mapping.expected_id,
                "function_id": db.get(
                    Function,
                    mapping.function_record_id,
                ).function_id,
                "data_type": mapping.data_type,
                "necessity": mapping.necessity,
                "expected_purpose": mapping.expected_purpose,
            }
            for mapping in mappings
        ],
    }

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "service": "fdo-privacy-backend",
    }

@app.get(
    "/api/v1/applications",
    response_model=list[ApplicationResponse],
)
def get_applications(
    db: Session = Depends(get_db),
):
    return get_all_applications(db)


@app.get(
    "/api/v1/applications/{application_id}",
    response_model=ApplicationDetailResponse,
)
def get_application_detail_endpoint(
    application_id: str,
    db: Session = Depends(get_db),
):
    application = get_application(
        db,
        application_id,
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail=f"Application not found: {application_id}",
        )

    functions = get_functions_by_application(
        db,
        application_id,
    )

    return {
        "application_id": application.application_id,
        "application_name": application.application_name,
        "category": application.category,
        "description": application.description,
        "functions": [
            {
                "function_id": function.function_id,
                "function_name": function.function_name,
                "feature": function.feature,
            }
            for function in functions
        ],
    }
@app.get(
    "/api/v1/applications/{application_id}/readiness",
    response_model=ApplicationReadinessResponse,
)
def get_application_readiness_endpoint(
    application_id: str,
    db: Session = Depends(get_db),
):
    readiness = get_application_readiness(
        db,
        application_id,
    )

    if readiness is None:
        raise HTTPException(
            status_code=404,
            detail=f"Application not found: {application_id}",
        )

    return readiness
@app.post(
    "/api/v1/extract-policy",
    response_model=PolicyExtractionResponse,
)
def extract_policy_endpoint(
    request: PolicyExtractionRequest,
):
    if not request.policy_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Privacy policy text is required.",
        )

    evidence = extract_policy_evidence(
        request.policy_text,
        request.application_name,
    )

    return {
        "extraction_status": "COMPLETED",
        "evidence": [
            PolicyEvidenceResponse(**item)
            for item in evidence
        ],
    }
@app.post(
    "/api/v1/analyze",
    response_model=AnalysisReportResponse,
)
def analyze_endpoint(
    request: AnalyzeRequest,
    db: Session = Depends(get_db),
):
    if not request.policy_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Privacy policy text is required.",
        )

    application = find_application_by_name_and_category(
        db,
        request.application_name,
        request.category,
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Application not found: "
                f"{request.application_name}"
            ),
        )

    analysis_id = (
        f"ANALYSIS-{application.application_id}-"
        f"{uuid4().hex[:8]}"
    )

    try:
        run_analysis(
            db,
            analysis_id,
            application.application_id,
        )

        db.commit()

    except ValueError as exc:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Analysis execution failed.",
        )

    report = build_analysis_report(
        db,
        analysis_id,
    )

    if report is None:
        raise HTTPException(
            status_code=500,
            detail="Analysis completed but report could not be loaded.",
        )

    return AnalysisReportResponse(
        analysis_id=report.analysis_id,
        application_id=report.application_id,
        policy_id=report.policy_id,
        analysis_status=report.analysis_status,
        total_mappings=report.total_mappings,
        fdo_count=report.fdo_count,
        not_fdo_count=report.not_fdo_count,
        ambiguous_count=report.ambiguous_count,
        comparisons=report.comparisons,
        fdo_results=report.fdo_results,
    )
@app.get(
    "/api/v1/analyses/{analysis_id}/results",
    response_model=list[AnalysisResultResponse],
)
def get_analysis_results_endpoint(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    report = build_analysis_report(
        db,
        analysis_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis not found: {analysis_id}",
        )

    return get_analysis_results(
        db,
        analysis_id,
    )
@app.get(
    "/api/v1/analysis/{analysis_id}/report",
    response_model=RichAnalysisReportResponse,
)
def get_analysis_report_endpoint(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    report = build_rich_analysis_report(
        db,
        analysis_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis not found: {analysis_id}",
        )

    return report
@app.get(
    "/api/v1/analysis/{analysis_id}",
    response_model=AnalysisReportResponse,
)
def get_analysis_endpoint(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    report = build_analysis_report(
        db,
        analysis_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis not found: {analysis_id}",
        )

    return AnalysisReportResponse(
        analysis_id=report.analysis_id,
        application_id=report.application_id,
        policy_id=report.policy_id,
        analysis_status=report.analysis_status,
        total_mappings=report.total_mappings,
        fdo_count=report.fdo_count,
        not_fdo_count=report.not_fdo_count,
        ambiguous_count=report.ambiguous_count,
        comparisons=report.comparisons,
        fdo_results=report.fdo_results,
    )
@app.get(
    "/api/v1/analyses/{analysis_id}",
    response_model=AnalysisReportResponse,
)
def get_analysis_report(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    report = build_analysis_report(
        db,
        analysis_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis not found: {analysis_id}",
        )

    return AnalysisReportResponse(
        analysis_id=report.analysis_id,
        application_id=report.application_id,
        policy_id=report.policy_id,
        analysis_status=report.analysis_status,
        total_mappings=report.total_mappings,
        fdo_count=report.fdo_count,
        not_fdo_count=report.not_fdo_count,
        ambiguous_count=report.ambiguous_count,
        comparisons=report.comparisons,
        fdo_results=report.fdo_results,
    )
@app.post(
    "/api/v1/analyses",
    response_model=AnalysisReportResponse,
)
def create_analysis_endpoint(
    request: AnalysisCreateRequest,
    db: Session = Depends(get_db),
):
    analysis_id = (
        f"ANALYSIS-{request.application_id}-"
        f"{uuid4().hex[:8]}"
    )

    try:
        run_analysis(
            db,
            analysis_id,
            request.application_id,
        )

        db.commit()

    except ValueError as exc:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Analysis execution failed.",
        )

    report = build_analysis_report(
        db,
        analysis_id,
    )

    if report is None:
        raise HTTPException(
            status_code=500,
            detail="Analysis completed but report could not be loaded.",
        )

    return AnalysisReportResponse(
        analysis_id=report.analysis_id,
        application_id=report.application_id,
        policy_id=report.policy_id,
        analysis_status=report.analysis_status,
        total_mappings=report.total_mappings,
        fdo_count=report.fdo_count,
        not_fdo_count=report.not_fdo_count,
        ambiguous_count=report.ambiguous_count,
        comparisons=report.comparisons,
        fdo_results=report.fdo_results,
    )