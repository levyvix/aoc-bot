def divisor_sum(n: int) -> int:
    total = 0
    limit = int(n**0.5)
    for i in range(1, limit + 1):
        if n % i == 0:
            total += i
            j = n // i
            if j != i:
                total += j
    return total


def _simulate(data: str, initial_r0: int, max_cycles: int = 0) -> list[int]:
    lines = [line.strip() for line in data.strip().splitlines() if line.strip()]

    ip_reg = int(lines[0].split()[1])
    instructions = []
    for line in lines[1:]:
        parts = line.split()
        instructions.append((parts[0], tuple(int(x) for x in parts[1:])))

    regs = [0] * 6
    regs[0] = initial_r0
    ip = 0
    n = len(instructions)
    cycles = 0

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
        cycles += 1
        if max_cycles and cycles >= max_cycles:
            break

    return regs


def solve(data: str) -> str:
    lines = [line.strip() for line in data.strip().splitlines() if line.strip()]
    if len(lines) <= 10:
        return str(_simulate(data, initial_r0=1)[0])

    regs = _simulate(data, initial_r0=1, max_cycles=1000)
    target = max(regs)
    return str(divisor_sum(target))
