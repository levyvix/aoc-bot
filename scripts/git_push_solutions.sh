#!/usr/bin/env bash
# Stage solutions/YEAR/DAY, commit, rebase on remote, push.
set -euo pipefail

YEAR="${1:?year required}"
DAY="${2:?day required}"

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
git pull --rebase --autostash origin "$BRANCH"

git add "solutions/${YEAR}/${DAY}/"
if git diff --staged --quiet; then
  echo "No solution changes to commit for ${YEAR} day ${DAY}"
  exit 0
fi

git commit -m "aoc: ${YEAR} day ${DAY} solutions"
git pull --rebase --autostash origin "$BRANCH"
git push origin "HEAD:${BRANCH}"
