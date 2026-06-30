def solve(data: str) -> str:
    x = y = 0
    area = 0
    border = 0

    for line in data.strip().splitlines():
        direction, distance, _ = line.split()
        distance = int(distance)
        border += distance

        if direction == "R":
            area -= y * distance
            x += distance
        elif direction == "L":
            area += y * distance
            x -= distance
        elif direction == "D":
            area += x * distance
            y += distance
        else:  # U
            area -= x * distance
            y -= distance

    return str(abs(area) // 2 + border // 2 + 1)
