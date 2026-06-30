import re


def solve(data: str) -> str:
    total = 0
    for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data):
        total += int(a) * int(b)
    return str(total)
