# H.A.R.D. Protocol 0.3

Human-centered AI Readiness and Decision Protocol  
Public Preview

## Why begin with the result?

AI-assisted creation can compress the distance between an intention and a convincing plan, design or implementation. The artifact may arrive before the people responsible for it have formed, examined or preserved the system model and consequential decisions they would normally use to judge what should be built.

H.A.R.D. starts with the result and reopens those decisions. It asks what was chosen, what purpose it serves, which alternatives matter, what assumptions and tradeoffs the choice depends on, what must remain true as the system changes state, what conditions could make the choice wrong, and what evidence supports the next human-owned commitment.

This preview calls that problem **decision compression**. Decision compression is a motivating model, not an established causal effect. The protocol does not claim that AI authorship creates defects, that experienced practitioners always follow one hidden sequence, or that H.A.R.D. improves outcomes. It makes consequential reasoning inspectable so a person can decide what still needs evidence.

H.A.R.D. never reconstructs private model chain-of-thought or invents creator intent. A documented historical reason, an attributed later report, a new review hypothesis, a newly proposed alternative and the human decision made now remain different record types.

### Core review loop

1. **Decompress.** Locate consequential choices in the supplied artifact. Connect each to purpose, criteria, alternatives, rationale provenance, assumptions and tradeoffs.
2. **Model.** When engineering deepening is warranted, externalize only the relevant system surfaces: truth, ownership, state, boundary, contract, failure/recovery and time/ordering. Record consequential assumptions separately as claims that can be supported, conflicted or left unassessed.
3. **Challenge.** Name a bounded condition that could disconfirm the choice, system model or consequential assumption. Record the evidence level of any assessed challenge so a walkthrough cannot be presented as implementation or runtime proof. Do not prescribe a fashionable architecture as the answer.
4. **Prove.** Keep specified, walkthrough, implemented and runtime-tested evidence separate. Bind executed checks to the exact artifact and decision context.
5. **Decide.** A person accepts, revises or keeps the choice pending, with an owner, smallest coherent next step and revisit trigger.

Generation must not outrun understanding. That sentence is a design principle for the review, not a measured claim about AI-assisted development.

## Choose the decision you need

| Purpose | Route | Result and boundary |
| --- | --- | --- |
| Inspect a plan, prototype or implementation and decide what needs clarification or repair | `artifact_review` | An evidence map, supported findings, recorded choices and a next action for the declared stage. A person working alone can use it. |
| Decide whether evidence supports funding a bounded engineering step | `engineering_commitment`, using QUICK6 or FULL | The existing six gates and fifteen criteria produce PROCEED_TO_ENGINEERING, REVISE or INSUFFICIENT_EVIDENCE. Owner authorization is separate. |
| Measure reviewer performance or compare conditions | Optional `independent_evaluation` | Eligible metrics against a frozen, independent reference, with role, timing and population checks. No engineering or deployment permission. |

Begin with [Start here](START-HERE.md). For a small team, the official minimum is [artifact review](ARTIFACT-REVIEW.md), supported by [decision review](DECISION-REVIEW.md) and the [worksheet](WORKSHEET.md). A measured baseline, ROI estimate and independent reference author are not prerequisites for that route. Missing information remains visible and limits the result.

For engineering commitment, use [QUICK-6](QUICK-6.md), [FULL](FULL-PROFILE.md) and the [criteria](CRITERIA.md). The minimum artifact route cannot waive or pass any of these gates. For performance measurement, use [independent evaluation](INDEPENDENT-EVALUATION.md). Independence requirements apply to the metric claimed, not to whether a solo practitioner may inspect an artifact.

Targeted deepening is an intermediate amount of work: inspect a consequential dependency, a weak rationale or an unclear recovery path before expanding the review. It is not a third validated scoring profile and does not relax a required gate or replace specialist review.

## Scope and artifact population

Plans and specifications are in scope even when no code exists. Declare the artifact stage and exact review question, such as whether the specification is clear enough for a bounded implementation task. The absence of runtime evidence is expected at that stage and must remain visible. It cannot be represented as runtime success.

Record `artifact_population`: `ai_generated`, `runtime_ai`, `both`, or `neither`. These are distinct populations. AI-generated code can run without an AI component; a runtime AI product may have been authored manually. Unknown provenance is unresolved, not `neither`. Record an actual runtime AI system's output uncertainty, external dependencies, authority, user recourse and fallback where applicable.

## Review choices and evidence together

Keep the exact original revision. For each consequential choice, connect purpose and affected people to alternatives, rationale provenance, tradeoffs, assumptions, evidence and an accountable disposition: keep, change, investigate or defer within a defensible scope. A current explanation generated by an assistant is not a record of what the original creator considered.

