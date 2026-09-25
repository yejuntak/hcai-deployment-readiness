"""Candidate contracts. Unknown evidence remains nullable; invalid data never passes."""
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
from .versions import versions

Text = Annotated[str, Field(min_length=1)]
Number = Annotated[float, Field(ge=0, allow_inf_nan=False)]
Count = Annotated[int, Field(ge=0)]
Digest = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
Decision = Literal["PROCEED_TO_ENGINEERING", "REVISE", "INSUFFICIENT_EVIDENCE"]
Tier = Literal["low", "moderate", "high"]
Profile = Literal["QUICK6", "FULL"]


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)


class Versions(Record):
    protocol: Text
    mcp: Text
    skill: Text
    contract: Text


class Evidence(Record):
    id: Text
    version: Text
    sha256: Digest
    locator: Text
    kind: Literal["observed", "estimate", "assumption", "synthetic"]
    description: Text
    origin_id: Text | None = None
    source_type: Literal["work_record", "end_user_discussion", "reference", "artifact", "validation_record", "review_record", "estimate", "unknown"] = "unknown"


class Check(Record):
    status: Literal["pass", "fail", "missing"] = "missing"
    evidence_ids: list[Text] = Field(default_factory=list)
    note: str = ""
    reviewer_role: Text | None = None
    reviewer_kind: Literal["human", "ai-assisted-human", "agent", "synthetic"] | None = None
    independent_from_artifact_owner: bool | None = None


class CurrentStep(Record):
    id: Text
    kind: Literal["normal", "edge", "recovery"]
    actor_role: Text
    trigger: Text
    action: Text
    data_handling: Text
    next_step_ids: list[Text]
    terminal: bool
    evidence_ids: list[Text]
    observation_status: Literal["observed", "reported"]


class Scope(Record):
    workflow_name: Text | None = None
    unit_of_work: Text | None = None
    starts_when: Text | None = None
    ends_when: Text | None = None
    environment: Text | None = None
    ai_role: Literal["artifact_creation", "in_workflow", "both", "neither"] | None = None
    alternatives_considered: list[Text] | None = None
    exclusions: list[Text] | None = None
    affected_roles: list[Text] | None = None


class Baseline(Record):
    steps: list[CurrentStep] = Field(default_factory=list)
    entry_step_id: Text | None = None
    map_review: Check = Field(default_factory=Check)
    current_state_summary: Text | None = None
    actor_roles: list[Text] | None = None
    observation_window: Text | None = None
    sample_size: Count | None = None
    cycle_minutes_per_case: Number | None = None
    labor_minutes_per_case: Number | None = None
    handoffs_per_case: Number | None = None
    touches_per_case: Number | None = None
    failure_points: list[Text] | None = None
    manual_review_minutes_per_case: Number | None = None
    escalation_minutes_per_case: Number | None = None
    rework_minutes_per_case: Number | None = None
    volume_per_period: Number | None = None
    period: Text | None = None
    evidence_ids: list[Text] = Field(default_factory=list)

    @model_validator(mode="after")
    def labor_subsets(self):
        parts = (self.manual_review_minutes_per_case, self.escalation_minutes_per_case, self.rework_minutes_per_case)
        if self.labor_minutes_per_case is not None and all(x is not None for x in parts):
            if sum(parts) > self.labor_minutes_per_case:
                raise ValueError("Baseline review/escalation/rework must be disjoint subsets of baseline labor")
        ids = [step.id for step in self.steps]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate current-state step IDs")
        if self.entry_step_id is not None and self.entry_step_id not in ids:
            raise ValueError("Current-state entry step does not resolve")
        for step in self.steps:
            if len(step.next_step_ids) != len(set(step.next_step_ids)) or not set(step.next_step_ids) <= set(ids):
                raise ValueError("Current-state next-step references must be unique and resolve")
            if step.terminal and step.next_step_ids:
                raise ValueError("A terminal current-state step cannot have an outgoing path")
        return self


class ContextScreen(Record):
    safety_or_rights_impact: bool | None = None
    irreversible_external_actions: bool | None = None
    sensitive_data: bool | None = None
    untrusted_input_to_actions: bool | None = None


class Risk(Record):
    context: ContextScreen = Field(default_factory=ContextScreen)
    complexity: Tier | None = None
    importance: Tier | None = None
    impact: Tier | None = None
    mission: Tier | None = None
    failure_consequence: Tier | None = None
    irreversibility: Tier | None = None
    rationale: str = ""
    evidence_ids: list[Text] = Field(default_factory=list)


