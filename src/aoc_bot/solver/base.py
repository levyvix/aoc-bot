from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SolveResult:
    answer: str
    source: str  # "llm" | "local"


class Solver(ABC):
    @abstractmethod
    def solve(self, *, day: int, part: int, puzzle_html: str, puzzle_input: str) -> SolveResult:
        ...


def strip_html(html: str) -> str:
    text = re.sub(r"<pre><code>(.*?)</code></pre>", r"\n```\n\1\n```\n", html, flags=re.DOTALL)
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
