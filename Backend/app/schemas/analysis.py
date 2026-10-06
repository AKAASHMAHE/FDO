from pydantic import BaseModel, ConfigDict

class AnalysisCreateRequest(BaseModel):
    application_id: str
class ComparisonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    comparison_id: str
    analysis_id: str
    expected_id: str
    evidence_id: str | None

    data_match: str
    purpose_compatibility: str
    functional_relationship: str
    functional_justification: str
    evidence_status: str


class FDOResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    result_id: str
    comparison_id: str
    fdo_status: str
    decision_reason: str
    decision_confidence: float | None
    created_at: str
class SemanticFDOResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    semantic_result_id: str

    application_id: str
    application: str
    function: str

    expected_data: str
    declared_data: str

    expected_type: str
    declared_type: str

    expected_purpose: str
    declared_purpose: str

    fdo_status: str
    confidence: float | None
    reason: str
    
class AnalysisHistoryResponse(BaseModel):
    analysis_id: str
    application_id: str
    policy_id: str
    analysis_status: str

    total_mappings: int
    fdo_count: int
    not_fdo_count: int
    ambiguous_count: int

    created_at: str
class AnalysisReportResponse(BaseModel):
    analysis_id: str
    application_id: str
    policy_id: str
    analysis_status: str

    total_mappings: int
    fdo_count: int
    not_fdo_count: int
    ambiguous_count: int

    comparisons: list[ComparisonResponse]
    fdo_results: list[FDOResultResponse]
    semantic_results: list[SemanticFDOResultResponse]=[]
class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    application_id: str
    application_name: str
    category: str
    description: str | None
class ApplicationReadinessResponse(BaseModel):
    application_id: str
    application_name: str
    category: str

    policy_count: int
    evidence_count: int

    ready_for_analysis: bool
class FunctionResponse(BaseModel):
    function_id: str
    function_name: str
    feature: str | None


class ApplicationDetailResponse(BaseModel):
    application_id: str
    application_name: str
    category: str
    description: str | None
    functions: list[FunctionResponse]
class ExpectedMappingResponse(BaseModel):
    expected_id: str
    function_id: str
    data_type: str
    necessity: str
    expected_purpose: str


class ExpectedMappingsResponse(BaseModel):
    application_id: str
    expected_mappings: list[ExpectedMappingResponse]
class AnalyzeRequest(BaseModel):
    application_name: str
    category: str
    description: str | None = None
    policy_text: str
    policy_source: str | None = None