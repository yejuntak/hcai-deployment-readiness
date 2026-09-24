# QUICK-6: six questions before engineering

Protocol 0.1-rc.4-candidate.3 · Advisor-led · Low risk only

**Purpose:** decide whether the evidence supports a bounded engineering commitment—not deployment.

Check risk first. Any moderate, high, or unknown risk dimension routes to FULL. Use QUICK-6 only when current records and the proposed artifact are available. The <=15-minute target is untested; preparation is reported separately. Capture and explaining the result count as session time.

Also screen consequential context: safety/rights or irreversible external actions require high-depth FULL; sensitive data or untrusted input influencing actions require at least moderate FULL. Unknown prevents the quick path. Explain the basis, not just yes/no.

| Ask in ordinary language | Look for |
| --- | --- |
| 1. What happens today? | A recent measured case; connected current steps, people, time, touches, errors, review, escalation, rework, and volume. |
| 2. What needs to improve, for whom? | Actual need, alternatives and affected people; screen access/use, privacy/security, unequal effects and human agency. |
| 3. What happens when things go wrong? | Connected normal, edge and recovery paths with a reachable exit; owners and explicit authority limits. |
| 4. What demonstrates the important behavior? | Each check bound to the exact artifact AND requirement/context. Label specified or simulated behavior. |
| 5. What work remains for people? | Review, correction, escalation/rework, residual manual work, and recurring/one-time costs. |
| 6. Is that enough to fund the next step? | Low-risk threshold met, human evidence-quality review recorded, critical findings resolved, owner and bounded limits. |

## Stop visibly; leave a useful next action

At the first failed or missing gate, say:

“We cannot support the engineering commitment yet because ____. The next action is ____. The owner is ____.”

Record the stopped gate. Later questions are NOT_EVALUATED, not passes. Keep known critical findings visible. Missing evidence means INSUFFICIENT_EVIDENCE; a demonstrated defect means REVISE. Missing baseline means ROI is indeterminate.

If continuing in FULL, save the stopped record first, then create a linked revision using previous_run_id and revision_summary. Reuse unchanged evidence. Do not erase the earlier stop.

## Close the conversation

When all gates pass, PROCEED_TO_ENGINEERING means the owner may consider a bounded engineering step. It says nothing about deployment or operational performance.

Machine checks are partial. They cannot authenticate evidence or the recorded human review. Do not convert a pass into certification.

Ask the participant: “In your own words, what does this result allow—and what is the next action?” Record confusion rather than coaching it away. Ask whether the evidence was easy to find.

## Minimal session notes

Workflow and unit of work: ____  
Date / facilitator / participant role: ____  
Risk and reason: ____  
Preparation / session minutes: ____ / ____  
Stopped gate or all gates passed: ____  
Missing evidence / next action / owner: ____  
Participant's explanation and confusing questions: ____

The full record is completed by the facilitator or tool. Use the [conversation worksheet](WORKSHEET.md) if helpful. Do not promise savings. See [Start here](START-HERE.md) or [FULL](FULL-PROFILE.md).
