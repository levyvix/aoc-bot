DIRS = "RDLU"


def solve(data: str) -> str:
    x = y = 0
    area = 0
    border = 0

    for line in data.strip().splitlines():
        hexcode = line.split()[2][2:-1]
        direction = DIRS[int(hexcode[-1])]
        distance = int(hexcode[:5], 16)
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
