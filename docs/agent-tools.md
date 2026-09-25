# Use the MCP server or ai-ready Skill

Protocol 0.1-rc.4-candidate.5; MCP 0.2.0rc5; Skill/contract 0.2.0-rc.5. The historical DOI and tags identify earlier releases only.

## Install the MCP server

From this candidate checkout, use Python 3.11+ and uv:

```sh
uv sync --group dev
uv run hcai-readiness-mcp
```

Configure a local stdio MCP server using the absolute candidate checkout path. Replace /ABSOLUTE/PATH/readiness-rc4 with your path; it is a placeholder.

```json
{"mcpServers":{"hcai-readiness-candidate":{"command":"uv","args":["--directory","/ABSOLUTE/PATH/readiness-rc4","run","hcai-readiness-mcp"]}}}
```

For an extracted candidate distribution, use its root directory instead. No candidate Git tag or package-index release is assumed. Call assessment_template to verify exact versions/schema/depth. Call assess_engineering_commitment with the assessment object. The tool checks the supplied record against the protocol's rules. It does not crawl files, verify facts, authorize engineering, deploy or send results. No model or model key is used, though your assistant host may receive the data you supply.

## Install the Skill

Copy skills/ai-ready into your assistant's Skill directory. Protocol, profiles, schemas and deterministic Python engine are bundled. Install scripts/requirements.txt in your Python environment (Pydantic 2). The Skill requires Python 3.11+; without a runtime it can prepare evidence but must report assessment pending.

```sh
python skills/ai-ready/scripts/assess.py examples/rc4/low-risk-quick.json
uv run hcai-readiness examples/rc4/low-risk-quick.json
```

These repository-relative examples are synthetic, not pilots. A portable installation uses its own input path.

## Operations and boundaries

- Prepare: Skill collects current-state evidence, classifies risk and walks QUICK6/FULL; it visibly stops at an unmet gate.
- Evaluate: MCP assess_engineering_commitment and the Skill script use byte-identical contracts/engine logic.
- Record use: validate_pilot_run checks versions, gates/decision and evidence references; it does not prove a session occurred.
- Export feedback: export_public_feedback strips private names, comments, dates, context and permission evidence. Review change/file metadata for inadvertent private content before publication.
- Legacy: assess_legacy_session and summarize_legacy_batch retain rc.3 formulas/identity. They cannot establish a candidate pass. Old assess_session/summarize_batch names are replaced to avoid mixing contracts.

Unknown/dangling IDs, malformed digests, inconsistent counts, nonfinite/negative numbers, booleans in numeric fields and version mismatches are rejected. Missing nullable/defaultable evidence produces unmet gates. QUICK6 marks later gates NOT_EVALUATED; FULL reports all gates.

Keep evaluator_burden, operational_oversight, roi, operational_performance, gates and provenance as separate outputs. They must not be combined into a deployment claim or weighted score. Unknown costs/tokens are null. Regenerate and parity-check copies with scripts/build_candidate_assets.py; tests include actual stdio MCP and a separate portable Skill subprocess.

## Run a guided review

Call new_review_record with a caller-supplied ID, timestamp and evaluator provenance. It returns a record with no evidence filled in. Use review_next_step for the next question, responsible role and action. The assistant should show the short question first and retain the returned detail for the facilitator.

get_gate_guide explains one gate. get_review_criterion retrieves a stable HCAI criterion and examples. assessment_report returns private Markdown or offline HTML with expandable requirement/artifact/test chains. Invalid drafts return field paths without echoing sensitive input values.

```sh
uv run hcai-readiness --new --run-id MY-REVIEW --recorded-at 2026-09-24T12:00:00Z --evaluator-kind human
uv run hcai-readiness examples/rc4/low-risk-quick.json --guide
uv run hcai-readiness examples/rc4/low-risk-quick.json --format html
python skills/ai-ready/scripts/assess.py examples/rc4/low-risk-quick.json --format markdown
```

Replace the example ID/time with actual metadata. Commands print to stdout and do not save records automatically. The HTML report is private by default, not a public export. It never loads artifact URLs or executes their content.

hcai://criteria exposes four principles and fifteen candidate criteria. validate_study_review is separate: it validates a locked reviewer-side record without keys, effect calculations or an engineering recommendation. A confidence field is not a validated scale.

get_validation_targets (or CLI --validation-targets) returns current artifact and requirement/context fingerprints for a new check. It does not execute a test, modify a record or verify evidence. Never use it to relabel a stale result; repeat the affected validation first. There are thirteen read-only MCP tools, including legacy diagnostics.

Candidate.5 retains the evidence requirements introduced in candidate.3: connected proposed transitions, affected-person impact screening, context risk flags, explicit authority boundaries and recorded human evidence-quality review. Candidate.4 revised the wording; candidate.5 removes the remaining em dashes and en dashes. The result's assurance object continues to distinguish structural checks, supplied review and unverified authenticity. See [migration](migration-rc3-to-rc4.md) before using old records.

Preserve a stopped QUICK6 record before continuing in FULL with previous_run_id and revision_summary. Preparation time and capture/reporting are explicit, source origins must be distinct, tests must identify the artifact revision tested, and simulated behavior stays labeled.
