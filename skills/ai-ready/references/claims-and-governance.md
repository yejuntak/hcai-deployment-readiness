# Reporting results and managing changes

HARD Protocol 0.2 · Public Preview

Exact protocol 0.2-preview.1. Preview rules, not certification.

## Which requirements govern the review?

The full profile's required fields, gate rules, risk/context floors, decision boundaries and version contract define the candidate procedure. The criteria describe the intended human review obligations. Quick guidance, examples, scenarios and test fixtures explain the procedure; an example is not a mandatory solution or a substitute for evidence.

The engine enforces the encoded structural and decision rules. A human reviewer must judge whether the evidence meets each criterion's intent. If code, schema and normative text disagree, record a defect, preserve the disputed run and do not issue a favorable recommendation based on the disagreement. Resolve it in a new version with a regression fixture.

Every profile retains the six mandatory gates. QUICK-6 changes how a low-risk review is conducted; it is not a weaker certification level. No gate can be marked not applicable. Inapplicability is available only for the explicitly scoped impact-screen items, with evidence, owner and rationale. Domain profiles may add requirements; they may not waive mandatory gates or use the base version identity for changed logic.

## Match the claim to the evidence

| Evidence available | Permitted description | Unsupported shortcut |
| --- | --- | --- |
| Regression tests pass | This implementation passes the named synthetic regression suite at these versions. | The protocol is effective or the product is safe. |
| Required gates and supplied human judgments pass | Evidence supports considering this bounded engineering step, subject to separate owner authorization. | Deployment ready, HCAI certified, or compliant with an external standard. |
| One actual permitted external use | One bounded formative use was recorded, with its scope and limitations. | Validated, widely adopted, or endorsed. |
| Comparative study with an appropriate design | Describe the measured outcome, sample, comparator, uncertainty and limitations. | Universal benefit or claims outside the tested population/task. |

A claim record must identify date, exact protocol/MCP/Skill/contract versions, workflow boundaries, requested/required profile, risk and context triggers, gate outcomes including skipped gates, evidence provenance, human-review basis, limitations, and the owner’s separate decision if one was made. Reusing the same artifact does not preserve a claim after scope, requirements, context or relevant evidence changes.

Do not issue a badge or a percentage that compresses evidence completeness, evaluator cost, operating oversight and actual system performance into one result. Do not describe an implementation parity check as independent certification.

## Contribution and correction process

Use the [public issue tracker](https://github.com/yejuntak/hcai-deployment-readiness/issues) for nonconfidential issues. Include the version, criterion/gate, expected versus observed behavior, a minimal synthetic reproduction and the consequence. Never attach private mail, client records, credentials, participant data or proprietary artifacts. For confidential material, agree a restricted channel and retention terms with the maintainer before transferring anything; the issue tracker is not that channel.

The maintainer records the report, whether it reproduces, proposed disposition, affected requirements and tests, and the change manifest entry. Preserve disagreement rather than silently changing the old record. Public credit requires permission; reporting a problem does not imply endorsement or authorship of a fix.

The author currently maintains the project. It has no independent standards body, multi-stakeholder consensus, external audit board or formal accreditation. Broader governance would require participating members, agreed decision rules and a public record of their work.

## Version and release policy

- Published artifacts and their hashes are immutable. Correct them by publishing a new versioned preview with migration notes and linked history.
- A changed required field or decision boundary requires a coordinated protocol, contract, MCP and Skill version advance. An editorial release may also advance these identities to identify the exact distribution, without changing the rules. Existing runs remain old-version evidence; migration cannot create new passes or observed facts.
- Stable criterion IDs remain attached to their meaning. Explain refinements; use a new ID when the obligation is materially new. Removed obligations would be deprecated explicitly rather than silently reassigned.
- Changes need regression tests, implementation parity, link/package checks, permission review and readable documentation. A Public Preview is allowed while actual-use evidence is missing; a finalized release is not. A shorter public version number does not waive this boundary.
- Current passing regressions and at least one genuine, version-matched bounded external use with feedback make a release eligible for author review, not automatic promotion. The author still evaluates unresolved issues and the adequacy of evidence. One pilot does not validate effectiveness or establish a standard.

Licensing remains as stated in the repository: original text CC BY 4.0, engine code MIT, third-party material subject to its own terms. This document does not grant rights to private practitioner correspondence.
