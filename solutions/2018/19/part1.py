def solve(data: str) -> str:
    lines = [line.strip() for line in data.strip().splitlines() if line.strip()]

    ip_reg = int(lines[0].split()[1])
    instructions = []
    for line in lines[1:]:
        parts = line.split()
        op = parts[0]
        args = tuple(int(x) for x in parts[1:])
        instructions.append((op, args))

    regs = [0] * 6
    ip = 0
    n = len(instructions)

    while 0 <= ip < n:
        regs[ip_reg] = ip
        op, (a, b, c) = instructions[ip]

        if op == "addr":
            regs[c] = regs[a] + regs[b]
        elif op == "addi":
            regs[c] = regs[a] + b
        elif op == "mulr":
            regs[c] = regs[a] * regs[b]
        elif op == "muli":
            regs[c] = regs[a] * b
        elif op == "banr":
            regs[c] = regs[a] & regs[b]
        elif op == "bani":
            regs[c] = regs[a] & b
        elif op == "borr":
            regs[c] = regs[a] | regs[b]
        elif op == "bori":
            regs[c] = regs[a] | b
        elif op == "setr":
            regs[c] = regs[a]
        elif op == "seti":
            regs[c] = a
        elif op == "gtir":
            regs[c] = 1 if a > regs[b] else 0
        elif op == "gtri":
            regs[c] = 1 if regs[a] > b else 0
        elif op == "gtrr":
            regs[c] = 1 if regs[a] > regs[b] else 0
        elif op == "eqir":
            regs[c] = 1 if a == regs[b] else 0
        elif op == "eqri":
            regs[c] = 1 if regs[a] == b else 0
        elif op == "eqrr":
            regs[c] = 1 if regs[a] == regs[b] else 0
        else:
            raise ValueError(f"unknown opcode: {op}")

        ip = regs[ip_reg] + 1

    return str(regs[0])
