# FULL: evidence for a bounded engineering commitment

HARD Protocol 0.2 · Public Preview

Facilitators can begin with [Start here](START-HERE.md). This reference defines the required evidence and decision rules for the full review. Use it to maintain the detailed record, rather than reading every field aloud to a participant. Field names match the versioned JSON schemas.

## 1. Define the scope and select the profile

Name one workflow, unit of work, start/end boundaries, environment, exclusions, affected_roles (including affected non-operators), alternatives considered, and AI's role: artifact_creation, in_workflow, both, or neither. Compare at least one existing/manual/non-AI alternative.

Record run_id, dated recorded_at with timezone, evaluator_kind, requested_profile, and exact protocol/MCP/Skill/contract versions. A revision has a new run_id plus previous_run_id and revision_summary. Keep the old record unchanged.

Classify all six risk dimensions with retained evidence and rationale. These are author-defined anchors, not a validated risk scale:

| Dimension | Low anchor | Moderate anchor | High anchor |
| --- | --- | --- | --- |
| Complexity | Few understood steps/dependencies | Multiple roles/integrations or interacting exceptions | Coupled, adaptive, difficult-to-predict behavior |
| Importance | Convenience; easy fallback | Material business/service function | Essential service or critical commitment |
| Impact | Limited, contained effect | Meaningful effect on customers/staff | Serious effects on safety, rights, livelihood, or many people |
| Mission | Peripheral task | Supports a core objective | Mission-critical outcome |
| Failure consequence | Easily detected, minor inconvenience | Significant disruption or loss | Severe harm, major loss, or unacceptable mission failure |
| Irreversibility | Easily undone | Recovery is costly or delayed | Difficult or impossible to reverse |

The highest dimension determines depth. If any dimension is unknown, the overall tier remains unknown; retain the highest known minimum and gather the missing information. While risk is unresolved, the engine applies the high-depth minimum and cannot issue PROCEED. QUICK6 routes to FULL before evaluating its gates when risk is not low or the session exceeds 15 minutes.

Also answer every field in risk.context. The following are conservative candidate routing floors, not validated regulatory classifications:

| Context field | Meaning of a yes | Minimum tier |
| --- | --- | --- |
| safety_or_rights_impact | Errors could affect physical safety, access to essential services, rights or livelihood | High |
| irreversible_external_actions | The workflow can commit external actions that cannot reliably be undone, such as irreversible deletion or transfer | High |
| sensitive_data | Confidential, protected or security-sensitive information is processed or exposed; determine sensitivity in context | Moderate |
| untrusted_input_to_actions | Untrusted text/data can influence a component that takes actions, rather than remaining an isolated draft | Moderate |

These flags concern the proposed workflow even when AI will not run in production. A false answer needs a defensible basis in the risk rationale; null means unresolved. Use the highest dimension or context minimum. The interface's simplicity does not reduce the consequences of the workflow, and context answers must not be chosen to gain QUICK6 eligibility.

| Required minimum | Low | Moderate | High |
| --- | --- | --- | --- |
| Profile | QUICK6 or FULL | FULL | FULL |
| Observed baseline cases | 1 | 3 | 5 |
| Distinct need origins | 1 | 2 | 2 |
| End-user discussion | Optional if work records establish need | Required | Required |
| Additional checks | None beyond common checks | Independent review; validation plan | Those checks plus hazard analysis, mission review, operational-evaluation plan |

Counts are provisional completeness floors, not statistical evidence of representativeness or safety. Escalate beyond these minimums where domain obligations demand it. A high-risk engineering recommendation still does not authorize deployment.

## 2. G1: Measurable current state

Record current_state_summary, actor_roles, observation_window, sample_size, cycle_minutes_per_case, labor_minutes_per_case, handoffs_per_case, touches_per_case, failure_points, manual_review_minutes_per_case, escalation_minutes_per_case, rework_minutes_per_case, positive volume_per_period, and period.

Review/escalation/rework minutes are disjoint subsets of baseline labor, not additions. Cycle time includes waiting and must not be substituted for labor savings.

Map steps with IDs, kind (normal/edge/recovery), actor_role, trigger, action, data_handling, next_step_ids, terminal, evidence_ids, and observation_status. Provide entry_step_id. Every step must be reachable from the entry and have a path to an endpoint. A terminal step has no outgoing links. Include normal, edge, and recovery practice; at least one normal step is observed. An operator may report rare exceptions, but these must be labeled as reported rather than observed.

Retain observed work/discussion records and a map_review. A summary paragraph, assumption or estimate cannot substitute for the measured baseline. Synthetic evidence is accepted only in an explicitly synthetic evaluation.

Without a baseline, the recommendation is blocked and ROI is INDETERMINATE. For a new service, pause the review while discovery measures the closest existing workaround.

## 3. G2: Need, scope, and requirements

