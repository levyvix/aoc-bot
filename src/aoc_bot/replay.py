from __future__ import annotations

import os

from aoc_bot.agent import run_agent
from aoc_bot.artifacts import ARTIFACT_DIR, load_meta, skip_commit_enabled
from aoc_bot.git_push import pull_rebase, push_solutions
from aoc_bot.prompt import render_prompt
from aoc_bot import toolkit


def day_already_solved() -> bool:
    if toolkit.check_day(files_only=True) != 0:
        return False
    if toolkit.prepare() != 0:
        return False
    if toolkit.assert_day() != 0:
        return False
    return toolkit.check_day() == 0


def solve_day(*, skip_commit: bool | None = None) -> int:
    if toolkit.prepare() != 0:
        return 1
    if toolkit.assert_day() != 0:
        return 1
    if render_prompt() != 0:
        return 1
    if run_agent() != 0:
        return 1
    if toolkit.verify() != 0:
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

    print(f"==> Replaying AoC {year} days {start_day}–{end_day} (dry_run={dry_run})")
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
            print(f"SKIP: day {day} already solved")
            continue

        if toolkit.prepare() != 0:
            return 1
        if toolkit.assert_day() != 0:
            return 1
        if render_prompt() != 0:
            return 1
        if toolkit.assert_day() != 0:
            return 1

        output = ARTIFACT_DIR / f"agent-output-{year}-day{day}.md"
        if run_agent(output_file=output) != 0:
            return 1
        if toolkit.verify() != 0:
            return 1

        if not should_skip and push_solutions(year, day) != 0:
            return 1

    print(f"==> Finished {year} days {start_day}–{end_day}")
    return 0
