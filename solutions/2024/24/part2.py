from collections import defaultdict


def solve(data: str) -> str:
    gates: dict[str, tuple[str, str, str]] = {}
    for line in data.strip().splitlines():
        if " -> " not in line:
            continue
        lhs, out = line.split(" -> ")
        a, op, b = lhs.split()
        gates[out] = (op, a, b)

    uses: dict[str, list[str]] = defaultdict(list)
    for out, (_op, a, b) in gates.items():
        uses[a].append(out)
        uses[b].append(out)

    max_z = max(int(wire[1:]) for wire in gates if wire.startswith("z"))
    swaps: set[str] = set()

    def xy_gates(bit: int) -> tuple[str | None, str | None]:
        xi, yi = f"x{bit:02d}", f"y{bit:02d}"
        xor_out = and_out = None
        for out, (op, a, b) in gates.items():
            if {a, b} != {xi, yi}:
                continue
            if op == "XOR":
                xor_out = out
            elif op == "AND":
                and_out = out
        return xor_out, and_out

    def sum_xor_output(bit: int) -> str | None:
        xor_out, _ = xy_gates(bit)
        if xor_out is None:
            return None
        for user in uses[xor_out]:
            if gates[user][0] == "XOR":
                return user
        return None

    for i in range(max_z + 1):
        z = f"z{i:02d}"
        op, a, b = gates[z]
        if i == 0:
            if op != "XOR" or {a, b} != {"x00", "y00"}:
                swaps.add(z)
        elif i == max_z:
            if op != "OR":
                swaps.add(z)
        elif op != "XOR" or a[0] in "xy" or b[0] in "xy":
            swaps.add(z)
            partner = sum_xor_output(i)
            if partner:
                swaps.add(partner)

    for i in range(1, max_z):
        z = f"z{i:02d}"
        if z in swaps:
            continue

        xor_out, and_out = xy_gates(i)
        if xor_out is None or and_out is None:
            continue

        xor_users = uses[xor_out]
        xor_ops = sorted(gates[user][0] for user in xor_users)
        if xor_ops != ["AND", "XOR"]:
            swaps.add(xor_out)
            swaps.add(and_out)

        and_users = uses[and_out]
        if len(and_users) != 1 or gates[and_users[0]][0] != "OR":
            swaps.add(xor_out)
            swaps.add(and_out)

    return ",".join(sorted(swaps))
