"""One deterministic engine for MCP, CLI and the portable agent Skill."""
import hashlib
import json
from .contracts import Assessment, AssessmentResult, Gate
from .versions import versions

RISK_FIELDS = ("complexity", "importance", "impact", "mission", "failure_consequence", "irreversibility")
CONTEXT_FLOORS = {"safety_or_rights_impact": "high", "irreversible_external_actions": "high",
                  "sensitive_data": "moderate", "untrusted_input_to_actions": "moderate"}
IMPACT_DOMAINS = ("access_usability", "privacy_security", "unequal_effects", "human_agency")
DEPTH = {
    "low": {"profile": "QUICK6", "baseline_samples": 1, "need_sources": 1, "checks": []},
    "moderate": {"profile": "FULL", "baseline_samples": 3, "need_sources": 2,
                 "checks": ["independent_review", "validation_plan"]},
    "high": {"profile": "FULL", "baseline_samples": 5, "need_sources": 2,
             "checks": ["independent_review", "validation_plan", "hazard_analysis", "mission_review", "operational_evaluation_plan"]},
}


def risk_tier(risk):
    levels = [getattr(risk, key) for key in RISK_FIELDS]
    if any(v is None for v in levels) or any(v is None for v in risk.context.model_dump().values()):
        return "unknown"
    return known_risk_floor(risk)


def known_risk_floor(risk):
    levels = [getattr(risk, key) for key in RISK_FIELDS if getattr(risk, key)]
    levels += [tier for key, tier in CONTEXT_FLOORS.items() if getattr(risk.context, key) is True]
    return max(levels, default=None, key=("low", "moderate", "high").index)


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


def requirement_digest(a, requirement):
    """Bind a check to its requirement and relevant design context, not just its artifact."""
    evidence = {e.id: e for e in a.evidence}
    return canonical_digest({
        "requirement": requirement.model_dump(), "scope": a.scope.model_dump(),
        "states": [s.model_dump() for s in a.workflow.states if requirement.id in s.requirement_ids],
        "entry_state_id": a.workflow.entry_state_id, "dependencies": a.workflow.dependencies,
        "action_boundaries": a.workflow.action_boundaries,
        "references": {ref: {"version": evidence[ref].version, "sha256": evidence[ref].sha256}
                       for ref in requirement.reference_material_ids}})


def validation_targets(a):
    """Current fingerprints, NOT validation receipts. Never stamps a passing test."""
    return {"versions": versions(), "artifact_digests": {e.id: e.sha256 for e in a.evidence},
            "requirement_digests": {r.id: requirement_digest(a, r) for r in a.workflow.requirements},
            "instruction": "Capture these targets when performing the check. Recheck changed requirements/context/artifacts; do not relabel an old result with new hashes.",
            "evidence_verified": False}