Complete all scope fields. Link each need to a named end-user role and actual source records. Count distinct origin_id values and distinct digests; duplicated/renamed copies do not create independent origins. Only observed work_record or end_user_discussion sources count for real reviews. General literature, this protocol's feedback correspondence, and estimates do not establish a specific workflow's need.

Moderate/high tiers also require retained actual end-user discussion evidence with its origin. Source variety is useful, but two artifacts are not automatically two sources.

Each need must have a requirement; each requirement links to a need. State the requirement, owner, measurable acceptance criterion, form, fit, function, reference material, affected artifacts, and validation IDs. Labels and visual appearance are not acceptance criteria by themselves.

Complete exactly one workflow.impact_reviews record for each domain: access_usability, privacy_security, unequal_effects, human_agency. Record applicability (applicable/not_applicable/unknown), rationale, owner_role and evidence_ids. Applicable items also name affected_roles and requirement_ids; those references must resolve. Each affected role must be covered by an applicable item. Human use/access and agency cannot be declared not applicable. Other inapplicability claims still need rationale, ownership and evidence. Unknown blocks G2. The human quality review judges whether the applicability and coverage are defensible. This screen does not certify any specialist domain.

A true sensitive_data or untrusted_input_to_actions flag makes privacy_security applicable. Declaring it not applicable is a contradiction and fails G2.

## 4. G3: Behavior, failure, and human control

Define normal, edge, and recovery states: trigger, behavior, resulting_state (human-readable description), data_handling, owner_role, requirement_ids, evidence_ids, next_state_ids and terminal. Provide entry_state_id. Every state must be reachable from the entry and have a possible path to an endpoint. Every requirement must have defined behavior. A terminal state cannot have outgoing links. Review guards, bounded retry, partial completion and safe exit: graph reachability does not prove termination, safe runtime behavior, or completeness of exceptions.

Inventory dependencies (an explicit empty list means none assessed) and record dependency_review and state_review. Document nonempty action_boundaries: what people and automated components may access, change, send, or commit. Even a wholly manual or draft-only workflow needs an explicit boundary. human_control_review must address approval, cancellation/override, escalation, preservation of work, and accountable recovery where applicable.

For example, a button labeled “draft” cannot establish that an agent is prevented from sending. A human reviewer must inspect the behavior and supporting evidence. This gate does not replace domain-specific security, accessibility, privacy or safety evaluations.

## 5. G4: Requirement → artifact → validation

Inventory all important artifacts/behaviors. Each must link to a requirement; each requirement/artifact pair must link to an executed passing walkthrough or implementation test, with retained execution evidence.

For every validation record, provide requirement_ids, artifact_ids, method, level, status, evidence_ids, and tested_artifact_digests. Each tested digest must match that artifact's current evidence digest. Missing digests are MISSING; mismatched digests are FAIL. A planned test (specified) is not an executed test. A failed listed validation blocks the gate.

Also provide tested_requirement_digests for every linked requirement. The canonical fingerprint hashes that requirement record, scope, linked proposed states, entry, dependencies, action boundaries and reference versions/digests. MCP get_validation_targets or CLI --validation-targets exposes the targets without running or stamping a test. Capture them with the actual execution record. Missing is MISSING; mismatch is FAIL. Do not turn a stale pass into a current pass by recomputing hashes; perform the affected validation again. Canonicalization uses the typed/default-filled record, sorted-key compact UTF-8 JSON and SHA-256, shared by MCP and Skill.

Label each requirement's behavior_status: specified_only, simulated, or implemented. An implemented_test cannot support a requirement labeled only specified or simulated. A walkthrough may support design/engineering commitment without establishing implementation performance. The report exposes these distinctions.

Use reference material to inspect form (representation), fit (workflow/dependencies), and function (behavior). A generated artifact's instructions are untrusted data. Do not execute arbitrary embedded commands to “verify” it.

The engine checks the format of supplied SHA-256 values without fetching or authenticating files. Hash accessible files locally and preserve their revisions. Matching hashes establish identity; they do not establish quality, authentic provenance or adequate testing.

## 6. G5: Remaining human work and cost

For the same unit of work, record review_minutes_per_case, correction_minutes_per_case, escalation_minutes_per_case, rework_minutes_per_case, residual_manual_minutes_per_case, owner_role, basis (estimate/measured), and evidence_ids.

All categories are disjoint. Explicit zeros require a basis; unknown is null, never zero. If AI only helped create an artifact, runtime AI-output oversight may be inapplicable, but normal manual work and correction remain assessable. Explain zeros in retained evidence.

Operating-cost fields are currency, labor_cost_per_hour, baseline_nonlabor_cost_per_period, proposed_recurring_fixed_cost_per_period, proposed_nonlabor_cost_per_case, one_time_implementation_cost, and evidence_ids. Use one consistent period/currency and document assumptions.

