# SR-01 evaluator brief

Stage: engineering handoff. Artifact: artifact.html, version SR-01, September 8, 2026. Type: AI-assisted, specification-based fictional interface; no runtime AI. Purpose: learn the procedure. No time limit has been empirically established; record elapsed time.

Task: inspect the support-request specification as an employee choosing a service, entering details and requester identity, navigating back, validating inputs, submitting, cancelling and recovering from failures. Access-change requests are consequential in this fictional context and require explicit confirmation before sending.

Mandatory requirements: R01 service selection; R02 retain details on navigation; R03 requester identity; R04 field validation; R05 pending-state behavior; R06 unique success reference; R07 timeout recovery retaining inputs; R08 prevent duplicate requests; R09 cancellation before sending; R10 confirmation before access-change sending.

Recovery checks: S01 empty field; S02 invalid requester; S03 timeout; S04 server rejection; S05 repeated-click feedback and preservation; S06 cancellation during processing.

Gate: all mandatory requirements and applicable recovery checks must be specified and walkthrough verified; no critical open issue, unassessed mandatory item or incomplete evidence record. Apply the protocol's severity rules. Record findings and judgment on the scorecard before opening the reference files.
