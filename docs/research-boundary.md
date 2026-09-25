# Research question and practical use

The proposed study examines how visual fidelity affects human review of AI-generated interface prototypes. Requirements, content, behavior and embedded defects are held constant, as is AI authorship. The protocol serves a separate practical purpose: reviewing evidence before a team funds engineering. It is neither the experimental treatment nor evidence that the hypothesized effect exists.

## Definitions and measurement boundaries

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

**In practice**, an owner or advisor uses the six gates, provides references, inspects behavior and records a bounded engineering recommendation. Designers, developers and small-business advisors are intended users. Usability and benefit across those groups remain untested.

**For a study**, the researcher freezes the requirements, intact and defective items, reference key, artifacts, generation/edit history, study version and assignment schedule. Reviewers do not receive the answer key before their judgments are locked. Do not use the guided practice prompts or public worked example as an unplanned experimental intervention: they could change detection and contaminate the comparison.

The optional `study-review` schema stores one defect/no-defect judgment or abstention per requirement, item-level confidence, review time and separate perceived-readiness/global-confidence fields. The example 1 to 7 readiness scale is an unvalidated capture convention, not a validated questionnaire. The schema contains no reference key and computes neither engineering readiness nor a treatment effect.

## Decisions still needed before a study

Define one primary estimand and unit of analysis. Detection probability, sensitivity and response criterion are not interchangeable. Include intact requirements to distinguish false alarms from misses. Prespecify handling of abstentions, missing confidence and extreme rates; do not silently transform them into correct responses.

Operationalize complexity using screens, flows, states, interactions, requirements and defect opportunities. Record the actual generative tool/model/version, prompts, seeds where available and post-generation edits. Pilot content, semantic and interaction equivalence: changing visual hierarchy can also change salience. Determine whether clarity is part of the manipulation, a mediator or a confound.

Counterbalance fidelity and order across scenarios. Account for repeated and crossed participant/prototype/item observations when planning analysis and power; do not treat every judgment as an independent participant. The participant target remains provisional until suitable simulation. Prespecify how AI familiarity enters the design. Recruitment, compensation, consent, institutional review and data handling require their own approved procedures.

Restrict conclusions to the bounded task, sampled scenarios and eligible participants with selection limitations. A study of designers' prototype review does not by itself generalize to all software engineers, autonomous agents, business owners or AI oversight. Extending the practice guide to AI-assisted/agentic coding is an application hypothesis to test, not a demonstrated research finding.

## Why the guide borrows a layered structure

The guide separates broad principles and stable testable criteria from explanations, examples and techniques. Readers can consult the level of detail their task requires. This is a structural analogy to [W3C WCAG 2.0's layers of guidance](https://www.w3.org/TR/WCAG20/#intro-layers-guidance), not an adaptation of its accessibility requirements. There is no W3C affiliation, A/AA/AAA level, legal compliance claim or HCAI certification. Accessibility, security, privacy, domain safety and deployment assurance still need their own applicable reviews.
