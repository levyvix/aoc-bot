def solve(data: str) -> str:
    total = 0
    for line in data.splitlines():
        if not line:
            continue
        first = last = None
        for ch in line:
            if ch.isdigit():
                if first is None:
                    first = ch
                last = ch
        total += int(first + last)
    return str(total)
