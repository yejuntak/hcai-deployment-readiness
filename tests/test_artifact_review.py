"""Invariant tests for practical artifact review, not evidence of protocol efficacy."""
import pytest
from pydantic import ValidationError
from hcai_readiness.artifact_review import ArtifactReview, ChoiceRecord, review_artifact
from hcai_readiness.versions import versions


def check(id):
    return {"id": id, "acceptance_check": "Timeout preserves the user's draft and offers a retry",
            "specified": {"status": "pass", "evidence_locations": ["spec.md#timeout"]},
            "walkthrough": {"status": "pass", "evidence_locations": ["walkthrough.md#timeout"]}}


def choice():
    return {"id": "C1", "purpose": "Preserve work after the upstream service times out",
            "criteria": ["No user draft loss", "Explicit retry without duplicate submission"],
            "observed_choice": "Keep draft locally until response confirmation",
            "observed_evidence_locations": ["spec.md#draft"],
            "historical_alternatives": [],
            "proposed_alternatives": [{"description": "Persist encrypted draft server-side"}],
            "rationale": "Local draft retention avoids coupling recovery to the unavailable server",
            "rationale_provenance": "new", "impacts_and_tradeoffs": ["Device loss requires separate recovery"],
            "assumptions": [{"id": "A1",
                             "statement": "Stable request identity prevents duplicate submission after timeout",
                             "status": "supported",
                             "consequence_if_false": "A retry can create a duplicate submission",
                             "evidence_needed": "Execute duplicate-retry coverage after implementation",
                             "evidence_locations": ["walkthrough.md#draft-recovery"],
                             "revisit_trigger": "Retry or request-identity behavior changes"}],
            "affected_check_ids": ["R1", "RC1"],
            "engineering_deepening_required": True,
            "deepening_rationale": "Draft persistence and timeout recovery depend on state, truth and retry assumptions.",
            "deepening_triggers": ["persistent_state_mutation", "unreliable_or_async_dependency"],
            "required_surface_kinds": ["truth", "state"],
            "decision_surfaces": [
                {"id": "D1", "kind": "truth", "question": "Which draft is authoritative?",
                 "current_model": "The local draft is authoritative until response confirmation", "status": "supported",
                 "evidence_locations": ["spec.md#draft"]},
                {"id": "D2", "kind": "state", "question": "What state follows a timeout?",
                 "current_model": "The draft remains editable and unsubmitted", "status": "supported",
                 "evidence_locations": ["walkthrough.md#timeout"]},
            ],
            "challenge_scenarios": [
                {"id": "CH1", "condition": "The upstream response times out and the user retries",
                 "claim_at_risk": "Recovery does not duplicate submission",
                 "expected_behavior_or_invariant": "One logical request produces at most one accepted submission",
                 "consequence_if_mishandled": "Duplicate request", "affected_check_ids": ["R1", "RC1"],
                 "status": "pass", "evidence_level": "walkthrough", "evidence_locations": ["walkthrough.md#draft-recovery"]}
            ],
            "next_coherent_slice": "Implement one timeout/retry path through stable request identity and preserved draft state.",
            "human_decision": "accepted",
            "human_decision_owner": "Fictional product owner",
            "human_decision_evidence_locations": ["synthetic-owner-review.md#C1"],
            "verification_evidence_locations": ["walkthrough.md#draft-recovery"],
            "follow_up": "Run fault-injection on the implemented flow", "follow_up_owner": "Fictional engineering owner"}


def fixture():
    return {"versions": versions(), "run_id": "synthetic-plan-1", "artifact_version": "spec-v1",
            "criterion_version": "plan-checks-v1", "artifact_population": "runtime_ai",
            "artifact_kind": "specification", "stage": "specification_handoff", "mode": "artifact_review",
            "evaluator_kind": "synthetic", "criteria_timing": "retrospective",
            "requirements": [check("R1")], "recovery": [check("RC1")],
            "important_choice_ids": ["C1"], "choices": [choice()]}


def test_plan_can_reach_declared_handoff_without_code_or_runtime_claim():
    result = review_artifact(ArtifactReview(**fixture()))
    assert result["criterion_status"] == "ready"
    assert result["required_evidence_levels"] == ["specified", "walkthrough"]
    assert result["requirements"]["evidence_levels"]["implemented"]["unassessed"] == 1
    assert result["requirements"]["evidence_levels"]["runtime_tested"]["coverage_percent"] == 0
    assert all(value is None for value in result["evaluator_metrics"].values())
    assert "release" in result["interpretation"]


