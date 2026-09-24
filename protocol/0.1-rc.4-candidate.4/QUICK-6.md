# QUICK-6: six questions before engineering

Protocol 0.1-rc.4-candidate.4 · Advisor-led · Low risk only

Use QUICK-6 to assess whether the available evidence supports a bounded engineering commitment. Deployment requires a separate evaluation.

Check risk before starting. Any moderate, high, or unknown risk dimension requires FULL. QUICK-6 assumes that current records and the proposed artifact are available. Its <=15-minute target remains untested. Include recording answers and explaining the result in session time, and report preparation separately.

Check the workflow's context as well. Safety/rights effects or irreversible external actions require high-depth FULL. Sensitive data or untrusted input influencing actions require at least moderate FULL. An unknown answer prevents QUICK-6. Record the basis for each answer.

| Ask in ordinary language | Look for |
| --- | --- |
| 1. What happens today? | A recent measured case; connected current steps, people, time, touches, errors, review, escalation, rework, and volume. |
| 2. What needs to improve, for whom? | Actual need, alternatives and affected people; screen access/use, privacy/security, unequal effects and human agency. |
| 3. What happens when things go wrong? | Connected normal, edge and recovery paths with a reachable exit; owners and explicit authority limits. |
| 4. What demonstrates the important behavior? | Each check bound to the exact artifact AND requirement/context. Label specified or simulated behavior. |
| 5. What work remains for people? | Review, correction, escalation/rework, residual manual work, and recurring/one-time costs. |
| 6. Is that enough to fund the next step? | Low-risk threshold met, human evidence-quality review recorded, critical findings resolved, owner and bounded limits. |

## When a gate cannot pass

At the first failed or missing gate, say:

“We cannot support the engineering commitment yet because ____. The next action is ____. The owner is ____.”

Record where the review stopped and mark later gates NOT_EVALUATED. Retain known critical findings. Use INSUFFICIENT_EVIDENCE for missing evidence and REVISE for a demonstrated defect. Without a baseline, ROI is indeterminate.

If continuing in FULL, save the stopped record first, then create a linked revision using previous_run_id and revision_summary. Reuse unchanged evidence. Do not erase the earlier stop.

## Close the conversation

When all gates pass, PROCEED_TO_ENGINEERING means the owner may consider a bounded engineering step. It says nothing about deployment or operational performance.

The software checks only part of the review. It cannot authenticate evidence or confirm that the recorded human review took place, so a pass is not certification.

Ask the participant: “In your own words, what does this result allow, and what is the next action?” Record their answer before offering another explanation, including any confusion. Ask whether the evidence was easy to find.

## Minimal session notes

Workflow and unit of work: ____  
Date / facilitator / participant role: ____  
Risk and reason: ____  
Preparation / session minutes: ____ / ____  
Stopped gate or all gates passed: ____  
Missing evidence / next action / owner: ____  
Participant's explanation and confusing questions: ____

The facilitator or tool completes the detailed record. The [conversation worksheet](WORKSHEET.md) can help with note-taking. Estimates should not be presented as promised savings. For more detail, see [Start here](START-HERE.md) or [FULL](FULL-PROFILE.md).
