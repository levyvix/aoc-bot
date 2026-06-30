from collections import Counter


def solve(data: str) -> str:
    left: list[int] = []
    right: list[int] = []
    for line in data.splitlines():
        if not line.strip():
            continue
        a, b = line.split()
        left.append(int(a))
        right.append(int(b))

    right_counts = Counter(right)
    total = sum(n * right_counts[n] for n in left)
    return str(total)
