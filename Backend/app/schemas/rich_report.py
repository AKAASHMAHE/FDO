from pydantic import BaseModel


class RichApplicationResponse(BaseModel):
    application_id: str
    application_name: str
    category: str
    description: str | None = None


class RichFunctionResponse(BaseModel):
    function_id: str
    function_name: str
    feature: str | None = None


class RichEvidenceResponse(BaseModel):
    evidence_id: str | None = None
    data_type: str | None = None
    purpose: str | None = None
    evidence_text: str | None = None
    source_section: str | None = None
    extraction_status: str | None = None
    confidence: float | None = None


class RichAnalysisResultResponse(BaseModel):
    expected_id: str

    function: RichFunctionResponse

    expected_data: str
    declared_data: str | None = None

    necessity: str
    expected_purpose: str
    declared_purpose: str | None = None

    data_match: str
    purpose_compatibility: str
    functional_relationship: str
    functional_justification: str

    evidence_status: str
    fdo_status: str

    evidence: RichEvidenceResponse | None = None

    explanation: str | None = None
    decision_confidence: float | None = None


class RichAnalysisSummaryResponse(BaseModel):
    total_mappings: int
    fdo: int
    not_fdo: int
    ambiguous: int


class RichAnalysisReportResponse(BaseModel):
    analysis_id: str
    application: RichApplicationResponse
    analysis_status: str
    summary: RichAnalysisSummaryResponse
    results: list[RichAnalysisResultResponse]