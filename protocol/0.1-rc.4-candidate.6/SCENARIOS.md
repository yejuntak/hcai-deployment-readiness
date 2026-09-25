# Scenarios for using the protocol

Protocol 0.1-rc.4-candidate.6 · All examples below are constructed, not external pilot results.

## 1. An owner wants to automate intake

The proposed AI intake screen is polished. The owner cannot say how many requests arrive, how long staff spend, or where cases get stuck.

**Review outcome:** INSUFFICIENT_EVIDENCE at G1; ROI indeterminate. Observe a recent case and record volume before estimating savings. Until then, the proposal has no measured basis for its time-saving claim.

## 2. A designer presents a convincing booking prototype

The normal flow works in the demonstration. After payment failure, the user's entered details disappear and no recovery owner is defined.

**Review outcome:** REVISE at G3. Define the recovery path, assign an owner and validate the revised artifact. Link that exact revision to the validation record.

## 3. An agent edits code after the tests pass

The test report is green, but its recorded artifact digest belongs to an earlier revision. The new code changes the permission check.

**Review outcome:** REVISE at G4. Revalidate the affected requirements against the new revision. The earlier test result belongs to the earlier artifact.

## 4. A helpful agent starts acting on behalf of a person

A prototype can draft and send customer messages, but nobody has specified approval, cancellation, escalation, or who can revoke its authority.

**Review outcome:** REVISE or INSUFFICIENT_EVIDENCE at G3, depending on whether the omission is observed or unknown. Bound permitted actions, data use, human approval and recovery. Higher impact or difficult reversal requires FULL.

## 5. AI wrote the interface, but does not run the service

A team used an AI coding assistant to build a conventional internal form. There are no AI-generated outputs during operation.

**Review outcome:** record ai_role as artifact_creation. Assess operational review burden honestly: relevant AI-output review can be zero with a reason, while normal support, error correction, and manual work may remain. Assess the service that will actually run; AI-assisted authorship alone does not establish a runtime AI risk.

## 6. Gross savings disappear during review

A fictional case saves 15 minutes before oversight. Checking takes 8 minutes, corrections 5, and escalation/rework 2. Net labor savings are zero before any recurring service cost.

**Review outcome:** show gross 15 and net 0 separately. Do not preserve the original inflated ROI. If the team still wants to invest for another reason, record the explicit rationale; the tool does not authorize that choice.

## 7. A researcher tests whether polish changes defect detection

Participants judge whether each requirement has a defect and how confident they are. AI authorship is held constant; fidelity varies.

**Review outcome:** a separate study-review record, not an engineering recommendation. Keep ground-truth answers outside the participant record. Perceived readiness is not actual readiness. Guided criteria may change the experimental task, so do not introduce them without the study design specifying that intervention.

## What these examples do not establish

These constructed cases explain how the review is intended to work. Establishing effects on defects, ROI or usability, or the causal effects of AI coding, requires appropriate empirical studies.
