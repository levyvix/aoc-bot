import math


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

    starts = [node for node in network if node.endswith("A")]

    def steps_to_z(start: str) -> int:
        current = start
        steps = 0
        while not current.endswith("Z"):
            direction = instructions[steps % len(instructions)]
            current = network[current][0 if direction == "L" else 1]
            steps += 1
        return steps

    cycle_lengths = [steps_to_z(start) for start in starts]

    result = cycle_lengths[0]
    for length in cycle_lengths[1:]:
        result = math.lcm(result, length)

    return str(result)
