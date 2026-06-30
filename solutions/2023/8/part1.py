def solve(data: str) -> str:
    lines = data.strip().splitlines()
    instructions = lines[0]

    network = {}
    for line in lines[1:]:
        if not line.strip():
            continue
        node, rest = line.split(" = ")
        left, right = rest.strip("()").split(", ")
        network[node] = (left, right)

    current = "AAA"
    steps = 0
    while current != "ZZZ":
        direction = instructions[steps % len(instructions)]
        current = network[current][0 if direction == "L" else 1]
        steps += 1

    return str(steps)
