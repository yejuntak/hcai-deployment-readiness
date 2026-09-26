# RP-01: synthetic runtime-AI support-draft plan

This is a fictional plan authored solely for instruction. It is not the external health-report attachment and contains no clinical scenario, user evidence, or real evaluation result. The feature will use runtime AI, but no implementation exists.

## A1 Purpose and boundary

A support worker requests a draft reply based on an authenticated customer's selected support ticket. The model only drafts. A human worker reviews and edits before sending in the existing mail tool. The model cannot send or update the account.

## A2 Identity and source

The server checks worker authorization and requests the selected ticket from ticket-service. The draft must identify the source ticket and be marked Draft. No other customer history is in scope.

## A3 Review and rejection

The human worker may reject or edit the proposed draft. Rejection returns to the unchanged ticket and does not send a message. A successful generation shows the editable draft beside the original ticket.

## A4 Planned validation

Before implementation, the owner must specify the timeout, service-unavailable, generation-failure, and misleading-output response states. These states are currently absent. No model performance evaluation, application code, or runtime test is supplied.

## A5 Deferred work

Phase 3 proposes sentiment analytics over historical tickets. It is excluded from this current ticket-only drafting handoff and has no dependency needed to draft or review this ticket. No analytics claim is made for the present phase.
