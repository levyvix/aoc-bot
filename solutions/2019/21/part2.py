import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "aoc_2019_21_part1",
    Path(__file__).with_name("part1.py"),
)
_part1 = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_part1)

Intcode = _part1.Intcode
parse_program = _part1.parse_program
springscript_input = _part1.springscript_input


SPRINGSCRIPT_RUN = """\
OR A J
AND B J
AND C J
NOT J J
AND D J
OR E T
OR H T
AND T J
RUN
"""


def solve(data: str) -> str:
    program = parse_program(data)
    inputs = springscript_input(SPRINGSCRIPT_RUN)
    outputs = Intcode(program).run(inputs)
    return str(outputs[-1])
