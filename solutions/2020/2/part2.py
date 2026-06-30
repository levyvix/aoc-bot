def solve(data: str) -> str:
    valid = 0
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        policy, password = line.split(": ")
        lo_hi, letter = policy.split()
        pos1, pos2 = map(int, lo_hi.split("-"))
        at1 = len(password) >= pos1 and password[pos1 - 1] == letter
        at2 = len(password) >= pos2 and password[pos2 - 1] == letter
        if at1 ^ at2:
            valid += 1
    return str(valid)
