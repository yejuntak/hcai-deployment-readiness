# Optional independent evaluation

H.A.R.D. Protocol 0.3 · Public Preview

The `independent_evaluation` layer measures reviewer judgments against an independently prepared reference under declared conditions. It is optional. A team can complete an artifact review and act on supported findings without collecting any reviewer-performance metric.

A metric is eligible only when its reference, timing, role and population conditions are satisfied. Disclosure does not restore independence. A warning must not be followed by presenting the affected number as a valid independent-performance result.

## Roles and order

The artifact owner supplies the revision and requirements. A reference author prepares a frozen criterion and defect/omission set. An evaluator reviews without access to that answer key and locks judgments before reference access. An adjudicator matches findings and resolves disputes. A decision owner acts on the resulting evidence.

Record identities privately or stable role IDs, all overlaps, timing, reference access, criterion version, artifact population and evaluator kind. State when a role was absent. A single person cannot be made independent by assigning several role names.

The reference author and adjudicator may be the same person if the reference was frozen before evaluator access, matches follow prespecified rules and disputed items receive a documented independent resolution before entering a claimed metric. Reference preparation is not itself independent evidence that the key is correct. A team needing a stronger inference may require additional separation and key-quality checks.

## Metric eligibility

| Measure or claim | Minimum eligible conditions | Overlap or deviation and required treatment |
| --- | --- | --- |
| Artifact requirements coverage | Declared current inventory, exact revision, source-cited independent evidence columns and reconciled counts | Artifact owner may also review. Report self-review or agent provenance. No independent-performance claim. |
| Artifact recovery coverage | Declared applicable scenarios, evidence level or specified-plus-walkthrough definition, counted unassessed items | Role overlap does not itself invalidate descriptive coverage. Missing inventory or denominator makes the measure N/A. |
| Unresolved critical findings | Supported applicability, severity basis and disposition at the declared stage | Role overlap is disclosed. A proposed or disputed severity remains identified as such; it is not converted into independent confirmation. |
| Reference-set defect recall | Frozen eligible defect set, evaluator independent of artifact creation and key preparation, judgments locked before key access, valid finding matches | Evaluator equals artifact author or reference author: N/A for independent recall. Evaluator also adjudicates: N/A unless finding matches receive independent confirmation. Missing lock, prior key access or unresolved disputed matches: N/A until eligible prospective data exist. |
| Expected-recall gap | Eligible reference recall plus a genuinely recorded expected percentage before the review/reference reveal | If recall is ineligible or expectation was reconstructed afterward: N/A with that reason. A confidence rating is not an expected-recall estimate. |
| Requirement-omission recognition | Frozen predefined omission set, independently locked evaluator findings, valid matches and a positive eligible denominator | Same evaluator/reference/author/adjudicator overlap limits as recall. New omissions are reported separately rather than added to the frozen denominator. |
| False-ready acceptance | Independent locked readiness judgments, independently established criterion status, a prespecified common criterion and eligible population | Shared evaluator/key or artifact-author role, reference leakage, missing lock, mixed criteria/populations or unresolved eligibility blocks the independent rate. Preserve raw judgments as descriptive records. |
| Measured operating performance | Exact implemented version, realistic-use context, observed retained execution evidence and relevant metrics | A specification, walkthrough, criterion pass or evaluator metric cannot substitute. |

A human who uses an agent is not automatically an independent human evaluator. Record what the agent saw, whether it had reference access, and who made and locked the judgment. Agent-only observations form an agent population. They may be examined separately under a declared agent protocol; they do not supply independent human-performance claims.

When machine support is stricter than a narrowly qualified design in this guide, retain N/A for the supported implementation. Do not manually override eligibility to obtain a number. A future expanded analysis requires an explicit versioned method, not a hidden exception.

## Denominators and interpretation

Reference recall is unique correctly matched frozen reference defects divided by eligible reference defects. Requirement-omission recognition uses the predefined eligible omission subset. Novel genuine findings can change the artifact disposition but do not silently change either frozen denominator. Preserve unsupported, duplicate and unresolved findings and the effort spent adjudicating them.

Expected-recall gap is expected recall percentage minus observed reference recall percentage, in percentage points. It is a descriptive signed discrepancy, not a validated general measure of metacognition or probability calibration. Report per-review values; opposite gaps can cancel in an average.

False-ready acceptance conditions on criterion-nonready instances: Ready judgments divided by observed judgments for those instances. An observed abstention stays in the denominator and is also reported. Missing judgments and unknown criterion status are counted separately. It is not the fraction of all Ready judgments that were wrong.

Unknown or zero eligible denominators produce N/A with a reason. A missing metric is not zero. Keep the raw counts and eligibility reasons available. Minimum artifact review does not require these metrics to complete.

## Separate populations before aggregation

At minimum, stratify by exact criterion version, evaluator kind and `artifact_population`. `ai_generated`, `runtime_ai`, `both` and `neither` cannot be pooled as though they were interchangeable. `unknown` cannot be silently combined with a known population. Preserve stage, review mode, eligibility and deviations; do not compare specification handoff with runtime evidence without an explicit justified analysis.

Different artifacts judged by one evaluator and repeated judgments on one artifact are not independent samples. A descriptive batch calculation does not supply an inferential analysis or an effectiveness claim. Performance comparisons require an appropriate study design and uncertainty analysis.

## What the formative feedback supports

A practitioner reported trying the materials through an agent, with role overlap, no blinded participants, no prospectively frozen criterion and no comparison condition. This supports identifying possible use barriers and consistency defects in the materials. It does not establish detection improvement or protocol effectiveness. The private source artifact, judgments and execution attachments were not independently examined in this release, so their reported findings and calculations are not verified here.

The proposed visual-fidelity study is a separate research activity. Keep its locked reviewer record and reference key separate, and do not introduce this guided practice procedure without an explicit study design. See [research boundaries](../../docs/research-boundary.md).

Execution versions: protocol 0.3-preview.2 · MCP 0.3.0rc2 · Skill/contract 0.3.0-rc.2.


## Keep deepening separate from controlled comparisons

Engineering-reasoning prompts, decision-surface maps and challenge scenarios are review interventions. Do not introduce them into a controlled fidelity or reviewer-performance session unless the approved study design includes them. A richer practice review and an unbiased measurement session can require different procedures.