class Need(Record):
    id: Text
    description: Text
    end_user_role: Text
    source_ids: list[Text]
    discussion_evidence_ids: list[Text] = Field(default_factory=list)


class Requirement(Record):
    id: Text
    description: Text
    acceptance_criteria: Text
    form: Text
    fit: Text
    function: Text
    reference_material_ids: list[Text]
    owner_role: Text
    need_ids: list[Text]
    artifact_ids: list[Text]
    validation_ids: list[Text]
    behavior_status: Literal["specified_only", "simulated", "implemented", "unknown"] = "unknown"


class State(Record):
    id: Text
    kind: Literal["normal", "edge", "recovery"]
    trigger: Text
    behavior: Text
    resulting_state: Text
    data_handling: Text
    owner_role: Text
    requirement_ids: list[Text]
    evidence_ids: list[Text]
    next_state_ids: list[Text] = Field(default_factory=list)
    terminal: bool | None = None


class ImpactReview(Record):
    domain: Literal["access_usability", "privacy_security", "unequal_effects", "human_agency"]
    applicability: Literal["applicable", "not_applicable", "unknown"] = "unknown"
    rationale: str = ""
    owner_role: Text | None = None
    affected_roles: list[Text] = Field(default_factory=list)
    requirement_ids: list[Text] = Field(default_factory=list)
    evidence_ids: list[Text] = Field(default_factory=list)


class Validation(Record):
    id: Text
    requirement_ids: list[Text]
    artifact_ids: list[Text]
    method: Text
    level: Literal["specified", "walkthrough", "implemented_test"]
    status: Literal["pass", "fail", "missing"]
    evidence_ids: list[Text]
    tested_artifact_digests: dict[str, Digest] = Field(default_factory=dict)
    tested_requirement_digests: dict[str, Digest] = Field(default_factory=dict)


class Workflow(Record):
    outcome: Text | None = None
    needs: list[Need] = Field(default_factory=list)
    requirements: list[Requirement] = Field(default_factory=list)
    states: list[State] = Field(default_factory=list)
    entry_state_id: Text | None = None
    impact_reviews: list[ImpactReview] = Field(default_factory=list)
    important_artifact_ids: list[Text] = Field(default_factory=list)
    validations: list[Validation] = Field(default_factory=list)
    dependencies: list[Text] | None = None
    dependency_review: Check = Field(default_factory=Check)
    state_review: Check = Field(default_factory=Check)
    human_control_review: Check = Field(default_factory=Check)
    action_boundaries: list[Text] | None = None


class Oversight(Record):
    basis: Literal["estimate", "measured"] = "estimate"
    review_minutes_per_case: Number | None = None
    correction_minutes_per_case: Number | None = None
    escalation_minutes_per_case: Number | None = None
    rework_minutes_per_case: Number | None = None
    residual_manual_minutes_per_case: Number | None = None
    owner_role: Text | None = None
    evidence_ids: list[Text] = Field(default_factory=list)


class Costs(Record):
    currency: Annotated[str, Field(pattern=r"^[A-Z]{3}$")] | None = None
    labor_cost_per_hour: Number | None = None
    baseline_nonlabor_cost_per_period: Number | None = None
    proposed_recurring_fixed_cost_per_period: Number | None = None
    proposed_nonlabor_cost_per_case: Number | None = None
    one_time_implementation_cost: Number | None = None
    evidence_ids: list[Text] = Field(default_factory=list)


class EvaluatorBurden(Record):
    preparation_elapsed_minutes: Number | None = None
    preparation_person_minutes: Number | None = None
    capture_reporting_minutes: Number | None = None
    elapsed_minutes: Number | None = None
    evaluator_minutes: Number | None = None
    participant_minutes: Number | None = None
    participant_count: Count | None = None
    adjudication_minutes: Number | None = None
    review_correction_cycles: Count | None = None
    tool_calls: Count | None = None
    model_calls: Count | None = None
    input_tokens: Count | None = None
    output_tokens: Count | None = None
    tool_model_cost: Number | None = None
    labor_cost_per_hour: Number | None = None
    currency: Annotated[str, Field(pattern=r"^[A-Z]{3}$")] | None = None
    evidence_ids: list[Text] = Field(default_factory=list)

    @model_validator(mode="after")
    def reporting_is_part_of_session(self):
        if self.elapsed_minutes is not None and self.capture_reporting_minutes is not None and self.capture_reporting_minutes > self.elapsed_minutes:
            raise ValueError("Capture/reporting time is a subset of session elapsed time")
        return self


