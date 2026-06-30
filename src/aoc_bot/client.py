from __future__ import annotations

import re
import time
from dataclasses import dataclass
from enum import Enum

import httpx
from bs4 import BeautifulSoup

from aoc_bot.config import AOC_BASE_URL, USER_AGENT, POLL_INTERVAL_SECONDS, MAX_UNLOCK_WAIT_SECONDS


class SubmitResult(Enum):
    CORRECT = "correct"
    WRONG = "wrong"
    TOO_SOON = "too_soon"
    ALREADY_COMPLETE = "already_complete"
    UNKNOWN = "unknown"


@dataclass
class PuzzlePage:
    title: str
    part1_html: str
    part2_html: str | None


class AoCClient:
    def __init__(self, session: str, year: int) -> None:
        self.year = year
        self._client = httpx.Client(
            base_url=AOC_BASE_URL,
            headers={"User-Agent": USER_AGENT},
            cookies={"session": session},
            timeout=30.0,
            follow_redirects=True,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> AoCClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def wait_for_day_unlock(self, day: int) -> None:
        """Poll until the day's puzzle input is available."""
        deadline = time.monotonic() + MAX_UNLOCK_WAIT_SECONDS
        while time.monotonic() < deadline:
            try:
                self.get_input(day)
                return
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    time.sleep(POLL_INTERVAL_SECONDS)
                    continue
                raise
        raise TimeoutError(f"Day {day} puzzle did not unlock within {MAX_UNLOCK_WAIT_SECONDS}s")

    def get_input(self, day: int) -> str:
        response = self._client.get(f"/{self.year}/day/{day}/input")
        response.raise_for_status()
        return response.text

    def get_puzzle_page(self, day: int) -> PuzzlePage:
        response = self._client.get(f"/{self.year}/day/{day}")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = f"Day {day}"
        title_tag = soup.find("title")
        if title_tag:
            title_match = re.search(r"Day \d+ - (.+?)\s*\|", title_tag.get_text())
            if title_match:
                title = title_match.group(1).strip()

        articles = soup.select("article.day-desc")
        if not articles:
            articles = soup.find_all("article")
        if not articles:
            main = soup.find("main")
            if main is not None:
                articles = [main]

        if not articles:
            raise ValueError(f"Could not parse puzzle description for day {day}")

        part1_html = articles[0].decode_contents()
        part2_html = articles[1].decode_contents() if len(articles) > 1 else None
        return PuzzlePage(title=title, part1_html=part1_html, part2_html=part2_html)

    def submit(self, day: int, part: int, answer: str) -> SubmitResult:
        response = self._client.post(
            f"/{self.year}/day/{day}/answer",
            data={"level": str(part), "answer": str(answer)},
        )
        response.raise_for_status()
        body = response.text.lower()

        if "that's the right answer" in body:
            return SubmitResult.CORRECT
        if "you gave an answer too recently" in body:
            return SubmitResult.TOO_SOON
        if "that's not the right answer" in body:
            return SubmitResult.WRONG
        if "you don't seem to be solving the right level" in body:
            return SubmitResult.ALREADY_COMPLETE
        if "did you already complete it" in body:
            return SubmitResult.ALREADY_COMPLETE
        if "both parts of this puzzle are complete" in body:
            return SubmitResult.ALREADY_COMPLETE
        return SubmitResult.UNKNOWN

    def submit_with_retry(
        self,
        day: int,
        part: int,
        answer: str,
        *,
        cooldown: int,
        max_attempts: int = 5,
    ) -> SubmitResult:
        for attempt in range(max_attempts):
            result = self.submit(day, part, answer)
            if result != SubmitResult.TOO_SOON:
                return result
            wait = cooldown * (attempt + 1)
            time.sleep(wait)
        return SubmitResult.TOO_SOON
