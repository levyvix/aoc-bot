def solve(data: str) -> str:
    lines = [line.strip() for line in data.strip().splitlines() if line.strip()]
    if not lines:
        return "0"
    width = len(lines[0])
    gamma = ""
    epsilon = ""
    for i in range(width):
        ones = sum(1 for line in lines if line[i] == "1")
        zeros = len(lines) - ones
        if ones >= zeros:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    return str(int(gamma, 2) * int(epsilon, 2))
