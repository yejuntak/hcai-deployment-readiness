"""Regression checks for public template/example interoperability and denominator safety."""
import csv
import importlib.util
from pathlib import Path
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("csv_verifier", ROOT / "Source/verify_example.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


def copy_example(tmp_path, runtime=False):
    source = ROOT / "Worked-Example"
    if runtime:
        source /= "runtime-ai-plan"
    for path in source.glob("*.csv"):
        shutil.copy(path, tmp_path / path.name)
    return tmp_path


def mutate(directory, name, transform):
    rows = verifier.read_csv(directory, name)
    transform(rows)
    with (directory / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=verifier.CONTRACT["files"][name]["columns"])
        writer.writeheader()
        writer.writerows(rows)


def test_all_current_templates_and_examples_use_identical_canonical_headers():
    verifier.validate_directory(ROOT / "Templates", allow_empty=True)
    for directory in (ROOT / "Worked-Example", ROOT / "Worked-Example/runtime-ai-plan"):
        verifier.validate_directory(directory)
        for path in directory.glob("*.csv"):
            with path.open() as completed, (ROOT / "Templates" / path.name).open() as template:
                assert next(csv.reader(completed)) == next(csv.reader(template))


def test_sr01_preserves_arithmetic_and_all_unassessed_denominators():
    result = verifier.summarize(ROOT / "Worked-Example")
    assert result["requirements"]["coverage"] == 0.7
    assert result["recovery"]["denominator"] == 6
    assert result["recovery"]["unassessed"] == 2
    assert result["recovery"]["coverage"] == 0.5
    assert result["reference_recall"] == 5 / 8
    assert result["expected_recall_gap_pp"] == pytest.approx(17.5)
    assert result["omission_recognition"] == 1 / 3
    assert result["false_ready_batch_rate"] == 0.75
    assert result["requirements"]["by_evidence_stage"]["runtime_tested"]["unassessed"] == 10


def test_runtime_ai_plan_is_descriptive_and_deferred_scope_stays_visible():
    result = verifier.summarize(ROOT / "Worked-Example/runtime-ai-plan")
    assert result["artifact_population"] == "runtime_ai"
    assert result["stage"] == "specification_handoff"
    assert result["requirements"]["denominator"] == 5
    assert result["requirements"]["excluded_or_deferred"] == 1
    assert result["recovery"]["unassessed"] == 1
    assert result["reference_recall"] is None
    assert result["critical_open"] == 0
    assert result["disposition"] == "Hold for remediation"


def test_template_alone_cannot_be_reported_as_completed_review():
    with pytest.raises(ValueError, match="At least one"):
        verifier.validate_directory(ROOT / "Templates")


def test_legacy_header_and_ragged_csv_are_rejected(tmp_path):
    directory = copy_example(tmp_path)
    (directory / "requirements.csv").write_text("requirement_id,handoff_status\nR01,Verified\n")
    with pytest.raises(ValueError, match="headers"):
        verifier.validate_directory(directory)
    shutil.copy(ROOT / "Worked-Example/requirements.csv", directory / "requirements.csv")
    with (directory / "requirements.csv").open("a") as stream:
        stream.write("R99,yes\n")
    with pytest.raises(ValueError, match="ragged"):
        verifier.validate_directory(directory)


def test_removing_unassessed_row_cannot_shrink_frozen_denominator(tmp_path):
    directory = copy_example(tmp_path)
    mutate(directory, "recovery.csv", lambda rows: rows.pop())
    with pytest.raises(ValueError, match="frozen scope"):
        verifier.validate_directory(directory)


def test_stage_evidence_cannot_be_invented_by_copying_one_status(tmp_path):
    directory = copy_example(tmp_path)
    mutate(directory, "requirements.csv", lambda rows: rows[0].update(runtime_tested_status="pass"))
    with pytest.raises(ValueError, match="own evidence location"):
        verifier.validate_directory(directory)


def test_malformed_status_and_duplicate_id_fail(tmp_path):
    directory = copy_example(tmp_path)
    mutate(directory, "requirements.csv", lambda rows: rows[0].update(specified_status="probably"))
    with pytest.raises(ValueError, match="invalid specified_status"):
        verifier.validate_directory(directory)
    mutate(directory, "requirements.csv", lambda rows: rows[0].update(specified_status="pass", requirement_id="R02"))
    with pytest.raises(ValueError, match="duplicate"):
        verifier.validate_directory(directory)


def test_not_applicable_required_stage_cannot_pass(tmp_path):
    directory = copy_example(tmp_path, runtime=True)
    mutate(directory, "requirements.csv", lambda rows: rows[0].update(walkthrough_status="not_applicable", walkthrough_reason="Reviewer unavailable", walkthrough_evidence_location=""))
    mutate(directory, "decision.csv", lambda rows: rows[0].update(mandatory_unassessed="2"))
    result = verifier.summarize(directory)
    assert result["requirements"]["verified"] == 2
    assert result["requirements"]["unassessed"] == 1
    assert result["requirements"]["denominator"] == 5


def test_mixed_and_unknown_artifact_populations_fail_pooling(tmp_path):
    directory = copy_example(tmp_path)
    mutate(directory, "batch.csv", lambda rows: rows[0].update(artifact_population="runtime_ai"))
    with pytest.raises(ValueError, match="stratify"):
        verifier.validate_directory(directory)
    mutate(directory, "batch.csv", lambda rows: rows[0].update(artifact_population="unknown"))
    with pytest.raises(ValueError, match="unknown artifact population"):
        verifier.validate_directory(directory)


def test_current_dependency_cannot_be_deferred(tmp_path):
    directory = copy_example(tmp_path, runtime=True)
    mutate(directory, "requirements.csv", lambda rows: rows[-1].update(current_dependency_yes_no="yes"))
    with pytest.raises(ValueError, match="current dependency"):
        verifier.validate_directory(directory)


def test_unconfirmed_disclaimer_concern_cannot_be_critical(tmp_path):
    directory = copy_example(tmp_path, runtime=True)
    mutate(directory, "findings.csv", lambda rows: rows[0].update(severity="critical"))
    with pytest.raises(ValueError, match="Critical must be confirmed"):
        verifier.validate_directory(directory)


def test_role_overlap_suppresses_evaluator_metrics_without_erasing_artifact_coverage(tmp_path):
    directory = copy_example(tmp_path)
    mutate(directory, "decision.csv", lambda rows: rows[0].update(reference_independent_of_findings="false"))
    result = verifier.summarize(directory)
    assert result["reference_recall"] is None
    assert result["expected_recall_gap_pp"] is None
    assert result["omission_recognition"] is None
    assert result["requirements"]["coverage"] == 0.7


def test_unknown_reference_and_contradictory_disposition_fail(tmp_path):
    directory = copy_example(tmp_path)
    mutate(directory, "findings.csv", lambda rows: rows[0].update(reference_id="MISSING"))
    with pytest.raises(ValueError, match="unknown reference match"):
        verifier.validate_directory(directory)
    mutate(directory, "findings.csv", lambda rows: rows[0].update(reference_id="D01"))
    mutate(directory, "decision.csv", lambda rows: rows[0].update(disposition="Eligible for handoff review"))
    with pytest.raises(ValueError, match="disposition must"):
        verifier.validate_directory(directory)


def positive_current_checks(directory):
    for name in ("requirements.csv", "recovery.csv"):
        def fill(rows):
            for row in rows:
                if row["scope"] == "current":
                    for level in ("specified", "walkthrough"):
                        row[level + "_status"] = "pass"
                        row[level + "_evidence_location"] = "synthetic-revision.md#retained-check"
        mutate(directory, name, fill)
    mutate(directory, "decision.csv", lambda rows: rows[0].update(mandatory_unassessed="0"))


def test_shared_engine_blocks_major_even_with_positive_stage_matrices(tmp_path):
    directory = copy_example(tmp_path, runtime=True)
    positive_current_checks(directory)
    result = verifier.summarize(directory)
    assert result["requirements"]["coverage"] == 1.0
    assert result["recovery"]["coverage"] == 1.0
    assert result["disposition"] == "Hold for remediation"
    assert result["stage_review"]["unresolved_major_ids"] == ["PF02"]
    mutate(directory, "decision.csv", lambda rows: rows[0].update(disposition="Eligible for declared stage handoff review"))
    with pytest.raises(ValueError, match="Hold for remediation"):
        verifier.validate_directory(directory)


def test_shared_engine_requires_human_choice_confirmation_before_handoff(tmp_path):
    directory = copy_example(tmp_path, runtime=True)
    positive_current_checks(directory)
    def resolve(rows):
        rows[0].update(adjudication="unsupported", scope_status="current", resolution_status="closed")
        rows[1].update(resolution_status="closed", remediation_evidence_location="synthetic-revision.md#remediation")
    mutate(directory, "findings.csv", resolve)
    mutate(directory, "decision.csv", lambda rows: rows[0].update(disposition="Insufficient evidence"))
    result = verifier.summarize(directory)
    assert "human_decision_pending" in result["stage_review"]["choice_issues"]["PC01"]
    mutate(directory, "choice-review.csv", lambda rows: rows[0].update(
        disposition="accepted", human_decision_evidence_location="synthetic-owner-record.md#confirmation",
        verification_evidence_location="synthetic-revision.md#choice-check",
        current_justification="Synthetic owner reviewed the alternatives against current control and recovery criteria.",
        current_justification_evidence_location="synthetic-owner-record.md#choice-reason"))
    def resolve_surfaces(rows):
        for row in rows:
            if row["status"] == "unassessed":
                row["status"] = "supported"
                row["current_model"] = "Synthetic current model retained only for this regression fixture."
                row["evidence_location"] = "synthetic-revision.md#decision-surface"
    mutate(directory, "decision-surfaces.csv", resolve_surfaces)
    mutate(directory, "challenge-scenarios.csv", lambda rows: rows[0].update(
        status="pass", evidence_level="walkthrough", evidence_location="synthetic-revision.md#challenge", next_evidence=""))
    mutate(directory, "decision.csv", lambda rows: rows[0].update(disposition="Eligible for declared stage handoff review"))
    result = verifier.summarize(directory)
    assert result["stage_review"]["criterion_status"] == "ready"
    assert result["stage_review"]["choice_issues"] == {}


def test_assumption_lifecycle_and_challenge_level_are_machine_enforced(tmp_path):
    directory = copy_example(tmp_path)
    mutate(directory, "assumptions.csv", lambda rows: rows[0].update(status="supported", evidence_location=""))
    with pytest.raises(ValueError, match="supported/conflicted needs retained evidence"):
        verifier.validate_directory(directory)
    directory = copy_example(tmp_path)
    mutate(directory, "challenge-scenarios.csv", lambda rows: rows[0].update(evidence_level=""))
    with pytest.raises(ValueError, match="assessed challenge needs walkthrough"):
        verifier.validate_directory(directory)


def test_csv_uses_shared_metric_eligibility_per_metric(tmp_path):
    directory = copy_example(tmp_path)
    mutate(directory, "decision.csv", lambda rows: rows[0].update(expected_recall_locked_before_reference="false"))
    result = verifier.summarize(directory)
    assert result["reference_recall"] == 5 / 8
    assert result["expected_recall_gap_pp"] is None
    assert result["omission_recognition"] == 1 / 3
    assert result["false_ready_batch_rate"] == 0.75
    mutate(directory, "decision.csv", lambda rows: rows[0].update(findings_locked_before_reference="false"))
    result = verifier.summarize(directory)
    assert result["reference_recall"] is None
    assert result["false_ready_batch_rate"] == 0.75
