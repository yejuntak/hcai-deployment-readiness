"""Current corrected diagnostics; the frozen rc.3 implementation remains historical.

Legacy-shaped counts support descriptive diagnostics only. Missing role/order facts
make evaluator measures N/A; no population, stage or mode is silently inferred.
"""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, StrictInt, model_validator
from .artifact_review import ArtifactPopulation, EvaluatorKind, EvaluatorValidity, evaluator_metric_reasons
from .versions import versions

Count = StrictInt
LegacyMode = Literal["artifact_review", "independent_evaluation", "legacy_diagnostic"]
LegacyStage = Literal["specification_handoff", "prototype_handoff", "implementation_review", "runtime_release_review", "unspecified"]


class Counts(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)

    @model_validator(mode="after")
    def nonnegative(self):
        for name, value in self.__dict__.items():
            if isinstance(value, int) and not isinstance(value, bool) and value < 0:
                raise ValueError(f"{name} must be nonnegative")
        return self


class Checks(Counts):
    total: Count
    verified: Count
    failed: Count
    unassessed: Count

    @model_validator(mode="after")
    def reconcile(self):
        if self.verified + self.failed + self.unassessed != self.total:
            raise ValueError("verified + failed + unassessed must equal total")
        return self


class Session(Counts):
    session_id: str = Field(min_length=1)
    artifact_version: str = Field(min_length=1)
    criterion_version: str = Field(min_length=1)
    artifact_population: ArtifactPopulation
    stage: LegacyStage = "unspecified"
    mode: LegacyMode = "legacy_diagnostic"
    evaluator_kind: EvaluatorKind
    evaluator_validity: EvaluatorValidity = Field(default_factory=EvaluatorValidity)
    reference_defects: Count | None
    detected_reference_defects: Count | None
    reference_omissions: Count | None
    detected_reference_omissions: Count | None
    expected_recall_percent: float | None = Field(ge=0, le=100, allow_inf_nan=False)
    requirements: Checks | None
    recovery: Checks | None
    zero_recovery_reason: str | None = None
    unresolved_critical: Count | None
    evidence_complete: bool | None
    judgment: Literal["Ready", "Not ready", "Unable to assess"] | None
    judgment_locked_before_reference: bool
    reference_basis: str = Field(min_length=1)
    unsupported_findings: Count
    duplicate_findings: Count
    novel_genuine_findings: Count
    unresolved_findings: Count
    elapsed_minutes: float | None = Field(ge=0, allow_inf_nan=False)

    @model_validator(mode="after")
    def consistency(self):
        d, h, o, m = (self.reference_defects, self.detected_reference_defects,
                       self.reference_omissions, self.detected_reference_omissions)
        for numerator, denominator in [(h, d), (m, o), (o, d), (m, h)]:
            if numerator is not None and denominator is not None and numerator > denominator:
                raise ValueError("Reference and detection counts are inconsistent")
        if all(x is not None for x in (d, h, o, m)) and h - m > d - o:
            raise ValueError("Detected non-omissions exceed reference non-omissions")
        if self.recovery is not None and self.recovery.total == 0 and not (self.zero_recovery_reason or "").strip():
            raise ValueError("Zero applicable recovery scenarios require an applicability reason")
        if self.requirements is not None and self.requirements.total == 0:
            raise ValueError("Define at least one mandatory requirement for this assessment")
        return self


def ratio(n, d):
    return None if n is None or d is None or d == 0 else round(100 * n / d, 6)


def _count_reasons(numerator, denominator):
    if numerator is None or denominator is None:
        return ["reference_counts_missing"]
    return ["zero_denominator"] if denominator == 0 else []


