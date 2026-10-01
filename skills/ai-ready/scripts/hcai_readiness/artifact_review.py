# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yejun Tak
"""Stage-bounded artifact review and explicit evaluator-measure eligibility.

These deterministic checks validate supplied records, not the truth of observations.
A current rationale is never evidence of a creator's historical thought process.
"""
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
from .versions import versions

Text = Annotated[str, Field(min_length=1)]
ArtifactPopulation = Literal["ai_generated", "runtime_ai", "both", "neither", "unknown"]
EvaluatorKind = Literal["human", "ai-assisted-human", "agent", "synthetic"]
ReviewMode = Literal["artifact_review", "independent_evaluation"]
Stage = Literal["specification_handoff", "prototype_handoff", "implementation_review", "runtime_release_review"]
DecisionSurfaceKind = Literal["truth", "ownership", "state", "boundary", "contract", "failure_recovery", "time_ordering"]
ChallengeEvidenceLevel = Literal["walkthrough", "implemented", "runtime_tested"]
DeepeningTrigger = Literal[
    "persistent_state_mutation", "external_side_effect", "irreversible_action", "privileged_or_tenant_boundary",
    "unreliable_or_async_dependency", "repeat_or_concurrent_operation", "money_or_data_loss",
    "material_scale_or_cost_assumption", "current_promise_depends_on_deferred_work",
    "ambiguous_source_of_truth", "other"
]
LEVELS = ("specified", "walkthrough", "implemented", "runtime_tested")
STAGE_LEVELS = {
    "specification_handoff": LEVELS[:2],
    "prototype_handoff": LEVELS[:2],
    "implementation_review": LEVELS[:3],
    "runtime_release_review": LEVELS,
}


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)


class ArtifactVersions(Record):
    protocol: Text
    mcp: Text
    skill: Text
    contract: Text


class EvaluatorValidity(Record):
    """Unknown role/order facts are ineligible, not silently assumed independent."""
    reference_frozen_before_evaluation: bool | None = None
    reference_independent_of_findings: bool | None = None
    evaluator_authored_artifact: bool | None = None
    evaluator_authored_reference: bool | None = None
    evaluator_is_adjudicator: bool | None = None
    matches_independently_confirmed: bool | None = None
    findings_locked_before_reference: bool | None = None
    expected_recall_locked_before_reference: bool | None = None
    omission_subset_frozen: bool | None = None
    criterion_independently_established: bool | None = None


def evaluator_metric_reasons(validity: EvaluatorValidity, mode: str,
                             judgment_locked_before_reference: bool | None) -> dict[str, list[str]]:
    """Return exclusion reasons; reference author = adjudicator alone is permitted."""
    base = []
    if mode != "independent_evaluation":
        base.append("independent_evaluation_not_selected")
    for field, code in (("reference_frozen_before_evaluation", "reference_not_prospectively_frozen"),
                        ("reference_independent_of_findings", "reference_not_independent_of_findings"),
                        ("findings_locked_before_reference", "findings_not_locked_before_reference")):
        if getattr(validity, field) is not True:
            base.append(code)
    for field, code in (("evaluator_authored_artifact", "self_evaluation"),
                        ("evaluator_authored_reference", "reference_known_to_evaluator")):
        if getattr(validity, field) is not False:
            base.append(code if getattr(validity, field) is True else "role_independence_unknown")
    if validity.evaluator_is_adjudicator is None:
        base.append("adjudicator_independence_unknown")
    elif validity.evaluator_is_adjudicator and validity.matches_independently_confirmed is not True:
        base.append("self_adjudicated_matches_unconfirmed")
    recall = list(dict.fromkeys(base))
    gap = recall + ([] if validity.expected_recall_locked_before_reference is True else ["expectation_not_locked_before_reference"])
    omissions = recall + ([] if validity.omission_subset_frozen is True else ["omission_subset_not_frozen"])
    # False-ready judgments have a separate criterion/lock requirement, not a recall denominator.
    judgment = [r for r in recall if r not in ("findings_not_locked_before_reference", "self_adjudicated_matches_unconfirmed")]
    if judgment_locked_before_reference is not True:
        judgment.append("judgment_not_locked_before_reference")
    if validity.criterion_independently_established is not True:
        judgment.append("criterion_not_independently_established")
    return {"reference_set_recall_percent": recall, "expected_recall_gap_pp": gap,
            "requirements_omission_recognition_percent": omissions,
            "false_ready_acceptance_percent": list(dict.fromkeys(judgment))}


