from __future__ import annotations

import os
from pathlib import Path

from aoc_bot.agent import run_agent
from aoc_bot.artifacts import ARTIFACT_DIR, load_meta, skip_commit_enabled
from aoc_bot.git_push import pull_rebase, push_solutions
from aoc_bot.prompt import render_prompt
from aoc_bot import toolkit

DEFAULT_SOLVE_ATTEMPTS = 3


def day_already_solved() -> bool:
    return toolkit.day_fully_solved()


def _submit_retry_note(feedback: str) -> str:
    return (
        "## Previous submit failed\n\n"
        f"Advent of Code rejected the last answer:\n\n{feedback}\n\n"
        "Fix the solution file(s), run `test`, then `submit` again."
    )


def _verify_retry_note() -> str:
    return (
        "## Previous attempt failed verification\n\n"
        "Local tests did not pass after the last agent run. "
        "Fix the solution files until every required `test` passes."
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
                f"WARN: agent exited {agent_rc} — verifying solutions anyway",
                flush=True,
            )

        if toolkit.verify() != 0:
            if attempt >= max_attempts:
                return 1
            retry_note = _verify_retry_note()
            continue

        if dry_run:
            return 0

        submit_rc, feedback = toolkit.submit_all_parts()
        if submit_rc == 0:
            return 0

        if attempt >= max_attempts:
            return 1

        retry_note = _submit_retry_note(feedback)
        print("==> Submit failed — re-running agent with feedback", flush=True)

    return 1


def solve_day(*, skip_commit: bool | None = None) -> int:
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

    print(f"==> Replaying AoC {year} days {start_day}–{end_day} (dry_run={dry_run})", flush=True)
    os.environ["AOC_YEAR"] = str(year)

    for day in range(start_day, end_day + 1):
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

    print(f"==> Finished {year} days {start_day}–{end_day}")
    return 0