def calculate_session(s: Session) -> dict:
    missing = [k for k in ("requirements", "recovery", "unresolved_critical", "evidence_complete")
               if getattr(s, k) is None]
    if s.stage == "unspecified":
        missing.append("stage")
    if s.artifact_population == "unknown":
        missing.append("artifact_population")
    if s.mode == "legacy_diagnostic":
        missing.append("mode")
    checks = [x for x in (s.requirements, s.recovery) if x is not None]
    failed = any(x.failed > 0 for x in checks) or (s.unresolved_critical or 0) > 0
    incomplete = s.evidence_complete is False or any(x.unassessed > 0 for x in checks) or s.unresolved_findings > 0
    if failed:
        status, disposition = "nonready", "Hold for remediation"
    elif incomplete:
        status, disposition = "nonready", "Insufficient evidence"
    elif missing:
        status, disposition = "unknown", "Not evaluated"
    else:
        status, disposition = "ready", "Aggregate checks satisfied; stage handoff not established"
    reasons = evaluator_metric_reasons(s.evaluator_validity, s.mode, s.judgment_locked_before_reference)
    reasons["reference_set_recall_percent"] += _count_reasons(s.detected_reference_defects, s.reference_defects)
    reasons["expected_recall_gap_pp"] += _count_reasons(s.detected_reference_defects, s.reference_defects)
    if s.expected_recall_percent is None:
        reasons["expected_recall_gap_pp"].append("expectation_missing")
    reasons["requirements_omission_recognition_percent"] += _count_reasons(s.detected_reference_omissions, s.reference_omissions)
    if s.artifact_population == "unknown" or s.stage == "unspecified":
        for codes in reasons.values():
            codes.append("comparison_stratum_unspecified")
    recall = None if reasons["reference_set_recall_percent"] else ratio(s.detected_reference_defects, s.reference_defects)
    gap = None if reasons["expected_recall_gap_pp"] else round(s.expected_recall_percent - recall, 6)
    omissions = None if reasons["requirements_omission_recognition_percent"] else ratio(s.detected_reference_omissions, s.reference_omissions)
    warnings = []
    if not s.judgment_locked_before_reference:
        warnings.append("Judgment was not locked before reference disclosure; exclude that judgment from independent evaluator comparisons.")
    if s.evaluator_kind in ("agent", "synthetic"):
        warnings.append("This is not an observed human evaluation. Do not pool it with human results.")
    if s.mode == "legacy_diagnostic" or s.stage == "unspecified":
        warnings.append("Legacy mode/stage is unspecified. Migrate explicitly before a stage handoff claim or pooled comparison.")
    if any(reasons[k] for k in ("reference_set_recall_percent", "expected_recall_gap_pp", "requirements_omission_recognition_percent")):
        warnings.append("Ineligible evaluator measures are null with reason codes; artifact coverage remains a descriptive measure.")
    return {
        "software_version": versions()["mcp"], "protocol_version": versions()["protocol"],
        "historical_protocol_reference": {"version": "0.1-rc.3", "doi": "10.5281/zenodo.22667623"},
        "compatibility": "Current corrected diagnostic contract, not frozen rc.3 reproduction; population and role/order eligibility are enforced.",
        "session_id": s.session_id, "evaluator_kind": s.evaluator_kind,
        "artifact_population": s.artifact_population, "stage": s.stage, "mode": s.mode,
        "metrics": {
            "reference_set_recall_percent": recall,
            "expected_recall_gap_pp": gap,
            "requirements_omission_recognition_percent": omissions,
            "artifact_requirements_coverage_percent": None if s.requirements is None else ratio(s.requirements.verified, s.requirements.total),
            "handoff_recovery_coverage_percent": None if s.recovery is None else ratio(s.recovery.verified, s.recovery.total),
        },
        "metric_ineligibility_reasons": reasons,
        "criterion_status": status, "criterion_scope": "supplied_aggregate_checks",
        "stage_handoff_eligibility": None, "disposition": disposition, "missing_gate_fields": missing,
        "inputs": s.model_dump(), "warnings": warnings,
        "interpretation": "Descriptive calculation from supplied adjudicated counts. Null metrics mean N/A, not zero. Use artifact review for four-level evidence and choice records; this aggregate diagnostic does not establish engineering or release eligibility. Role/order assertions, reference quality and owner approval need human review; this is not production certification or an effect estimate.",
    }


