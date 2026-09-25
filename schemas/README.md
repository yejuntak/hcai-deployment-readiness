# Candidate contracts

These JSON Schema 2020-12 contracts are generated from src/hcai_readiness/contracts.py using Pydantic 2. Records reject unknown fields. The engine also checks version identity, references, reconciled counts, risk tiers, gate rules and consistency between pilot records and assessments.

- assessment.schema.json: five-layer input and exact compatibility versions.
- assessment-result.schema.json: engineering-only result with separate measures.
- pilot-run.schema.json: actual or explicitly synthetic use, embedding full assessment/provenance.
- feedback-entry.schema.json: internal permission-aware feedback. Public export is a smaller allowlisted projection.
- change-manifest.schema.json: observed problems, sources, requirements/files and acceptance test IDs.

Durations use minutes; baseline/oversight are per case; recurring costs and volume share the baseline period; money uses one currency. Input numbers must be finite and nonnegative; computed net effects may be negative. Booleans and numeric strings are not measurements. Use null for unknown values and zero or an empty collection only when none was explicitly assessed. Baseline labor includes disjoint review/escalation/rework. Evaluator/participant/adjudication minutes are disjoint person-time; elapsed is wall-clock.

Pilot-Kit/rc4-pilot-runs.json remains empty until actual use. examples/rc4/pilot-synthetic.json tests format only. Never relabel it actual. Exact compatibility versions are mandatory even when only one execution surface was used.

Candidate.2 introduced scope, connected current-state steps, original evidence origins/types, tested artifact digests, specified/simulated/implemented labels, human-control checks, preparation/capture time, revision links, and pilot usability notes. study-review.schema.json is a separate locked reviewer-side contract, not an engineering recommendation or validated psychometric measure. Preparation person-time is included in evaluation cost; capture/reporting is a subset of the session, not counted twice.

Candidate.3 added requirement/context fingerprints, connected proposed-state transitions, context risk flags, affected-person impact reviews, recorded human evidence-quality review and complete pilot routing records. Candidate.4 edits the documentation and tool guidance without changing these contracts or the decision rules. Its exact compatibility versions identify the new distribution; existing runs retain their original versions.

Candidate.5 removes em dashes and en dashes from current prose and advances the exact distribution identities. Required fields and decision rules remain unchanged.
