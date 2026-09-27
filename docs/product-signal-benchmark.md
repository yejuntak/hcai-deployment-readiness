# Product benchmark: Cracked Resume -> H.A.R.D. Readiness Report

This note benchmarks Cracked Resume at the level of product strategy, interaction compression, report behavior, and visual grammar. The H.A.R.D. acquisition experience should feel deliberately close in composition and visual family: atmospheric sky, a single floating product specimen, oversized editorial serif question, one white primary action surface, extreme whitespace, and minimal navigation. Do not reuse Cracked Resume's exact copy, logos, sky asset, or source code; reproduce the visual logic with original assets and implementation.

Sources reviewed:
- https://crackedresume.com/
- https://peerlist.io/felix/project/cracked-resumeai-faang-resume-reviewer
- https://www.linkedin.com/posts/felixleezd_i-exposed-faangs-elitist-hiring-practice-activity-7349084486896111617-3M0E


## Aggressive visual benchmark

Treat the visual benchmark as near-clone in **grammar**, not in brand assets.

The first screenshot should preserve the same perceptual sequence:

1. **Atmosphere first.** A bright blue/white sky fills the viewport instead of generic SaaS white or a dark dashboard.
2. **One floating specimen.** Cracked Resume uses the resume object. H.A.R.D. uses a believable product/browser surface.
3. **Editorial question.** Large centered serif copy carries the tension. The headline must feel like an editorial statement, not a startup feature pitch.
4. **One white action object.** URL input + one action should read as the obvious thing to touch.
5. **Tiny friction reducer.** Public-surface review and no-signup copy sit directly under the action.
6. **Trust after the job.** Do not lead with methodology, standards, partner logos, or feature cards.
7. **Result as reveal, not dashboard.** The B and 78/100 become the dominant editorial objects on a floating white sheet. H.A.R.D. posture is the second-level answer.
8. **Reasoning by typography.** The developer trace should be structured by headings, rules, spacing, and prose rather than colored dashboard cards.

Reject the screen if it feels like:
- a cybersecurity scanner,
- a compliance dashboard,
- a design-system documentation page,
- a purple AI SaaS landing page,
- a bento-grid startup homepage,
- or a generic “research tool.”

The intended reaction is closer to:

> “This feels like Cracked Resume, but the thing being judged is my product.”

The acquisition page may be visually aggressive. The H.A.R.D. evidence boundary may not be.

## What Cracked Resume gets right

### 1. It compresses the entire job into one high-stakes question

The landing page does not begin with AI architecture, ATS theory, feature cards, or a product tour.

It begins with:

> Your Resume Has 30s to Live. Will It Pass FAANG Recruiter?

The user immediately understands:
- the object being judged,
- the evaluator,
- the stakes,
- the decision they want answered.

H.A.R.D. needs the same compression.

Recommended product question:

> **Your product looks done. Is it?**

Supporting question:

> Would it survive a real product review?

The detailed protocol comes later.

### 2. One action dominates the first screen

Cracked Resume gives one primary action: upload the resume.

The site also explicitly removes one common objection: no signup is required before value.

H.A.R.D. translation:

> Paste a public product URL.

Primary action:

> **Grade my product**

Microcopy:

> Public-surface review · No signup required

Do not put MCP, Skill, protocol PDF, research paper, pilot packet, or criterion navigation beside the primary action. Those remain available in methodology/developer contexts, not in the acquisition funnel.

### 3. The evaluator has a point of view

Cracked Resume is not framed as a generic “resume analyzer.” It says the resume is judged from a FAANG recruiter point of view.

H.A.R.D. should also avoid generic “AI website audit” framing.

The evaluator point of view is:

> A finished-looking product reviewed the way a serious product/engineering team would reopen its consequential decisions, failure paths, and evidence before a broader commitment.

The point of view is the differentiation.

### 4. It converts uncertainty into a score plus reasons

The public product description emphasizes:
- a score,
- blunt feedback,
- what is getting the user rejected.

That sequence is stronger than a checklist.

H.A.R.D. translation:

1. **B · 78/100**
2. **H.A.R.D. posture: EVIDENCE NEEDED**
3. **The one thing to fix first**
4. Why it matters
5. What to prove next

The grade gets attention. The reasoning earns trust.

### 5. Social proof appears after the core job is obvious

Cracked Resume follows the main action with trust signals rather than placing them before the user understands the product.

H.A.R.D. must not fabricate equivalent proof.

Until real external-use data exists, use methodological trust instead:
- H.A.R.D. Protocol version
- public methodology
- evidence boundary
- exact reviewed surface
- exact retained evidence

Later, real partner/cohort proof can be added only when permission and evidence exist.

## What H.A.R.D. should not copy

### 1. Do not turn rigor into “roast” theater

The resume product can use entertainment language because its job is low-consequence advice.