class Finding(Record):
    id: Text
    severity: Literal["critical", "major", "minor"]
    status: Literal["open", "resolved", "accepted"]
    description: Text
    evidence_ids: list[Text]


class Handoff(Record):
    evidence_quality_review: Check = Field(default_factory=Check)
    reference_defect_ids: list[Text] | None = None
    reviewer_findings: list[Finding] | None = None
    unresolved_risks: list[Text] | None = None
    reference_review: Check = Field(default_factory=Check)
    findings_review: Check = Field(default_factory=Check)
    independent_review: Check = Field(default_factory=Check)
    hazard_analysis: Check = Field(default_factory=Check)
    validation_plan: Check = Field(default_factory=Check)
    mission_review: Check = Field(default_factory=Check)
    operational_evaluation_plan: Check = Field(default_factory=Check)
    risk_acceptance: Check = Field(default_factory=Check)
    decision_owner_role: Text | None = None
    commitment_scope: Text | None = None
    resource_limit: Text | None = None
    next_review_trigger: Text | None = None
    investment_rationale: Text | None = None


class OperationalEvidence(Record):
    status: Literal["not_collected", "collected_after_implementation"] = "not_collected"
    implemented_version: Text | None = None
    realistic_use_context: Text | None = None
    evidence_ids: list[Text] = Field(default_factory=list)
    metrics: dict[str, float] = Field(default_factory=dict)

    @model_validator(mode="after")
    def scope(self):
        import math
        if not all(math.isfinite(x) for x in self.metrics.values()):
            raise ValueError("Operational metrics must be finite")
        if self.status == "not_collected" and (self.metrics or self.evidence_ids or self.implemented_version):
            raise ValueError("Operational metrics require actual post-implementation evidence")
        if self.status == "collected_after_implementation" and not (
            self.implemented_version and self.realistic_use_context and self.evidence_ids
        ):
            raise ValueError("Operational evidence needs implementation version, realistic context and retained records")
        return self


