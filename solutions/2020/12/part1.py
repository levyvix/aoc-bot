def solve(data: str) -> str:
    east, north = 0, 0
    # 0=east, 90=south, 180=west, 270=north (clockwise from east)
    heading = 0

    for line in data.strip().splitlines():
        action, value = line[0], int(line[1:])
        if action == "N":
            north += value
        elif action == "S":
            north -= value
        elif action == "E":
            east += value
        elif action == "W":
            east -= value
        elif action == "L":
            heading = (heading - value) % 360
        elif action == "R":
            heading = (heading + value) % 360
        elif action == "F":
            if heading == 0:
                east += value
            elif heading == 90:
                north -= value
            elif heading == 180:
                east -= value
            elif heading == 270:
                north += value

    return str(abs(east) + abs(north))