class EvidenceCheck(Record):
    status: Literal["pass", "fail", "unassessed", "not_applicable"] = "unassessed"
    evidence_locations: list[Text] = Field(default_factory=list)
    reason: Text | None = None

    @model_validator(mode="after")
    def evidence_for_claim(self):
        if self.status in ("pass", "fail") and not self.evidence_locations:
            raise ValueError("Assessed pass/fail needs evidence locations, including an inspected absence")
        if self.status == "not_applicable" and self.reason is None:
            raise ValueError("Not applicable requires an explicit reason")
        return self


class ArtifactCheck(Record):
    id: Text
    acceptance_check: Text
    scope: Literal["current", "deferred", "excluded"] = "current"
    exclusion_reason: Text | None = None
    current_dependency: bool = False
    specified: EvidenceCheck = Field(default_factory=EvidenceCheck)
    walkthrough: EvidenceCheck = Field(default_factory=EvidenceCheck)
    implemented: EvidenceCheck = Field(default_factory=EvidenceCheck)
    runtime_tested: EvidenceCheck = Field(default_factory=EvidenceCheck)

    @model_validator(mode="after")
    def exclusions(self):
        if self.scope != "current" and (self.exclusion_reason is None or self.current_dependency):
            raise ValueError("Exclusions need a recorded reason and cannot hide a current dependency")
        return self


class Alternative(Record):
    description: Text
    evidence_locations: list[Text] = Field(default_factory=list)


class AssumptionRecord(Record):
    """One explicit assumption that can be challenged and revisited independently."""
    id: Text
    statement: Text
    status: Literal["supported", "conflicted", "unassessed"] = "unassessed"
    consequence_if_false: Text
    evidence_needed: Text
    evidence_locations: list[Text] = Field(default_factory=list)
    revisit_trigger: Text

    @model_validator(mode="after")
    def evidence_boundary(self):
        if self.status in ("supported", "conflicted") and not self.evidence_locations:
            raise ValueError("Supported/conflicted assumptions need retained evidence")
        return self


class DecisionSurfaceRecord(Record):
    """One externalized part of the system model. It is review evidence, not recovered private reasoning."""
    id: Text
    kind: DecisionSurfaceKind
    question: Text
    current_model: Text | None = None
    status: Literal["supported", "conflicted", "unassessed", "not_applicable"] = "unassessed"
    evidence_locations: list[Text] = Field(default_factory=list)
    consequence_if_wrong: Text | None = None
    evidence_needed: Text | None = None
    revisit_trigger: Text | None = None
    reason: Text | None = None

    @model_validator(mode="after")
    def evidence_boundary(self):
        if self.status in ("supported", "conflicted") and (self.current_model is None or not self.evidence_locations):
            raise ValueError("Supported/conflicted decision surfaces need the current model and retained evidence")
        if self.status == "unassessed" and self.evidence_needed is None:
            raise ValueError("An unassessed decision surface needs the evidence or inspection required next")
        if self.status == "not_applicable" and self.reason is None:
            raise ValueError("A not-applicable decision surface needs a bounded reason")
        return self


class ChallengeScenario(Record):
    """A bounded attempt to disconfirm an important choice or system model."""
    id: Text
    condition: Text
    claim_at_risk: Text
    expected_behavior_or_invariant: Text
    consequence_if_mishandled: Text
    affected_check_ids: list[Text] = Field(default_factory=list)
    status: Literal["pass", "fail", "unassessed"] = "unassessed"
    evidence_level: ChallengeEvidenceLevel | None = None
    evidence_locations: list[Text] = Field(default_factory=list)
    next_evidence: Text | None = None

    @model_validator(mode="after")
    def evidence_boundary(self):
        if self.status in ("pass", "fail") and (not self.evidence_locations or self.evidence_level is None):
            raise ValueError("Assessed challenge scenarios need retained evidence and an explicit evidence level")
        if self.status == "unassessed" and self.next_evidence is None:
            raise ValueError("An unassessed challenge scenario needs the next evidence or check")
        if self.status == "unassessed" and self.evidence_level is not None:
            raise ValueError("Unassessed challenge scenarios cannot claim an evidence level")
        return self


