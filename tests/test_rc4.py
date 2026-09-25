import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError
from hcai_readiness.contracts import Assessment, FeedbackEntry, PilotRun
from hcai_readiness.engine import assess
from hcai_readiness.records import public_feedback, release_readiness
from hcai_readiness.versions import versions

ROOT = Path(__file__).resolve().parents[1]


def fixture(name="low-risk-quick"):
    return json.loads((ROOT / "examples/rc4" / f"{name}.json").read_text())


def evaluate(data):
    return assess(Assessment.model_validate(data))


def test_polished_without_baseline_cannot_proceed():
    r = evaluate(fixture("polished-no-baseline"))
    assert r["decision"] == "INSUFFICIENT_EVIDENCE"
    assert r["stop_at_gate"] == "G1_BASELINE"
    assert all(g["status"] == "NOT_EVALUATED" for g in r["gates"][1:])
    assert r["roi"]["status"] == "INDETERMINATE"
    assert r["roi"]["net_operational_benefit_per_period"] is None


def test_documentation_pass_never_claims_operational_performance():
    r = evaluate(fixture("documentation-no-operational-evidence"))
    assert r["decision"] == "PROCEED_TO_ENGINEERING"
    assert r["decision_scope"] == "bounded_engineering_commitment"
    assert r["operational_performance"]["metrics"] == {}
    assert r["operational_performance"]["deployment_decision"] == "NOT_ASSESSED"
    assert r["handoff_record"]["owner_authorization"] == "PENDING_SEPARATE_RECORDED_DECISION"


def test_prototype_without_traceability_revises():
    r = evaluate(fixture("prototype-no-traceability"))
    assert r["decision"] == "REVISE"
    assert r["stop_at_gate"] == "G4_TRACEABILITY"


def test_low_risk_quick_is_sufficient():
    r = evaluate(fixture())
    assert r["decision"] == "PROCEED_TO_ENGINEERING"
    assert r["required_profile"] == "QUICK6"
    assert not r["escalation_required"]
    assert len(r["gates"]) == 6
    assert all(g["status"] == "PASS" for g in r["gates"])


def test_higher_risk_escalates_and_requires_deeper_evidence():
    r = evaluate(fixture("high-risk-quick"))
    assert r["risk_tier"] == "high"
    assert r["escalation_required"] and r["required_profile"] == "FULL"
    assert r["decision"] == "INSUFFICIENT_EVIDENCE"
    assert evaluate(fixture("high-risk-full"))["decision"] == "PROCEED_TO_ENGINEERING"
    d = fixture("high-risk-full")
    d["handoff"]["hazard_analysis"] = {}
    assert evaluate(d)["decision"] == "INSUFFICIENT_EVIDENCE"


def test_gross_savings_can_be_erased_by_oversight():
    r = evaluate(fixture("savings-erased"))
    assert r["roi"]["gross_minutes_saved_per_case"] == 15
    assert r["roi"]["oversight_minutes_per_case"] == 15
    assert r["roi"]["net_minutes_saved_per_case"] == 0
    assert r["roi"]["net_operational_benefit_per_period"] == -30
    assert r["roi"]["recurring_roi_percent"] < 0
    assert r["roi"]["payback_periods"] is None


def test_evaluation_expense_is_separate():
    base, expensive = evaluate(fixture()), evaluate(fixture("expensive-evaluation"))
    assert expensive["evaluator_burden"]["protocol_evaluation_cost"] == 740
    assert expensive["evaluator_burden"]["total_person_minutes"] == 360
    assert expensive["roi"] == base["roi"]
    assert expensive["operational_performance"] == base["operational_performance"]


def test_missing_recovery_stops_quick():
    r = evaluate(fixture("missing-recovery"))
    assert r["decision"] == "INSUFFICIENT_EVIDENCE"
    assert r["stop_at_gate"] == "G3_STATES_RECOVERY"
    assert all(g["status"] == "NOT_EVALUATED" for g in r["gates"][3:])


