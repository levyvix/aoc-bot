#!/usr/bin/env bash
# Solve one puzzle part with agent + verify (+ optional submit), retrying on failure.
#
# Usage: solve_part.sh PART [submit]
#   PART   - 1 or 2
#   submit - "true" to submit to AoC after verify passes (default: false)
#
# Env:
#   AOC_MAX_ATTEMPTS - max tries (default: 3)
#   CURSOR_API_KEY   - required
#   AOC_SESSION      - required when submit=true
set -euo pipefail

PART="${1:?usage: solve_part.sh PART [submit]}"
SUBMIT="${2:-false}"
MAX_ATTEMPTS="${AOC_MAX_ATTEMPTS:-3}"

BASE_PROMPT=".aoc/prompt-part${PART}.md"
FEEDBACK=".aoc/retry-feedback-part${PART}.txt"

if [[ ! -f "$BASE_PROMPT" ]]; then
  echo "ERROR: missing $BASE_PROMPT — run render_prompt.py --part $PART first" >&2
  exit 1
fi

rm -f "$FEEDBACK"

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  echo ""
  echo "========== Part ${PART} — attempt ${attempt}/${MAX_ATTEMPTS} =========="

  PROMPT="$BASE_PROMPT"
  OUTPUT=".aoc/agent-output-part${PART}-attempt${attempt}.md"

  if [[ "$attempt" -gt 1 ]]; then
    if [[ ! -f "$FEEDBACK" ]]; then
      echo "ERROR: expected feedback file $FEEDBACK for retry" >&2
      exit 1
    fi
    PROMPT=".aoc/prompt-part${PART}-attempt${attempt}.md"
    uv run python scripts/append_retry_prompt.py \
      --part "$PART" \
      --attempt "$attempt" \
      --base "$BASE_PROMPT" \
      --feedback "$FEEDBACK" \
      --output "$PROMPT"
  fi

  if ! bash scripts/run_cursor_agent.sh "$PROMPT" "$OUTPUT"; then
    echo "Cursor agent failed on attempt $attempt" | tee "$FEEDBACK"
    if [[ "$attempt" -eq "$MAX_ATTEMPTS" ]]; then
      exit 1
    fi
    continue
  fi

  if ! VERIFY_OUT="$(AOC_PART="$PART" uv run python scripts/verify_solution.py 2>&1)"; then
    echo "$VERIFY_OUT"
    {
      echo "Verification failed on attempt ${attempt}."
      echo "$VERIFY_OUT"
    } | tee "$FEEDBACK" >/dev/null
    if [[ "$attempt" -eq "$MAX_ATTEMPTS" ]]; then
      exit 1
    fi
    continue
  fi
  echo "$VERIFY_OUT"

  if [[ "$SUBMIT" != "true" ]]; then
    echo "Part $PART solved (verify OK, submit skipped)"
    exit 0
  fi

  if SUBMIT_OUT="$(AOC_PART="$PART" uv run python scripts/submit_part.py 2>&1)"; then
    echo "$SUBMIT_OUT"
    echo "Part $PART accepted by AoC"
    exit 0
  fi

  echo "$SUBMIT_OUT"
  if [[ "$attempt" -eq "$MAX_ATTEMPTS" ]]; then
    echo "Part $PART failed after $MAX_ATTEMPTS attempts" >&2
    exit 1
  fi
  echo "Wrong answer — retrying with feedback for agent..."
done

exit 1
