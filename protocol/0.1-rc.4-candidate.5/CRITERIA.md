# HCAI review criteria

Protocol 0.1-rc.4-candidate.5; candidate criteria, not certification.

Use these criteria to review the evidence before an engineering commitment. The software checks record structure and the six gates; a human reviewer must judge the evidence itself. The protocol does not produce an aggregate conformance score.

## Understand the work before judging the solution

### HCAI-1.1 Bound the task

Name the workflow, one unit of work, start and end boundaries, context, AI role, exclusions and a current/manual/non-AI alternative.

**How to check:** Ask a second person to describe the review's boundaries, then compare their answer with the scope record.

**Example that meets the intent:** Review one intake request from receipt to advisor confirmation; exclude live sending.

**Common failure:** Make our business AI-ready without naming a task.

**Verification:** Required fields plus accountable human scope review. Gate: G2_NEED_REQUIREMENTS.

### HCAI-1.2 Observe the current workflow

Retain an observed baseline and a connected current-state map with actors, normal work, exceptions, recovery, time, volume and an endpoint. Mark reported paths separately.

**How to check:** Follow a recent case through every step; reconcile elapsed time, labor and the sampling window. Inspect where work changes hands or returns for correction.

**Example that meets the intent:** A work log supports measured labor; a separate operator account describes an exception not observed in that sample.

**Common failure:** The owner guesses hours saved without knowing today's steps or work volume.

**Verification:** Graph and numeric checks plus direct observation review. Gate: G1_BASELINE.

### HCAI-1.3 Connect requirements to an actual need

Connect each need to an owned, checkable requirement. Use distinct original work or end-user sources at the required risk depth.

**How to check:** Ask whose difficulty the requirement resolves, what would count as success, and whether two sources share the same origin.

**Example that meets the intent:** An operator discussion and a work record independently support preserving data after cancellation.

**Common failure:** Two summaries of one conversation are presented as two independent customers.

**Verification:** Reference, origin and source-kind checks plus human relevance judgment. Gate: G2_NEED_REQUIREMENTS.

### HCAI-1.4 Include the people who bear the consequences

Name affected roles, including non-operators. Screen access/usability, privacy/security, unequal effects and human agency. Link applicable concerns to requirements and validation; justify inapplicable items with an owner and evidence. Human use/control cannot be excluded.

**How to check:** Ask who might be unable to use, correct, decline or challenge the workflow, and who could be affected without operating it. Inspect the linked success conditions and supporting evidence; a checked box alone is insufficient.

**Example that meets the intent:** A requester and an advisor can correct an intake; the requirement specifies retained data, readable error feedback and a human escalation path.

**Common failure:** The owner saves time, but a requester cannot correct a wrong generated record and nobody evaluated that effect.

**Verification:** Deterministic coverage and applicability checks plus human/context-specific review; not an accessibility, fairness, privacy or security certification. Gate: G2_NEED_REQUIREMENTS.

## Make intended behavior and evidence inspectable

### HCAI-2.1 Explain form, fit and function

Every requirement names what is represented, how it fits the surrounding workflow, what it must do and the reference material used to judge it.

**How to check:** Compare the artifact with its reference material to judge whether its role and behavior meet the requirement.

**Example that meets the intent:** A review form is linked to required intake fields, advisor responsibilities and cancellation rules.

**Common failure:** A finished-looking screen is accepted without knowing its purpose or reference requirements.

**Verification:** Structured references plus human interpretation. Gate: G4_TRACEABILITY.

### HCAI-2.2 Trace the exact artifact to a check

Each important requirement/artifact pair has an executed check bound to both its exact artifact digest and its requirement/context fingerprint. A change to acceptance criteria, scope, linked states, references, dependencies or authority invalidates the affected check.

**How to check:** Compare both fingerprints with the record captured when the check ran. Repeat the affected check after a change; computing a new hash does not constitute retesting.

**Example that meets the intent:** A cancellation walkthrough records the exact screen revision and the field-preservation result.

**Common failure:** An agent edits error handling after tests ran, but the old test pass is reused.

**Verification:** Deterministic chain and revision checks plus inspection of execution evidence. Gate: G4_TRACEABILITY.

### HCAI-2.3 Distinguish simulated from implemented behavior

Label each requirement's behavior as specified only, simulated or implemented. Do not label a walkthrough of a simulation as an implementation test.

**How to check:** Identify the connected components and the mocks. Judge functionality from evidence of behavior, independently of visual polish.

**Example that meets the intent:** The export button is simulated; the review checks the intended recovery behavior and funds only implementation of that behavior.

**Common failure:** A mock success screen is presented as proof that a payment or export completed.

**Verification:** Behavior-status and test-level consistency plus human inspection. Gate: G4_TRACEABILITY.

## Keep people able to understand and recover

### HCAI-3.1 Cover normal, edge and recovery states