def feedback(permission="private"):
    return FeedbackEntry(id="FBTEST", source_person="PRIVATE_NAME_SENTINEL", source_date="2026-09-01",
                         recorded_on="2026-09-24", context="PRIVATE_CONTEXT_SENTINEL", feedback="PRIVATE_FEEDBACK_SENTINEL",
                         permission=permission, permission_basis="PRIVATE_PERMISSION_SENTINEL", changes=["C01"],
                         affected_files=["protocol/0.2-preview.1/PROTOCOL.md"], affected_requirements=["G6_COMMITMENT"],
                         validation_status="software_tests_only")


def test_feedback_permission_export():
    exported = json.dumps(public_feedback([feedback()]))
    assert "PRIVATE_" not in exported
    assert "2026-09-01" not in exported
    approved = public_feedback([feedback("attribution_approved")])[0]
    assert approved["source_person"] == "PRIVATE_NAME_SENTINEL"
    assert "permission_basis" not in approved
    ledger = json.loads((ROOT / "evidence/feedback-ledger.public.json").read_text())
    assert len(ledger) == 5
    assert [x["source_person"] for x in ledger if x["source_person"]] == ["Hillel Glazer"]
    assert all(x["feedback"] is None for x in ledger if x["permission"] == "private")


def test_pilot_exact_versions_and_provenance():
    p = PilotRun.model_validate(fixture("pilot-synthetic"))
    assert p.assessment.versions.model_dump() == versions()
    assert all(len(e.sha256) == 64 and e.version and e.locator for e in p.assessment.evidence)
    bad = p.model_dump()
    del bad["assessment"]["versions"]["skill"]
    with pytest.raises(ValidationError):
        PilotRun.model_validate(bad)
    bad = p.model_dump()
    bad["assessment"]["evidence"][0]["sha256"] = "unknown"
    with pytest.raises(ValidationError):
        PilotRun.model_validate(bad)
    bad = p.model_dump()
    bad["gates_passed"] = []
    with pytest.raises(ValidationError):
        PilotRun.model_validate(bad)


def test_synthetic_pilot_cannot_unlock_release():
    p = PilotRun.model_validate(fixture("pilot-synthetic"))
    result = release_readiness([p], regression_passed=True)
    assert result["status"] == "REMAIN_CANDIDATE"
    assert result["eligible_pilot_ids"] == []
    assert not result["automatic_promotion"]
    bad = p.model_dump()
    bad.update(external_participant=True, actual_bounded_use=True)
    with pytest.raises(ValidationError):
        PilotRun.model_validate(bad)


@pytest.mark.parametrize("field", ["complexity", "importance", "impact", "mission", "failure_consequence", "irreversibility"])
def test_each_risk_dimension_changes_depth(field):
    d = fixture()
    d["risk"][field] = "moderate"
    assert evaluate(d)["required_profile"] == "FULL"
    d["risk"][field] = None
    assert evaluate(d)["risk_tier"] == "unknown"
    assert evaluate(d)["decision"] != "PROCEED_TO_ENGINEERING"


def test_depth_changes_baseline_and_need_thresholds():
    d = fixture("high-risk-full")
    d["baseline"]["sample_size"] = 4
    assert evaluate(d)["gates"][0]["status"] == "MISSING"
    d = fixture("high-risk-full")
    d["workflow"]["needs"][0]["source_ids"] = ["E2"]
    assert evaluate(d)["gates"][1]["status"] == "MISSING"
    d = fixture("high-risk-full")
    d["workflow"]["needs"][0]["discussion_evidence_ids"] = []
    assert evaluate(d)["gates"][1]["status"] == "MISSING"


def test_no_self_declared_independent_review():
    d = fixture("high-risk-full")
    d["handoff"]["independent_review"]["independent_from_artifact_owner"] = False
    assert evaluate(d)["decision"] == "INSUFFICIENT_EVIDENCE"


def test_quick_time_limit_is_enforced():
    d = fixture()
    d["evaluator_burden"]["elapsed_minutes"] = 15
    assert evaluate(d)["decision"] == "PROCEED_TO_ENGINEERING"
    d["evaluator_burden"]["elapsed_minutes"] = 15.01
    assert evaluate(d)["decision"] == "INSUFFICIENT_EVIDENCE"
    assert evaluate(d)["required_profile"] == "FULL"