H.A.R.D. may surface accessibility, authority, recovery, privacy, and agent actions. It should be direct, but not sensational.

Use:

> Duplicate refund protection is not demonstrated.

Not:

> Your refund system is broken.

### 2. Do not make the score unstable or opaque

A public LinkedIn comment on the Cracked Resume launch reported that after accepting suggested resume changes and uploading the revised version, the tool returned more red flags.

Whether that specific report reflects a product defect or changed analysis cannot be established from the comment alone, but it exposes an important product requirement for H.A.R.D.:

**a report must be reproducible enough to explain why a score changed.**

Therefore every H.A.R.D.-adjacent report should retain:
- report/rule version,
- reviewed surface,
- content/evidence identity where possible,
- finding status,
- evidence level,
- score contribution,
- changes between runs.

“Your grade changed” is not sufficient. The product must be able to answer “what changed?”

### 3. Do not make trust depend on an unverifiable expert claim

Cracked Resume markets a FAANG-recruiter point of view.

H.A.R.D. should instead expose the actual method:
- public signal rules,
- H.A.R.D. route,
- evidence stage,
- decision posture,
- specialist-review boundaries.

Trust should come from inspectability.

## H.A.R.D.'s deeper product model: decision debugging

The unique experience is not the score.

The score is only the entry point.

For every consequential issue the product moves through a developer-like debugging sequence:

### OBSERVED

What can actually be seen in the reviewed surface or retained evidence?

### DECISION UNDERNEATH

What product/system decision does that observed behavior depend on?

### WHAT MUST BE TRUE?

What invariant, source of truth, authority boundary, state rule, contract, or assumption must remain true for the decision to be sound?

### IF IT FAILS

What bounded failure condition makes the risk concrete?

### EVIDENCE

What evidence exists and at what level?

### PROVE NEXT

What is the smallest coherent test, walkthrough, artifact, or runtime check that would resolve the uncertainty?

Example:

**Observed**  
The automated agent can issue a refund.

**Decision underneath**  
An automated component is allowed to create an external financial side effect.

**What must be true?**  
One authorized request maps to one refund even under duplication, timeout, or retry.

**If it fails**  
The user can receive duplicate refunds or the order/payment systems can disagree.

**Evidence**  
Walkthrough only.

**Prove next**  
Execute the same refund request twice against the exact implementation and retain the transaction/idempotency/final-state evidence.

This is the interaction that turns the protocol into a product.

## Product architecture

### Acquisition

One page. One job.

**Your product looks done. Is it?**

URL -> public review -> report.

### Report first frame

The first viewport must show:
- product/company,
- letter grade,
- 0-100 Product Signal Grade,
- H.A.R.D. posture,
- evidence confidence,
- coverage,
- one highest-priority finding.

### Progressive disclosure

Do not lead with all protocol detail.

Order:

1. Grade
2. H.A.R.D. posture
3. Fix first
4. Five product-signal areas
5. Developer view
6. Unknowns / Verify next
7. Full H.A.R.D. evidence detail
8. Technical provenance

### Evidence upgrade loop

A public scan will often have low confidence.

That is useful rather than embarrassing.

The product should convert low confidence into the next action:

> 5 unknowns were not counted as failures.

> Verify these with a PRD, prototype, code, test record, runbook, or walkthrough.

This creates the natural path:

Public surface -> supplied artifacts -> walkthrough -> implementation -> runtime evidence.

## Cheap product architecture

Cracked Resume's zero-friction behavior only works if the product can afford to give value before account creation.

H.A.R.D. should therefore keep the expensive intelligence out of the critical path.

### Tier 0: deterministic

- bounded fetch
- metadata extraction
- HTML/semantic checks
- deterministic accessibility signals
- policy/docs presence
- static rule checks
- report scoring
- report rendering
- content-hash cache

No model required.

### Tier 1: bounded synthesis

Optional small-model call after findings are frozen:
- remove repetition,
- turn rule output into concise recipient language,
- rank already-supported findings.

The model cannot change status or create evidence.

### Tier 2: actual H.A.R.D. review

Triggered only when the organization supplies stronger artifacts/evidence.

This is where consequential decisions, assumptions, system surfaces, challenge scenarios, and human-owned disposition become deeper.

Mass outreach therefore does not require a full expensive H.A.R.D. run for every URL.

The cheap public grade opens the door; H.A.R.D. creates the deeper value.

## Design rejection criteria

Reject a design if it:
- looks like a compliance dashboard,
- puts the six gates before the user's result,
- calls 0-100 a H.A.R.D. score,
- uses a radar chart/gauge as the main visual,
- has more than one main CTA in the first viewport,
- needs signup before showing value,
- automatically treats unknown as fail,
- hides evidence confidence,
- cannot explain a score delta,
- requires an LLM to render the report,
- contains fake benchmark/social proof,
- reduces the developer reasoning sequence to generic “recommendations.”