def connected_paths(g, rows, entry, next_field, label):
    if not rows or not entry:
        g.require(False, f"{label}: define an entry and connected states")
        return
    by_id = {row.id: row for row in rows}
    reached, pending = set(), [entry]
    while pending:
        node = pending.pop()
        if node not in reached:
            reached.add(node)
            pending.extend(getattr(by_id[node], next_field))
    g.require(reached == set(by_id), f"{label}: every state must be reachable from the entry")
    can_end = {row.id for row in rows if row.terminal}
    while True:
        expanded = can_end | {row.id for row in rows if any(n in can_end for n in getattr(row, next_field))}
        if expanded == can_end:
            break
        can_end = expanded
    g.require(set(by_id) <= can_end, f"{label}: every state needs a reachable endpoint or safe exit")


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
    parts = (burden.preparation_person_minutes, burden.evaluator_minutes, burden.participant_minutes, burden.adjudication_minutes)
    minutes = sum(parts) if all(p is not None for p in parts) else None
    cost = (minutes / 60 * burden.labor_cost_per_hour + burden.tool_model_cost
            if minutes is not None and burden.labor_cost_per_hour is not None
            and burden.tool_model_cost is not None and burden.currency else None)
    result.update(total_person_minutes=minutes, protocol_evaluation_cost=None if cost is None else round(cost, 6),
                  cost_status="INDETERMINATE" if cost is None else "RECORDED_COST",
                  accounting_rule="Preparation, evaluator, participant and adjudication person-minutes are disjoint. Capture/reporting is included in session time, not added again. Preparation wall time is separate from the timed session.")
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
    g.require(bool(a.scope.unit_of_work), "Define one unit of work before comparing minutes or volume")
    g.require(bool(b.entry_step_id) and bool(b.steps), "Map the current workflow step by step, with an entry step")
    for kind in ("normal", "edge", "recovery"):
        g.require(any(s.kind == kind for s in b.steps), f"Current-state {kind} path required; distinguish observed from reported practice")
    g.require(any(s.kind == "normal" and s.observation_status == "observed" for s in b.steps), "At least one current normal path must be observed")
    for step in b.steps:
        g.require(bool(step.evidence_ids) and all(evidence[r].kind in accepted_kinds for r in step.evidence_ids), f"{step.id}: current practice needs retained observation/discussion records")
        g.require(step.terminal or bool(step.next_step_ids), f"{step.id}: identify the next step or mark the endpoint")
    if b.steps and b.entry_step_id:
        by_id = {s.id: s for s in b.steps}
        reached, pending = set(), [b.entry_step_id]
        while pending:
            node = pending.pop()
            if node not in reached:
                reached.add(node)
                pending.extend(by_id[node].next_step_ids)
        g.require(reached == set(by_id), "Every current-state step must be reachable from the entry")
        can_end = {s.id for s in b.steps if s.terminal}
        while True:
            expanded = can_end | {s.id for s in b.steps if any(n in can_end for n in s.next_step_ids)}
            if expanded == can_end:
                break
            can_end = expanded
        g.require(set(by_id) <= can_end, "Every current-state path needs a reachable endpoint or safe exit")
    g.check(b.map_review, "current_state_map_review")
    gates.append(g.result())

    g = GateBuilder("G2_NEED_REQUIREMENTS")
    g.require(bool(w.outcome), "Explicit intended outcome required")
    g.require(bool(w.needs) and bool(w.requirements), "End-user need and requirements required")
    for key in type(a.scope).model_fields:
        g.require(getattr(a.scope, key) is not None, f"scope.{key}: define the bounded workflow and alternatives")
    g.require(bool(a.scope.alternatives_considered), "Compare at least one existing/manual/non-AI alternative")
    g.require(bool(a.scope.affected_roles), "Name affected people, including non-operators where relevant")
    impacts = {row.domain: row for row in w.impact_reviews}
    for domain in IMPACT_DOMAINS:
        row = impacts.get(domain)
        g.require(row is not None, f"{domain}: screen effects on people; unknown is not not-applicable")
        if row is None:
            continue
        g.require(row.applicability != 'unknown', f"{domain}: applicability unresolved")
        g.require(bool(row.rationale.strip()) and bool(row.owner_role) and bool(row.evidence_ids), f"{domain}: record rationale, owner and evidence even for not-applicable")
        if domain in ('access_usability', 'human_agency'):
            g.fail(row.applicability == 'not_applicable', f"{domain}: human use and control cannot be excluded from this profile")
        if domain == 'privacy_security' and (a.risk.context.sensitive_data is True or a.risk.context.untrusted_input_to_actions is True):
            g.fail(row.applicability == 'not_applicable', 'privacy_security: consequential-context flags make this review applicable')
        if row.applicability == 'applicable':
            g.require(bool(row.affected_roles) and bool(row.requirement_ids), f"{domain}: affected roles and testable requirements required")
    covered = {role for row in w.impact_reviews if row.applicability == 'applicable' for role in row.affected_roles}
    g.require(set(a.scope.affected_roles or []) <= covered, "Every affected role needs coverage in an applicable impact review")
    for need in w.needs:
        sources = [evidence[r] for r in need.source_ids if evidence[r].origin_id and evidence[r].kind in accepted_kinds
                   and evidence[r].source_type in ("work_record", "end_user_discussion")]
        independent_count = min(len({e.origin_id for e in sources}), len({e.sha256 for e in sources}))
        g.require(independent_count >= depth["need_sources"], f"{need.id}: {depth['need_sources']} distinct original work/discussion sources required; copies, estimates and general references do not count")
        if tier != "low":
            g.require(bool(need.discussion_evidence_ids), f"{need.id}: actual end-user discussion required")
            g.require(all(evidence[r].kind in accepted_kinds for r in need.discussion_evidence_ids), f"{need.id}: discussion cannot be assumed")
            g.require(all(evidence[r].source_type == "end_user_discussion" and evidence[r].origin_id for r in need.discussion_evidence_ids), f"{need.id}: identify the actual end-user discussion origin")
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
        g.require(state.terminal is not None, f"{state.id}: specify whether this is an endpoint")
        g.require(state.terminal or bool(state.next_state_ids), f"{state.id}: identify the next state or an endpoint")
    connected_paths(g, w.states, w.entry_state_id, 'next_state_ids', 'Proposed workflow')
    for requirement in w.requirements:
        g.require(any(requirement.id in s.requirement_ids for s in w.states), f"{requirement.id}: no defined state behavior")
    g.require(w.dependencies is not None, "Dependency inventory required; [] explicitly means none")
    g.check(w.dependency_review, "dependency_review")
    g.check(w.state_review, "state_review")
    g.require(bool(w.action_boundaries), "Record what people and automated components may access, change or send; an empty inventory is insufficient")
    g.check(w.human_control_review, "human_control_review")
    gates.append(g.result())

    g = GateBuilder("G4_TRACEABILITY")
    g.require(bool(w.important_artifact_ids), "Important artifact/behavior inventory required")
    g.require(bool(w.requirements) and bool(w.validations), "Requirement and validation records required")
    validations = {v.id: v for v in w.validations}
    for r in w.requirements:
        g.require(r.behavior_status != "unknown", f"{r.id}: label behavior as specified only, simulated or implemented")
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
        for requirement in w.requirements:
            if requirement.id in v.requirement_ids:
                tested = v.tested_requirement_digests.get(requirement.id)
                g.require(tested is not None, f"{v.id}/{requirement.id}: record the requirement/context fingerprint tested")
                g.fail(tested is not None and tested != requirement_digest(a, requirement), f"{v.id}/{requirement.id}: requirement or context changed since validation; repeat the affected check")
        if v.level == "implemented_test":
            g.fail(any(req.behavior_status != "implemented" for req in w.requirements if req.id in v.requirement_ids), f"{v.id}: cannot label a check implemented when linked behavior is only specified or simulated")
        g.fail(v.status == "fail", f"{v.id}: failed validation")
        g.require(bool(v.requirement_ids) and bool(v.artifact_ids), f"{v.id}: validation references required")
        g.require(v.status != "missing" and v.level != "specified" and bool(v.evidence_ids),
                  f"{v.id}: every listed validation requires execution evidence")
        g.require(all(evidence[r].kind in accepted_kinds for r in v.evidence_ids), f"{v.id}: execution cannot be assumed or estimated")
        for artifact in v.artifact_ids:
            tested_digest = v.tested_artifact_digests.get(artifact)
            g.require(tested_digest is not None, f"{v.id}/{artifact}: record the exact artifact digest that was tested")
            g.fail(tested_digest is not None and tested_digest != evidence[artifact].sha256, f"{v.id}/{artifact}: artifact changed since validation; rerun the check")
    gates.append(g.result())

    g = GateBuilder("G5_OVERSIGHT")
    for key in ("review_minutes_per_case", "correction_minutes_per_case", "escalation_minutes_per_case",
                "rework_minutes_per_case", "residual_manual_minutes_per_case", "owner_role"):
        g.require(getattr(o, key) is not None, f"operational_oversight.{key}: estimate required")
    g.require(bool(o.evidence_ids), "Oversight estimate basis required, including explicit zero assumptions")
    gates.append(g.result())

    g = GateBuilder("G6_COMMITMENT")
    g.require(tier != "unknown", "All six risk dimensions must be classified")
    g.require(all(v is not None for v in a.risk.context.model_dump().values()), "Answer every consequential-context question; unknown cannot be treated as no")
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
    review = h.evidence_quality_review
    g.check(review, 'evidence_quality_review')
    allowed_reviewers = {'synthetic'} if a.evaluator_kind == 'synthetic' else {'human', 'ai-assisted-human'}
    quality_record_complete = (review.status == 'pass' and bool(review.reviewer_role)
                               and review.reviewer_kind in allowed_reviewers and bool(review.note.strip())
                               and bool(review.evidence_ids) and all(evidence[r].kind in accepted_kinds for r in review.evidence_ids))
    if review.status == 'pass':
        g.require(bool(review.reviewer_role) and review.reviewer_kind in allowed_reviewers,
                  'A human evidence-quality reviewer must inspect relevance, coverage, authenticity and test adequacy; agent-only review cannot pass')
        g.require(all(evidence[r].kind in accepted_kinds for r in review.evidence_ids), 'Evidence-quality review needs retained observation records, not estimates or assumptions')
    if tier != "low":
        g.require(h.independent_review.independent_from_artifact_owner is True and bool(h.independent_review.reviewer_role),
                  "Independent reviewer role and separation from artifact owner required")
    for key in ("elapsed_minutes", "evaluator_minutes", "participant_minutes", "participant_count",
                "adjudication_minutes", "review_correction_cycles", "preparation_elapsed_minutes",
                "preparation_person_minutes", "capture_reporting_minutes"):
        g.require(getattr(a.evaluator_burden, key) is not None, f"evaluator_burden.{key}: required")
    g.require(bool(a.evaluator_burden.evidence_ids), "Evaluation timing/participant record required")
    if a.requested_profile == "QUICK6":
        g.require(a.evaluator_burden.elapsed_minutes is not None and a.evaluator_burden.elapsed_minutes <= 15,
                  "QUICK6 exceeded 15 minutes or was not timed: continue as FULL in a new run")
    projected = economics(a, gates[0].status == "PASS")
    nonpositive = (projected["net_operational_benefit_per_period"] is not None and projected["net_operational_benefit_per_period"] <= 0) or (
        projected["net_minutes_saved_per_case"] is not None and projected["net_minutes_saved_per_case"] <= 0)
    if nonpositive:
        g.require(bool(h.investment_rationale), "Net benefit is nonpositive: owner must explain the nonfinancial or learning reason to fund engineering")
    gates.append(g.result())

    stop = next((g.id for g in gates if g.status != "PASS"), None)
    routing = {"status": "REVIEW", "reason": "Use the six gates at the classified depth.",
               "known_risk_floor": known_risk_floor(a.risk),
               "context_triggers": [{"field": key, "minimum_tier": floor} for key, floor in CONTEXT_FLOORS.items() if getattr(a.risk.context, key) is True]}
    if a.requested_profile == "QUICK6" and tier != "low":
        routing.update(status="USE_FULL", reason="Classify missing risk dimensions and use FULL." if tier == "unknown" else "This risk tier requires FULL before any QUICK6 gate is evaluated.")
    elif a.requested_profile == "QUICK6" and a.evaluator_burden.elapsed_minutes is not None and a.evaluator_burden.elapsed_minutes > 15:
        routing.update(status="USE_FULL", reason="The short-session limit was exceeded. Preserve this run and continue in FULL; extra time is not a product defect.")
    if routing["status"] == "USE_FULL":
        stop = "PROFILE_ROUTING"
        gates = [Gate(id=g.id, status="NOT_EVALUATED", reasons=[routing["reason"]]) for g in gates]
    elif a.requested_profile == "QUICK6" and stop:
        index = next(i for i, g in enumerate(gates) if g.id == stop)
        gates[index + 1:] = [Gate(id=g.id, status="NOT_EVALUATED", reasons=[f"Stopped at {stop}"]) for g in gates[index + 1:]]
    decision = ("REVISE" if any(g.status == "FAIL" for g in gates)
                else "INSUFFICIENT_EVIDENCE" if any(g.status != "PASS" for g in gates)
                else "PROCEED_TO_ENGINEERING")
    attention = [{"kind": "critical_finding", "id": f.id, "message": f.description,
                  "action": "Resolve this critical finding before any engineering recommendation."}
                 for f in h.reviewer_findings or [] if f.severity == "critical" and f.status != "resolved"]
    if attention:
        decision = "REVISE"
    if nonpositive:
        attention.append({"kind": "nonpositive_benefit", "id": "OPERATING_BENEFIT",
                          "message": "Oversight or recurring costs erase the claimed benefit.",
                          "action": "Revise the business case or record an explicit nonfinancial/learning rationale."})
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
                     "Risk thresholds and the <=15-minute target are provisional and unvalidated."],
        routing=routing, attention_items=attention,
        assurance={"machine_check": "STRUCTURAL_AND_RULE_CHECKS_ONLY",
                   "human_quality_review": "RECORDED_PASS" if quality_record_complete else "NOT_ESTABLISHED",
                   "supplied_review_status": review.status,
                   "reviewer_role": review.reviewer_role, "reviewer_kind": review.reviewer_kind,
                   "evidence_authenticity": "NOT_INDEPENDENTLY_VERIFIED", "criterion_conformance": "NOT_CERTIFIED",
                   "meaning": "A pass combines deterministic checks with supplied human judgments. Software cannot establish that the evidence is true or adequate, or that the reviewer actually inspected it."})
    return result.model_dump()


BaselineFields = ("current_state_summary", "actor_roles", "observation_window", "sample_size", "cycle_minutes_per_case", "labor_minutes_per_case",
                  "handoffs_per_case", "touches_per_case", "failure_points", "manual_review_minutes_per_case",
                  "escalation_minutes_per_case", "rework_minutes_per_case", "volume_per_period", "period")
