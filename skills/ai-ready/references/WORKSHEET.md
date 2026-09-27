# Worksheet: choices, evidence and the next decision

H.A.R.D. Protocol 0.3 · Public Preview

Use paper or existing notes. The facilitator can maintain the detailed machine record. Completing this worksheet does not authenticate evidence or grant a favorable result.

## Set the boundary

Artifact / revision / date: ______  Purpose / affected people: ______

Route: artifact_review / engineering_commitment / independent_evaluation

Stage: specification_handoff / prototype_handoff / implementation_review / runtime_release_review

Artifact population: ai_generated / runtime_ai / both / neither / unknown

Current scope: ______  Deferred or excluded items and reasons: ______

Reviewer kind: ______  Role overlaps and reference access: ______

Criteria fixed when, before or after viewing the artifact? ______  Owner of next decision: ______

## Inspect one consequential choice

| Question | Record |
| --- | --- |
| What is actually chosen, and where? | Choice ID, observed behavior and source location: ______ |
| What purpose and criteria should it meet? | Outcome, affected people, priorities and acceptance conditions: ______ |
| What reason was recorded at the time? | Documented / reported / unknown, source: ______ |
| What alternatives were recorded or are newly proposed? | Historical alternatives with sources: ______. New alternatives: ______ |
| What are the effects and tradeoffs? | Benefits, costs, assumptions, conflicting priorities and limits: ______ |
| What evidence supports or questions the choice? | Sources and validation result: ______ |
| What does a person decide now? | Current rationale, labeled new when appropriate: ______. Accepted / revise / pending: ______ |
| What happens next? | Action or revisit condition: ______. Owner: ______ |

Repeat only for consequential choices. No need to replace an appropriate original choice. An unrecorded reason stays unrecorded; a plausible explanation is new analysis.

## Record requirement and recovery evidence

| Item and acceptance check | Scope and reason | Specified | Walkthrough | Implemented | Runtime tested |
| --- | --- | --- | --- | --- | --- |
| ______ | ______ | ______ | ______ | ______ | ______ |

For each level, record pass, fail, unassessed or justified not_applicable plus a source location. Do not collapse the columns. Current unassessed items remain in the denominator. A future-scope exclusion cannot conceal a dependency necessary for the current claim.

Finding / expected vs observed / location: ______  Current applicability: ______

Proposed severity and basis: ______  Accepted, unsupported, duplicate or unresolved: ______

Confirmed severity, if actually reviewed: ______  Remediation and verification: ______

## Complete the minimum artifact review

Declared-stage result: ______  Evidence that supports it: ______

Choices retained: ______  Open decisions: ______  Findings requiring repair: ______

Next action / owner / revisit trigger: ______

Reviewer metrics: N/A unless eligible under [independent evaluation](INDEPENDENT-EVALUATION.md). Reason for each N/A: ______

Preparation / session effort, if recorded: ______  Do not invent retrospectively measured times.

This route does not require a measured baseline or ROI estimate. It does not issue an engineering recommendation or deployment approval.

## If funding engineering, complete all six gates

| Gate | Additional evidence |
| --- | --- |
| G1: What happens today? | Observed current case, connected steps, time, touches, failures, review, escalation, rework, volume and observation window: ______ |
| G2: What needs to improve, for whom? | Actual need, alternatives, requirements, affected roles and impact checks: ______ |
| G3: What happens on failure? | Connected states and recovery, dependencies, authority boundaries, data preservation and owner: ______ |
| G4: What demonstrates behavior? | Requirement, exact artifact and requirement/context fingerprints, executed validation and result: ______ |
| G5: What work remains for people? | Disjoint review, correction, escalation, rework and residual manual minutes; cost assumptions: ______ |
| G6: What bounded step is justified? | Risk depth, human evidence-quality review, findings, owner, resource cap and next review trigger: ______ |

Apply the full risk rules before selecting QUICK6 or FULL. QUICK6 stops at the first failed or missing gate; later gates are NOT_EVALUATED, and known critical findings remain visible. Preserve a stopped record before a new linked FULL run. Missing baseline blocks a qualifying engineering recommendation and leaves ROI indeterminate.

Engineering recommendation / reason / next action: ______  Separate owner authorization: ______

Ask: **In your own words, what does this result allow, and what remains undecided?** Record the answer before explaining again.

Permission / anonymization / retention: ______  Previous run / changes: ______

Execution versions: protocol 0.3-preview.1 · MCP 0.3.0rc1 · Skill/contract 0.3.0-rc.1.


## Engineering reasoning deepening

Complete this section for each consequential choice only after recording whether deepening applies.

**Choice ID:** ____________________

**Does engineering deepening apply?** yes / no

**Why?** ________________________________________________________________

**Trigger(s):** state mutation / external side effect / irreversible action / privileged or tenant boundary / unreliable dependency / repeat or concurrent execution / money or data loss / material scale or cost assumption / current promise depends on deferred work / ambiguous source of truth / other

Record each consequential assumption separately before the surface table. Leave unsupported claims unassessed.

| Assumption ID | Statement | Status | Consequence if false | Evidence needed / retained evidence | Revisit trigger |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

For each relevant system surface, record the current model and status.

| Surface | Current model or question | Status | Evidence or next evidence |
| --- | --- | --- | --- |
| Truth |  |  |  |
| Ownership |  |  |  |
| State |  |  |  |
| Boundary |  |  |  |
| Contract |  |  |  |
| Failure/recovery |  |  |  |
| Time/ordering |  |  |  |

**What would have to be true for this choice to be wrong?** ____________________

**Expected behavior or invariant:** ________________________________________

**Consequence if mishandled:** ____________________________________________

**Evidence that would resolve the challenge:** _____________________________

**Evidence level when assessed:** walkthrough / implemented / runtime-tested / unassessed

**Smallest coherent next slice:** _________________________________________

Do not fill blanks with a generated rationale. Unknown is a valid review result.
