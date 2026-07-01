import importlib.util
from pathlib import Path


def solve(data: str) -> str:
    part1 = Path(__file__).with_name("part1.py")
    spec = importlib.util.spec_from_file_location("aoc_2019_day_25_part_1", part1)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {part1}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve(data)
