import re


def solve(data: str) -> str:
    enabled = True
    total = 0
    pattern = re.compile(r"don't\(\)|do\(\)|mul\((\d{1,3}),(\d{1,3})\)")
    for m in pattern.finditer(data):
        s = m.group(0)
        if s == "do()":
            enabled = True
        elif s == "don't()":
            enabled = False
        elif enabled:
            total += int(m.group(1)) * int(m.group(2))
    return str(total)
