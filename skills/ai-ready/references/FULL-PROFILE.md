# Full risk-tiered engineering profile

Protocol 0.1-rc.4-candidate · MCP 0.2.0rc1 · Skill/contract 0.2.0-rc.1

Use FULL after a QUICK6 stop, whenever risk is moderate/high/unknown, or when the team elects deeper review. FULL has no claimed duration. It uses the same six gates and field definitions in PROTOCOL.md; it evaluates all gates and retains all failures and missing evidence.

1. Freeze scope, current and proposed versions, actor roles, evidence sources and risk classification. Gather actual baseline observations; review variation and whether the window represents the intended work. At least 1/3/5 observed cases are required for low/moderate/high tiers. These are provisional floors, not statistical sufficiency.
2. Conduct need review. Moderate/high require two distinct sources for each need plus actual end-user discussion. Record which requirement responds to each need. Do not treat an expert's opinion about this protocol as product-need evidence.
3. Walk through requirements and normal, edge and recovery behavior, including data preservation and dependencies. Retain reproduction steps and reference material for form, fit and function. Compare each requirement/artifact pair with an executed walkthrough or test. Keep runtime tests and walkthroughs distinguishable.
4. Record defects, reviewer findings, disputes and unresolved risks. Moderate/high add an independent reviewer and a validation plan. High adds hazard analysis, mission review and a realistic operational evaluation plan specifying future users, conditions, measures, acceptance criteria and stopping conditions. A plan is not operational performance evidence.
5. Estimate gross and net operating effects, including review/correction/escalation/rework and remaining manual work. Separate recurring from one-time costs. Record evaluation person-minutes, calls/tokens/costs and adjudication burden independently.
6. Run the shared engine. A documented failure yields REVISE; otherwise missing required evidence yields INSUFFICIENT_EVIDENCE; all passes yield a bounded PROCEED_TO_ENGINEERING recommendation. The owner records authorization/refusal separately, resource ceiling and next review trigger. Preserve prior runs and record revisions.

If evaluating human reviewers as a research question, use a separate blinded packet and pre-disclosure judgment lock, followed by adjudication. Retain rc.3 evaluator metrics separately and do not pool criterion versions. The shared engine is model-agnostic, but classification, evidence truth and scope completeness still require human judgment.
