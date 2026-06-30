def solve(data: str) -> str:
    valid = 0
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        policy, password = line.split(": ")
        lo_hi, letter = policy.split()
        lo, hi = map(int, lo_hi.split("-"))
        count = password.count(letter)
        if lo <= count <= hi:
            valid += 1
    return str(valid)