class ChoiceRecord(Record):
    id: Text
    purpose: Text
    criteria: list[Text] = Field(default_factory=list)
    observed_choice: Text | None
    observed_evidence_locations: list[Text] = Field(default_factory=list)
    historical_alternatives: list[Alternative] = Field(default_factory=list)
    proposed_alternatives: list[Alternative] = Field(default_factory=list)
    alternatives_review: Text | None = None
    rationale: Text | None
    rationale_provenance: Literal["documented", "reported", "new", "unknown"]
    rationale_evidence_locations: list[Text] = Field(default_factory=list)
    impacts_and_tradeoffs: list[Text] = Field(default_factory=list)
    assumptions: list[AssumptionRecord] = Field(default_factory=list)
    affected_check_ids: list[Text] = Field(default_factory=list)
    engineering_deepening_required: bool
    deepening_rationale: Text
    deepening_triggers: list[DeepeningTrigger] = Field(default_factory=list)
    required_surface_kinds: list[DecisionSurfaceKind] = Field(default_factory=list)
    decision_surfaces: list[DecisionSurfaceRecord] = Field(default_factory=list)
    challenge_scenarios: list[ChallengeScenario] = Field(default_factory=list)
    next_coherent_slice: Text | None = None
    human_decision: Literal["accepted", "revise", "pending"] = "pending"
    human_decision_owner: Text | None = None
    human_decision_evidence_locations: list[Text] = Field(default_factory=list)
    verification_evidence_locations: list[Text] = Field(default_factory=list)
    follow_up: Text | None = None
    follow_up_owner: Text | None = None

    @model_validator(mode="after")
    def provenance(self):
        if any(not alt.evidence_locations for alt in self.historical_alternatives):
            raise ValueError("Historical alternatives need source evidence; newly proposed alternatives stay separate")
        if self.rationale_provenance == "unknown" and self.rationale is not None:
            raise ValueError("An unknown historical rationale cannot contain a generated explanation; use new")
        if self.rationale_provenance != "unknown" and self.rationale is None:
            raise ValueError("Known or new rationale needs a concise inspectable justification")
        if self.rationale_provenance in ("documented", "reported") and not self.rationale_evidence_locations:
            raise ValueError("Historical rationale needs a document or attributed report location")
        if self.human_decision != "pending" and (self.human_decision_owner is None or not self.human_decision_evidence_locations):
            raise ValueError("A human disposition requires an accountable human owner and retained confirmation evidence; an agent cannot invent approval")
        if len(self.required_surface_kinds) != len(set(self.required_surface_kinds)):
            raise ValueError("Required decision-surface kinds must be unique")
        for group, label in ((self.assumptions, "assumption"), (self.decision_surfaces, "decision surface"), (self.challenge_scenarios, "challenge scenario")):
            ids = [row.id for row in group]
            if len(ids) != len(set(ids)):
                raise ValueError(f"Duplicate {label} IDs within one consequential choice")
        if self.engineering_deepening_required:
            if not self.deepening_triggers:
                raise ValueError("Engineering deepening requires at least one recorded trigger")
            if not self.required_surface_kinds:
                raise ValueError("Engineering deepening requires explicit decision-surface kinds")
            if not self.challenge_scenarios:
                raise ValueError("Engineering deepening requires at least one bounded challenge scenario")
            if self.next_coherent_slice is None:
                raise ValueError("Engineering deepening requires a smallest coherent next slice")
        return self


def choice_gaps(choice: ChoiceRecord) -> list[str]:
    gaps = []
    for field in ("criteria", "observed_choice", "observed_evidence_locations", "impacts_and_tradeoffs", "assumptions",
                  "verification_evidence_locations", "follow_up", "follow_up_owner", "human_decision_owner"):
        if not getattr(choice, field):
            gaps.append(field + "_missing")
    if not (choice.historical_alternatives or choice.proposed_alternatives or choice.alternatives_review):
        gaps.append("alternatives_review_missing")
    if choice.rationale is None:
        gaps.append("current_choice_justification_missing")
    if choice.human_decision == "pending":
        gaps.append("human_decision_pending")
    for assumption in choice.assumptions:
        if assumption.status == "unassessed":
            gaps.append("assumption_" + assumption.id + "_unassessed")
        elif assumption.status == "conflicted":
            gaps.append("assumption_" + assumption.id + "_conflicted")
    if choice.engineering_deepening_required:
        active = [row for row in choice.decision_surfaces if row.status != "not_applicable"]
        for kind in choice.required_surface_kinds:
            if not any(row.kind == kind for row in active):
                gaps.append("decision_surface_" + kind + "_missing")
        for row in active:
            if row.status == "unassessed":
                gaps.append("decision_surface_" + row.id + "_unassessed")
            elif row.status == "conflicted":
                gaps.append("decision_surface_" + row.id + "_conflicted")
        for row in choice.challenge_scenarios:
            if row.status == "unassessed":
                gaps.append("challenge_" + row.id + "_unassessed")
            elif row.status == "fail":
                gaps.append("challenge_" + row.id + "_failed")
        if not choice.next_coherent_slice:
            gaps.append("next_coherent_slice_missing")
    return gaps


