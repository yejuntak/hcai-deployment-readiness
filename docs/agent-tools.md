# H.A.R.D. Protocol: MCP and Skill

H.A.R.D. Protocol 0.2 · Public Preview

Human-centered AI Readiness and Decision Protocol

Exact protocol 0.2-preview.3; MCP 0.2.0rc9; Skill/contract 0.2.0-rc.9. The ArtifactReview versions object requires exact protocol, mcp, skill and contract values. Package names, hcai-readiness commands and the ai-ready invocation remain supported. Use the exact versions returned by the installed tools; old records are not silently migrated.

## Install locally

Use Python 3.11+ and uv from this checkout:

```sh
uv sync --group dev
uv run hcai-readiness-mcp
```

Configure a stdio MCP server, replacing the placeholder with the absolute checkout or extracted distribution path:

```json
{"mcpServers":{"hard-protocol":{"command":"uv","args":["--directory","/ABSOLUTE/PATH/hard-protocol","run","hcai-readiness-mcp"]}}}
```

No package-index publication is assumed. The server checks supplied records; it does not crawl private files, authenticate evidence, send reports or authorize deployment. No model key is required by the deterministic server. Your assistant host may receive the data you choose to supply.

To install the Skill, copy skills/ai-ready to a Skill directory supported by your assistant and install its scripts/requirements.txt into Python 3.11+. The references, schemas and deterministic code are bundled. Without a runtime, the Skill can prepare evidence and must state that deterministic assessment is pending.

## Choose the record that matches the task

| Need | Tools and contract | Boundary |
| --- | --- | --- |
| Inspect a specification, prototype or code at its declared stage | `artifact_review_template`, then `assess_artifact_review` with the ArtifactReview record | No baseline or ROI prerequisite. Stage-bounded evidence result, not engineering permission. |
| Fund a bounded engineering step | `assessment_template` or `new_review_record`, `review_next_step`, then `assess_engineering_commitment` | QUICK6/FULL preserve all six gates and risk rules. |
| Capture a research participant's judgments | `validate_study_review` | Reviewer-side judgments only; no answer key or engineering recommendation. |
| Calculate supplied reference metrics under explicit eligibility | Corrected `assess_legacy_session` and `summarize_legacy_batch` diagnostic tools | Amended implementation of historical measures, not a frozen rc.3 run or current engineering gate pass. |

Use artifact_review mode for a solo/small-team inspection. independent_evaluation is an optional layer requiring reference, timing and role eligibility. Merely selecting that mode does not establish independence. ArtifactReview has no adjudicated reference counts, so its reviewer metrics remain null with the reason adjudicated_reference_counts_not_supplied; use the diagnostic Session only when the eligible counts and reference records actually exist.

The current server exposes fifteen read-only tools. The artifact route is also available through `--artifact-review`; this route currently emits JSON only and cannot combine with engineering guidance or report-format flags:

```sh
uv run hcai-readiness /ABSOLUTE/PATH/artifact-review.json --artifact-review
python skills/ai-ready/scripts/assess.py /ABSOLUTE/PATH/artifact-review.json --artifact-review
```

## Artifact review fields

Retain exact versions, run_id, artifact_version, criterion_version, artifact_kind, stage, mode, evaluator_kind, criteria_timing and artifact_population. Population is ai_generated, runtime_ai, both, neither or unknown; unknown remains an evidence gap. Review stages are specification_handoff, prototype_handoff, implementation_review and runtime_release_review. A release-stage label does not authorize release.

Every current requirement and recovery row has specified, walkthrough, implemented and runtime_tested EvidenceCheck objects. Status is pass, fail, unassessed or not_applicable. Pass/fail needs a source location; not_applicable needs a reason. Current unassessed items remain in the denominator. A required-stage not_applicable cannot count as pass. Deferred/excluded items need a reason and cannot hide a current dependency.

Specification/prototype stage requires specified plus walkthrough evidence. Implementation review adds implemented evidence; runtime review adds execution evidence. The result exposes every level separately. Aggregate diagnostic counts have criterion_scope supplied_aggregate_checks and stage_handoff_eligibility null; satisfying them does not establish stage handoff without choice and four-level records. A plan can be inspected without code, with useful findings even when its walkthrough is incomplete.

ChoiceRecord captures purpose, criteria, observed choice/evidence, historical and newly proposed alternatives, rationale provenance, tradeoffs, verification, human decision and follow-up. Use documented/reported only with historical source evidence. New is a present rationale, not reconstructed private reasoning. Important choices need actual human acceptance or revision evidence; an agent cannot supply human confirmation on its own.

Findings preserve recognition, current applicability, proposed and adjudicated severity, evidence and resolution. Critical needs a supported failure mechanism and consequence. Future work and absent disclaimer text do not automatically establish current critical defects.

## Engineering tools and readable reports

`new_review_record` takes caller-supplied metadata and returns a draft without invented evidence. `review_next_step` presents the next missing question. `get_gate_guide` and `get_review_criterion` explain the existing gates and stable criteria.

```sh
uv run hcai-readiness --new --run-id MY-REVIEW --recorded-at 2026-09-26T12:00:00Z --evaluator-kind human
uv run hcai-readiness examples/rc4/low-risk-quick.json --guide
uv run hcai-readiness examples/rc4/low-risk-quick.json --format html
python skills/ai-ready/scripts/assess.py examples/rc4/low-risk-quick.json --format markdown
```

Replace example metadata with actual metadata. Repository examples are synthetic. These commands print to stdout and do not save automatically. `assessment_report` offers a private Markdown or offline HTML engineering report. It does not load artifact URLs or execute their content.

`get_validation_targets` and CLI --validation-targets compute current artifact and requirement/context fingerprints. They do not execute validation or renew a stale pass. Repeat affected checks after a change and retain the old record.

## Eligibility and population consistency

The diagnostic tools retain the historical metric definitions while correcting role/lock eligibility and population handling in this implementation. A current diagnostic result must identify that amended method/version. Existing archived rc.3 inputs and outputs remain historical evidence; do not relabel them.

Independent metrics require a prospectively frozen reference independent of findings, an evaluator who did not author the artifact or reference, and locks before reference access. Self-adjudicated matches require independent confirmation. Expected-recall gap additionally requires an actual locked expectation; omission recognition requires a frozen omission subset. False-ready acceptance requires an independently established criterion and locked judgment. See the [eligibility table](../protocol/0.2-preview.3/INDEPENDENT-EVALUATION.md).

Batch metrics stratify by criterion version, evaluator kind and artifact_population. Preserve stage, mode and remaining eligibility distinctions before comparing results. Agent or synthetic results cannot be presented as observed independent human results. Unknown is not neither.

## Operations and limits

Use `validate_pilot_run` only for an actual bounded engineering use record with the required evidence. Formative feedback or an artifact-only review is not automatically such a run. Keep role deviations, routing and skipped gates visible. `export_public_feedback` supports privacy-conscious summaries; inspect the result before publication. Do not publish private names, source artifacts or quotations by default.

The software rejects malformed or contradictory records and checks arithmetic, references and encoded rules. A structurally valid file can still contain false or inadequate evidence. Human evidence-quality review and real owner authorization remain separate. Do not combine artifact coverage, evaluator metrics, review burden, projected operating benefit and actual performance into a readiness percentage.

Regenerate bundled copies with scripts/build_candidate_assets.py and test MCP/Skill parity. Tests cover implementation behavior, not empirical effectiveness. See [claims and governance](claims-and-governance.md) and [preview.3 migration](migration-preview-3.md).
