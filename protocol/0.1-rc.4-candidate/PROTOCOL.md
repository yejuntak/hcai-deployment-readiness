# Human-Centered AI Deployment Readiness Protocol

## Engineering-Handoff Profile: engineering-commitment readiness

Version 0.1-rc.4-candidate · September 24, 2026 · Yejun Tak

Companions: MCP 0.2.0rc1; ai-ready Skill 0.2.0-rc.1; contract 0.2.0-rc.1.
Status: candidate for bounded external use. No candidate DOI or final rc.4 release.

### 1. The decision and its limits

This upstream instrument asks whether the available evidence supports committing a bounded amount of engineering effort to a defined AI-related workflow. It starts with the current workflow and end-user need, before reviewing the proposed solution. Testability is decided while requirements and intended workflow are being defined.

The historical program title is retained for continuity. This profile does not decide deployment readiness, measure full-system performance, certify a product, or demonstrate that an AI approach is better than the current process. Deployment requires separate post-implementation evaluation with real operators under realistic conditions. Complete documentation and successful upstream walkthroughs cannot substitute for that evidence.

Record whether AI generates the artifact, runs in the proposed workflow, both, or neither in the frozen scope. Identify the intended users, environment, task boundaries, alternatives, dependencies and exclusions. An engineering commitment may fund a disposable prototype or limited feasibility implementation; specify its resource ceiling and next review trigger. A recommendation is not owner authorization.

### 2. Five measurement layers

| Layer | Capture | What it supports |
| --- | --- | --- |
| A. Current state | Observation window and sample, current states and actors, cycle time, labor time, handoffs/touches, failure points, manual review, escalation, rework, volume/frequency | A grounded comparison and a baseline gate |
| B. Proposed workflow | End-user need, measurable requirements and acceptance criteria, normal/edge/recovery paths, data preservation, ownership and dependencies | An inspectable intended behavior |
| C. Evaluation and oversight burden | Protocol elapsed time and disjoint evaluator/participant/adjudication minutes; participants, correction cycles, calls, tokens and costs when available; a separate operational oversight estimate | Evaluation affordability and projected operating burden, reported separately |
| D. Engineering handoff | Requirement → artifact → executed validation links, form/fit/function references, reference defects, reviewer findings, unresolved risks, evidence completeness and decision record | A bounded engineering recommendation |
| E. Operational performance | Actual measurements collected after implementation, with implementation version, realistic context and observation records | A separate operational evaluation; never inferred from A–D |

There is no total score. Evaluator quality, evaluator burden, operating oversight and system performance have different meanings and must remain separate outputs. Missing is not zero. A critical gate cannot be averaged away.

### 3. Evidence preparation and roles

The workflow owner supplies current-state records and a proposed artifact. The advisor/evaluator examines evidence. A reference reviewer checks requirements, states and defect records. An adjudicator resolves disagreements. The engineering decision owner records the commitment or refusal. Disclose overlapping roles. Moderate and high tiers require a reviewer independent of the artifact owner and a recorded role/separation statement.

Freeze the run ID, timestamp with timezone, exact four-part version set, artifact versions, evidence identifiers and SHA-256 digests. Retain original records separately from interpretations. Each evidence item has an ID, locator, version, digest, description and kind: observed, estimate, assumption or synthetic. The engine validates references and digest format; it does not fetch artifacts or establish truth from a hash. Verify bytes locally when collecting evidence.

Baseline evidence must be observed. Estimates and assumptions cannot establish a measured baseline. Synthetic evidence is permitted only in explicitly synthetic runs and never in actual pilots. Zero values need an assessed basis. A current-state baseline includes labor minutes as well as elapsed cycle time: waiting time must not be monetized as employee labor savings.

Every requirement states its end-user need, owner, measurable acceptance criterion, form (what is represented), fit (how it belongs in the workflow/dependencies), function (what it must do), and reference material. Every important artifact or behavior must link back to a requirement and to a validation of that requirement on that artifact. A test plan alone is not an executed walkthrough. A walkthrough pass supports specification review; it is not proof of implementation or operating performance.

For an evaluator-comparison study, retain rc.3's separate evaluator packet and reference key. Lock raw findings, expected reference-defect recall and judgment before disclosure. Record matched, duplicate, unsupported, novel genuine and unresolved findings separately. New defects may affect the decision but must not silently change the frozen recall denominator. Preserve abstentions, missing judgments and criterion uncertainty; stratify different criteria and human/agent/synthetic populations. Public examples are training material, not unseen test cases.

### 4. Risk tier and deterministic depth

Classify each of six dimensions as low, moderate or high: complexity, importance, impact, mission, failure consequence and irreversibility. Retain rationale and evidence. The resulting tier is the highest dimension. An unknown dimension makes the tier unknown and prevents a qualifying pass. Do not lower a tier to fit available time.

