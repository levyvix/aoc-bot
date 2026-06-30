from __future__ import annotations

import logging
import sys
import time

from aoc_bot.client import AoCClient, SubmitResult
from aoc_bot.config import SUBMIT_COOLDOWN_SECONDS, Settings, resolve_day, is_historical_replay
from aoc_bot.solver import LLMSolver, LocalSolver

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("aoc-bot")


def pick_solver(settings: Settings, day: int) -> LocalSolver | LLMSolver:
    local = LocalSolver()
    mode = settings.solver

    if mode == "local":
        return local
    if mode == "llm":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for LLM solver")
        return LLMSolver(api_key=settings.openai_api_key, model=settings.openai_model)
    # auto: prefer committed solution, fall back to LLM
    if local.has_solution(settings.year, day):
        log.info("Using local solution for year %s day %s", settings.year, day)
        return local
    if not settings.openai_api_key:
        raise ValueError(
            f"No local solution for day {day} and OPENAI_API_KEY is not set"
        )
    log.info("No local solution; using LLM solver for day %s", day)
    return LLMSolver(api_key=settings.openai_api_key, model=settings.openai_model)


def run_part(
    client: AoCClient,
    solver: LocalSolver | LLMSolver,
    *,
    year: int,
    day: int,
    part: int,
    puzzle_html: str,
    puzzle_input: str,
    dry_run: bool,
) -> SubmitResult | None:
    log.info("Solving year %s day %s part %s...", year, day, part)
    if isinstance(solver, LocalSolver):
        result = solver.solve(
            year=year,
            day=day,
            part=part,
            puzzle_html=puzzle_html,
            puzzle_input=puzzle_input,
        )
    else:
        result = solver.solve(
            day=day, part=part, puzzle_html=puzzle_html, puzzle_input=puzzle_input
        )
    log.info("Answer (via %s): %s", result.source, result.answer)

    if dry_run:
        log.info("Dry run — skipping submission")
        return None

    submit = client.submit_with_retry(
        day, part, result.answer, cooldown=SUBMIT_COOLDOWN_SECONDS
    )
    log.info("Submit part %s: %s", part, submit.value)

    if submit == SubmitResult.WRONG:
        raise RuntimeError(f"Wrong answer for day {day} part {part}: {result.answer}")
    if submit == SubmitResult.UNKNOWN:
        log.warning("Unexpected submit response — check AoC manually")
    return submit


def main() -> None:
    settings = Settings.from_env()
    day = resolve_day(settings)
    parts = [settings.part] if settings.part else [1, 2]
    log.info(
        "Running AoC %s day %s parts=%s (dry_run=%s)",
        settings.year,
        day,
        parts,
        settings.dry_run,
    )

    solver = pick_solver(settings, day)

    with AoCClient(settings.session, settings.year) as client:
        if is_historical_replay(settings.year, day):
            log.info("Historical replay — skipping unlock wait")
        else:
            log.info("Waiting for puzzle unlock...")
            client.wait_for_day_unlock(day)

        puzzle_input = client.get_input(day)
        log.info("Fetched input (%d bytes)", len(puzzle_input))

        page = client.get_puzzle_page(day)
        log.info("Puzzle: %s", page.title)

        for idx, part in enumerate(parts):
            if part == 2:
                page = client.get_puzzle_page(day)
                if not page.part2_html:
                    log.warning("Part 2 not available yet")
                    return
                puzzle_html = page.part2_html
            else:
                puzzle_html = page.part1_html

            result = run_part(
                client,
                solver,
                year=settings.year,
                day=day,
                part=part,
                puzzle_html=puzzle_html,
                puzzle_input=puzzle_input,
                dry_run=settings.dry_run,
            )

            if (
                part == 1
                and 2 in parts
                and not settings.dry_run
                and result not in (SubmitResult.ALREADY_COMPLETE, None)
            ):
                time.sleep(SUBMIT_COOLDOWN_SECONDS)

    log.info("Done.")


if __name__ == "__main__":
    main()
