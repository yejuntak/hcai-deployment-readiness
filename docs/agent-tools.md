# Candidate MCP and ai-ready Skill

Protocol 0.1-rc.4-candidate; MCP 0.2.0rc1; Skill/contract 0.2.0-rc.1. The historical DOI and tags identify earlier releases only.

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

For an extracted candidate distribution, use its root directory instead. No candidate Git tag or package-index release is assumed. Call assessment_template to verify exact versions/schema/depth. Call assess_engineering_commitment with the assessment object. The tool validates supplied evidence; it does not crawl files, verify facts, authorize engineering, deploy or send results. It uses no model or model key. Your assistant host may still receive supplied data.

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

Preserve separate evaluator_burden, operational_oversight, roi, operational_performance, gates and provenance. Never derive deployment claims or weighted scores. Unknown costs/tokens are null. Regenerate and parity-check copies with scripts/build_candidate_assets.py; tests include actual stdio MCP and a separate portable Skill subprocess.
