from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_product_signal_prototype_keeps_one_job_and_one_primary_action():
    page = (ROOT / "docs/product-signal-prototype.html").read_text()
    assert "Your product" in page
    assert "looks done." in page
    assert "Grade my product" in page
    assert page.count('class="scan"') == 1
    assert "No signup required" in page


def test_prototype_keeps_hard_separate_from_numeric_grade():
    page = (ROOT / "docs/product-signal-prototype.html").read_text()
    assert "78 / 100" in page
    assert "EVIDENCE NEEDED" in page
    assert "not a H.A.R.D. protocol score" in page
    assert "H.A.R.D. Score" not in page


def test_prototype_contains_developer_debugging_sequence():
    page = (ROOT / "docs/product-signal-prototype.html").read_text()
    for label in ("Observed", "Decision underneath", "What must be true?", "If it fails", "Prove next"):
        assert label in page
    assert "Duplicate refund protection is not demonstrated." in page


def test_prototype_does_not_turn_unknown_into_failure():
    page = (ROOT / "docs/product-signal-prototype.html").read_text()
    assert "unknowns were not counted as failures" in page
    assert "Evidence confidence" in page
    assert "Coverage" in page


def test_benchmark_rejects_dashboard_and_fake_proof_patterns():
    benchmark = (ROOT / "docs/product-signal-benchmark.md").read_text()
    assert "looks like a compliance dashboard" in benchmark
    assert "fake benchmark/social proof" in benchmark
    assert "requires an LLM to render the report" in benchmark
    assert "what changed?" in benchmark
