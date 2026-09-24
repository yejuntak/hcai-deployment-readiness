"""One deterministic engine for MCP, CLI and the portable agent Skill."""
import hashlib
import json
from .contracts import Assessment, AssessmentResult, Gate
from .versions import versions

RISK_FIELDS = ("complexity", "importance", "impact", "mission", "failure_consequence", "irreversibility")
DEPTH = {
    "low": {"profile": "QUICK6", "baseline_samples": 1, "need_sources": 1, "checks": []},
    "moderate": {"profile": "FULL", "baseline_samples": 3, "need_sources": 2,
                 "checks": ["independent_review", "validation_plan"]},
    "high": {"profile": "FULL", "baseline_samples": 5, "need_sources": 2,
             "checks": ["independent_review", "validation_plan", "hazard_analysis", "mission_review", "operational_evaluation_plan"]},
}


def risk_tier(risk):
    levels = [getattr(risk, key) for key in RISK_FIELDS]
    if any(v is None for v in levels):
        return "unknown"
    return max(levels, key=("low", "moderate", "high").index)


class GateBuilder:
    def __init__(self, id):
        self.id, self.missing, self.failures = id, [], []

    def require(self, condition, message):
        if not condition:
            self.missing.append(message)

    def fail(self, condition, message):
        if condition:
            self.failures.append(message)

    def check(self, check, name):
        self.fail(check.status == "fail", f"{name}: documented failure")
        self.require(check.status != "missing", f"{name}: not assessed")
        if check.status == "pass":
            self.require(bool(check.evidence_ids) and bool(check.note.strip()), f"{name}: pass needs evidence and rationale")

    def result(self):
        return Gate(id=self.id, status="FAIL" if self.failures else "MISSING" if self.missing else "PASS",
                    reasons=self.failures + self.missing)


def canonical_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                                     allow_nan=False).encode()).hexdigest()


def economics(a, baseline_usable):
    b, o, c = a.baseline, a.operational_oversight, a.costs
    fields = ("review_minutes_per_case", "correction_minutes_per_case", "escalation_minutes_per_case",
              "rework_minutes_per_case", "residual_manual_minutes_per_case")
    result = {"status": "INDETERMINATE", "basis": "projected_operating_scenario",
              "period": b.period, "currency": c.currency, "gross_minutes_saved_per_case": None,
              "oversight_minutes_per_case": None, "net_minutes_saved_per_case": None,
              "net_minutes_saved_per_period": None, "net_operational_benefit_per_period": None,
              "gross_labor_value_per_period": None, "baseline_operating_cost_per_period": None,
              "proposed_operating_cost_per_period": None, "one_time_implementation_cost": c.one_time_implementation_cost,
              "payback_periods": None, "recurring_roi_percent": None, "missing": [],
              "note": "Scenario estimate, not measured system performance. One-time implementation and protocol evaluation are separate; no automatic amortization."}
    if not baseline_usable:
        result["missing"].append("Measurable, evidence-backed current-state baseline")
    result["missing"].extend(f"operational_oversight.{f}" for f in fields if getattr(o, f) is None)
    if not o.evidence_ids:
        result["missing"].append("Oversight estimate evidence")
    if result["missing"]:
        return result
    gross = b.labor_minutes_per_case - o.residual_manual_minutes_per_case
    oversight = sum(getattr(o, f) for f in fields if f != "residual_manual_minutes_per_case")
    net = gross - oversight
    result.update(status="TIME_ONLY", gross_minutes_saved_per_case=round(gross, 6),
                  oversight_minutes_per_case=round(oversight, 6), net_minutes_saved_per_case=round(net, 6),
                  net_minutes_saved_per_period=round(net * b.volume_per_period, 6))
    required = ("currency", "labor_cost_per_hour", "baseline_nonlabor_cost_per_period",
                "proposed_recurring_fixed_cost_per_period", "proposed_nonlabor_cost_per_case")
    result["missing"].extend(f"costs.{f}" for f in required if getattr(c, f) is None)
    if not c.evidence_ids:
        result["missing"].append("Cost estimate evidence")
    if result["missing"]:
        return result
    base_cost = b.labor_minutes_per_case / 60 * c.labor_cost_per_hour * b.volume_per_period + c.baseline_nonlabor_cost_per_period
    new_cost = ((o.residual_manual_minutes_per_case + oversight) / 60 * c.labor_cost_per_hour
                + c.proposed_nonlabor_cost_per_case) * b.volume_per_period + c.proposed_recurring_fixed_cost_per_period
    benefit = base_cost - new_cost
    result.update(status="PROJECTED", gross_labor_value_per_period=round(gross / 60 * c.labor_cost_per_hour * b.volume_per_period, 6),
                  baseline_operating_cost_per_period=round(base_cost, 6), proposed_operating_cost_per_period=round(new_cost, 6),
                  net_operational_benefit_per_period=round(benefit, 6),
                  recurring_roi_percent=round(100 * benefit / new_cost, 6) if new_cost > 0 else None,
                  payback_periods=round(c.one_time_implementation_cost / benefit, 6)
                  if benefit > 0 and c.one_time_implementation_cost is not None else None)
    return result


