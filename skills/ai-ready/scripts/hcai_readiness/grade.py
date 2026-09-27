"""Deterministic external report grade for H.A.R.D.-adjacent product reviews.

This module intentionally does NOT produce a H.A.R.D. protocol score.

The public-facing report has two independent layers:

1. Product Signal Grade: one simple letter/0-100 triage score built only from
   externally scorable product-surface modules.
2. H.A.R.D. Decision Posture: the non-compensatory protocol result. It is never
   converted to points and never averaged with accessibility, privacy, or other
   modules.

That separation preserves the H.A.R.D. 0.3 rule that gate outcomes, evidence
coverage, operating burden, evaluator measures, and actual system performance
must not be compressed into a weighted readiness percentage.

Unknown findings do not silently fail. They reduce evidence confidence/coverage.
The calculator and renderer are pure/deterministic: no network or model call is
required, which keeps batch report generation cheap.
"""
from __future__ import annotations

import html
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ModuleId = Literal[
    "accessibility",
    "action_recovery",
    "privacy_data",
    "ai_transparency",
    "public_evidence",
]
FindingStatus = Literal["pass", "warning", "critical", "unknown"]
ReportEvidenceLevel = Literal[
    "unknown",
    "public_observation",
    "documented",
    "walkthrough",
    "implemented",
    "runtime_tested",
]
HardRoute = Literal["not_reviewed", "artifact_review", "engineering_commitment"]
HardDisposition = Literal[
    "not_reviewed",
    "insufficient_evidence",
    "hold_for_remediation",
    "eligible_for_declared_stage_handoff_review",
    "proceed_to_engineering",
    "revise_before_engineering",
]
HardEvidenceCeiling = Literal[
    "unknown",
    "specified",
    "walkthrough",
    "implemented",
    "runtime_tested",
]

# Only comparable public/product-surface signals are scored.
# H.A.R.D. itself is deliberately absent from this table.
MODULES: dict[str, dict[str, object]] = {
    "accessibility": {"label": "Accessibility", "weight": 25},
    "action_recovery": {"label": "Action & Recovery", "weight": 25},
    "privacy_data": {"label": "Privacy & Data Boundary", "weight": 20},
    "ai_transparency": {"label": "AI Transparency & Claims", "weight": 20},
    "public_evidence": {"label": "Public Evidence & Documentation", "weight": 10},
}

STATUS_FACTOR = {
    "pass": 1.0,
    "warning": 0.5,
    "critical": 0.0,
}

REPORT_EVIDENCE_CONFIDENCE = {
    "unknown": 0.0,
    "public_observation": 0.25,
    "documented": 0.45,
    "walkthrough": 0.65,
    "implemented": 0.80,
    "runtime_tested": 1.0,
}

BLOCKING_HARD_DISPOSITIONS = {
    "hold_for_remediation",
    "revise_before_engineering",
}

EVIDENCE_NEEDED_HARD_DISPOSITIONS = {
    "insufficient_evidence",
}


