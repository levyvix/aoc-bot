def solve(data: str) -> str:
    blocks = data.strip().split("\n\n")
    numbers = [int(x) for x in blocks[0].split(",")]

    boards = []
    for block in blocks[1:]:
        grid = []
        for line in block.splitlines():
            grid.append([int(x) for x in line.split()])
        boards.append(grid)

    marked = [[[False] * 5 for _ in range(5)] for _ in boards]
    active = set(range(len(boards)))
    last_score = 0

    for num in numbers:
        for b in list(active):
            board = boards[b]
            for r in range(5):
                for c in range(5):
                    if board[r][c] == num:
                        marked[b][r][c] = True

            for i in range(5):
                row_win = all(marked[b][i][j] for j in range(5))
                col_win = all(marked[b][j][i] for j in range(5))
                if row_win or col_win:
                    unmarked_sum = sum(
                        board[r][c]
                        for r in range(5)
                        for c in range(5)
                        if not marked[b][r][c]
                    )
                    last_score = unmarked_sum * num
                    active.remove(b)
                    break

    return str(last_score)
