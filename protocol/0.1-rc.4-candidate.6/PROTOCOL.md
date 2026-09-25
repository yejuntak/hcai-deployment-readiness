# Review AI-built workflows before engineering

Human-Centered AI Deployment Readiness Protocol: Engineering-Handoff Profile  
Protocol 0.1-rc.4-candidate.6 · MCP 0.2.0rc6 · Skill 0.2.0-rc.6

## What this helps you decide

**Is there enough evidence to commit engineering resources to this bounded workflow?**

A booking screen can look complete yet lose a customer's details after a payment failure. A test report can show a pass for code that an agent has since changed. This protocol asks reviewers to examine the evidence for the proposed workflow before the team commits engineering resources.

The intended uses include proposed workflows, interface prototypes, and AI-assisted, “vibe-coded,” or agent-built artifacts. Record whether AI helped create the artifact, will act within the service, or both. These applications do not establish that AI authorship causes defects.

Although the historical title contains “Deployment Readiness,” this profile **does not approve deployment**. It neither measures full-system performance nor certifies software quality. The evidence needed to fund engineering differs from the evidence needed to permit operation.

## Choose a reading path

- New here? Read [Start here](START-HERE.md).
- Reviewing a low-risk workflow with records already available? Use [QUICK-6](QUICK-6.md).
- Need an example? Read the [scenarios](SCENARIOS.md).
- Need to inspect a particular rule? Use the [15 review criteria](CRITERIA.md).
- Want a simple recording aid? Use the [conversation worksheet](WORKSHEET.md).
- Higher risk, missing evidence, or a longer review? Use the [full profile](FULL-PROFILE.md).

An advisor can ask the questions aloud and record answers. Participants need no software installation or knowledge of the data format. When an answer is unknown, record the gap and identify the evidence needed to resolve it.

## The six review questions

1. **What happens today?** Show a recent case, who touched it, how long it took, and where it failed or needed rework.
2. **What needs to improve, for whom?** State the intended outcome and evidence of an actual end-user need.
3. **What happens when things go wrong?** Explain normal, edge, recovery, and escalation paths, including human and automated responsibilities.
4. **What demonstrates the important behavior?** Connect each requirement to an exact artifact revision and an appropriate test or validation.
5. **What work remains for people?** Estimate review, correction, escalation, rework, and residual manual effort before claiming savings.
6. **Is this enough to fund the next engineering step?** Apply the risk tier, resolve critical findings, and record the owner, limits, and remaining uncertainty.

QUICK-6 stops at the first failed or missing gate and marks later gates NOT_EVALUATED. Known critical findings remain visible even after an earlier stop. Passing other gates cannot offset a critical failure. The stop identifies unfinished work; it is not a judgment of the participant.

QUICK-6 has an **untested design target of <=15 minutes**, assuming records are already available. Session time includes recording answers and explaining the result; preparation is reported separately. Offer breaks or accessible formats when needed. If the review takes longer, continue in FULL without treating the participant as deficient.

## What the result means

| Result | Meaning | What happens next |
| --- | --- | --- |
| PROCEED_TO_ENGINEERING | Required upstream evidence passes for the recorded scope and risk tier. | The accountable owner decides whether to fund the bounded next step. This is not deployment permission. |
| REVISE | Evidence demonstrates a failed gate or a critical unresolved finding. | Name the repair, owner, and evidence needed for another review. |
| INSUFFICIENT_EVIDENCE | Required information is missing, or the selected profile is insufficient. | Obtain the missing evidence or continue in FULL. Do not substitute confidence for evidence. |

The result explains the recommendation and names a next action. It also retains gate statuses, separate burden and benefit outputs, evidence links or identifiers, and exact versions. The accountable owner must authorize spending separately. The protocol does not produce a general “AI readiness score.”

## Principles and review criteria

Four principles organize the review criteria. Each criterion states the required evidence, a way to check it and examples of adequate and inadequate evidence. This author-defined HCAI protocol supports engineering-commitment reviews; it does not certify a system or approve deployment.

| Principle | Review focus | Criteria |
| --- | --- | --- |
| Understand the work before judging the solution | Scope, current workflow, actual need, affected people | HCAI-1.1 to 1.4 |
| Make intended behavior and evidence inspectable | Form/fit/function, exact tested revision, simulated versus implemented behavior | HCAI-2.1 to 2.3 |
| Keep people able to understand and recover | Failure paths, human control, remaining work | HCAI-3.1 to 3.3 |
| Make the commitment accountable | Risk depth, findings, ownership, separate measurements, provenance | HCAI-4.1 to 4.5 |

