def solve(data: str) -> str:
    grid = data.splitlines()
    rows = len(grid)
    total = 0

    for r, line in enumerate(grid):
        c = 0
        while c < len(line):
            if line[c].isdigit():
                start = c
                while c < len(line) and line[c].isdigit():
                    c += 1
                num = int(line[start:c])
                adjacent = False
                for pos_c in range(start, c):
                    for dr, dc in (
                        (-1, -1), (-1, 0), (-1, 1),
                        (0, -1),           (0, 1),
                        (1, -1),  (1, 0),  (1, 1),
                    ):
                        nr, nc = r + dr, pos_c + dc
                        if 0 <= nr < rows and 0 <= nc < len(grid[nr]):
                            ch = grid[nr][nc]
                            if ch != "." and not ch.isdigit():
                                adjacent = True
                                break
                    if adjacent:
                        break
                if adjacent:
                    total += num
            else:
                c += 1

    return str(total)
