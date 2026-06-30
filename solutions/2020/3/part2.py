def count_trees(grid: list[str], right: int, down: int) -> int:
    width = len(grid[0])
    trees = 0
    col = 0
    for row in range(0, len(grid), down):
        if grid[row][col % width] == "#":
            trees += 1
        col += right
    return trees


def solve(data: str) -> str:
    grid = data.strip().splitlines()
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    product = 1
    for right, down in slopes:
        product *= count_trees(grid, right, down)
    return str(product)
