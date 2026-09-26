# Minimum artifact review

H.A.R.D. Protocol 0.2 · Public Preview

`artifact_review` is the official route for inspecting one artifact at a declared stage. It is useful for a solo practitioner or small team that has no separate reference author, evaluator and adjudicator. You can identify missing requirements, inspect consequential choices and plan repairs without measuring reviewer performance or engineering ROI.

This route does not issue PROCEED_TO_ENGINEERING, waive the six engineering gates or approve deployment. Its result is bounded to the supplied artifact, scope, stage and evidence.

## 1. Fix the review boundary

Record the exact revision and date, artifact kind, intended use, affected people, current scope, deferred work, review stage and who owns the next decision. Use `specification_handoff`, `prototype_handoff`, `implementation_review` or `runtime_release_review`. The last label means the artifact is being inspected in a release-review context; it does not grant release authority.

Record the artifact population as `ai_generated`, `runtime_ai`, `both`, `neither` or `unknown`. AI authorship and runtime AI are separate facts. Unknown is unresolved and must not be silently assigned to a known population. Disclose whether the reviewer is human, an agent, or a human working with an agent, and every overlapping role.

A specification is a valid artifact. For specification handoff, the question is whether the current plan defines the behavior needed for the proposed implementation work. Record later evidence levels as unassessed when no such evidence exists. Do not invent implementation or runtime records and do not require a financial baseline merely to inspect the plan.

Before interpretation, retain or freeze the applicable requirement and recovery inventories. If a new issue changes scope, preserve the original inventory and create a dated amendment. A retroactive inventory can support a disclosed descriptive review, but it cannot be presented as a prospectively frozen reference for performance measurement.

## 2. Inspect the important choices

Use [decision review](DECISION-REVIEW.md) to connect each consequential choice to purpose, acceptance criteria, alternatives, rationale, tradeoffs, assumptions, evidence and the remaining human decision. Reuse supplied context; ask only for material unknowns.

Begin broadly, deepen a specific weak choice when useful, and inspect related implementation or policy when the consequences require it. This progressive depth is practical guidance, not a new scoring profile. Retain a justified original choice. Absence of a rationale record is not proof that the creator gave it no thought.

## 3. Keep four evidence columns

Use the same columns and status vocabulary in templates, complete examples, imported CSVs and machine records. Each level is assessed independently.

| Column | Evidence supporting a pass | A missing or failing result |
| --- | --- | --- |
| `specified` | The cited revision defines a checkable behavior or acceptance condition | Missing or contradictory required behavior; unreviewed material remains unassessed |
| `walkthrough` | A retained walkthrough covers the requirement or scenario with a recorded outcome | A planned walkthrough is not a completed one |
| `implemented` | The cited code or connected implementation contains the relevant behavior | A mock, screen label or generated explanation is insufficient |
| `runtime_tested` | A retained execution result checks the exact implementation and relevant context | A stale result or unrelated successful run is insufficient |

Use `pass`, `fail`, `unassessed` or justified `not_applicable` per level. Never infer one column from another. Include evidence locations, including document lines when useful, and bind executed checks to the revision actually checked.

A requirement's scope and an evidence level's applicability are separate. A current requirement remains in the declared artifact inventory even when a later evidence level is not yet required at this stage. For example, a plan may have ten current requirements, with six specified passes and no runtime evidence. That is six of ten at the specified level; it is not 60% runtime readiness. The report must identify the level and stage beside every fraction.

At any reported level, retain required unassessed rows in the denominator. Report excluded/deferred items and reasons separately. A genuinely inapplicable item needs an explicit rationale and a reviewable boundary; blank cells and lack of staff are not inapplicability. Preserve the counts of passes, failures and unassessed items so the declared inventory reconciles. Zero or unknown eligible denominator means N/A with a reason, not 100%.

The historical handoff coverage measure is the intersection of specified and walkthrough passes over the applicable current inventory. It must remain named as that measure when used; specified-only coverage is a separate stage-level result. Implemented and runtime-tested coverage remain separate and never silently replace it.

