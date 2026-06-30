def solve(data: str) -> str:
    a = b = c = 0
    program = []

    for line in data.strip().splitlines():
        if line.startswith("Register A:"):
            a = int(line.split(":")[1].strip())
        elif line.startswith("Register B:"):
            b = int(line.split(":")[1].strip())
        elif line.startswith("Register C:"):
            c = int(line.split(":")[1].strip())
        elif line.startswith("Program:"):
            program = list(map(int, line.split(":")[1].strip().split(",")))

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

    output = []
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

    return ",".join(map(str, output))
