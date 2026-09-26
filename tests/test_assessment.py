import json
from pathlib import Path
import pytest
from pydantic import ValidationError
from hcai_readiness.assessment import Session, Judgment, calculate_session, summarize_judgments

ROOT = Path(__file__).resolve().parents[1]

def valid_roles():
    return {"reference_frozen_before_evaluation": True, "reference_independent_of_findings": True,
            "evaluator_authored_artifact": False, "evaluator_authored_reference": False,
            "evaluator_is_adjudicator": False, "findings_locked_before_reference": True,
            "expected_recall_locked_before_reference": True, "omission_subset_frozen": True,
            "criterion_independently_established": True}

def sample():
    data = json.loads((ROOT / "examples/session.json").read_text())
    # Explicit synthetic fixture facts, not a production migration default.
    data.update(artifact_population="ai_generated", stage="prototype_handoff",
                mode="independent_evaluation", evaluator_validity=valid_roles())
    return data

def test_published_example():
    r = calculate_session(Session(**sample()))
    assert r["metrics"] == {"reference_set_recall_percent":62.5, "expected_recall_gap_pp":17.5,
        "requirements_omission_recognition_percent":33.333333,
        "artifact_requirements_coverage_percent":70.0, "handoff_recovery_coverage_percent":50.0}
    assert r["disposition"] == "Hold for remediation"

@pytest.mark.parametrize("field,value", [("reference_defects",-1),("reference_defects",True),
    ("reference_defects",8.2),("detected_reference_defects",9),("detected_reference_omissions",4),
    ("expected_recall_percent",float("nan")),("expected_recall_percent",101)])
def test_reject_bad_counts(field,value):
    d=sample(); d[field]=value
    with pytest.raises(ValidationError): Session(**d)

def test_cross_subset_consistency():
    d=sample(); d.update(detected_reference_defects=7, detected_reference_omissions=1)
    with pytest.raises(ValidationError): Session(**d)

def test_missing_is_not_pass_or_zero():
    d=sample(); d.update(requirements=None,recovery=None,unresolved_critical=None,evidence_complete=None,
                         reference_defects=None, detected_reference_defects=None)
    r=calculate_session(Session(**d))
    assert r["criterion_status"]=="unknown"
    assert r["metrics"]["reference_set_recall_percent"] is None

def test_unassessed_is_nonready_and_zero_recovery_requires_reason():
    d=sample(); d.update(unresolved_critical=0,requirements={"total":10,"verified":9,"failed":0,"unassessed":1},
                       recovery={"total":0,"verified":0,"failed":0,"unassessed":0})
    with pytest.raises(ValidationError): Session(**d)
    d["zero_recovery_reason"]="No applicable scenarios under this hypothetical scoped task"
    r=calculate_session(Session(**d))
    assert r["disposition"]=="Insufficient evidence"
    assert r["metrics"]["handoff_recovery_coverage_percent"] is None

def test_ready_is_not_approval():
    d=sample(); d.update(unresolved_critical=0,requirements={"total":10,"verified":10,"failed":0,"unassessed":0},
                       recovery={"total":6,"verified":6,"failed":0,"unassessed":0})
    assert calculate_session(Session(**d))["disposition"]=="Aggregate checks satisfied; stage handoff not established"

def row(i,j,status="nonready",kind="synthetic"):
    return Judgment(instance_id=str(i),artifact_version="v1",criterion_version="c1",evaluator_kind=kind,
                    artifact_population="ai_generated", stage="prototype_handoff", mode="independent_evaluation",
                    evaluator_validity=valid_roles(), judgment_locked_before_reference=True,
                    criterion_status=status,judgment=j)

def test_abstention_missing_and_unknown():
    r=summarize_judgments([row(1,"Unable to assess"),row(2,None),row(3,"Ready","unknown")])
    assert r["nonready"]["false_ready_acceptance_percent"]==0
    assert r["nonready"]["decision_coverage_percent"]==0
    assert r["nonready"]["decisive_false_ready_acceptance_percent"] is None
    assert r["nonready"]["missing"]==1
    assert r["unknown_criterion_count"]==1

def test_ready_controls_and_population_separation():
    assert summarize_judgments([row(1,"Not ready","ready")])["ready"]["false_hold_percent"]==100
    with pytest.raises(ValueError): summarize_judgments([row(1,"Ready"),row(2,"Ready",kind="human")])
    with pytest.raises(ValueError): summarize_judgments([row(1,"Ready"),row(1,"Ready")])

def test_check_totals():
    d=sample(); d["requirements"]["verified"]=8
    with pytest.raises(ValidationError): Session(**d)


@pytest.mark.parametrize("model", [Session, Judgment])
def test_population_is_required(model):
    data = sample() if model is Session else row(1, "Ready").model_dump()
    data.pop("artifact_population")
    with pytest.raises(ValidationError): model(**data)

