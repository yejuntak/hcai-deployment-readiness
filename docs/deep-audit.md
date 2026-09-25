# Audit findings and the evidence needed for adoption

September 24, 2026 · Protocol 0.1-rc.4-candidate.5 · Author-defined candidate

## Assessment

This protocol addresses a specific review problem: an AI-built artifact may appear complete before there is enough evidence to justify further engineering. Its proposed contribution is a structured way to examine that evidence. There is not yet evidence that the method improves defect detection, saves money or changes HCAI practice. Editorial improvements and passing software tests do not establish those effects or the standing of a standard.

The audit supports retaining a narrow scope: a bounded engineering decision with evidence that reviewers can inspect. Accessibility, human-AI design, security and risk-management practices still have their own requirements. This recommendation is an audit judgment, not an empirical finding or a determination of novelty.

## Comparison with established guidance

Exa returned 20 search results across four angles: accessibility standards, AI risk governance, human-AI interaction, and software assurance. Duplicate URLs/DOI versions and superseded drafts were not counted as independent support. The primary sources below ground the comparison; this was a targeted comparison, not an exhaustive systematic review.

| Reference | Relevant lesson | Consequence for this candidate |
| --- | --- | --- |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Technology-independent requirements are separated from supporting explanations and techniques. Its status also reflects a consensus process, not only document structure. | Keep stable criterion IDs, a defined scope and clear requirements. Do not borrow W3C status, A/AA/AAA labels, or certification language. |
| [W3C guidance on test rules](https://www.w3.org/WAI/WCAG22/Understanding/understanding-act-rules.html) | A passing partial check does not establish every aspect of a success criterion. | State the automated-check boundary in every result; require human evidence-quality review. |
| [NIST AI RMF 1.0 Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | Risk management involves context, diverse perspectives, and continuing governance across the lifecycle; its functions are not a simple ordered checklist. | Screen affected people and consequences. Keep this narrower engineering decision distinct from lifecycle risk management. |
| [Guidelines for Human-AI Interaction, CHI 2019](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/) | The original work reports multiple evaluation rounds, including practitioner application. Guidance and demonstrated applicability are different accomplishments. | Test whether people can interpret and apply this protocol; do not equate correspondence with comparable evaluation. |
| [NIST SSDF AI community profile, SP 800-218A](https://www.nist.gov/publications/secure-software-development-practices-generative-ai-and-dual-use-foundation-models-ssdf) | The AI-specific profile supplements the SSDF and explicitly defines its scope. | Route security concerns to appropriate engineering review. This profile does not replace secure development or certify generated code. |

The W3C also distinguishes functional conformance checks from usability testing and recommends involving people with disabilities in usability evaluation. The protocol's own reading experience needs that work too. HTML is the primary reading alternative to the untagged PDFs; no WCAG conformance claim is made. [W3C conformance guidance](https://www.w3.org/WAI/WCAG22/Understanding/conformance)

## Problems reproduced in the candidate.3 audit

The findings below concern the candidate.2 implementation and its correction in candidate.3. Candidate.4 edits the explanation while retaining those corrections and the remaining limitations.

| Audit finding in candidate.2 | Candidate.3 correction | What remains human or untested |
| --- | --- | --- |
| Changing an acceptance criterion preserved an old passing validation. | Bind validation to both artifact and requirement/context fingerprints. Missing fingerprints block; mismatches require revision. | A new hash is not a new test. A person must inspect actual execution and test adequacy. |
| A proposed state could name an unrelated destination without affecting the decision. | Require resolvable transitions, entry reachability and possible exit paths. | Transition guards, bounded retries, runtime termination and full exception coverage. |
| An empty action-boundary list could pass. | Require explicit nonempty authority limits, including draft-only/manual cases. | Whether implementation actually enforces those limits. |
| Risk depended entirely on six self-selected labels. | Consequential-context flags set deterministic minimum depth; unknown cannot mean no. | Context answers and risk rationale still require competent judgment. Floors are provisional. |
| Human-centered concerns could be omitted while the owner’s efficiency story remained complete. | Add HCAI-1.4: affected roles, access/use, privacy/security, unequal effects and human agency, linked to requirements. | This is coverage screening, not assurance that every harm is discovered or mitigated. |
| A structural pass could be read as evidence-quality assurance. | Require a recorded human quality review and distinguish rule checks, supplied judgment and unverified authenticity in outputs. | The software cannot authenticate that the reviewer performed the inspection. |
| Routed pilot records could omit skipped gates and the reason for stopping. | Reconcile routing, NOT_EVALUATED gates and all follow-up reasons. | Whether the pilot occurred and what participants actually experienced. |

The first three findings were reproduced as PROCEED_TO_ENGINEERING before correction. Regression tests now exercise these and the added boundaries. The examples remain synthetic; this is evidence about implementation behavior only.

## Burden on participants and facilitators

The intended process gives the participant one question at a time and identifies a next action. The facilitator maintains the detailed evidence record. A shared note can support several checks, so a new document is not required for every field. References, criteria and schemas remain available when needed.

The [conversation worksheet](/static/research/ai-readiness/rc4-candidate-5/WORKSHEET.html) makes this division explicit. It is not a shortcut around evidence. If evidence must be created from scratch, the short session stops and identifies the discovery work. Preparation, session and capture time remain visible.

There is a real tradeoff: stronger evidence requirements may make QUICK-6 less attainable. The <=15-minute target is conditional on an available evidence packet and a low-risk case. Do not advertise an end-to-end 15-minute implementation assessment. A pilot should test whether even this narrower target is useful and realistic. If not, revise the process or the target rather than hiding preparation time.

## Questions for empirical evaluation

The proposed hypothesis is that, for a defined review task, the protocol helps reviewers detect consequential gaps or contradictions and choose a justified next step, without disproportionate burden or unnecessary stops on sound proposals.

Evidence should be gathered in distinct stages:

1. **Bounded formative use.** Observe a consenting external advisor/end user with a real workflow. Record preparation, elapsed time, stops, evidence difficulty, independent explanation of the result and next action. A declined or incomplete session is informative; do not remove it from the denominator. One eligible run is a release prerequisite, not proof of usability or effectiveness.
2. **Reproducibility and disagreement.** Have reviewers independently assess the same versioned packets before seeing one another's results. Include adequate, defective and incomplete cases, not only obvious failures. Retain original judgments and reasons, report gate-level agreement and denominators, then adjudicate disputes with an appropriate independent domain reviewer. Do not call the author's preferred answer ground truth without a defensible reference process.
3. **Comparative effectiveness.** Prespecify a suitable ordinary-review comparator, assignment/order, primary outcome, meaningful effect, burden tradeoff and analysis. Measure consequential omissions, false alarms/unnecessary stops, and appropriateness of the engineering decision as well as satisfaction. Choose sample size from the actual design and uncertainty needs. Keep the proposed visual-fidelity experiment separate unless an approved design explicitly studies this intervention.
4. **Transfer and maintenance.** Replicate in additional workflows, sectors, accessibility needs and reviewer experience levels. Record adaptations and where the method fails. An English-language owner-led pilot does not establish universal usability. Retest implementations whenever normative rules change.

No stage above is reported as completed. No sample sizes, effects, adoption totals or endorsements are invented. Registration, participant protections and institutional requirements must be resolved before a controlled study; this roadmap is not research approval.

## Maintenance and governance

Keep public, versioned requirements and examples; a no-install path; interoperable records; clear licenses; correction procedures; and a visible record of disputed interpretations. Allow domain profiles to add checks without weakening mandatory gates. Distinguish a request, a reported problem, a reproduced defect, software verification, actual use and empirical evidence. Do not turn downloads, email replies or interest into adoption metrics.

Read [claims and governance](claims-and-governance.md), the [update log](https://www.takyejun.com/research/ai-readiness/updates), and the [current verification record](/static/research/ai-readiness/rc4-candidate-5/rc4-test-results.json). These records allow others to inspect the work; they do not establish the protocol as an international standard.
