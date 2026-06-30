def _run(instructions: list[list[str]]) -> int | None:
    acc = 0
    pc = 0
    seen: set[int] = set()
    n = len(instructions)

    while 0 <= pc < n:
        if pc in seen:
            return None
        seen.add(pc)
        op, arg = instructions[pc]
        value = int(arg)
        if op == "acc":
            acc += value
            pc += 1
        elif op == "jmp":
            pc += value
        else:  # nop
            pc += 1

    return acc if pc == n else None


def solve(data: str) -> str:
    original = [line.split() for line in data.strip().splitlines()]

    for i, (op, arg) in enumerate(original):
        if op not in ("jmp", "nop"):
            continue
        flipped = [inst[:] for inst in original]
        flipped[i][0] = "nop" if op == "jmp" else "jmp"
        result = _run(flipped)
        if result is not None:
            return str(result)

    raise RuntimeError("no fix found")
