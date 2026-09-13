from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import harmonise_csv, validate_site_metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and harmonise livestock research data")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("metadata")
    harmonise = sub.add_parser("harmonise")
    harmonise.add_argument("input")
    harmonise.add_argument("output")
    args = parser.parse_args()

    if args.command == "validate":
        data = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
        errors = validate_site_metadata(data)
        if errors:
            raise SystemExit("metadata errors: " + ", ".join(errors))
        print("metadata valid")
    else:
        print(json.dumps(harmonise_csv(args.input, args.output), indent=2))


if __name__ == "__main__":
    main()
