"""Local assessment CLI. Reads one JSON input and prints one validated result."""
import argparse
import json
from pathlib import Path
from pydantic import ValidationError
from .contracts import Assessment
from .engine import assess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        result = assess(Assessment.model_validate_json(args.input.read_text()))
    except (ValidationError, ValueError, OSError) as exc:
        parser.exit(2, f"Invalid assessment; no decision produced: {exc}\n")
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
