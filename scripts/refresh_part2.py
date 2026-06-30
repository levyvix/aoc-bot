#!/usr/bin/env python3
"""Re-fetch puzzle page after Part 1 — delegates to aoc_tool."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    tool = Path(__file__).resolve().parent / "aoc_tool.py"
    raise SystemExit(subprocess.call([sys.executable, str(tool), "refresh"]))
