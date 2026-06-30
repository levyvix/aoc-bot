def _seat_id(boarding_pass: str) -> int:
    row = int("".join("0" if c == "F" else "1" for c in boarding_pass[:7]), 2)
    col = int("".join("0" if c == "L" else "1" for c in boarding_pass[7:]), 2)
    return row * 8 + col


def solve(data: str) -> str:
    ids = {_seat_id(line.strip()) for line in data.splitlines() if line.strip()}
    for seat_id in range(min(ids) + 1, max(ids)):
        if seat_id not in ids and seat_id - 1 in ids and seat_id + 1 in ids:
            return str(seat_id)
    raise ValueError("no missing seat found")
