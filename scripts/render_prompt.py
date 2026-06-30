#!/usr/bin/env python3
"""Render the autonomous agent prompt."""

from __future__ import annotations

import json
import os
from pathlib import Path

ARTIFACT_DIR = Path(".aoc")
TEMPLATE = Path(".github/codex/prompts/autonomous.md.template")
OUTPUT = ARTIFACT_DIR / "prompt.md"


def main() -> None:
    dry_run = os.environ.get("AOC_DRY_RUN", "").lower() in {"1", "true", "yes"}

    # Defaults for template rendering before prepare (CI sets AOC_YEAR/AOC_DAY)
    year = os.environ.get("AOC_YEAR", "2026")
    day = os.environ.get("AOC_DAY", "1")
    title = "Advent of Code"

    if (ARTIFACT_DIR / "meta.json").exists():
        meta = json.loads((ARTIFACT_DIR / "meta.json").read_text(encoding="utf-8"))
        year = str(meta["year"])
        day = str(meta["day"])
        title = meta.get("title", title)

    if dry_run:
        dry_section = (
            "## Dry run mode\n\n"
            "Do **not** call `submit`. Solve and verify Part 1 only. "
            "Leave `part2` as `raise NotImplementedError(...)`."
        )
        submit_p1 = "Skip submit (dry run)."
        submit_p2 = "Skip Part 2 entirely."
    else:
        dry_section = ""
        submit_p1 = (
            "**Loop** until `submit 1` succeeds (`OK part 1 accepted`). "
            "On WRONG, fix and retry."
        )
        submit_p2 = (
            "**Loop** until `submit 2` succeeds (`OK part 2 accepted`). "
            "On WRONG, fix and retry."
        )

    template = TEMPLATE.read_text(encoding="utf-8")
    prompt = (
        template.replace("{{YEAR}}", year)
        .replace("{{DAY}}", day)
        .replace("{{DAY_PADDED}}", f"{int(day):02d}")
        .replace("{{TITLE}}", title)
        .replace("{{DRY_RUN_SECTION}}", dry_section)
        .replace("{{SUBMIT_PART1_SECTION}}", submit_p1)
        .replace("{{SUBMIT_PART2_SECTION}}", submit_p2)
    )

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(prompt, encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(prompt)} bytes)")


if __name__ == "__main__":
    main()
