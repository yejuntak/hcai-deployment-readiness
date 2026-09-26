# Assessment brief

Complete and retain a dated scope record before inspection. If scope changes, preserve the prior version, record the reason and owner, and start a new criterion version. Do not overwrite a denominator after seeing the outcome.

- Session ID / artifact ID and version:
- Mode: `artifact_review` or `independent_evaluation`:
- Stage: `specification_handoff`, `prototype_handoff`, `implementation_review`, or `runtime_release_review`:
- Artifact kind: specification / prototype / code:
- Intended user, task, present claims and handoff decision:
- Artifact population: `ai_generated` / `runtime_ai` / `both` / `neither` / `unknown`:
- Generation provenance, if known; no creator reasoning inferred:
- Evaluator kind: human / agent / synthetic:
- Evaluator / artifact owner / reference author / adjudicator / decision owner:
- Role overlaps, prior artifact exposure and reference exposure:
- Criterion version / freeze time with timezone:
- Requirements and recovery brief filenames; mandatory/applicable IDs:
- Deferred and excluded items: reason, owner, present-dependency check:
- Presentation / device / environment / time limit:
- Planned task sequence and evidence recording method:
- Retention and publication permissions:

## Use the matching CSV records

Copy `requirements-brief.csv` and `recovery-brief.csv` into the review folder and freeze their scope. Complete `requirements.csv` and `recovery.csv` using those exact IDs and scope fields. The current contract is `schemas/csv-contract.json`; the templates and both worked examples use identical headers. Every evidence stage has its own status, location and reason. A plan may be assessed at specification handoff without code; unperformed implementation and runtime checks stay `unassessed` and visible.

Copy the population, stage, mode and evaluator kind into `decision.csv`. `unknown` population requires follow-up before pooling. Batch strata include criterion version, evaluator kind, artifact population, mode and stage.

Use `choice-review.csv` to inspect decisions beneath the artifact. Separate contemporaneous recorded choices and reasons from reconstructed possibilities or newly proposed alternatives. An explanation generated now does not establish the creator's actual prior reasoning. Record selection criteria and their provenance, consequences, current requirements, the human owner and the next evidence action. Keep a new current justification separate from an unknown original rationale. Retain human confirmation and verification evidence before marking an important choice accepted or revise.

## Minimal artifact-review route

One person or a small team may inspect an artifact, trace its requirements and recovery, record proposed findings, and assign remediation owners. Role overlap does not erase descriptive artifact coverage. Record the overlap. Evaluator-performance metrics remain N/A unless their independent-evaluation conditions are met. An agent may assist this descriptive route; do not report its findings as independent human performance.

A missing disclaimer is a proposed concern until its current obligation and consequential exposure are established. An explicit future-phase item is not a current defect unless the present scope depends on it. An accepted Critical finding requires evidence, current applicability, plausible severe consequence and affected exposure; the keyword alone is insufficient.

## Optional independent-evaluation packet

Keep the reference key and completed outcomes away from the evaluator until judgment is locked. The administrative reference key location belongs here, not in the delivered evaluator packet:

- Reference key version / location (withhold from evaluator):
- Expected recall estimate recorded before reference exposure:
- Judgment lock timestamp:
- Criterion frozen before review: true / false:
- Reference frozen before evaluation and independent of findings: true / false / unknown:
- Evaluator authored the artifact / authored the reference / is the adjudicator: true / false / unknown:
- Matches independently confirmed if roles overlap: true / false / unknown:
- Findings and expected recall locked before reference exposure: true / false / unknown:
- Omission subset frozen and criterion independently established: true / false / unknown:
- Any protocol deviations and affected metric claims:

Distribute the outcome-free briefs and artifact. Completed findings retain `locked_at`; adjudication adds its result and timestamp without replacing the original observation. For a real study, preserve frozen study materials and document validity conditions separately. CSV structural checks cannot establish that the declared role separation or ordering actually occurred.
