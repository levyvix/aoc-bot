def hash_string(s: str) -> int:
    value = 0
    for ch in s:
        value = (value + ord(ch)) * 17 % 256
    return value


def solve(data: str) -> str:
    steps = data.replace("\n", "").split(",")
    total = sum(hash_string(step) for step in steps if step)
    return str(total)
