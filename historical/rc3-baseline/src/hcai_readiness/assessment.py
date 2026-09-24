"""Descriptive calculations, not empirical validation or an approval system."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, StrictInt, model_validator

Count = StrictInt

class Counts(BaseModel):
    model_config = ConfigDict(extra="forbid")

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
    evaluator_kind: Literal["human", "ai-assisted-human", "agent", "synthetic"]
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

def calculate_session(s: Session) -> dict:
    missing = [k for k in ("requirements", "recovery", "unresolved_critical", "evidence_complete")
               if getattr(s, k) is None]
    checks = [x for x in (s.requirements, s.recovery) if x is not None]
    failed = any(x.failed > 0 for x in checks) or (s.unresolved_critical or 0) > 0
    incomplete = s.evidence_complete is False or any(x.unassessed > 0 for x in checks)
    if failed:
        status, disposition = "nonready", "Hold for remediation"
    elif incomplete:
        status, disposition = "nonready", "Insufficient evidence"
    elif missing:
        status, disposition = "unknown", "Not evaluated"
    else:
        status, disposition = "ready", "Eligible for handoff review"
    recall = ratio(s.detected_reference_defects, s.reference_defects)
    warnings = []
    if not s.judgment_locked_before_reference:
        warnings.append("Judgment was not locked before reference disclosure; exclude from protocol-compliant evaluator comparisons.")
    if s.evaluator_kind in ("agent", "synthetic"):
        warnings.append("This is not an observed human evaluation. Do not pool it with human results.")
    return {
        "software_version": "0.1.0", "protocol_version": "0.1-rc.3",
        "protocol_doi": "10.5281/zenodo.22667623", "session_id": s.session_id,
        "evaluator_kind": s.evaluator_kind,
        "metrics": {
            "reference_set_recall_percent": recall,
            "expected_recall_gap_pp": None if recall is None or s.expected_recall_percent is None else round(s.expected_recall_percent - recall, 6),
            "requirements_omission_recognition_percent": ratio(s.detected_reference_omissions, s.reference_omissions),
            "artifact_requirements_coverage_percent": None if s.requirements is None else ratio(s.requirements.verified, s.requirements.total),
            "handoff_recovery_coverage_percent": None if s.recovery is None else ratio(s.recovery.verified, s.recovery.total),
        },
        "criterion_status": status, "disposition": disposition, "missing_gate_fields": missing,
        "inputs": s.model_dump(), "warnings": warnings,
        "interpretation": "Descriptive calculation from supplied adjudicated counts. Null metrics mean N/A, not zero. Reference quality, records and owner approval require human review; this is not production certification.",
    }

class Judgment(Counts):
    instance_id: str = Field(min_length=1)
    artifact_version: str = Field(min_length=1)
    criterion_version: str = Field(min_length=1)
    evaluator_kind: Literal["human", "ai-assisted-human", "agent", "synthetic"]
    criterion_status: Literal["ready", "nonready", "unknown"]
    judgment: Literal["Ready", "Not ready", "Unable to assess"] | None

def summarize_judgments(records: list[Judgment]) -> dict:
    if not records:
        raise ValueError("Supply at least one assessment instance")
    if len({r.instance_id for r in records}) != len(records):
        raise ValueError("Duplicate instance IDs")
    if len({(r.criterion_version, r.evaluator_kind) for r in records}) != 1:
        raise ValueError("Stratify different criteria and evaluator populations before calculation")
    result = {"instances": len(records), "unknown_criterion_count": sum(r.criterion_status == "unknown" for r in records)}
    for status in ("nonready", "ready"):
        group = [r for r in records if r.criterion_status == status]
        counts = {j: sum(r.judgment == j for r in group) for j in ("Ready", "Not ready", "Unable to assess")}
        observed = sum(counts.values())
        decisive = counts["Ready"] + counts["Not ready"]
        error = counts["Ready" if status == "nonready" else "Not ready"]
        result[status] = {
            "instances": len(group), "observed": observed, "missing": len(group) - observed,
            "counts": counts, "abstention_percent": ratio(counts["Unable to assess"], observed),
            "decision_coverage_percent": ratio(decisive, observed),
            "false_ready_acceptance_percent" if status == "nonready" else "false_hold_percent": ratio(error, observed),
            "decisive_false_ready_acceptance_percent" if status == "nonready" else "decisive_false_hold_percent": ratio(error, decisive),
        }
    result["interpretation"] = "Descriptive instance counts only; repeated evaluators or artifacts are not independent samples. Zero false acceptance with universal abstention is not useful discrimination."
    return result
