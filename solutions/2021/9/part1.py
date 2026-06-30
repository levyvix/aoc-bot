def solve(data: str) -> str:
    grid = [list(line.strip()) for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])
    total = 0
    for r in range(rows):
        for c in range(cols):
            h = int(grid[r][c])
            neighbors = []
            if r > 0:
                neighbors.append(int(grid[r - 1][c]))
            if r < rows - 1:
                neighbors.append(int(grid[r + 1][c]))
            if c > 0:
                neighbors.append(int(grid[r][c - 1]))
            if c < cols - 1:
                neighbors.append(int(grid[r][c + 1]))
            if all(h < n for n in neighbors):
                total += h + 1
    return str(total)
