def count_vertical_mismatches(grid: list[list[str]], left: int) -> int:
    h, w = len(grid), len(grid[0])
    count = 0
    for r in range(h):
        for c in range(left):
            mirror = 2 * left - 1 - c
            if mirror < w and grid[r][c] != grid[r][mirror]:
                count += 1
                if count > 1:
                    return count
    return count


def count_horizontal_mismatches(grid: list[list[str]], top: int) -> int:
    h, w = len(grid), len(grid[0])
    count = 0
    for r in range(top):
        mirror = 2 * top - 1 - r
        if mirror < h:
            for c in range(w):
                if grid[r][c] != grid[mirror][c]:
                    count += 1
                    if count > 1:
                        return count
    return count


def solve(data: str) -> str:
    total = 0
    for pattern in data.strip().split("\n\n"):
        grid = [list(row) for row in pattern.splitlines()]
        h, w = len(grid), len(grid[0])

        for left in range(1, w):
            if count_vertical_mismatches(grid, left) == 1:
                total += left
                break
        else:
            for top in range(1, h):
                if count_horizontal_mismatches(grid, top) == 1:
                    total += 100 * top
                    break

    return str(total)
