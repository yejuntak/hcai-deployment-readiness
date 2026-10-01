# Migration: H.A.R.D. 0.2-preview.3 to 0.3-preview.2

H.A.R.D. Protocol 0.3 · Public Preview

Exact current versions: protocol 0.3-preview.2; MCP 0.3.0rc2; Skill/contract 0.3.0-rc.2.

## Why this is a 0.3 preview

Preview.3 already inspected purpose, alternatives, rationale provenance, tradeoffs, four evidence stages and human disposition. 0.3 changes the machine-readable meaning of a consequential choice by requiring explicit engineering-deepening triage and by adding structured system-model and challenge records. That is a contract change, not an editorial revision.

The six engineering gates and fifteen criterion IDs are retained. Published 0.2 files and runs remain frozen and must not be relabeled.

## ChoiceRecord changes

Every current ChoiceRecord now requires:

- `assumptions`,
- `engineering_deepening_required`,
- `deepening_rationale`.

When engineering deepening is true, it also requires:

- at least one `deepening_trigger`,
- explicit `required_surface_kinds`,
- matching `decision_surfaces`,
- at least one `challenge_scenario`,
- `next_coherent_slice`.

Decision surfaces may be truth, ownership, state, boundary, contract, failure_recovery or time_ordering. Their status is supported, conflicted, unassessed or not_applicable with the evidence rules in the schema. Consequential assumptions are separate first-class records with supported, conflicted or unassessed status plus consequence-if-false, evidence-needed, retained evidence and revisit-trigger fields.

A historical rationale is still different from a new current justification. The new fields do not permit reconstruction of private model chain-of-thought or unrecorded creator intent.

## Gate mapping

- G2 now requires the choice's assumptions and explicit deepening rationale.
- G3 evaluates required decision surfaces when deepening applies. Missing/unassessed surfaces are missing evidence; conflicted surfaces are failures.
- G4 evaluates bounded challenge scenarios and exact decision-context fingerprints. A changed decision surface invalidates affected prior validation.
- G6 retains human disposition and the bounded engineering commitment. For software work, the next step should be the smallest coherent slice that exposes the important assumption where applicable.

## CSV transport 2.1.0

`choice-review.csv` adds:

- engineering_deepening_required_yes_no
- deepening_rationale
- deepening_triggers
- required_surface_kinds
- next_coherent_slice

Two canonical files are added:

- `assumptions.csv`, one row per consequential assumption lifecycle
- `decision-surfaces.csv`
- `challenge-scenarios.csv`, with explicit `evidence_level` for every assessed challenge

Templates and completed examples must use the exact same headers. The verifier does not infer missing rows from prose.

## Migration rule

Do not mutate an old 0.2 review into a 0.3 pass. Preserve the old record and create a linked new review. Carry forward only evidence that still refers to the same artifact and decision context; reassess applicability and rerun affected checks when the new decision model changes the context fingerprint.

## Compatibility

Existing command names, MCP tool names and the `ai-ready` invocation remain supported. Exact version matching is still mandatory. Old 0.2 records fail current schema validation by design and remain valid only as records of the version that created them.

## Claim boundary

This migration supplies software-tested structure for reasoning-decompression records. It does not establish that decision compression occurs at a measured rate, that H.A.R.D. reproduces expert cognition, or that the new lens improves software outcomes.

Execution versions: protocol 0.3-preview.2 · MCP 0.3.0rc2 · Skill/contract 0.3.0-rc.2.
