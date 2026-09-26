# Inspect the decisions inside the result

H.A.R.D. Protocol 0.2 · Public Preview

AI-assisted creation can compress the path from a request to a finished-looking artifact. A useful review makes the choices in that path discussable: their purpose, alternatives, reasons, tradeoffs, evidence and unresolved human judgment. It does not pretend to recover an unrecorded generation process.

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

## Relation to the other routes

Minimum artifact review can use this record without financial measurements. Engineering commitment maps relevant evidence into the existing gates: purpose and alternatives into G2, dependencies and authority into G3, revision-specific checks into G4, human work into G5, and the bounded decision into G6. G1 remains necessary when making that engineering recommendation.

This review technique is unvalidated. Do not add its prompts or alternative lists to a controlled fidelity study unless the approved study design explicitly includes them.

Execution versions: protocol 0.2-preview.3 · MCP 0.2.0rc9 · Skill/contract 0.2.0-rc.9.
