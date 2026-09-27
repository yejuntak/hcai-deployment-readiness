"""Deterministic H.A.R.D. Grade summary for external-facing reports.

The grade is a communication layer over reviewed findings. It never replaces the
six H.A.R.D. gates, owner authorization, deployment evaluation, accessibility
conformance testing, security review, or legal/compliance assessment.

Unknown findings do not silently fail. They lower evidence confidence instead.
A caller may mark a critical finding as blocking; a blocking finding caps the
display score while preserving the uncapped raw score for transparency.
"""
from __future__ import annotations

import html
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ModuleId = Literal[
    "hard_core",
    "accessibility",
    "action_recovery",
    "privacy_trust",
    "public_evidence",
]
FindingStatus = Literal["pass", "warning", "critical", "unknown"]
EvidenceStage = Literal["specified", "walkthrough", "implemented", "runtime_tested", "unknown"]

MODULES: dict[str, dict[str, object]] = {
    "hard_core": {"label": "H.A.R.D. Core Readiness", "weight": 60},
    "accessibility": {"label": "Accessibility", "weight": 15},
    "action_recovery": {"label": "AI Action & Recovery", "weight": 10},
    "privacy_trust": {"label": "Privacy & Trust", "weight": 10},
    "public_evidence": {"label": "Public Product Evidence", "weight": 5},
}

STATUS_FACTOR = {
    "pass": 1.0,
    "warning": 0.5,
    "critical": 0.0,
}

EVIDENCE_CONFIDENCE = {
    "unknown": 0.0,
    "specified": 0.35,
    "walkthrough": 0.60,
    "implemented": 0.80,
    "runtime_tested": 1.0,
}


