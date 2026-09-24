"""Constructed acceptance input. Never label these values as actual observations."""
import hashlib
from pathlib import Path
from hcai_readiness.versions import versions
from hcai_readiness.contracts import Assessment
from hcai_readiness.engine import validation_targets, IMPACT_DOMAINS


def synthetic_case(root: Path):
    evidence = []
    for id, name in (("E1", "synthetic-workflow.md"), ("E2", "synthetic-observation.md"), ("E3", "synthetic-discussion.md")):
        path = root / "examples/evidence" / name
        evidence.append({"id": id, "version": "fixture-1", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                         "locator": f"examples/evidence/{name}", "kind": "synthetic", "description": "Constructed test evidence; no actual use",
                         "origin_id": "FICTIONAL-ORIGIN-" + id,
                         "source_type": {"E1": "artifact", "E2": "work_record", "E3": "end_user_discussion"}[id]})
    check = {"status": "pass", "evidence_ids": ["E1"], "note": "Stipulated synthetic review for software tests"}
    data = {
        "run_id": "SYNTHETIC-LOW-001", "recorded_at": "2026-09-24T12:00:00-05:00", "versions": versions(),
        "evaluator_kind": "synthetic", "requested_profile": "QUICK6", "evidence": evidence,
        "scope": {"workflow_name": "Fictional advisor intake", "unit_of_work": "one intake request",
                  "starts_when": "Request received", "ends_when": "Advisor confirms or cancels the request",
                  "environment": "Fictional office; no live sending", "ai_role": "in_workflow",
                  "alternatives_considered": ["Retain current manual intake", "Use a non-AI form with field checks"],
                  "exclusions": ["No autonomous customer messages"], "affected_roles": ["intake advisor", "requester"]},
        "baseline": {"current_state_summary": "Intake → advisor review → correction or confirmation", "actor_roles": ["intake advisor", "intake lead"],
                     "entry_step_id": "C1", "map_review": dict(check),
                     "steps": [
                         {"id": "C1", "kind": "normal", "actor_role": "intake advisor", "trigger": "Request received", "action": "Read and check intake", "data_handling": "Keep original fields", "next_step_ids": ["C2", "C4"], "terminal": False, "evidence_ids": ["E2"], "observation_status": "observed"},
                         {"id": "C2", "kind": "edge", "actor_role": "intake advisor", "trigger": "Field missing", "action": "Ask for correction", "data_handling": "Keep original fields", "next_step_ids": ["C3"], "terminal": False, "evidence_ids": ["E2"], "observation_status": "reported"},
                         {"id": "C3", "kind": "recovery", "actor_role": "intake advisor", "trigger": "Correction received or request cancelled", "action": "Correct saved fields or retain cancelled record", "data_handling": "No silent overwrite", "next_step_ids": ["C4"], "terminal": False, "evidence_ids": ["E2"], "observation_status": "reported"},
                         {"id": "C4", "kind": "normal", "actor_role": "intake lead", "trigger": "Review finished", "action": "Confirm or close intake", "data_handling": "Retain review record", "next_step_ids": [], "terminal": True, "evidence_ids": ["E2"], "observation_status": "observed"}],
                     "observation_window": "Fictional five-case window", "sample_size": 5,
                     "cycle_minutes_per_case": 30, "labor_minutes_per_case": 20, "handoffs_per_case": 1,
                     "touches_per_case": 3, "failure_points": ["Missing contact field"], "manual_review_minutes_per_case": 2,
                     "escalation_minutes_per_case": 1, "rework_minutes_per_case": 1,
                     "volume_per_period": 100, "period": "month", "evidence_ids": ["E2"]},
        "risk": {**{key: "low" for key in ("complexity", "importance", "impact", "mission", "failure_consequence", "irreversibility")},
                 "context": {"safety_or_rights_impact": False, "irreversible_external_actions": False,
                             "sensitive_data": False, "untrusted_input_to_actions": False},
                 "rationale": "Constructed reversible, low-consequence intake draft with human approval", "evidence_ids": ["E1"]},
        "workflow": {"outcome": "Reduce repetitive entry without losing advisor control", "entry_state_id": "S1",
            "impact_reviews": [{"domain": domain, "applicability": "applicable", "owner_role": "intake lead",
                                "affected_roles": ["intake advisor", "requester"], "requirement_ids": ["R1"], "evidence_ids": ["E1"],
                                "rationale": "Stipulated synthetic case: readable editable drafts, equal correction access, local fictional data, advisor control. Not empirical evidence."} for domain in IMPACT_DOMAINS],
            "needs": [{"id": "N1", "description": "Preserve contact details", "end_user_role": "intake advisor",
                       "source_ids": ["E2", "E3"], "discussion_evidence_ids": ["E3"]}],
            "requirements": [{"id": "R1", "description": "Correct or cancel without data loss", "acceptance_criteria": "All three paths preserve the defined fields",
                              "form": "Review form with editable fields", "fit": "Advisor intake workflow and email dependency", "function": "Preserve details through correction/cancel",
                              "reference_material_ids": ["E1"],
                              "owner_role": "intake lead", "need_ids": ["N1"], "artifact_ids": ["E1"], "validation_ids": ["T1"], "behavior_status": "simulated"}],
            "states": [{"id": f"S{i}", "kind": kind, "trigger": trigger, "behavior": behavior, "resulting_state": state,
                        "data_handling": "Preserve entered contact details", "owner_role": "intake advisor", "requirement_ids": ["R1"], "evidence_ids": ["E1"],
                        "next_state_ids": {1:["S2", "S4"], 2:["S3"], 3:["S4"], 4:[]}[i], "terminal": i == 4}
                       for i, (kind, trigger, behavior, state) in enumerate([
                           ("normal", "Draft available", "Review request", "Confirmed"),
                           ("edge", "Contact detail missing", "Flag missing field", "Correction required"),
                           ("recovery", "Advisor corrects or cancels", "Retain corrected or cancelled intake", "Ready to close"),
                           ("normal", "Advisor confirms outcome", "Close with retained record", "Confirmed or cancelled")], 1)],
            "important_artifact_ids": ["E1"],
            "validations": [{"id": "T1", "requirement_ids": ["R1"], "artifact_ids": ["E1"], "method": "Stipulated three-path walkthrough",
                             "level": "walkthrough", "status": "pass", "evidence_ids": ["E1"], "tested_artifact_digests": {"E1": evidence[0]["sha256"]}}],
            "dependencies": ["email system"], "dependency_review": dict(check), "state_review": dict(check),
            "human_control_review": dict(check), "action_boundaries": ["Draft only; advisor approves changes; no sending or external data access"]},
        "operational_oversight": {"basis": "estimate", "review_minutes_per_case": 2, "correction_minutes_per_case": 1,
             "escalation_minutes_per_case": 1, "rework_minutes_per_case": 1, "residual_manual_minutes_per_case": 5,
             "owner_role": "intake lead", "evidence_ids": ["E1"]},
        "costs": {"currency": "USD", "labor_cost_per_hour": 30, "baseline_nonlabor_cost_per_period": 0,
                  "proposed_recurring_fixed_cost_per_period": 20, "proposed_nonlabor_cost_per_case": 0.1,
                  "one_time_implementation_cost": 1000, "evidence_ids": ["E1"]},
        "evaluator_burden": {"elapsed_minutes": 12, "evaluator_minutes": 12, "participant_minutes": 12,
             "preparation_elapsed_minutes": 0, "preparation_person_minutes": 0, "capture_reporting_minutes": 2,
             "participant_count": 1, "adjudication_minutes": 0, "review_correction_cycles": 0,
             "tool_calls": 1, "model_calls": 0, "input_tokens": 0, "output_tokens": 0, "tool_model_cost": 0,
             "labor_cost_per_hour": 30, "currency": "USD", "evidence_ids": ["E1"]},
        "handoff": {"reference_defect_ids": [], "reviewer_findings": [], "unresolved_risks": [],
                    "evidence_quality_review": {**check, "reviewer_role": "fictional reviewer", "reviewer_kind": "synthetic"},
                    **{key: dict(check) for key in ("reference_review", "findings_review", "risk_acceptance")},
                    "decision_owner_role": "engineering lead", "commitment_scope": "Build a disposable intake prototype",
                    "resource_limit": "One engineer-day; no live sending", "next_review_trigger": "Review after prototype walkthrough"},
        "operational_performance": {"status": "not_collected"},
    }
    # Constructed test targets only, not a mechanism for relabeling a real passing check.
    targets = validation_targets(Assessment.model_validate(data))
    data['workflow']['validations'][0]['tested_requirement_digests'] = targets['requirement_digests']
    return data