class Assessment(Record):
    run_id: Text
    recorded_at: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}T.*(?:Z|[+-]\d{2}:\d{2})$")]
    versions: Versions
    evaluator_kind: Literal["human", "ai-assisted-human", "agent", "synthetic"]
    requested_profile: Profile
    evidence: list[Evidence]
    scope: Scope = Field(default_factory=Scope)
    previous_run_id: Text | None = None
    revision_summary: Text | None = None
    baseline: Baseline = Field(default_factory=Baseline)
    risk: Risk = Field(default_factory=Risk)
    workflow: Workflow = Field(default_factory=Workflow)
    operational_oversight: Oversight = Field(default_factory=Oversight)
    costs: Costs = Field(default_factory=Costs)
    evaluator_burden: EvaluatorBurden = Field(default_factory=EvaluatorBurden)
    handoff: Handoff = Field(default_factory=Handoff)
    operational_performance: OperationalEvidence = Field(default_factory=OperationalEvidence)

    @model_validator(mode="after")
    def integrity(self):
        from datetime import datetime
        datetime.fromisoformat(self.recorded_at.replace("Z", "+00:00"))
        if self.versions.model_dump() != versions():
            raise ValueError("Exact protocol/MCP/Skill/contract candidate versions required; migrate explicitly")
        if bool(self.previous_run_id) != bool(self.revision_summary) or self.previous_run_id == self.run_id:
            raise ValueError("A revision needs a different previous_run_id and a revision_summary")
        groups = {"evidence": self.evidence, "need": self.workflow.needs,
                  "requirement": self.workflow.requirements, "state": self.workflow.states,
                  "validation": self.workflow.validations, "finding": self.handoff.reviewer_findings or []}
        ids = {}
        for name, group in groups.items():
            keys = [x.id for x in group]
            if len(keys) != len(set(keys)):
                raise ValueError(f"Duplicate {name} IDs")
            ids[name] = set(keys)
        def refs(values, category):
            if len(values) != len(set(values)) or not set(values) <= ids[category]:
                raise ValueError(f"Duplicate or dangling {category} references: {values}")
        def evidence_refs(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key in ("evidence_ids", "artifact_ids", "important_artifact_ids", "source_ids", "discussion_evidence_ids", "reference_material_ids"):
                        refs(item, "evidence")
                    else:
                        evidence_refs(item)
            elif isinstance(value, list):
                for item in value:
                    evidence_refs(item)
        evidence_refs(self.model_dump())
        for requirement in self.workflow.requirements:
            refs(requirement.need_ids, "need")
            refs(requirement.validation_ids, "validation")
        for row in [*self.workflow.states, *self.workflow.validations]:
            refs(row.requirement_ids, "requirement")
        for row in self.workflow.impact_reviews:
            refs(row.requirement_ids, "requirement")
            if not set(row.affected_roles) <= set(self.scope.affected_roles or []):
                raise ValueError("Impact-review roles must resolve to scope.affected_roles")
        domains = [r.domain for r in self.workflow.impact_reviews]
        if len(domains) != len(set(domains)):
            raise ValueError("Duplicate impact-review domains")
        if self.workflow.entry_state_id is not None and self.workflow.entry_state_id not in ids['state']:
            raise ValueError("Proposed entry state does not resolve")
        for state in self.workflow.states:
            refs(state.next_state_ids, 'state')
            if state.terminal and state.next_state_ids:
                raise ValueError("A terminal proposed state cannot have outgoing paths")
        for validation in self.workflow.validations:
            if not set(validation.tested_artifact_digests) <= set(validation.artifact_ids):
                raise ValueError("Tested digest keys must be linked artifact IDs")
            if not set(validation.tested_requirement_digests) <= set(validation.requirement_ids):
                raise ValueError("Tested requirement digest keys must be linked requirement IDs")
        if self.evaluator_kind != "synthetic" and any(e.kind == "synthetic" for e in self.evidence):
            raise ValueError("Synthetic evidence cannot support a real/agent run")
        if self.operational_oversight.basis == "measured":
            observed_kinds = {"observed", "synthetic"} if self.evaluator_kind == "synthetic" else {"observed"}
            if self.operational_performance.status != "collected_after_implementation" or not self.operational_oversight.evidence_ids:
                raise ValueError("Measured operational oversight requires post-implementation observation context")
            if any(next(e for e in self.evidence if e.id == r).kind not in observed_kinds for r in self.operational_oversight.evidence_ids):
                raise ValueError("Measured oversight cannot be supported by an assumption or estimate")
        for ref in self.operational_performance.evidence_ids:
            entry = next(e for e in self.evidence if e.id == ref)
            if entry.kind not in ({"observed", "synthetic"} if self.evaluator_kind == "synthetic" else {"observed"}):
                raise ValueError("Operational performance requires observed evidence")
        return self


class Gate(Record):
    id: Text
    status: Literal["PASS", "FAIL", "MISSING", "NOT_EVALUATED"]
    reasons: list[str]


class AssessmentResult(Record):
    run_id: Text
    versions: Versions
    evaluator_kind: Text
    decision: Decision
    decision_scope: Literal["bounded_engineering_commitment"]
    risk_tier: Literal["low", "moderate", "high", "unknown"]
    requested_profile: Profile
    required_profile: Profile
    escalation_required: bool
    stop_at_gate: str | None
    gates: list[Gate]
    roi: dict
    evaluator_burden: dict
    operational_oversight: dict
    operational_performance: dict
    handoff_record: dict
    provenance: dict
    limitations: list[str]
    routing: dict
    attention_items: list[dict]
    assurance: dict


class FeedbackEntry(Record):
    id: Text
    source_person: Text | None
    source_date: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$")] | None
    recorded_on: Text
    context: Text
    feedback: Text | None
    permission: Literal["private", "attribution_approved"]
    permission_basis: Text
    changes: list[Text]
    affected_files: list[Text]
    affected_requirements: list[Text]
    validation_status: Literal["implemented_untested", "software_tests_only", "bounded_use_recorded"]


class UsabilityNotes(Record):
    first_use: bool | None = None
    participant_explanation_of_decision: Text | None = None
    confusing_questions: list[Text] = Field(default_factory=list)
    difficult_evidence: list[Text] = Field(default_factory=list)
    facilitator_prompts: Count | None = None
    next_action_understood: bool | None = None
    would_use_again: bool | None = None


class StudyJudgment(Record):
    requirement_id: Text
    judgment: Literal["defect", "no_defect", "abstain"]
    confidence_correct: Annotated[float, Field(ge=0, le=1, allow_inf_nan=False)] | None = None
    finding: str = ""


class StudyReview(Record):
    """Reviewer-side lock record. No reference answers or engineering decision are permitted."""
    study_version: Text
    participant_id: Text
    scenario_id: Text
    artifact_version: Text
    artifact_sha256: Digest
    requirement_ids: Annotated[list[Text], Field(min_length=1)]
    judgments: Annotated[list[StudyJudgment], Field(min_length=1)]
    review_minutes: Number
    perceived_handoff_readiness: Annotated[int, Field(ge=1, le=7)] | None = None
    global_confidence: Annotated[float, Field(ge=0, le=1, allow_inf_nan=False)] | None = None
    locked_at: Text
    reference_answers_disclosed: Literal[False]

    @model_validator(mode="after")
    def locked_before_disclosure(self):
        from datetime import datetime
        timestamp = datetime.fromisoformat(self.locked_at.replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            raise ValueError("Study judgment lock needs a timezone")
        ids = [j.requirement_id for j in self.judgments]
        if len(set(self.requirement_ids)) != len(self.requirement_ids) or len(set(ids)) != len(ids) or set(ids) != set(self.requirement_ids):
            raise ValueError("Record one judgment or explicit abstention for every requirement")
        return self


class PilotRun(Record):
    pilot_id: Text
    date: Text
    participant_role: Text
    sector: Text
    participant_id: Text
    permission: Literal["private", "anonymized_public", "attributed_public"]
    permission_evidence: Text
    anonymization: Text
    external_participant: bool
    actual_bounded_use: bool
    record_kind: Literal["actual", "synthetic_fixture"]
    profile_used: Profile
    risk_tier: Literal["low", "moderate", "high", "unknown"]
    elapsed_minutes: Number
    assessment: Assessment
    gates_passed: list[Text]
    gates_failed: list[Text]
    gates_missing: list[Text]
    gates_not_evaluated: list[Text]
    routing_status: Literal["REVIEW", "USE_FULL"]
    follow_up_reasons: list[Text]
    evidence_missing: list[Text]
    decision_before: Decision | None
    decision_after: Decision
    revision_triggered: Text | None
    participant_feedback: str | None
    observation_evidence_ids: Annotated[list[Text], Field(min_length=1)]
    usability: UsabilityNotes = Field(default_factory=UsabilityNotes)

    @model_validator(mode="after")
    def reconcile(self):
        from datetime import date
        from .engine import assess
        date.fromisoformat(self.date)
        if self.record_kind == "actual" and self.assessment.evaluator_kind not in ("human", "ai-assisted-human"):
            raise ValueError("Actual pilot needs retained human/assisted-human observations")
        if self.record_kind == "synthetic_fixture" and (self.actual_bounded_use or self.external_participant):
            raise ValueError("Synthetic pilot cannot count as external actual use")
        evidence = {e.id: e for e in self.assessment.evidence}
        if any(ref not in evidence for ref in self.observation_evidence_ids):
            raise ValueError("Pilot observation references must resolve")
        if self.record_kind == "actual" and any(evidence[r].kind != "observed" for r in self.observation_evidence_ids):
            raise ValueError("Actual pilot requires observed discussion/use records")
        result = assess(self.assessment)
        for attr, status in (("gates_passed", "PASS"), ("gates_failed", "FAIL"), ("gates_missing", "MISSING"), ("gates_not_evaluated", "NOT_EVALUATED")):
            if sorted(getattr(self, attr)) != sorted(g["id"] for g in result["gates"] if g["status"] == status):
                raise ValueError(f"{attr} disagrees with assessment")
        follow_up = sorted({reason for g in result['gates'] if g['status'] != 'PASS' for reason in g['reasons']})
        if self.routing_status != result['routing']['status'] or sorted(self.follow_up_reasons) != follow_up:
            raise ValueError("Pilot must preserve routing and all unevaluated/failed/missing follow-up reasons")
        if (self.decision_after != result["decision"] or self.risk_tier != result["risk_tier"]
                or self.profile_used != self.assessment.requested_profile
                or self.elapsed_minutes != self.assessment.evaluator_burden.elapsed_minutes):
            raise ValueError("Pilot decision/profile/risk/time disagrees with assessment")
        expected_missing = [reason for g in result["gates"] if g["status"] == "MISSING" for reason in g["reasons"]]
        if sorted(self.evidence_missing) != sorted(expected_missing):
            raise ValueError("Pilot missing-evidence list disagrees with evaluated missing gates")
        return self
