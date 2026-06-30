def parse_pair(line: str) -> tuple[tuple[int, int], tuple[int, int]]:
    left, right = line.split(",")
    a, b = map(int, left.split("-"))
    c, d = map(int, right.split("-"))
    return (a, b), (c, d)


def contains(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[0] and a[1] >= b[1]


def solve(data: str) -> str:
    count = 0
    for line in data.strip().splitlines():
        if not line:
            continue
        first, second = parse_pair(line)
        if contains(first, second) or contains(second, first):
            count += 1
    return str(count)