class GradeFinding(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(min_length=1)
    module: ModuleId
    title: str = Field(min_length=1)
    status: FindingStatus
    evidence_stage: EvidenceStage
    points: float = Field(default=1.0, gt=0, le=100, allow_inf_nan=False)
    summary: str = ""
    blocking: bool = False

    @model_validator(mode="after")
    def status_matches_evidence(self):
        if self.status == "unknown" and self.evidence_stage != "unknown":
            raise ValueError("Unknown findings must use evidence_stage=unknown")
        if self.status != "unknown" and self.evidence_stage == "unknown":
            raise ValueError("Assessed findings require a non-unknown evidence stage")
        if self.blocking and self.status != "critical":
            raise ValueError("Only critical findings may be marked blocking")
        return self


class GradeInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    subject: str = Field(min_length=1)
    product: str | None = None
    reviewed_surface: str = Field(min_length=1)
    findings: list[GradeFinding] = Field(min_length=1)
    apply_blocker_cap: bool = True

    @model_validator(mode="after")
    def unique_finding_ids(self):
        ids = [finding.id for finding in self.findings]
        if len(ids) != len(set(ids)):
            raise ValueError("Finding IDs must be unique")
        return self


def grade_letter(score: int) -> str:
    """Business-readiness bands, intentionally not academic letter grading."""
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


def _verdict(letter: str) -> str:
    return {
        "A+": "Strong evidence across the reviewed surface.",
        "A": "Strong readiness signals with limited evidence gaps.",
        "B": "Generally strong, but important evidence gaps remain.",
        "C": "Material decisions or evidence remain unresolved.",
        "D": "Significant readiness gaps require focused remediation.",
        "F": "Major readiness evidence is missing or conflicted.",
    }[letter]


def calculate_grade(report: GradeInput) -> dict:
    module_results: list[dict] = []
    weighted_score = 0.0
    available_weight = 0.0
    weighted_confidence = 0.0
    deductions: list[dict] = []

    for module_id, meta in MODULES.items():
        items = [finding for finding in report.findings if finding.module == module_id]
        total_points = sum(finding.points for finding in items)
        known = [finding for finding in items if finding.status != "unknown"]
        known_points = sum(finding.points for finding in known)

        module_score = None
        if known_points:
            earned = sum(finding.points * STATUS_FACTOR[finding.status] for finding in known)
            module_score = round(100 * earned / known_points)
            available_weight += float(meta["weight"])
            weighted_score += module_score * float(meta["weight"])

            for finding in known:
                factor = STATUS_FACTOR[finding.status]
                if factor < 1:
                    deduction = float(meta["weight"]) * (finding.points / known_points) * (1 - factor)
                    deductions.append(
                        {
                            "id": finding.id,
                            "module": module_id,
                            "module_label": meta["label"],
                            "title": finding.title,
                            "status": finding.status,
                            "summary": finding.summary,
                            "points": round(deduction),
                        }
                    )

        module_confidence = 0
        if total_points:
            confidence_units = sum(
                finding.points * EVIDENCE_CONFIDENCE[finding.evidence_stage] for finding in items
            )
            module_confidence = round(100 * confidence_units / total_points)
        weighted_confidence += module_confidence * float(meta["weight"])

        module_results.append(
            {
                "id": module_id,
                "label": meta["label"],
                "weight": meta["weight"],
                "score": module_score,
                "confidence": module_confidence,
                "passed": sum(finding.status == "pass" for finding in items),
                "warnings": sum(finding.status == "warning" for finding in items),
                "critical": sum(finding.status == "critical" for finding in items),
                "unknown": sum(finding.status == "unknown" for finding in items),
            }
        )

    if not available_weight:
        raise ValueError("At least one finding must be assessed before a grade can be calculated")

    raw_score = round(weighted_score / available_weight)
    blockers = [
        {
            "id": finding.id,
            "module": finding.module,
            "title": finding.title,
            "summary": finding.summary,
        }
        for finding in report.findings
        if finding.blocking
    ]
    score = min(raw_score, 69) if report.apply_blocker_cap and blockers else raw_score
    letter = grade_letter(score)
    confidence = round(weighted_confidence / 100)

    deductions.sort(key=lambda row: (-row["points"], row["title"]))
    counts = {
        "critical": sum(finding.status == "critical" for finding in report.findings),
        "warnings": sum(finding.status == "warning" for finding in report.findings),
        "passed": sum(finding.status == "pass" for finding in report.findings),
        "unknown": sum(finding.status == "unknown" for finding in report.findings),
    }

    return {
        "subject": report.subject,
        "product": report.product,
        "reviewed_surface": report.reviewed_surface,
        "grade": letter,
        "score": score,
        "raw_score": raw_score,
        "confidence": confidence,
        "confidence_label": _confidence_label(confidence),
        "verdict": _verdict(letter),
        "counts": counts,
        "modules": module_results,
        "top_priority": deductions[0] if deductions else None,
        "deductions": deductions,
        "blockers": blockers,
        "score_cap_applied": bool(blockers and report.apply_blocker_cap and score != raw_score),
        "boundary": (
            "The H.A.R.D. Grade summarizes evidence available to this review. "
            "It is not certification of product quality, safety, accessibility, security, privacy, "
            "legal compliance, or deployment readiness. Unknowns lower confidence rather than silently failing."
        ),
        "scoring": {
            "module_weights": {key: value["weight"] for key, value in MODULES.items()},
            "status_factors": STATUS_FACTOR,
            "evidence_confidence": EVIDENCE_CONFIDENCE,
            "blocker_cap": 69,
        },
    }


def render_grade_report(report: GradeInput, format: Literal["markdown", "html"] = "html") -> str:
    result = calculate_grade(report)
    if format == "markdown":
        lines = [
            f"# {result['subject']} - H.A.R.D. Grade",
            "",
            f"## {result['grade']} - {result['score']} / 100",
            f"Evidence confidence: {result['confidence']}% ({result['confidence_label']})",
            "",
            result["verdict"],
            "",
            f"Critical: {result['counts']['critical']} | Warnings: {result['counts']['warnings']} | "
            f"Passed: {result['counts']['passed']} | Unknown: {result['counts']['unknown']}",
            "",
            "## Breakdown",
        ]
        for module in result["modules"]:
            score = "N/A" if module["score"] is None else str(module["score"])
            lines.append(
                f"- {module['label']}: {score} (confidence {module['confidence']}%, weight {module['weight']}%)"
            )
        if result["top_priority"]:
            priority = result["top_priority"]
            lines += [
                "",
                "## Fix first",
                f"**{priority['title']}** (-{priority['points']} points)",
                priority["summary"] or "Review the evidence and resolve this finding.",
            ]
        if result["blockers"]:
            lines += ["", "## Blocking findings"]
            lines.extend(f"- {item['title']}: {item['summary']}" for item in result["blockers"])
        lines += ["", result["boundary"]]
        return "\n".join(lines)

    if format != "html":
        raise ValueError("Grade report format must be markdown or html")

    def esc(value: object) -> str:
        return html.escape(str(value), quote=True)

    module_rows = "".join(
        "<tr><th scope=\"row\">"
        + esc(module["label"])
        + "</th><td>"
        + ("N/A" if module["score"] is None else esc(module["score"]))
        + "</td><td>"
        + esc(module["confidence"])
        + "%</td></tr>"
        for module in result["modules"]
    )
    priority = ""
    if result["top_priority"]:
        item = result["top_priority"]
        priority = (
            "<section class=\"priority\"><p class=\"eyebrow\">Fix first</p><h2>"
            + esc(item["title"])
            + "</h2><p class=\"deduction\">-"
            + esc(item["points"])
            + " points</p><p>"
            + esc(item["summary"] or "Review the evidence and resolve this finding.")
            + "</p></section>"
        )
    blocker_note = ""
    if result["score_cap_applied"]:
        blocker_note = (
            "<p class=\"cap\"><strong>Blocking cap applied.</strong> Raw score "
            + esc(result["raw_score"])
            + " was capped because at least one supplied finding is explicitly blocking.</p>"
        )

    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>""" + esc(result["subject"]) + """ - H.A.R.D. Grade</title>
<style>
:root{font-family:Inter,system-ui,sans-serif;color:#111;background:#f5f5f2}
*{box-sizing:border-box}body{margin:0}main{max-width:980px;margin:auto;padding:48px 24px 72px}
.card{background:white;border:1px solid #d8d8d2;border-radius:20px;padding:32px}
.eyebrow{font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 12px}
.hero{display:grid;grid-template-columns:220px 1fr;gap:32px;align-items:end}
.grade{font-size:96px;line-height:.9;font-weight:750;letter-spacing:-.06em}
.score{font-size:26px;margin-top:12px}.confidence{font-size:14px;margin-top:14px}
.verdict{font-size:28px;line-height:1.18;max-width:24ch;margin:0}
.counts{margin-top:18px;font-size:14px}.cap{margin-top:16px}
table{width:100%;border-collapse:collapse;margin-top:28px}th,td{text-align:left;padding:14px 0;border-top:1px solid #e7e7e1}
.priority{margin-top:24px;background:white;border:1px solid #d8d8d2;border-radius:20px;padding:28px}
.priority h2{font-size:28px;margin:0 0 8px}.deduction{font-size:20px;font-weight:700;margin:0 0 12px}
.boundary{font-size:13px;line-height:1.5;margin-top:24px;max-width:78ch}
@media(max-width:680px){.hero{grid-template-columns:1fr}.grade{font-size:72px}.verdict{font-size:24px}}
</style></head><body><main>
<section class="card">
<p class="eyebrow">H.A.R.D. Grade</p>
<div class="hero"><div><div class="grade">""" + esc(result["grade"]) + """</div><div class="score">""" + esc(result["score"]) + """ / 100</div><div class="confidence">Evidence confidence: <strong>""" + esc(result["confidence"]) + """%</strong> (""" + esc(result["confidence_label"]) + """)</div></div>
<div><h1>""" + esc(result["subject"]) + """</h1><p class="verdict">""" + esc(result["verdict"]) + """</p><p class="counts">""" + esc(result["counts"]["critical"]) + """ critical · """ + esc(result["counts"]["warnings"]) + """ warnings · """ + esc(result["counts"]["passed"]) + """ passed · """ + esc(result["counts"]["unknown"]) + """ unknown</p>""" + blocker_note + """</div></div>
<table><thead><tr><th>Area</th><th>Score</th><th>Confidence</th></tr></thead><tbody>""" + module_rows + """</tbody></table>
</section>""" + priority + """
<p class="boundary">""" + esc(result["boundary"]) + """</p>
</main></body></html>"""
