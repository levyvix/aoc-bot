#!/usr/bin/env python3
"""Render the Codex prompt from puzzle artifacts."""

from __future__ import annotations

import json
from pathlib import Path

ARTIFACT_DIR = Path(".aoc")
TEMPLATE = Path(".github/codex/prompts/solve.md.template")
OUTPUT = ARTIFACT_DIR / "codex-prompt.md"


def main() -> None:
    meta = json.loads((ARTIFACT_DIR / "meta.json").read_text(encoding="utf-8"))
    day = int(meta["day"])
    year = int(meta["year"])
    part2 = (ARTIFACT_DIR / "puzzle-part2.md").exists()

    template = TEMPLATE.read_text(encoding="utf-8")
    prompt = (
        template.replace("{{YEAR}}", str(year))
        .replace("{{DAY}}", str(day))
        .replace("{{DAY_PADDED}}", f"{day:02d}")
        .replace("{{TITLE}}", meta["title"])
        .replace("{{HAS_PART2}}", "yes" if part2 else "no")
    )

    if part2:
        part2_text = (ARTIFACT_DIR / "puzzle-part2.md").read_text(encoding="utf-8")
        prompt = prompt.replace("{{PART2_SECTION}}", f"## Part 2 puzzle text\n\n{part2_text}")
    else:
        prompt = prompt.replace(
            "{{PART2_SECTION}}",
            "## Part 2\n\nPart 2 is not unlocked yet. Implement only `part1` for now; "
            "leave `part2` raising `NotImplementedError`.",
        )

    part1_text = (ARTIFACT_DIR / "puzzle-part1.md").read_text(encoding="utf-8")
    prompt = prompt.replace("{{PART1_SECTION}}", part1_text)

    OUTPUT.write_text(prompt, encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(prompt)} bytes)")


if __name__ == "__main__":
    main()
