from __future__ import annotations

import os
import subprocess
import sys
import threading
from pathlib import Path

from aoc_bot.artifacts import ARTIFACT_DIR

DEFAULT_AGENT_TIMEOUT_SECONDS = 1800


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
    print(f"==> Cursor agent (model={model_name}, year={year}, day={day})", flush=True)

    timeout_raw = os.environ.get("AGENT_TIMEOUT_SECONDS")
    timeout = int(timeout_raw) if timeout_raw else DEFAULT_AGENT_TIMEOUT_SECONDS

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_handle:
        process = subprocess.Popen(
            ["agent", "-p", prompt, "--force", "--model", model_name, "--output-format", "text"],
            stdout=subprocess.PIPE,
            stderr=None,
            text=True,
            bufsize=1,
        )
        assert process.stdout is not None

        def copy_output() -> None:
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                output_handle.write(line)

        reader = threading.Thread(target=copy_output, daemon=True)
        reader.start()

        try:
            return process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            print(
                f"ERROR: agent timed out after {timeout}s — terminating",
                file=sys.stderr,
                flush=True,
            )
            process.terminate()
            try:
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            return 124
        finally:
            reader.join(timeout=10)
