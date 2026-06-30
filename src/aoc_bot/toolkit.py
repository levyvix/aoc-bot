from __future__ import annotations

import json
import os
import sys
import time

from aoc_bot.artifacts import (
    ARTIFACT_DIR,
    active_year_day,
    artifacts_mismatch,
    load_meta,
    required_parts,
    resolve_year_day,
    write_artifacts,
)
from aoc_bot.client import AoCClient, SubmitResult
from aoc_bot.config import SUBMIT_COOLDOWN_SECONDS, Settings, is_historical_replay, resolve_day
from aoc_bot.solver.local import LocalSolver


def prepare() -> int:
    settings = Settings.from_env()
    day = resolve_day(settings)

    with AoCClient(settings.session, settings.year) as client:
        if is_historical_replay(settings.year, day):
            print(f"Historical replay — skipping unlock wait (year={settings.year}, day={day})")
        else:
            print(f"Waiting for day {day} to unlock...")
            client.wait_for_day_unlock(day)
        puzzle_input = client.get_input(day)
        page = client.get_puzzle_page(day)

    meta = write_artifacts(
        settings, day, puzzle_input, page.part1_html, page.part2_html, page.title
    )
    print(json.dumps(meta, indent=2))
    return 0


def refresh() -> int:
    settings = Settings.from_env()
    day = resolve_day(settings)
    if not (ARTIFACT_DIR / "input.txt").exists():
        print("ERROR: run prepare first", file=sys.stderr)
        return 1

    with AoCClient(settings.session, settings.year) as client:
        page = client.get_puzzle_page(day)
        puzzle_input = client.get_input(day)

    meta = write_artifacts(
        settings, day, puzzle_input, page.part1_html, page.part2_html, page.title
    )
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


def puzzle(part: int) -> int:
    year, day = active_year_day()
    err = artifacts_mismatch(year, day)
    if err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1
    path = ARTIFACT_DIR / f"puzzle-part{part}.md"
    if not path.exists():
        if part == 2 and load_meta().get("finale"):
            print(
                "Finale day — there is no Part 2 puzzle. "
                'Implement part2.py with a placeholder answer (e.g. return "0"), '
                "then test 2 and submit 2 to claim the final star."
            )
            return 0
        print(f"ERROR: {path} not found.", file=sys.stderr)
        if part == 2:
            print("Part 2 unlocks after Part 1 is accepted. Run: submit 1 → refresh", file=sys.stderr)
        return 1
    print(path.read_text(encoding="utf-8"))
    return 0


def part_test_result(
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


def test(part: int) -> int:
    year, day = active_year_day()
    err = artifacts_mismatch(year, day)
    if err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1
    puzzle_input = (ARTIFACT_DIR / "input.txt").read_text(encoding="utf-8")
    ok, detail = part_test_result(
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


def assert_day() -> int:
    year, day = active_year_day()
    err = artifacts_mismatch(year, day)
    if err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(f"OK: artifacts match {year} day {day} ({load_meta().get('title', '')})")
    return 0


def day_complete_on_site() -> int:
    """Exit 0 when adventofcode.com shows both parts complete for the active day."""
    settings = Settings.from_env()
    day = resolve_day(settings)
    dry_run = os.environ.get("AOC_DRY_RUN", "").lower() in {"1", "true", "yes"}
    if dry_run:
        return 1

    with AoCClient(settings.session, settings.year) as client:
        if client.both_parts_complete(day):
            print(f"SKIP: {settings.year} day {day} already complete on adventofcode.com")
            return 0
    return 1


def check_day(*, files_only: bool = False) -> int:
    year, day = resolve_year_day()
    parts = required_parts()
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
        ok, _detail = part_test_result(
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


def submit(part: int) -> int:
    if os.environ.get("AOC_DRY_RUN", "").lower() in {"1", "true", "yes"}:
        print("DRY RUN — submit skipped")
        return 0

    settings = Settings.from_env()
    day = resolve_day(settings)
    year = settings.year
    puzzle_input = (ARTIFACT_DIR / "input.txt").read_text(encoding="utf-8")
    answer = LocalSolver().solve(
        year=year,
        day=day,
        part=part,
        puzzle_html="",
        puzzle_input=puzzle_input,
    ).answer

    with AoCClient(settings.session, settings.year) as client:
        outcome = None
        for attempt in range(5):
            outcome = client.submit_detail(day, part, answer)
            if outcome.result != SubmitResult.TOO_SOON:
                break
            wait = SUBMIT_COOLDOWN_SECONDS * (attempt + 1)
            print(f"Rate limited — sleeping {wait}s (AoC allows ~1 submit/min)")
            time.sleep(wait)

    assert outcome is not None
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


def meta() -> int:
    if not (ARTIFACT_DIR / "meta.json").exists():
        print("ERROR: run prepare first", file=sys.stderr)
        return 1
    print((ARTIFACT_DIR / "meta.json").read_text(encoding="utf-8"))
    return 0


def input_path() -> int:
    path = ARTIFACT_DIR / "input.txt"
    if not path.exists():
        print("ERROR: run prepare first", file=sys.stderr)
        return 1
    print(path.resolve())
    return 0


def verify() -> int:
    parts = required_parts()
    if not (ARTIFACT_DIR / "meta.json").exists():
        print("ERROR: agent did not run prepare — missing .aoc/meta.json", file=sys.stderr)
        return 1
    if assert_day() != 0:
        return 1
    for part in parts:
        if test(part) != 0:
            print("ERROR: post-agent verification failed", file=sys.stderr)
            return 1
    print("Post-agent check passed")
    return 0