class Judgment(Counts):
    instance_id: str = Field(min_length=1)
    artifact_version: str = Field(min_length=1)
    criterion_version: str = Field(min_length=1)
    artifact_population: ArtifactPopulation
    stage: LegacyStage = "unspecified"
    mode: LegacyMode = "legacy_diagnostic"
    evaluator_kind: EvaluatorKind
    evaluator_validity: EvaluatorValidity = Field(default_factory=EvaluatorValidity)
    judgment_locked_before_reference: bool | None = None
    criterion_status: Literal["ready", "nonready", "unknown"]
    judgment: Literal["Ready", "Not ready", "Unable to assess"] | None


def _judgment_group(records: list[Judgment], status: str) -> dict:
    group = [r for r in records if r.criterion_status == status]
    counts = {j: sum(r.judgment == j for r in group) for j in ("Ready", "Not ready", "Unable to assess")}
    observed = sum(counts.values())
    decisive = counts["Ready"] + counts["Not ready"]
    error = counts["Ready" if status == "nonready" else "Not ready"]
    return {"instances": len(group), "observed": observed, "missing": len(group) - observed,
            "counts": counts, "abstention_percent": ratio(counts["Unable to assess"], observed),
            "decision_coverage_percent": ratio(decisive, observed),
            "false_ready_acceptance_percent" if status == "nonready" else "false_hold_percent": ratio(error, observed),
            "decisive_false_ready_acceptance_percent" if status == "nonready" else "decisive_false_hold_percent": ratio(error, decisive)}


def summarize_judgments(records: list[Judgment]) -> dict:
    if not records:
        raise ValueError("Supply at least one assessment instance")
    if len({r.instance_id for r in records}) != len(records):
        raise ValueError("Duplicate instance IDs")
    if any(r.artifact_population == "unknown" or r.stage == "unspecified" or r.mode == "legacy_diagnostic" for r in records):
        raise ValueError("Explicit artifact population, stage and mode are required before batch calculation")
    if len({(r.criterion_version, r.evaluator_kind, r.artifact_population, r.stage, r.mode) for r in records}) != 1:
        raise ValueError("Stratify different criteria, evaluator populations, artifact populations, stages and modes before calculation")
    excluded = []
    eligible = []
    for row in records:
        reasons = evaluator_metric_reasons(row.evaluator_validity, row.mode, row.judgment_locked_before_reference)["false_ready_acceptance_percent"]
        if reasons:
            excluded.append({"instance_id": row.instance_id, "reasons": reasons})
        else:
            eligible.append(row)
    first = records[0]
    result = {"versions": versions(), "instances": len(records),
              "artifact_population": first.artifact_population, "stage": first.stage, "mode": first.mode,
              "criterion_version": first.criterion_version, "evaluator_kind": first.evaluator_kind,
              "unknown_criterion_count": sum(r.criterion_status == "unknown" for r in records),
              "eligible_instances": len(eligible), "ineligible_instances": len(excluded), "excluded": excluded,
              "descriptive_counts": {status: {key: value for key, value in _judgment_group(records, status).items()
                                          if key not in ("false_ready_acceptance_percent", "false_hold_percent",
                                                         "decisive_false_ready_acceptance_percent", "decisive_false_hold_percent")}
                                     for status in ("nonready", "ready")}}
    for status in ("nonready", "ready"):
        result[status] = _judgment_group(eligible, status)
    result["interpretation"] = "Evaluator error rates use only eligible locked, independent judgments. All supplied observations remain in descriptive_counts and excluded records remain visible. Descriptive instance counts are not an effect estimate; repeated evaluators or artifacts are not independent samples. Zero false acceptance with universal abstention is not useful discrimination."
    return result
