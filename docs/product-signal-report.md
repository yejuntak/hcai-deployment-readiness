# H.A.R.D. Readiness Report: Product Signal Grade

Status: experimental reporting layer. It is not part of the H.A.R.D. Protocol 0.3 scoring logic and does not change any gate, criterion, evidence stage, decision rule, or claim boundary.

## The first five seconds

A recipient should be able to answer four questions without reading a methodology page:

1. **What is the overall product-surface grade?** Example: `B · 78/100`.
2. **What did H.A.R.D. conclude?** Example: `EVIDENCE NEEDED` or `HOLD`.
3. **What is the single most important thing to fix?**
4. **How much of the result is actually supported by available evidence?**

The shareable headline therefore uses two independent results:

> **B · 78/100 / EVIDENCE NEEDED**

The `78` is the **Product Signal Grade**. `EVIDENCE NEEDED` is the **H.A.R.D. Decision Posture**. They are shown together but never averaged together.

## Why H.A.R.D. is not 60% of the score

H.A.R.D. 0.3 explicitly keeps gate outcomes, evidence coverage, evaluator measures, operating burden, and actual system performance separate. Passing one area cannot cancel a failed gate or unresolved critical finding.

For that reason the report does **not** calculate a "H.A.R.D. score." The numeric grade covers only comparable product-surface signals:

| Product-surface module | Weight |
| --- | ---: |
| Accessibility | 25% |
| Action & Recovery | 25% |
| Privacy & Data Boundary | 20% |
| AI Transparency & Claims | 20% |
| Public Evidence & Documentation | 10% |

H.A.R.D. remains a non-compensatory decision layer beside the grade.

A product can therefore show:

> **A · 92 / HOLD**

That is intentional. It means the observable surface is strong, while an actual H.A.R.D. review found a blocker that the surface score cannot erase.

## Unknown is not failure

A public scan often cannot know whether an internal runbook, test, architecture decision, or human review exists.

The report must say:

> Runtime recovery evidence was not observable in the reviewed material.

It must not silently convert that into:

> The company has no recovery mechanism.

Unknown findings are excluded from the signal-score denominator and reduce **coverage** and **confidence** instead.

The report therefore shows all three:

- **Signal grade**: what the assessed product-surface evidence indicates.
- **Coverage**: how much of the defined report surface was actually assessable.
- **Confidence**: how strong the retained evidence was.

## H.A.R.D. posture

The reporting layer only projects an existing H.A.R.D. result. It does not invent one.

Supported display states are:

- **NOT VERIFIED**: H.A.R.D. was not run.
- **EVIDENCE NEEDED**: the H.A.R.D. result is insufficient evidence.
- **HOLD**: remediation/revision is required.
- **BOUNDED NEXT STEP**: the applicable H.A.R.D. result supports a declared-stage handoff review or considering a bounded engineering step.

The underlying route and exact disposition remain available in the machine-readable result.

## Report hierarchy

The recipient-facing report should stay simple.

### 1. Headline

`B · 78/100 / EVIDENCE NEEDED`

### 2. Plain-language surface verdict

One sentence. No certification language.

### 3. Evidence confidence and coverage

Show both percentages near the headline.

### 4. Fix first

Show one evidence-backed issue and its contribution to the signal score.

### 5. Five module scores

Do not expose the full H.A.R.D. schema here.

### 6. Verify next

Show the highest-value unknowns and exactly what evidence would resolve them.

### 7. H.A.R.D. detail

Only after the simple summary: route, disposition, consequential choices, assumptions, challenge results, evidence stages, owners, and bounded next action.

### 8. Technical appendix

Exact evidence locations, timestamps, scanner versions, criterion IDs, provenance, and applicable specialist-review notes.

## Cheap by design

The grade calculator and HTML/Markdown renderer require:

- no network access,
- no model call,
- no embedding call,
- no external database,
- no generative copy step.

That means once findings and evidence references exist, thousands of reports can be recalculated or re-rendered deterministically with zero model tokens.

### Collector contract for a future public URL scan

The public collector should be equally conservative and inexpensive:

1. Fetch a small bounded surface: homepage, product page, documentation/help entry, privacy page, accessibility statement when present, and one representative product/demo flow.
2. Run deterministic checks first.
3. Retain exact evidence locations and hashes.
4. Mark inaccessible/internal facts unknown.
5. Use an optional model only to turn already-retained findings into concise recipient language or to propose H.A.R.D. questions. A model must never create evidence or silently change status.
6. Reuse unchanged evidence on rescan instead of repeating analysis.

A model is therefore an optional **compression layer**, not the judge.

### Recommended batch limits

These are implementation defaults for a future collector, not H.A.R.D. protocol rules:

- up to 6 public pages per initial organization scan,
- one representative interactive flow when technically accessible,
- deterministic checks before any model use,
- at most the top 5 unknowns in the recipient report,
- at most one optional summary call after findings are frozen,
- incremental rescans keyed to content hash.

This is the path to inexpensive mass outreach without turning the report into an unsupported automated compliance claim.

## Growth signals stay separate

SEO, AEO, search discoverability, and similar commercial visibility signals can be useful in the same report, but they are not product readiness evidence. They appear under **Growth signals** and do not alter the Product Signal Grade or H.A.R.D. posture.

## Claim boundary

The Product Signal Grade is triage. It is not:

- a H.A.R.D. protocol score,
- accessibility conformance certification,
- a privacy/security audit,
- legal compliance,
- deployment authorization,
- measured operational performance,
- proof that H.A.R.D. improves outcomes.

Specialist reviews remain necessary where applicable.

## Machine-readable implementation

Canonical implementation:

- `src/hcai_readiness/grade.py`
- `ReportGradeInput`
- `calculate_report_grade()`
- `render_grade_report()`
- `hard_posture_from_artifact_result()`
- `hard_posture_from_engineering_result()`

Synthetic example:

- `examples/report-grade/synthetic-public-scan.json`

CLI:

```sh
hcai-readiness examples/report-grade/synthetic-public-scan.json --product-signal-grade --format json
hcai-readiness examples/report-grade/synthetic-public-scan.json --product-signal-grade --format html
```

MCP tools:

- `product_signal_grade_template`
- `calculate_product_signal_grade`
- `product_signal_report`

## Definition of Done for v0.1

The reporting layer is ready for bounded external use when all of the following are true:

- a recipient can understand the first screen without reading the protocol;
- the sample displays a letter grade, 0-100 score, H.A.R.D. posture, confidence, coverage, fix-first item, and unknowns;
- H.A.R.D. is absent from the numeric-score weights;
- a H.A.R.D. blocker cannot be averaged away;
- unknowns do not become failures;
- every assessed finding has a retained evidence location;
- every unknown names the evidence required next;
- SEO/AEO and other auxiliary scores cannot change the overall grade;
- the same JSON produces the same result without a model or network;
- HTML escapes supplied content;
- automated tests cover these boundaries;
- the report describes itself as triage, not certification or deployment approval.
