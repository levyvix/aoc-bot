#!/usr/bin/env python3
"""Fetch today's AoC puzzle and write artifacts for the Codex agent."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Allow running without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aoc_bot.client import AoCClient
from aoc_bot.config import Settings, resolve_day, is_historical_replay
from aoc_bot.solver.base import strip_html

ARTIFACT_DIR = Path(".aoc")


def main() -> None:
    settings = Settings.from_env()
    day = resolve_day(settings)
    out = ARTIFACT_DIR
    out.mkdir(parents=True, exist_ok=True)

    with AoCClient(settings.session, settings.year) as client:
        if is_historical_replay(settings.year, day):
            print(f"Historical replay — skipping unlock wait (year={settings.year}, day={day})")
        else:
            print(f"Waiting for day {day} to unlock...")
            client.wait_for_day_unlock(day)

        try:
            puzzle_input = client.get_input(day)
            page = client.get_puzzle_page(day)
        except Exception:
            ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
            try:
                debug = client._client.get(f"/{settings.year}/day/{day}")
                (ARTIFACT_DIR / "debug-day-page.html").write_text(debug.text, encoding="utf-8")
            except Exception:
                pass
            raise

    (out / "day.txt").write_text(str(day), encoding="utf-8")
    (out / "year.txt").write_text(str(settings.year), encoding="utf-8")
    (out / "input.txt").write_text(puzzle_input, encoding="utf-8")
    (out / "puzzle-part1.md").write_text(strip_html(page.part1_html), encoding="utf-8")

    part2_path = out / "puzzle-part2.md"
    if page.part2_html:
        part2_path.write_text(strip_html(page.part2_html), encoding="utf-8")
    elif part2_path.exists():
        part2_path.unlink()

    meta = {
        "day": day,
        "year": settings.year,
        "title": page.title,
        "has_part2": page.part2_html is not None,
        "input_bytes": len(puzzle_input),
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(json.dumps(meta))


if __name__ == "__main__":
    main()