class DeveloperTrace(BaseModel):
    """Compact product-engineering reasoning attached to an evidence-backed finding.

    This is a present-day review model, not reconstructed private chain-of-thought.
    It can be populated from deterministic rule text; no model call is required.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    observed: str = Field(min_length=1)
    decision_underneath: str = Field(min_length=1)
    must_be_true: str = Field(min_length=1)
    if_wrong: str = Field(min_length=1)
    prove_next: str = Field(min_length=1)


class ReportFinding(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(min_length=1)
    module: ModuleId
    title: str = Field(min_length=1)
    status: FindingStatus
    evidence_level: ReportEvidenceLevel
    weight: float = Field(default=1.0, gt=0, le=100, allow_inf_nan=False)
    summary: str = ""
    evidence_locations: list[str] = Field(default_factory=list)
    next_evidence: str | None = None
    developer_trace: DeveloperTrace | None = None

    @model_validator(mode="after")
    def evidence_boundary(self):
        if self.status == "unknown":
            if self.evidence_level != "unknown":
                raise ValueError("Unknown findings must use evidence_level=unknown")
            if not self.next_evidence:
                raise ValueError("Unknown findings must name the evidence needed next")
        else:
            if self.evidence_level == "unknown":
                raise ValueError("Assessed findings require a non-unknown evidence level")
            if not self.evidence_locations:
                raise ValueError("Assessed findings require retained evidence locations")
        return self


class HardPosture(BaseModel):
    """A display-safe projection of a real H.A.R.D. result, never a score."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    route: HardRoute = "not_reviewed"
    disposition: HardDisposition = "not_reviewed"
    evidence_ceiling: HardEvidenceCeiling = "unknown"
    blocker_ids: list[str] = Field(default_factory=list)
    summary: str = ""

    @model_validator(mode="after")
    def route_and_disposition_match(self):
        if self.route == "not_reviewed" and self.disposition != "not_reviewed":
            raise ValueError("A non-reviewed H.A.R.D. route cannot claim a disposition")
        if self.route != "not_reviewed" and self.disposition == "not_reviewed":
            raise ValueError("A reviewed H.A.R.D. route needs a disposition")
        return self


class HardPriority(BaseModel):
    """One display priority projected from an actual H.A.R.D. review record.

    No numeric contribution is assigned. The priority exists to ensure a protocol
    blocker or evidence gap is never subordinated to a product-surface score.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    evidence_locations: list[str] = Field(min_length=1)
    next_evidence: str = Field(min_length=1)
    developer_trace: DeveloperTrace | None = None


class AuxiliaryScore(BaseModel):
    """Optional growth/visibility score, explicitly excluded from the overall grade."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    label: str = Field(min_length=1)
    score: int = Field(ge=0, le=100)
    note: str = ""


class ReportGradeInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    subject: str = Field(min_length=1)
    product: str | None = None
    reviewed_surface: str = Field(min_length=1)
    findings: list[ReportFinding] = Field(min_length=1)
    hard: HardPosture = Field(default_factory=HardPosture)
    hard_priority: HardPriority | None = None
    auxiliary_scores: list[AuxiliaryScore] = Field(default_factory=list)

    @model_validator(mode="after")
    def unique_ids(self):
        ids = [finding.id for finding in self.findings]
        if len(ids) != len(set(ids)):
            raise ValueError("Finding IDs must be unique")
        labels = [score.label.lower() for score in self.auxiliary_scores]
        if len(labels) != len(set(labels)):
            raise ValueError("Auxiliary score labels must be unique")
        if self.hard_priority is not None and self.hard.route == "not_reviewed":
            raise ValueError("A H.A.R.D. priority requires an actual H.A.R.D. review route")
        return self


def grade_letter(score: int) -> str:
    """Simple report bands. These are not H.A.R.D. protocol outcomes."""
    if score >= 95:
        return "A+"
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "F"


def _confidence_label(value: int) -> str:
    if value >= 80:
        return "High"
    if value >= 50:
        return "Medium"
    return "Limited"


def _surface_verdict(letter: str) -> str:
    return {
        "A+": "Very strong signals across the reviewed surface.",
        "A": "Strong signals across the reviewed surface.",
        "B": "Good surface signals, with important gaps worth resolving.",
        "C": "Material product-surface gaps remain.",
        "D": "Significant product-surface gaps need remediation.",
        "F": "Major product-surface problems were observed.",
    }[letter]


