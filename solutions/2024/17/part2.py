def parse(data: str) -> tuple[int, int, int, list[int]]:
    a = b = c = 0
    program: list[int] = []

    for line in data.strip().splitlines():
        if line.startswith("Register A:"):
            a = int(line.split(":")[1].strip())
        elif line.startswith("Register B:"):
            b = int(line.split(":")[1].strip())
        elif line.startswith("Register C:"):
            c = int(line.split(":")[1].strip())
        elif line.startswith("Program:"):
            program = list(map(int, line.split(":")[1].strip().split(",")))

    return a, b, c, program


def run(a: int, b: int, c: int, program: list[int]) -> list[int]:
    def combo(op: int) -> int:
        if op <= 3:
            return op
        if op == 4:
            return a
        if op == 5:
            return b
        if op == 6:
            return c
        raise ValueError(f"invalid combo operand {op}")

    output: list[int] = []
    ip = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]

        if opcode == 0:
            a = a // (2 ** combo(operand))
        elif opcode == 1:
            b = b ^ operand
        elif opcode == 2:
            b = combo(operand) % 8
        elif opcode == 3:
            if a != 0:
                ip = operand
                continue
        elif opcode == 4:
            b = b ^ c
        elif opcode == 5:
            output.append(combo(operand) % 8)
        elif opcode == 6:
            b = a // (2 ** combo(operand))
        elif opcode == 7:
            c = a // (2 ** combo(operand))
        else:
            raise ValueError(f"unknown opcode {opcode}")

        ip += 2

    return output


def solve(data: str) -> str:
    _, _, _, program = parse(data)

    candidates = [0]
    for step in range(len(program)):
        expected_len = step + 1
        next_candidates: list[int] = []
        suffix = program[-expected_len:]
        for a in candidates:
            for digit in range(8):
                new_a = (a << 3) | digit
                out = run(new_a, 0, 0, program)
                if len(out) == expected_len and out == suffix:
                    next_candidates.append(new_a)
        candidates = next_candidates

    return str(min(a for a in candidates if a > 0))