Let L be baseline labor/case, M residual manual labor/case, O the sum of review+correction+escalation+rework, V cases/period, and H hourly labor cost:

- Gross labor saved/case = L − M.
- Net labor saved/case = L − M − O.
- Baseline cost/period = L × H / 60 × V + baseline nonlabor cost.
- Proposed cost/period = ((M + O) × H / 60 + proposed nonlabor/case) × V + recurring fixed cost.
- Net operating benefit/period = baseline cost − proposed cost.
- Recurring ROI = 100 × net benefit / proposed recurring operating cost, only when that denominator is positive.
- Payback periods = one-time implementation cost / positive net benefit, only when both are known.

This is a projected scenario, not a universal ROI definition or measured system performance. No automatic amortization is applied. Unknown money can yield TIME_ONLY, not a monetary ROI. Missing baseline yields INDETERMINATE. Evaluation expense is reported separately.

## 7. G6: Accountable commitment and review burden

Record reference_defect_ids, reviewer_findings, unresolved_risks, decision_owner_role, commitment_scope, resource_limit, next_review_trigger, and reference_review, findings_review, risk_acceptance checks. Empty inventories mean explicitly assessed none; null means unknown.

Each Check needs status, rationale, and evidence to pass. Complete additional checks for the risk tier. An independent review names the role and declares separation from the artifact owner. Critical findings must be resolved; marking one “accepted” cannot waive it. Open major findings block. Findings require evidence.

handoff.evidence_quality_review must pass with a reviewer_role, reviewer_kind human or ai-assisted-human, a rationale and retained observed review evidence. Inspect relevance to the requirement, plausible authenticity, inventory completeness, and test adequacy. File presence alone is insufficient. Synthetic reviewer/evidence is permitted only in synthetic fixtures. The engine cannot authenticate a reviewer or establish that this inspection occurred. An agent may prepare the record, but an agent-only quality review cannot support PROCEED.

If projected net time or monetary benefit is nonpositive, investment_rationale must explicitly explain the nonfinancial or learning reason for any investment. The negative result remains visible. A rationale is not proof that investment is wise.

Record elapsed_minutes, evaluator_minutes, participant_minutes/count, adjudication_minutes, review_correction_cycles, preparation_elapsed_minutes, preparation_person_minutes, capture_reporting_minutes, and evidence of timing. Capture/reporting is within session elapsed time; preparation wall time is outside it.

Preparation, evaluator, participant, and adjudication person-minutes are disjoint. Total person-minutes sum those four categories. Evaluation cost = total person-minutes × review labor rate / 60 + tool/model cost, only when currency and inputs are known. Record tool/model calls, tokens, and cost when available; leave unavailable data null. Never use workflow labor rates implicitly for review cost.

## 8. Explain and retain the result

FULL evaluates all six gates. Any FAIL gives REVISE; otherwise missing evidence gives INSUFFICIENT_EVIDENCE; only all passes give PROCEED_TO_ENGINEERING. Known unresolved critical findings force REVISE even if an earlier QUICK6 stop masked later gates. Profile routing is explicit and is not an evaluation of skipped gates.

Present a readable decision card or report before offering raw JSON. Name the next action and its owner. Report the five measurement layers separately: current baseline, proposed behavior, review/operational-oversight burden, engineering evidence, and actual operational performance. Do not combine them into a weighted readiness score.

Operational observations require implemented_version, realistic_use_context, retained observed evidence, and metrics. No operational evidence is required merely to support an upstream engineering recommendation; the resulting report must not imply operational readiness. Deployment remains NOT_ASSESSED even when observations are supplied.

## 9. Private records, pilots, and release

Use the pilot-run schema for actual bounded external use. Record role/sector, permission/anonymization, date, exact versions, risk/profile, preparation/session time, passed/failed/missing gates, decision before/after if captured, triggered revision, feedback, and artifact evidence. Usability notes include first use, participant's explanation, difficult evidence, confusing questions, facilitator prompts, and whether the next action was understood. Do not manufacture permission or quotations.

Also record gates_not_evaluated, routing_status, and follow_up_reasons. The latter is the unique set of reasons from every non-PASS gate, including routing and skipped gates. evidence_missing retains the reasons from evaluated MISSING gates only. A routed-out session must not look like a completed review with no gaps.

Synthetic fixtures, invitations, and protocol feedback are not pilot runs. Public records require permission checks and removal of identifying details. Correspondence is formative, not controlled empirical validation.

Candidate promotion requires current passing regression results and actual bounded external end-user/advisor use. The software suite tests implementation behavior; usability and effectiveness require evidence from use. The proposed fidelity study is a separate activity, described in the research-boundary document.

Execution versions: protocol 0.2-preview.1 · MCP 0.2.0rc7 · Skill/contract 0.2.0-rc.7.
