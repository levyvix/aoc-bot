def solve(data: str) -> str:
    lines = data.strip().splitlines()
    timestamp = int(lines[0])
    bus_ids = [int(x) for x in lines[1].split(",") if x != "x"]

    best_bus = 0
    best_wait = float("inf")
    for bus_id in bus_ids:
        remainder = timestamp % bus_id
        wait = 0 if remainder == 0 else bus_id - remainder
        if wait < best_wait:
            best_wait = wait
            best_bus = bus_id

    return str(best_bus * best_wait)
