# Worksheet for a workflow review

Protocol 0.1-rc.4-candidate.4 · MCP 0.2.0rc4 · Skill/contract 0.2.0-rc.4

Use this worksheet on paper or in your usual notes. The advisor records where the evidence can be found, so participants need not fill in technical fields. Reuse existing records where appropriate. The [full evidence contract](FULL-PROFILE.md) still governs the review; completing this worksheet does not grant a pass.

## Before the six questions

Workflow / one completed case: ______  Owner: ______  Date / run ID: ______

Where does it start and end? ______  Proposed artifact revision: ______

Risk: safety/rights effects? ___ irreversible external action? ___ sensitive data? ___ untrusted input to actions? ___

Record yes, no or unknown and give the reason. The first two “yes” answers require high-depth FULL, the others at least moderate FULL; any unknown prevents QUICK-6. Combine these with the six risk dimensions in the full profile. Path selected: ______

## Questions and evidence notes

| Ask aloud | Advisor's short record |
| --- | --- |
| 1. Show one recent case of today's work. Who checked, fixed or chased it? | Steps, times, handoffs, rework, volume, observation window and evidence pointer: ______ |
| 2. Whose difficulty should improve, and how will we know? Who else is affected? | Need and success condition: ______. Access/use, privacy/security, unequal effects, human control: ______. Applicable concern → requirement/check; justify exceptions. |
| 3. When something goes wrong, who notices and how do they recover? | Normal → edge → recovery → endpoint; saved work and authority limits: ______ |
| 4. Show the requirement, the artifact and the check together. | Exact revisions and executed result: ______. Changed requirement/context or artifact? ______ |
| 5. What work remains for people? | Review ___ correction ___ escalation ___ rework ___ residual manual ___ minutes/case. Basis: ______ |
| 6. What bounded engineering step could this evidence support? | Human quality review ___; unresolved findings ___; owner ___; resource cap ___; revisit trigger ___ |

For QUICK-6, stop at the first missing or failed gate. Mark later gates NOT_EVALUATED. A known critical finding remains visible. After addressing the gap, continue in a new linked FULL record and retain this one. An unknown answer identifies evidence still needed.

## Explain the result

Recommendation: consider a bounded engineering step / revise / gather evidence.

Because: ______  Next action: ______  Owner: ______  Revisit when: ______

Preparation elapsed/person-minutes: ______  Session elapsed/person-minutes: ______

Adjudication minutes: ______  Capture/reporting minutes (already inside session): ______

Estimated gross benefit: ______  Oversight burden: ______  Net effect: ______

Missing baseline means ROI is indeterminate. These are not measured operating-performance results. Separate protocol review expense from operating costs.

Ask the participant: **“In your own words, what does this result allow us to do, and what does it not allow?”** Record their answer before explaining again. Retain any misunderstanding in the usability notes.

The advisor retains exact versions, artifact/requirement fingerprints and evidence locations in the detailed private record. Fingerprints identify revisions but cannot establish adequate testing. The software also cannot independently authenticate a recorded human review. Funding authorization and deployment evaluation remain separate decisions.

Permission / anonymization / retention agreement: ______  Previous run if any: ______
