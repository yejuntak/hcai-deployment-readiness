# Verification of v0.1-rc.2

Prepared September 8, 2026.

- Protocol PDF (7 pages), complete scorecard (3), evaluator-only scorecard (2) and calculation notes (1) rendered and visually checked. The preceding 3-page worked-example narrative is retained with a separate correction note.
- Both worksheets in both blank and completed workbooks rendered and visually checked.
- Three rc.1 boundary defects reproduced, recorded, and corrected: impossible omission subsets, unassessed-only disposition, and a blank first batch row.
- Eleven named regression checks passed in the artifact-tool calculation engine; see Verification/rc2-workbook-tests.json. Blank inputs also remain unevaluated.
- Added checks reconcile verified, failed and unassessed mandatory items. Companion rates expose abstention and false holds rather than interpreting false-ready acceptance alone.
- Formula-error scans returned no matches in the final blank and completed workbooks.
- Source/verify_example.py separately reproduces six synthetic CSV measurements using the Python standard library.

These are technical checks assisted by OpenAI Codex, not independent review, participant results, validation of the reference key, or evidence of effectiveness. The exported workbooks have not been interactively tested in Microsoft Excel.