@pytest.mark.parametrize("dimension,value", [("artifact_population", "runtime_ai"),
    ("stage", "specification_handoff"), ("mode", "artifact_review"), ("criterion_version", "c2")])
def test_all_comparison_dimensions_are_stratified(dimension, value):
    first, second = row(1, "Ready"), row(2, "Ready")
    second = Judgment(**{**second.model_dump(), dimension: value})
    with pytest.raises(ValueError, match="Stratify"):
        summarize_judgments([first, second])

@pytest.mark.parametrize("dimension,value", [("artifact_population", "unknown"),
    ("stage", "unspecified"), ("mode", "legacy_diagnostic")])
def test_unknown_comparison_dimensions_cannot_be_pooled(dimension, value):
    record = Judgment(**{**row(1, "Ready").model_dump(), dimension: value})
    with pytest.raises(ValueError, match="Explicit"):
        summarize_judgments([record])

def test_artifact_review_retains_coverage_without_research_metrics():
    data = sample(); data.update(mode="artifact_review", evaluator_validity={})
    result = calculate_session(Session(**data))
    for name in ("reference_set_recall_percent", "expected_recall_gap_pp", "requirements_omission_recognition_percent"):
        assert result["metrics"][name] is None
        assert result["metric_ineligibility_reasons"][name]
    assert result["metrics"]["artifact_requirements_coverage_percent"] == 70
    assert result["metrics"]["handoff_recovery_coverage_percent"] == 50

@pytest.mark.parametrize("field,value,code", [
    ("evaluator_authored_artifact", True, "self_evaluation"),
    ("evaluator_authored_reference", True, "reference_known_to_evaluator"),
    ("reference_frozen_before_evaluation", False, "reference_not_prospectively_frozen"),
    ("reference_independent_of_findings", False, "reference_not_independent_of_findings"),
    ("findings_locked_before_reference", False, "findings_not_locked_before_reference"),
    ("evaluator_is_adjudicator", True, "self_adjudicated_matches_unconfirmed"),
])
def test_invalid_roles_null_evaluator_recall(field, value, code):
    data = sample(); data["evaluator_validity"][field] = value
    result = calculate_session(Session(**data))
    assert result["metrics"]["reference_set_recall_percent"] is None
    assert code in result["metric_ineligibility_reasons"]["reference_set_recall_percent"]

def test_shared_adjudication_with_independent_confirmation_can_be_eligible():
    data = sample(); data["evaluator_validity"].update(evaluator_is_adjudicator=True, matches_independently_confirmed=True)
    assert calculate_session(Session(**data))["metrics"]["reference_set_recall_percent"] == 62.5

def test_missing_expectation_is_null_but_real_zero_is_zero():
    data = sample(); data["expected_recall_percent"] = None
    result = calculate_session(Session(**data))
    assert result["metrics"]["expected_recall_gap_pp"] is None
    assert "expectation_missing" in result["metric_ineligibility_reasons"]["expected_recall_gap_pp"]
    data["expected_recall_percent"] = 0
    assert calculate_session(Session(**data))["metrics"]["expected_recall_gap_pp"] == -62.5

def test_post_disclosure_judgment_is_excluded_not_erased():
    record = Judgment(**{**row(1, "Ready").model_dump(), "judgment_locked_before_reference": False})
    result = summarize_judgments([record])
    assert result["eligible_instances"] == 0
    assert result["ineligible_instances"] == 1
    assert result["nonready"]["false_ready_acceptance_percent"] is None
    assert result["descriptive_counts"]["nonready"]["counts"]["Ready"] == 1
    assert "judgment_not_locked_before_reference" in result["excluded"][0]["reasons"]

def test_legacy_defaults_are_visible_and_do_not_grant_handoff():
    data = sample(); data.pop("stage"); data.pop("mode")
    data.update(unresolved_critical=0, requirements={"total":1,"verified":1,"failed":0,"unassessed":0},
                recovery={"total":1,"verified":1,"failed":0,"unassessed":0})
    result = calculate_session(Session(**data))
    assert result["criterion_status"] == "unknown"
    assert result["stage"] == "unspecified"
    assert result["mode"] == "legacy_diagnostic"
    assert "Current corrected" in result["compatibility"]


def test_aggregate_runtime_counts_do_not_establish_stage_handoff():
    data = sample(); data.update(stage="runtime_release_review", unresolved_critical=0,
        requirements={"total":1,"verified":1,"failed":0,"unassessed":0},
        recovery={"total":1,"verified":1,"failed":0,"unassessed":0})
    result = calculate_session(Session(**data))
    assert result["stage_handoff_eligibility"] is None
    assert result["criterion_scope"] == "supplied_aggregate_checks"
    assert result["disposition"] == "Aggregate checks satisfied; stage handoff not established"
