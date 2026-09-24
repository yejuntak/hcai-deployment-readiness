# Review AI-built workflows before engineering

Human-Centered AI Deployment Readiness Protocol — Engineering-Handoff Profile  
Protocol 0.1-rc.4-candidate.2 · MCP 0.2.0rc2 · Skill 0.2.0-rc.2

## What this helps you decide

**Is there enough evidence to commit engineering resources to this bounded workflow?**

A polished booking screen may look complete while losing a customer's details after a payment failure. A passing test may belong to yesterday's code, before an agent changed it. This guide helps a reviewer distinguish what looks finished from what has actually been demonstrated.

Use it for proposed workflows, interface prototypes, and AI-assisted, “vibe-coded,” or agent-built artifacts. AI may have helped create the artifact without being part of the eventual service. Record which is true. These are application scenarios, not evidence that AI authorship causes defects.

The historical title contains “Deployment Readiness.” This profile **does not approve deployment**, measure full-system performance, or certify software quality. A supported engineering commitment is one decision; permission to operate is another.

## Start with the smallest useful path

- New here? Read [Start here](START-HERE.md).
- Reviewing a low-risk workflow with records already available? Use [QUICK-6](QUICK-6.md).
- Need an example? Read the [scenarios](SCENARIOS.md).
- Need to inspect a particular rule? Use the [14 review criteria](CRITERIA.md).
- Higher risk, missing evidence, or a longer review? Use the [full profile](FULL-PROFILE.md).

An advisor can ask the questions aloud and record answers. Participants do not need to edit JSON, install a tool, or understand an evaluation framework. “We do not know yet” is a useful answer: it identifies the next piece of work.

## Six questions, one next action

1. **What happens today?** Show a recent case, who touched it, how long it took, and where it failed or needed rework.
2. **What needs to improve, for whom?** State the intended outcome and evidence of an actual end-user need.
3. **What happens when things go wrong?** Explain normal, edge, recovery, and escalation paths, including human and automated responsibilities.
4. **What demonstrates the important behavior?** Connect each requirement to an exact artifact revision and an appropriate test or validation.
5. **What work remains for people?** Estimate review, correction, escalation, rework, and residual manual effort before claiming savings.
6. **Is this enough to fund the next engineering step?** Apply the risk tier, resolve critical findings, and record the owner, limits, and remaining uncertainty.

A critical gate cannot be averaged away. QUICK-6 stops at the first failed or missing gate; later gates say NOT_EVALUATED. Known critical findings remain visible even when the review stops earlier. A stopped session is a useful result, not a failed participant.

The <=15-minute QUICK-6 target is an **untested design target**, not a measured completion rate. It assumes records are available. Count capture and explanation within the session; report preparation separately. Take breaks, use accessible formats, or move to FULL without treating the participant as deficient.

## What the result means

| Result | Meaning | What happens next |
| --- | --- | --- |
| PROCEED_TO_ENGINEERING | Required upstream evidence passes for the recorded scope and risk tier. | The accountable owner decides whether to fund the bounded next step. This is not deployment permission. |
| REVISE | Evidence demonstrates a failed gate or a critical unresolved finding. | Name the repair, owner, and evidence needed for another review. |
| INSUFFICIENT_EVIDENCE | Required information is missing, or the selected profile is insufficient. | Obtain the missing evidence or continue in FULL. Do not substitute confidence for evidence. |

Every result includes a plain-language explanation, the first useful next action, gate status, separate burden/benefit outputs, evidence links or identifiers, and exact versions. A recommendation is not a spending authorization. Never convert it into a general “AI readiness score.”

## Four principles; inspectable criteria