If needed, create a separate information outline, state map, dependency diagram, wireframe or execution trace. Preserve known labels and behavior; mark unknowns instead of completing them by imagination. A structural view is a discussion aid, not a validated treatment or substitute for execution evidence.

Inspect four connected aspects: experience and information; workflow and architecture; implementation and evidence; people and operation. In software, this includes asynchronous versus synchronous processing, data contracts, tenancy boundaries, authorization, error handling, retries, partial completion and maintenance. In design, it includes hierarchy, competing actions, feedback, accessibility and recovery. Review the choices relevant to the specific artifact, not a universal list of preferred solutions.

## Four evidence levels stay independent

| Evidence level | What a supported record establishes | What it cannot establish alone |
| --- | --- | --- |
| Specified | A requirement or behavior is defined and checkable in the cited revision | That anyone walked through, implemented or executed it |
| Walkthrough | A recorded review or simulation checked the stated path | That production components behaved that way |
| Implemented | The cited implementation contains the required behavior | That the behavior passed a runtime check |
| Runtime tested | A retained execution result covers the named revision and context | Universal safety, reliability or deployment readiness |

Record each separately for every requirement and recovery item. An executed result does not fill a missing specification by inference. Unassessed items stay in their declared denominators. Explicit scope exclusions require a reason and cannot conceal current dependencies. Coverage at one level is not an overall maturity score. See [artifact review](ARTIFACT-REVIEW.md) for stage and applicability rules.

## Engineering commitment retains six gates

1. **G1: What happens today?** Retain observed work, a connected baseline and measurements.
2. **G2: What needs to improve, for whom?** Connect actual need, affected people and requirements.
3. **G3: What happens when things go wrong?** Specify normal, edge, recovery and authority paths.
4. **G4: What demonstrates important behavior?** Bind requirements, exact artifact revisions and executed validation.
5. **G5: What work remains for people?** Separate residual work, review, correction, escalation and rework.
6. **G6: Is this enough to fund the next engineering step?** Apply risk depth, resolve blockers, retain human evidence-quality review and name the owner, limits and next trigger.

QUICK6 is for low risk with records available. Its <=15-minute target remains untested. It stops at the first failed or missing gate; later gates are NOT_EVALUATED and known critical findings stay visible. FULL evaluates all six. Moderate, high or unknown risk prevents QUICK6. Consequential-context floors and all other risk rules remain in [FULL](FULL-PROFILE.md).

A demonstrated gate failure or unresolved critical finding leads to REVISE. Missing required evidence leads to INSUFFICIENT_EVIDENCE. All required passes support PROCEED_TO_ENGINEERING, subject to separate owner authorization. Passing other gates cannot offset a critical finding. No result approves deployment or certifies software quality.

A missing measurable baseline prevents a qualifying engineering recommendation and leaves ROI indeterminate. It does not prevent a limited artifact review from identifying a missing timeout, unclear purpose or unsupported design assumption.

## Keep claims proportional

Artifact coverage, review effort, reviewer performance, projected operating burden and measured operational performance are different outputs. Do not combine them into a weighted readiness percentage. Software checks structure and consistency; people must judge evidence relevance, authenticity, completeness and adequacy.

Role overlap is permitted in minimum artifact review and must be disclosed. Optional performance metrics require their own eligibility checks. Agent findings may inform repairs but must not be reported as independent human detection results. See the [metric eligibility table](INDEPENDENT-EVALUATION.md).

Formative practitioner feedback identified usability and schema-consistency concerns. The underlying private assessment attachments were not independently examined for this release, so individual findings, severity assignments and reported values are not reproduced as verified results. The report does not establish effectiveness, adoption or endorsement. Public summaries omit private names and quotations.

The related proposed fidelity study remains separate. It investigates defect detection while AI authorship is held constant. Neither this rationale nor the formative feedback establishes that hypothesized effect. Do not introduce guided review prompts or reference keys into a research session unless its design calls for them. See [research boundaries](../../docs/research-boundary.md).

## Status and records

Keep original evidence, version identities, source origins and prior runs. Changed evidence requires a new linked review; historical runs are not silently relabeled. Private is the default. Public disclosure requires its own permission check.

All historical version directories remain frozen. This Public Preview adds explicit routes, decision-review guidance and record consistency requirements. The six engineering gates, fifteen criteria, risk floors and engineering formulas remain in force. Usability, completion time, decision quality and defect-prevention effects remain unvalidated. Software regressions alone cannot answer those questions.

Read the [scenarios](SCENARIOS.md), [claims and governance](../../docs/claims-and-governance.md), [agent tools](../../docs/agent-tools.md) and [update log](https://www.takyejun.com/research/ai-readiness/updates).

Execution versions: protocol 0.3-preview.2 · MCP 0.3.0rc2 · Skill/contract 0.3.0-rc.2.
