import pytest
from pydantic import ValidationError

from hcai_readiness.public_rules import (
    RULES,
    RuleObservation,
    evaluate_public_observation,
    rule_catalog,
)


OFFICIAL_PREFIXES = (
    "docs/research-content.gohtml",
    "docs/claims-and-governance.md",
    "docs/research-boundary.md",
    "docs/agent-tools.md",
    "protocol/0.3-preview.1/",
    "src/hcai_readiness/criteria.json",
)


def test_every_public_rule_is_grounded_only_in_official_hard_sources():
    assert RULES
    for rule in RULES:
        assert rule.official_sources
        assert rule.hard_lenses
        assert rule.hard_criteria
        for source in rule.official_sources:
            assert source.path.startswith(OFFICIAL_PREFIXES)
            assert source.public_href.startswith("/research/ai-readiness") or source.public_href.startswith(
                "/static/research/ai-readiness/"
            )


def test_no_portfolio_or_client_case_principles_leak_into_rule_catalog():
    payload = repr(rule_catalog()).lower()
    for forbidden in (
        "t-mobile",
        "vita",
        "portfolio",
        "recommendations capped at three",
        "color, count",
        "natural language earns its place",
        "case study",
    ):
        assert forbidden not in payload


def test_advisory_rules_are_excluded_from_scored_catalog():
    scored_ids = {row["id"] for row in rule_catalog(scored_only=True)}
    advisory = {rule.id for rule in RULES if not rule.score_included}
    assert advisory
    assert advisory.isdisjoint(scored_ids)
    assert {"DATA-TRUTH-02", "EVID-UNKNOWN-03", "HARD-ASSUMPTION-04", "HARD-CHALLENGE-05", "HARD-NEXT-06"} <= advisory


def test_unknown_remains_unknown_and_names_next_evidence():
    result = evaluate_public_observation(
        RuleObservation(
            rule_id="ACT-REPEAT-02",
            status="unknown",
            evidence_level="unknown",
            next_evidence="Provide the exact repeat/retry check.",
        )
    )
    finding = result["finding"]
    assert finding["status"] == "unknown"
    assert finding["evidence_level"] == "unknown"
    assert finding["next_evidence"] == "Provide the exact repeat/retry check."
    assert result["score_included"] is True


def test_public_warning_produces_developer_trace_from_hard_reasoning():
    result = evaluate_public_observation(
        RuleObservation(
            rule_id="ACT-DEPENDENCY-04",
            status="warning",
            evidence_level="documented",
            evidence_locations=["https://example.test/docs/failures"],
            observed="The docs mention retry but do not define timeout or final-state behavior.",
        )
    )
    trace = result["finding"]["developer_trace"]
    assert "retry" in trace["observed"].lower()
    assert trace["decision_underneath"]
    assert trace["must_be_true"]
    assert trace["if_wrong"]
    assert trace["prove_next"]
    assert "HCAI-3.1" in result["hard_provenance"]["criteria"]


def test_critical_requires_both_supported_failure_mechanism_and_consequence():
    with pytest.raises(ValidationError):
        RuleObservation(
            rule_id="ACT-AUTHORITY-01",
            status="critical",
            evidence_level="public_observation",
            evidence_locations=["https://example.test/action"],
        )

    result = evaluate_public_observation(
        RuleObservation(
            rule_id="ACT-AUTHORITY-01",
            status="critical",
            evidence_level="walkthrough",
            evidence_locations=["synthetic://authority-challenge"],
            observed="An automated action crosses an authority boundary.",
            failure_mechanism="The action can be committed without the required authorization context.",
            consequence="A consequential external state change can be created by an unauthorized actor.",
        )
    )
    assert result["finding"]["status"] == "critical"


def test_noncritical_rule_rejects_critical_label_even_with_evidence():
    with pytest.raises(ValueError):
        evaluate_public_observation(
            RuleObservation(
                rule_id="EXP-TASK-01",
                status="critical",
                evidence_level="walkthrough",
                evidence_locations=["synthetic://task"],
                observed="The task is ambiguous.",
                failure_mechanism="Two actions compete.",
                consequence="A user may choose the wrong flow.",
            )
        )
