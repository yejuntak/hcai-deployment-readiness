import pytest
from pydantic import ValidationError

from hcai_readiness.grade import (
    HardPosture,
    ReportGradeInput,
    ReportFinding,
    calculate_report_grade,
    hard_posture_from_artifact_result,
    hard_posture_from_engineering_result,
    render_grade_report,
)


def finding(
    id,
    module,
    status="pass",
    evidence_level="public_observation",
    weight=1,
    title=None,
    **extra,
):
    data = {
        "id": id,
        "module": module,
        "title": title or id,
        "status": status,
        "evidence_level": evidence_level,
        "weight": weight,
        "summary": "Synthetic test finding",
        **extra,
    }
    if status == "unknown":
        data.setdefault("evidence_level", "unknown")
        data.setdefault("next_evidence", "Supply the relevant retained evidence")
    else:
        data.setdefault("evidence_locations", [f"synthetic://{id}"])
    return ReportFinding(**data)


def sample_report(hard=None):
    # Module scores: accessibility 90, action/recovery 62.5,
    # privacy 80, AI transparency 80, public evidence 80 => weighted 78.
    findings = [
        finding("a1", "accessibility", weight=4),
        finding("a2", "accessibility", status="warning", weight=1),
        finding("r1", "action_recovery", weight=2),
        finding("r2", "action_recovery", status="warning"),
        finding("r3", "action_recovery", status="critical"),
        finding("p1", "privacy_data", weight=3),
        finding("p2", "privacy_data", status="warning", weight=2),
        finding("t1", "ai_transparency", weight=3),
        finding("t2", "ai_transparency", status="warning", weight=2),
        finding("e1", "public_evidence", weight=3),
        finding("e2", "public_evidence", status="warning", weight=2),
    ]
    return ReportGradeInput(
        subject="Synthetic Product",
        reviewed_surface="Synthetic public product surface",
        findings=findings,
        hard=hard or HardPosture(),
    )


def test_public_product_grade_is_78_and_hard_is_not_weighted():
    result = calculate_report_grade(sample_report())
    assert result["score"] == 78
    assert result["grade"] == "B"
    assert result["scoring"]["hard_in_numeric_score"] is False
    assert "hard_core" not in result["scoring"]["module_weights"]
    assert result["hard"]["status"] == "NOT VERIFIED"


def test_hard_hold_does_not_change_numeric_grade_but_is_prominent():
    report = sample_report(
        HardPosture(
            route="artifact_review",
            disposition="hold_for_remediation",
            evidence_ceiling="walkthrough",
            blocker_ids=["choice-refund"],
            summary="Synthetic blocker",
        )
    )
    result = calculate_report_grade(report)
    assert result["score"] == 78
    assert result["hard"]["status"] == "HOLD"
    assert result["overall_display"] == "B · 78/100 / HOLD"
    assert result["hard"]["blocker_ids"] == ["choice-refund"]


def test_unknown_does_not_lower_signal_score_but_lowers_coverage_and_confidence():
    baseline = sample_report()
    base = calculate_report_grade(baseline)
    report = sample_report()
    report.findings.append(
        finding(
            "a-unknown",
            "accessibility",
            status="unknown",
            evidence_level="unknown",
            weight=5,
            next_evidence="Run an assistive-technology walkthrough",
        )
    )
    result = calculate_report_grade(report)
    assert result["score"] == base["score"]
    accessibility = next(row for row in result["modules"] if row["id"] == "accessibility")
    assert accessibility["coverage"] == 50
    assert result["coverage"] < base["coverage"]
    assert result["confidence"] < base["confidence"]


def test_assessed_findings_require_retained_evidence_and_unknown_requires_next_evidence():
    with pytest.raises(ValidationError):
        finding("bad1", "public_evidence", evidence_locations=[])
    with pytest.raises(ValidationError):
        ReportFinding(
            id="bad2",
            module="public_evidence",
            title="Unknown without next evidence",
            status="unknown",
            evidence_level="unknown",
        )


def test_auxiliary_scores_never_enter_overall_grade():
    report = sample_report()
    before = calculate_report_grade(report)["score"]
    report.auxiliary_scores = [
        {"label": "SEO", "score": 5, "note": "Synthetic"},
        {"label": "AEO", "score": 100, "note": "Synthetic"},
    ]
    result = calculate_report_grade(report)
    assert result["score"] == before
    assert result["scoring"]["auxiliary_scores_in_numeric_score"] is False


def test_artifact_result_projection_reuses_existing_disposition_without_scoring_it():
    posture = hard_posture_from_artifact_result(
        {
            "disposition": "Hold for remediation",
            "required_evidence_levels": ["specified", "walkthrough"],
            "unresolved_critical_ids": ["F1"],
            "unresolved_major_ids": [],
            "deepening_failure_ids": ["C1"],
            "choices_requiring_revision": [],
        }
    )
    assert posture.disposition == "hold_for_remediation"
    assert posture.evidence_ceiling == "walkthrough"
    assert posture.blocker_ids == ["F1", "C1"]


def test_engineering_result_projection_preserves_noncompensatory_gate_failure():
    posture = hard_posture_from_engineering_result(
        {
            "decision": "REVISE",
            "gates": [
                {"id": "G1_BASELINE", "status": "PASS"},
                {"id": "G3_STATES_RECOVERY", "status": "FAIL"},
            ],
            "unresolved_critical_ids": ["critical-1"],
        }
    )
    assert posture.disposition == "revise_before_engineering"
    assert posture.blocker_ids == ["G3_STATES_RECOVERY", "critical-1"]


def test_html_escapes_subject_and_evidence_copy():
    report = sample_report()
    report.subject = "<script>alert(1)</script>"
    output = render_grade_report(report, "html")
    assert "<script>alert(1)</script>" not in output
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in output
    assert "Product Signal Grade" in output
    assert "H.A.R.D. posture" not in output  # HTML uses the compact status treatment


def test_markdown_says_grade_is_not_hard_score():
    output = render_grade_report(sample_report(), "markdown")
    assert "Product Signal Grade" in output
    assert "H.A.R.D. posture:" in output
    assert "not a H.A.R.D. protocol score" in output