@pytest.mark.parametrize("value", [-1, True, "12", float("nan"), float("inf")])
def test_invalid_numeric_evidence_rejected(value):
    d = fixture()
    d["baseline"]["labor_minutes_per_case"] = value
    with pytest.raises(ValidationError):
        Assessment.model_validate(d)


def test_dangling_duplicate_and_mislinked_traceability():
    d = fixture()
    d["workflow"]["requirements"][0]["artifact_ids"] = ["missing"]
    with pytest.raises(ValidationError):
        Assessment.model_validate(d)
    d = fixture()
    d["evidence"].append(copy.deepcopy(d["evidence"][0]))
    with pytest.raises(ValidationError):
        Assessment.model_validate(d)
    d = fixture()
    d["workflow"]["validations"][0]["artifact_ids"] = ["E2"]
    d["workflow"]["validations"][0]["tested_artifact_digests"] = {"E2": d["evidence"][1]["sha256"]}
    assert evaluate(d)["decision"] == "REVISE"


def test_test_plan_is_not_executed_evidence():
    d = fixture()
    d["workflow"]["validations"][0]["level"] = "specified"
    assert evaluate(d)["decision"] == "INSUFFICIENT_EVIDENCE"


def test_duplicate_source_bytes_do_not_meet_multisource_threshold():
    d = fixture("high-risk-full")
    d["evidence"][2]["sha256"] = d["evidence"][1]["sha256"]
    assert evaluate(d)["gates"][1]["status"] == "MISSING"


def test_unassessed_additional_validation_cannot_be_averaged_away():
    d = fixture()
    extra = copy.deepcopy(d["workflow"]["validations"][0])
    extra.update(id="T2", status="missing")
    d["workflow"]["validations"].append(extra)
    assert evaluate(d)["decision"] == "INSUFFICIENT_EVIDENCE"


def test_measured_oversight_cannot_be_claimed_upstream():
    d = fixture()
    d["operational_oversight"]["basis"] = "measured"
    with pytest.raises(ValidationError):
        Assessment.model_validate(d)


def test_important_artifacts_and_reference_material_cannot_be_omitted():
    d = fixture()
    d["workflow"]["important_artifact_ids"].append("E2")
    assert evaluate(d)["decision"] == "REVISE"
    d = fixture()
    d["workflow"]["requirements"][0]["reference_material_ids"] = []
    assert evaluate(d)["decision"] == "REVISE"  # Missing reference AND stale recorded validation.


def test_critical_failure_cannot_be_waived_or_averaged():
    d = fixture()
    d["handoff"]["reviewer_findings"] = [{"id": "F1", "severity": "critical", "status": "accepted",
                                           "description": "Unresolved critical consequence", "evidence_ids": ["E1"]}]
    assert evaluate(d)["decision"] == "REVISE"


def test_full_failure_precedes_missing_evidence():
    d = fixture("polished-no-baseline")
    d["requested_profile"] = "FULL"
    d["workflow"]["validations"][0]["status"] = "fail"
    r = evaluate(d)
    assert r["decision"] == "REVISE"
    assert r["gates"][0]["status"] == "MISSING"
    assert r["gates"][3]["status"] == "FAIL"


def test_assumed_baseline_is_not_measured():
    d = fixture()
    d["evidence"][1]["kind"] = "estimate"
    r = evaluate(d)
    assert r["decision"] == "INSUFFICIENT_EVIDENCE"
    assert r["roi"]["status"] == "INDETERMINATE"


def test_unknown_money_does_not_become_zero():
    d = fixture()
    d["costs"]["labor_cost_per_hour"] = None
    d["evaluator_burden"]["tool_model_cost"] = None
    r = evaluate(d)
    assert r["roi"]["status"] == "TIME_ONLY"
    assert r["roi"]["net_minutes_saved_per_case"] == 10
    assert r["roi"]["recurring_roi_percent"] is None
    assert r["evaluator_burden"]["protocol_evaluation_cost"] is None


