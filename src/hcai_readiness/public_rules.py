"""Evidence-bounded public-surface rules for H.A.R.D.-adjacent reports.

These rules are not H.A.R.D. gates and do not create a H.A.R.D. decision.
They translate public, inspectable product signals into deterministic findings
that preserve the protocol's reasoning shape:

Observed -> Decision underneath -> What must be true -> If wrong -> Prove next.

The catalog intentionally distinguishes:
- universal-ish public signals that may contribute to Product Signal Grade;
- advisory review prompts that should never become numeric penalties.

Context-specific portfolio decisions are generalized into decision-quality rules
rather than copied as universal prescriptions.
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


class PublicRule(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str
    module: RuleModule
    title: str
    hard_lenses: tuple[HardLens, ...]
    hard_criteria: tuple[str, ...]
    decision_surfaces: tuple[DecisionSurfaceKind, ...] = ()
    portfolio_principles: tuple[str, ...] = ()
    score_included: bool = True
    public_ceiling: RuleEvidenceLevel = "public_observation"
    absence_is_failure: bool = False
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


# Portfolio principle strings are intentionally descriptive rather than normative.
# They preserve where the product-thinking pattern came from without claiming
# that a context-specific design decision is universal.
RULES: tuple[PublicRule, ...] = (
    PublicRule(
        id="A11Y-HIERARCHY-01",
        module="accessibility",
        title="Task hierarchy is structurally legible",
        hard_lenses=("experience_information",),
        hard_criteria=("HCAI-1.4", "HCAI-2.1"),
        portfolio_principles=(
            "takyejun.com design system: one h1 per page; subsection hierarchy remains explicit",
            "supporting copy should not compete with the primary task",
        ),
        intent="The product should expose a task hierarchy that people and assistive technology can parse without reconstructing the visual design.",
        observe=(
            "heading hierarchy and landmark structure",
            "primary versus secondary actions",
            "whether supporting meta copy competes with the task",
        ),
        pass_condition="The inspected surface has a coherent heading/landmark hierarchy and one clearly prioritized task at the current decision point.",
        warning_condition="Hierarchy exists but competing actions, labels, or structural omissions make the task harder to parse.",
        decision_underneath="The product has chosen which information and action deserve attention first.",
        must_be_true="The visual priority and semantic structure must point to the same task and remain understandable without relying on appearance alone.",
        failure_condition="A person or assistive technology must infer the task from layout, or multiple actions compete without a clear decision hierarchy.",
        prove_next="Retain an accessibility/structure walkthrough of the exact release and correct the smallest hierarchy conflict.",
        claim_limit="Public markup can support a structural observation, not a complete usability or WCAG conformance claim.",
    ),
    PublicRule(
        id="A11Y-FOCUS-02",
        module="accessibility",
        title="Keyboard focus and task order are observable",
        hard_lenses=("experience_information", "implementation_evidence"),
        hard_criteria=("HCAI-1.4", "HCAI-2.3"),
        portfolio_principles=(
            "takyejun.com design system: visible focus states and skip-to-content are first-class behavior",
            "keyboard actions should not depend on hidden pointer-only behavior",
        ),
        intent="A public interactive flow should expose a usable keyboard path and visible focus rather than making the visual mock imply accessibility.",
        observe=(
            "focus-visible styling",
            "tab order through primary task controls",
            "focus movement after validation errors or modal transitions",
        ),
        pass_condition="Primary public task controls are keyboard reachable in a coherent order with visible focus.",
        warning_condition="Keyboard access exists but order, focus visibility, or post-error focus behavior is inconsistent.",
        decision_underneath="The product has defined how non-pointer users move through the same task state.",
        must_be_true="Focus order must track the task order and remain visible as state changes.",
        failure_condition="A user can become unable to locate focus, reach an action, or recover after validation using the keyboard.",
        prove_next="Run and retain a keyboard-only walkthrough of the exact public flow, including at least one validation/recovery state.",
        claim_limit="A public keyboard walkthrough is evidence for the inspected path only, not complete accessibility conformance.",
    ),
    PublicRule(
        id="A11Y-STATUS-03",
        module="accessibility",
        title="Consequential status is not encoded by one visual channel",
        hard_lenses=("experience_information", "people_operation"),
        hard_criteria=("HCAI-1.4",),
        portfolio_principles=(
            "T-Mobile case library: consequential severity used reinforcing channels such as color, count, and position",
            "one visual channel is a single point of failure for accessibility and speed",
        ),
        intent="Important status should remain perceivable when color, position, or a single visual affordance is unavailable.",
        observe=(
            "status labels/text in addition to color",
            "icons/counts/position used as reinforcing rather than sole signals",
            "screen-reader accessible status wording when inspectable",
        ),
        pass_condition="Consequential statuses have at least one non-color semantic cue and do not depend on a single visual encoding.",
        warning_condition="Status is technically present but one visual channel carries most of the meaning.",
        decision_underneath="The product has chosen how urgency and state are communicated under constrained perception and rapid scanning.",
        must_be_true="A person must be able to distinguish consequential states without decoding color alone.",
        failure_condition="A consequential state becomes ambiguous when color is unavailable or visual scanning conditions change.",
        prove_next="Retain a visual and screen-reader/semantic check for the exact status components.",
        claim_limit="This rule checks redundant status communication, not all contrast, vision, or assistive-technology requirements.",
    ),
    PublicRule(
        id="A11Y-RECOVERY-04",
        module="accessibility",
        title="Errors explain a recovery action",
        hard_lenses=("experience_information", "workflow_architecture"),
        hard_criteria=("HCAI-1.4", "HCAI-3.1"),
        decision_surfaces=("failure_recovery",),
        portfolio_principles=(
            "takyejun.com case library: generic error -> named failure type + actionable next step",
            "recovery copy should be informational rather than punitive",
        ),
        intent="An error should help a person recover rather than merely announce that something failed.",
        observe=(
            "plain-language cause or condition when appropriate",
            "specific next action",
            "preservation of entered state when visible",
        ),
        pass_condition="The observed error state names a useful condition and gives a specific recovery action.",
        warning_condition="An error is visible but recovery guidance is generic, ambiguous, or forces unnecessary restart.",
        decision_underneath="The product has chosen what a person can do after the happy path breaks.",
        must_be_true="The failure state must preserve enough context and agency for the person to continue, correct, retry, or escalate safely.",
        failure_condition="A user is stranded, loses work unnecessarily, or repeats a failing action without knowing how state changed.",
        prove_next="Walk one real failure path and retain the error state, preserved state, and successful recovery result.",
        claim_limit="Public error copy can show recovery intent; it cannot establish backend recovery correctness.",
    ),
    PublicRule(
        id="A11Y-DISCLOSURE-05",
        module="accessibility",
        title="Complexity is progressively disclosed around the current task",
        hard_lenses=("experience_information",),
        hard_criteria=("HCAI-1.4", "HCAI-2.1"),
        portfolio_principles=(
            "Vita case library: curate the few most relevant items first; keep the full panel accessible on demand",
            "information hierarchy is a product decision, not decoration",
        ),
        score_included=False,
        intent="Dense products should reveal depth when it serves the current task rather than exposing all available information by default.",
        observe=(
            "initial task surface versus deeper detail",
            "whether secondary metrics/actions remain accessible on demand",
            "whether disclosure follows a clear user decision",
        ),
        pass_condition="The current task exposes the minimum coherent information needed to decide while preserving access to deeper detail.",
        warning_condition="The product exposes broad system depth before the current decision is clear, or hides necessary detail behind unclear affordances.",
        decision_underneath="The team has chosen which complexity is necessary now versus later.",
        must_be_true="The first view must support the current decision without permanently hiding information required for deeper work.",
        failure_condition="Users must either synthesize too much at once or cannot reach the depth needed to verify a decision.",
        prove_next="Observe the first-task path with target users and retain which information was needed before versus after the decision.",
        claim_limit="This is an advisory product-review prompt, not a numeric accessibility penalty or a universal item-count rule.",
    ),
    PublicRule(
        id="ACT-AUTHORITY-01",
        module="action_recovery",
        title="Consequential action authority is bounded",
        hard_lenses=("workflow_architecture", "people_operation"),
        hard_criteria=("HCAI-3.2", "HCAI-4.1"),
        decision_surfaces=("ownership", "boundary", "contract"),
        intent="A product that changes external state should make the actor, authority, and boundary inspectable rather than treating the button as the whole decision.",
        observe=(
            "who or what is allowed to take the action",
            "visible approval/limit/escalation conditions",
            "user recourse or interruption path",
        ),
        pass_condition="The inspected public surface or documentation bounds who/what can perform the consequential action and under what conditions.",
        warning_condition="The action is visible but authority, approval limits, or recourse are only partially described.",
        critical_permitted=True,
        decision_underneath="The product has delegated authority to a person or automated component to create a consequential side effect.",
        must_be_true="Only an authorized actor may create the effect, within the declared scope and limits, with a defined recourse path.",
        failure_condition="An unauthorized or over-broad actor can create a consequential external change that a user cannot safely interrupt or challenge.",
        prove_next="Provide the action-boundary contract and run one bounded authorization/denial challenge against the exact implementation.",
        claim_limit="Public copy can reveal declared authority. It cannot prove enforcement without implementation/runtime evidence.",
    ),
    PublicRule(
        id="ACT-DUPLICATE-02",
        module="action_recovery",
        title="Repeat and retry behavior is defined",
        hard_lenses=("workflow_architecture", "implementation_evidence"),
        hard_criteria=("HCAI-3.1", "HCAI-3.2", "HCAI-4.2"),
        decision_surfaces=("state", "contract", "failure_recovery", "time_ordering"),
        intent="State-changing operations should survive repeated requests, retries, refreshes, or replay without silently multiplying the side effect.",
        observe=(
            "duplicate submission protections",
            "idempotency/replay behavior in public technical documentation",
            "visible repeated-action state",
        ),
        pass_condition="The inspected evidence defines or demonstrates safe behavior for repeated consequential operations.",
        warning_condition="Retry/repeat handling is described incompletely or only at walkthrough level.",
        critical_permitted=True,
        decision_underneath="The system must decide whether two apparently identical requests represent one intended action or two.",
        must_be_true="A repeated request must map to the intended number of state changes even across retries, refreshes, or transport ambiguity.",
        failure_condition="One intended operation can create duplicate financial, data, messaging, or account side effects.",
        prove_next="Execute the same consequential request twice against the exact implementation and retain request identity, side-effect identity, and final state.",
        claim_limit="Absence of public idempotency documentation is unknown, not proof that duplicate protection does not exist.",
    ),
    PublicRule(
        id="ACT-PARTIAL-03",
        module="action_recovery",
        title="Partial completion has a reconciliation path",
        hard_lenses=("workflow_architecture", "implementation_evidence"),
        hard_criteria=("HCAI-3.1", "HCAI-3.2"),
        decision_surfaces=("truth", "state", "failure_recovery"),
        intent="Multi-step consequential actions need an inspectable answer for what happens when execution stops after some state has already changed.",
        observe=(
            "partial-failure documentation",
            "rollback/compensation/reconciliation behavior",
            "user-visible state after interrupted execution",
        ),
        pass_condition="The inspected evidence defines how partially completed work is reconciled to a coherent state.",
        warning_condition="A recovery path is described but ownership, authoritative final state, or proof is incomplete.",
        critical_permitted=True,
        decision_underneath="The system must decide which state is authoritative after only part of a multi-step action succeeds.",
        must_be_true="Interrupted work must converge to an explainable state with an owner and bounded recovery path.",
        failure_condition="Different systems or representations can disagree after partial completion, leaving the user unable to know what actually happened.",
        prove_next="Interrupt one multi-step action after a state change and retain the reconciliation outcome across affected systems.",
        claim_limit="A public rollback statement is specified/documented evidence only unless the exact recovery is executed.",
    ),
    PublicRule(
        id="ACT-DEPENDENCY-04",
        module="action_recovery",
        title="Dependency delay and outage behavior is bounded",
        hard_lenses=("workflow_architecture", "implementation_evidence"),
        hard_criteria=("HCAI-3.1", "HCAI-3.2"),
        decision_surfaces=("contract", "failure_recovery", "time_ordering"),
        intent="A product depending on external services should have a bounded response to timeout, unavailability, and delayed completion.",
        observe=(
            "timeout/fallback/retry language",
            "status communication for delayed dependencies",
            "safe exit or escalation path",
        ),
        pass_condition="The inspected evidence defines a bounded timeout/failure response and a safe next state.",
        warning_condition="Dependency failure is acknowledged but retry, timeout, fallback, or ownership is ambiguous.",
        decision_underneath="The product has chosen how long to wait, when to retry, and what state to expose when a dependency does not respond normally.",
        must_be_true="Waiting, retry, fallback, and final-state communication must not create contradictory or endless behavior.",
        failure_condition="A dependency outage can leave the product spinning indefinitely, retrying unsafely, or reporting success before authoritative completion.",
        prove_next="Run a bounded dependency timeout/unavailable scenario and retain the visible state plus resulting system state.",
        claim_limit="Public status language can show intended handling; runtime behavior remains unverified until executed.",
    ),
    PublicRule(
        id="ACT-RECOURSE-05",
        module="action_recovery",
        title="People can interrupt, correct, decline, or escalate",
        hard_lenses=("people_operation", "experience_information"),
        hard_criteria=("HCAI-1.4", "HCAI-3.2"),
        decision_surfaces=("ownership", "boundary", "failure_recovery"),
        intent="Human agency must remain explicit where the product can create consequential outcomes.",
        observe=(
            "cancel/decline/correct controls",
            "human escalation or support path",
            "recourse after automated action",
        ),
        pass_condition="The inspected surface gives a meaningful path to correct, decline, interrupt, or escalate consequential behavior.",
        warning_condition="Recourse exists but is delayed, hidden, generic, or unclear about what state will be preserved.",
        critical_permitted=True,
        decision_underneath="The product has chosen when a person may override or challenge automated or workflow behavior.",
        must_be_true="A person affected by a consequential action must have a realistic path to intervene or seek correction when context requires it.",
        failure_condition="The system can create a consequential outcome with no meaningful way for the affected person to interrupt, correct, or challenge it.",
        prove_next="Walk an escalation/correction path end to end and retain the resulting state and responsible owner.",
        claim_limit="A support link alone does not prove effective recourse.",
    ),
    PublicRule(
        id="DATA-PURPOSE-01",
        module="privacy_data",
        title="Public data use has a bounded purpose",
        hard_lenses=("people_operation", "workflow_architecture"),
        hard_criteria=("HCAI-1.4", "HCAI-3.2"),
        decision_surfaces=("boundary", "ownership"),
        intent="People should be able to understand what data the product uses for the reviewed workflow and why.",
        observe=(
            "privacy/product documentation naming data classes and purposes",
            "product-specific versus company-wide ambiguity",
            "training or secondary-use statements when relevant",
        ),
        pass_condition="Public documentation identifies the relevant data classes and a bounded use purpose for the product/workflow.",
        warning_condition="A general privacy statement exists but product-specific purpose or secondary use is ambiguous.",
        decision_underneath="The product has chosen which data is necessary for the workflow and what uses are inside versus outside that purpose.",
        must_be_true="Data use and secondary use must remain within the disclosed and authorized boundary for the reviewed context.",
        failure_condition="People cannot tell whether data collected for one task may be reused, retained, or exposed for another.",
        prove_next="Provide the product-level data inventory, purpose mapping, and owner for the reviewed workflow.",
        claim_limit="Public documentation supports disclosure observations, not a privacy-compliance determination.",
    ),
    PublicRule(
        id="DATA-DELETE-02",
        module="privacy_data",
        title="Deletion or correction has a visible path and boundary",
        hard_lenses=("people_operation", "workflow_architecture"),
        hard_criteria=("HCAI-1.4", "HCAI-3.2"),
        decision_surfaces=("truth", "ownership", "boundary"),
        intent="A deletion/correction promise should identify how a person requests it and what system boundary the promise covers.",
        observe=(
            "request path",
            "retention/deletion statement",
            "downstream/subprocessor propagation statement when public",
        ),
        pass_condition="The public surface documents how to request correction/deletion and gives a meaningful retention or scope boundary.",
        warning_condition="A request path exists but retention timing, exceptions, or propagation is too broad to interpret.",
        decision_underneath="The product has chosen which representation is authoritative after a person asks to remove or correct data.",
        must_be_true="The user-facing promise must map to an owned process and a coherent authoritative state across relevant representations.",
        failure_condition="The user believes data was changed or deleted while downstream or derived representations remain inconsistent without disclosure.",
        prove_next="Provide the deletion/correction propagation map and a retained verification for one bounded request.",
        claim_limit="Public policy language cannot prove propagation across internal systems.",
    ),
    PublicRule(
        id="DATA-TRUTH-03",
        module="privacy_data",
        title="Authoritative data truth is identifiable for consequential state",
        hard_lenses=("workflow_architecture",),
        hard_criteria=("HCAI-2.1", "HCAI-3.2"),
        decision_surfaces=("truth", "ownership", "state"),
        score_included=False,
        intent="When multiple representations exist, the review should identify which one wins and who may change it.",
        observe=(
            "public architecture/API docs when available",
            "language describing source of record or synchronization",
            "visible contradictory representations",
        ),
        pass_condition="The supplied/public evidence identifies the authoritative representation and mutation owner for the consequential state.",
        warning_condition="Multiple representations are visible or documented without a clear authority/reconciliation model.",
        decision_underneath="The system has chosen which record is authoritative when representations disagree.",
        must_be_true="Every consequential representation must either be authoritative or have a defined relationship to the authority.",
        failure_condition="Two representations can disagree and different actors act on different truths.",
        prove_next="Provide a source-of-truth map and demonstrate one disagreement/reconciliation scenario.",
        claim_limit="This is a H.A.R.D.-style advisory prompt; lack of public architecture evidence remains unknown and should not reduce the public score.",
    ),
    PublicRule(
        id="AI-DISCLOSURE-01",
        module="ai_transparency",
        title="AI role is disclosed at the point it matters",
        hard_lenses=("experience_information", "people_operation"),
        hard_criteria=("HCAI-1.1", "HCAI-1.4"),
        intent="People should be able to distinguish an AI-assisted/automated role when that knowledge changes how they interpret, verify, or challenge the interaction.",
        observe=(
            "AI/automated-agent labeling",
            "role disclosure near consequential interactions",
            "human handoff distinction",
        ),
        pass_condition="The inspected flow identifies the AI/automation role where it materially affects interpretation or recourse.",
        warning_condition="AI is disclosed only in distant policy/marketing copy while the consequential interaction itself is ambiguous.",
        decision_underneath="The product has chosen what a person needs to know about who/what is producing the interaction or taking the action.",
        must_be_true="The disclosure must appear early enough to change verification, consent, or recourse behavior when those are consequential.",
        failure_condition="A person reasonably treats an automated judgment/action as a human-authored or independently verified one.",
        prove_next="Review the exact consequential flow with the disclosure visible and retain the user-facing state.",
        claim_limit="Disclosure quality is context-specific; this is not a legal transparency determination.",
    ),
    PublicRule(
        id="AI-CAPABILITY-02",
        module="ai_transparency",
        title="AI capability claims are bounded to observable scope",
        hard_lenses=("experience_information", "implementation_evidence"),
        hard_criteria=("HCAI-2.1", "HCAI-4.4"),
        intent="Marketing/product claims should not imply broader autonomy, accuracy, or evidence than the reviewed product surface supports.",
        observe=(
            "capability language",
            "scope qualifiers and exclusions",
            "whether claims distinguish draft/help/recommendation from autonomous action",
        ),
        pass_condition="Public capability language is bounded to a clear task/context and does not imply stronger evidence than is shown.",
        warning_condition="Claims are broad, absolute, or mix assistance with autonomous authority without clear scope.",
        decision_underneath="The company has chosen how much trust and authority its public wording asks users to grant the product.",
        must_be_true="The claim scope must not exceed the behavior and evidence users can reasonably expect from the product.",
        failure_condition="People rely on a broader capability or level of assurance than the product can support.",
        prove_next="Provide the claim definition, applicable population/context, and retained evidence used to support it.",
        claim_limit="The rule evaluates claim boundedness, not underlying model quality by itself.",
    ),
    PublicRule(
        id="AI-SOURCE-03",
        module="ai_transparency",
        title="Consequential AI output exposes its evidence/source boundary",
        hard_lenses=("implementation_evidence", "experience_information"),
        hard_criteria=("HCAI-2.1", "HCAI-2.2"),
        portfolio_principles=(
            "T-Mobile AI Copilot case: every answer links back to source data",
            "trust should come from inspectability rather than unverifiable expert claims",
        ),
        intent="Where an AI answer informs a consequential decision, the product should expose what source/evidence supports the answer or clearly state when it cannot.",
        observe=(
            "source links/citations/data provenance",
            "answer-to-source relationship",
            "fallback when no adequate source is available",
        ),
        pass_condition="The inspected consequential answer exposes its source/evidence boundary or explicitly declines unsupported specificity.",
        warning_condition="Source information exists but is detached, generic, or too weak to inspect the consequential claim.",
        decision_underneath="The product has chosen whether users can verify the basis of an AI-mediated answer.",
        must_be_true="A consequential answer should not ask for more trust than its inspectable evidence can support.",
        failure_condition="A confident answer can drive action while the user cannot inspect or challenge its basis.",
        prove_next="Retain one answer with its exact source chain and one low-evidence case showing the fallback behavior.",
        claim_limit="A citation/link can improve inspectability but does not prove the source itself is correct.",
    ),
    PublicRule(
        id="AI-RECOVERY-04",
        module="ai_transparency",
        title="AI uncertainty has a bounded fallback",
        hard_lenses=("people_operation", "workflow_architecture"),
        hard_criteria=("HCAI-1.4", "HCAI-3.1", "HCAI-3.2"),
        decision_surfaces=("boundary", "failure_recovery"),
        intent="An AI-mediated flow should define what happens when confidence, source quality, or task fit is inadequate.",
        observe=(
            "uncertainty language",
            "refusal/fallback/handoff",
            "preservation of context during escalation",
        ),
        pass_condition="The inspected flow has a bounded fallback or escalation when the AI cannot support the requested action/answer.",
        warning_condition="The product acknowledges uncertainty but recovery or handoff is generic or loses task context.",
        critical_permitted=True,
        decision_underneath="The product has chosen the boundary between AI continuation and human/alternative handling.",
        must_be_true="Low-evidence or unsupported situations must route to a safe next state without fabricating certainty.",
        failure_condition="The system continues with consequential confidence despite missing basis or no adequate path to recovery.",
        prove_next="Run one unsupported/low-evidence case and retain the fallback/handoff state through completion.",
        claim_limit="Public fallback copy can show intended behavior; executed evidence is needed to establish actual behavior.",
    ),
    PublicRule(
        id="AI-CLAIM-05",
        module="ai_transparency",
        title="Performance claims identify their measurement basis",
        hard_lenses=("implementation_evidence",),
        hard_criteria=("HCAI-2.2", "HCAI-4.4"),
        intent="A numeric performance claim should identify enough context to understand what was measured.",
        observe=(
            "metric definition",
            "population/task/context",
            "date/version or measurement window",
            "method/reference when public",
        ),
        pass_condition="The public claim identifies the metric and enough population/context/version information to interpret it.",
        warning_condition="A numeric or superlative performance claim is shown without enough measurement context to understand what it represents.",
        decision_underneath="The company has chosen how much evidence is attached to a public claim that may influence product trust.",
        must_be_true="The reported number must remain bound to the population, task, version, and method that produced it.",
        failure_condition="Users generalize a narrow or stale measurement to contexts it never tested.",
        prove_next="Publish or provide the metric definition, evaluated population/task, version/date, and retained measurement method.",
        claim_limit="This rule checks claim traceability, not whether the measurement design is statistically adequate.",
    ),
    PublicRule(
        id="AI-NAV-06",
        module="ai_transparency",
        title="Natural language has a defined product job",
        hard_lenses=("experience_information",),
        hard_criteria=("HCAI-1.3", "HCAI-2.1"),
        portfolio_principles=(
            "T-Mobile case library: natural language earns its place when it removes navigation rather than merely adding a chat box",
            "quick replies teach useful question shapes through use",
        ),
        score_included=False,
        intent="An AI conversational surface should solve a concrete navigation/decision problem rather than exist as an ornamental second interface.",
        observe=(
            "what task the assistant shortcuts",
            "relationship to existing navigation/workflow",
            "discovery guidance such as useful prompts or quick replies",
        ),
        pass_condition="The conversational surface removes or compresses a real task cost and preserves access to the underlying source/workflow.",
        warning_condition="The assistant duplicates existing search/navigation without a clear user need or creates a disconnected second mental model.",
        decision_underneath="The team has chosen what interaction cost natural language is meant to remove.",
        must_be_true="The AI surface must make the user job easier without hiding the system state or source needed to act.",
        failure_condition="The chat layer adds ambiguity or another navigation layer without improving the underlying decision.",
        prove_next="Compare the same task with and without the AI surface and retain task steps, time, and source visibility.",
        claim_limit="This is an advisory design/product rule, not a universal requirement that every AI product reduce navigation.",
    ),
    PublicRule(
        id="EVID-VERSION-01",
        module="public_evidence",
        title="Public evidence identifies the version or change boundary",
        hard_lenses=("implementation_evidence",),
        hard_criteria=("HCAI-2.2", "HCAI-4.5"),
        intent="A report or product claim should be tied to a version/change boundary so later changes do not silently inherit stale evidence.",
        observe=(
            "version/release/date identity",
            "change history",
            "links to exact reviewed documentation or artifact",
        ),
        pass_condition="The inspected public evidence identifies a release/date/version boundary sufficient to distinguish materially different states.",
        warning_condition="Documentation exists but it is difficult to tell which release or change state the claim refers to.",
        decision_underneath="The product has chosen how users/reviewers distinguish current evidence from stale evidence.",
        must_be_true="Material changes must not silently inherit a previous check or claim.",
        failure_condition="A passing statement remains visible after the artifact or context changed in a way that invalidates the evidence.",
        prove_next="Retain the exact release identity and link evidence to the version it actually checked.",
        claim_limit="Version labels improve provenance but do not authenticate the truth of the evidence.",
    ),
    PublicRule(
        id="EVID-LIMITS-02",
        module="public_evidence",
        title="Known limitations and support boundaries are stated",
        hard_lenses=("experience_information", "people_operation"),
        hard_criteria=("HCAI-1.1", "HCAI-4.5"),
        intent="Public product evidence should make important scope limits visible instead of allowing a polished surface to imply universal capability.",
        observe=(
            "known limitations",
            "unsupported contexts",
            "status/incident/support boundary",
        ),
        pass_condition="The inspected public material states meaningful limitations or scope boundaries relevant to the product's claims.",
        warning_condition="The product makes broad claims while limitations, exclusions, or support boundaries are difficult to locate or interpret.",
        decision_underneath="The company has chosen which unsupported or uncertain contexts users need to know before relying on the product.",
        must_be_true="The public promise must remain proportional to the declared scope and evidence.",
        failure_condition="Users treat an unsupported context as covered because the public surface never exposes the boundary.",
        prove_next="Publish the highest-consequence known limitations and the owner/process for revisiting them.",
        claim_limit="Absence of a public limitations page is a transparency signal, not proof of unsafe implementation.",
    ),
    PublicRule(
        id="EVID-TRACE-03",
        module="public_evidence",
        title="Important public claims can be traced to supporting material",
        hard_lenses=("implementation_evidence",),
        hard_criteria=("HCAI-2.1", "HCAI-2.2", "HCAI-4.5"),
        portfolio_principles=(
            "takyejun.com design system: sources stay traceable to original project files",
            "trust comes from source-linked evidence, not decorative confidence",
        ),
        intent="A recipient should be able to inspect the source behind a consequential public claim without reverse engineering the site.",
        observe=(
            "source links/references",
            "artifact/date/version identity",
            "preserved original versus summary distinction",
        ),
        pass_condition="Consequential public claims point to inspectable supporting material with enough identity to understand the basis.",
        warning_condition="A source is named but cannot be inspected, dated, or connected clearly to the claim.",
        decision_underneath="The product has chosen whether claims are inspectable or authority-based.",
        must_be_true="The evidence relationship must remain reconstructable after the summary is separated from its source.",
        failure_condition="A reviewer cannot tell whether a confident summary came from measured evidence, a draft, a simulation, or marketing copy.",
        prove_next="Link the claim to the exact supporting artifact/version and preserve the source identity in the report.",
        claim_limit="Traceability supports review; it does not make the underlying source independently valid.",
    ),
    PublicRule(
        id="EVID-CHOICE-04",
        module="public_evidence",
        title="A consequential prioritization has an inspectable rationale",
        hard_lenses=("experience_information", "implementation_evidence"),
        hard_criteria=("HCAI-2.1", "HCAI-4.3"),
        portfolio_principles=(
            "takyejun.com case studies treat numbers such as recommendation limits as design decisions when grounded in observed behavior",
            "context-specific decisions should remain context-specific rather than become universal prescriptions",
        ),
        score_included=False,
        intent="When a product visibly limits, ranks, hides, or promotes options, the review should ask what decision criterion supports that prioritization.",
        observe=(
            "ranked/recommended options",
            "hard limits or defaults",
            "public rationale or measurable criterion when available",
        ),
        pass_condition="The supplied evidence connects the prioritization to a user need, measurable criterion, or explicit product tradeoff.",
        warning_condition="A consequential limit/default/rank appears arbitrary or its rationale cannot be reconstructed from available evidence.",
        decision_underneath="The product has chosen which options deserve attention or exclusion at a decision point.",
        must_be_true="The prioritization must fit the user need and consequence rather than merely encode a convenient implementation default.",
        failure_condition="A hidden/default/ranked choice systematically pushes users toward an outcome without a defensible criterion.",
        prove_next="Retain the decision rationale, alternative considered, and one bounded test showing why the prioritization fits the task.",
        claim_limit="This is an advisory H.A.R.D.-style prompt. It must never enforce a fixed number of recommendations across products.",
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
        raise ValueError("This rule does not permit an automated/public critical label")

    status = observation.status
    if status == "unknown" and rule.absence_is_failure:
        raise ValueError("Rule configuration contradiction: unknown cannot be an automatic failure")

    observed = observation.observed or (
        "The reviewed public surface did not provide enough evidence to assess this rule."
        if status == "unknown"
        else rule.title
    )
    next_evidence = observation.next_evidence or rule.prove_next

    trace = DeveloperTrace(
        observed=observed,
        decision_underneath=rule.decision_underneath,
        must_be_true=rule.must_be_true,
        if_wrong=(
            observation.failure_mechanism + (" Consequence: " + observation.consequence if observation.consequence else "")
            if observation.failure_mechanism
            else rule.failure_condition
        ),
        prove_next=next_evidence,
    )

    if status == "unknown":
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
        summary = rule.pass_condition if status == "pass" else rule.warning_condition
        if status == "critical":
            summary = observation.failure_mechanism + " " + observation.consequence
        finding = ReportFinding(
            id=rule.id,
            module=rule.module,
            title=rule.title,
            status=status,
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
        },
        "portfolio_provenance": list(rule.portfolio_principles),
    }
