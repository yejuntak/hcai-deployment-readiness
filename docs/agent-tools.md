# MCP server and agent skill

Use the published engineering-handoff protocol from an MCP-compatible assistant or a file-based agent skill. **Software 0.1.0** implements the descriptive calculations and workflow of **protocol 0.1-rc.3** ([archived method](https://doi.org/10.5281/zenodo.22667623)). The software is a separate release, not part of the earlier Zenodo archive and not evidence of external validation.

[Project website](https://takyejun.com/research/ai-readiness#agent-tools) · [Source repository](https://github.com/yejuntak/hcai-deployment-readiness) · [Skill](../skills/hcai-readiness/SKILL.md)

## Quick start and when to use

**Before handoff:** install the Skill to prepare the scope, requirements and evidence records. Run this in your project terminal (Node.js required), then choose your agent:

```sh
npx skills add yejuntak/hcai-deployment-readiness --skill hcai-readiness
```

Example: “Use hcai-readiness to prepare a handoff review. Identify missing criteria before judging readiness. Label your own findings as an agent review.”

**After findings are locked and adjudicated:** use MCP to validate counts and calculate results. It does not inspect an interface or validate the truth of submitted evidence. Example: “Use assess_session with these reconciled records, explain each metric and flag missing evidence.” Use summarize_batch for multiple instances with the same criterion and evaluator population.

**Together:** the Skill guides the process; MCP performs deterministic checks and arithmetic. The Skill works without MCP. Neither substitutes for human participant records, the decision owner's review, or production testing.

For a checkout-free MCP connection, install uv and Python 3.11+, then add this to a client supporting mcpServers JSON:

```json
{
  "mcpServers": {
    "hcai-readiness": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/yejuntak/hcai-deployment-readiness.git@agent-tools-v0.1.0", "hcai-readiness-mcp"]
    }
  }
}
```

Reload the client and ask it to call `assessment_template`; expect a checklist and JSON schema. If `uvx` is not found, use its absolute executable path in `command`. Clients with other config formats can use the same stdio command and args. First launch downloads the tagged software and dependencies. For a locked checkout installation, use the steps below.

The shortcut was checked with a fresh project-level Skills CLI installation and actual MCP initialize/template/session/batch calls through uvx using the published tag. The known synthetic case produced 62.5% recall; an all-abstention batch correctly returned N/A for decisive false-ready acceptance. These are installation and software checks, not empirical validation of the Skill's judgment quality.

## Install the MCP server

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/getting-started/installation/). Clone the tagged release, install the locked dependencies, then use its absolute directory in your client configuration:

```sh
git clone --branch agent-tools-v0.1.0 https://github.com/yejuntak/hcai-deployment-readiness.git
cd hcai-deployment-readiness
uv sync --frozen --no-dev
```

For clients accepting the common `mcpServers` JSON format:

```json
{
  "mcpServers": {
    "hcai-readiness": {
      "command": "uv",
      "args": ["run", "--frozen", "--no-dev", "--directory", "/ABSOLUTE/PATH/hcai-deployment-readiness", "hcai-readiness-mcp"]
    }
  }
}
```

Replace the absolute path. Some clients use a different settings format; use their local stdio server option with the same command and arguments. Start the command through your MCP client; a terminal alone waits for protocol messages. Installation downloads dependencies. The running server performs no network calls, file writes or telemetry. Inputs and outputs are visible to the host assistant, so use a host appropriate for your data.

The implementation uses the official MCP Python SDK's supported 1.x interface, bounded below 2 and pinned in `uv.lock`. It does not require an API key or run an AI model itself.

## Available operations

| Operation | Purpose |
|---|---|
| `assessment_template` | Input JSON schema and preparation checklist; no answer key |
| `assess_session` | Validate supplied adjudicated counts, calculate five descriptive measures and provisional handoff status |
| `summarize_batch` | Criterion-conditioned false-ready/false-hold rates with abstention, decision coverage, missing and unknown counts |
| `hcai://protocol` resource | Full protocol reference, including clearly marked public synthetic training answers |
| `plan_handoff_review` prompt | Prepare a scoped review while separating evaluator and reference roles |

Example request: “Use assessment_template to prepare an engineering-handoff review of this prototype. Record missing criteria first; label your own findings as an agent review.”

After real human findings have been locked and adjudicated: “Use assess_session with these reconciled counts and retain the input records in the report.” `examples/session.json` is an explicitly synthetic arithmetic fixture. It yields 62.5% recall, +17.5 percentage points expected-recall gap, 50% recovery coverage, 33.333333% omission recognition and 70% requirements coverage, with Hold for remediation.

`null` means missing/N/A, not zero. Whole-number counts must reconcile. Expected recall is a percentage from 0 to 100 (the Excel workbook instead uses a fraction). Unknown gate inputs prevent an established pass; documented missing required evidence makes the artifact nonready. Zero applicable recovery scenarios require a reason. Batch records must share a criterion version and evaluator population. Use artifact/evaluator provenance and stratify different populations even if they use the same criterion label.

The server checks arithmetic and structural consistency. It cannot verify the truth of supplied counts, timestamps, reference quality or evidence completeness. Human decisions and source records remain essential. A full repository or the protocol resource exposes the public training answers; use a separate outcome-free packet and context for blinded work. The server is not an access-control boundary for reference materials.

## Install the skill

Download `hcai-readiness-skill-v0.1.0.zip` from the [agent tools release](https://github.com/yejuntak/hcai-deployment-readiness/releases/tag/agent-tools-v0.1.0), or copy `skills/hcai-readiness/` from this repository into your agent's skills directory. Keep the whole folder, including `references/`. For Codex, a standard personal location is `~/.codex/skills/hcai-readiness/`; other hosts have their own locations and discovery rules. Do not overwrite a customized installed skill without comparing it first.

Invoke `hcai-readiness` using your host's skill selector. The skill can guide the workflow without MCP. MCP adds deterministic validation and calculation; it does not turn an agent into a human participant. The skill does not install the server automatically.

## Test and reproduce

```sh
uv sync --frozen
uv run --frozen pytest
```

Tests cover the archived synthetic arithmetic, invalid counts, missing data, zero denominators, abstention, criterion-ready controls, evaluator populations, and an actual stdio MCP handshake/tool/resource/prompt round trip. These are software checks, not empirical validation of the method.

## Version and attribution

Cite the underlying method as Tak, Y. (2026). *Human-Centered AI Deployment Readiness Protocol: Engineering-Handoff Profile* (0.1-rc.3). Zenodo. https://doi.org/10.5281/zenodo.22667623 . Identify software `agent-tools-v0.1.0` separately when reporting calculations. Original software is MIT; protocol and skill text are CC BY 4.0. See [LICENSE](../LICENSE). Development assisted by OpenAI Codex. No NIST endorsement or autonomous production certification is claimed.
