# H.A.R.D. Protocol 0.3

Human-centered AI Readiness and Decision Protocol  
**Public Preview**

Exact execution versions: protocol **0.3-preview.1** · MCP **0.3.0rc1** · Skill/contract **0.3.0-rc.1**. Existing `hcai-readiness` commands and the `ai-ready` invocation remain supported.

AI-assisted creation can compress the distance between an intention and a convincing plan, design or implementation. H.A.R.D. starts with the result and reopens the consequential decisions that may have been compressed inside it. It separates observed choices from invented history, externalizes the relevant system model when engineering deepening is warranted, challenges conditions that could make a choice wrong, and keeps the next human commitment proportional to the evidence.

**Generation must not outrun understanding.** This is a design principle for the review, not a measured claim about AI-assisted development.

## Start with the decision you need

| Your task | Route |
| --- | --- |
| Inspect one artifact, including a plan with no code, alone or in a small team | [Minimum artifact review](protocol/0.3-preview.1/ARTIFACT-REVIEW.md). No baseline or ROI prerequisite. |
| Reopen choices, rationale, assumptions and tradeoffs | [Decision review](protocol/0.3-preview.1/DECISION-REVIEW.md) and [worksheet](protocol/0.3-preview.1/WORKSHEET.md). |
| Deepen a consequential software/code choice | [Engineering reasoning deepening](protocol/0.3-preview.1/ENGINEERING-REASONING.md). This is a targeted lens, not a seventh gate or score. |
| Decide whether to fund bounded engineering work | [QUICK-6](protocol/0.3-preview.1/QUICK-6.md) or [FULL](protocol/0.3-preview.1/FULL-PROFILE.md). All six gates and [fifteen criteria](protocol/0.3-preview.1/CRITERIA.md) remain. |
| Measure reviewer performance | [Optional independent evaluation](protocol/0.3-preview.1/INDEPENDENT-EVALUATION.md). Metric-specific independence, reference and timing rules apply. |

Read [Start here](protocol/0.3-preview.1/START-HERE.md), the [complete protocol](protocol/0.3-preview.1/PROTOCOL.md), [constructed software/SaaS scenarios](protocol/0.3-preview.1/SCENARIOS.md), [MCP/Skill setup](docs/agent-tools.md) or the [external-use packet](Pilot-Kit/hard-0.3-preview-1-external-packet.md).

## What 0.3 changes

0.3 makes the reasoning-recovery mechanism explicit without pretending to reconstruct private chain-of-thought. Every consequential choice now records whether engineering deepening applies and why. When it applies, the machine-readable record can carry decision surfaces for truth, ownership, state, boundary, contract, failure/recovery, time/ordering and assumption, plus bounded challenge scenarios and a smallest coherent next slice.

The six engineering gates and fifteen stable criterion IDs remain. G3 now makes relevant system truth, authority, state and temporal behavior inspectable. G4 requires actual challenge/check evidence and invalidates stale checks when the consequential decision context changes. G6 keeps the next commitment bounded and, for software, favors a coherent end-to-end slice that exposes the important assumption before a broad build.

The four evidence levels remain separate: specified, walkthrough, implemented and runtime tested. A plausible rationale, complete decision-surface record or passing software regression does not imply runtime behavior or empirical protocol effectiveness.

The CSV transport contract advances to 2.0.0 and adds `decision-surfaces.csv` and `challenge-scenarios.csv`. Old records and published packages remain frozen. See [0.2 to 0.3 migration](docs/migration-0.2-to-0.3.md).

## Evidence and claims

Decision compression and "implementation outrunning understanding" are motivating models for this preview. They are not established causal effects. Public practitioner feedback remains formative. The related visual-fidelity study remains separate and must not silently receive engineering-reasoning prompts as an unplanned intervention.

No H.A.R.D. result certifies a product, proves software quality or approves deployment. Artifact coverage, reviewer performance, review effort, projected operating burden and measured operational performance remain separate outputs.

See [research boundaries](docs/research-boundary.md), [claims and governance](docs/claims-and-governance.md) and the [update log](docs/updates.md).

## Versions and verification

Published version directories and earlier runs remain frozen. Root Templates, Worked-Example and `Source/verify_example.py` provide the current interoperable record path. Historical copies remain under preserved baselines and previous distributions.

[DOI 10.5281/zenodo.22667623](https://doi.org/10.5281/zenodo.22667623) identifies the historical rc.3 release only. It does not identify this preview.

Run current checks from a repository clone:

```sh
git clone https://github.com/yejuntak/hcai-deployment-readiness.git
cd hcai-deployment-readiness
git fetch --tags
uv sync --group dev
uv run python scripts/build_candidate_assets.py --check
uv run pytest -q
uv run python scripts/verify_candidate.py
```

Software tests establish implementation behavior for named synthetic cases. They do not establish usability, review time, decision improvement or defect prevention. Finalized release consideration still requires current regressions and actual version-matched bounded external use reviewed by the author.

Original method/Skill text and synthetic data: CC BY 4.0, Yejun Tak. Original software: MIT. Development and checks were AI-assisted; author judgment and external validation remain separate.
