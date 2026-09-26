# H.A.R.D. Protocol 0.2

Human-centered AI Readiness and Decision Protocol  
**Public Preview**

Exact execution versions: protocol **0.2-preview.3** · MCP **0.2.0rc9** · Skill/contract **0.2.0-rc.9**. Existing hcai-readiness commands and the ai-ready invocation remain supported.

AI can deliver a result before people have examined the decisions inside it. H.A.R.D. starts with a plan, prototype or implementation and works backward: what was chosen, what purpose it serves, what alternatives matter, what tradeoffs it creates, what evidence supports it and which human decisions remain. A justified existing choice can be retained. A new explanation is never presented as the creator's unrecorded reasoning.

## Start with the decision you need

| Your task | Route |
| --- | --- |
| Inspect one artifact, including a plan with no code, alone or in a small team | [Minimum artifact review](protocol/0.2-preview.3/ARTIFACT-REVIEW.md). No baseline or ROI prerequisite. |
| Examine choices and missing expert judgment | [Decision review](protocol/0.2-preview.3/DECISION-REVIEW.md) and [worksheet](protocol/0.2-preview.3/WORKSHEET.md). |
| Decide whether to fund bounded engineering work | [QUICK-6](protocol/0.2-preview.3/QUICK-6.md) or [FULL](protocol/0.2-preview.3/FULL-PROFILE.md). All six gates and [fifteen criteria](protocol/0.2-preview.3/CRITERIA.md) remain. |
| Measure reviewer performance | [Optional independent evaluation](protocol/0.2-preview.3/INDEPENDENT-EVALUATION.md). Metric-specific independence, reference and timing rules apply. |

Read [Start here](protocol/0.2-preview.3/START-HERE.md), the [complete protocol](protocol/0.2-preview.3/PROTOCOL.md), [constructed software/SaaS scenarios](protocol/0.2-preview.3/SCENARIOS.md), [MCP/Skill setup](docs/agent-tools.md) or the [external-use packet](Pilot-Kit/hard-0.2-preview-3-external-packet.md).

## What this preview changes

The minimum artifact route is now explicit. It keeps specified, walkthrough, implemented and runtime-tested evidence separate, retains unassessed requirements in denominators, records artifact population and supports choice-level rationale and human disposition. Templates, examples and verification must use the same schema. Optional reviewer metrics state N/A reasons when role, reference or lock conditions are not met.

Targeted deepening lets a reviewer examine an unresolved choice before expanding the review; it is not a new validated scoring profile. Engineering commitment still requires measured current work, actual need, recovery, exact-revision validation, remaining human work and accountable limits. Results remain PROCEED_TO_ENGINEERING, REVISE or INSUFFICIENT_EVIDENCE. A missing baseline blocks a qualifying engineering recommendation and leaves ROI indeterminate, while a limited artifact review can still identify useful gaps.

Public summaries of practitioner feedback describe formative usability and consistency concerns. They do not reproduce private identities or quotes, verify unseen attachments or establish effectiveness. The related visual-fidelity study remains separate. No result certifies a product or approves deployment. See [research boundaries](docs/research-boundary.md), [claims and governance](docs/claims-and-governance.md) and the [update log](docs/updates.md) and [preview.3 migration](docs/migration-preview-3.md).

## Versions and verification

Published version directories and earlier runs remain frozen. Root Templates, Worked-Example and Source/verify_example.py provide the current corrected interoperable record path; historical copies remain under the preserved baseline and previous distributions. Current corrected diagnostic tools must identify their amended implementation instead of claiming byte-identical historical behavior.

[DOI 10.5281/zenodo.22667623](https://doi.org/10.5281/zenodo.22667623) identifies the historical rc.3 release only. It does not identify this preview. The [baseline manifest](historical/baseline-manifest.json) preserves historical artifact identity. Research Harness v3 is separate and supplies no validation evidence here.

The compact current-version ZIP includes the runnable tools, current documents, templates and worked examples. It omits frozen historical releases and Git metadata. Run the full regression and release-building commands below from a repository clone with historical tags; archive-identity checks are not standalone ZIP checks. For a downloaded bundle, use the CSV verification commands in [Source/README.md](Source/README.md).

```sh
git clone https://github.com/yejuntak/hcai-deployment-readiness.git
cd hcai-deployment-readiness
git fetch --tags
uv sync --group dev
uv run python scripts/build_candidate_assets.py --check
uv run pytest -q
uv run python scripts/verify_candidate.py
```

Software tests establish implementation behavior for the tested cases. They do not establish usability, review time, decision improvement or defect prevention. Finalized release consideration still requires current regressions and actual version-matched bounded external use reviewed by the author. This preview is not automatically promoted by the build.

Original method/Skill text and synthetic data: CC BY 4.0, Yejun Tak. Original software: MIT. Development and checks were AI-assisted; author judgment and external validation remain separate.