For a machine-readable stage result, the required levels are:

| Stage | Required evidence |
| --- | --- |
| `specification_handoff` | Specified and walkthrough |
| `prototype_handoff` | Specified and walkthrough |
| `implementation_review` | Specified, walkthrough and implemented |
| `runtime_release_review` | All four levels |

At a required level, `not_applicable` cannot produce a pass or remove a current requirement from its denominator. You can begin and retain a useful specification review before a walkthrough exists; the missing required walkthrough produces Insufficient evidence. Later implementation and runtime statuses remain visible without blocking a specification-stage result solely because code does not yet exist.

The stage result is Hold for remediation when a required check fails, an accepted current critical or major finding remains unresolved, or an important choice has a human `revise` disposition. It is Insufficient evidence when required evidence, choice justification, a human disposition or relevant finding resolution is missing. Eligible for declared stage handoff review means the supplied record satisfies this limited route's checks. It is not engineering funding authorization, runtime certification or release permission. The tool cannot authenticate the recorded human decision or evidence.

## 4. Recognize findings before assigning severity

For each finding, record its location, expected condition, observed condition, applicable current requirement or defensible new requirement, effect and uncertainty. Separate a proposed finding from an adjudicated finding. Preserve matched, novel, unsupported, duplicate and unresolved records rather than counting every statement as a confirmed defect.

| Question | Rule |
| --- | --- |
| Is the requirement in current scope? | Check the declared stage and intended use. A future feature is not automatically a current failure. |
| Does current behavior depend on deferred work? | If a current claim, dependency or necessary control requires it now, investigate that dependency explicitly. A Phase 3 label cannot excuse a current contradiction. |
| Is this an omission or a preference? | State the applicable requirement and consequence. A preferred design pattern alone is insufficient. |
| Is it critical? | Require a defensible severe consequence, relevant exposure, current applicability and supporting evidence. A missing keyword or disclosure alone does not establish critical severity. |
| Is the source inaccessible or ambiguous? | Keep the finding provisional or unresolved. Do not claim to have verified it. |

For a runtime AI health-related plan, the absence of a disclaimer may raise a question about intended use, limitations, communication or other controls. It is not automatically a critical defect, and adding a disclaimer does not by itself establish adequate safety. Severity requires the relevant intended use, risk and evidence. This protocol supplies no legal or clinical compliance ruling.

A deferred item is not a failure solely because it is unimplemented. First ask whether the current user promise or dependency needs it. Record that reasoning and any scope correction; do not rewrite the original scope after seeing the result without a visible amendment.

## 5. Finish with an accountable next action

Report the scope and exact revision, stage and population, four evidence results, unresolved findings, choices retained or questioned, limitations, owner and next action. Keep uncertainty visible. Distinguish evidence to gather from implementation to change.

An agent-assisted or solo review can produce useful findings and artifact coverage. Reviewer-performance measures remain N/A unless their specific eligibility requirements are satisfied. Lack of an independent evaluator does not invalidate a source-cited omission; it limits claims about how well a reviewer detected omissions.

If the next question is whether to fund engineering, continue with a new or linked QUICK6/FULL engineering record and supply its baseline, risk, traceability, human review and commitment evidence. If the next question is reviewer performance, prospectively plan [independent evaluation](INDEPENDENT-EVALUATION.md). Do not repair a contaminated performance record by filling in independence fields after the fact.

## Small-team completion checklist

- Exact artifact, intended use, stage, population, scope and role overlaps are recorded.
- Consequential choices have purpose, evidence, provenance and a current disposition or open question.
- Current requirements and recovery scenarios have four independent evidence statuses and locators.
- Unassessed items remain counted; deferred or excluded work has a defensible boundary.
- Findings state current applicability, supporting evidence, uncertainty and severity basis.
- The report names the next action and owner and marks ineligible reviewer metrics N/A with reasons.

These are record-completeness checks, not proof that all defects were found. Actual-use validation of the route remains future work.

Execution versions: protocol 0.2-preview.3 · MCP 0.2.0rc9 · Skill/contract 0.2.0-rc.9.
