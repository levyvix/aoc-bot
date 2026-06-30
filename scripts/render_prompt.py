#!/usr/bin/env python3
"""Render the agent prompt for part 1 or part 2."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ARTIFACT_DIR = Path(".aoc")
PROMPTS = Path(".github/codex/prompts")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", type=int, choices=(1, 2), required=True)
    args = parser.parse_args()

    meta_path = ARTIFACT_DIR / "meta.json"
    if not meta_path.exists():
        print("ERROR: run prepare_day.py first", file=sys.stderr)
        sys.exit(1)

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    day = int(meta["day"])
    year = int(meta["year"])

    if args.part == 1:
        template = (PROMPTS / "solve-part1.md.template").read_text(encoding="utf-8")
        part1_text = (ARTIFACT_DIR / "puzzle-part1.md").read_text(encoding="utf-8")
        prompt = (
            template.replace("{{YEAR}}", str(year))
            .replace("{{DAY}}", str(day))
            .replace("{{DAY_PADDED}}", f"{day:02d}")
            .replace("{{TITLE}}", meta["title"])
            .replace("{{PART1_SECTION}}", part1_text)
        )
        output = ARTIFACT_DIR / "prompt-part1.md"
    else:
        part2_path = ARTIFACT_DIR / "puzzle-part2.md"
        if not part2_path.exists():
            print(
                "ERROR: Part 2 text not available. Submit Part 1 first, then re-run prepare_day.py.",
                file=sys.stderr,
            )
            sys.exit(1)
        template = (PROMPTS / "solve-part2.md.template").read_text(encoding="utf-8")
        part2_text = part2_path.read_text(encoding="utf-8")
        prompt = (
            template.replace("{{YEAR}}", str(year))
            .replace("{{DAY}}", str(day))
            .replace("{{DAY_PADDED}}", f"{day:02d}")
            .replace("{{TITLE}}", meta["title"])
            .replace("{{PART2_SECTION}}", part2_text)
        )
        output = ARTIFACT_DIR / "prompt-part2.md"

    output.write_text(prompt, encoding="utf-8")
    print(f"Wrote {output} ({len(prompt)} bytes)")


if __name__ == "__main__":
    main()
