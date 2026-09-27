# Inspect the decisions inside the result

H.A.R.D. Protocol 0.3 · Public Preview

AI-assisted creation can compress the path from intention to a finished-looking artifact. A useful review decompresses consequential choices without pretending to recover an unrecorded generation process. It makes purpose, alternatives, assumptions, reasons, tradeoffs, system dependencies, evidence and unresolved human judgment discussable.

## Record a consequential choice

| Record | Prompt | Evidence boundary |
| --- | --- | --- |
| Observed choice and location | What does this revision actually do or propose? | Cite the artifact; separate observation from interpretation. |
| Purpose and affected people | What outcome should this choice serve, and for whom? | Use a supplied requirement or record a purpose that needs confirmation. |
| Historical reason | Is there a dated rationale or decision record? | Cite it or state that none was found. Never fabricate creator intent. |
| Alternatives | What materially different approach could meet the same purpose? | Separate documented past alternatives from options proposed during this review. |
| Tradeoffs and assumptions | What does each option gain, cost, constrain or put at risk? | Label assumptions; identify the evidence that could resolve them. |
| Supporting and conflicting evidence | Why retain or question this choice? | Include counterevidence and missing checks, not just a persuasive explanation. |
| Missing human judgment | Which value, risk, authority or scope decision requires a person? | An agent may frame the question; it cannot invent approval. |
| Current disposition | Keep, change, investigate or defer? Who decides, and when should this be revisited? | This is a new decision, even if it retains the original choice. |

The machine record uses `rationale_provenance`: `documented`, `reported`, `new` or `unknown`. Historical alternatives require source evidence; newly proposed alternatives have their own list. Unknown historical rationale remains null. A reviewer may propose a current justification using `new`, with its supporting evidence, while retaining the absence of a historical record.

Record `human_decision` as `accepted`, `revise` or `pending`, with an accountable owner and `human_decision_evidence_locations` recording the actual human confirmation. Keeping the existing choice maps to accepted when a human has actually accepted it. Investigation or unresolved deferral remains pending, with a follow-up and owner. Accepted is a current disposition, not proof that the original creation process was reviewed. Important choices need explicit criteria, observation, alternatives review, tradeoffs, verification evidence and a next action or revisit plan.

Historical rationale, reviewer inference, proposed alternative and current decision are distinct record types. A reason produced after the fact is a candidate explanation unless evidence shows it was recorded at the time. Ask for concise, verifiable reasons and tradeoffs, not private model chain-of-thought.

## A practical sequence

First identify the purpose and observed choice. Then ask whether any preserved rationale explains it. When the reason is absent, record the gap and consider plausible options explicitly as new analysis. Compare only alternatives that could materially change the decision. An exhaustive list of hypothetical choices is not required.

Check assumptions using the smallest relevant evidence: a source line, dependency contract, state walkthrough, code revision, observed execution or an affected person's account. If the existing choice is well supported, retain it and explain why. If information is missing, state what would change the decision rather than forcing a redesign.

Record a disposition, owner, next action and revisit trigger. Do not automatically rewrite the artifact. A review finding and permission to implement a change are separate acts.

## Software and SaaS examples

These are constructed examples, not measured results.

| Observed choice | Review question | Useful next evidence |
| --- | --- | --- |
| Synchronous external API call | Does the user need an immediate complete answer, or would queued work preserve reliability? | Latency budget, dependency behavior, cancellation and partial-failure specification |
| Automatic retry after payment timeout | Can the first charge have succeeded before its response was lost? | Provider idempotency contract, transaction state and duplicate-action test |
| Client-side tenant filter | Where is tenant isolation enforced, and what happens if the client request changes? | Server authorization logic and a cross-tenant test at the cited revision |
| Model-generated report delivered directly | What uncertainty is acceptable, who may contest it, and when is human review needed? | Intended use, output constraints, escalation requirements and representative failure cases |
| Shared mutable cache | What consistency and isolation does this use case require? | Invalidation policy, access boundaries and concurrent execution evidence |
| Detailed visual interface | Which actions, information and recovery steps serve the user's task? | Task requirement, interaction map and walkthrough, not appearance alone |

The original choice may be right in each example. Asynchronous work, more prompts or additional automation are not universal improvements. An appropriate review preserves what is justified and exposes where an accountable decision is still missing.

## Assumptions are reviewable claims

Do not leave a consequential assumption buried in a rationale paragraph. Record it separately with a stable ID, its current statement, status, consequence if false, evidence needed, retained evidence when assessed and the trigger that should reopen it. Use supported, conflicted or unassessed. Supported means the retained evidence supports the assumption within the declared scope. It does not turn the assumption into a permanent fact.

A conflicted assumption is a real contradiction in the supplied record, not a request for an AI to invent a more persuasive explanation. An unassessed assumption stays visible until the relevant evidence exists.

## Engineering decision surfaces

Do not make every review a software architecture exercise. First record whether engineering deepening is required and why. Deepening is warranted when an important choice depends on consequential state mutation, an external or irreversible side effect, privileged or tenant boundaries, an unreliable/asynchronous dependency, repeat or concurrent execution, material money/data loss, a scale/cost assumption, a current promise that depends on deferred work, an ambiguous source of truth or another comparable condition.

When deepening applies, record only the surfaces needed to understand the choice:

| Surface | Question |
| --- | --- |
| Truth | Which fact or record is authoritative when representations disagree? |
| Ownership | Who owns that truth and who may mutate it? |
| State | Which states and transitions can actually exist? |
| Boundary | Which component or role owns each responsibility and side effect? |
| Contract | What must cross that boundary, and what does success or failure mean? |
| Failure/recovery | What partial or contradictory state can remain after failure, and how is it repaired? |
| Time/ordering | What if requests repeat, race, arrive late or stop halfway? |

A surface may be supported, conflicted, unassessed or not applicable with a reason. Supported means the supplied evidence supports the current model within scope. It does not establish universal correctness. Conflicted means retained evidence contradicts the current model and is a blocker until the choice, evidence or scope is resolved transparently.

### Challenge before acceptance

For a deepened choice, name at least one bounded challenge condition. Ask: **What would have to be true for this decision to be wrong?** Record the claim at risk, expected behavior or invariant, consequence if mishandled and the evidence needed. When a challenge is actually assessed, record whether the retained evidence is a walkthrough, implemented check or runtime test. A plausible AI explanation is not challenge evidence.

Examples include a duplicated request, delayed first response, stale cache, partial write, dependency outage, cancellation racing completion, conflicting authority or a load assumption being exceeded. Only use cases that are material to the actual choice and risk.

The goal is not maximal complexity. The goal is to distinguish an understood tradeoff from an implementation that merely arrived first.

## Relation to the other routes

Minimum artifact review can use this record without financial measurements. Engineering commitment maps relevant evidence into the existing gates: purpose and alternatives into G2, dependencies and authority into G3, revision-specific checks into G4, human work into G5, and the bounded decision into G6. G1 remains necessary when making that engineering recommendation.

This review technique is unvalidated. Do not add its prompts or alternative lists to a controlled fidelity study unless the approved study design explicitly includes them.

Execution versions: protocol 0.3-preview.1 · MCP 0.3.0rc1 · Skill/contract 0.3.0-rc.1.
