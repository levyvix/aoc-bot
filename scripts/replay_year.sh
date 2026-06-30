#!/usr/bin/env bash
# Solve a range of AoC days sequentially (one agent run per day).
set -euo pipefail

YEAR="${AOC_YEAR:?AOC_YEAR required}"
START="${AOC_START_DAY:-1}"
END="${AOC_END_DAY:-25}"
SKIP_COMMIT="${AOC_SKIP_COMMIT:-}"

cd "$(dirname "$0")/.."

echo "==> Replaying AoC ${YEAR} days ${START}–${END} (dry_run=${AOC_DRY_RUN:-false})"

for day in $(seq "$START" "$END"); do
  echo ""
  echo "############################################"
  echo "# ${YEAR} Day ${day}"
  echo "############################################"

  export AOC_DAY="$day"

  if [[ "$SKIP_COMMIT" != "true" ]]; then
    BRANCH="$(git rev-parse --abbrev-ref HEAD)"
    git pull --rebase origin "$BRANCH"
  fi

  need_agent=true
  if uv run python scripts/aoc_tool.py check-day --files-only; then
    uv run python scripts/aoc_tool.py prepare
    uv run python scripts/aoc_tool.py assert-day
    if uv run python scripts/aoc_tool.py check-day; then
      need_agent=false
    fi
  else
    uv run python scripts/aoc_tool.py prepare
    uv run python scripts/aoc_tool.py assert-day
  fi

  if ! $need_agent; then
    echo "SKIP: day ${day} already solved"
    continue
  fi

  uv run python scripts/render_prompt.py
  uv run python scripts/aoc_tool.py assert-day
  bash scripts/run_cursor_agent.sh ".aoc/prompt.md" ".aoc/agent-output-${YEAR}-day${day}.md"
  uv run python scripts/final_check.py

  if [[ "$SKIP_COMMIT" != "true" ]]; then
    bash scripts/git_push_solutions.sh "$YEAR" "$day"
  fi
done

echo "==> Finished ${YEAR} days ${START}–${END}"
