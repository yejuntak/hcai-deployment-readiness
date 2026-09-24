# Candidate contracts

Generated from src/hcai_readiness/contracts.py using Pydantic 2; JSON Schema 2020-12. Records reject unknown fields. Engine semantic checks additionally enforce version identity, reference integrity, count reconciliation, tier/gate logic and pilot consistency.

- assessment.schema.json: five-layer input and exact compatibility versions.
- assessment-result.schema.json: engineering-only result with separate measures.
- pilot-run.schema.json: actual or explicitly synthetic use, embedding full assessment/provenance.
- feedback-entry.schema.json: internal permission-aware feedback. Public export is a smaller allowlisted projection.
- change-manifest.schema.json: observed problems, sources, requirements/files and acceptance test IDs.

Durations use minutes; baseline/oversight are per case; recurring costs and volume share the baseline period; money uses one currency. Numbers are finite/nonnegative except computed net effects. Booleans/numeric strings are not measurements. Unknown is null; assessed none is zero/empty. Baseline labor includes disjoint review/escalation/rework. Evaluator/participant/adjudication minutes are disjoint person-time; elapsed is wall-clock.

Pilot-Kit/rc4-pilot-runs.json remains empty until actual use. examples/rc4/pilot-synthetic.json tests format only. Never relabel it actual. Exact compatibility versions are mandatory even when only one execution surface was used.
