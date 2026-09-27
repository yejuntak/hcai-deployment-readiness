# Start with one artifact and one decision

H.A.R.D. Protocol 0.3 · Public Preview

Bring the plan, screen, workflow or code you want to inspect. Name its exact revision and the next decision you need to make. You can review a specification before any implementation exists.

Start with this question: **What is this result trying to achieve, which choices inside it have we actually reviewed, and what system model do those choices depend on?**

## Choose your route

| What you need | Start here |
| --- | --- |
| Find unclear choices, missing requirements, weak evidence or recovery gaps | [Minimum artifact review](ARTIFACT-REVIEW.md). One person is sufficient; no ROI or measured baseline is required. |
| Decide whether to invest in a bounded engineering step | [QUICK-6](QUICK-6.md) for low risk with evidence ready; [FULL](FULL-PROFILE.md) otherwise. All six gates apply. |
| Measure a reviewer's detection or compare conditions | [Independent evaluation](INDEPENDENT-EVALUATION.md). Plan independent references and locked judgments before collecting measurements. |

An advisor can record the answers, or a solo practitioner can use the [worksheet](WORKSHEET.md). Reuse existing records. Do not create extra documents merely to fill a form.

## The minimum review

1. **Bound the artifact.** Record purpose, affected people, revision, stage and current versus future scope. Identify whether AI created it, operates within it, both or neither.
2. **Decompress consequential choices.** Inspect what was chosen, why it serves the purpose, credible alternatives, assumptions and tradeoffs. Cite documented reasons; label current hypotheses and new alternatives honestly.
3. **Deepen only where consequence warrants it.** Explicitly record whether engineering deepening applies. When it does, model the relevant truth, ownership, state, boundary/contract, failure and time/ordering surfaces, record consequential assumptions separately, and name at least one condition that could disconfirm the choice, model or assumption. If checked, label the challenge evidence level.
4. **Check evidence.** For each current requirement and recovery path, record specified, walkthrough, implemented and runtime-tested evidence separately. Unknown is visible, not a pass.
5. **Record the next decision.** Keep justified choices. For supported gaps, name the change or question, evidence needed, owner and revisit condition. A person owns the decision.

For example, an AI-written SaaS plan calls a user service before generating a report. The plan explains the happy path but says nothing about a timeout. You can identify that specification gap without code or a measured ROI. You cannot say the implementation fails at runtime, or that adding a retry is necessarily the best solution. Compare bounded retries, queued work, partial results and a manual fallback against the actual purpose and constraints. If the choice changes consequential state, also ask which result is authoritative after a timeout, whether repeat execution is safe, and what evidence could disconfirm the current model.

If only one dependency needs closer inspection, deepen that part. Targeted deepening changes review depth; it does not create a new scoring profile or validated claim. Consequential decisions may need a competent independent or specialist reviewer even when the first inspection was done alone.

## Explain the result

Record what the supplied evidence supports at the declared stage, what remains unassessed and one next action with its owner. Report artifact coverage separately from any eligible reviewer metrics. If independence or a locked reference is missing, mark affected metrics N/A with the reason; keep useful findings.

For an engineering funding recommendation, complete QUICK6 or FULL afterward. A minimum artifact review never implies those gates passed. For research, keep reference answers away from reviewers until judgments are locked.

The protocol is a Public Preview. Examples are constructed and feedback is formative. Neither a complete record nor a favorable recommendation approves deployment.

Execution versions: protocol 0.3-preview.1 · MCP 0.3.0rc1 · Skill/contract 0.3.0-rc.1.
