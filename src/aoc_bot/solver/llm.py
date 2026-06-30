from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

from openai import OpenAI

from aoc_bot.solver.base import SolveResult, Solver, strip_html

SYSTEM_PROMPT = """\
You are an expert competitive programmer solving Advent of Code puzzles.

Write a single Python file that:
1. Defines `def solve(data: str) -> str` returning ONLY the answer as a string (no extra text).
2. Reads input from the `data` parameter (newline-separated puzzle input).
3. Uses only the Python standard library.
4. Is correct and efficient for the given puzzle.

Output ONLY valid Python code. No markdown fences, no explanation.
"""


class LLMSolver(Solver):
  def __init__(self, *, api_key: str, model: str, max_retries: int = 3) -> None:
    self.client = OpenAI(api_key=api_key)
    self.model = model
    self.max_retries = max_retries

  def solve(self, *, day: int, part: int, puzzle_html: str, puzzle_input: str) -> SolveResult:
    puzzle_text = strip_html(puzzle_html)
    last_error: str | None = None

    for attempt in range(self.max_retries):
      user_prompt = self._build_prompt(
        day=day,
        part=part,
        puzzle_text=puzzle_text,
        puzzle_input=puzzle_input,
        previous_error=last_error,
      )
      code = self._generate_code(user_prompt)
      try:
        answer = self._execute_code(code, puzzle_input)
        if answer:
          return SolveResult(answer=answer, source="llm")
      except Exception as exc:  # noqa: BLE001 - retry loop
        last_error = str(exc)

    raise RuntimeError(f"LLM solver failed after {self.max_retries} attempts: {last_error}")

  def _build_prompt(
    self,
    *,
    day: int,
    part: int,
    puzzle_text: str,
    puzzle_input: str,
    previous_error: str | None,
  ) -> str:
    sample = puzzle_input[:500] + ("..." if len(puzzle_input) > 500 else "")
    prompt = f"""Solve Advent of Code {day}, Part {part}.

## Puzzle
{puzzle_text}

## Sample of your puzzle input (full input passed to solve())
```
{sample}
```

Return only Python code with a `solve(data: str) -> str` function.
"""
    if previous_error:
      prompt += f"\n\nYour previous attempt failed with:\n{previous_error}\nFix the code."
    return prompt

  def _generate_code(self, user_prompt: str) -> str:
    response = self.client.chat.completions.create(
      model=self.model,
      messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
      ],
      temperature=0,
    )
    content = response.choices[0].message.content or ""
    return self._extract_code(content)

  @staticmethod
  def _extract_code(content: str) -> str:
    fence = re.search(r"```(?:python)?\s*(.*?)```", content, flags=re.DOTALL)
    if fence:
      return fence.group(1).strip()
    return content.strip()

  @staticmethod
  def _execute_code(code: str, puzzle_input: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
      script = Path(tmp) / "solve.py"
      runner = Path(tmp) / "runner.py"
      script.write_text(code, encoding="utf-8")
      runner.write_text(
        "import json, sys\nfrom solve import solve\n"
        "data = sys.stdin.read()\n"
        "print(solve(data), end='')\n",
        encoding="utf-8",
      )
      result = subprocess.run(
        [sys.executable, str(runner)],
        input=puzzle_input,
        capture_output=True,
        text=True,
        timeout=120,
        cwd=tmp,
      )
      if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "solver exited with non-zero status")
      return result.stdout.strip()
