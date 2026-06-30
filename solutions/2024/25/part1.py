def solve(data: str) -> str:
    blocks = data.strip().split("\n\n")

    locks: list[tuple[int, ...]] = []
    keys: list[tuple[int, ...]] = []

    for block in blocks:
        lines = block.splitlines()
        heights = tuple(
            sum(line[c] == "#" for line in lines[1:6]) for c in range(5)
        )
        if lines[0][0] == "#":
            locks.append(heights)
        else:
            keys.append(heights)

    count = 0
    for lock in locks:
        for key in keys:
            if all(a + b <= 5 for a, b in zip(lock, key)):
                count += 1

    return str(count)
