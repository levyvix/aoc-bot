from __future__ import annotations


def _parse(data: str) -> tuple[str, list[str]]:
    lines = data.strip().splitlines()
    algo = lines[0].strip()
    grid = [line.strip() for line in lines[2:] if line.strip()]
    return algo, grid


def _enhance(algo: str, grid: list[str], fill: str) -> tuple[list[str], str]:
    rows, cols = len(grid), len(grid[0])

    def pixel(r: int, c: int) -> str:
        if 0 <= r < rows and 0 <= c < cols:
            return grid[r][c]
        return fill

    new_grid: list[str] = []
    for r in range(-1, rows + 1):
        row_chars: list[str] = []
        for c in range(-1, cols + 1):
            bits = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    bits = (bits << 1) | (1 if pixel(r + dr, c + dc) == "#" else 0)
            row_chars.append(algo[bits])
        new_grid.append("".join(row_chars))

    new_fill = algo[0 if fill == "." else 511]
    return new_grid, new_fill


def solve(data: str) -> str:
    algo, grid = _parse(data)
    fill = "."
    for _ in range(2):
        grid, fill = _enhance(algo, grid, fill)
    return str(sum(row.count("#") for row in grid))
