MOD = 20183


def _parse(data: str) -> tuple[int, int, int]:
    depth = 0
    target_x = 0
    target_y = 0
    for line in data.strip().splitlines():
        line = line.strip()
        if line.startswith("depth:"):
            depth = int(line.split(":")[1].strip())
        elif line.startswith("target:"):
            coords = line.split(":")[1].strip().split(",")
            target_x = int(coords[0])
            target_y = int(coords[1])
    return depth, target_x, target_y


def _geologic_index(
    x: int,
    y: int,
    depth: int,
    target_x: int,
    target_y: int,
    erosion: list[list[int]],
) -> int:
    if (x, y) == (0, 0) or (x, y) == (target_x, target_y):
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return erosion[y][x - 1] * erosion[y - 1][x]


def solve(data: str) -> str:
    depth, target_x, target_y = _parse(data)
    erosion = [[0] * (target_x + 1) for _ in range(target_y + 1)]

    total = 0
    for y in range(target_y + 1):
        for x in range(target_x + 1):
            gi = _geologic_index(x, y, depth, target_x, target_y, erosion)
            erosion[y][x] = (gi + depth) % MOD
            total += erosion[y][x] % 3

    return str(total)