def _hard_display(posture: HardPosture) -> dict:
    if posture.disposition in BLOCKING_HARD_DISPOSITIONS:
        status = "HOLD"
        tone = "blocking"
    elif posture.disposition in EVIDENCE_NEEDED_HARD_DISPOSITIONS:
        status = "EVIDENCE NEEDED"
        tone = "evidence"
    elif posture.disposition in (
        "eligible_for_declared_stage_handoff_review",
        "proceed_to_engineering",
    ):
        status = "BOUNDED NEXT STEP"
        tone = "reviewed"
    else:
        status = "NOT VERIFIED"
        tone = "unverified"

    label = {
        "not_reviewed": "H.A.R.D. not yet reviewed",
        "insufficient_evidence": "H.A.R.D. found insufficient evidence",
        "hold_for_remediation": "H.A.R.D. requires remediation before proceeding",
        "eligible_for_declared_stage_handoff_review": "Eligible for declared-stage handoff review",
        "proceed_to_engineering": "Evidence supports considering a bounded engineering step",
        "revise_before_engineering": "Revise before committing engineering resources",
    }[posture.disposition]

    return {
        "status": status,
        "tone": tone,
        "label": label,
        "route": posture.route,
        "disposition": posture.disposition,
        "evidence_ceiling": posture.evidence_ceiling,
        "blocker_ids": posture.blocker_ids,
        "summary": posture.summary,
    }


def calculate_report_grade(report: ReportGradeInput) -> dict:
    module_results: list[dict] = []
    weighted_score = 0.0
    scorable_weight = 0.0
    weighted_confidence = 0.0
    weighted_coverage = 0.0
    deductions: list[dict] = []

    for module_id, meta in MODULES.items():
        items = [finding for finding in report.findings if finding.module == module_id]
        all_weight = sum(finding.weight for finding in items)
        known = [finding for finding in items if finding.status != "unknown"]
        known_weight = sum(finding.weight for finding in known)

        module_score = None
        if known_weight:
            earned = sum(finding.weight * STATUS_FACTOR[finding.status] for finding in known)
            module_score = round(100 * earned / known_weight)
            weighted_score += module_score * float(meta["weight"])
            scorable_weight += float(meta["weight"])

            for finding in known:
                factor = STATUS_FACTOR[finding.status]
                if factor < 1:
                    deduction = float(meta["weight"]) * (finding.weight / known_weight) * (1 - factor)
                    deductions.append(
                        {
                            "id": finding.id,
                            "module": module_id,
                            "module_label": meta["label"],
                            "title": finding.title,
                            "status": finding.status,
                            "summary": finding.summary,
                            "points": round(deduction),
                            "evidence_locations": finding.evidence_locations,
                            "developer_trace": None if finding.developer_trace is None else finding.developer_trace.model_dump(),
                        }
                    )

        module_coverage = round(100 * known_weight / all_weight) if all_weight else 0
        module_confidence = 0
        if all_weight:
            confidence_units = sum(
                finding.weight * REPORT_EVIDENCE_CONFIDENCE[finding.evidence_level]
                for finding in items
            )
            module_confidence = round(100 * confidence_units / all_weight)

        weighted_coverage += module_coverage * float(meta["weight"])
        weighted_confidence += module_confidence * float(meta["weight"])
        module_results.append(
            {
                "id": module_id,
                "label": meta["label"],
                "weight": meta["weight"],
                "score": module_score,
                "coverage": module_coverage,
                "confidence": module_confidence,
                "passed": sum(finding.status == "pass" for finding in items),
                "warnings": sum(finding.status == "warning" for finding in items),
                "critical": sum(finding.status == "critical" for finding in items),
                "unknown": sum(finding.status == "unknown" for finding in items),
            }
        )

    if not scorable_weight:
        raise ValueError("At least one finding must be assessed before a report grade can be calculated")

    score = round(weighted_score / scorable_weight)
    grade = grade_letter(score)
    coverage = round(weighted_coverage / 100)
    confidence = round(weighted_confidence / 100)
    hard = _hard_display(report.hard)

    deductions.sort(key=lambda row: (-row["points"], row["title"]))
    signal_priority = deductions[0] if deductions else None
    if report.hard_priority is not None:
        primary_action = {
            "source": "hard",
            "id": report.hard_priority.id,
            "title": report.hard_priority.title,
            "summary": report.hard_priority.summary,
            "points": None,
            "evidence_locations": report.hard_priority.evidence_locations,
            "next_evidence": report.hard_priority.next_evidence,
            "developer_trace": None if report.hard_priority.developer_trace is None else report.hard_priority.developer_trace.model_dump(),
        }
    elif signal_priority is not None:
        primary_action = {
            "source": "product_signal",
            **signal_priority,
            "next_evidence": None,
        }
    else:
        primary_action = None
    counts = {
        "critical": sum(finding.status == "critical" for finding in report.findings),
        "warnings": sum(finding.status == "warning" for finding in report.findings),
        "passed": sum(finding.status == "pass" for finding in report.findings),
        "unknown": sum(finding.status == "unknown" for finding in report.findings),
    }

    if confidence < 50:
        qualifier = "Provisional"
    elif confidence < 80:
        qualifier = "Evidence-limited"
    else:
        qualifier = "Evidence-supported"

    return {
        "subject": report.subject,
        "product": report.product,
        "reviewed_surface": report.reviewed_surface,
        "grade_name": "Product Signal Grade",
        "grade": grade,
        "score": score,
        "grade_qualifier": qualifier,
        "coverage": coverage,
        "confidence": confidence,
        "confidence_label": _confidence_label(confidence),
        "surface_verdict": _surface_verdict(grade),
        "counts": counts,
        "modules": module_results,
        "top_priority": signal_priority,
        "primary_action": primary_action,
        "deductions": deductions,
        "hard": hard,
        "overall_display": f"{grade} · {score}/100 / {hard['status']}",
        "auxiliary_scores": [AuxiliaryScore.model_validate(score).model_dump() for score in report.auxiliary_scores],
        "boundary": (
            "The Product Signal Grade is a triage summary of the reviewed product surface, "
            "not a H.A.R.D. protocol score and not certification. H.A.R.D. posture remains a "
            "separate, non-compensatory decision result. Unknowns reduce coverage/confidence "
            "instead of becoming automatic failures. Accessibility, privacy, security, legal "
            "compliance, and deployment assurance still require their applicable reviews."
        ),
        "cost_model": {
            "grade_calculation_requires_model": False,
            "report_rendering_requires_model": False,
            "network_required": False,
            "batch_rule": "Reuse retained findings/evidence; recompute deterministically. Model summarization is optional.",
        },
        "scoring": {
            "module_weights": {key: value["weight"] for key, value in MODULES.items()},
            "status_factors": STATUS_FACTOR,
            "report_evidence_confidence": REPORT_EVIDENCE_CONFIDENCE,
            "hard_in_numeric_score": False,
            "unknowns_are_failures": False,
            "auxiliary_scores_in_numeric_score": False,
        },
    }


