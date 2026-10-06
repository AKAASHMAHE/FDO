from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from app.config import settings
from app.database import (
    SessionLocal,
    ensure_sqlite_schema_compatibility,
)
from fastapi.middleware.cors import CORSMiddleware
from app.models.function import Function

from app.services.analysis_report_service import build_analysis_report

from uuid import uuid4

from app.services.rich_report_service import (
    build_rich_analysis_report,
)
from app.services.policy_ingestion_service import (
    create_runtime_policy,
)
from app.services.application_service import (
    get_all_applications,
    get_application,
    get_application_readiness,
    get_or_create_application_for_analysis,
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
    AnalysisHistoryResponse,
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
from app.services.policy_discovery_service import (
    discover_privacy_policy,
)
from app.services.functional_baseline_service import (
    ensure_functional_baseline,
)

from app.services.expected_mapping_service import (
    get_expected_mappings_by_application,
    get_expected_mapping,
)
from app.services.policy_ingestion_service import (
    create_runtime_policy,
)
from app.ontology.semantic_result_repository import (
    SemanticResultRepository,
)
from app.ontology.db_semantic_repository import DBSemanticRepository
from app.ontology.db_semantic_result_service import DBSemanticResultService

from app.services.analysis_service import (
    create_analysis,
    get_analysis,
    get_all_analyses,
    get_comparisons_by_analysis,
    get_fdo_results_by_analysis,
)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for the FDO-Privacy prototype.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def ensure_schema_on_startup():
    ensure_sqlite_schema_compatibility()


from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisReportResponse,
    ApplicationResponse,
    ApplicationReadinessResponse,
    ApplicationDetailResponse,
    ExpectedMappingsResponse,
    AnalyzeRequest,
    AnalysisHistoryResponse,
    SemanticFDOResultResponse,
)

def _analysis_response(report):
    semantic_results = [
        SemanticFDOResultResponse.model_validate(r)
        if not isinstance(r, SemanticFDOResultResponse)
        else r
        for r in (report.semantic_results or [])
    ]
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
        semantic_results=semantic_results,
        policy_analysis=report.policy_analysis,
        has_expected_baseline=report.has_expected_baseline,
        baseline_source=report.baseline_source,
        baseline_confidence=report.baseline_confidence,
        baseline_status=report.baseline_status,
        functional_baseline=report.functional_baseline,
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
    application = get_or_create_application_for_analysis(
        db,
        request.application_name,
        (request.category or "Other").strip() or "Other",
        request.description,
    )

    policy_text = (
        request.policy_text or ""
    ).strip()
    policy_source = request.policy_source

    if not policy_text:
        discovery = discover_privacy_policy(
            request.application_name
        )

        if not discovery.success or not discovery.policy_text:
            raise HTTPException(
                status_code=422,
                detail=(
                    discovery.error
                    or "Privacy policy text is required."
                ),
            )

        policy_text = discovery.policy_text
        policy_source = discovery.source_url

    analysis_id = (
        f"ANALYSIS-{application.application_id}-"
        f"{uuid4().hex[:8]}"
    )

    try:
        # ---------------------------------------------------------
        # 1. Extract policy evidence using AI
        # ---------------------------------------------------------

        evidence = extract_policy_evidence(
            policy_text,
            request.application_name,
        )

        # ---------------------------------------------------------
        # 2. Create runtime policy + evidence records
        # ---------------------------------------------------------

        runtime_policy = create_runtime_policy(
            db,
            application_id=application.application_id,
            policy_text=policy_text,
            policy_source=policy_source,
            evidence=evidence,
            analysis_id=analysis_id,
        )

        # ---------------------------------------------------------
        # 3. Ensure expected functional baseline exists
        # ---------------------------------------------------------

        baseline_result = ensure_functional_baseline(
            db,
            application,
        )

        # ---------------------------------------------------------
        # 4. Run deterministic FDO analysis on runtime policy
        # ---------------------------------------------------------

        run_analysis(
        db,
        analysis_id,
        application.application_id,
        policy_id=runtime_policy.policy_id,
    )

    # ---------------------------------------------------------
    # Semantic FDO analysis
    # ---------------------------------------------------------

        persisted_semantic_results = []

        if baseline_result.available:
            try:
                semantic_repository = DBSemanticRepository(db)

                semantic_service = DBSemanticResultService(
                semantic_repository
            )

                semantic_output_path = (
                Path("outputs")
                / "semantic"
                / f"{analysis_id}.ttl"
            )
                semantic_results = semantic_service.analyze(
            application_id=application.application_id,
            policy_id=runtime_policy.policy_id,
            output_path=semantic_output_path,
        )

                semantic_repository = SemanticResultRepository(db)

                semantic_repository.save_results(
            analysis_id=analysis_id,
            results=semantic_results,
        )
                persisted_semantic_results = (
            semantic_repository.get_by_analysis_id(
                analysis_id
            )
        )
            except Exception:
                persisted_semantic_results = []

        db.commit()

    except ValueError as exc:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        import traceback
        traceback.print_exc()
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Analysis execution failed: {exc}",
        )

    # -------------------------------------------------------------
    # 4. Build final analysis report
    # -------------------------------------------------------------

    report = build_analysis_report(
        db,
        analysis_id,
    )

    if report is None:
        raise HTTPException(
            status_code=500,
            detail="Analysis completed but report could not be loaded.",
        )

    response = _analysis_response(report)
    response.semantic_results = [
        SemanticFDOResultResponse.model_validate(r)
        if not isinstance(r, SemanticFDOResultResponse)
        else r
        for r in (persisted_semantic_results or [])
    ]
    response.baseline_status = baseline_result.status
    return response
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

    return _analysis_response(report)
@app.get(
    "/api/v1/analyses",
    response_model=list[AnalysisHistoryResponse],
)
def get_all_analyses_endpoint(
    db: Session = Depends(get_db),
):
    return get_all_analyses(db)
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

    return _analysis_response(report)
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
        application = get_application(
            db,
            request.application_id,
        )

        if application is None:
            raise ValueError(
                f"Application not found: {request.application_id}"
            )

        ensure_functional_baseline(
            db,
            application,
        )

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

    return _analysis_response(report)
