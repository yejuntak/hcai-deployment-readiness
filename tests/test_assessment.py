import json
from pathlib import Path
import pytest
from pydantic import ValidationError
from hcai_readiness.assessment import Session, Judgment, calculate_session, summarize_judgments

ROOT = Path(__file__).resolve().parents[1]

def sample():
    return json.loads((ROOT / "examples/session.json").read_text())

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
    assert calculate_session(Session(**d))["disposition"]=="Eligible for handoff review"

def row(i,j,status="nonready",kind="synthetic"):
    return Judgment(instance_id=str(i),artifact_version="v1",criterion_version="c1",evaluator_kind=kind,criterion_status=status,judgment=j)

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