class ArtifactFinding(Record):
    id: Text
    description: Text
    acceptance: Literal["matched_reference", "novel_accepted", "unsupported", "duplicate", "unresolved"]
    scope: Literal["current", "deferred", "unclear"] = "current"
    current_dependency: bool = False
    scope_reason: Text | None = None
    proposed_severity: Literal["critical", "major", "minor", "undetermined"] = "undetermined"
    adjudicated_severity: Literal["critical", "major", "minor", "undetermined"] = "undetermined"
    criterion_or_novel_risk: Text | None = None
    failure_mechanism: Text | None = None
    consequence: Text | None = None
    evidence_locations: list[Text] = Field(default_factory=list)
    resolution: Literal["open", "remediated", "accepted_risk"] = "open"
    remediation_evidence_locations: list[Text] = Field(default_factory=list)

    @model_validator(mode="after")
    def acceptance_and_scope(self):
        if self.scope == "deferred" and (self.current_dependency or not self.scope_reason):
            raise ValueError("Deferred findings need a scope reason and no current dependency")
        if self.acceptance in ("matched_reference", "novel_accepted"):
            if not self.criterion_or_novel_risk or not self.evidence_locations:
                raise ValueError("Accepted defects need an applicable criterion or novel risk and evidence")
            if self.adjudicated_severity == "critical" and not (self.failure_mechanism and self.consequence):
                raise ValueError("Critical needs a supported failure mechanism and consequential outcome; omission alone is insufficient")
        if self.resolution == "remediated" and not self.remediation_evidence_locations:
            raise ValueError("Remediation needs verification evidence")
        return self


class ArtifactReview(Record):
    versions: ArtifactVersions
    run_id: Text
    artifact_version: Text
    criterion_version: Text
    artifact_population: ArtifactPopulation
    artifact_kind: Literal["specification", "prototype", "code"]
    stage: Stage
    mode: ReviewMode
    evaluator_kind: EvaluatorKind
    criteria_timing: Literal["prospective", "retrospective", "unknown"]
    requirements: Annotated[list[ArtifactCheck], Field(min_length=1)]
    recovery: list[ArtifactCheck]
    zero_recovery_reason: Text | None = None
    important_choice_ids: Annotated[list[Text], Field(min_length=1)]
    choices: list[ChoiceRecord]
    findings: list[ArtifactFinding] = Field(default_factory=list)
    evaluator_validity: EvaluatorValidity = Field(default_factory=EvaluatorValidity)
    judgment_locked_before_reference: bool | None = None

    @model_validator(mode="after")
    def unique_and_linked(self):
        if self.versions.model_dump() != versions():
            raise ValueError("Exact current protocol/MCP/Skill/contract versions required; migrate explicitly")
        ids = [row.id for row in [*self.requirements, *self.recovery]]
        if len(ids) != len(set(ids)):
            raise ValueError("Requirement and recovery IDs must be unique")
        for group in (self.choices, self.findings):
            keys = [row.id for row in group]
            if len(keys) != len(set(keys)):
                raise ValueError("Duplicate choice or finding IDs")
        if len(self.important_choice_ids) != len(set(self.important_choice_ids)):
            raise ValueError("Duplicate important choice IDs")
        if not any(row.scope == "current" for row in self.requirements):
            raise ValueError("At least one current mandatory requirement is required")
        if not any(row.scope == "current" for row in self.recovery) and not self.zero_recovery_reason:
            raise ValueError("Zero applicable recovery scenarios require an applicability reason")
        for choice in self.choices:
            if not set(choice.affected_check_ids) <= set(ids):
                raise ValueError("Affected checks must resolve to declared requirements or recovery")
            for challenge in choice.challenge_scenarios:
                if not set(challenge.affected_check_ids) <= set(ids):
                    raise ValueError("Challenge checks must resolve to declared requirements or recovery")
        return self


def _coverage(rows: list[ArtifactCheck], required_levels: tuple[str, ...]) -> dict:
    current = [row for row in rows if row.scope == "current"]
    total = len(current)
    levels = {}
    for level in LEVELS:
        counts = {status: sum(getattr(row, level).status == status for row in current)
                  for status in ("pass", "fail", "unassessed", "not_applicable")}
        levels[level] = {"total": total, **counts,
                         "coverage_percent": round(100 * counts["pass"] / total, 6) if total else None}
    verified = sum(all(getattr(row, level).status == "pass" for level in required_levels) for row in current)
    failed = sum(any(getattr(row, level).status == "fail" for level in required_levels) for row in current)
    return {"total": total, "verified": verified, "failed": failed, "unassessed": total - verified - failed,
            "coverage_percent": round(100 * verified / total, 6) if total else None,
            "evidence_levels": levels, "excluded_ids": [row.id for row in rows if row.scope != "current"]}


