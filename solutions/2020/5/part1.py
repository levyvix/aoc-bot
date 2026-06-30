def _seat_id(boarding_pass: str) -> int:
    row = int("".join("0" if c == "F" else "1" for c in boarding_pass[:7]), 2)
    col = int("".join("0" if c == "L" else "1" for c in boarding_pass[7:]), 2)
    return row * 8 + col


def solve(data: str) -> str:
    return str(max(_seat_id(line.strip()) for line in data.splitlines() if line.strip()))
