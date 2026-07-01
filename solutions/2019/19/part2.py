from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_part1():
    part1 = Path(__file__).with_name("part1.py")
    spec = importlib.util.spec_from_file_location("aoc_2019_day_19_part_1", part1)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {part1}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def solve(data: str) -> str:
    part1 = _load_part1()
    beam = part1.BeamScanner(part1.parse_program(data))

    x = 0
    y = 0
    while True:
        while not beam(x, y + 99):
            x += 1
        if beam(x + 99, y):
            return str(x * 10_000 + y)
        y += 1
