# Claude Design prompt: near-clone composition, H.A.R.D. meaning

Design the H.A.R.D. Readiness Report experience by using Cracked Resume (https://crackedresume.com/) as a near-clone benchmark for composition, pacing, interaction compression, and first-screen hierarchy.

IMPORTANT:
- Do NOT make a generic "inspired by" SaaS page.
- Get much closer to Cracked Resume's actual visual skeleton.
- Do NOT copy its logo, exact wording, proprietary images, school logos, or other identity assets.
- The composition and interaction model should feel immediately familiar if someone has seen Cracked Resume.

## What to reproduce very closely

Landing composition:
1. Full-viewport bright atmospheric/sky background.
2. One floating white specimen/card near the top center.
3. Large centered serif question below it.
4. One very short supporting sentence.
5. One small row that makes the evaluator/lenses concrete.
6. One dominant white CTA/input element.
7. Tiny friction-removal copy directly beneath it.
8. One small trust/value line below.
9. Almost no navigation.
10. No feature grid before the user takes action.

Use the same extreme whitespace, narrow centered column, playful confidence, and "single poster" feeling.

## Replace the job, not the structure

Cracked Resume's job:
Resume -> "will a recruiter pass this?" -> upload -> score -> rejection reasons.

H.A.R.D.'s job:
Product -> "is this actually ready underneath the polish?" -> URL/artifact -> Product Signal Grade -> one issue to fix first -> open the product decisions underneath it.

The hero should resolve to something as compressed as:

H.A.R.D. READINESS REPORT

Your product looks done.
Is it?

We review it like a real product and engineering team would:
the decisions, failure paths, and evidence hiding underneath the polish.

[ https://yourproduct.com                 Grade product ]

public-surface review · no signup required

One grade. One thing to fix first.
Then open the decisions underneath it with H.A.R.D.

Do not treat the wording above as sacred. Improve it only if it becomes more immediate, not more explanatory.

## Floating specimen

Instead of a resume sheet, show a small original product/browser specimen.

It should look like a finished SaaS/AI flow, for example:
- customer requests refund
- polished support-agent UI
- obvious successful end state

Then subtly expose the hidden questions:
Authority?
Duplicate request?
Timeout?
Partial failure?
Recovery?

The specimen exists to make the thesis visual:
"looks finished" does not mean "the decisions underneath it are closed."

Do NOT add a decorative abstract AI illustration.

## Product result reveal

After the scan, keep the same ruthless simplicity.

First viewport of result:

NORTHSTAR AI

B
78 / 100

Product Signal Grade

H.A.R.D.
EVIDENCE NEEDED

Evidence confidence 30%
Coverage 70%

THE ONE THING TO FIX FIRST

Duplicate refund protection is not demonstrated.

The user should understand this in under 5 seconds.

## Critical semantic separation

Never call 78 the "H.A.R.D. score."

The numeric grade is a Product Signal Grade only.

The numeric grade may use these public/product-surface modules:
- Accessibility
- Action & Recovery
- Privacy & Data Boundary
- AI Transparency & Claims
- Public Evidence & Documentation

H.A.R.D. remains separate and non-compensatory:
- NOT VERIFIED
- EVIDENCE NEEDED
- HOLD
- BOUNDED NEXT STEP

A product may show:

A · 92/100
HOLD

That is intentional.

A high product-surface score cannot average away:
- a failed H.A.R.D. gate
- a conflicted consequential assumption
- a failed challenge
- an unresolved critical finding

SEO/AEO may appear later under "Growth signals."
They never change readiness.

## The deep interaction model: think like a developer debugging a system

The score is only the front door.

When a user opens a consequential finding, do not give a generic recommendation card.

Use this exact reasoning progression:

OBSERVED
What can we actually see in the reviewed artifact or evidence?

DECISION UNDERNEATH
What product/system decision is embodied by the observed behavior?

WHAT MUST BE TRUE?
Which invariant, authority rule, source of truth, state model, contract, or assumption must hold?

IF IT FAILS
What concrete bounded failure condition makes the consequence real?

EVIDENCE
What is actually supported?
Public observation / documented / specified / walkthrough / implemented / runtime tested / unknown.

PROVE NEXT
What is the smallest coherent test, artifact, or walkthrough that would resolve the uncertainty?

Example:

Observed
The AI support agent can initiate a refund.

Decision underneath
An automated component is authorized to create an external financial side effect.

What must be true?
One authorized request must map to one refund even under retries, duplicate requests, timeout, or interrupted execution.

If it fails
The customer can receive duplicate refunds or the order and payment systems can disagree.

Evidence
Walkthrough only.

Prove next
Execute the same refund request twice against the exact implementation and retain the transaction, idempotency, and final-state evidence.

This is the core of the product.

Do not reduce this into:
"Recommendation: improve refund handling."

## Unknowns

Unknown is not failure.

If the public surface cannot establish something, say:

"Runtime recovery evidence was not observable from the reviewed public material."

Never say:
"The company has no recovery mechanism."

Unknown findings:
- do not silently count as failures
- reduce coverage/confidence
- create the next conversion step

Example:

5 UNKNOWN
These were not counted as failures.

Verify them with:
PRD
prototype
code
runbook
test evidence
walkthrough

[ Verify the unknowns ]

This is how a cheap public scan becomes a deeper H.A.R.D. review.

## Analysis/progress state

Stay visually close to the same landing composition.

Do not suddenly switch into a dense dashboard.

Show only real steps:
- Reading public product surface
- Checking accessibility signals
- Mapping action/recovery paths
- Reviewing privacy/data boundaries
- Checking AI claims
- Building evidence map

Do not show fake "AI thinking" animations.

## Visual rules

Stay extremely close to Cracked Resume's visual density:
- atmospheric blue/white backdrop
- black text
- centered serif headline
- white floating object/card
- subtle soft shadow
- rounded white CTA
- tiny supporting text
- very little chrome
- no dashboard sidebar
- no gradients that look like generic AI SaaS branding beyond the sky atmosphere
- no neon
- no glassmorphism
- no radar charts
- no speedometer/gauge
- no card soup

Report can transition to a neutral off-white background, but it should still feel like the same product.

## Trust

Do not invent:
- customer count
- partner logos
- universities
- benchmark percentile
- testimonials
- certifications
- standards endorsements

Until real cohort data exists, trust comes from:
- exact reviewed surface
- retained evidence
- evidence confidence
- coverage
- H.A.R.D. version/methodology
- explicit unknowns
- reproducible score changes

## Cost constraint

The product should be cheap enough to mass-generate.

Every core UI element must render from structured JSON.

No LLM is required for:
- grade
- module scores
- confidence
- coverage
- deductions
- unknowns
- H.A.R.D. posture
- HTML/PDF rendering

Optional model use is allowed only after findings are frozen, to compress wording.
A model cannot create evidence or change status.

## Deliverables

Produce:
1. Near-clone landing page composition
2. URL input state
3. Analysis state
4. Grade reveal
5. Full desktop report
6. Mobile report
7. Finding-detail interaction
8. Verify-unknown flow
9. Shareable report state

For every screen specify:
- exact hierarchy
- exact or near-final copy
- component behavior
- what changes between states
- what is intentionally omitted

## Final audit

Do not finish until all answers are YES:

- Does the landing feel almost compositionally identical to Cracked Resume?
- Is there only one obvious action?
- Can the user explain the product in one sentence after 5 seconds?
- Is B · 78/100 visible before methodology?
- Is H.A.R.D. visibly separate from the numeric score?
- Can a strong score never erase a H.A.R.D. blocker?
- Does every important issue open into Observed -> Decision -> Must be true -> If it fails -> Evidence -> Prove next?
- Are unknowns visibly different from failures?
- Could the report render without an LLM?
- Does the experience avoid feeling like compliance software?
- Is every claimed fact backed by an evidence location or labeled unknown?

If any answer is no, revise before presenting.
