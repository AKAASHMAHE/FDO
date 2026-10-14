from eval.run_idf_b_eval import _semantic_finding_reason


def test_semantic_reason_distinguishes_no_finding():
    assert _semantic_finding_reason([]) == (
        "No semantic finding was returned for this mapping."
    )


def test_semantic_reason_preserves_single_finding_reason():
    assert _semantic_finding_reason(
        [{"reason": "The semantic finding is supported."}]
    ) == "The semantic finding is supported."


def test_semantic_reason_reports_multiple_unanimous_findings():
    assert _semantic_finding_reason(
        [
            {"fdo_status": "FDO"},
            {"fdo_status": "FDO"},
        ]
    ) == "2 semantic findings were returned with unanimous verdict FDO."


def test_semantic_reason_reports_conflicting_findings():
    assert _semantic_finding_reason(
        [
            {"fdo_status": "FDO"},
            {"fdo_status": "NOT_FDO"},
        ]
    ) == "2 semantic findings were returned with conflicting verdicts."