Low means a narrow, reversible workflow with limited consequences, readily detected errors and a manual fallback. Moderate includes multiple actors or integrations, material rework/cost, or consequential decisions with practical recovery. High includes serious harm or rights impacts, mission-critical decisions, hard-to-reverse actions, or complex failures whose consequences are difficult to bound. These are classification anchors, not legal determinations or a validated risk instrument. Record context; a competent owner must review the classification.

| Required evidence | Low | Moderate | High |
| --- | --- | --- | --- |
| Profile | QUICK6 or FULL | FULL | FULL |
| Observed baseline cases | At least 1 | At least 3 | At least 5 |
| Distinct need-source records per need | At least 1 | At least 2 | At least 2 |
| Actual end-user discussion evidence | Recommended | Required | Required |
| All six core gates | Required | Required | Required |
| Independent review and validation plan | Optional | Required | Required |
| Hazard analysis, mission review and operational evaluation plan | Optional | Optional | Required |

The counts are provisional minimum evidence floors for candidate feasibility testing, not claims of statistical representativeness, sufficient test coverage or validated safety thresholds. Independent sources must reflect genuinely distinct observations or perspectives, not duplicated files. Full review can require a larger sample when heterogeneity warrants it; the minimum never prohibits deeper review. Repeated evaluation after changed scope creates a new run/versioned record.

### 5. Six mandatory gates

G1_BASELINE: quantify the current workflow. All Layer A fields must be present, with positive volume, defined period, required sample count and observed evidence. A baseline-free proposal cannot proceed. ROI remains indeterminate until this gate passes.

G2_NEED_REQUIREMENTS: state the outcome and end-user need, meet the tier's source/discussion requirements, and connect each need to at least one owned requirement with measurable acceptance criteria. Practitioner feedback about the protocol does not itself establish a customer's need for a proposed product.

G3_STATES_RECOVERY: define normal, edge and recovery paths with triggers, actions, resulting states, data treatment, owner and requirement links. Every requirement needs behavior coverage. Review dependencies and state completeness with evidence and rationale. A simple workflow still needs an error/edge case and a safe recovery such as cancel or return to manual work. Missing paths prevent a pass.

G4_TRACEABILITY: cover every important artifact and every requirement/artifact pair with linked validation. Retain form/fit/function reference material. Missing execution evidence or merely specified tests are insufficient; a broken chain or a documented failed validation requires revision. Visual fidelity supplies no substitute.

G5_OVERSIGHT: estimate review, correction, escalation, rework and residual manual minutes per case, with a responsible role and evidence/assumption basis. Keep components disjoint to avoid double counting. Explicit assessed zero is allowed. A favorable gross savings claim cannot suppress these costs.

G6_COMMITMENT: apply the tier's extra reviews, record defect/finding/risk inventories, check reference and findings completeness, and record risk acceptance. An unresolved critical finding cannot be waived by marking it accepted. Open major findings block. Record the decision owner, bounded commitment, resource limit and next review trigger. Capture elapsed time, evaluator/participant/adjudication minutes, participant count and review/correction cycles; unknown model calls/tokens/costs stay null. QUICK6 must be timed at 15 minutes or less. Missing or failed requirements prevent a pass.

### 6. Decision rules and QUICK6 stop behavior

PROCEED_TO_ENGINEERING: every required evaluated gate passes. The output remains a recommendation for the specified engineering scope. The owner must separately record authorization, date and conditions.

REVISE: at least one evaluated gate documents a failure, including broken traceability, failed validation or an unresolved blocking finding. Retain all missing evidence as well.

INSUFFICIENT_EVIDENCE: no documented failure has priority, but at least one required gate lacks evidence, risk is unknown, QUICK6 cannot satisfy the tier, or QUICK6 exceeded its time limit.

For FULL, evaluate and report all six gates; documented failure takes precedence over missing evidence. For QUICK6, stop at the first non-pass gate, mark later gates NOT_EVALUATED and base the decision on the evaluated gates only. Return the stop reason and require a new FULL run after evidence gathering/remediation. High or moderate risk automatically requires FULL even if a QUICK6 request was submitted. No later pass can rescue a stopped QUICK6 run. An empty/invalid contract is rejected without a decision.

The advisor-led QUICK6 target is <=15 minutes including the discussion, evidence check, decision and burden record, using existing records. It does not promise to collect a missing baseline in that time. Stop early when records are absent. See QUICK-6.md for the six prompts and proposed time allocation; the time target remains untested.

### 7. Gross savings, net benefit and protocol cost

Use consistent per-case and per-period units. All operating outputs are scenario estimates until separately measured after implementation.

