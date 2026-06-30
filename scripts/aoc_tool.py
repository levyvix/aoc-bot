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
  uv run python scripts/aoc_tool.py check-day
  uv run python scripts/aoc_tool.py assert-day
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
from aoc_bot.config import SUBMIT_COOLDOWN_SECONDS, Settings, resolve_day, is_historical_replay, is_finale_day
from aoc_bot.solution_paths import ensure_solution_dir, part_file, solution_dir
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

    ensure_solution_dir(settings.year, day)

    meta = {
        "day": day,
        "year": settings.year,
        "title": title,
        "has_part2": part2_html is not None,
        "finale": is_finale_day(settings.year, day),
        "input_bytes": len(puzzle_input),
        "solution_dir": str(solution_dir(settings.year, day)),
        "part1_file": str(part_file(settings.year, day, 1)),
        "part2_file": str(part_file(settings.year, day, 2)),
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
    if meta.get("finale"):
        print("Finale day — no Part 2 puzzle text; submit Part 2 after Part 1 to claim the last star.")
        print(json.dumps(meta, indent=2))
        return 0
    if not meta["has_part2"]:
        print("WARNING: Part 2 text not available yet — submit Part 1 first, then refresh again.")
        return 1
    print("Part 2 unlocked.")
    print(json.dumps(meta, indent=2))
    return 0


def cmd_puzzle(part: int) -> int:
    year, day = _active_year_day()
    err = _artifacts_mismatch(year, day)
    if err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1
    path = ARTIFACT_DIR / f"puzzle-part{part}.md"
    if not path.exists():
        if part == 2 and _load_meta().get("finale"):
            print(
                "Finale day — there is no Part 2 puzzle. "
                "Implement part2.py with a placeholder answer (e.g. return \"0\"), "
                "then test 2 and submit 2 to claim the final star."
            )
            return 0
        print(f"ERROR: {path} not found.", file=sys.stderr)
        if part == 2:
            print("Part 2 unlocks after Part 1 is accepted. Run: submit 1 → refresh", file=sys.stderr)
        return 1
    print(path.read_text(encoding="utf-8"))
    return 0


def _required_parts() -> list[int]:
    dry_run = os.environ.get("AOC_DRY_RUN", "").lower() in {"1", "true", "yes"}
    return [1] if dry_run else [1, 2]


def _part_test_result(
    *,
    year: int,
    day: int,
    part: int,
    puzzle_input: str,
    solver: LocalSolver,
) -> tuple[bool, str]:
    path = solver.part_path(year, day, part)
    if not path.exists():
        return False, f"missing {path}"
    try:
        result = solver.solve(
            year=year,
            day=day,
            part=part,
            puzzle_html="",
            puzzle_input=puzzle_input,
        )
    except (NotImplementedError, AttributeError) as exc:
        return False, f"part{part} not implemented: {exc}"
    if not result.answer:
        return False, f"part{part} returned empty answer"
    return True, result.answer


def cmd_test(part: int) -> int:
    year, day = _active_year_day()
    err = _artifacts_mismatch(year, day)
    if err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1
    puzzle_input = (ARTIFACT_DIR / "input.txt").read_text(encoding="utf-8")
    ok, detail = _part_test_result(
        year=year,
        day=day,
        part=part,
        puzzle_input=puzzle_input,
        solver=LocalSolver(),
    )
    if not ok:
        print(f"ERROR: {detail}", file=sys.stderr)
        return 1
    print(f"OK part{part}={detail}")
    return 0


def _active_year_day() -> tuple[int, int]:
    """Year/day for toolkit commands — AOC_YEAR/AOC_DAY env wins over stale meta.json."""
    env_year = os.environ.get("AOC_YEAR")
    env_day = os.environ.get("AOC_DAY")
    if env_year and env_day:
        return int(env_year), int(env_day)
    if (ARTIFACT_DIR / "meta.json").exists():
        meta = _load_meta()
        return int(meta["year"]), int(meta["day"])
    settings = _settings()
    return settings.year, resolve_day(settings)


def _artifacts_mismatch(year: int, day: int) -> str | None:
    if not (ARTIFACT_DIR / "meta.json").exists():
        return "missing .aoc/meta.json — run prepare"
    meta = _load_meta()
    meta_year, meta_day = int(meta["year"]), int(meta["day"])
    if meta_year != year or meta_day != day:
        return (
            f".aoc artifacts are {meta_year} day {meta_day}, "
            f"but expected {year} day {day} — run prepare with AOC_DAY={day}"
        )
    return None


def cmd_assert_day() -> int:
    year, day = _active_year_day()
    err = _artifacts_mismatch(year, day)
    if err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(f"OK: artifacts match {year} day {day} ({_load_meta().get('title', '')})")
    return 0


def _resolve_year_day() -> tuple[int, int]:
    from datetime import date

    year = int(os.environ.get("AOC_YEAR", str(date.today().year)))
    day_raw = os.environ.get("AOC_DAY")
    if not day_raw:
        raise ValueError("AOC_DAY is required")
    return year, int(day_raw)


def cmd_check_day(*, files_only: bool = False) -> int:
    """Exit 0 when day can be skipped; --files-only needs no prepare or session."""
    year, day = _resolve_year_day()
    parts = _required_parts()
    solver = LocalSolver()

    for part in parts:
        if not solver.part_path(year, day, part).exists():
            return 1

    if files_only:
        return 0

    if not (ARTIFACT_DIR / "input.txt").exists():
        print("ERROR: run prepare before check-day", file=sys.stderr)
        return 1

    puzzle_input = (ARTIFACT_DIR / "input.txt").read_text(encoding="utf-8")
    for part in parts:
        ok, detail = _part_test_result(
            year=year,
            day=day,
            part=part,
            puzzle_input=puzzle_input,
            solver=solver,
        )
        if not ok:
            return 1

    scope = "part 1" if parts == [1] else "parts 1–2"
    print(f"SKIP: {year} day {day} already solved ({scope} pass local tests)")
    return 0


def cmd_submit(part: int) -> int:
    if os.environ.get("AOC_DRY_RUN", "").lower() in {"1", "true", "yes"}:
        print("DRY RUN — submit skipped")
        return 0

    settings = _settings()
    day = resolve_day(settings)
    year = settings.year
    puzzle_input = (ARTIFACT_DIR / "input.txt").read_text(encoding="utf-8")
    solver = LocalSolver()
    answer = solver.solve(
        year=year,
        day=day,
        part=part,
        puzzle_html="",
        puzzle_input=puzzle_input,
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
    p_check = sub.add_parser(
        "check-day",
        help="Exit 0 if day is solved; --files-only needs no prepare",
    )
    p_check.add_argument(
        "--files-only",
        action="store_true",
        help="Only check solution files exist (no AoC fetch, no session)",
    )
    sub.add_parser("assert-day", help="Exit 1 if .aoc/meta.json does not match AOC_YEAR/AOC_DAY")

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
        if args.command == "check-day":
            return cmd_check_day(files_only=args.files_only)
        if args.command == "assert-day":
            return cmd_assert_day()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
