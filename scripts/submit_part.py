#!/usr/bin/env python3
"""Submit the local solution for one part. Exit 0 on success, 1 on wrong answer."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aoc_bot.client import AoCClient, SubmitResult
from aoc_bot.config import SUBMIT_COOLDOWN_SECONDS, Settings, resolve_day
from aoc_bot.solver.local import LocalSolver

ARTIFACT_DIR = Path(".aoc")


def main() -> None:
    part_raw = os.environ.get("AOC_PART")
    if not part_raw:
        print("ERROR: AOC_PART is required", file=sys.stderr)
        sys.exit(2)
    part = int(part_raw)

    settings = Settings.from_env()
    day = resolve_day(settings)
    feedback_path = ARTIFACT_DIR / f"retry-feedback-part{part}.txt"

    solver = LocalSolver()
    puzzle_input = (ARTIFACT_DIR / "input.txt").read_text(encoding="utf-8")
    answer = solver.solve(
        day=day, part=part, puzzle_html="", puzzle_input=puzzle_input
    ).answer
    print(f"Submitting part {part} answer: {answer}")

    with AoCClient(settings.session, settings.year) as client:
        outcome = None
        for attempt in range(5):
            outcome = client.submit_detail(day, part, answer)
            if outcome.result != SubmitResult.TOO_SOON:
                break
            time.sleep(SUBMIT_COOLDOWN_SECONDS * (attempt + 1))
        assert outcome is not None

    print(f"Result: {outcome.result.value}")
    if outcome.feedback:
        print(outcome.feedback)

    if outcome.result in (SubmitResult.CORRECT, SubmitResult.ALREADY_COMPLETE):
        feedback_path.unlink(missing_ok=True)
        sys.exit(0)

    if outcome.result == SubmitResult.WRONG:
        feedback_path.write_text(
            f"Submitted answer: {answer}\nAoC response: {outcome.feedback}\n",
            encoding="utf-8",
        )
        sys.exit(1)

    feedback_path.write_text(
        f"Unexpected submit result: {outcome.result.value}\n{outcome.feedback}\n",
        encoding="utf-8",
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