- Gross minutes saved per case = current labor minutes − proposed residual manual minutes.
- Oversight minutes per case = review + correction + escalation + rework.
- Net minutes saved per case = gross minutes saved − oversight minutes.
- Net period minutes = net per-case minutes × baseline volume for that period.
- Baseline operating cost = baseline labor hours × hourly cost × volume + baseline nonlabor cost for the period.
- Proposed operating cost = (residual manual + oversight) hours × hourly cost × volume + proposed nonlabor per-case cost × volume + recurring fixed cost.
- Net operational benefit = baseline operating cost − proposed operating cost.
- Recurring ROI percentage = 100 × net benefit / proposed recurring operating cost, only when that denominator is positive. This is an explicitly defined comparison, not a universal investment ROI measure.
- Implementation payback periods = one-time implementation cost / positive recurring net benefit. Otherwise report null; do not invent payback when benefit is zero/negative or implementation cost is unknown.

Report one-time implementation cost separately; do not silently amortize it. Unknown monetary inputs produce TIME_ONLY, with monetary ROI indeterminate. Missing baseline or oversight produces INDETERMINATE and null savings. A negative net estimate remains visible and is not a system failure metric; an owner may fund bounded investigation for a documented nonfinancial need.

Protocol evaluation cost = disjoint evaluator + participant + adjudication person-minutes / 60 × the recorded blended hourly rate + tool/model cost, in the stated currency. Elapsed wall-clock time is separate. Unknown rates/costs yield indeterminate cost while retaining measured minutes. These evaluation expenses are excluded from workflow operating cost and operating ROI. Any later total investment analysis must add them explicitly and state its time horizon.

### 8. Records, feedback permissions and bounded pilots

Keep a feedback ledger with source/person, date, context, feedback, permission basis, protocol change IDs, affected files/requirements and validation status. An internal ledger may retain private correspondence; public exports allow only approved attribution and comments. Hillel Glazer approved attribution by email. Other identities/comments remain private unless separately approved. Permission to attribute a suggestion is not an endorsement of the instrument or its results.

The change manifest connects observed problems or feedback themes to requirements, implementation files and acceptance tests. Public themes are authored design rationales; private email wording and identities are withheld. Correspondence informed refinement; it is not controlled empirical validation.

The next evidence stage is actual bounded use of one real workflow with an external end user or advisor. Outreach, an invitation to meet, willingness to review, automated acknowledgments and expressions of interest are not pilot results or adoption. A short voluntary packet is supplied so a practitioner can participate without reading the full method. No organization is represented as sponsoring, arranging or requiring participation.

A pilot record captures date, role/sector, pseudonym, permission/anonymization, actual-use and external-participant flags, profile, derived risk tier, elapsed time, all gate outcomes, missing evidence, optional before-decision, after-decision, triggered revision, participant feedback and observation references. The complete assessment embeds exact versions, artifact versions/digests and evidence provenance. Validation rejects inconsistencies. A synthetic fixture can test this format but cannot count toward release eligibility.

Preserve negative findings and stopped sessions. Capture whether a gate changed or clarified the decision, where participants were confused, and time spent gathering evidence versus using the instrument. Do not reconstruct a pre-decision after showing the result; leave it null. Obtain any applicable institutional research determination before covered recruitment/data collection. This packet does not supply institutional approval.

### 9. Release, migration and limitations

rc.3 remains frozen in historical/rc3-baseline with a manifest of exact byte hashes, original archive/PDF and historical tag commit IDs. Root legacy PDFs/workbooks and Source/Protocol-v0.1.md remain historical, not candidate implementations. Their DOI 10.5281/zenodo.22667623 identifies rc.3 only. Do not recalculate old results as if this contract had been used.

The candidate MCP, CLI and portable Skill run the same engine and schema. Generated copies are byte-checked. Prompts assist interpretation but cannot override gates or thresholds. Legacy evaluator calculations remain explicitly named and versioned as rc.3. MCP 0.2.0rc1 and Skill 0.2.0-rc.1 signal a changed contract; old software tags are preserved.

Remain a candidate until current regression tests pass and at least one bounded external end-user/advisor use with feedback has been recorded and checked by the author. Passing software tests establishes implementation behavior only. One pilot establishes bounded feasibility evidence, not controlled effectiveness, generalizability, adoption or an endorsement. No automatic promotion or publication occurs in the release checker.

Untested assumptions include the <=15-minute target, classification anchors, minimum samples/source counts, evidence sufficiency for engineering decisions, consistency between advisors, business benefit of the method and comparative improvement over a strong existing checklist. Self-reported evidence can be wrong; structural checks do not prove completeness or authenticity. Hashes support reproducibility, not truth. Research Harness assets are architectural references only; Research Harness v3 is not this protocol or its validation evidence.

Historical theoretical references and evaluator definitions remain available in the frozen rc.3 source. This update introduces no new literature-verification or priority claim. Development and technical checks were AI-assisted; author review, external use and empirical validation are distinct stages.

Original method and synthetic data: CC BY 4.0, Yejun Tak. Original software: MIT. Attribution does not imply endorsement.
