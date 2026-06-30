from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, datetime
from zoneinfo import ZoneInfo

AOC_BASE_URL = "https://adventofcode.com"
USER_AGENT = "aoc-bot/0.1 (github-actions; +https://github.com/)"
EST = ZoneInfo("America/New_York")

# AoC asks automations to stay under ~1 request / 15 min; submissions are 1/min.
SUBMIT_COOLDOWN_SECONDS = 60
POLL_INTERVAL_SECONDS = 2
MAX_UNLOCK_WAIT_SECONDS = 120


@dataclass(frozen=True)
class Settings:
    session: str
    year: int
    day: int | None
    openai_api_key: str | None
    openai_model: str
    solver: str  # "llm" | "local" | "auto"
    dry_run: bool
    part: int | None  # 1, 2, or None for both

    @classmethod
    def from_env(cls) -> Settings:
        today = date.today()
        year = int(os.environ.get("AOC_YEAR", today.year))
        day_raw = os.environ.get("AOC_DAY")
        day = int(day_raw) if day_raw else None

        session = os.environ.get("AOC_SESSION", "")
        if not session:
            raise ValueError("AOC_SESSION is required")

        part_raw = os.environ.get("AOC_PART")
        part = int(part_raw) if part_raw else None
        if part is not None and part not in (1, 2):
            raise ValueError("AOC_PART must be 1 or 2")

        return cls(
            session=session,
            year=year,
            day=day,
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            openai_model=os.environ.get("OPENAI_MODEL", "gpt-4.1"),
            solver=os.environ.get("AOC_SOLVER", "auto"),
            dry_run=os.environ.get("AOC_DRY_RUN", "").lower() in {"1", "true", "yes"},
            part=part,
        )


def current_aoc_day(year: int | None = None) -> int | None:
    """Return today's AoC day number (1-25) in US Eastern, or None outside December."""
    now = datetime.now(EST)
    if now.month != 12:
        return None
    event_year = year or now.year
    if now.year != event_year:
        return None
    return now.day


def is_historical_replay(year: int, day: int) -> bool:
    """True when the puzzle day is already in the past (skip midnight unlock polling)."""
    now = datetime.now(EST)
    if year < now.year:
        return True
    if year > now.year:
        return False
    if now.month < 12:
        return False
    if now.month > 12:
        return True
    return day < now.day


def resolve_day(settings: Settings) -> int:
    if settings.day is not None:
        return settings.day
    day = current_aoc_day(settings.year)
    if day is None:
        raise ValueError(
            "No AOC_DAY set and today is not an active Advent of Code day "
            f"(year={settings.year}, eastern date={datetime.now(EST).date()})"
        )
    return day
