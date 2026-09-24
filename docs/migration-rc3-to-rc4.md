# Migrating rc.3 records and tools to rc.4-candidate

## Current editorial release: candidate.4

Protocol 0.1-rc.4-candidate.4, MCP 0.2.0rc4 and Skill/contract 0.2.0-rc.4 revise the writing from candidate.3. Gates, required fields, risk thresholds and calculations are unchanged. The coordinated identity advance records the exact distribution used; it does not imply a new validated method.

For a new review, use the candidate.4 documents and tools together. Retain existing runs with their original versions. If continuing an earlier review, create a new run linked through previous_run_id and explain the revision. Reuse unchanged evidence only when it still describes the reviewed scope and revisions; do not invent a fresh observation or silently relabel an old pass.

Candidate.3 documents and downloads are recorded in historical/candidate-3-manifest.json, with published web assets in historical/candidate-3-site-manifest.json. New downloads use /static/research/ai-readiness/rc4-candidate-4/. The historical migration notes below retain their original version references.

## Historical migration notes

The historical baseline is identified in historical/baseline-manifest.json. It contains all 71 files from commit 24ad1e1 plus the original rc.3 release archive and PDF. Existing tags agent-tools-v0.1.0 and skill-v0.1.1 remain unchanged. No rc.3 Git tag existed when inspected; its DOI/archive and hashes supply its provenance. Do not invent a past tag or overwrite a published asset.

Keep root Protocol-v0.1.pdf, Evaluation-Template.xlsx, Source/Protocol-v0.1.md, legacy CSV templates and Worked-Example records as historical rc.3 materials. They have not been upgraded into candidate worksheets. Candidate documents live under protocol/0.1-rc.4-candidate.3; candidate contracts under schemas; candidate examples under examples/rc4. The historic DOI is not a DOI for the new protocol or software.

| rc.3 concept | Candidate treatment |
| --- | --- |
| Eligible for handoff review / ready criterion | No automatic migration. Reassess all six gates; possible bounded PROCEED_TO_ENGINEERING recommendation. |
| Hold for remediation | REVISE when an evaluated gate documents failure. |
| Insufficient evidence / unknown | INSUFFICIENT_EVIDENCE with explicit missing evidence; malformed input is rejected. |
| Requirement and recovery coverage counts | Preserve as evaluator/artifact diagnostics; add actual requirement/artifact/validation and state records. |
| Elapsed minutes | Retain original value; separately collect disjoint person-minutes, adjudication, calls, tokens and costs. |
| Ready / Not ready / Unable to assess human judgment | Preserve verbatim in legacy records; never reinterpret as deployment approval or copy into the new recommendation field. |
| Missing baseline and operational burden | Leave missing; collect evidence in a new candidate run. Do not backfill invented zeroes. |

MCP 0.2.0rc3 exposes assess_engineering_commitment, assessment_template, validate_pilot_run and export_public_feedback. Historical APIs are explicitly named assess_legacy_session and summarize_legacy_batch; their outputs retain rc.3/software-0.1.0 calculation identity. Update integrations calling the old assess_session or summarize_batch names. Legacy calculations cannot produce candidate gate eligibility.

Use ai-ready Skill 0.2.0-rc.3 with its bundled deterministic engine. Every candidate run must supply exact protocol/MCP/Skill/contract versions even when executed through only one companion, identifying the compatibility set. Do not relabel an old run with the new version. Save original records, gather missing evidence, assign a new run ID and link prior decisions in retained notes.

Unknown operating ROI, unknown tool costs and unavailable post-implementation evidence remain null/not_collected. The model cannot infer them from polished artifacts or complete documentation.

Research Harness discovery: an unrelated quantitative-research capability matrix and a general workflow-system audit were inspected for architectural separation of specs, evidence and decisions. No identifiable Research Harness v3 package was found in the searched NIW assets. No harness logic, claimed tests or results have been imported as protocol evidence.

## From candidate.2 to candidate.3

This is a breaking candidate contract advance: protocol 0.1-rc.4-candidate.3, MCP 0.2.0rc3, Skill/contract 0.2.0-rc.3. Preserve the original record and tool package; a version-string replacement is not a valid migration.

- Add scope.affected_roles and the four workflow.impact_reviews, with applicability, owner, rationale and evidence; connect applicable concerns to requirements.
- Classify risk.context flags. True answers set minimum tiers; missing answers remain unknown and prevent QUICK6.
- Add workflow.entry_state_id and each proposed state's next_state_ids/terminal. Do not invent transitions. Provide a nonempty action-boundary inventory.
- Reperform affected validation and capture tested_requirement_digests alongside tested_artifact_digests. The requirement/context hash covers scope, linked states, reference versions, dependencies and authority. New fingerprints do not authenticate old checks.
- Record handoff.evidence_quality_review, including human reviewer kind/role, rationale and observed review evidence. Do not synthesize a reviewer or a pass during migration.
- Pilot records additionally need gates_not_evaluated, routing_status and follow_up_reasons reconciled to the result. Preserve stopped/routed sessions.
- Use a new run ID linked to the prior run and describe the revision. Earlier passing decisions are not carried forward automatically. New outputs include assurance limits; owner authorization remains separate.

Candidate.2 documents, PDFs, packages and published website assets are hash-frozen. Existing criterion IDs retain their intent; HCAI-1.4 is new. The [audit](deep-audit.md) explains the substantive changes.

## From the first rc.4 candidate to candidate.2

The first candidate (protocol 0.1-rc.4-candidate, MCP 0.2.0rc1, Skill 0.2.0-rc.1) remains byte-frozen in the named artifacts in historical/candidate-1-manifest.json. Its complete ZIP retains all original source and reports. Published downloads remain at /static/research/ai-readiness/rc4-candidate/. New downloads use /rc4-candidate-3/.

Do not merely replace version strings in a run. Retain the original, create a new linked run, and collect:
- Scope boundaries, unit, AI role, exclusions, and alternatives.
- Connected current-state steps and a map review.
- Original need-source IDs and work/discussion source types.
- Specified/simulated/implemented behavior labels, human-control review, and action boundaries.
- The exact artifact digests that each validation tested.
- Preparation wall/person time and capture/reporting time.
- An explicit investment rationale when net benefit is nonpositive.

Early risk routing now marks all QUICK6 gates NOT_EVALUATED for higher/unknown risk. A known critical finding remains visible despite an earlier stop. The result adds routing and attention_items; decision names and the engineering-only boundary remain unchanged.

New read-only MCP tools guide an empty record, retrieve individual criteria, and render private reports. Legacy and first-candidate results are not silently recalculated. Candidate.2 still lacks real external pilot evidence.
