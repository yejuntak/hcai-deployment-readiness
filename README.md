# HCAI Engineering-Handoff Profile

Protocol **0.1-rc.4-candidate.2** · MCP **0.2.0rc2** · ai-ready Skill **0.2.0-rc.2** · contract **0.2.0-rc.2**

Decide whether evidence supports a bounded commitment of engineering resources. Begin with the current workflow, end-user need and risk. This candidate does not determine deployment readiness or infer operational performance from documentation.

## Start here

[One-page introduction](protocol/0.1-rc.4-candidate.2/START-HERE.md) · [Scenarios](protocol/0.1-rc.4-candidate.2/SCENARIOS.md) · [14 review criteria](protocol/0.1-rc.4-candidate.2/CRITERIA.md) · [Public update log](https://www.takyejun.com/research/ai-readiness/updates)

The human-review problem: distinguish what looks finished from what has been demonstrated. Four principles organize inspectable criteria; they are not a W3C standard or certification. The related fidelity study and this practical guide have distinct claims; see [research boundaries](docs/research-boundary.md).

- [QUICK-6 advisor profile](protocol/0.1-rc.4-candidate.2/QUICK-6.md): six mandatory gates, a proposed <=15-minute low-risk path, and a visible stop.
- [External pilot packet](Pilot-Kit/rc4-candidate-2-external-packet.md): short, voluntary bounded-use instructions.
- [Complete protocol](protocol/0.1-rc.4-candidate.2/PROTOCOL.md) and [full risk-tiered profile](protocol/0.1-rc.4-candidate.2/FULL-PROFILE.md).
- [Install MCP/Skill and run a local assessment](docs/agent-tools.md).
- [Contracts](schemas/README.md), [change manifest](evidence/change-manifest.json), [public feedback ledger](evidence/feedback-ledger.public.json), [migration](docs/migration-rc3-to-rc4.md).

The gates cover measured baseline; need/requirements; states/recovery; traceability; operational oversight; and risk/evidence for engineering commitment. Outputs are PROCEED_TO_ENGINEERING, REVISE or INSUFFICIENT_EVIDENCE. No combined score. Missing baseline blocks a qualifying decision and leaves ROI indeterminate. Evaluation cost, projected operating oversight and actual operational performance remain separate.

## Candidate status

Practitioner correspondence informed refinement; it is not controlled empirical validation. The time target and risk thresholds are untested assumptions. Actual external pilot records are currently empty. Software tests establish implementation behavior only. Promotion requires current passing regression tests and recorded bounded external use reviewed by the author. The release checker never automatically promotes or publishes.

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
