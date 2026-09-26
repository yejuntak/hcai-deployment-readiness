# Research question and practical use

H.A.R.D. Protocol 0.2 · Public Preview · Exact protocol 0.2-preview.3

The proposed study examines how visual fidelity affects human review of AI-generated interface prototypes. Requirements, content, behavior and embedded defects are held constant, as is AI authorship. The protocol serves a separate practical purpose: inspecting choices and evidence in an artifact, and, through QUICK6/FULL, reviewing evidence before a team funds engineering. It is neither the experimental treatment nor evidence that the hypothesized effect exists.

## Definitions and measurement boundaries

The author's originating anecdote concerns architectural previsualization: an architect described presenting an intermediate 3D view with a watercolor treatment to invite discussion of overall structure. No firm or individual is identified here. The anecdote motivates a question; it does not establish the treatment's effect.

The practical protocol starts from a finished-looking artifact and works backward through its choices: product purpose, criteria, alternatives, rationale, tradeoffs, verification and missing human judgment. The original choice can be retained when justified. This inspection can reveal questions about information structure, workflow, technical evidence or operating responsibility that have not yet been resolved. This is an application hypothesis, not a finding that AI always skips those steps. In practice a separate structural view may expose questions. It should preserve relevant information and label unknowns, not merely blur the original.

| Construct | Meaning in this work | Do not substitute |
| --- | --- | --- |
| Visual fidelity | Presentation attributes such as typography, spacing, hierarchy and component styling | Functional completeness or correctness |
| Requirements correctness | Whether specified behavior meets the frozen requirement and reference judgment | Visual appeal, general usefulness or brand fit |
| Defect detection | A reviewer's judgment on a defined requirement or defect opportunity | A global impression of readiness |
| Perceived handoff readiness | A separately recorded subjective judgment | The protocol's rule-based engineering recommendation |
| Confidence calibration | Relationship between item-level confidence and correctness across sufficient observations | A few global confidence ratings |
| Operational performance | Implemented behavior with real operators in realistic use | Documents, prototypes or upstream review completeness |

“Fidelity-maturity mismatch” is a study-specific framing, not a validated construct or established effect. A polished prototype may be correct or defective. Determining whether polish changes defect detection requires experimental evidence; protocol software tests cannot answer that question.

## Practice reviews and research sessions

**In practice**, a solo practitioner or small team can use artifact_review at a declared specification, prototype, implementation or runtime-review stage. It produces a bounded evidence record and next action, without requiring financial measurements or independent research roles. QUICK6/FULL separately retain the six gates for a bounded engineering recommendation. Neither route establishes runtime performance from specification completeness.

**For optional independent evaluation**, apply the [metric eligibility rules](../protocol/0.2-preview.3/INDEPENDENT-EVALUATION.md). Role overlap does not eliminate useful artifact findings, but it can make evaluator-performance measures N/A. Agent, human and assisted-human populations remain distinct, as do AI-generated, runtime AI, both and neither artifact populations. Stratification is necessary but does not itself establish a sound study design.

The rationale draws on a proposed common pattern of expert work: interpret purpose, define criteria, compare alternatives, choose in context and verify the result. This is a design premise, not a demonstrated theory of expertise across domains. A newly generated reason is not evidence of the creator's historical reasoning, and no private chain-of-thought reconstruction is claimed. Designers, developers and small-business advisors are intended users; usability and benefit remain unvalidated.

**For a study**, the researcher freezes the requirements, intact and defective items, reference key, artifacts, generation/edit history, study version and assignment schedule. Reviewers do not receive the answer key before their judgments are locked. Do not use the guided practice prompts or public worked example as an unplanned experimental intervention: they could change detection and contaminate the comparison.

The optional `study-review` schema stores one defect/no-defect judgment or abstention per requirement, item-level confidence, review time and separate perceived-readiness/global-confidence fields. The example 1 to 7 readiness scale is an unvalidated capture convention, not a validated questionnaire. The schema contains no reference key and computes neither engineering readiness nor a treatment effect.

## What the additional feedback can establish

A practitioner reported agent-mediated use and identified template/example schema friction, an omitted population axis and difficulty applying independent-reviewer metrics with overlapping roles. Such feedback informs usability and implementation consistency. It does not establish performance improvement, protocol compliance, adoption or endorsement.

The underlying private artifact, CSVs and execution attachments were not independently examined for this release. Reported findings, numerical results and severity are not treated as verified. Public documentation uses separate constructed examples and omits private names and quotes. A missing disclosure is not automatically critical; deferred scope is not automatically a current defect. See the [finding-recognition rules](../protocol/0.2-preview.3/ARTIFACT-REVIEW.md).

## Decisions still needed before a study

Define one primary estimand and unit of analysis. Detection probability, sensitivity and response criterion are not interchangeable. Include intact requirements to distinguish false alarms from misses. Prespecify handling of abstentions, missing confidence and extreme rates; do not silently transform them into correct responses.

Operationalize complexity using screens, flows, states, interactions, requirements and defect opportunities. Record the actual generative tool/model/version, prompts, seeds where available and post-generation edits. Pilot content, semantic and interaction equivalence: changing visual hierarchy can also change salience. Determine whether clarity is part of the manipulation, a mediator or a confound.

Counterbalance fidelity and order across scenarios. Account for repeated and crossed participant/prototype/item observations when planning analysis and power; do not treat every judgment as an independent participant. The participant target remains provisional until suitable simulation. Prespecify how AI familiarity enters the design. Recruitment, compensation, consent, institutional review and data handling require their own approved procedures.

Restrict conclusions to the bounded task, sampled scenarios and eligible participants with selection limitations. A study of designers' prototype review does not by itself generalize to all software engineers, autonomous agents, business owners or AI oversight. Extending the practice guide to AI-assisted/agentic coding is an application hypothesis to test, not a demonstrated research finding.

## How to find the detail you need

The guide separates broad principles and stable testable criteria from explanations, examples and techniques. Readers can consult the level of detail their task requires. The protocol is an author-defined HCAI engineering-commitment review, not a legal compliance assessment or certification. Accessibility, security, privacy, domain safety and deployment assurance still need their own applicable reviews.
