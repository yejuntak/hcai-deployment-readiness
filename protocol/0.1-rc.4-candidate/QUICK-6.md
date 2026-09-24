# QUICK-6: a short advisor-led engineering decision

Protocol 0.1-rc.4-candidate · MCP 0.2.0rc1 · Skill/contract 0.2.0-rc.1

Proposed target: <=15 minutes for a low-risk case with existing records. Duration and usability have not been tested with practitioners. The advisor records evidence; the business owner does not need to learn the schema. Time includes capture and reporting, not just asking questions.

Before starting, identify one real workflow, the user and engineering decision owner. Start the timer. If any risk dimension is moderate/high or unknown, choose FULL. Do not force a quick result. Record a pre-decision only if it is captured before discussing the gates.

| Time | Ask | Pass evidence / visible stop |
| --- | --- | --- |
| 3 min | 1. Can we quantify how this work happens today? | Current path and people, at least one observed case, elapsed/labor minutes, touches/handoffs, failures, review/escalation/rework and volume. Missing baseline: STOP; insufficient evidence; ROI indeterminate. |
| 2 min | 2. Whose need are we solving, and what would count as success? | Explicit need, source, outcome, owned requirements and measurable acceptance criteria. Missing need or testable criteria: STOP. |
| 3 min | 3. What happens normally, when something goes wrong, and during recovery? | Owned normal/edge/recovery paths, data handling, requirement links and reviewed dependencies. Missing path: STOP. |
| 2 min | 4. Can we connect each important artifact/behavior to its requirement and a check? | Form/fit/function reference and an executed walkthrough/test record for every requirement/artifact pair. Broken link or failed check: STOP; revise. A planned test alone is insufficient. |
| 2 min | 5. Who reviews, corrects or escalates AI output, and how long will that take? | Separate review, correction, escalation, rework and residual manual minutes per case. Show gross minus oversight; missing estimate: STOP. |
| 3 min | 6. Does this evidence justify a bounded engineering commitment at this risk level? | All gates pass, all risk dimensions low, no blocking findings, complete reference/risk/decision records, time <=15 min, resource cap and review trigger. Otherwise STOP and route to FULL. |

A stop is an outcome, not a bad participant result. Record the first unmet gate and mark later gates NOT_EVALUATED. Save what is missing and the next evidence-gathering action. Start a new FULL run after remediation; never edit a stopped run into a pass.

When all gates pass, record PROCEED_TO_ENGINEERING as a recommendation and ask the designated owner to make a separate, dated authorization. This does not approve deployment. Do not add up yes answers or allow five passes to outweigh one failure.

Use the structured assessment schema or the portable Skill; synthetic examples illustrate format only. Retain elapsed time and evaluator/participant/adjudication person-minutes separately. Calls, tokens and money may be unknown; never enter zero merely because they were not measured.