def hard_posture_from_artifact_result(result: dict) -> HardPosture:
    """Project review_artifact() output without creating a new H.A.R.D. judgment."""
    disposition = result.get("disposition")
    mapped = {
        "Hold for remediation": "hold_for_remediation",
        "Insufficient evidence": "insufficient_evidence",
        "Eligible for declared stage handoff review": "eligible_for_declared_stage_handoff_review",
    }.get(disposition)
    if mapped is None:
        raise ValueError("Unrecognized artifact-review disposition")

    required = result.get("required_evidence_levels") or []
    order = ["specified", "walkthrough", "implemented", "runtime_tested"]
    ceiling = next((stage for stage in reversed(order) if stage in required), "unknown")
    blockers = [
        *result.get("unresolved_critical_ids", []),
        *result.get("unresolved_major_ids", []),
        *result.get("deepening_failure_ids", []),
        *result.get("choices_requiring_revision", []),
    ]
    return HardPosture(
        route="artifact_review",
        disposition=mapped,
        evidence_ceiling=ceiling,
        blocker_ids=list(dict.fromkeys(blockers)),
        summary="Stage-bounded artifact review. It does not authorize deployment.",
    )


def hard_posture_from_engineering_result(result: dict) -> HardPosture:
    """Project assess() output without translating gates into a numeric score."""
    decision = result.get("decision")
    mapped = {
        "PROCEED_TO_ENGINEERING": "proceed_to_engineering",
        "REVISE": "revise_before_engineering",
        "INSUFFICIENT_EVIDENCE": "insufficient_evidence",
    }.get(decision)
    if mapped is None:
        raise ValueError("Unrecognized engineering-commitment decision")

    blocker_ids: list[str] = []
    for gate in result.get("gates", []):
        if gate.get("status") == "FAIL":
            blocker_ids.append(str(gate.get("id")))
    blocker_ids.extend(result.get("unresolved_critical_ids", []))

    return HardPosture(
        route="engineering_commitment",
        disposition=mapped,
        evidence_ceiling="unknown",
        blocker_ids=list(dict.fromkeys(blocker_ids)),
        summary="Engineering recommendation only. Owner authorization and deployment evaluation remain separate.",
    )


