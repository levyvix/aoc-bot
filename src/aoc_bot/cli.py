from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from aoc_bot.agent import run_agent
from aoc_bot.artifacts import skip_commit_enabled
from aoc_bot.git_push import push_solutions
from aoc_bot.prompt import render_prompt
from aoc_bot.replay import replay_year, solve_day
from aoc_bot import toolkit


def _add_part_commands(sub: argparse._SubParsersAction) -> None:
    for name, handler in (
        ("puzzle", toolkit.puzzle),
        ("test", toolkit.test),
        ("submit", toolkit.submit),
    ):
        parser = sub.add_parser(name, help=f"{name} for a puzzle part (1 or 2)")
        parser.add_argument("part", type=int, choices=(1, 2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aoc",
        description="Advent of Code automation — agent toolkit and CI workflows",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("prepare", help="Fetch input and puzzle text from adventofcode.com")
    sub.add_parser("refresh", help="Re-fetch puzzle page (after Part 1 accepted)")
    sub.add_parser("meta", help="Print .aoc/meta.json")
    sub.add_parser("input-path", help="Print path to puzzle input file")
    sub.add_parser("assert-day", help="Exit 1 if .aoc/meta.json does not match AOC_YEAR/AOC_DAY")
    sub.add_parser("render-prompt", help="Write the autonomous agent prompt to .aoc/prompt.md")
    sub.add_parser("verify", help="Post-agent sanity check (assert-day + test)")

    check = sub.add_parser("check-day", help="Exit 0 if day is already solved")
    check.add_argument(
        "--files-only",
        action="store_true",
        help="Only check solution files exist (no AoC fetch, no session)",
    )

    agent = sub.add_parser("run-agent", help="Run the Cursor agent against .aoc/prompt.md")
    agent.add_argument("--prompt", type=Path, default=None)
    agent.add_argument("--output", type=Path, default=None)
    agent.add_argument("--model", default=None)

    push = sub.add_parser("push", help="Commit and push solutions for the current day")
    push.add_argument("--year", type=int, default=None)
    push.add_argument("--day", type=int, default=None)

    solve = sub.add_parser(
        "solve-day",
        help="Full pipeline: prepare → prompt → agent → verify → push",
    )
    solve.add_argument(
        "--skip-commit",
        action="store_true",
        help="Do not push solutions (also respects AOC_SKIP_COMMIT)",
    )

    replay = sub.add_parser("replay-year", help="Solve a range of days sequentially")
    replay.add_argument("--year", type=int, default=None)
    replay.add_argument("--start", type=int, default=None)
    replay.add_argument("--end", type=int, default=None)
    replay.add_argument(
        "--skip-commit",
        action="store_true",
        help="Do not push solutions (also respects AOC_SKIP_COMMIT)",
    )

    _add_part_commands(sub)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        match args.command:
            case "prepare":
                return toolkit.prepare()
            case "refresh":
                return toolkit.refresh()
            case "meta":
                return toolkit.meta()
            case "input-path":
                return toolkit.input_path()
            case "assert-day":
                return toolkit.assert_day()
            case "check-day":
                return toolkit.check_day(files_only=args.files_only)
            case "puzzle":
                return toolkit.puzzle(args.part)
            case "test":
                return toolkit.test(args.part)
            case "submit":
                return toolkit.submit(args.part)
            case "render-prompt":
                return render_prompt()
            case "verify":
                return toolkit.verify()
            case "run-agent":
                return run_agent(
                    prompt_file=args.prompt,
                    output_file=args.output,
                    model=args.model,
                )
            case "push":
                year = args.year
                day = args.day
                if year is None or day is None:
                    from aoc_bot.artifacts import load_meta

                    meta = load_meta()
                    year = year or int(meta["year"])
                    day = day or int(meta["day"])
                return push_solutions(year, day)
            case "solve-day":
                skip = args.skip_commit or skip_commit_enabled()
                return solve_day(skip_commit=skip)
            case "replay-year":
                year = args.year or int(os.environ["AOC_YEAR"])
                start = args.start or int(os.environ.get("AOC_START_DAY", "1"))
                end = args.end or int(os.environ.get("AOC_END_DAY", "25"))
                skip = args.skip_commit or skip_commit_enabled()
                return replay_year(
                    year=year,
                    start_day=start,
                    end_day=end,
                    skip_commit=skip,
                )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except KeyError as exc:
        print(f"ERROR: missing required env var {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
