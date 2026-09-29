"""Choice evidence is part of the existing six-gate commitment, not a score."""
import copy
import importlib.util
from pathlib import Path

import pytest
from pydantic import ValidationError

from hcai_readiness.contracts import Assessment
from hcai_readiness.engine import assess, requirement_digest, validation_targets
from hcai_readiness.guidance import new_review
from hcai_readiness.reporting import render_report


ROOT = Path(__file__).resolve().parents[1]


def case():
    spec = importlib.util.spec_from_file_location("choice_fixture", ROOT / "examples/make_fixture.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.synthetic_case(ROOT)


def evaluate(data):
    return assess(Assessment.model_validate(data))


def test_engineering_population_required_and_mode_fixed():
    data = case()
    del data["artifact_population"]
    with pytest.raises(ValidationError, match="artifact_population"):
        Assessment.model_validate(data)
    data = case()
    data["mode"] = "artifact_review"
    with pytest.raises(ValidationError, match="mode"):
        Assessment.model_validate(data)
    assert "artifact_population" in Assessment.model_json_schema()["required"]


@pytest.mark.parametrize("role,population", [("artifact_creation", "ai_generated"), ("in_workflow", "runtime_ai"),
                                            ("both", "both"), ("neither", "neither")])
def test_population_matches_scope_role(role, population):
    data = case()
    data["scope"]["ai_role"] = role
    data["artifact_population"] = population
    assert Assessment.model_validate(data).artifact_population == population
    data["artifact_population"] = "runtime_ai" if population != "runtime_ai" else "ai_generated"
    with pytest.raises(ValidationError, match="conflicts"):
        Assessment.model_validate(data)


def test_unknown_population_cannot_qualify_or_be_silently_inferred():
    data = case()
    data["artifact_population"] = "unknown"
    result = evaluate(data)
    assert result["artifact_population"] == "unknown"
    assert result["decision"] != "PROCEED_TO_ENGINEERING"
    assert result["stop_at_gate"] == "G2_NEED_REQUIREMENTS"


def test_new_engineering_review_keeps_unknowns_and_no_invented_choices():
    data = new_review("EMPTY", "2026-09-26T17:00:00-05:00", "human")
    assert data["artifact_population"] == "unknown"
    assert data["mode"] == "engineering_commitment"
    assert data["important_choice_ids"] == data["choice_ledger"] == data["evidence"] == []
    assert all(value is None for value in data["scope"].values())


def test_current_justification_can_retain_choice_without_historical_rationale():
    data = case()
    choice = data["choice_ledger"][0]
    assert choice["rationale_provenance"] == "new"
    assert choice["historical_alternatives"] == choice["rationale_evidence_locations"] == []
    result = evaluate(data)
    assert result["decision"] == "PROCEED_TO_ENGINEERING"
    assert len(result["gates"]) == 6
    assert result["choice_review"]["gaps"] == {}
    assert result["operational_performance"]["deployment_decision"] == "NOT_ASSESSED"
    assert data["evaluator_kind"] == "synthetic"
    assert "Synthetic" in choice["rationale"]


def test_missing_consequential_choice_inventory_or_record_cannot_pass():
    data = case()
    data["important_choice_ids"] = []
    assert evaluate(data)["stop_at_gate"] == "G2_NEED_REQUIREMENTS"
    data = case()
    data["choice_ledger"] = []
    result = evaluate(data)
    assert result["stop_at_gate"] == "G2_NEED_REQUIREMENTS"
    assert result["choice_review"]["gaps"]["CHOICE-SYNTHETIC-1"] == ["important_choice_record_missing"]


@pytest.mark.parametrize("field", ["criteria", "observed_evidence_locations"])
def test_observed_choice_and_decision_criteria_are_required(field):
    data = case()
    data["choice_ledger"][0][field] = []
    result = evaluate(data)
    assert result["stop_at_gate"] == "G2_NEED_REQUIREMENTS"
    assert result["decision"] != "PROCEED_TO_ENGINEERING"


def test_engineering_deepening_maps_model_gaps_to_g3_and_challenges_to_g4():
    data = case()
    data["choice_ledger"][0]["decision_surfaces"][0] = {
        "id": "DS-TRUTH", "kind": "truth", "question": "Which record is authoritative?",
        "status": "unassessed", "evidence_needed": "Inspect persistence ownership"
    }
    result = evaluate(data)
    assert result["stop_at_gate"] == "G3_STATES_RECOVERY"
    data = case()
    data["choice_ledger"][0]["challenge_scenarios"][0].update(
        status="unassessed", evidence_level=None, evidence_locations=[], next_evidence="Run a new bounded walkthrough")
    result = evaluate(data)
    assert result["stop_at_gate"] == "G4_TRACEABILITY"


def test_assumption_lifecycle_maps_unknown_to_g3_and_conflict_to_revise():
    data = case()
    data["choice_ledger"][0]["assumptions"][0].update(status="unassessed", evidence_locations=[])
    result = evaluate(data)
    assert result["stop_at_gate"] == "G3_STATES_RECOVERY"
    data = case()
    data["choice_ledger"][0]["assumptions"][0]["status"] = "conflicted"
    result = evaluate(data)
    assert result["stop_at_gate"] == "G3_STATES_RECOVERY"
    assert result["decision"] == "REVISE"


def test_decision_surface_change_invalidates_exact_revision_validation():
    data = case()
    data["choice_ledger"][0]["decision_surfaces"][0]["current_model"] = "Changed synthetic source of truth"
    result = evaluate(data)
    assert result["stop_at_gate"] == "G4_TRACEABILITY"
    assert any("context changed" in reason for reason in result["gates"][3]["reasons"])


def test_choice_verification_gap_uses_traceability_gate():
    data = case()
    data["choice_ledger"][0]["verification_evidence_locations"] = []
    result = evaluate(data)
    assert result["stop_at_gate"] == "G4_TRACEABILITY"
    assert result["gates"][3]["status"] == "MISSING"


def test_pending_human_choice_and_missing_followup_block_commitment():
    data = case()
    data["choice_ledger"][0].update(human_decision="pending", human_decision_owner=None, follow_up_owner=None)
    result = evaluate(data)
    assert result["stop_at_gate"] == "G6_COMMITMENT"
    assert result["decision"] == "INSUFFICIENT_EVIDENCE"
    assert "human_decision_pending" in result["choice_review"]["gaps"]["CHOICE-SYNTHETIC-1"]


def test_known_choice_revision_remains_visible_after_an_earlier_stop():
    data = case()
    data["baseline"] = {}
    data["choice_ledger"][0]["human_decision"] = "revise"
    result = evaluate(data)
    assert result["stop_at_gate"] == "G1_BASELINE"
    assert result["gates"][5]["status"] == "NOT_EVALUATED"
    assert result["decision"] == "REVISE"
    assert any(item["kind"] == "consequential_choice" for item in result["attention_items"])


@pytest.mark.parametrize("field,value", [
    ("observed_choice", "Changed synthetic behavior"),
    ("criteria", ["Changed synthetic acceptance criterion"]),
    ("rationale", "Changed synthetic current justification"),
    ("impacts_and_tradeoffs", ["Changed synthetic impact"]),
])
def test_choice_context_changes_invalidate_exact_revision_validation(field, value):
    data = case()
    data["choice_ledger"][0][field] = value
    result = evaluate(data)
    assert result["stop_at_gate"] == "G4_TRACEABILITY"
    assert result["decision"] == "REVISE"
    assert any("context changed" in reason for reason in result["gates"][3]["reasons"])
    # Stipulate a new constructed walkthrough for this synthetic scenario only.
    data["workflow"]["validations"][0]["tested_requirement_digests"] = validation_targets(Assessment.model_validate(data))["requirement_digests"]
    assert evaluate(data)["decision"] == "PROCEED_TO_ENGINEERING"


def test_choice_linkage_is_strict_and_unrelated_choice_not_hashed():
    data = case()
    data["choice_ledger"][0]["affected_check_ids"] = ["UNDECLARED"]
    with pytest.raises(ValidationError, match="dangling"):
        Assessment.model_validate(data)
    data = case()
    extra = copy.deepcopy(data["workflow"]["requirements"][0])
    extra["id"] = "R2"
    data["workflow"]["requirements"].append(extra)
    data["choice_ledger"][0]["affected_check_ids"] = ["R2"]
    assessment = Assessment.model_validate(data)
    before = requirement_digest(assessment, assessment.workflow.requirements[0])
    assessment.choice_ledger[0].rationale = "Synthetic change affecting R2 only"
    assert requirement_digest(assessment, assessment.workflow.requirements[0]) == before


def test_report_exposes_provenance_evidence_and_choice_gaps_safely():
    data = case()
    data["choice_ledger"][0].update(human_decision="pending", human_decision_owner=None)
    data["choice_ledger"][0]["rationale"] = "<script>synthetic</script>"
    report = render_report(Assessment.model_validate(data), "html")
    assert "Consequential choices and accountable review" in report
    assert "Rationale provenance: new" in report
    assert "human_decision_pending" in report
    assert "&lt;script&gt;" in report and "<script>" not in report

def test_engineering_deepening_toggle_cannot_erase_existing_failed_challenge():
    data = case()
    data["choice_ledger"][0]["challenge_scenarios"][0]["status"] = "fail"
    data["choice_ledger"][0]["engineering_deepening_required"] = False
    result = evaluate(data)
    assert result["decision"] == "REVISE"
    assert result["stop_at_gate"] in ("G3_STATES_RECOVERY", "G4_TRACEABILITY")
    assert any("bounded challenge disconfirmed" in reason for gate in result["gates"] for reason in gate["reasons"])

