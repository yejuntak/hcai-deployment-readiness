# H.A.R.D. Protocol 0.2

Human-centered AI Readiness and Decision Protocol  
**Public Preview**

Exact execution versions: protocol **0.2-preview.2** · MCP **0.2.0rc8** · Skill/contract **0.2.0-rc.8**. Existing hcai-readiness commands and the ai-ready invocation remain supported.

A polished result can still be unfinished. This protocol helps people inspect the information structure, workflow, technical evidence and human responsibilities underneath an AI-created or AI-enabled artifact. Use six questions to decide whether to invest in building it, revise it, or gather missing evidence. The next step is a bounded engineering commitment, not permission to put a system into use or a measure of its performance.

## Start here

[Starting guide](protocol/0.2-preview.2/START-HERE.md) · [Worksheet](protocol/0.2-preview.2/WORKSHEET.md) · [Scenarios](protocol/0.2-preview.2/SCENARIOS.md) · [15 review criteria](protocol/0.2-preview.2/CRITERIA.md) · [Public update log](https://www.takyejun.com/research/ai-readiness/updates)

This naming revision uses Human-centered AI Readiness and Decision Protocol. The public name H.A.R.D. Protocol 0.2 and separate Public Preview label stay the same. All six prior candidates and the first 0.2 preview remain frozen. Gates, risk thresholds, calculations and evidence requirements are unchanged. Read the [naming migration notes](docs/decision-naming-migration.md) and [editorial review](docs/editorial-review.md). The [deep audit and validation roadmap](docs/deep-audit.md) and [claims/governance rules](docs/claims-and-governance.md) explain what the method still needs to demonstrate.

The review addresses a specific problem: an artifact's finished appearance may exceed the evidence available for its behavior. Four principles organize the criteria for engineering-commitment reviews. The result is a recommendation, not certification. The related fidelity study asks a separate research question; see [research boundaries](docs/research-boundary.md).

- [QUICK-6 advisor profile](protocol/0.2-preview.2/QUICK-6.md): six mandatory gates, a proposed <=15-minute low-risk path, and a visible stop.
- [External pilot packet](Pilot-Kit/hard-0.2-preview-2-external-packet.md): short, voluntary bounded-use instructions.
- [Complete protocol](protocol/0.2-preview.2/PROTOCOL.md) and [full risk-tiered profile](protocol/0.2-preview.2/FULL-PROFILE.md).
- [Install MCP/Skill and run a local assessment](docs/agent-tools.md).
- [Contracts](schemas/README.md), [change manifest](evidence/change-manifest.json), [public feedback ledger](evidence/feedback-ledger.public.json), [migration](docs/migration-rc3-to-rc4.md).

The six gates cover the measured baseline, need and requirements, states and recovery, traceability, operational oversight, and evidence for engineering commitment at the required risk depth. Results are PROCEED_TO_ENGINEERING, REVISE or INSUFFICIENT_EVIDENCE. A missing baseline prevents a qualifying decision and leaves ROI indeterminate. Evaluation cost, projected operating oversight and actual operational performance are reported separately, without a combined score.

## Candidate status

Practitioner correspondence informed the revisions, but is not controlled empirical validation. The time target and risk thresholds remain untested, and no actual external pilot is recorded. Software tests establish behavior only for the implementation cases they cover. Promotion requires current passing regressions and recorded bounded external use reviewed by the author; the release checker cannot promote or publish automatically.

## Frozen history

[Baseline manifest](historical/baseline-manifest.json) hashes the inspected rc.3 repository and original archive. [Frozen artifacts](historical/rc3-baseline/) and historical software tags are preserved. Root PDFs/workbooks, Source/Protocol-v0.1.md, Templates and Worked-Example remain legacy materials, not rc.4 gate implementations. Candidate PDFs live under output/pdf.

[DOI 10.5281/zenodo.22667623](https://doi.org/10.5281/zenodo.22667623) identifies rc.3 only. Research Harness v3 is a separate project and supplies no validation evidence here.

## Verify

```sh
uv sync --group dev
uv run python scripts/build_candidate_assets.py --check
uv run pytest -q
uv run python scripts/verify_candidate.py
```

Verification reports are under Verification/rc4-*.json. Original method/Skill text and synthetic data: CC BY 4.0, Yejun Tak. Original software: MIT. Development and technical checks were AI-assisted; author review and external validation remain separate.
