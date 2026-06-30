from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

from aoc_bot.config import Settings, is_finale_day, resolve_day
from aoc_bot.solution_paths import ensure_solution_dir, part_file, solution_dir
from aoc_bot.solver.base import strip_html

ARTIFACT_DIR = Path(".aoc")
PROMPT_TEMPLATE = Path(".github/codex/prompts/autonomous.md.template")
PROMPT_OUTPUT = ARTIFACT_DIR / "prompt.md"


def load_meta() -> dict:
    path = ARTIFACT_DIR / "meta.json"
    if not path.exists():
        raise ValueError("missing .aoc/meta.json — run prepare")
    return json.loads(path.read_text(encoding="utf-8"))


def active_year_day(settings: Settings | None = None) -> tuple[int, int]:
    """AOC_YEAR/AOC_DAY env wins over stale meta.json."""
    env_year = os.environ.get("AOC_YEAR")
    env_day = os.environ.get("AOC_DAY")
    if env_year and env_day:
        return int(env_year), int(env_day)
    if (ARTIFACT_DIR / "meta.json").exists():
        meta = load_meta()
        return int(meta["year"]), int(meta["day"])
    settings = settings or Settings.from_env()
    return settings.year, resolve_day(settings)


def resolve_year_day() -> tuple[int, int]:
    year = int(os.environ.get("AOC_YEAR", str(date.today().year)))
    day_raw = os.environ.get("AOC_DAY")
    if not day_raw:
        raise ValueError("AOC_DAY is required")
    return year, int(day_raw)


def artifacts_mismatch(year: int, day: int) -> str | None:
    if not (ARTIFACT_DIR / "meta.json").exists():
        return "missing .aoc/meta.json — run prepare"
    meta = load_meta()
    meta_year, meta_day = int(meta["year"]), int(meta["day"])
    if meta_year != year or meta_day != day:
        return (
            f".aoc artifacts are {meta_year} day {meta_day}, "
            f"but expected {year} day {day} — run prepare with AOC_DAY={day}"
        )
    return None


def write_artifacts(
    settings: Settings,
    day: int,
    puzzle_input: str,
    part1_html: str,
    part2_html: str | None,
    title: str,
) -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
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
    return meta


def required_parts() -> list[int]:
    dry_run = os.environ.get("AOC_DRY_RUN", "").lower() in {"1", "true", "yes"}
    return [1] if dry_run else [1, 2]


def skip_commit_enabled() -> bool:
    return os.environ.get("AOC_SKIP_COMMIT", "").lower() in {"1", "true", "yes"}