def evaluation_cost(burden):
    result = burden.model_dump()
    parts = (burden.evaluator_minutes, burden.participant_minutes, burden.adjudication_minutes)
    minutes = sum(parts) if all(p is not None for p in parts) else None
    cost = (minutes / 60 * burden.labor_cost_per_hour + burden.tool_model_cost
            if minutes is not None and burden.labor_cost_per_hour is not None
            and burden.tool_model_cost is not None and burden.currency else None)
    result.update(total_person_minutes=minutes, protocol_evaluation_cost=None if cost is None else round(cost, 6),
                  cost_status="INDETERMINATE" if cost is None else "RECORDED_COST",
                  accounting_rule="Evaluator, participant and adjudication person-minutes are disjoint; elapsed time is wall-clock, not additive.")
    return result


def assess(a: Assessment) -> dict:
    tier = risk_tier(a.risk)
    depth = DEPTH.get(tier, DEPTH["high"])
    evidence = {e.id: e for e in a.evidence}
    gates = []
    b, w, h, o = a.baseline, a.workflow, a.handoff, a.operational_oversight
    g = GateBuilder("G1_BASELINE")
    for field in BaselineFields:
        g.require(getattr(b, field) is not None, f"baseline.{field}: missing")
    g.require((b.sample_size or 0) >= depth["baseline_samples"], f"At least {depth['baseline_samples']} observed baseline cases for this tier")
    g.require((b.volume_per_period or 0) > 0, "Positive current workflow volume and a period required")
    g.require(bool(b.evidence_ids), "Baseline observation records required")
    g.require(bool(b.actor_roles), "Current workflow actor roles required")
    accepted_kinds = {"observed", "synthetic"} if a.evaluator_kind == "synthetic" else {"observed"}
    g.require(all(evidence[r].kind in accepted_kinds for r in b.evidence_ids), "Estimates/assumptions are not a measured baseline")
    gates.append(g.result())

    g = GateBuilder("G2_NEED_REQUIREMENTS")
    g.require(bool(w.outcome), "Explicit intended outcome required")
    g.require(bool(w.needs) and bool(w.requirements), "End-user need and requirements required")
    for need in w.needs:
        g.require(len({evidence[r].sha256 for r in need.source_ids}) >= depth["need_sources"], f"{need.id}: {depth['need_sources']} distinct need sources required (duplicate bytes do not count twice)")
        if tier != "low":
            g.require(bool(need.discussion_evidence_ids), f"{need.id}: actual end-user discussion required")
            g.require(all(evidence[r].kind in accepted_kinds for r in need.discussion_evidence_ids), f"{need.id}: discussion cannot be assumed")
    for requirement in w.requirements:
        g.require(bool(requirement.need_ids), f"{requirement.id}: link to end-user need required")
    for need in w.needs:
        g.require(any(need.id in r.need_ids for r in w.requirements), f"{need.id}: no requirement addresses this need")
    gates.append(g.result())

    g = GateBuilder("G3_STATES_RECOVERY")
    for kind in ("normal", "edge", "recovery"):
        g.require(any(s.kind == kind for s in w.states), f"{kind} state path required")
    for state in w.states:
        g.require(bool(state.requirement_ids) and bool(state.evidence_ids), f"{state.id}: requirement and behavior evidence required")
    for requirement in w.requirements:
        g.require(any(requirement.id in s.requirement_ids for s in w.states), f"{requirement.id}: no defined state behavior")
    g.require(w.dependencies is not None, "Dependency inventory required; [] explicitly means none")
    g.check(w.dependency_review, "dependency_review")
    g.check(w.state_review, "state_review")
    gates.append(g.result())

    g = GateBuilder("G4_TRACEABILITY")
    g.require(bool(w.important_artifact_ids), "Important artifact/behavior inventory required")
    g.require(bool(w.requirements) and bool(w.validations), "Requirement and validation records required")
    validations = {v.id: v for v in w.validations}
    for r in w.requirements:
        g.require(bool(r.reference_material_ids), f"{r.id}: form/fit/function reference material required")
        g.fail(not r.artifact_ids or not r.validation_ids, f"{r.id}: broken requirement→artifact→validation chain")
        for artifact in r.artifact_ids:
            matches = [validations[t] for t in r.validation_ids
                       if r.id in validations[t].requirement_ids and artifact in validations[t].artifact_ids]
            g.fail(not matches, f"{r.id}/{artifact}: no matching requirement/artifact validation")
            g.require(any(t.status == "pass" and t.level != "specified" and t.evidence_ids for t in matches),
                      f"{r.id}/{artifact}: executed walkthrough or test evidence required")
    for artifact in w.important_artifact_ids:
        g.fail(not any(artifact in r.artifact_ids for r in w.requirements), f"{artifact}: important artifact has no requirement")
    for v in w.validations:
        g.fail(v.status == "fail", f"{v.id}: failed validation")
        g.require(bool(v.requirement_ids) and bool(v.artifact_ids), f"{v.id}: validation references required")
        g.require(v.status != "missing" and v.level != "specified" and bool(v.evidence_ids),
                  f"{v.id}: every listed validation requires execution evidence")
        g.require(all(evidence[r].kind in accepted_kinds for r in v.evidence_ids), f"{v.id}: execution cannot be assumed or estimated")
    gates.append(g.result())

    g = GateBuilder("G5_OVERSIGHT")
    for key in ("review_minutes_per_case", "correction_minutes_per_case", "escalation_minutes_per_case",
                "rework_minutes_per_case", "residual_manual_minutes_per_case", "owner_role"):
        g.require(getattr(o, key) is not None, f"operational_oversight.{key}: estimate required")
    g.require(bool(o.evidence_ids), "Oversight estimate basis required, including explicit zero assumptions")
    gates.append(g.result())

    g = GateBuilder("G6_COMMITMENT")
    g.require(tier != "unknown", "All six risk dimensions must be classified")
    g.require(bool(a.risk.rationale.strip()) and bool(a.risk.evidence_ids), "Risk rationale and evidence required")
    if depth["profile"] == "FULL":
        g.require(a.requested_profile == "FULL", "Escalate to FULL and submit a new run; QUICK6 cannot satisfy this tier")
    for key in ("reference_defect_ids", "reviewer_findings", "unresolved_risks", "decision_owner_role",
                "commitment_scope", "resource_limit", "next_review_trigger"):
        g.require(getattr(h, key) is not None, f"handoff.{key}: required")
    for finding in h.reviewer_findings or []:
        g.fail(finding.severity == "critical" and finding.status != "resolved", f"{finding.id}: unresolved critical finding (acceptance cannot waive)")
        g.fail(finding.severity == "major" and finding.status == "open", f"{finding.id}: unresolved major finding")
        g.require(bool(finding.evidence_ids), f"{finding.id}: finding evidence required")
    for key in ["reference_review", "findings_review", "risk_acceptance", *depth["checks"]]:
        g.check(getattr(h, key), key)
    if tier != "low":
        g.require(h.independent_review.independent_from_artifact_owner is True and bool(h.independent_review.reviewer_role),
                  "Independent reviewer role and separation from artifact owner required")
    for key in ("elapsed_minutes", "evaluator_minutes", "participant_minutes", "participant_count",
                "adjudication_minutes", "review_correction_cycles"):
        g.require(getattr(a.evaluator_burden, key) is not None, f"evaluator_burden.{key}: required")
    g.require(bool(a.evaluator_burden.evidence_ids), "Evaluation timing/participant record required")
    if a.requested_profile == "QUICK6":
        g.require(a.evaluator_burden.elapsed_minutes is not None and a.evaluator_burden.elapsed_minutes <= 15,
                  "QUICK6 exceeded 15 minutes or was not timed: continue as FULL in a new run")
    gates.append(g.result())

    stop = next((g.id for g in gates if g.status != "PASS"), None)
    if a.requested_profile == "QUICK6" and stop:
        index = next(i for i, g in enumerate(gates) if g.id == stop)
        gates[index + 1:] = [Gate(id=g.id, status="NOT_EVALUATED", reasons=[f"Stopped at {stop}"]) for g in gates[index + 1:]]
    decision = ("REVISE" if any(g.status == "FAIL" for g in gates)
                else "INSUFFICIENT_EVIDENCE" if any(g.status != "PASS" for g in gates)
                else "PROCEED_TO_ENGINEERING")
    result = AssessmentResult(
        run_id=a.run_id, versions=versions(), evaluator_kind=a.evaluator_kind, decision=decision,
        decision_scope="bounded_engineering_commitment", risk_tier=tier, requested_profile=a.requested_profile,
        required_profile="FULL" if depth["profile"] == "FULL" or (a.requested_profile == "QUICK6" and stop) else a.requested_profile,
        escalation_required=a.requested_profile == "QUICK6" and (depth["profile"] == "FULL" or bool(stop)),
        stop_at_gate=stop, gates=gates, roi=economics(a, gates[0].status == "PASS"),
        evaluator_burden=evaluation_cost(a.evaluator_burden), operational_oversight=o.model_dump(),
        operational_performance={**a.operational_performance.model_dump(), "deployment_decision": "NOT_ASSESSED",
                                 "interpretation": "Supplied post-implementation observations only; no performance is inferred from upstream gates."},
        handoff_record={**h.model_dump(), "recommendation": decision, "owner_authorization": "PENDING_SEPARATE_RECORDED_DECISION"},
        provenance={"input_sha256": canonical_digest(a.model_dump()), "artifacts": [e.model_dump() for e in a.evidence],
                    "digest_verification": "Supplied artifact digests are format-checked, not independently fetched/verified by this offline engine."},
        limitations=["Engineering commitment recommendation only; never deployment certification.",
                     "Evidence truth, completeness of inventories and risk judgments require accountable human review.",
                     "Practitioner correspondence informed refinement; it is not controlled empirical validation.",
                     "Risk thresholds and the <=15-minute target are provisional and unvalidated."])
    return result.model_dump()


BaselineFields = ("current_state_summary", "actor_roles", "observation_window", "sample_size", "cycle_minutes_per_case", "labor_minutes_per_case",
                  "handoffs_per_case", "touches_per_case", "failure_points", "manual_review_minutes_per_case",
                  "escalation_minutes_per_case", "rework_minutes_per_case", "volume_per_period", "period")
