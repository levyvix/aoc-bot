import re

OFFSET = 10_000_000_000_000


def solve(data: str) -> str:
    total = 0
    blocks = data.strip().split("\n\n")
    for block in blocks:
        lines = block.splitlines()
        ax, ay = map(int, re.findall(r"\d+", lines[0]))
        bx, by = map(int, re.findall(r"\d+", lines[1]))
        px, py = map(int, re.findall(r"\d+", lines[2]))
        px += OFFSET
        py += OFFSET

        det = ax * by - ay * bx
        if det == 0:
            continue

        a_num = px * by - py * bx
        b_num = ax * py - ay * px
        if a_num % det != 0 or b_num % det != 0:
            continue

        a = a_num // det
        b = b_num // det
        if a < 0 or b < 0:
            continue

        total += 3 * a + b

    return str(total)
