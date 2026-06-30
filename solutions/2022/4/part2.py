def parse_pair(line: str) -> tuple[tuple[int, int], tuple[int, int]]:
    left, right = line.split(",")
    a, b = map(int, left.split("-"))
    c, d = map(int, right.split("-"))
    return (a, b), (c, d)


def overlaps(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[1] and b[0] <= a[1]


def solve(data: str) -> str:
    count = 0
    for line in data.strip().splitlines():
        if not line:
            continue
        first, second = parse_pair(line)
        if overlaps(first, second):
            count += 1
    return str(count)