def render_grade_report(report: ReportGradeInput, format: Literal["markdown", "html"] = "html") -> str:
    result = calculate_report_grade(report)
    hard = result["hard"]

    if format == "markdown":
        lines = [
            f"# {result['subject']} - H.A.R.D. Readiness Report",
            "",
            f"## {result['grade']} - {result['score']} / 100",
            f"{result['grade_qualifier']} {result['grade_name']}",
            f"H.A.R.D. posture: **{hard['status']}** - {hard['label']}",
            f"Evidence confidence: {result['confidence']}% ({result['confidence_label']}); coverage: {result['coverage']}%",
            "",
            result["surface_verdict"],
            "",
            f"Critical: {result['counts']['critical']} | Warnings: {result['counts']['warnings']} | "
            f"Passed: {result['counts']['passed']} | Unknown: {result['counts']['unknown']}",
            "",
            "## Score breakdown",
        ]
        for module in result["modules"]:
            score = "N/A" if module["score"] is None else str(module["score"])
            lines.append(
                f"- {module['label']}: {score} (coverage {module['coverage']}%, confidence {module['confidence']}%)"
            )
        if result["primary_action"]:
            item = result["primary_action"]
            lines += ["", "## Fix first", f"**{item['title']}**"]
            if item["source"] == "product_signal":
                lines.append(f"-{item['points']} signal points")
            else:
                lines.append("H.A.R.D. priority; not converted to points")
            lines.append(item["summary"] or "Resolve this evidence-backed finding.")
            if item.get("next_evidence"):
                lines += ["", f"Prove next: {item['next_evidence']}"]
            trace = item.get("developer_trace")
            if trace:
                lines += [
                    "",
                    "### Developer view",
                    f"- Observed: {trace['observed']}",
                    f"- Decision underneath: {trace['decision_underneath']}",
                    f"- What must be true: {trace['must_be_true']}",
                    f"- If it fails: {trace['if_wrong']}",
                    f"- Prove next: {trace['prove_next']}",
                ]
        unknowns = [f for f in report.findings if f.status == "unknown"]
        if unknowns:
            lines += ["", "## Verify next"]
            lines.extend(f"- {f.title}: {f.next_evidence}" for f in unknowns[:5])
        if result["auxiliary_scores"]:
            lines += ["", "## Growth signals (not included in the grade)"]
            lines.extend(f"- {s['label']}: {s['score']}" for s in result["auxiliary_scores"])
        lines += ["", result["boundary"]]
        return "\n".join(lines)

    if format != "html":
        raise ValueError("Grade report format must be markdown or html")

    def esc(value: object) -> str:
        return html.escape(str(value), quote=True)

    module_rows = "".join(
        "<div class=\"signal-row\"><div class=\"signal-copy\"><strong>"
        + esc(module["label"])
        + "</strong><span>"
        + esc(module["coverage"])
        + "% coverage · "
        + esc(module["confidence"])
        + "% confidence</span></div><div class=\"signal-score\">"
        + ("N/A" if module["score"] is None else esc(module["score"]))
        + "</div></div>"
        for module in result["modules"]
    )

    priority = ""
    if result["primary_action"]:
        item = result["primary_action"]
        trace = item.get("developer_trace")
        trace_html = ""
        if trace:
            trace_html = (
                "<div class=\"developer-view\"><p class=\"eyebrow\">Developer view</p>"
                "<div class=\"trace-grid\">"
                "<div><span>Observed</span><p>" + esc(trace["observed"]) + "</p></div>"
                "<div><span>Decision underneath</span><p>" + esc(trace["decision_underneath"]) + "</p></div>"
                "<div><span>What must be true?</span><p>" + esc(trace["must_be_true"]) + "</p></div>"
                "<div><span>If it fails</span><p>" + esc(trace["if_wrong"]) + "</p></div>"
                "</div><div class=\"prove-next\"><span>Prove next</span><strong>" + esc(trace["prove_next"]) + "</strong></div></div>"
            )
        marker = ("-" + esc(item["points"])) if item["source"] == "product_signal" else "H.A.R.D."
        next_html = ""
        if item.get("next_evidence"):
            next_html = "<div class=\"prove-next\"><span>Prove next</span><strong>" + esc(item["next_evidence"]) + "</strong></div>"
        priority = (
            "<section class=\"priority\"><p class=\"eyebrow\">The one thing to fix first</p><div class=\"priority-grid\"><div>"
            "<h2>" + esc(item["title"]) + "</h2><p>" + esc(item["summary"] or "Resolve this evidence-backed finding.") + "</p></div>"
            "<div class=\"deduction\">" + marker + "</div></div>" + trace_html + next_html + "</section>"
        )

    unknowns = [finding for finding in report.findings if finding.status == "unknown"]
    verify = ""
    if unknowns:
        verify_rows = "".join(
            "<li><strong>" + esc(finding.title) + "</strong><span>" + esc(finding.next_evidence) + "</span></li>"
            for finding in unknowns[:5]
        )
        verify = (
            "<section class=\"verify\"><p class=\"eyebrow\">Verify next</p><h2>"
            + esc(len(unknowns))
            + " unknowns were not counted as failures</h2><ul>"
            + verify_rows
            + "</ul></section>"
        )

    auxiliary = ""
    if result["auxiliary_scores"]:
        aux = "".join(
            "<span><strong>" + esc(score["label"]) + "</strong> " + esc(score["score"]) + "</span>"
            for score in result["auxiliary_scores"]
        )
        auxiliary = (
            "<section class=\"aux\"><p class=\"eyebrow\">Growth signals - excluded from overall grade</p><div>"
            + aux
            + "</div></section>"
        )

    posture_class = "posture " + esc(hard["tone"])
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>""" + esc(result["subject"]) + """ - H.A.R.D. Readiness Report</title>
<style>
:root{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#111;background:#f3f3ef}
*{box-sizing:border-box}body{margin:0}main{max-width:1040px;margin:auto;padding:56px 24px 80px}
.card,.priority,.verify,.aux{background:#fff;border:1px solid #d8d8d1;border-radius:22px}
.card{padding:36px}.eyebrow{font-size:11px;letter-spacing:.13em;text-transform:uppercase;margin:0 0 12px}
.hero{display:grid;grid-template-columns:240px 1fr;gap:40px;align-items:end}.grade{font-size:104px;line-height:.84;font-weight:760;letter-spacing:-.07em}
.score{font-size:28px;font-weight:620;margin-top:16px}.qualifier{font-size:13px;margin-top:6px}
h1{font-size:18px;font-weight:600;margin:0 0 14px}.verdict{font-size:30px;line-height:1.15;letter-spacing:-.025em;max-width:25ch;margin:0}
.posture{display:flex;gap:10px;align-items:center;margin-top:22px;padding:12px 14px;border-radius:12px;background:#f0f0ec;font-size:14px}
.posture strong{font-size:12px;letter-spacing:.06em}.posture.blocking{border:1px solid #111}.posture.evidence{border:1px dashed #777}
.meta,.counts{font-size:13px;margin-top:14px}.counts{margin-top:8px}
.signal-list{margin-top:34px;border-top:1px solid #e5e5df}.signal-row{display:grid;grid-template-columns:1fr auto;gap:20px;align-items:center;padding:17px 0;border-bottom:1px solid #e5e5df}.signal-copy{display:flex;flex-direction:column;gap:4px}.signal-copy strong{font-size:15px}.signal-copy span{font-size:12px;color:#666}.signal-score{font-size:26px;font-weight:720;letter-spacing:-.03em}
.priority,.verify,.aux{margin-top:18px;padding:28px}.priority-grid{display:grid;grid-template-columns:1fr auto;gap:24px}.priority h2,.verify h2{font-size:24px;line-height:1.2;margin:0 0 8px}
.priority p,.verify span{font-size:14px;line-height:1.5}.deduction{font-size:38px;font-weight:720;letter-spacing:-.04em}.developer-view{border-top:1px solid #e5e5df;margin-top:24px;padding-top:22px}.trace-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 24px}.trace-grid>div{border-top:1px solid #ecece7;padding:14px 0}.trace-grid span,.prove-next span{display:block;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#666}.trace-grid p{margin:6px 0 0}.prove-next{margin-top:10px;padding:16px;background:#111;color:white;border-radius:12px}.prove-next span{color:#cfcfc8;margin-bottom:5px}.prove-next strong{font-size:15px;line-height:1.4}
.verify ul{list-style:none;padding:0;margin:18px 0 0}.verify li{display:grid;grid-template-columns:minmax(150px,.7fr) 1fr;gap:18px;padding:12px 0;border-top:1px solid #e5e5df}.verify li span{display:block}
.aux div{display:flex;gap:20px;flex-wrap:wrap;font-size:14px}.boundary{font-size:12px;line-height:1.55;margin:22px 4px 0;max-width:86ch}
@media(max-width:700px){main{padding:28px 16px 56px}.card{padding:24px}.hero{grid-template-columns:1fr}.grade{font-size:80px}.verdict{font-size:25px}.priority-grid,.verify li,.trace-grid{grid-template-columns:1fr}.deduction{font-size:30px}.signal-row{padding:14px 0}}
</style></head><body><main>
<section class="card">
<p class="eyebrow">H.A.R.D. Readiness Report</p>
<div class="hero"><div><div class="grade">""" + esc(result["grade"]) + """</div><div class="score">""" + esc(result["score"]) + """ / 100</div><div class="qualifier">""" + esc(result["grade_qualifier"]) + """ Product Signal Grade</div></div>
<div><h1>""" + esc(result["subject"]) + """</h1><p class="verdict">""" + esc(result["surface_verdict"]) + """</p>
<div class="""" + posture_class + """"><strong>""" + esc(hard["status"]) + """</strong><span>""" + esc(hard["label"]) + """</span></div>
<p class="meta">Evidence confidence <strong>""" + esc(result["confidence"]) + """%</strong> · Coverage <strong>""" + esc(result["coverage"]) + """%</strong></p>
<p class="counts">""" + esc(result["counts"]["critical"]) + """ critical · """ + esc(result["counts"]["warnings"]) + """ warnings · """ + esc(result["counts"]["passed"]) + """ passed · """ + esc(result["counts"]["unknown"]) + """ unknown</p></div></div>
<div class="signal-list" aria-label="Product signal breakdown">""" + module_rows + """</div>
</section>""" + priority + verify + auxiliary + """
<p class="boundary">""" + esc(result["boundary"]) + """</p>
</main></body></html>"""
