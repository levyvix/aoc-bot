def solve(data: str) -> str:
    grid = data.splitlines()
    rows = len(grid)

    numbers: list[tuple[int, set[tuple[int, int]]]] = []
    for r, line in enumerate(grid):
        c = 0
        while c < len(line):
            if line[c].isdigit():
                start = c
                while c < len(line) and line[c].isdigit():
                    c += 1
                num = int(line[start:c])
                positions = {(r, pos_c) for pos_c in range(start, c)}
                numbers.append((num, positions))
            else:
                c += 1

    neighbors = (
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    )

    total = 0
    for r, line in enumerate(grid):
        for c, ch in enumerate(line):
            if ch != "*":
                continue
            adjacent_nums: list[int] = []
            for num_val, positions in numbers:
                for dr, dc in neighbors:
                    if (r + dr, c + dc) in positions:
                        adjacent_nums.append(num_val)
                        break
            if len(adjacent_nums) == 2:
                total += adjacent_nums[0] * adjacent_nums[1]

    return str(total)
