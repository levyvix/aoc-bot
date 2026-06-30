#!/usr/bin/env bash
# Thin wrapper — delegates to aoc_tool prepare.
set -euo pipefail
cd "$(dirname "$0")/.."
exec uv run python scripts/aoc_tool.py prepare "$@"
