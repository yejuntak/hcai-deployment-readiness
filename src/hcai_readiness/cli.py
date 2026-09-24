"""Local assessment CLI. Reads one JSON input and prints one validated result."""
import argparse
import json
from pathlib import Path
from pydantic import ValidationError
from .contracts import Assessment
from .engine import assess
from .guidance import new_review, guided_review
from .reporting import render_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, nargs="?")
    parser.add_argument("--format", choices=("json", "markdown", "html"), default="json")
    parser.add_argument("--guide", action="store_true", help="Return a decision card and one next question")
    parser.add_argument("--new", action="store_true", help="Print an empty versioned record; never seed evidence")
    parser.add_argument("--run-id")
    parser.add_argument("--recorded-at")
    parser.add_argument("--evaluator-kind", choices=("human", "ai-assisted-human", "agent", "synthetic"))
    parser.add_argument("--profile", choices=("QUICK6", "FULL"), default="QUICK6")
    args = parser.parse_args()
    try:
        if args.new:
            if args.input or args.guide or args.format != "json":
                parser.error("--new cannot be combined with an input, --guide or a report format")
            if not (args.run_id and args.recorded_at and args.evaluator_kind):
                parser.error("--new requires --run-id, --recorded-at and --evaluator-kind")
            result = new_review(args.run_id, args.recorded_at, args.evaluator_kind, args.profile)
        else:
            if args.input is None:
                parser.error("Supply an assessment JSON file, or use --new")
            if args.guide and args.format != "json":
                parser.error("--guide returns JSON; use --format separately for a readable report")
            assessment = Assessment.model_validate_json(args.input.read_text())
            result = guided_review(assessment) if args.guide else assess(assessment)
            if args.format != "json":
                print(render_report(assessment, args.format))
                return
    except ValidationError as exc:
        errors = [{"field": ".".join(map(str, e["loc"])), "type": e["type"]} for e in exc.errors(include_input=False, include_context=False)]
        parser.exit(2, json.dumps({"valid": False, "decision": None, "errors": errors}) + "\n")
    except (ValueError, OSError):
        parser.exit(2, "Unable to read or validate assessment; no decision produced. Check the file and JSON format.\n")
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
