#!/usr/bin/env bash
# Local replay test against a past AoC year (default 2025 day 1).
# Requires: AOC_SESSION, OPENAI_API_KEY (for Codex CLI) or run on GitHub Actions instead.
set -euo pipefail

YEAR="${AOC_YEAR:-2025}"
DAY="${AOC_DAY:-1}"
DRY_RUN="${AOC_DRY_RUN:-true}"

cd "$(dirname "$0")/.."

if [[ -z "${AOC_SESSION:-}" ]]; then
  echo "ERROR: export AOC_SESSION=... (AoC session cookie)" >&2
  exit 1
fi

export AOC_YEAR="$YEAR"
export AOC_DAY="$DAY"
export AOC_DRY_RUN="$DRY_RUN"

echo "==> Replay test: year=$YEAR day=$DAY dry_run=$DRY_RUN"
uv sync --quiet

echo "==> Prepare puzzle"
uv run python scripts/prepare_day.py

echo "==> Render Codex prompt"
uv run python scripts/render_prompt.py

if command -v codex >/dev/null 2>&1 && [[ -n "${OPENAI_API_KEY:-}" ]]; then
  echo "==> Run Codex locally"
  codex exec "$(cat .aoc/codex-prompt.md)" --sandbox workspace-write
else
  echo "SKIP Codex (install codex CLI + OPENAI_API_KEY, or use GitHub Actions test-replay workflow)"
fi

if [[ -f solutions/day$(printf '%02d' "$DAY").py ]]; then
  echo "==> Verify solution"
  uv run python scripts/verify_solution.py
else
  echo "No solution file yet — Codex step may not have run"
fi

if [[ "$DRY_RUN" != "true" ]]; then
  echo "==> Submit"
  AOC_SOLVER=local uv run aoc-bot
fi

echo "==> Done. Artifacts in .aoc/"