Each criterion states a requirement and explains how to check it, with examples of a pass and a failure. The software checks record structure and decision rules. A human reviewer must judge the evidence itself: a correctly linked file may still contain an inadequate test.

A pass establishes that the supplied record satisfies the encoded rules and includes the required human judgments. It does not independently establish that the evidence is true, complete, adequately tested, or consistent with each criterion's intent. A human evidence-quality reviewer must examine those questions and retain the basis for the review. Agent-only review is insufficient. Both the machine result and the readable report state these limits.

### Include people affected by the workflow

Name affected roles beyond the purchaser or operator. Within question 2, screen access/usability, privacy/security, unequal effects, and human agency. Connect applicable concerns to requirements and validation. For example: can a requester correct a generated record, use an alternative channel, understand an error, and reach a person with authority to help?

Keep unknown items unresolved. A not-applicable item requires an owner, reason and evidence; human use and control cannot be excluded. This screen identifies concerns for review. It does not certify fairness, privacy, security or accessibility. Seek specialist review where the effects exceed the team's competence.

## Establish the baseline and trace the evidence

The current-state map records connected steps, actors, triggers, actions, data handling, branches, and endpoints. Distinguish observed steps from reported exceptions. Record cycle time separately from labor time; elapsed waiting is not labor savings.

Need evidence must come from actual work records or end-user discussions, with distinct source origins. Two renamed copies of the same interview are one source. General reports and correspondence informing this protocol do not establish the need for a particular workflow.

Traceability means **requirement → artifact revision → test/validation**. Describe form (what is shown), fit (how it connects to the surrounding workflow), and function (what it does). A visual demonstration can support design intent; it cannot establish implementation behavior. A code change after testing requires fresh evidence for affected requirements.

Each validation also records a requirement/context fingerprint covering acceptance criteria, scope, linked states, reference revisions, dependencies and action boundaries. A changed requirement invalidates the affected pass even if the code is unchanged. Repeat the affected checks; replacing an old hash is not retesting. Current and proposed state maps must have connected paths and a reachable endpoint. These graph checks establish possible paths, but cannot show that a running system always terminates or recovers.

## Risk changes the required evidence

Classify impact, importance, complexity, failure consequence, irreversibility, and mission criticality before choosing the path. The highest known dimension sets the minimum depth. An unknown dimension prevents a low-risk shortcut.

Four context answers set additional minimums: safety/rights impact or irreversible external action → **high**; sensitive data or untrusted input capable of triggering actions → **at least moderate**. Any unknown answer prevents QUICK-6. The highest dimension or context minimum wins. These conservative author-defined routing rules are not a validated risk taxonomy; see the full profile for definitions.

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
E. **Operational performance:** measured only after implementation in realistic use. It cannot be inferred from layers A through D.

Gross labor savings already deduct residual manual work. Net savings also deduct review, correction, escalation and rework; use the disjoint categories and formulas in the full profile. Report recurring and one-time costs separately. ROI is indeterminate without a measurable baseline. Retain any nonpositive net benefit and an explicit rationale for proposed investment.

## Research and practice are different activities

The related proposed study investigates visual fidelity and defect detection while AI authorship is held constant. Perceived handoff readiness and confidence are separate judgments, not proof of correctness. This protocol is a practical response to that review problem, not a validated intervention or a result of the proposed experiment.

Do not give experimental participants criterion hints or answer keys unless the approved study design calls for them. The separate study-review contract captures judgments without issuing an engineering decision. See [research boundaries](../../docs/research-boundary.md).

## Limitations and release status

Practitioner correspondence informed refinement; it is not controlled empirical validation, proof of adoption, or an endorsement. No actual external pilot is recorded in this release. Usability, time-to-complete, benefit, and defect-prevention effects remain untested.

Records are private by default. Publish only separately permission-checked material. Hillel Glazer approved attribution; other correspondence is represented by anonymized themes unless explicit permission is documented. Do not upload confidential artifacts simply to complete a field.

rc.3 and candidates.1 through .5 remain frozen. Candidate.6 removes an inaccurate external-standard comparison; gates, risk thresholds and calculations are unchanged. Final rc.4 still requires passing regressions and recorded bounded external end-user/advisor use, neither of which proves effectiveness. Research Harness v3 is a separate project.

Whether this review improves engineering decisions remains untested. See the [deep audit and validation roadmap](../../docs/deep-audit.md) and [claims and governance rules](../../docs/claims-and-governance.md).

See the [linked update log](https://www.takyejun.com/research/ai-readiness/updates) and [migration notes](../../docs/migration-rc3-to-rc4.md).
