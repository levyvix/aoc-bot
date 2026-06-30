def solve(data: str) -> str:
    ship_east, ship_north = 0, 0
    wp_east, wp_north = 10, 1

    for line in data.strip().splitlines():
        action, value = line[0], int(line[1:])
        if action == "N":
            wp_north += value
        elif action == "S":
            wp_north -= value
        elif action == "E":
            wp_east += value
        elif action == "W":
            wp_east -= value
        elif action == "L":
            for _ in range(value // 90):
                wp_east, wp_north = -wp_north, wp_east
        elif action == "R":
            for _ in range(value // 90):
                wp_east, wp_north = wp_north, -wp_east
        elif action == "F":
            ship_east += value * wp_east
            ship_north += value * wp_north

    return str(abs(ship_east) + abs(ship_north))