Represent connected normal, edge and recovery paths with an entry, resolvable next-state IDs, reachable endpoints, data treatment, ownership and requirement links. Review transition conditions, dependency failures and bounded retry/exit behavior.

**How to check:** Try missing input, empty results, delay, unavailable dependency, cancellation and resumption where relevant. Document which cases apply.

**Example that meets the intent:** A failed save keeps entered data and explains how to retry or return to manual work.

**Common failure:** The happy path works but a failed save silently discards the user's input.

**Verification:** State/reference checks plus context-specific human walkthrough. Gate: G3_STATES_RECOVERY.

### HCAI-3.2 Make human and automated authority explicit

Record what people and automated components may access, change or send. Review approval, interruption, escalation and recovery boundaries. If AI only created the artifact, say so.

**How to check:** For an agent action, ask who authorizes it, how to stop it, what happens after partial completion and who resolves exceptions.

**Example that meets the intent:** A draft-only agent cannot send; an advisor approves changes and can return to a saved record.

**Common failure:** An agent may delete or message externally without a stated owner, approval boundary or recovery path.

**Verification:** Required boundary review plus specialist verification when risk demands it. Gate: G3_STATES_RECOVERY.

### HCAI-3.3 Count human oversight work

Estimate disjoint review, correction, escalation, rework and residual manual minutes with an owner and basis. Distinguish gross from net benefit.

**How to check:** Subtract every oversight component from gross labor savings. Keep waiting time and labor time separate. Leave missing baseline ROI indeterminate.

**Example that meets the intent:** Fifteen minutes of gross savings and fifteen minutes of oversight are reported as zero net time savings.

**Common failure:** Only generation speed is counted while a person must check and rewrite every output.

**Verification:** Required fields and arithmetic plus human estimate review. Gate: G5_OVERSIGHT.

## Make the commitment accountable

### HCAI-4.1 Scale depth before starting

Classify six risk dimensions and four consequential-context flags. Use the highest dimension or context floor. Safety/rights impact or irreversible external action sets high; sensitive data or untrusted input to actions sets at least moderate. Any unknown prevents QUICK6.

**How to check:** Review consequence, reversibility, complexity, importance, impact and mission before choosing the path. Do not lower the classification to fit the meeting's length.

**Example that meets the intent:** A consequential allocation workflow goes to FULL even when its interface has only one screen.

**Common failure:** A simple-looking UI is treated as low risk despite an irreversible outcome.

**Verification:** Deterministic routing plus competent human risk classification. Gate: G6_COMMITMENT.

### HCAI-4.2 Resolve findings at the required depth

Review reference defects, findings and unresolved risks. Unresolved critical findings cannot be waived. Add independent review and deeper plans when the risk tier requires them. A recorded human evidence-quality review must address relevance, completeness, authenticity and test adequacy; agent-only assertions cannot replace it.

**How to check:** Inspect each unresolved finding; passing other gates cannot offset it. Verify reviewer independence for moderate/high risk.

**Example that meets the intent:** A critical data-loss defect stays visible even when the baseline is also missing.

**Common failure:** A critical finding is marked accepted to obtain a favorable readiness result.

**Verification:** Finding status and evidence checks plus reviewer judgment. Gate: G6_COMMITMENT.

### HCAI-4.3 Limit the engineering commitment

Record an owner, bounded engineering step, resource limit and next review trigger. Explain any investment despite a nonpositive net estimate; obtain separate owner authorization.

**How to check:** Ask what the team may build next and what it may not do yet. Retain a separate dated owner decision.

**Example that meets the intent:** One engineer-day for a disposable prototype, with no live sending and a review before further work.

**Common failure:** A gate pass is treated as permission for unrestricted building or deployment.

**Verification:** Recorded bounds and rationale; authorization remains a separate human act. Gate: G6_COMMITMENT.

### HCAI-4.4 Separate effort from performance

Record preparation, timed-session and reporting burden. Keep protocol cost, projected operating oversight, reviewer judgments and actual system performance separate.

**How to check:** Check units and which activity each number measures. Do not infer operational accuracy, safety or readiness from document completeness.

**Example that meets the intent:** An expensive evaluation is reported separately from the workflow's projected operating cost.

**Common failure:** A high checklist score is reported as evidence that the implemented system works.

**Verification:** Separate contract fields and arithmetic; no combined score. Gate: G6_COMMITMENT.

### HCAI-4.5 Preserve evidence and disclosure boundaries

Retain exact versions, source origins, digests and previous-run links. Preserve missing and stopped records. Keep private identities/comments out of public materials without permission.

**How to check:** Check whether another reviewer could reconstruct the run and whether each proposed disclosure is permitted. Retain the old record when creating a new run.

**Example that meets the intent:** A new FULL record links to the stopped QUICK6 record; private notes remain outside the public package.

**Common failure:** A synthetic example is relabeled as an actual pilot or private feedback is published as an endorsement.

**Verification:** Structural provenance checks plus human permission review; hashes alone do not prove truth. Gate: G6_COMMITMENT.
