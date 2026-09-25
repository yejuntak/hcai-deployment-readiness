# Start a workflow review

H.A.R.D. Protocol 0.2 · Public Preview

Human-centered AI Readiness and Decision Protocol

Use this guide when a team has a proposed workflow and needs to decide whether to invest engineering time. An advisor asks six questions about the work and records the evidence behind the answers. You can begin here without reading the full protocol. The review supports an engineering recommendation; it cannot certify a system or approve a launch.

## What to bring

1. A recent example of how the work happens today.
2. The proposed screen, workflow, prototype, or code revision.
3. Someone who knows the work and someone accountable for the next decision. One person may fill both roles in a small team.

The advisor can take notes while the participant talks. Paper is sufficient. The optional MCP and Skill tools record the same evidence and apply the protocol's rules.

## Begin with this question

“Walk me through one recent case, from the request arriving to the work being finished. Where did someone have to check, fix, or chase it?”

If nobody can show a current case or quantify the work, stop and arrange to observe it. A prototype does not supply the missing baseline. For a genuinely new service, investigate the closest real workaround. Until a baseline is available, leave ROI unresolved.

## Choose the path together

When the proposed artifact looks finished, ask for the work underneath it. Keep the original and sketch a separate task or state map. Show the information people need, the choices they face, dependencies, failure/recovery paths and who acts. Mark unknowns instead of filling gaps by assumption. Check findings against the original artifact and its requirements. This is a discussion aid, not proof that a simplified presentation improves detection.

Low risk, with records already available: use [QUICK-6](QUICK-6.md).  
Higher or unknown risk, missing evidence, or a longer conversation: use [FULL](FULL-PROFILE.md).

Before choosing, ask whether mistakes could affect safety or rights, perform an irreversible external action, expose sensitive data, or turn untrusted input into actions. The first two require high-depth FULL; the others require at least moderate FULL. If unsure, do not guess “no.”

Ask about people affected by the result as well as those buying or operating it. Who might struggle to use it, be treated differently, lose privacy, or be unable to correct a mistake? Each applicable concern needs a requirement and a check.

The 15-minute target is untested and does not include undisclosed preparation. Record preparation and session time separately. Needing more time or an accessible format is not a failure.

## Record the result

- A recommendation: fund a bounded engineering step, revise, or gather evidence.
- The reason, in ordinary language.
- One next action and an accountable owner.
- What has been demonstrated and what remains untested.
- Review effort separate from estimated operating benefit.

Suppose a booking prototype looks finished, but nobody can show what happens after a payment failure. A “72% ready” rating would leave the problem unresolved. The review should instead name the work: “Define and validate recovery of the booking details; the product owner owns that revision.”

Examples are constructed, not pilot results. Read [more scenarios](SCENARIOS.md), inspect the [criteria](CRITERIA.md), or see [what changed](https://www.takyejun.com/research/ai-readiness/updates).

Use the [worksheet](WORKSHEET.md) to note where the evidence can be found. One existing work log or review note may support several fields. The advisor handles the detailed record and file fingerprints; participants should not have to create extra documents simply to fill a form.

Execution versions: protocol 0.2-preview.2 · MCP 0.2.0rc8 · Skill/contract 0.2.0-rc.8.
