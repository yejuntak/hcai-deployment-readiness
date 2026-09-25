# Design system and evaluation protocol

The [Peter Tak Design System](https://github.com/yejuntak/peter-tak-design-system) provides reusable CSS, tokens, component specifications and reference interfaces. This protocol provides a separate procedure for evaluating a frozen artifact against explicit engineering-handoff requirements. The design system is not a validation result for the protocol.

## Candidate checks for an original reference case

| Specification | Required evidence to examine | Current status |
| --- | --- | --- |
| Action trio | Each action has a defined resulting state; adjustment can be completed or cancelled; keyboard order agrees with markup; feedback and recovery are specified. | Mapping prepared; no full protocol assessment completed. |
| Confidence tier | Label meaning, supporting evidence and escalation conditions are explicit. Presentation and model capability are treated separately. | Design choice documented; interpretation and calibration not validated by the component. |
| Shared tokens and styles | Freeze the exact revision and presentation conditions so case comparisons can describe what changed. | Public implementation materials exist; no matched-case study completed. |

The initial protocol scope remains AI-generated prototypes at engineering handoff. Healthcare reference screens do not supply evidence of clinical effectiveness. Runtime AI or clinical evaluation requires additional criteria and expertise.

## Actual documentation review

A maintainer-authorized review with Codex assistance found that the action-trio example's HTML order was set-aside, adjust, accept, while its keyboard description stated the reverse sequence. The documentation was corrected to follow the example's DOM order. The same revision clarifies contrast requirements, the unvalidated status of confidence-presentation choices, and the distinction between interface hooks and implemented runtime behavior.

- [Baseline](https://github.com/yejuntak/peter-tak-design-system/tree/8bba5e4853e9f0a15edbf9201f469fb22fd99de6)
- [Correction and exact diff](https://github.com/yejuntak/peter-tak-design-system/commit/49e1978259b45452889b78d341e2d37d114cd622)

This is a documentation consistency review. It is not independent feedback, a participant study, runtime accessibility testing, or a full protocol evaluation. No defect-recall rate or effectiveness estimate is inferred from it.

## Next evidence to collect

Prepare an original nonclinical case, freeze its requirements and reference key, and have a reviewer who did not build it follow the protocol. Preserve actual findings, judgment, adjudication and remediation records. Obtain any applicable institutional determination before covered participant work. Report the author's relationship to reviewers and distinguish independent use from the author's own application.
