from __future__ import annotations

import json
import os
import sys

from aoc_bot.artifacts import ARTIFACT_DIR, PROMPT_OUTPUT, PROMPT_TEMPLATE
from aoc_bot.config import is_finale_day


def _part1_workflow(*, year: str, day: str, submit_p1: str) -> str:
    return (
        "## Part 1 workflow\n\n"
        f'1. `meta` → confirm `"day": {day}` and `"year": {year}` → `puzzle 1`.\n'
        "2. Note the Part 1 example input and expected answer.\n"
        f"3. Implement `part1.py` in `solutions/{year}/{day}/`.\n"
        f"4. Run the solve loop for Part 1. {submit_p1}\n"
    )


def render_prompt(*, retry_note: str = "") -> int:
    dry_run = os.environ.get("AOC_DRY_RUN", "").lower() in {"1", "true", "yes"}

    year = os.environ.get("AOC_YEAR", "2026")
    day = os.environ.get("AOC_DAY", "1")
    title = "Advent of Code"
    finale_section = ""
    part2_workflow = ""

    if (ARTIFACT_DIR / "meta.json").exists():
        meta = json.loads((ARTIFACT_DIR / "meta.json").read_text(encoding="utf-8"))
        if not os.environ.get("AOC_YEAR"):
            year = str(meta["year"])
        if not os.environ.get("AOC_DAY"):
            day = str(meta["day"])
        meta_year, meta_day = int(meta["year"]), int(meta["day"])
        if int(year) == meta_year and int(day) == meta_day:
            title = meta.get("title", title)
        else:
            print(
                f"WARNING: meta.json is {meta_year} day {meta_day} "
                f"but prompt targets {year} day {day} — run prepare first",
                file=sys.stderr,
            )

    if dry_run:
        dry_section = (
            "## Dry run mode\n\n"
            "Do **not** call `submit`. Solve Part 1 only and verify it against the puzzle example. "
            "Leave `part2` as `raise NotImplementedError(...)`."
        )
        submit_p1 = "Stop after the Part 1 example passes (dry run — do not submit)."
        part1_workflow = _part1_workflow(year=year, day=day, submit_p1=submit_p1)
    else:
        dry_section = ""
        submit_p1 = (
            "Call `submit 1` and **loop** until it succeeds (`OK part 1 accepted`). "
            "On WRONG, fix or optimize, re-check the example, then retry. "
            "Do not proceed to Part 2 until Part 1 is accepted."
        )
        part1_workflow = _part1_workflow(year=year, day=day, submit_p1=submit_p1)

        submit_p2 = (
            "Call `submit 2` and **loop** until it succeeds (`OK part 2 accepted`). "
            "On WRONG, fix or optimize, re-check the example, then retry."
        )
        submit_p2_finale = (
            "Call `submit 2` and **loop** until it succeeds (`OK part 2 accepted`) "
            "to claim the final star."
        )

        year_int, day_int = int(year), int(day)
        if is_finale_day(year_int, day_int):
            finale_section = (
                "## Finale day\n\n"
                f"Day {day} is the **event finale** — there is no real Part 2 puzzle. "
                "After Part 1 is accepted, skip `refresh` and `puzzle 2`. "
                'Implement `part2.py` with a placeholder answer (e.g. `return "0"`), '
                "then `submit 2` to claim the final star.\n\n"
                "Do **not** modify toolkit source under `src/` — finale handling is built in."
            )
            part2_workflow = (
                "## Part 2 workflow (finale)\n\n"
                "5. Skip `refresh` and `puzzle 2` (finale — no Part 2 description).\n"
                "6. Implement `part2.py` with a placeholder answer (e.g. `return \"0\"`).\n"
                "7. Skip the example gate (no Part 2 puzzle text).\n"
                f"8. {submit_p2_finale}\n"
            )
        else:
            part2_workflow = (
                "## Part 2 workflow\n\n"
                '5. `refresh` → confirm `meta` shows `"has_part2": true` → `puzzle 2`.\n'
                "6. Note the Part 2 example input and expected answer.\n"
                "7. Implement `part2.py` (keep part1 working).\n"
                f"8. Run the solve loop for Part 2. {submit_p2}\n"
            )

    template = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    prompt = (
        template.replace("{{YEAR}}", year)
        .replace("{{DAY}}", day)
        .replace("{{DAY_PADDED}}", f"{int(day):02d}")
        .replace("{{TITLE}}", title)
        .replace("{{DRY_RUN_SECTION}}", dry_section)
        .replace("{{FINALE_SECTION}}", finale_section)
        .replace("{{PART1_WORKFLOW}}", part1_workflow)
        .replace("{{PART2_WORKFLOW}}", part2_workflow)
    )

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    if retry_note:
        prompt = f"{retry_note.strip()}\n\n---\n\n{prompt}"
    PROMPT_OUTPUT.write_text(prompt, encoding="utf-8")
    print(f"Wrote {PROMPT_OUTPUT} ({len(prompt)} bytes)")
    return 0
