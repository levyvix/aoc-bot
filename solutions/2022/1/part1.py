def solve(data: str) -> str:
    max_calories = 0
    current = 0
    for line in data.splitlines():
        if not line.strip():
            max_calories = max(max_calories, current)
            current = 0
        else:
            current += int(line)
    max_calories = max(max_calories, current)
    return str(max_calories)
