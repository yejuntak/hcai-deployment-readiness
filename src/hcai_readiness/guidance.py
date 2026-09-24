"""Small, deterministic review prompts and decision cards. No evidence generation."""
import json
from importlib.resources import files
from .contracts import Assessment
from .engine import assess, RISK_FIELDS
from .versions import versions

GUIDES = {
    "G1_BASELINE": {
        "title": "Understand today's work", "question": "Can you show one recent case from its first step to its final outcome?",
        "owner": "workflow owner", "fields": ["scope.unit_of_work", "baseline.steps", "baseline.entry_step_id", "baseline.observation_window", "baseline.sample_size", "baseline.labor_minutes_per_case", "baseline.cycle_minutes_per_case", "baseline.volume_per_period", "baseline.period", "baseline.map_review"],
        "action": "Observe the current work, map who does each step and how exceptions are handled, then record disjoint labor and elapsed time.",
        "example": "Illustration only: intake received -> advisor review -> confirmed; missing details -> correction -> return to review.",
        "do_not": "Do not replace observations with the proposed process or recollected savings estimates."},
    "G2_NEED_REQUIREMENTS": {
        "title": "Name the need and success condition", "question": "Whose difficulty are we solving, and what observable result would satisfy them?",
        "owner": "product/workflow owner", "fields": ["scope", "workflow.outcome", "workflow.needs", "workflow.requirements"],
        "action": "Connect a real work record or end-user discussion to an owned requirement with a checkable acceptance condition. Compare a manual/non-AI option.",
        "example": "Illustration only: after cancellation, the advisor can reopen all previously entered contact fields.",
        "do_not": "Do not count two copies of one source, general industry articles, or feedback about this protocol as independent customer need evidence."},
    "G3_STATES_RECOVERY": {
        "title": "Walk through normal work, failure and recovery", "question": "When the proposed workflow cannot finish, who notices and how do they recover?",
        "owner": "workflow designer and operator", "fields": ["workflow.states", "workflow.state_review", "workflow.dependencies", "workflow.dependency_review", "workflow.action_boundaries", "workflow.human_control_review"],
        "action": "Walk the normal, edge and recovery paths. Record triggers, actions, data preservation and the responsible role; review dependencies.",
        "example": "Illustration only: a missing field is shown to the advisor; cancelling returns to saved intake without data loss.",
        "do_not": "Do not infer an error or recovery path from a polished happy-path screen."},
    "G4_TRACEABILITY": {
        "title": "Inspect why each artifact belongs", "question": "Show the requirement, the exact artifact revision and the check that tested it together.",
        "owner": "requirement owner and reviewer", "fields": ["workflow.important_artifact_ids", "workflow.requirements", "workflow.validations", "evidence"],
        "action": "Repair each requirement -> artifact -> executed-check link. Compare tested artifact digests; repeat checks after changed artifacts.",
        "example": "Illustration only: requirement R1 -> saved-intake screen revision 2 -> recorded cancellation walkthrough of that exact file.",
        "do_not": "Do not count a planned test, an old artifact revision, or visual fidelity as a passing check."},
    "G5_OVERSIGHT": {
        "title": "Count the work AI leaves or creates", "question": "For each case, how much human checking, correction and remaining manual work will be needed?",
        "owner": "operating workflow owner", "fields": ["operational_oversight", "costs"],
        "action": "Estimate review, correction, escalation, rework and residual manual minutes separately, with a basis. Keep recurring and one-time costs separate.",
        "example": "Illustration only: 15 gross minutes saved minus 15 oversight minutes leaves zero net time savings.",
        "do_not": "Do not count the same minute twice or convert unknown money, time or token usage into zero."},
    "G6_COMMITMENT": {
        "title": "Bound the engineering decision", "question": "What exact engineering step, resource limit and next review would this evidence justify?",
        "owner": "engineering decision owner", "fields": ["handoff", "evaluator_burden"],
        "action": "Resolve blocking findings, complete tier-specific reviews, record preparation/session burden, and name the scope, owner, resource cap and revisit trigger.",
        "example": "Illustration only: one engineer-day for a disposable prototype; no live sending; review the cancellation path before any further spend.",
        "do_not": "Do not treat this recommendation as owner authorization or deployment approval. Explain funding despite nonpositive benefit."},
}

