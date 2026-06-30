def solve(data: str) -> str:
    horizontal = 0
    depth = 0
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        cmd, value = line.split()
        n = int(value)
        if cmd == "forward":
            horizontal += n
        elif cmd == "down":
            depth += n
        elif cmd == "up":
            depth -= n
    return str(horizontal * depth)
