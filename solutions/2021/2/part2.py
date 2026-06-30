def solve(data: str) -> str:
    horizontal = 0
    depth = 0
    aim = 0
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        cmd, value = line.split()
        n = int(value)
        if cmd == "forward":
            horizontal += n
            depth += aim * n
        elif cmd == "down":
            aim += n
        elif cmd == "up":
            aim -= n
    return str(horizontal * depth)
