"""Validate canonical CSV reviews and recompute results with the shared stage engine.

Usage: python3 Source/verify_example.py [DIRECTORY] [--json] [--templates]
The default directory is Worked-Example. This checks supplied records and arithmetic;
it cannot authenticate evidence, recover a creator's hidden reasoning, or certify safety.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "schemas/csv-contract.json").read_text(encoding="utf-8"))
STAGES = ("specified", "walkthrough", "implemented", "runtime_tested")
KINDS = {"human", "ai-assisted-human", "agent", "synthetic"}
MODES = {"artifact_review", "independent_evaluation"}
SEVERITIES = {"unrated", "minor", "major", "critical"}
SURFACE_KINDS = {"truth", "ownership", "state", "boundary", "contract", "failure_recovery", "time_ordering", "assumption"}
SURFACE_STATUSES = {"supported", "conflicted", "unassessed", "not_applicable"}
CHALLENGE_STATUSES = {"pass", "fail", "unassessed"}
CORE = ("requirements.csv", "recovery.csv", "requirements-brief.csv", "recovery-brief.csv", "decision.csv",
        "choice-review.csv", "decision-surfaces.csv", "challenge-scenarios.csv")


def to_artifact_review(tables: dict[str, list[dict[str, str]]]):
    """Convert validated CSV records to the same contract consumed by MCP/Skill.

    Source/header validation is stdlib-only. Stage recommendations deliberately use
    the installed project's shared engine; there is no parallel CSV gate algorithm.
    A frozen reference defect is distinct from an evaluator-detected finding.
    """
    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
    from hcai_readiness.artifact_review import ArtifactReview
    from hcai_readiness.versions import versions

    d = tables["decision.csv"][0]
    split = lambda value: [v.strip() for v in value.split(";") if v.strip()]
    def checks(name):
        values = []
        ident, flag = ("requirement_id", "mandatory_yes_no") if name == "requirements.csv" else ("scenario_id", "applicable_yes_no")
        for row in tables[name]:
            values.append({"id": row[ident],
                "acceptance_check": row.get("acceptance_check") or row["trigger"] + ": " + row["expected_state_and_preserved_data"],
                "scope": row["scope"] if row[flag] == "yes" or row["scope"] != "current" else "excluded",
                "exclusion_reason": row["exclusion_reason"] or None,
                "current_dependency": row["current_dependency_yes_no"] == "yes",
                **{level: {"status": row[level + "_status"], "evidence_locations": split(row[level + "_evidence_location"]),
                           "reason": row[level + "_reason"] or None} for level in STAGES}})
        return values
    surfaces_by_choice = {}
    for row in tables.get("decision-surfaces.csv", []):
        surfaces_by_choice.setdefault(row["choice_id"], []).append({
            "id": row["surface_id"], "kind": row["surface_kind"], "question": row["question"],
            "current_model": row["current_model"] or None, "status": row["status"],
            "evidence_locations": split(row["evidence_location"]),
            "consequence_if_wrong": row["consequence_if_wrong"] or None,
            "evidence_needed": row["evidence_needed"] or None,
            "revisit_trigger": row["revisit_trigger"] or None, "reason": row["reason"] or None})
    challenges_by_choice = {}
    for row in tables.get("challenge-scenarios.csv", []):
        challenges_by_choice.setdefault(row["choice_id"], []).append({
            "id": row["challenge_id"], "condition": row["condition"], "claim_at_risk": row["claim_at_risk"],
            "expected_behavior_or_invariant": row["expected_behavior_or_invariant"],
            "consequence_if_mishandled": row["consequence_if_mishandled"],
            "affected_check_ids": split(row["requirement_or_scenario_ids"]), "status": row["status"],
            "evidence_locations": split(row["evidence_location"]), "next_evidence": row["next_evidence"] or None})
    choices = []
    for row in tables.get("choice-review.csv", []):
        historical = row["alternative_provenance"] == "historical"
        current = row["current_justification"]
        provenance = "new" if current else {"historical": "documented", "reconstructed": "new", "proposed": "new", "unknown": "unknown"}[row["rationale_provenance"]]
        rationale = current or (row["recorded_rationale"] if provenance != "unknown" else None)
        alternatives = [{"description": text, "evidence_locations": split(row["evidence_location"]) if historical else []} for text in split(row["alternatives"])]
        choices.append({"id": row["choice_id"], "purpose": row["purpose"], "criteria": split(row["selection_criteria"]),
            "observed_choice": row["chosen_approach"] or None, "observed_evidence_locations": split(row["evidence_location"]),
            "historical_alternatives": alternatives if historical else [], "proposed_alternatives": [] if historical else alternatives,
            "rationale": rationale, "rationale_provenance": provenance,
            "rationale_evidence_locations": split(row["current_justification_evidence_location"] if current else row["evidence_location"]) if rationale else [],
            "impacts_and_tradeoffs": split(row["foreseeable_impacts"]), "assumptions": split(row["assumptions"]),
            "affected_check_ids": split(row["requirement_or_scenario_ids"]),
            "engineering_deepening_required": row["engineering_deepening_required_yes_no"] == "yes",
            "deepening_rationale": row["deepening_rationale"],
            "deepening_triggers": split(row["deepening_triggers"]),
            "required_surface_kinds": split(row["required_surface_kinds"]),
            "decision_surfaces": surfaces_by_choice.get(row["choice_id"], []),
            "challenge_scenarios": challenges_by_choice.get(row["choice_id"], []),
            "next_coherent_slice": row["next_coherent_slice"] or None,
            "human_decision": row["disposition"], "human_decision_owner": row["human_owner"] or None,
            "human_decision_evidence_locations": split(row["human_decision_evidence_location"]),
            "verification_evidence_locations": split(row["verification_evidence_location"]),
            "follow_up": row["followup"] or None, "follow_up_owner": row["followup_owner"] or None})
    findings = []
    acceptance = {"matched": "matched_reference", "novel": "novel_accepted", "unsupported": "unsupported", "duplicate": "duplicate", "unresolved": "unresolved"}
    severity = lambda value: "undetermined" if value == "unrated" else value
    for row in tables.get("findings.csv", []):
        accepted = row["adjudication"] in {"matched", "novel"}
        resolution = "remediated" if row["resolution_status"] == "closed" and accepted else "open" if row["resolution_status"] == "closed" else row["resolution_status"]
        findings.append({"id": row["finding_id"], "description": row["observed"], "acceptance": acceptance[row["adjudication"]],
            "scope": {"current": "current", "deferred": "deferred", "excluded": "deferred", "uncertain": "unclear"}[row["scope_status"]],
            "scope_reason": row["rationale"] or None, "proposed_severity": severity(row["proposed_severity"]),
            "adjudicated_severity": severity(row["severity"]), "criterion_or_novel_risk": row["severity_basis"] or None,
            "failure_mechanism": row["failure_mechanism"] or None, "consequence": row["exposure_and_consequence"] or None,
            "evidence_locations": split(row["evidence_location"]), "resolution": resolution,
            "remediation_evidence_locations": split(row["remediation_evidence_location"])})
    matched_refs = {r["reference_id"] for r in tables.get("findings.csv", []) if r["adjudication"] == "matched"}
    for row in tables.get("reference-key.csv", []):
        if row["defect_id"] in matched_refs:
            continue
        findings.append({"id": "reference-" + row["defect_id"], "description": row["deficiency"],
            "acceptance": "matched_reference", "scope": "current", "proposed_severity": row["severity"],
            "adjudicated_severity": row["severity"], "criterion_or_novel_risk": row["criterion_basis"],
            "failure_mechanism": row["failure_mechanism"] or None, "consequence": row["consequence"] or None,
            "evidence_locations": split(row["evidence_location"]), "resolution": "open"})
    return ArtifactReview.model_validate({"versions": versions(), "run_id": d["session_id"],
        "artifact_version": d["artifact_version"], "criterion_version": d["criterion_version"],
        "artifact_population": d["artifact_population"], "artifact_kind": d["artifact_kind"], "stage": d["stage"],
        "mode": d["mode"], "evaluator_kind": d["evaluator_kind"], "criteria_timing": d["criteria_timing"],
        "requirements": checks("requirements.csv"), "recovery": checks("recovery.csv"),
        "zero_recovery_reason": d["zero_recovery_reason"] or None,
        "important_choice_ids": split(d["important_choice_ids"]), "choices": choices, "findings": findings,
        "evaluator_validity": {key: {"true": True, "false": False, "unknown": None}[d[key]] for key in CONTRACT["evaluator_validity_fields"]},
        "judgment_locked_before_reference": {"true": True, "false": False, "unknown": None}[d["judgment_locked_before_reference"]]})


def shared_review(tables):
    record = to_artifact_review(tables)
    from hcai_readiness.artifact_review import review_artifact
    return review_artifact(record)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_csv(directory: Path | str, name: str) -> list[dict[str, str]]:
    """Read a known file, rejecting extra/missing/duplicate headers and ragged rows."""
    path = Path(directory) / name
    require(name in CONTRACT["files"], f"Unknown CSV contract: {name}")
    with path.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        require(reader.fieldnames == CONTRACT["files"][name]["columns"],
                f"{name}: headers must exactly match schemas/csv-contract.json; legacy handoff_status files require migration")
        rows = []
        for index, row in enumerate(reader, start=2):
            require(None not in row and all(v is not None for v in row.values()),
                    f"{name}:{index}: ragged row or unexpected extra column")
            rows.append({k: v.strip() for k, v in row.items()})
    return rows


def unique(rows: list[dict[str, str]], field: str, name: str) -> None:
    ids = [r[field] for r in rows]
    require(all(ids) and len(set(ids)) == len(ids), f"{name}: empty or duplicate {field}")


def yes_no(value: str, label: str) -> None:
    require(value in {"yes", "no"}, f"{label}: use yes or no")


def nonnegative_integer(value: str, label: str) -> int:
    require(value.isdigit(), f"{label}: use a nonnegative integer")
    return int(value)


def validate_scope(row: dict[str, str], name: str) -> None:
    require(row["scope"] in CONTRACT["scopes"], f"{name}: invalid scope")
    yes_no(row["current_dependency_yes_no"], name + ": current_dependency_yes_no")
    require(bool(row["scope_owner"]), f"{name}: scope_owner required")
    if row["scope"] != "current":
        require(bool(row["exclusion_reason"]), f"{name}: deferred/excluded scope needs a reason")
        require(row["current_dependency_yes_no"] == "no", f"{name}: a current dependency cannot be deferred/excluded")


def validate_checks(rows: list[dict[str, str]], name: str) -> None:
    ident, flag = ("requirement_id", "mandatory_yes_no") if name == "requirements.csv" else ("scenario_id", "applicable_yes_no")
    unique(rows, ident, name)
    for row in rows:
        label = name + ":" + row[ident]
        yes_no(row[flag], label + ":" + flag)
        validate_scope(row, label)
        if row[flag] == "no":
            require(bool(row["exclusion_reason"]), label + ": a nonmandatory/nonapplicable item needs an explicit scope reason")
        for stage in STAGES:
            status, location, reason = (row[stage + suffix] for suffix in ("_status", "_evidence_location", "_reason"))
            require(status in CONTRACT["evidence_statuses"], label + f": invalid {stage}_status")
            if status in {"pass", "fail"}:
                require(bool(location), label + f": {stage} {status} needs its own evidence location")
            if status == "not_applicable":
                require(bool(reason), label + f": {stage} not_applicable needs a reason")
        require(row["runtime_tested_status"] != "pass" or row["implemented_status"] == "pass",
                label + ": runtime proof requires the tested implementation to be identified")
        require(bool(row["assessor"]) and bool(row["assessed_at"]), label + ": assessor and assessed_at required")


def validate_brief(rows: list[dict[str, str]], brief: list[dict[str, str]], name: str) -> None:
    ident = "requirement_id" if name.startswith("requirements") else "scenario_id"
    unique(brief, ident, name)
    fields = CONTRACT["files"][name]["columns"]
    expected = {r[ident]: {key: r[key] for key in fields} for r in rows}
    require(expected == {r[ident]: r for r in brief},
            name + ": frozen scope and completed rows differ; retain deleted/unassessed items or record a new scope version")


def in_scope(row: dict[str, str], name: str) -> bool:
    flag = "mandatory_yes_no" if name == "requirements.csv" else "applicable_yes_no"
    return row["scope"] == "current" and row[flag] == "yes"


def check_summary(rows: list[dict[str, str]], name: str, stage: str) -> dict[str, Any]:
    eligible = [row for row in rows if in_scope(row, name)]
    needed = CONTRACT["stages"][stage]
    passed = sum(all(r[s + "_status"] == "pass" for s in needed) for r in eligible)
    failed = sum(any(r[s + "_status"] == "fail" for s in needed) for r in eligible)
    unassessed = len(eligible) - passed - failed
    return {"verified": passed, "failed": failed, "unassessed": unassessed,
            "denominator": len(eligible), "coverage": passed / len(eligible) if eligible else None,
            "excluded_or_deferred": sum(r["scope"] != "current" for r in rows),
            "by_evidence_stage": {s: {status: sum(r[s + "_status"] == status for r in eligible)
                                      for status in CONTRACT["evidence_statuses"]} for s in STAGES}}


def validate_directory(directory: Path | str, allow_empty: bool = False) -> dict[str, list[dict[str, str]]]:
    directory = Path(directory)
    tables = {name: read_csv(directory, name) for name in CONTRACT["files"] if (directory / name).is_file()}
    require(all(name in tables for name in CORE), "Missing core CSV file; copy requirements/recovery, their frozen briefs, and decision.csv from Templates")
    if allow_empty:
        require(all(not rows for rows in tables.values()), "--templates accepts header-only files; use normal validation for completed records")
        return tables
    require(bool(tables["requirements.csv"]), "At least one declared requirement is needed")
    require(len(tables["decision.csv"]) == 1, "decision.csv: exactly one decision per review directory")
    for name in ("requirements.csv", "recovery.csv"):
        validate_checks(tables[name], name)
        brief_name = name.replace(".csv", "-brief.csv")
        validate_brief(tables[name], tables[brief_name], brief_name)
    decision = tables["decision.csv"][0]
    require(decision["artifact_population"] in CONTRACT["artifact_populations"], "decision.csv: invalid artifact_population")
    require(decision["evaluator_kind"] in KINDS, "decision.csv: invalid evaluator_kind")
    require(decision["mode"] in MODES, "decision.csv: invalid mode")
    require(decision["stage"] in CONTRACT["stages"], "decision.csv: invalid stage")
    for field in ("session_id", "artifact_version", "criterion_version", "owner", "decision_date", "reevaluation_trigger"):
        require(bool(decision[field]), f"decision.csv: {field} required")
    for field in ["judgment_locked_before_reference", *CONTRACT["evaluator_validity_fields"]]:
        require(decision[field] in {"true", "false", "unknown"}, f"decision.csv: {field} must be true, false or unknown")
    if decision["expected_recall"]:
        try:
            expected = float(decision["expected_recall"])
        except ValueError as exc:
            raise ValueError("decision.csv: expected_recall must be numeric") from exc
        require(0 <= expected <= 1, "decision.csv: expected_recall outside [0,1]")
    known = {r["requirement_id"] for r in tables["requirements.csv"]} | {r["scenario_id"] for r in tables["recovery.csv"]}
    findings = tables.get("findings.csv", [])
    unique(findings, "finding_id", "findings.csv")
    refs = tables.get("reference-key.csv", [])
    unique(refs, "defect_id", "reference-key.csv")
    ref_ids = {r["defect_id"] for r in refs}
    for row in refs:
        require(row["requirement_or_scenario_id"] in known, "reference-key.csv: unknown requirement/scenario")
        yes_no(row["reference_omission_yes_no"], "reference-key.csv: reference_omission_yes_no")
        require(row["severity"] in SEVERITIES - {"unrated"}, "reference-key.csv: invalid severity")
        require(all(row[f] for f in ("reference_version", "evidence_location", "reference_reviewer", "verified_at", "match_rule")), "reference-key.csv: incomplete reference record")
    for row in findings:
        require(row["session_id"] == decision["session_id"], "findings.csv: wrong session_id")
        require(row["requirement_or_scenario_id"] in known, "findings.csv: unknown requirement/scenario")
        require(row["proposed_severity"] in SEVERITIES and row["severity"] in SEVERITIES, "findings.csv: invalid severity")
        require(row["scope_status"] in {"current", "deferred", "excluded", "uncertain"}, "findings.csv: invalid scope_status")
        require(row["adjudication"] in {"matched", "duplicate", "unsupported", "novel", "unresolved"}, "findings.csv: invalid adjudication")
        require(row["resolution_status"] in {"open", "accepted_risk", "closed"}, "findings.csv: invalid resolution_status")
        require(bool(row["locked_at"]), "findings.csv: locked_at required")
        if row["adjudication"] in {"matched", "duplicate"}:
            require(row["reference_id"] in ref_ids, "findings.csv: unknown reference match")
        if row["adjudication"] in {"matched", "novel"}:
            require(row["scope_status"] == "current", "findings.csv: deferred/uncertain concern cannot be an accepted current defect")
            require(all(row[k] for k in ("evidence_location", "severity_basis", "adjudicator", "adjudicated_at")), "findings.csv: accepted finding needs retained evidence and adjudication")
        if row["severity"] == "critical":
            require(row["scope_status"] == "current" and row["adjudication"] in {"matched", "novel"}, "findings.csv: Critical must be confirmed against current scope")
            require(bool(row["exposure_and_consequence"]) and bool(row["severity_basis"]), "findings.csv: Critical needs exposure, consequence and a severity basis; keyword absence is insufficient")
    for row in tables.get("adjudication.csv", []):
        finding = next((r for r in findings if r["finding_id"] == row["finding_id"]), None)
        require(finding is not None, "adjudication.csv: unknown finding_id")
        require(row["session_id"] == decision["session_id"] and row["reference_id"] == finding["reference_id"] and row["matched_duplicate_unsupported_novel_unresolved"] == finding["adjudication"], "adjudication.csv: conflicts with findings.csv")
    choices = tables.get("choice-review.csv", [])
    unique(choices, "choice_id", "choice-review.csv")
    choice_ids = {row["choice_id"] for row in choices}
    surfaces = tables.get("decision-surfaces.csv", [])
    surface_keys = [(row["choice_id"], row["surface_id"]) for row in surfaces]
    require(all(a and b for a, b in surface_keys) and len(surface_keys) == len(set(surface_keys)),
            "decision-surfaces.csv: empty or duplicate choice_id/surface_id")
    challenges = tables.get("challenge-scenarios.csv", [])
    challenge_keys = [(row["choice_id"], row["challenge_id"]) for row in challenges]
    require(all(a and b for a, b in challenge_keys) and len(challenge_keys) == len(set(challenge_keys)),
            "challenge-scenarios.csv: empty or duplicate choice_id/challenge_id")
    for row in surfaces:
        require(row["choice_id"] in choice_ids, "decision-surfaces.csv: unknown choice_id")
        require(row["surface_kind"] in SURFACE_KINDS, "decision-surfaces.csv: invalid surface_kind")
        require(row["status"] in SURFACE_STATUSES, "decision-surfaces.csv: invalid status")
        require(bool(row["question"]), "decision-surfaces.csv: question required")
        if row["status"] in {"supported", "conflicted"}:
            require(bool(row["current_model"]) and bool(row["evidence_location"]),
                    "decision-surfaces.csv: supported/conflicted needs current_model and evidence")
        if row["status"] == "unassessed":
            require(bool(row["evidence_needed"]), "decision-surfaces.csv: unassessed needs evidence_needed")
        if row["status"] == "not_applicable":
            require(bool(row["reason"]), "decision-surfaces.csv: not_applicable needs reason")
        if row["surface_kind"] == "assumption" and row["status"] != "not_applicable":
            require(all(row[k] for k in ("consequence_if_wrong", "evidence_needed", "revisit_trigger")),
                    "decision-surfaces.csv: assumptions need consequence, evidence needed and revisit trigger")
    for row in challenges:
        require(row["choice_id"] in choice_ids, "challenge-scenarios.csv: unknown choice_id")
        require(row["status"] in CHALLENGE_STATUSES, "challenge-scenarios.csv: invalid status")
        require(all(row[k] for k in ("condition", "claim_at_risk", "expected_behavior_or_invariant", "consequence_if_mishandled")),
                "challenge-scenarios.csv: condition, claim, invariant and consequence required")
        require(all(ref in known for ref in row["requirement_or_scenario_ids"].split(";") if ref),
                "challenge-scenarios.csv: unknown requirement/scenario")
        if row["status"] in {"pass", "fail"}:
            require(bool(row["evidence_location"]), "challenge-scenarios.csv: assessed challenge needs evidence")
        if row["status"] == "unassessed":
            require(bool(row["next_evidence"]), "challenge-scenarios.csv: unassessed challenge needs next_evidence")
    for row in choices:
        require(row["alternative_provenance"] in {"historical", "reconstructed", "proposed", "unknown"}, "choice-review.csv: invalid alternative_provenance")
        require(row["rationale_provenance"] in {"historical", "reconstructed", "proposed", "unknown"}, "choice-review.csv: invalid rationale_provenance")
        require(row["criteria_provenance"] in {"historical", "reconstructed", "proposed", "unknown"}, "choice-review.csv: invalid criteria_provenance")
        require(row["disposition"] in {"accepted", "revise", "pending"}, "choice-review.csv: invalid human disposition")
        yes_no(row["engineering_deepening_required_yes_no"], "choice-review.csv: engineering_deepening_required_yes_no")
        require(all(row[k] for k in ("purpose", "selection_criteria", "assumptions", "deepening_rationale",
                                     "human_owner", "disposition", "followup", "followup_owner")),
                "choice-review.csv: purpose, criteria, assumptions, deepening rationale, human owner and follow-up required")
        if row["engineering_deepening_required_yes_no"] == "yes":
            require(bool(row["deepening_triggers"]) and bool(row["required_surface_kinds"]) and bool(row["next_coherent_slice"]),
                    "choice-review.csv: required deepening needs triggers, surface kinds and next coherent slice")
            required_kinds = {value.strip() for value in row["required_surface_kinds"].split(";") if value.strip()}
            require(required_kinds <= SURFACE_KINDS, "choice-review.csv: invalid required_surface_kinds")
            active_kinds = {s["surface_kind"] for s in surfaces if s["choice_id"] == row["choice_id"] and s["status"] != "not_applicable"}
            require(required_kinds <= active_kinds, "choice-review.csv: missing required decision surface")
            require(any(ch["choice_id"] == row["choice_id"] for ch in challenges),
                    "choice-review.csv: required deepening needs a challenge scenario")
        if "historical" in {row["alternative_provenance"], row["rationale_provenance"], row["criteria_provenance"]}:
            require(bool(row["evidence_location"]), "choice-review.csv: historical claims require contemporaneous evidence")
        if row["disposition"] in {"accepted", "revise"}:
            require(bool(row["human_decision_evidence_location"]), "choice-review.csv: accepted/revise decisions require retained human confirmation")
        require(all(ref in known for ref in row["requirement_or_scenario_ids"].split(";") if ref), "choice-review.csv: unknown requirement/scenario")
    batch = tables.get("batch.csv", [])
    unique(batch, "assessment_id", "batch.csv")
    for row in batch:
        require(row["artifact_population"] in CONTRACT["artifact_populations"] and row["artifact_population"] != "unknown", "batch.csv: unknown artifact population cannot be pooled")
        require(row["evaluator_kind"] in KINDS and row["mode"] in MODES and row["stage"] in CONTRACT["stages"], "batch.csv: invalid population/mode/stage")
        require(row["criterion_status"] in {"ready", "nonready", "unknown"}, "batch.csv: invalid criterion_status")
        require(row["evaluator_judgment"] in {"ready", "not_ready", "unable_to_assess", "missing"}, "batch.csv: invalid evaluator_judgment")
    strata = {(r["criterion_version"], r["evaluator_kind"], r["artifact_population"], r["mode"], r["stage"]) for r in batch}
    require(len(strata) <= 1, "batch.csv: stratify different criteria, evaluators, artifact populations, modes and stages before pooling")
    if strata:
        require(next(iter(strata)) == tuple(decision[k] for k in ("criterion_version", "evaluator_kind", "artifact_population", "mode", "stage")), "batch.csv: stratum differs from the decision record")
    summaries = [check_summary(tables[name], name, decision["stage"]) for name in ("requirements.csv", "recovery.csv")]
    require(summaries[0]["denominator"] > 0, "No current mandatory requirements; a review without a decision scope cannot pass")
    unassessed = sum(r["unassessed"] for r in summaries)
    require(nonnegative_integer(decision["mandatory_unassessed"], "decision.csv: mandatory_unassessed") == unassessed, "decision.csv: unassessed count disagrees with retained current checks")
    critical = nonnegative_integer(decision["critical_open"], "decision.csv: critical_open")
    evaluated = shared_review(tables)
    require(critical == len(evaluated["unresolved_critical_ids"]), "decision.csv: unresolved confirmed Critical count disagrees with retained findings/reference evidence")
    require(decision["disposition"] == evaluated["disposition"], f'decision.csv: disposition must be {evaluated["disposition"]!r}')
    return tables


def summarize(directory: Path | str) -> dict[str, Any]:
    tables = validate_directory(directory)
    decision = tables["decision.csv"][0]
    result: dict[str, Any] = {"csv_contract_version": CONTRACT["contract_version"],
                             **{k: decision[k] for k in ("session_id", "artifact_population", "evaluator_kind", "mode", "stage", "disposition")},
                             "requirements": check_summary(tables["requirements.csv"], "requirements.csv", decision["stage"]),
                             "recovery": check_summary(tables["recovery.csv"], "recovery.csv", decision["stage"]),
                             "critical_open": int(decision["critical_open"]),
                             "reference_recall": None, "expected_recall_gap_pp": None,
                             "omission_recognition": None, "false_ready_batch_rate": None,
                             "warnings": [], "claim_limit": "Record validation and synthetic/descriptive arithmetic only; no evidence authentication, empirical effectiveness, or deployment authorization."}
    record = to_artifact_review(tables)
    from hcai_readiness.artifact_review import evaluator_metric_reasons
    reasons = evaluator_metric_reasons(record.evaluator_validity, record.mode, record.judgment_locked_before_reference)
    result["stage_review"] = shared_review(tables)
    result["metric_ineligibility_reasons"] = reasons
    eligible = not reasons["reference_set_recall_percent"] and decision["evaluator_kind"] != "agent"
    refs = tables.get("reference-key.csv", [])
    if eligible and refs:
        ids = {r["defect_id"] for r in refs}
        matched = {r["reference_id"] for r in tables.get("findings.csv", []) if r["adjudication"] == "matched"}
        omissions = {r["defect_id"] for r in refs if r["reference_omission_yes_no"] == "yes"}
        result["reference_recall"] = len(matched) / len(ids)
        result["expected_recall_gap_pp"] = (float(decision["expected_recall"]) - result["reference_recall"]) * 100 if decision["expected_recall"] and not reasons["expected_recall_gap_pp"] else None
        result["omission_recognition"] = len(matched & omissions) / len(omissions) if omissions and not reasons["requirements_omission_recognition_percent"] else None
    else:
        result["warnings"].append("Reference-recall metrics are unavailable: inspect per-metric mode, role, exposure, ordering and reference-key reasons.")
    batch = tables.get("batch.csv", [])
    observed = [r for r in batch if r["criterion_status"] == "nonready" and r["evaluator_judgment"] != "missing"]
    result["false_ready_batch_rate"] = sum(r["evaluator_judgment"] == "ready" for r in observed) / len(observed) if observed and not reasons["false_ready_acceptance_percent"] and decision["evaluator_kind"] != "agent" else None
    result["batch_nonready_missing_judgments"] = sum(r["criterion_status"] == "nonready" and r["evaluator_judgment"] == "missing" for r in batch)
    if decision["evaluator_kind"] == "synthetic":
        result["warnings"].append("All observations and evaluator metrics in this example are stipulated synthetic values, not human participant results.")
    if decision["evaluator_kind"] == "agent":
        result["warnings"].append("Agent-assisted artifact findings must not be pooled with human evaluator performance.")
    if decision["artifact_population"] == "unknown":
        result["warnings"].append("Resolve artifact_population before any pooled comparison.")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=ROOT / "Worked-Example")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable descriptive summary")
    parser.add_argument("--artifact-json", action="store_true", help="Export the canonical ArtifactReview consumed by MCP/Skill")
    parser.add_argument("--templates", action="store_true", help="Validate header-only templates, not a completed assessment")
    args = parser.parse_args()
    try:
        if args.templates:
            validate_directory(args.directory, allow_empty=True)
            print("Canonical template headers verified. Empty templates are not assessment evidence.")
        else:
            if args.artifact_json:
                print(to_artifact_review(validate_directory(args.directory)).model_dump_json(indent=2))
                return 0
            result = summarize(args.directory)
            if args.json:
                print(json.dumps(result, indent=2, allow_nan=False))
            else:
                for key in ("requirements", "recovery"):
                    r = result[key]
                    print(f'{key}: {r["verified"]}/{r["denominator"]} verified; {r["failed"]} failed; {r["unassessed"]} unassessed')
                for key in ("reference_recall", "expected_recall_gap_pp", "omission_recognition", "false_ready_batch_rate"):
                    print(f'{key}: {result[key] if result[key] is not None else "N/A"}')
                print(result["disposition"])
                print(result["claim_limit"])
                for warning in result["warnings"]:
                    print("Warning: " + warning)
    except ModuleNotFoundError as exc:
        parser.exit(2, f"Missing installed project dependency ({exc.name}). Install this project or use its .venv/bin/python. Header-only --templates validation needs only Python standard library.\n")
    except (ValueError, FileNotFoundError) as exc:
        parser.exit(2, f"Invalid review: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
