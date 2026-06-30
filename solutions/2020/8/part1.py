def solve(data: str) -> str:
    instructions = [line.split() for line in data.strip().splitlines()]
    acc = 0
    pc = 0
    seen: set[int] = set()

    while pc not in seen:
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

    return str(acc)
