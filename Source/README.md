# Reproduction and canonical CSV validation

The current templates and worked examples share the exact ordered headers in `schemas/csv-contract.json`. `Source/verify_example.py` accepts a user-created review directory. Install the project first (`python3 -m pip install .`) or run it with the project virtual environment. Header-only validation uses the standard library; completed reviews use the same Pydantic contract and gate engine as MCP and the portable Skill:

```sh
python3 Source/verify_example.py
python3 Source/verify_example.py Worked-Example/runtime-ai-plan --json
python3 Source/verify_example.py Templates --templates
python3 Source/verify_example.py /path/to/completed-review --json
python3 Source/verify_example.py Worked-Example/runtime-ai-plan --artifact-json > artifact-review.json
```

Copy the templates to a new directory, freeze the requirements and recovery briefs, and fill the matching completed matrices plus one decision row. Header-only templates validate with `--templates`; they do not count as a completed assessment. Findings, reference keys, choice records and batch records are optional, but any supplied file is validated against its canonical contract. References and brief IDs must reconcile. Old `handoff_status` files are rejected explicitly; migrate each stage against retained evidence instead of copying one historical status into all four evidence stages.

Each requirement and recovery scenario records `specified`, `walkthrough`, `implemented` and `runtime_tested` independently, with separate status, evidence location and reason. `pass` and `fail` need their own location. `not_applicable` needs a reason and never counts as a pass for a required stage. Unassessed current checks remain in their denominators. Specification/prototype handoff requires specified and walkthrough evidence; implementation review adds implemented evidence; runtime release review adds runtime evidence. None of these arithmetic labels authorizes deployment.

The verifier checks exact headers, row shape, identifiers, retained scope, evidence-stage records, finding references, Critical support fields, population stratification and stage counts. It converts the CSVs to `ArtifactReview` and uses `review_artifact` for the recorded disposition; there is no separate CSV gate algorithm. Accepted unresolved major or Critical findings block handoff, and unresolved important choices prevent eligibility even with positive matrices. Human choice acceptance/revision requires retained confirmation evidence. The `--artifact-json` export is a directly consumable record for the current MCP/Skill artifact-review path. Deferred/excluded items need a reason and scope owner and cannot be current dependencies. These are checks on supplied records; software does not authenticate the contents of a source location or establish severity by itself.

The synthetic SR-01 example preserves its instructional arithmetic: requirements 7/10, recovery 3/6, reference recall 5/8, expected-recall gap 17.5 percentage points, omission recognition 1/3, and synthetic batch false-ready rate 3/4. The separate runtime-AI plan example demonstrates artifact-review mode with all evaluator metrics N/A. It was authored for instruction and is not a reconstruction of an external user's private report.

Evaluator eligibility uses the shared `evaluator_metric_reasons` function and the same explicit role/order fields as MCP. Unknown declarations remain unknown. An evaluator who authored the artifact or reference cannot claim independent detection performance. Self-adjudication needs independently confirmed matches; reference author and adjudicator may be the same person when the evaluator is independent. Missing pre-reference expectation lock suppresses only the gap; an unfrozen omission subset suppresses omission recognition. False-ready diagnostics separately require a locked judgment and independently established criterion. Missing recall findings lock does not automatically invalidate an otherwise valid judgment metric. Agent runs do not produce independent-human performance metrics. Synthetic eligibility is stipulated for arithmetic instruction only.

Batch pooling requires the same criterion version, evaluator kind, artifact population, mode and stage. Unknown populations are rejected. Missing judgments are reported separately, not silently turned into a successful decision.

`Source/build_workbook.mjs` and existing PDF/XLSX files reproduce historical release arithmetic. They are not current CSV importers and do not express this upgraded four-stage contract. Use the current CSVs and verifier for the current examples; preserve historical binaries as release records. JSON verification records describe technical checks, not participant studies.
