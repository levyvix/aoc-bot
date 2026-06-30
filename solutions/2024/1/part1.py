def solve(data: str) -> str:
    left: list[int] = []
    right: list[int] = []
    for line in data.splitlines():
        if not line.strip():
            continue
        a, b = line.split()
        left.append(int(a))
        right.append(int(b))

    left.sort()
    right.sort()
    total = sum(abs(a - b) for a, b in zip(left, right))
    return str(total)
