def solve(data: str) -> str:
    grid = [line.strip() for line in data.strip().splitlines() if line.strip()]
    rows, cols = len(grid), len(grid[0])
    word = "XMAS"
    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    ]

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != word[0]:
                continue
            for dr, dc in directions:
                match = True
                for i, ch in enumerate(word):
                    nr, nc = r + dr * i, c + dc * i
                    if nr < 0 or nr >= rows or nc < 0 or nc >= cols or grid[nr][nc] != ch:
                        match = False
                        break
                if match:
                    count += 1

    return str(count)
