# Verification of v0.1-rc.1

Prepared September 8, 2026.

- Three PDFs rendered: protocol (8 pages), scorecard (3), worked example (3). Page layouts reviewed.
- Both workbook sheets rendered in the blank and completed workbooks.
- Spreadsheet calculations checked in the artifact-tool calculation engine against the synthetic source records.
- Checked blank versus zero, numerator exceeding denominator, missing judgment, abstention, duplicate batch ID, incomplete evidence and handoff eligibility.
- Formula-error scans returned no matches after corrections.
- Source/verify_example.py independently reproduces six example measurements with the Python standard library.

The workbook has not been interactively tested in Microsoft Excel. It uses ordinary scalar Excel formulas and validation lists. These checks establish arithmetic and packaging behavior, not empirical validity of the protocol, reference key or severity judgments.
