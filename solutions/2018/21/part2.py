def _hash(r4: int, initial: int, multiplier: int) -> int:
    value = r4
    result = initial
    while True:
        result = (result + (value & 255)) & 0xFFFFFF
        result = (result * multiplier) & 0xFFFFFF
        value >>= 8
        if value == 0:
            break
    return result


def _parse_constants(data: str) -> tuple[int, int, int]:
    lines = [line.strip() for line in data.strip().splitlines() if line.strip()]
    instructions = [line.split() for line in lines[1:]]
    initial = int(instructions[7][1])
    multiplier = int(instructions[11][2])
    base = int(instructions[6][2])
    return initial, multiplier, base


def solve(data: str) -> str:
    initial, multiplier, base = _parse_constants(data)
    seen: set[int] = set()
    r4 = base
    last = 0
    while True:
        value = _hash(r4, initial, multiplier)
        if value in seen:
            break
        seen.add(value)
        last = value
        r4 = value | base
    return str(last)
