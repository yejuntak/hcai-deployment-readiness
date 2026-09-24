"""Generate only named candidate copies/schemas/fixtures; --check detects drift."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
from hcai_readiness.contracts import Assessment, AssessmentResult, FeedbackEntry, PilotRun
from hcai_readiness.engine import DEPTH, assess
from hcai_readiness.versions import versions

ROOT = Path(__file__).resolve().parents[1]


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()


def generated():
    output = {"versions.json": encoded(versions()), "schemas/risk-depth.json": encoded(DEPTH)}
    for model, name in ((Assessment, "assessment"), (AssessmentResult, "assessment-result"),
                        (FeedbackEntry, "feedback-entry"), (PilotRun, "pilot-run")):
        output[f"schemas/{name}.schema.json"] = encoded({"$schema": "https://json-schema.org/draft/2020-12/schema", **model.model_json_schema()})
    protocol = (ROOT / "protocol/0.1-rc.4-candidate/PROTOCOL.md").read_bytes()
    output["src/hcai_readiness/protocol.md"] = protocol
    output["skills/ai-ready/references/protocol.md"] = protocol
    for name in ("QUICK-6.md", "FULL-PROFILE.md"):
        output[f"skills/ai-ready/references/{name}"] = (ROOT / "protocol/0.1-rc.4-candidate" / name).read_bytes()
    for name in ("assessment", "pilot-run"):
        output[f"skills/ai-ready/references/{name}.schema.json"] = output[f"schemas/{name}.schema.json"]
    for name in ("__init__.py", "versions.py", "contracts.py", "engine.py", "cli.py"):
        output[f"skills/ai-ready/scripts/hcai_readiness/{name}"] = (ROOT / "src/hcai_readiness" / name).read_bytes()
    spec = importlib.util.spec_from_file_location("make_fixture", ROOT / "examples/make_fixture.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base = module.synthetic_case(ROOT)
    cases = {"low-risk-quick": base}
    def case(name):
        value = copy.deepcopy(base)
        value["run_id"] = "SYNTHETIC-" + name.upper()
        cases[name] = value
        return value
    case("polished-no-baseline")["baseline"] = {}
    case("documentation-no-operational-evidence")["requested_profile"] = "FULL"
    case("prototype-no-traceability")["workflow"]["requirements"][0]["validation_ids"] = []
    case("high-risk-quick")["risk"]["impact"] = "high"
    high = case("high-risk-full")
    high["risk"]["impact"] = "high"
    high["requested_profile"] = "FULL"
    for key in DEPTH["high"]["checks"]:
        high["handoff"][key] = {"status": "pass", "evidence_ids": ["E1"], "note": "Synthetic stipulated evidence only",
                                "reviewer_role": "independent reviewer", "independent_from_artifact_owner": True}
    case("savings-erased")["operational_oversight"].update(review_minutes_per_case=8, correction_minutes_per_case=5)
    expensive = case("expensive-evaluation")
    expensive["requested_profile"] = "FULL"
    expensive["evaluator_burden"].update(elapsed_minutes=240, evaluator_minutes=240, participant_minutes=60,
                                         adjudication_minutes=60, labor_cost_per_hour=120, tool_model_cost=20)
    recovery = case("missing-recovery")
    recovery["workflow"]["states"] = [s for s in recovery["workflow"]["states"] if s["kind"] != "recovery"]
    for name, value in cases.items():
        # Validate synthetic records as inputs; expected decisions live independently in tests.
        Assessment.model_validate(value)
        output[f"examples/rc4/{name}.json"] = encoded(value)
    outcome = assess(Assessment.model_validate(base))
    pilot = {"pilot_id": "SYNTHETIC-PILOT-FORMAT-ONLY", "date": "2026-09-24", "participant_role": "fictional advisor",
             "sector": "fictional intake", "participant_id": "SYNTHETIC-P01", "permission": "private",
             "permission_evidence": "Constructed fixture; no real permission was collected", "anonymization": "No real person",
             "external_participant": False, "actual_bounded_use": False, "record_kind": "synthetic_fixture",
             "profile_used": "QUICK6", "risk_tier": "low", "elapsed_minutes": 12, "assessment": base,
             "gates_passed": [g["id"] for g in outcome["gates"]], "gates_failed": [], "gates_missing": [], "evidence_missing": [],
             "decision_before": None, "decision_after": "PROCEED_TO_ENGINEERING", "revision_triggered": None,
             "participant_feedback": "Synthetic format example, not actual feedback", "observation_evidence_ids": ["E3"]}
    PilotRun.model_validate(pilot)
    output["examples/rc4/pilot-synthetic.json"] = encoded(pilot)
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drift = []
    for name, content in generated().items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_bytes() != content:
                drift.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    if drift:
        raise SystemExit("Generated candidate drift:\n" + "\n".join(drift))
    print("Candidate assets verified" if args.check else "Candidate assets generated")


if __name__ == "__main__":
    main()
