def solve(data: str) -> str:
    grid = data.strip().splitlines()
    width = len(grid[0])
    trees = 0
    col = 0
    for row in range(0, len(grid), 1):
        if grid[row][col % width] == "#":
            trees += 1
        col += 3
    return str(trees)