def test_unassessed_required_scenario_stays_in_denominator():
    data = fixture()
    data["recovery"].append({"id": "RC2", "acceptance_check": "Handle upstream outage"})
    result = review_artifact(ArtifactReview(**data))
    assert result["recovery"]["total"] == 2
    assert result["recovery"]["unassessed"] == 1
    assert result["recovery"]["coverage_percent"] == 50
    assert result["disposition"] == "Insufficient evidence"


def test_inspected_absence_is_failure_not_unassessed():
    data = fixture()
    data["recovery"][0]["specified"] = {"status": "fail", "evidence_locations": ["spec.md#inspected-absence"]}
    result = review_artifact(ArtifactReview(**data))
    assert result["recovery"]["failed"] == 1
    assert result["recovery"]["unassessed"] == 0
    assert result["disposition"] == "Hold for remediation"


def test_four_evidence_levels_are_independent():
    data = fixture()
    data["requirements"][0]["runtime_tested"] = {"status": "pass", "evidence_locations": ["runtime-log#1"]}
    data["requirements"][0]["specified"] = {"status": "unassessed"}
    result = review_artifact(ArtifactReview(**data))
    assert result["requirements"]["evidence_levels"]["runtime_tested"]["pass"] == 1
    assert result["requirements"]["evidence_levels"]["specified"]["unassessed"] == 1
    assert result["criterion_status"] == "nonready"


def test_plan_cannot_claim_runtime_release_even_with_supplied_passes():
    data = fixture()
    data["stage"] = "runtime_release_review"
    for row in data["requirements"] + data["recovery"]:
        for level in ("implemented", "runtime_tested"):
            row[level] = {"status": "pass", "evidence_locations": ["alleged-execution#1"]}
    result = review_artifact(ArtifactReview(**data))
    assert result["criterion_status"] == "nonready"
    assert "implemented_artifact_required_for_selected_stage" in result["evidence_gaps"]


def test_not_applicable_cannot_remove_required_stage_check():
    data = fixture()
    data["requirements"][0]["walkthrough"] = {"status": "not_applicable", "reason": "No time available"}
    result = review_artifact(ArtifactReview(**data))
    assert result["requirements"]["total"] == 1
    assert result["requirements"]["coverage_percent"] == 0
    assert result["criterion_status"] == "nonready"


@pytest.mark.parametrize("mutation", [
    lambda d: d.pop("artifact_population"),
    lambda d: d.pop("stage"),
    lambda d: d.pop("mode"),
    lambda d: d.pop("versions"),
    lambda d: d["versions"].update(protocol="stale-version"),
    lambda d: d.update(unexpected=True),
    lambda d: d["requirements"][0]["specified"].update(evidence_locations=[]),
    lambda d: d["choices"][0].update(human_decision_evidence_locations=[]),
])
def test_strict_inputs_and_evidence(mutation):
    data = fixture()
    mutation(data)
    with pytest.raises(ValidationError):
        ArtifactReview(**data)


def test_unknown_population_is_visible_and_ineligible_for_handoff():
    data = fixture(); data["artifact_population"] = "unknown"
    result = review_artifact(ArtifactReview(**data))
    assert result["criterion_status"] == "nonready"
    assert result["artifact_population"] == "unknown"


def test_missing_important_choice_or_human_pending_prevents_handoff():
    data = fixture(); data["important_choice_ids"].append("C2")
    result = review_artifact(ArtifactReview(**data))
    assert result["choice_issues"]["C2"] == ["important_choice_record_missing"]
    data = fixture(); data["choices"][0]["human_decision"] = "pending"
    result = review_artifact(ArtifactReview(**data))
    assert result["disposition"] == "Insufficient evidence"
    assert "human_decision_pending" in result["choice_issues"]["C1"]


def test_new_rationale_is_not_recorded_history():
    data = choice()
    assert ChoiceRecord(**data).rationale_provenance == "new"
    data["rationale_provenance"] = "documented"
    with pytest.raises(ValidationError): ChoiceRecord(**data)
    data["rationale_provenance"] = "unknown"
    with pytest.raises(ValidationError): ChoiceRecord(**data)
    data = choice(); data["historical_alternatives"] = data.pop("proposed_alternatives")
    with pytest.raises(ValidationError): ChoiceRecord(**data)


def test_current_justification_can_be_new_without_inventing_historical_alternatives():
    result = review_artifact(ArtifactReview(**fixture()))
    assert result["choices"][0]["historical_alternatives"] == []
    assert result["choices"][0]["rationale_provenance"] == "new"
    assert result["criterion_status"] == "ready"


