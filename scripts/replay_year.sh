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

  uv run python scripts/render_prompt.py
  bash scripts/run_cursor_agent.sh ".aoc/prompt.md" ".aoc/agent-output-${YEAR}-day${day}.md"
  uv run python scripts/final_check.py

  if [[ "$SKIP_COMMIT" != "true" ]]; then
    git config user.name "github-actions[bot]"
    git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
    git add "solutions/${YEAR}/${day}/"
    if ! git diff --staged --quiet; then
      git commit -m "aoc: ${YEAR} day ${day} solutions"
      git push
    fi
  fi
done

echo "==> Finished ${YEAR} days ${START}–${END}"
