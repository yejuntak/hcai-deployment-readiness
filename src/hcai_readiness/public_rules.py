"""Official H.A.R.D.-grounded rules for low-cost public product reports.

Source boundary
---------------
This catalog is derived ONLY from the public H.A.R.D. research surface and the
official library it links to:
- /research/ai-readiness
- START-HERE
- ARTIFACT-REVIEW
- DECISION-REVIEW
- ENGINEERING-REASONING
- WORKSHEET
- QUICK-6 / FULL
- the stable HCAI criteria
- claims-and-governance / research-boundary / MCP+Skill documentation

Portfolio case studies, client work, private correspondence, and unrelated
takyejun.com pages are intentionally excluded.

These rules do not create a H.A.R.D. gate result. They turn inspectable public
signals into evidence-bounded report findings using the protocol's own reasoning
shape:

Observed -> Decision underneath -> What must be true -> If wrong -> Prove next.

A rule can be advisory-only. Advisory rules are useful H.A.R.D. questions but
must never reduce the Product Signal Grade merely because internal evidence is
not public.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .grade import DeveloperTrace, ReportFinding

RuleModule = Literal[
    "accessibility",
    "action_recovery",
    "privacy_data",
    "ai_transparency",
    "public_evidence",
]
HardLens = Literal[
    "experience_information",
    "workflow_architecture",
    "implementation_evidence",
    "people_operation",
]
DecisionSurfaceKind = Literal[
    "truth",
    "ownership",
    "state",
    "boundary",
    "contract",
    "failure_recovery",
    "time_ordering",
]
ObservationStatus = Literal["pass", "warning", "critical", "unknown"]
RuleEvidenceLevel = Literal[
    "unknown",
    "public_observation",
    "documented",
    "walkthrough",
    "implemented",
    "runtime_tested",
]


class OfficialSource(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    path: str
    section: str
    public_href: str


class PublicRule(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str
    module: RuleModule
    title: str
    hard_lenses: tuple[HardLens, ...]
    hard_criteria: tuple[str, ...]
    decision_surfaces: tuple[DecisionSurfaceKind, ...] = ()
    official_sources: tuple[OfficialSource, ...]
    score_included: bool = True
    public_ceiling: RuleEvidenceLevel = "public_observation"
    critical_permitted: bool = False
    intent: str
    observe: tuple[str, ...]
    pass_condition: str
    warning_condition: str
    decision_underneath: str
    must_be_true: str
    failure_condition: str
    prove_next: str
    claim_limit: str


class RuleObservation(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    rule_id: str
    status: ObservationStatus
    evidence_level: RuleEvidenceLevel
    evidence_locations: list[str] = Field(default_factory=list)
    observed: str = ""
    failure_mechanism: str | None = None
    consequence: str | None = None
    next_evidence: str | None = None

    @model_validator(mode="after")
    def evidence_boundary(self):
        if self.status == "unknown":
            if self.evidence_level != "unknown":
                raise ValueError("Unknown observations must use evidence_level=unknown")
            if not self.next_evidence:
                raise ValueError("Unknown observations must state what evidence is needed next")
        else:
            if self.evidence_level == "unknown":
                raise ValueError("Assessed observations require a non-unknown evidence level")
            if not self.evidence_locations:
                raise ValueError("Assessed observations require retained evidence locations")
        if self.status == "critical" and not (self.failure_mechanism and self.consequence):
            raise ValueError("Critical requires an observed failure mechanism and consequence")
        return self


def source(path: str, section: str, href: str) -> OfficialSource:
    return OfficialSource(path=path, section=section, public_href=href)


RESEARCH = "/research/ai-readiness"
LIB = "/static/research/ai-readiness/hard-0.3-preview-1/"


RULES: tuple[PublicRule, ...] = (
    PublicRule(
        id="EXP-TASK-01",
        module="accessibility",
        title="Information and competing choices support the current task",
        hard_lenses=("experience_information",),
        hard_criteria=("HCAI-1.1", "HCAI-1.3", "HCAI-2.1"),
        official_sources=(
            source("docs/research-content.gohtml", "Experience and information", RESEARCH+"#criteria"),
            source("protocol/0.3-preview.1/START-HERE.md", "The minimum review", LIB+"START-HERE.html"),
            source("src/hcai_readiness/criteria.json", "HCAI-1.1 / HCAI-1.3 / HCAI-2.1", RESEARCH+"/developers#rules"),
        ),
        intent="The visible product should make its current task, purpose, and consequential choices inspectable before visual polish is treated as evidence of completeness.",
        observe=(
            "labels and information hierarchy around the current task",
            "competing primary actions or unclear task boundaries",
            "whether the public surface states a purpose that can be connected to the behavior being reviewed",
        ),
        pass_condition="The inspected surface has a bounded task with labels and choices that are coherent with the stated purpose.",
        warning_condition="The surface looks complete, but the current task, competing choices, or acceptance intent is ambiguous.",
        decision_underneath="The product has chosen what the user is trying to accomplish and which choices deserve attention at this point.",
        must_be_true="The visible hierarchy and available actions must serve the same bounded purpose rather than forcing the reviewer to infer the intended workflow.",
        failure_condition="A polished result can conceal an unclear task boundary or competing choices that have not been tied to a real requirement.",
        prove_next="Name the exact workflow and acceptance condition, then walk the current task with the artifact revision being reviewed.",
        claim_limit="This is a bounded experience/information observation, not a complete usability or accessibility assessment.",
    ),
    PublicRule(
        id="EXP-AGENCY-02",
        module="accessibility",
        title="Affected people have visible correction, decline, challenge, or support paths",
        hard_lenses=("experience_information", "people_operation"),
        hard_criteria=("HCAI-1.4", "HCAI-3.2"),
        decision_surfaces=("ownership", "boundary", "failure_recovery"),
        official_sources=(
            source("src/hcai_readiness/criteria.json", "HCAI-1.4 Include the people who bear the consequences", RESEARCH+"/developers#rules"),
            source("protocol/0.3-preview.1/ENGINEERING-REASONING.md", "Ownership / Boundary / Failure and recovery", LIB+"ENGINEERING-REASONING.html"),
        ),
        intent="Human use and control cannot be assumed away when people bear the consequences of a workflow.",
        observe=(
            "ways to correct, decline, challenge, cancel, or seek support",
            "whether recourse appears near the consequential interaction rather than only in generic policy copy",
            "whether the visible path preserves enough context to continue or escalate",
        ),
        pass_condition="The inspected surface exposes a meaningful correction, decline, challenge, or support path appropriate to the visible consequence.",
        warning_condition="A recourse path exists but is generic, remote from the action, or unclear about what happens to current state.",
        critical_permitted=True,
        decision_underneath="The product has chosen when and how an affected person can interrupt, correct, or challenge the workflow.",
        must_be_true="A consequential workflow must preserve meaningful human agency where the declared context requires it.",
        failure_condition="A person can be affected by a consequential outcome without a realistic way to correct, decline, challenge, or escalate it.",
        prove_next="Walk one correction or escalation path end to end and retain the resulting state, owner, and recovery evidence.",
        claim_limit="A visible support or recourse path does not prove that the internal process resolves the issue correctly.",
    ),
    PublicRule(
        id="EXP-RECOVERY-03",
        module="accessibility",
        title="Visible failure states give a bounded recovery path",
        hard_lenses=("experience_information", "workflow_architecture"),
        hard_criteria=("HCAI-3.1",),
        decision_surfaces=("state", "failure_recovery"),
        official_sources=(
            source("docs/research-content.gohtml", "Workflow and architecture", RESEARCH+"#criteria"),
            source("src/hcai_readiness/criteria.json", "HCAI-3.1 Cover state transitions, edge cases and recovery", RESEARCH+"/developers#rules"),
        ),
        intent="A public error/failure state should make the next safe action inspectable rather than merely announce failure.",
        observe=(
            "normal, edge, and visible recovery states",
            "whether the state offers a specific next action",
            "whether cancel/resume/retry behavior is understandable from the user-facing surface",
        ),
        pass_condition="The inspected failure state identifies a bounded next action or recovery path and does not leave the user stranded.",
        warning_condition="Failure is visible, but recovery, resume, or resulting state is ambiguous.",
        decision_underneath="The product has chosen what a person should do when the happy path no longer applies.",
        must_be_true="A failed or interrupted interaction must lead to an explainable state with a bounded next action.",
        failure_condition="A person can repeat, abandon, or restart an action without understanding what state remains.",
        prove_next="Retain one failure walkthrough from trigger through recovery and record the exact artifact revision.",
        claim_limit="A visible recovery path is walkthrough/public-surface evidence only; it does not establish backend recovery correctness.",
    ),
    PublicRule(
        id="ACT-AUTHORITY-01",
        module="action_recovery",
        title="Consequential action authority is bounded",
        hard_lenses=("workflow_architecture", "people_operation"),
        hard_criteria=("HCAI-3.2", "HCAI-4.1"),
        decision_surfaces=("ownership", "boundary", "contract"),
        official_sources=(
            source("protocol/0.3-preview.1/ENGINEERING-REASONING.md", "Ownership / Boundary / Contract", LIB+"ENGINEERING-REASONING.html"),
            source("src/hcai_readiness/criteria.json", "HCAI-3.2 Make system truth and authority explicit", RESEARCH+"/developers#rules"),
        ),
        intent="A state-changing product should make authority a reviewable decision rather than treating the visible action as sufficient evidence.",
        observe=(
            "who or what is described as able to take the action",
            "visible approval, limit, confirmation, or escalation conditions",
            "whether automated and human authority are distinguished when public",
        ),
        pass_condition="The inspected evidence bounds who or what can perform the consequential action and under what declared conditions.",
        warning_condition="The consequential action is visible but authority, approval, or boundary conditions are only partially described.",
        critical_permitted=True,
        decision_underneath="The product delegates authority to a person or automated component to change consequential state.",
        must_be_true="Only an authorized actor may create the effect, within the declared scope and contract.",
        failure_condition="An unauthorized or over-broad actor can create a consequential side effect.",
        prove_next="Provide the authority/boundary contract and run one authorization/denial challenge against the exact implementation.",
        claim_limit="Public copy can show declared authority; enforcement remains unverified without implementation or runtime evidence.",
    ),
    PublicRule(
        id="ACT-REPEAT-02",
        module="action_recovery",
        title="Repeat, retry, and concurrent behavior is explicitly bounded",
        hard_lenses=("workflow_architecture", "implementation_evidence"),
        hard_criteria=("HCAI-3.1", "HCAI-3.2", "HCAI-4.2"),
        decision_surfaces=("state", "contract", "failure_recovery", "time_ordering"),
        official_sources=(
            source("protocol/0.3-preview.1/ENGINEERING-REASONING.md", "Time and ordering / Challenge scenarios", LIB+"ENGINEERING-REASONING.html"),
            source("src/hcai_readiness/criteria.json", "HCAI-3.1 / HCAI-3.2", RESEARCH+"/developers#rules"),
        ),
        intent="When an operation can repeat or race, the product must have an inspectable model for how many state changes should actually occur.",
        observe=(
            "repeat/retry behavior exposed in product or technical documentation",
            "duplicate submission or repeated action handling when observable",
            "ordering/concurrency guarantees when publicly documented",
        ),
        pass_condition="The inspected evidence explicitly defines or demonstrates safe repeated/concurrent behavior for the consequential operation.",
        warning_condition="Repeat/retry handling is mentioned but the expected invariant, authority, or evidence level is incomplete.",
        critical_permitted=True,
        decision_underneath="The system must decide whether repeated or concurrent requests represent one intended transition or several.",
        must_be_true="The number and ordering of state changes must remain consistent with the intended operation despite retries, duplicates, races, or late responses.",
        failure_condition="One intended operation can produce duplicate or contradictory state changes.",
        prove_next="Execute a bounded same-request-twice or ordering challenge and retain request identity, side-effect identity, and final state.",
        claim_limit="No public retry statement means unknown; it is not proof that duplicate protection is absent.",
    ),
    PublicRule(
        id="ACT-PARTIAL-03",
        module="action_recovery",
        title="Partial completion has an owned reconciliation path",
        hard_lenses=("workflow_architecture", "implementation_evidence"),
        hard_criteria=("HCAI-3.1", "HCAI-3.2"),
        decision_surfaces=("truth", "ownership", "state", "failure_recovery"),
        official_sources=(
            source("protocol/0.3-preview.1/ENGINEERING-REASONING.md", "Failure and recovery / Challenge scenarios", LIB+"ENGINEERING-REASONING.html"),
            source("src/hcai_readiness/criteria.json", "HCAI-3.1 / HCAI-3.2", RESEARCH+"/developers#rules"),
        ),
        intent="A multi-step consequential operation needs an explicit answer for what remains true when execution stops halfway.",
        observe=(
            "partial-failure behavior described publicly",
            "rollback, compensation, reconciliation, or manual recovery",
            "which state/result is shown to the person after interruption",
        ),
        pass_condition="The inspected evidence defines how partial completion is detected and reconciled to an explainable state.",
        warning_condition="A recovery idea is described, but authoritative final state, ownership, or proof remains incomplete.",
        critical_permitted=True,
        decision_underneath="The system must decide which state is authoritative after only part of a multi-step operation succeeds.",
        must_be_true="Interrupted work must converge to a coherent state with a named owner and bounded recovery path.",
        failure_condition="Different components or representations can disagree after partial completion and no accountable recovery model resolves them.",
        prove_next="Interrupt one multi-step action after a state change and retain the resulting state plus reconciliation evidence.",
        claim_limit="A public rollback/recovery statement is specified/documented evidence, not proof that recovery executed correctly.",
    ),
    PublicRule(
        id="ACT-DEPENDENCY-04",
        module="action_recovery",
        title="Slow, unavailable, or ambiguous dependencies have a bounded response",
        hard_lenses=("workflow_architecture", "implementation_evidence"),
        hard_criteria=("HCAI-3.1", "HCAI-3.2"),
        decision_surfaces=("contract", "failure_recovery", "time_ordering"),
        official_sources=(
            source("protocol/0.3-preview.1/ENGINEERING-REASONING.md", "When engineering deepening applies / Contract / Time and ordering", LIB+"ENGINEERING-REASONING.html"),
            source("protocol/0.3-preview.1/START-HERE.md", "Minimum review timeout example", LIB+"START-HERE.html"),
        ),
        intent="External/asynchronous dependencies can create decision ambiguity even when the visible happy path looks finished.",
        observe=(
            "timeout, unavailable-dependency, delayed-completion, or fallback behavior",
            "retry/exit/escalation language",
            "whether success is distinguished from unknown/late completion",
        ),
        pass_condition="The inspected evidence defines a bounded response to dependency delay/unavailability and an explainable resulting state.",
        warning_condition="Dependency failure is acknowledged but waiting, retry, fallback, or final-state communication is ambiguous.",
        critical_permitted=True,
        decision_underneath="The product chooses how long to wait, what to trust after an ambiguous response, and when to retry or exit.",
        must_be_true="A delayed or missing response must not be silently interpreted as success/failure when the external action may have a different authoritative state.",
        failure_condition="The product retries unsafely, waits indefinitely, or exposes the wrong state after an ambiguous dependency result.",
        prove_next="Run a bounded timeout/unavailable-dependency scenario and retain both visible state and authoritative final state.",
        claim_limit="Public failure copy shows intended handling only; actual dependency behavior remains unverified until executed.",
    ),
    PublicRule(
        id="DATA-PURPOSE-01",
        module="privacy_data",
        title="Data handling is bounded to the reviewed workflow and affected people",
        hard_lenses=("people_operation", "workflow_architecture"),
        hard_criteria=("HCAI-1.1", "HCAI-1.4"),
        decision_surfaces=("boundary", "ownership"),
        official_sources=(
            source("src/hcai_readiness/criteria.json", "HCAI-1.1 Bound the task / HCAI-1.4 affected people and privacy/security", RESEARCH+"/developers#rules"),
            source("protocol/0.3-preview.1/FULL-PROFILE.md", "G2 need, scope and requirements / impact reviews", LIB+"FULL-PROFILE.html"),
        ),
        intent="The report should distinguish the reviewed workflow's data boundary from a generic privacy promise.",
        observe=(
            "public description of relevant data classes and uses",
            "whether the product-specific workflow is distinguishable from company-wide policy",
            "affected-role or control language where visible",
        ),
        pass_condition="The public evidence gives a bounded description of data handling relevant to the reviewed workflow.",
        warning_condition="A general privacy statement exists but the reviewed workflow's data boundary remains difficult to interpret.",
        decision_underneath="The product has chosen what data is inside the workflow boundary, who is affected, and who owns relevant handling decisions.",
        must_be_true="The reviewed workflow must not rely on an unstated data boundary when privacy/security impact is relevant.",
        failure_condition="People cannot tell what data boundary applies to the consequential workflow being reviewed.",
        prove_next="Provide the workflow-level data boundary, affected roles, owner, and evidence used to support the privacy/security applicability judgment.",
        claim_limit="This is a H.A.R.D. scope/evidence observation, not a privacy-law compliance determination.",
    ),
    PublicRule(
        id="DATA-TRUTH-02",
        module="privacy_data",
        title="Authoritative truth and mutation ownership can be identified",
        hard_lenses=("workflow_architecture",),
        hard_criteria=("HCAI-2.1", "HCAI-3.2"),
        decision_surfaces=("truth", "ownership", "state"),
        official_sources=(
            source("docs/research-content.gohtml", "Workflow and architecture: what is true, and who may change it?", RESEARCH+"#criteria"),
            source("protocol/0.3-preview.1/ENGINEERING-REASONING.md", "Truth / Ownership / State", LIB+"ENGINEERING-REASONING.html"),
        ),
        score_included=False,
        intent="A consequential choice may depend on more than one representation of state; H.A.R.D. asks which one is authoritative and who can mutate it.",
        observe=(
            "public architecture/API/workflow statements identifying authoritative state",
            "visible cases where multiple representations may disagree",
            "ownership or reconciliation language when available",
        ),
        pass_condition="The supplied evidence identifies authoritative truth and mutation ownership for the consequential state.",
        warning_condition="More than one representation is involved but authority or reconciliation remains unclear.",
        decision_underneath="The product has chosen which record/rule wins when representations disagree.",
        must_be_true="Consequential state must have an inspectable authority and an owned mutation/reconciliation model.",
        failure_condition="Different actors or components can act on contradictory representations of the same consequential state.",
        prove_next="Provide a source-of-truth/ownership map and challenge one disagreement or stale-representation scenario.",
        claim_limit="Internal source-of-truth architecture is usually not public; lack of public evidence remains unknown and must not lower the public score.",
    ),
    PublicRule(
        id="AI-ROLE-01",
        module="ai_transparency",
        title="The AI role is bounded in the reviewed workflow",
        hard_lenses=("experience_information", "people_operation"),
        hard_criteria=("HCAI-1.1", "HCAI-1.4"),
        decision_surfaces=("boundary",),
        official_sources=(
            source("protocol/0.3-preview.1/PROTOCOL.md", "Scope and artifact population", RESEARCH+"/protocol"),
            source("protocol/0.3-preview.1/FULL-PROFILE.md", "Define scope and AI role", LIB+"FULL-PROFILE.html"),
        ),
        intent="H.A.R.D. distinguishes AI that created an artifact from AI operating inside the runtime workflow and asks the review to bound that role.",
        observe=(
            "whether AI is described as artifact creation, runtime behavior, or both",
            "what task/decision/action the AI is said to perform",
            "where human control or fallback begins when visible",
        ),
        pass_condition="The inspected public surface gives a bounded description of the AI role in the workflow.",
        warning_condition="AI is marketed broadly but its actual runtime role, authority, or boundary is ambiguous.",
        decision_underneath="The product has chosen which part of the workflow AI participates in and what responsibility remains elsewhere.",
        must_be_true="Claims about AI capability and control must be tied to the actual role being reviewed rather than inferred from AI authorship or branding.",
        failure_condition="A user or reviewer cannot tell whether AI merely generated an artifact, recommends an action, or executes consequential runtime behavior.",
        prove_next="State the exact AI role and walk one representative workflow showing where AI begins, ends, escalates, or hands off.",
        claim_limit="This rule scopes the AI role; it does not establish model quality or regulatory transparency compliance.",
    ),
    PublicRule(
        id="AI-FALLBACK-02",
        module="ai_transparency",
        title="Runtime AI uncertainty has recourse and fallback",
        hard_lenses=("workflow_architecture", "people_operation"),
        hard_criteria=("HCAI-1.4", "HCAI-3.1", "HCAI-3.2"),
        decision_surfaces=("boundary", "failure_recovery"),
        official_sources=(
            source("protocol/0.3-preview.1/PROTOCOL.md", "Runtime AI: output uncertainty, external dependencies, authority, user recourse and fallback", RESEARCH+"/protocol"),
            source("protocol/0.3-preview.1/ENGINEERING-REASONING.md", "Failure and recovery / Boundary", LIB+"ENGINEERING-REASONING.html"),
        ),
        intent="A runtime AI product should make uncertainty, recourse, and fallback inspectable where those conditions affect consequential behavior.",
        observe=(
            "fallback/refusal/escalation behavior",
            "user recourse when the AI cannot support the request",
            "whether context/state is preserved through fallback",
        ),
        pass_condition="The inspected flow exposes a bounded fallback or recourse path for unsupported or uncertain runtime AI behavior.",
        warning_condition="Uncertainty is acknowledged but fallback, escalation, or preserved state is ambiguous.",
        critical_permitted=True,
        decision_underneath="The product has chosen the boundary between AI continuation and alternative/human handling.",
        must_be_true="Unsupported or uncertain cases must reach a safe next state without inventing certainty or silently expanding authority.",
        failure_condition="The system continues consequential behavior despite insufficient basis and no meaningful fallback or recourse.",
        prove_next="Run one unsupported/uncertain case and retain the fallback or escalation state through completion.",
        claim_limit="Public fallback text can show intended behavior; implementation/runtime evidence is needed to establish actual handling.",
    ),
    PublicRule(
        id="AI-CLAIM-03",
        module="ai_transparency",
        title="Public AI claims stay proportional to the evidence shown",
        hard_lenses=("implementation_evidence", "experience_information"),
        hard_criteria=("HCAI-2.2", "HCAI-4.4", "HCAI-4.5"),
        official_sources=(
            source("docs/claims-and-governance.md", "Match the claim to the evidence", LIB+"claims-and-governance.html"),
            source("src/hcai_readiness/criteria.json", "HCAI-4.4 / HCAI-4.5", RESEARCH+"/developers#rules"),
        ),
        intent="A polished public claim should not imply operational performance, certification, or deployment readiness that the visible evidence cannot support.",
        observe=(
            "performance/capability claims and their stated basis",
            "whether artifact completeness is presented as runtime proof",
            "whether claim scope/version/population is visible when relevant",
        ),
        pass_condition="The public claim is bounded to the evidence type and scope actually presented.",
        warning_condition="The claim language is broader or more certain than the inspectable evidence basis.",
        decision_underneath="The product has chosen how much trust its public claim asks users to place in the evidence.",
        must_be_true="The claim must remain proportional to the evidence type, stage, population, and version that support it.",
        failure_condition="People infer runtime performance, certification, or broader capability from evidence that only supports a narrower statement.",
        prove_next="Attach the claim to its exact evidence type, scope, version, population, and measurement/check record.",
        claim_limit="This evaluates evidence proportionality, not the truth of an inaccessible underlying study or model.",
    ),
    PublicRule(
        id="EVID-STAGE-01",
        module="public_evidence",
        title="Evidence stages are not collapsed into one maturity claim",
        hard_lenses=("implementation_evidence",),
        hard_criteria=("HCAI-2.3", "HCAI-4.4"),
        official_sources=(
            source("protocol/0.3-preview.1/PROTOCOL.md", "Four evidence levels stay independent", RESEARCH+"/protocol"),
            source("protocol/0.3-preview.1/ARTIFACT-REVIEW.md", "Keep four evidence columns", RESEARCH+"/artifact-review"),
        ),
        intent="Specified, walkthrough, implemented, and runtime-tested evidence answer different questions and must remain visibly distinct.",
        observe=(
            "whether public evidence labels specification/demo/implementation/runtime test distinctly",
            "whether a prototype/demo is described as if it proves runtime behavior",
            "whether actual execution evidence is tied to the exact context",
        ),
        pass_condition="The inspected evidence clearly distinguishes its evidence stage and does not upgrade one stage by implication.",
        warning_condition="The product presents a demo, prototype, generated implementation, or document completeness as stronger evidence than it actually is.",
        decision_underneath="The product has chosen what level of proof a public artifact is supposed to establish.",
        must_be_true="Evidence from one stage must not silently stand in for a later stage.",
        failure_condition="A reviewer treats a specified or walkthrough result as implemented/runtime proof and makes a broader commitment than the evidence supports.",
        prove_next="Label the current evidence stage and add the smallest next check needed to move to the next claimed level.",
        claim_limit="This is an evidence-labeling judgment; it does not establish that all defects were found.",
    ),
    PublicRule(
        id="EVID-TRACE-02",
        module="public_evidence",
        title="Important evidence is bound to the exact artifact or decision context",
        hard_lenses=("implementation_evidence",),
        hard_criteria=("HCAI-2.2", "HCAI-4.5"),
        decision_surfaces=("contract",),
        official_sources=(
            source("src/hcai_readiness/criteria.json", "HCAI-2.2 Trace the exact artifact to a check", RESEARCH+"/developers#rules"),
            source("protocol/0.3-preview.1/ENGINEERING-REASONING.md", "Evidence mapping", LIB+"ENGINEERING-REASONING.html"),
        ),
        intent="A passing check becomes stale when a material choice, assumption, context, requirement, or artifact changes.",
        observe=(
            "version/date/revision identity on public evidence",
            "whether a validation/check names what it actually evaluated",
            "whether changed context is distinguishable from the earlier checked state",
        ),
        pass_condition="The inspected evidence identifies the artifact/revision or context it actually supports.",
        warning_condition="Evidence exists but its relationship to the current version or decision context is ambiguous.",
        decision_underneath="The product has chosen whether evidence remains reconstructable after the artifact or context changes.",
        must_be_true="A changed consequential choice, assumption, state context, dependency, authority boundary, or artifact must not silently inherit an old pass.",
        failure_condition="A stale result is treated as evidence for a materially changed product state.",
        prove_next="Bind the next check to the exact artifact/version and decision context, retaining the prior record separately.",
        claim_limit="Version identity improves provenance; it does not authenticate evidence truth by itself.",
    ),
    PublicRule(
        id="EVID-UNKNOWN-03",
        module="public_evidence",
        title="Unknowns remain visible instead of becoming pass or fail",
        hard_lenses=("implementation_evidence",),
        hard_criteria=("HCAI-4.2", "HCAI-4.5"),
        official_sources=(
            source("protocol/0.3-preview.1/START-HERE.md", "Unknown is visible, not a pass", LIB+"START-HERE.html"),
            source("protocol/0.3-preview.1/ARTIFACT-REVIEW.md", "Unassessed items remain counted", RESEARCH+"/artifact-review"),
            source("protocol/0.3-preview.1/ENGINEERING-REASONING.md", "Do not turn every unknown into a defect", LIB+"ENGINEERING-REASONING.html"),
        ),
        score_included=False,
        intent="The report must preserve uncertainty instead of rewarding missing evidence or inventing a defect from inaccessible evidence.",
        observe=(
            "whether inaccessible/internal facts are explicitly marked unknown/unassessed",
            "whether unknowns name the next evidence needed",
            "whether the report avoids converting absence of public evidence into a factual absence claim",
        ),
        pass_condition="Unassessed facts remain visibly unknown and name a bounded next evidence action.",
        warning_condition="The report blurs not-observed, not-applicable, failed, and passed conditions.",
        decision_underneath="The review has chosen whether uncertainty is preserved or hidden inside a score.",
        must_be_true="Missing evidence must remain distinguishable from demonstrated failure and from justified non-applicability.",
        failure_condition="The report becomes overconfident because inaccessible evidence is silently converted into pass or fail.",
        prove_next="Record the missing evidence, owner, and exact check/artifact that would resolve the unknown.",
        claim_limit="This is a report-integrity rule and is intentionally excluded from the numeric Product Signal Grade.",
    ),
    PublicRule(
        id="HARD-ASSUMPTION-04",
        module="public_evidence",
        title="Consequential assumptions are stated as revisitable claims",
        hard_lenses=("workflow_architecture", "implementation_evidence"),
        hard_criteria=("HCAI-2.1", "HCAI-4.2"),
        decision_surfaces=("truth", "state", "boundary", "contract", "failure_recovery", "time_ordering"),
        official_sources=(
            source("protocol/0.3-preview.1/ENGINEERING-REASONING.md", "Assumptions are first-class claims", LIB+"ENGINEERING-REASONING.html"),
            source("protocol/0.3-preview.1/WORKSHEET.md", "Engineering reasoning deepening", RESEARCH+"/worksheet"),
        ),
        score_included=False,
        intent="A consequential assumption should be inspectable as a claim with status, consequence-if-false, evidence, and revisit trigger.",
        observe=(
            "explicit assumptions in supplied/public technical evidence",
            "whether an assumption is supported, conflicted, or still unassessed",
            "whether a revisit trigger/evidence need is named",
        ),
        pass_condition="The consequential assumption is separately stated with evidence status, consequence-if-false, and revisit trigger.",
        warning_condition="A material assumption is buried in rationale or treated as true without an inspectable evidence lifecycle.",
        decision_underneath="The current product choice depends on a statement about the system or context remaining true.",
        must_be_true="The assumption must remain evidence-bounded and reopen when its trigger changes.",
        failure_condition="A hidden assumption silently controls a consequential choice after the surrounding context changes or conflicts with it.",
        prove_next="Record the assumption separately, name the evidence needed, and define what change should reopen it.",
        claim_limit="This is an advisory deepening rule and is excluded from the public numeric grade unless actual H.A.R.D. evidence is supplied.",
    ),
    PublicRule(
        id="HARD-CHALLENGE-05",
        module="public_evidence",
        title="A consequential choice has a bounded disconfirming challenge",
        hard_lenses=("workflow_architecture", "implementation_evidence"),
        hard_criteria=("HCAI-4.2", "HCAI-4.3"),
        official_sources=(
            source("docs/research-content.gohtml", "Challenge the model", RESEARCH+"#method"),
            source("protocol/0.3-preview.1/ENGINEERING-REASONING.md", "Challenge scenarios", LIB+"ENGINEERING-REASONING.html"),
        ),
        score_included=False,
        intent="H.A.R.D. asks what would have to be true for an important choice or model to be wrong, then bounds the evidence needed to check it.",
        observe=(
            "stated failure/challenge scenarios in supplied evidence",
            "expected invariant/behavior",
            "consequence and evidence level when assessed",
        ),
        pass_condition="The consequential choice has a bounded challenge with an invariant, consequence, and explicit evidence level when assessed.",
        warning_condition="The rationale is persuasive but no disconfirming condition or bounded check is retained.",
        decision_underneath="The team has chosen what evidence could falsify the current model rather than only collecting confirming explanations.",
        must_be_true="The choice must remain open to evidence that can contradict its assumptions or decision surfaces.",
        failure_condition="A plausible explanation is treated as proof because the review never asks what could make the model wrong.",
        prove_next="Define one bounded challenge, expected invariant, consequence, affected requirement, and stage-appropriate evidence.",
        claim_limit="This is an advisory H.A.R.D. deepening rule; it is not a requirement to enumerate every edge case.",
    ),
    PublicRule(
        id="HARD-NEXT-06",
        module="public_evidence",
        title="The next proof is the smallest coherent slice",
        hard_lenses=("implementation_evidence", "people_operation"),
        hard_criteria=("HCAI-4.3",),
        decision_surfaces=("state", "failure_recovery"),
        official_sources=(
            source("protocol/0.3-preview.1/ENGINEERING-REASONING.md", "Smallest coherent next slice", LIB+"ENGINEERING-REASONING.html"),
            source("src/hcai_readiness/criteria.json", "HCAI-4.3 Limit the next commitment to a coherent slice", RESEARCH+"/developers#rules"),
        ),
        score_included=False,
        intent="The report should end in a bounded evidence-producing next step rather than a generic redesign or build recommendation.",
        observe=(
            "whether the recommended next action tests the important assumption end to end",
            "whether the action includes only the required input/validation/state/side-effect/recovery/outcome elements",
            "whether an owner or revisit trigger is identified when supplied",
        ),
        pass_condition="The proposed next action is a bounded coherent slice that can resolve the important uncertainty.",
        warning_condition="The next action is a broad rebuild, generic best practice, or more analysis without a specific evidence target.",
        decision_underneath="The team chooses how much work to fund before the important assumption has been exposed to evidence.",
        must_be_true="The next commitment must be small enough to learn and coherent enough to exercise the consequential path.",
        failure_condition="The team builds broad surface area before testing the assumption that actually controls the decision.",
        prove_next="Define the smallest end-to-end slice that exposes the unresolved assumption and name the owner/revisit trigger.",
        claim_limit="This is a H.A.R.D. commitment-shaping prompt, not automatic authorization to build or deploy.",
    ),
)


RULE_INDEX = {rule.id: rule for rule in RULES}


def rule_catalog(*, scored_only: bool = False) -> list[dict]:
    rows = [rule for rule in RULES if not scored_only or rule.score_included]
    return [rule.model_dump() for rule in rows]


def evaluate_public_observation(observation: RuleObservation) -> dict:
    rule = RULE_INDEX.get(observation.rule_id)
    if rule is None:
        raise ValueError("Unknown public-signal rule")

    if observation.status == "critical" and not rule.critical_permitted:
        raise ValueError("This rule does not permit a public critical label")

    observed = observation.observed or (
        "The reviewed public surface did not provide enough evidence to assess this rule."
        if observation.status == "unknown"
        else rule.title
    )
    next_evidence = observation.next_evidence or rule.prove_next

    trace = DeveloperTrace(
        observed=observed,
        decision_underneath=rule.decision_underneath,
        must_be_true=rule.must_be_true,
        if_wrong=(
            observation.failure_mechanism
            + (" Consequence: " + observation.consequence if observation.consequence else "")
            if observation.failure_mechanism
            else rule.failure_condition
        ),
        prove_next=next_evidence,
    )

    if observation.status == "unknown":
        finding = ReportFinding(
            id=rule.id,
            module=rule.module,
            title=rule.title,
            status="unknown",
            evidence_level="unknown",
            summary=rule.claim_limit,
            next_evidence=next_evidence,
            developer_trace=trace,
        )
    else:
        summary = rule.pass_condition if observation.status == "pass" else rule.warning_condition
        if observation.status == "critical":
            summary = observation.failure_mechanism + " " + observation.consequence
        finding = ReportFinding(
            id=rule.id,
            module=rule.module,
            title=rule.title,
            status=observation.status,
            evidence_level=observation.evidence_level,
            summary=summary,
            evidence_locations=observation.evidence_locations,
            next_evidence=next_evidence,
            developer_trace=trace,
        )

    return {
        "rule": rule.model_dump(),
        "score_included": rule.score_included,
        "finding": finding.model_dump(),
        "claim_limit": rule.claim_limit,
        "hard_provenance": {
            "lenses": list(rule.hard_lenses),
            "criteria": list(rule.hard_criteria),
            "decision_surfaces": list(rule.decision_surfaces),
            "official_sources": [item.model_dump() for item in rule.official_sources],
        },
    }
