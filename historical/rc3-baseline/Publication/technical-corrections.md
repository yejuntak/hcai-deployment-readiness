# Technical corrections in v0.1-rc.2

An AI-assisted technical audit of v0.1-rc.1 reproduced three boundary defects: impossible omission subsets were accepted; an unassessed-only gate case was labeled Hold for remediation; and a blank first batch row blocked otherwise consistent criteria. The corrected workbook enforces subset consistency, reconciles verified/failed/unassessed checks, and compares populated criteria without requiring the first row.

Added companion measures expose abstention, decision coverage, decisive false-ready acceptance, false holds and missingness on criterion-ready controls. Added physically separate evaluator materials to reduce accidental answer disclosure. Added closest prior work and a controlled-comparison plan. The instructional arithmetic and provisional gate remain, with implementation corrections documented.

Executed checks are retained in Verification/. They establish calculation behavior only. No independent external review, participant study, benchmark validation or measured benefit was performed. Historical v0.1-rc.1 remains a separate release.
