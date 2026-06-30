def solve(data: str) -> str:
    count = 0
    for line in data.splitlines():
        if not line.strip():
            continue
        levels = [int(x) for x in line.split()]
        if is_safe_with_dampener(levels):
            count += 1
    return str(count)


def is_safe(levels: list[int]) -> bool:
    if len(levels) < 2:
        return True
    diffs = [b - a for a, b in zip(levels, levels[1:])]
    if all(d > 0 for d in diffs):
        pass
    elif all(d < 0 for d in diffs):
        pass
    else:
        return False
    return all(1 <= abs(d) <= 3 for d in diffs)


def is_safe_with_dampener(levels: list[int]) -> bool:
    if is_safe(levels):
        return True
    for i in range(len(levels)):
        if is_safe(levels[:i] + levels[i + 1 :]):
            return True
    return False