def test_unassessed_decision_surface_is_insufficient_and_conflict_holds():
    data = fixture()
    data["choices"][0]["decision_surfaces"][0] = {
        "id": "D1", "kind": "truth", "question": "Which draft is authoritative?",
        "status": "unassessed", "evidence_needed": "Inspect persistence ownership"
    }
    result = review_artifact(ArtifactReview(**data))
    assert result["disposition"] == "Insufficient evidence"
    assert "decision_surface_D1_unassessed" in result["choice_issues"]["C1"]
    data = fixture()
    data["choices"][0]["decision_surfaces"][0]["status"] = "conflicted"
    data["choices"][0]["decision_surfaces"][0]["current_model"] = "Local draft is authoritative"
    data["choices"][0]["decision_surfaces"][0]["evidence_locations"] = ["spec.md#conflict"]
    result = review_artifact(ArtifactReview(**data))
    assert result["disposition"] == "Hold for remediation"
    assert result["deepening_failure_ids"] == ["C1"]


def test_failed_challenge_holds_and_generated_reason_cannot_erase_it():
    data = fixture()
    data["choices"][0]["challenge_scenarios"][0]["status"] = "fail"
    result = review_artifact(ArtifactReview(**data))
    assert result["disposition"] == "Hold for remediation"
    assert "challenge_CH1_failed" in result["choice_issues"]["C1"]


def test_choice_revision_holds_even_with_complete_checks():
    data = fixture(); data["choices"][0]["human_decision"] = "revise"
    result = review_artifact(ArtifactReview(**data))
    assert result["disposition"] == "Hold for remediation"


def test_deferred_phase_is_explicit_but_cannot_hide_current_dependency():
    data = fixture()
    data["requirements"].append({"id": "PHASE3", "acceptance_check": "Later analytics export",
                                "scope": "deferred", "exclusion_reason": "Versioned Phase 3 scope"})
    result = review_artifact(ArtifactReview(**data))
    assert result["requirements"]["total"] == 1
    assert result["requirements"]["excluded_ids"] == ["PHASE3"]
    assert result["criterion_status"] == "ready"
    data["requirements"][1]["current_dependency"] = True
    with pytest.raises(ValidationError): ArtifactReview(**data)


def test_disclaimer_omission_does_not_automatically_establish_critical():
    data = fixture()
    data["findings"] = [{"id": "F01", "description": "Disclaimer absent", "acceptance": "novel_accepted",
                         "proposed_severity": "critical", "criterion_or_novel_risk": "Review unsupported medical claims",
                         "evidence_locations": ["spec.md#output"], "adjudicated_severity": "undetermined"}]
    result = review_artifact(ArtifactReview(**data))
    assert result["unresolved_critical_ids"] == []
    assert result["finding_scope_or_adjudication_gaps"] == ["F01"]
    data["findings"][0]["adjudicated_severity"] = "critical"
    with pytest.raises(ValidationError): ArtifactReview(**data)


def test_novel_accepted_critical_changes_disposition_not_reference_denominator():
    data = fixture()
    data["findings"] = [{"id": "F1", "description": "Unsafe default action", "acceptance": "novel_accepted",
                         "criterion_or_novel_risk": "Unauthenticated actuation", "evidence_locations": ["spec.md#actuation"],
                         "adjudicated_severity": "critical", "failure_mechanism": "Unauthenticated request activates machine",
                         "consequence": "Physical injury", "resolution": "accepted_risk"}]
    result = review_artifact(ArtifactReview(**data))
    assert result["unresolved_critical_ids"] == ["F1"]
    assert result["disposition"] == "Hold for remediation"
    assert result["requirements"]["total"] == 1
    assert result["evaluator_metrics"]["reference_set_recall_percent"] is None


def test_zero_recovery_requires_reason_and_is_null():
    data = fixture(); data["recovery"] = []
    data["choices"][0]["affected_check_ids"] = ["R1"]
    data["choices"][0]["challenge_scenarios"][0]["affected_check_ids"] = ["R1"]
    with pytest.raises(ValidationError): ArtifactReview(**data)
    data["zero_recovery_reason"] = "Bounded static copy review has no transitions or recoverable state"
    result = review_artifact(ArtifactReview(**data))
    assert result["recovery"]["coverage_percent"] is None


def test_accepted_open_major_finding_cannot_be_overridden_by_positive_matrix():
    data = fixture()
    data["findings"] = [{"id":"F1", "description":"Required action cannot be completed",
                         "acceptance":"novel_accepted", "adjudicated_severity":"major",
                         "criterion_or_novel_risk":"R1 mandatory acceptance check",
                         "evidence_locations":["walkthrough.md#failure"]}]
    result = review_artifact(ArtifactReview(**data))
    assert result["requirements"]["verified"] == 1
    assert result["disposition"] == "Hold for remediation"
    assert result["unresolved_major_ids"] == ["F1"]