def review_artifact(review: ArtifactReview) -> dict:
    required_levels = STAGE_LEVELS[review.stage]
    requirements = _coverage(review.requirements, required_levels)
    recovery = _coverage(review.recovery, required_levels)
    indexed = {choice.id: choice for choice in review.choices}
    choice_issues = {key: choice_gaps(indexed[key]) if key in indexed else ["important_choice_record_missing"]
                     for key in review.important_choice_ids}
    choice_issues = {key: value for key, value in choice_issues.items() if value}
    revised = [key for key in review.important_choice_ids if key in indexed and indexed[key].human_decision == "revise"]
    critical = [f.id for f in review.findings if f.scope == "current"
                and f.acceptance in ("matched_reference", "novel_accepted")
                and f.adjudicated_severity == "critical" and f.resolution != "remediated"]
    major = [f.id for f in review.findings if f.scope == "current"
             and f.acceptance in ("matched_reference", "novel_accepted")
             and f.adjudicated_severity == "major" and f.resolution != "remediated"]
    finding_gaps = [f.id for f in review.findings if f.scope == "unclear" or
                    (f.scope == "current" and (f.acceptance == "unresolved" or
                     (f.acceptance in ("matched_reference", "novel_accepted") and f.adjudicated_severity == "undetermined")))]
    gaps = []
    if review.artifact_population == "unknown":
        gaps.append("artifact_population_unknown")
    if review.criteria_timing == "unknown":
        gaps.append("criteria_timing_unknown")
    if review.artifact_kind != "code" and review.stage in ("implementation_review", "runtime_release_review"):
        gaps.append("implemented_artifact_required_for_selected_stage")
    deepening_failures = [key for key, values in choice_issues.items()
                          if any(value.endswith("_conflicted") or value.endswith("_failed") for value in values)]
    if requirements["failed"] or recovery["failed"] or critical or major or revised or deepening_failures:
        status, disposition = "nonready", "Hold for remediation"
    elif requirements["unassessed"] or recovery["unassessed"] or choice_issues or finding_gaps or gaps:
        status, disposition = "nonready", "Insufficient evidence"
    else:
        status, disposition = "ready", "Eligible for declared stage handoff review"
    reasons = evaluator_metric_reasons(review.evaluator_validity, review.mode, review.judgment_locked_before_reference)
    # Artifact records do not include a frozen answer key or adjudicated matched counts.
    reasons = {metric: list(dict.fromkeys([*codes, "adjudicated_reference_counts_not_supplied"]))
               for metric, codes in reasons.items() if metric != "false_ready_acceptance_percent"}
    warnings = []
    if review.evaluator_kind in ("agent", "synthetic"):
        warnings.append("Not an observed human evaluation; keep this evaluator population separate.")
    if review.criteria_timing == "retrospective":
        warnings.append("Retrospective criteria support descriptive artifact review, not a prospectively frozen experiment.")
    if review.mode == "independent_evaluation":
        warnings.append("Use the corrected diagnostic session with independent reference counts for evaluator measures; selecting a mode does not establish eligibility.")
    return {"versions": versions(), "run_id": review.run_id, "artifact_version": review.artifact_version,
            "criterion_version": review.criterion_version, "artifact_population": review.artifact_population,
            "artifact_kind": review.artifact_kind, "stage": review.stage, "mode": review.mode,
            "evaluator_kind": review.evaluator_kind, "criteria_timing": review.criteria_timing,
            "required_evidence_levels": list(required_levels), "criterion_status": status, "disposition": disposition,
            "requirements": requirements, "recovery": recovery, "unresolved_critical_ids": critical, "unresolved_major_ids": major,
            "choice_issues": choice_issues, "choices_requiring_revision": revised,
            "deepening_required_ids": [choice.id for choice in review.choices if choice.engineering_deepening_required],
            "deepening_failure_ids": deepening_failures,
            "finding_scope_or_adjudication_gaps": finding_gaps, "evidence_gaps": gaps,
            "evaluator_metrics": {metric: None for metric in reasons}, "metric_ineligibility_reasons": reasons,
            "choices": [choice.model_dump() for choice in review.choices], "inputs": review.model_dump(),
            "warnings": warnings,
            "interpretation": "Descriptive evidence review for the declared stage. Four evidence levels remain independent; unassessed in-scope items remain in denominators. New rationale is a present-day proposal, never proof of historical reasoning. The result does not authorize release or demonstrate protocol effectiveness."}