The structure borrows the idea of principles, testable criteria, and practical techniques from [WCAG 2.0's layers of guidance](https://www.w3.org/TR/WCAG20/#intro-layers-guidance). This is an author-defined candidate, **not a W3C standard, accessibility conformance claim, or A/AA/AAA certification**.

| Principle | Review focus | Criteria |
| --- | --- | --- |
| Understand the work before judging the solution | Scope, current workflow, actual need | HCAI-1.1–1.3 |
| Make intended behavior and evidence inspectable | Form/fit/function, exact tested revision, simulated versus implemented behavior | HCAI-2.1–2.3 |
| Keep people able to understand and recover | Failure paths, human control, remaining work | HCAI-3.1–3.3 |
| Make the commitment accountable | Risk depth, findings, ownership, separate measurements, provenance | HCAI-4.1–4.5 |

Each criterion has a requirement, a way to check it, and pass/failure examples. Deterministic checks enforce structure and boundaries; a human must still judge evidence quality. A correctly linked file can still contain a bad test.

## Evidence must describe the work, not just the proposal

The current-state map records connected steps, actors, triggers, actions, data handling, branches, and endpoints. Distinguish observed steps from reported exceptions. Record cycle time separately from labor time; elapsed waiting is not labor savings.

Need evidence must come from actual work records or end-user discussions, with distinct source origins. Two renamed copies of the same interview are one source. General reports and correspondence informing this protocol do not establish the need for a particular workflow.

Traceability means **requirement → artifact revision → test/validation**. Describe form (what is shown), fit (how it connects to the surrounding workflow), and function (what it does). A visual demonstration can support design intent; it cannot establish implementation behavior. A code change after testing requires fresh evidence for affected requirements.

## Risk changes the required evidence

Classify impact, importance, complexity, failure consequence, irreversibility, and mission criticality before choosing the path. The highest known dimension sets the minimum depth. An unknown dimension prevents a low-risk shortcut.

| Minimum evidence | Low | Moderate | High |
| --- | --- | --- | --- |
| Profile | QUICK-6 or FULL | FULL | FULL |
| Current cases | 1 | 3 | 5 |
| Distinct need-source origins | 1 | 2 | 2 |
| Actual end-user discussion | Not mandatory; work evidence still required | Required | Required |
| Additional review | Owner review | Independent review and evaluation plan | Also hazard, mission, and operational-evaluation planning |

These counts are provisional minimum completeness rules, **not statistically adequate sample sizes**. All tiers need the same six basic gates. More consequential work may require domain-specific review beyond this profile.

## Five measurement layers stay separate

A. **Current state:** cycle time, labor, touches, failure points, review, escalation, rework, volume, and the workflow map.  
B. **Proposed workflow:** requirements, states, recovery, responsibility, dependencies, acceptance criteria, and action boundaries.  
C. **Burden:** the cost of running this review, separately from the expected cost of overseeing AI outputs in operation.  
D. **Engineering evidence:** requirement/artifact/validation links, defects, reviewer findings, residual risks, and the decision record.  
E. **Operational performance:** measured only after implementation in realistic use. Not inferred from A–D.

Gross time saved minus review, correction, escalation/rework, and residual manual work gives a net labor estimate. Recurring operating costs and one-time implementation costs remain visible. Without a measurable baseline, ROI is indeterminate. Nonpositive net benefit requires an explicit investment rationale; the tool does not hide it behind a passing gate.

## Research and practice are different activities

The related proposed study investigates visual fidelity and defect detection while AI authorship is held constant. Perceived handoff readiness and confidence are separate judgments, not proof of correctness. This protocol is a practical response to that review problem, not a validated intervention or a result of the proposed experiment.

Do not give experimental participants criterion hints or answer keys unless the approved study design calls for them. The separate study-review contract captures judgments without issuing an engineering decision. See [research boundaries](../../docs/research-boundary.md).

## Limitations and release status

Practitioner correspondence informed refinement; it is not controlled empirical validation, proof of adoption, or an endorsement. No actual external pilot is recorded in this release. Usability, time-to-complete, benefit, and defect-prevention effects remain untested.

Records are private by default. Publish only separately permission-checked material. Hillel Glazer approved attribution; other correspondence is represented by anonymized themes unless explicit permission is documented. Do not upload confidential artifacts simply to complete a field.

rc.3 and the first rc.4 candidate remain frozen. This is a new candidate, not final rc.4. Promotion requires passing regression checks and recorded bounded external end-user/advisor use. Research Harness v3 is a separate project, not this protocol's version.

See the [linked update log](https://www.takyejun.com/research/ai-readiness/updates) and [migration notes](../../docs/migration-rc3-to-rc4.md).