LABELS = {"PROCEED_TO_ENGINEERING": "Evidence supports a bounded engineering step",
          "REVISE": "Fix the identified problem before committing engineering",
          "INSUFFICIENT_EVIDENCE": "Pause: the decision does not yet have enough evidence"}


def criteria_catalog():
    return json.loads(files("hcai_readiness").joinpath("criteria.json").read_text())


def criterion_guide(criterion_id):
    match = next((c for c in criteria_catalog()["criteria"] if c["id"] == criterion_id), None)
    if match is None:
        return {"found": False, "valid_ids": [c["id"] for c in criteria_catalog()["criteria"]]}
    return {"found": True, "versions": versions(), **match, "gate_guide": GUIDES[match["gate"]],
            "claim_limit": "Candidate criterion; structural checks do not replace human evidence review or prove system performance."}


def new_review(run_id, recorded_at, evaluator_kind, requested_profile="QUICK6"):
    """Only user-supplied metadata and declared versions are populated; all evidence is empty."""
    return Assessment(run_id=run_id, recorded_at=recorded_at, evaluator_kind=evaluator_kind,
                      requested_profile=requested_profile, versions=versions(), evidence=[]).model_dump()


def next_step(a, result=None):
    r = result or assess(a)
    if not a.scope.workflow_name or not a.scope.unit_of_work:
        return {"stage": "SCOPE", "question": "Which one piece of work are we reviewing, and what counts as one completed case?",
                "owner": "workflow owner", "fields": ["scope.workflow_name", "scope.unit_of_work", "scope.starts_when", "scope.ends_when"],
                "action": "Name one bounded workflow. Do not start with the proposed technology."}
    if r["routing"]["status"] == "USE_FULL":
        unknown = ["risk." + k for k in RISK_FIELDS if getattr(a.risk, k) is None]
        return {"stage": "PROFILE_ROUTING", "question": "Who will help classify the missing risk information and lead the full review?" if unknown else "Who will lead the full review for this workflow?",
                "owner": "workflow owner and qualified reviewer", "fields": unknown or ["requested_profile"],
                "action": r["routing"]["reason"] + " Preserve this record; create a new FULL run linked through previous_run_id and revision_summary."}
    gate = next((g for g in r["gates"] if g["status"] != "PASS"), None)
    if gate:
        return {"stage": gate["id"], **GUIDES[gate["id"]], "reasons": gate["reasons"],
                "resume_rule": "Preserve a stopped QUICK6 run. After remediation, use a new FULL run with a previous-run link."}
    return {"stage": "OWNER_DECISION", "question": "Does the named owner authorize this exact bounded engineering step?",
            "owner": a.handoff.decision_owner_role, "fields": [],
            "action": "Record the owner's separate dated authorization or refusal and conditions. Do not infer authorization from a gate pass."}


def decision_card(a, result=None):
    r = result or assess(a)
    return {"headline": LABELS[r["decision"]], "decision": r["decision"], "run_id": a.run_id,
            "versions": versions(), "workflow": a.scope.workflow_name, "unit_of_work": a.scope.unit_of_work,
            "risk": r["risk_tier"], "required_profile": r["required_profile"], "routing": r["routing"],
            "stop_at": r["stop_at_gate"], "next_step": next_step(a, r), "attention_items": r["attention_items"],
            "gates": [{**g, "title": GUIDES[g["id"]]["title"],
                       "criteria_ids": [c["id"] for c in criteria_catalog()["criteria"] if c["gate"] == g["id"]]} for g in r["gates"]],
            "operating_benefit": r["roi"], "protocol_evaluation_burden": r["evaluator_burden"],
            "operating_oversight": r["operational_oversight"], "operational_performance": r["operational_performance"],
            "engineering_scope": a.handoff.commitment_scope, "resource_limit": a.handoff.resource_limit,
            "owner": a.handoff.decision_owner_role, "revisit_when": a.handoff.next_review_trigger,
            "boundary": "Engineering recommendation only. Owner authorization and deployment evaluation are separate.",
            "input_sha256": r["provenance"]["input_sha256"], "record_privacy": "PRIVATE working record; review permission and identifying content before sharing."}


def guided_review(a, include_assessment=False):
    r = assess(a)
    output = {"decision_card": decision_card(a, r)}
    if include_assessment:
        output["assessment"] = r
    return output
