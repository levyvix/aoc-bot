from __future__ import annotations

import os
import sys
from pathlib import Path

from aoc_bot.agent import run_agent
from aoc_bot.artifacts import ARTIFACT_DIR, load_meta, skip_commit_enabled
from aoc_bot.config import Settings, max_event_day, resolve_day
from aoc_bot.git_push import pull_rebase, push_solutions
from aoc_bot.prompt import render_prompt
from aoc_bot import toolkit

DEFAULT_SOLVE_ATTEMPTS = 3


def day_already_solved() -> bool:
    return toolkit.day_fully_solved()


def _aoc_incomplete_retry_note() -> str:
    return (
        "## Both parts must be submitted on adventofcode.com\n\n"
        "The last run ended before both stars were earned. "
        "Use `uv run aoc test` and `uv run aoc submit` until part 1 and part 2 "
        "each print `OK part N accepted`. Do not stop until both are accepted."
    )


def _verify_retry_note() -> str:
    return (
        "## Previous attempt failed verification\n\n"
        "Local tests did not pass after the last agent run. "
        "Fix the solution files until every required `test` passes, then submit."
    )


def run_solve_attempts(*, year: int, day: int, output: Path) -> int:
    max_attempts = int(os.environ.get("AOC_SOLVE_ATTEMPTS", str(DEFAULT_SOLVE_ATTEMPTS)))
    dry_run = os.environ.get("AOC_DRY_RUN", "").lower() in {"1", "true", "yes"}
    retry_note = ""

    for attempt in range(1, max_attempts + 1):
        if attempt > 1:
            print(f"==> Solve attempt {attempt}/{max_attempts}", flush=True)

        if render_prompt(retry_note=retry_note) != 0:
            return 1
        if toolkit.assert_day() != 0:
            return 1

        agent_rc = run_agent(output_file=output)
        if agent_rc != 0:
            print(
                f"WARN: agent exited {agent_rc} — checking results anyway",
                flush=True,
            )

        if toolkit.verify() != 0:
            if attempt >= max_attempts:
                return 1
            retry_note = _verify_retry_note()
            continue

        if dry_run:
            return 0

        if toolkit.both_parts_complete_on_site():
            return 0

        if attempt >= max_attempts:
            print(
                "ERROR: agent finished but adventofcode.com does not show both parts complete",
                file=sys.stderr,
            )
            return 1

        retry_note = _aoc_incomplete_retry_note()
        print("==> AoC missing stars — re-running agent", flush=True)

    return 1


def _skip_past_event_end(year: int, day: int) -> bool:
    last_day = max_event_day(year)
    if day <= last_day:
        return False
    print(
        f"SKIP: no puzzle for {year} day {day} "
        f"(event ends on day {last_day})",
        flush=True,
    )
    return True


def solve_day(*, skip_commit: bool | None = None) -> int:
    settings = Settings.from_env()
    day = resolve_day(settings)
    if _skip_past_event_end(settings.year, day):
        return 0

    if toolkit.prepare() != 0:
        return 1
    if toolkit.assert_day() != 0:
        return 1

    year, day = toolkit.active_year_day()
    output = ARTIFACT_DIR / f"agent-output-{year}-day{day}.md"
    if run_solve_attempts(year=year, day=day, output=output) != 0:
        return 1

    should_skip = skip_commit if skip_commit is not None else skip_commit_enabled()
    if should_skip:
        return 0

    meta = load_meta()
    return push_solutions(int(meta["year"]), int(meta["day"]))


def replay_year(
    *,
    year: int,
    start_day: int,
    end_day: int,
    skip_commit: bool | None = None,
) -> int:
    should_skip = skip_commit if skip_commit is not None else skip_commit_enabled()
    dry_run = os.environ.get("AOC_DRY_RUN", "").lower() in {"1", "true", "yes"}

    last_day = min(end_day, max_event_day(year))
    if end_day > last_day:
        print(
            f"NOTE: capping replay end at day {last_day} for {year} "
            f"(requested end day {end_day})",
            flush=True,
        )

    print(f"==> Replaying AoC {year} days {start_day}–{last_day} (dry_run={dry_run})", flush=True)
    os.environ["AOC_YEAR"] = str(year)

    for day in range(start_day, last_day + 1):
        print()
        print("############################################")
        print(f"# {year} Day {day}")
        print("############################################")
        os.environ["AOC_DAY"] = str(day)

        if not should_skip and pull_rebase() != 0:
            return 1

        if day_already_solved():
            print(f"SKIP: day {day} fully solved (local tests + AoC stars)")
            continue

        if toolkit.prepare() != 0:
            return 1
        if toolkit.assert_day() != 0:
            return 1

        output = ARTIFACT_DIR / f"agent-output-{year}-day{day}.md"
        if run_solve_attempts(year=year, day=day, output=output) != 0:
            return 1

        if not should_skip and push_solutions(year, day) != 0:
            return 1

    print(f"==> Finished {year} days {start_day}–{last_day}")
    return 0
