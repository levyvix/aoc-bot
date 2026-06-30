def solve(data: str) -> str:
    values: dict[str, int] = {}
    gates: list[tuple[str, str, str, str]] = []

    for line in data.strip().splitlines():
        if ": " in line:
            wire, val = line.split(": ")
            values[wire] = int(val)
        elif " -> " in line:
            lhs, out = line.split(" -> ")
            in1, op, in2 = lhs.split()
            gates.append((in1, op, in2, out))

    pending = list(gates)
    while pending:
        next_pending: list[tuple[str, str, str, str]] = []
        for in1, op, in2, out in pending:
            if in1 not in values or in2 not in values:
                next_pending.append((in1, op, in2, out))
                continue
            v1, v2 = values[in1], values[in2]
            if op == "AND":
                values[out] = v1 & v2
            elif op == "OR":
                values[out] = v1 | v2
            else:
                values[out] = v1 ^ v2
        if len(next_pending) == len(pending):
            break
        pending = next_pending

    z_bits = sorted(
        ((wire, bit) for wire, bit in values.items() if wire.startswith("z")),
        key=lambda item: int(item[0][1:]),
        reverse=True,
    )
    binary = "".join(str(bit) for _, bit in z_bits)
    return str(int(binary, 2))
