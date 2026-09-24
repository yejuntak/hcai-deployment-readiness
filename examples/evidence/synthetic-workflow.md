# SYNTHETIC fixture — no actual pilot or participant

Fictional appointment intake, version fixture-1. Requirement R1: an advisor
can review a draft request, correct missing information, cancel, and return
to intake without losing entered data. Acceptance: each path preserves the
documented fields and never sends an unapproved request. Normal: review →
confirm. Edge: missing detail → flag. Recovery: cancel → saved intake.
The hypothetical owner is the intake lead. The email system is a dependency.
T1 is a stipulated successful specification walkthrough, not an executed
system test. No model or operational performance measurement exists.
All roles, notes, checks, rates and costs in examples are constructed inputs.
