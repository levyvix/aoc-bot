#!/usr/bin/env bash
# Run Cursor agent headlessly in CI (reads prompt from file).
set -euo pipefail

PROMPT_FILE="${1:-.aoc/codex-prompt.md}"
MODEL="${CURSOR_MODEL:-composer-2.5}"
OUTPUT="${2:-.aoc/agent-output.md}"

if [[ -z "${CURSOR_API_KEY:-}" ]]; then
  echo "ERROR: CURSOR_API_KEY is not set" >&2
  exit 1
fi

if [[ -z "${AOC_YEAR:-}" || -z "${AOC_DAY:-}" ]]; then
  echo "ERROR: AOC_YEAR and AOC_DAY must be set" >&2
  exit 1
fi

export AOC_YEAR AOC_DAY

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "ERROR: prompt file not found: $PROMPT_FILE" >&2
  exit 1
fi

PROMPT="$(cat "$PROMPT_FILE")"

echo "==> Cursor agent (model=$MODEL, year=$AOC_YEAR, day=$AOC_DAY)"
agent -p "$PROMPT" --force --model "$MODEL" --output-format text | tee "$OUTPUT"
