from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from aoc_bot.artifacts import ARTIFACT_DIR


def run_agent(
    *,
    prompt_file: Path | None = None,
    output_file: Path | None = None,
    model: str | None = None,
) -> int:
    if not os.environ.get("CURSOR_API_KEY"):
        print("ERROR: CURSOR_API_KEY is not set", file=sys.stderr)
        return 1

    year = os.environ.get("AOC_YEAR")
    day = os.environ.get("AOC_DAY")
    if not year or not day:
        print("ERROR: AOC_YEAR and AOC_DAY must be set", file=sys.stderr)
        return 1

    prompt_path = prompt_file or (ARTIFACT_DIR / "prompt.md")
    output_path = output_file or (ARTIFACT_DIR / "agent-output.md")
    model_name = model or os.environ.get("CURSOR_MODEL", "composer-2.5")

    if not prompt_path.is_file():
        print(f"ERROR: prompt file not found: {prompt_path}", file=sys.stderr)
        return 1

    prompt = prompt_path.read_text(encoding="utf-8")
    print(f"==> Cursor agent (model={model_name}, year={year}, day={day})")

    result = subprocess.run(
        ["agent", "-p", prompt, "--force", "--model", model_name, "--output-format", "text"],
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="" if result.stderr.endswith("\n") else "\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result.stdout, encoding="utf-8")
    return result.returncode
