# Migrating rc.3 records and tools to rc.4-candidate

The historical baseline is identified in historical/baseline-manifest.json. It contains all 71 files from commit 24ad1e1 plus the original rc.3 release archive and PDF. Existing tags agent-tools-v0.1.0 and skill-v0.1.1 remain unchanged. No rc.3 Git tag existed when inspected; its DOI/archive and hashes supply its provenance. Do not invent a past tag or overwrite a published asset.

Keep root Protocol-v0.1.pdf, Evaluation-Template.xlsx, Source/Protocol-v0.1.md, legacy CSV templates and Worked-Example records as historical rc.3 materials. They have not been upgraded into candidate worksheets. Candidate documents live under protocol/0.1-rc.4-candidate; candidate contracts under schemas; candidate examples under examples/rc4. The historic DOI is not a DOI for the new protocol or software.

| rc.3 concept | Candidate treatment |
| --- | --- |
| Eligible for handoff review / ready criterion | No automatic migration. Reassess all six gates; possible bounded PROCEED_TO_ENGINEERING recommendation. |
| Hold for remediation | REVISE when an evaluated gate documents failure. |
| Insufficient evidence / unknown | INSUFFICIENT_EVIDENCE with explicit missing evidence; malformed input is rejected. |
| Requirement and recovery coverage counts | Preserve as evaluator/artifact diagnostics; add actual requirement/artifact/validation and state records. |
| Elapsed minutes | Retain original value; separately collect disjoint person-minutes, adjudication, calls, tokens and costs. |
| Ready / Not ready / Unable to assess human judgment | Preserve verbatim in legacy records; never reinterpret as deployment approval or copy into the new recommendation field. |
| Missing baseline and operational burden | Leave missing; collect evidence in a new candidate run. Do not backfill invented zeroes. |

MCP 0.2.0rc1 exposes assess_engineering_commitment, assessment_template, validate_pilot_run and export_public_feedback. Historical APIs are explicitly named assess_legacy_session and summarize_legacy_batch; their outputs retain rc.3/software-0.1.0 calculation identity. Update integrations calling the old assess_session or summarize_batch names. Legacy calculations cannot produce candidate gate eligibility.

Use ai-ready Skill 0.2.0-rc.1 with its bundled deterministic engine. Every candidate run must supply exact protocol/MCP/Skill/contract versions even when executed through only one companion, identifying the compatibility set. Do not relabel an old run with the new version. Save original records, gather missing evidence, assign a new run ID and link prior decisions in retained notes.

Unknown operating ROI, unknown tool costs and unavailable post-implementation evidence remain null/not_collected. The model cannot infer them from polished artifacts or complete documentation.

Research Harness discovery: an unrelated quantitative-research capability matrix and a general workflow-system audit were inspected for architectural separation of specs, evidence and decisions. No identifiable Research Harness v3 package was found in the searched NIW assets. No harness logic, claimed tests or results have been imported as protocol evidence.
