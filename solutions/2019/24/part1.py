def solve(data: str) -> str:
    grid = [line.strip() for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])

    def biodiversity(g: list[str]) -> int:
        score = 0
        for i, row in enumerate(g):
            for j, cell in enumerate(row):
                if cell == "#":
                    score += 1 << (i * cols + j)
        return score

    def step(g: list[str]) -> list[str]:
        new_grid: list[str] = []
        for i in range(rows):
            row_chars: list[str] = []
            for j in range(cols):
                neighbors = 0
                for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and g[ni][nj] == "#":
                        neighbors += 1
                if g[i][j] == "#":
                    row_chars.append("#" if neighbors == 1 else ".")
                else:
                    row_chars.append("#" if neighbors in (1, 2) else ".")
            new_grid.append("".join(row_chars))
        return new_grid

    seen = {tuple(grid)}
    while True:
        grid = step(grid)
        key = tuple(grid)
        if key in seen:
            return str(biodiversity(grid))
        seen.add(key)
