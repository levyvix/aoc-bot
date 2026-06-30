#!/usr/bin/env python3
"""Agent-facing AoC toolkit — fetch, test, submit, refresh.

Usage:
  uv run python scripts/aoc_tool.py prepare
  uv run python scripts/aoc_tool.py puzzle 1|2
  uv run python scripts/aoc_tool.py test 1|2
  uv run python scripts/aoc_tool.py submit 1|2
  uv run python scripts/aoc_tool.py refresh
  uv run python scripts/aoc_tool.py meta
  uv run python scripts/aoc_tool.py input-path
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aoc_bot.client import AoCClient, SubmitResult
from aoc_bot.config import SUBMIT_COOLDOWN_SECONDS, Settings, resolve_day, is_historical_replay
from aoc_bot.solver.base import strip_html
from aoc_bot.solver.local import LocalSolver

ARTIFACT_DIR = Path(".aoc")


def _settings() -> Settings:
    return Settings.from_env()


def cmd_prepare() -> int:
    settings = _settings()
    day = resolve_day(settings)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    with AoCClient(settings.session, settings.year) as client:
        if is_historical_replay(settings.year, day):
            print(f"Historical replay — skipping unlock wait (year={settings.year}, day={day})")
        else:
            print(f"Waiting for day {day} to unlock...")
            client.wait_for_day_unlock(day)
        puzzle_input = client.get_input(day)
        page = client.get_puzzle_page(day)

    _write_artifacts(settings, day, puzzle_input, page.part1_html, page.part2_html, page.title)
    print(json.dumps(json.loads((ARTIFACT_DIR / "meta.json").read_text()), indent=2))
    return 0


def _write_artifacts(
    settings: Settings,
    day: int,
    puzzle_input: str,
    part1_html: str,
    part2_html: str | None,
    title: str,
) -> None:
    (ARTIFACT_DIR / "day.txt").write_text(str(day), encoding="utf-8")
    (ARTIFACT_DIR / "year.txt").write_text(str(settings.year), encoding="utf-8")
    (ARTIFACT_DIR / "input.txt").write_text(puzzle_input, encoding="utf-8")
    (ARTIFACT_DIR / "puzzle-part1.md").write_text(strip_html(part1_html), encoding="utf-8")

    part2_path = ARTIFACT_DIR / "puzzle-part2.md"
    if part2_html:
        part2_path.write_text(strip_html(part2_html), encoding="utf-8")
    elif part2_path.exists():
        part2_path.unlink()

    meta = {
        "day": day,
        "year": settings.year,
        "title": title,
        "has_part2": part2_html is not None,
        "input_bytes": len(puzzle_input),
        "solution_file": f"solutions/day{day:02d}.py",
    }
    (ARTIFACT_DIR / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")


def cmd_refresh() -> int:
    """Re-fetch puzzle page (call after Part 1 is accepted to unlock Part 2 text)."""
    settings = _settings()
    day = resolve_day(settings)
    if not (ARTIFACT_DIR / "input.txt").exists():
        print("ERROR: run prepare first", file=sys.stderr)
        return 1

    with AoCClient(settings.session, settings.year) as client:
        page = client.get_puzzle_page(day)
        puzzle_input = client.get_input(day)

    _write_artifacts(settings, day, puzzle_input, page.part1_html, page.part2_html, page.title)
    meta = json.loads((ARTIFACT_DIR / "meta.json").read_text())
    if not meta["has_part2"]:
        print("WARNING: Part 2 text not available yet — submit Part 1 first, then refresh again.")
        return 1
    print("Part 2 unlocked.")
    print(json.dumps(meta, indent=2))
    return 0


def cmd_puzzle(part: int) -> int:
    path = ARTIFACT_DIR / f"puzzle-part{part}.md"
    if not path.exists():
        print(f"ERROR: {path} not found.", file=sys.stderr)
        if part == 2:
            print("Part 2 unlocks after Part 1 is accepted. Run: submit 1 → refresh", file=sys.stderr)
        return 1
    print(path.read_text(encoding="utf-8"))
    return 0


def cmd_test(part: int) -> int:
    meta = _load_meta()
    day = int(meta["day"])
    puzzle_input = (ARTIFACT_DIR / "input.txt").read_text(encoding="utf-8")
    solver = LocalSolver()
    if not solver.has_solution(day):
        print(f"ERROR: missing solutions/day{day:02d}.py", file=sys.stderr)
        return 1
    try:
        result = solver.solve(
            day=day, part=part, puzzle_html="", puzzle_input=puzzle_input
        )
    except (NotImplementedError, AttributeError) as exc:
        print(f"ERROR: part{part} not implemented: {exc}", file=sys.stderr)
        return 1
    if not result.answer:
        print(f"ERROR: part{part} returned empty answer", file=sys.stderr)
        return 1
    print(f"OK part{part}={result.answer}")
    return 0


def cmd_submit(part: int) -> int:
    if os.environ.get("AOC_DRY_RUN", "").lower() in {"1", "true", "yes"}:
        print("DRY RUN — submit skipped")
        return 0

    settings = _settings()
    day = resolve_day(settings)
    meta = _load_meta()
    puzzle_input = (ARTIFACT_DIR / "input.txt").read_text(encoding="utf-8")
    solver = LocalSolver()
    answer = solver.solve(
        day=day, part=part, puzzle_html="", puzzle_input=puzzle_input
    ).answer

    with AoCClient(settings.session, settings.year) as client:
        for attempt in range(5):
            outcome = client.submit_detail(day, part, answer)
            if outcome.result == SubmitResult.TOO_SOON:
                wait = SUBMIT_COOLDOWN_SECONDS * (attempt + 1)
                print(f"Rate limited — sleeping {wait}s (AoC allows ~1 submit/min)")
                time.sleep(wait)
                continue
            break

    print(f"Submitted part {part} answer: {answer}")
    print(f"Result: {outcome.result.value}")
    if outcome.feedback:
        print(outcome.feedback)

    if outcome.result in (SubmitResult.CORRECT, SubmitResult.ALREADY_COMPLETE):
        print(f"OK part {part} accepted")
        return 0
    if outcome.result == SubmitResult.WRONG:
        print(f"WRONG answer for part {part} — fix the solution and retry", file=sys.stderr)
        return 1
    print(f"Unexpected result: {outcome.result.value}", file=sys.stderr)
    return 2


def cmd_meta() -> int:
    if not (ARTIFACT_DIR / "meta.json").exists():
        print("ERROR: run prepare first", file=sys.stderr)
        return 1
    print((ARTIFACT_DIR / "meta.json").read_text(encoding="utf-8"))
    return 0


def cmd_input_path() -> int:
    path = ARTIFACT_DIR / "input.txt"
    if not path.exists():
        print("ERROR: run prepare first", file=sys.stderr)
        return 1
    print(path.resolve())
    return 0


def _load_meta() -> dict:
    path = ARTIFACT_DIR / "meta.json"
    if not path.exists():
        raise SystemExit("ERROR: run prepare first")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="AoC agent toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("prepare", help="Fetch input and puzzle text from adventofcode.com")
    sub.add_parser("refresh", help="Re-fetch puzzle page (after Part 1 accepted)")
    sub.add_parser("meta", help="Print .aoc/meta.json")
    sub.add_parser("input-path", help="Print path to puzzle input file")

    p_puzzle = sub.add_parser("puzzle", help="Print puzzle description")
    p_puzzle.add_argument("part", type=int, choices=(1, 2))

    p_test = sub.add_parser("test", help="Run local solution against input")
    p_test.add_argument("part", type=int, choices=(1, 2))

    p_submit = sub.add_parser("submit", help="Submit answer to adventofcode.com")
    p_submit.add_argument("part", type=int, choices=(1, 2))

    args = parser.parse_args()

    try:
        if args.command == "prepare":
            return cmd_prepare()
        if args.command == "refresh":
            return cmd_refresh()
        if args.command == "puzzle":
            return cmd_puzzle(args.part)
        if args.command == "test":
            return cmd_test(args.part)
        if args.command == "submit":
            return cmd_submit(args.part)
        if args.command == "meta":
            return cmd_meta()
        if args.command == "input-path":
            return cmd_input_path()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
