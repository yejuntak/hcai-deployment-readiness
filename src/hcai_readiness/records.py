"""Permission-aware exports and release prerequisites, not a publication mechanism."""
from .contracts import FeedbackEntry, PilotRun
from .versions import versions


def public_feedback(entries: list[FeedbackEntry]) -> list[dict]:
    exported = []
    for entry in entries:
        row = {"id": entry.id, "permission": entry.permission, "changes": entry.changes,
               "affected_files": entry.affected_files, "affected_requirements": entry.affected_requirements,
               "validation_status": entry.validation_status}
        if entry.permission == "attribution_approved":
            row.update(source_person=entry.source_person, feedback=entry.feedback)
        else:
            row.update(source_person=None, feedback=None)
        exported.append(row)
    return exported


def release_readiness(pilots: list[PilotRun], regression_passed: bool) -> dict:
    eligible = [p.pilot_id for p in pilots if p.record_kind == "actual" and p.external_participant
                and p.actual_bounded_use and bool((p.participant_feedback or "").strip())
                and p.assessment.versions.model_dump() == versions()]
    blockers = []
    if not regression_passed:
        blockers.append("Passing current regression report required")
    if not eligible:
        blockers.append("At least one recorded bounded external end-user/advisor use with feedback required")
    return {"status": "REMAIN_CANDIDATE" if blockers else "ELIGIBLE_FOR_AUTHOR_RELEASE_REVIEW",
            "eligible_pilot_ids": eligible, "blockers": blockers,
            "automatic_promotion": False,
            "note": "Author must verify actual use, permission and current tests. One pilot is a release prerequisite, not controlled validation."}
