# Scenarios for reviewing AI-created and AI-enabled work

H.A.R.D. Protocol 0.3 · Public Preview

All examples below are constructed. They illustrate decisions and evidence boundaries, not pilot findings or proven effects.

## 1. A SaaS specification has no code yet

The plan promises a generated report after retrieving account data. It defines the happy path but no timeout, unavailable dependency or user-visible retry state. The reviewer works alone.

**Route:** artifact_review, specification_handoff. Inspect the purpose of immediate generation and compare newly proposed queued work, bounded retry, partial results or manual fallback. Keep those alternatives separate from any documented historical rationale. A missing required recovery behavior is a specification finding; lack of code is not itself a plan defect. Record specified and walkthrough separately, and keep implementation/runtime unassessed. No baseline or ROI is needed to identify this gap. Reviewer-performance metrics are N/A without an eligible independent reference.

## 2. A runtime AI product generates health-related text

An AI component generates text using a separate user-data service. The plan contains no failure behavior when that dependency is unavailable. A reviewer also proposes a critical finding because a disclaimer is absent, and flags a feature labeled as future scope.

**Route:** artifact_review with runtime_ai or both, based on actual authorship. Define intended use, relevant output limits, human recourse, data handling, dependency failure and evidence needed at this stage. Assess the missing required recovery behavior from the source. Treat the disclaimer concern as provisional until its current requirement, failure mechanism and consequence support a severity. A future feature is not a current defect unless a present promise or dependency requires it. This example is independent of any private practitioner's unseen artifact and supplies no clinical or legal compliance judgment.

## 3. An AI-coded payment integration retries a timeout

The screen says the payment failed, but the provider may already have processed the charge. The generated code retries immediately.

**Review:** identify the purpose of retry, the provider's idempotency behavior and the distinction between a failed transaction and a lost response. Compare retry, status lookup and an explicit unresolved state. Cite the actual implementation and execution evidence; do not infer duplicate charges from a screenshot. A supported choice can be retained. Test results must identify the exact revision and context.

## 4. A small SaaS uses a shared database

An assistant proposes replacing it with isolated services. The existing database meets the product's current consistency needs and has tested server-side tenant isolation.

**Review:** compare maintenance burden, scale assumptions, isolation evidence and failure consequences against the product's actual goals. A more complex architecture is not automatically better. Record a new human decision to retain the shared database, its evidence, known limits and the trigger for reconsideration. Do not claim the generated rationale was the original author's reason.

## 5. An owner wants to fund automation without observing current work

The prototype looks complete, but nobody can show volume, labor or rework in the current workflow.

**Engineering result:** INSUFFICIENT_EVIDENCE at G1; ROI indeterminate. Observe real current work before a qualifying funding recommendation. A separate artifact review can still inspect purpose, requirements and recovery while that baseline is gathered. It must not imply the funding gates passed.

## 6. A booking prototype loses entered details on failure

A retained walkthrough shows that payment failure discards the user's details, contrary to the required recovery behavior.

**Engineering result:** REVISE at G3. Define the repair and owner, then validate the exact revised artifact. A complete-looking success screen does not resolve the observed recovery defect.

## 7. An agent changes code after a passing test

The report records a previous digest; the new revision changes authorization.

**Engineering result:** REVISE at G4. Execute the affected checks against the new artifact and requirement/context fingerprints. Recomputing a hash does not renew a test result.

## 8. AI wrote the code but does not run the service

A coding assistant created a conventional internal form. The service uses no runtime AI output.

**Review:** record ai_generated in the artifact-review population and artifact_creation in the engineering scope. Check the service that will run. Runtime AI-output checking may be zero with a basis, while ordinary support, correction and manual work remain. Do not pool this case with a runtime AI system in batch reviewer metrics.

## 9. Gross savings disappear during checking

A fictional workflow saves 15 minutes before oversight. Review takes 8 minutes, correction 5 and escalation/rework 2.

**Engineering review:** retain gross savings of 15 minutes and net savings of zero before recurring service cost. If another learning or nonfinancial reason supports investment, record it explicitly. The calculation neither authorizes spending nor measures actual future performance.

## 10. A researcher tests whether polish changes detection

Participants judge intact and defective requirements, record confidence and lock their judgments before seeing a frozen reference key. Fidelity varies while AI authorship is held constant.

**Route:** a separately designed research study. Do not introduce guided decision-review prompts, alternatives or reference answers as an unplanned intervention. Role and timing eligibility alone does not establish causal evidence; the design, sample, comparison and analysis must support that claim. Perceived readiness remains separate from actual correctness.

Execution versions: protocol 0.3-preview.1 · MCP 0.3.0rc1 · Skill/contract 0.3.0-rc.1.


## 11. AI generated a team-invitation feature that works on the happy path

The implementation has a team-members table, invitation token and accept endpoint. It does not say which record is authoritative before acceptance, whether a revoked invitation can race an accept request, or when a billing seat is consumed.

**Review:** artifact_review with ai_generated population. Decompress the observed schema and endpoint choices. Engineering deepening is warranted because the feature mutates persistent membership and authorization state. Record the relevant truth, ownership, state and time/ordering surfaces. Record the seat-allocation and invitation-validity assumptions separately with consequence-if-false, evidence and revisit triggers. Challenge duplicate acceptance and revoke/accept ordering, and label any assessed challenge with its evidence level. Do not infer a race-condition defect unless the code or execution supports it; an unassessed transition remains an evidence gap.

## 12. AI generated a synchronous report workflow around an external service

The generated code calls an upstream service and returns a complete report. A timeout path immediately retries.

**Review:** identify whether an immediate complete result is actually required. Model the authoritative outcome after a lost response, the dependency contract and repeat-execution behavior. Compare bounded retry, status lookup, queued work, partial result and manual fallback only against the actual purpose. A new queue is not automatically better architecture.

## 13. AI generated tenant filtering in the client

The interface filters visible records by tenant ID. No server-side authorization evidence is supplied.

**Review:** the observed client filter does not establish a cross-tenant data leak by itself. It does create an important authority question. Deepen the truth, ownership, boundary and contract surfaces; inspect the server authorization evidence. If server-side isolation is absent in the exact implementation, record the supported finding and severity based on actual exposure and consequence.

## 14. The team asks AI to generate the entire product after one promising prototype

The prototype covers one normal path but the important persistence and recovery assumptions have not been tested.

**Engineering commitment:** do not convert a visually coherent prototype into permission for a broad frontend/backend build. Define the smallest coherent slice that can test the important assumption through input, validation, state/persistence, failure/recovery and observable outcome as applicable. Bound resources and reopen the decision after that evidence exists.