def test_missing_oversight_blocks_and_roi_indeterminate():
    d = fixture()
    d["operational_oversight"]["correction_minutes_per_case"] = None
    r = evaluate(d)
    assert r["stop_at_gate"] == "G5_OVERSIGHT"
    assert r["roi"]["status"] == "INDETERMINATE"


def test_cost_and_cycle_time_units():
    r = evaluate(fixture())
    assert r["roi"]["gross_minutes_saved_per_case"] == 15  # labor 20, not elapsed 30
    assert r["roi"]["baseline_operating_cost_per_period"] == 1000
    assert r["roi"]["proposed_operating_cost_per_period"] == 530
    assert r["roi"]["net_operational_benefit_per_period"] == 470
    assert r["evaluator_burden"]["protocol_evaluation_cost"] == 12


def test_operational_claims_require_actual_context():
    d = fixture()
    d["operational_performance"]["metrics"] = {"accuracy": 0.9}
    with pytest.raises(ValidationError):
        Assessment.model_validate(d)
    d["operational_performance"].update(status="collected_after_implementation", implemented_version="fictional-1",
                                        realistic_use_context="Synthetic scenario only", evidence_ids=["E1"])
    r = evaluate(d)
    assert r["operational_performance"]["deployment_decision"] == "NOT_ASSESSED"


def test_synthetic_evidence_cannot_be_relabelled_human():
    d = fixture()
    d["evaluator_kind"] = "human"
    with pytest.raises(ValidationError):
        Assessment.model_validate(d)


def test_generated_parity_and_json_schemas():
    subprocess.run([sys.executable, "scripts/build_candidate_assets.py", "--check"], cwd=ROOT, check=True)
    schema = json.loads((ROOT / "schemas/assessment.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    for path in (ROOT / "examples/rc4").glob("*.json"):
        data = json.loads(path.read_text())
        if path.stem == "pilot-synthetic":
            pilot_schema = json.loads((ROOT / "schemas/pilot-run.schema.json").read_text())
            Draft202012Validator(pilot_schema).validate(data)
        else:
            Draft202012Validator(schema).validate(data)
            output_schema = json.loads((ROOT / "schemas/assessment-result.schema.json").read_text())
            Draft202012Validator(output_schema).validate(evaluate(data))


def test_portable_skill_matches_engine_all_fixtures(tmp_path):
    import shutil
    portable = tmp_path / "ai-ready"
    shutil.copytree(ROOT / "skills/ai-ready", portable)
    for path in (ROOT / "examples/rc4").glob("*.json"):
        if path.stem == "pilot-synthetic":
            continue
        proc = subprocess.run([sys.executable, str(portable / "scripts/assess.py"), str(path)],
                              cwd=tmp_path, capture_output=True, text=True, check=True)
        assert json.loads(proc.stdout) == evaluate(json.loads(path.read_text()))


def test_baseline_history_is_byte_frozen():
    manifest = json.loads((ROOT / "historical/baseline-manifest.json").read_text())
    for name, digest in manifest["files"].items():
        assert hashlib.sha256((ROOT / "historical/rc3-baseline" / name).read_bytes()).hexdigest() == digest, name
    for tag, commit in manifest["historical_tags"].items():
        assert subprocess.check_output(["git", "rev-parse", f"{tag}^{{commit}}"], cwd=ROOT, text=True).strip() == commit


def test_change_manifest_maps_to_existing_tests_and_files():
    manifest = json.loads((ROOT / "evidence/change-manifest.json").read_text())
    schema = json.loads((ROOT / "schemas/change-manifest.schema.json").read_text())
    Draft202012Validator(schema).validate(manifest)
    test_text = "\n".join(p.read_text() for p in (ROOT / "tests").glob("test_*.py"))
    for change in manifest["changes"]:
        assert all((ROOT / path).exists() for path in change["files"])
        assert all(f"def {test}(" in test_text for test in change["acceptance_tests"])
