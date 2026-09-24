# Protocol update log

Last updated: September 24, 2026. Current: **0.1-rc.4-candidate.2**. MCP 0.2.0rc2; ai-ready Skill/contract 0.2.0-rc.2.

This is a public record of changes, not a validation claim. Earlier versions remain available. No completed external pilot, adoption, endorsement, or performance improvement is claimed.

## September 24, 2026 — candidate.2: make the review usable and inspectable

The first candidate corrected the decision boundary but still asked too much of the reader: technical records were more developed than the actual guided experience. Its current-state summary did not require a connected step map; tests were linked to artifacts without explicitly recording the revision tested; preparation effort could remain hidden.

### Why rc.4 changed

| Feedback theme | Concrete change | Evidence boundary |
| --- | --- | --- |
| Requirements-first, risk-scaled evaluation | Requirements and acceptance criteria precede tests; risk routes before the quick review; operational deployment remains separate. | Correspondence informed design, not validation. |
| Hillel Glazer: reference material and form/fit/function traceability | Inspectable requirement/artifact/test chains, exact tested revisions, reference material, and expandable details. | Attribution approved; no endorsement implied. |
| SMB current-state and adoption | Connected current-workflow map, six plain questions, one next action, visible stops, and preparation/session time. | The 15-minute target and usability remain untested. |
| Review/correction burden | Gross and net benefit remain separate; nonpositive benefit needs an explicit investment rationale. | Scenario estimates are not measured operating performance. |
| Actual end-user discussion and use | Distinct work/discussion origins; general references do not count; a short voluntary pilot packet captures actual use and comprehension. | Outreach and interest are not pilots. |

Other correspondents' identities and comments remain private. A separate permission-controlled audit maps the original emails to these public themes.

### What is new beyond the first candidate

- A one-page starting guide, role-appropriate entry points, six questions, and seven constructed scenarios.
- Four principles and fourteen stable, inspectable HCAI criteria, each with a check and pass/failure examples.
- Explicit human/agent action boundaries and labels for specified, simulated, and implemented behavior.
- A guided MCP/Skill path, private readable reports, exact-revision traceability, and revision-linked stopped runs.
- A separate reviewer-study record: requirement judgments, confidence and perceived readiness are not engineering gate results.
- Usability fields for first use, confusing questions, difficult evidence, facilitator prompts and understanding of the next action.
- Preserved rc.3 and first-candidate artifacts; no silent replacement or final-release promotion.

The criteria structure takes inspiration from WCAG's principles/criteria/techniques hierarchy. It is not a W3C standard, accessibility certification, or proof of universal usability.

### What still needs evidence

Actual bounded end-user/advisor use, accessible-use testing, observed completion and preparation time, evidence-gathering burden, and whether the decision/next action is understood. Controlled effectiveness and the proposed visual-fidelity experiment require separate designs. A passing software suite cannot answer these questions.

See the [test record](/static/research/ai-readiness/rc4-candidate-2/rc4-test-results.json), [change-to-test manifest](/static/research/ai-readiness/rc4-candidate-2/change-manifest.json), and [release status](/static/research/ai-readiness/rc4-candidate-2/rc4-release-readiness.json).

## September 24, 2026 — first rc.4 candidate

Introduced the current-state gate, six mandatory gates, risk-tier depth, separated review/operating costs, engineering-only decisions, permission-aware feedback, pilot contracts, and synchronized MCP/Skill logic. This was a software-tested candidate, not an empirically validated release.

[Preserved first-candidate package](/static/research/ai-readiness/rc4-candidate/HCAI-v0.1-rc.4-candidate.zip).

## Historical rc.3

Original protocol and earlier tools remain frozen. The [historical DOI](https://doi.org/10.5281/zenodo.22667623) identifies rc.3, not either rc.4 candidate. Research Harness v3 is a separate project.

[Return to the review guide](/research/ai-readiness).
