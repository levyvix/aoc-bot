def parse_program(data: str) -> list[int]:
    return [int(x) for x in data.strip().split(",")]


class Intcode:
    def __init__(self, program: list[int]) -> None:
        self.memory = dict(enumerate(program))
        self.ip = 0
        self.relative_base = 0
        self.halted = False

    def _read(self, addr: int) -> int:
        return self.memory.get(addr, 0)

    def _write(self, addr: int, value: int) -> None:
        self.memory[addr] = value

    def _mode(self, instruction: int, n: int) -> int:
        return (instruction // (10 ** (n + 1))) % 10

    def _param(self, n: int) -> int:
        instruction = self._read(self.ip)
        mode = self._mode(instruction, n)
        addr = self.ip + n
        if mode == 0:
            return self._read(self._read(addr))
        if mode == 1:
            return self._read(addr)
        return self._read(self.relative_base + self._read(addr))

    def _param_addr(self, n: int) -> int:
        instruction = self._read(self.ip)
        mode = self._mode(instruction, n)
        addr = self.ip + n
        if mode == 0:
            return self._read(addr)
        if mode == 1:
            raise ValueError("immediate mode not valid for write")
        return self.relative_base + self._read(addr)

    def run(self, inputs: list[int]) -> list[int]:
        outputs: list[int] = []
        input_idx = 0

        while not self.halted:
            instruction = self._read(self.ip) % 100
            if instruction == 99:
                self.halted = True
                break
            if instruction == 1:
                self._write(
                    self._param_addr(3),
                    self._param(1) + self._param(2),
                )
                self.ip += 4
            elif instruction == 2:
                self._write(
                    self._param_addr(3),
                    self._param(1) * self._param(2),
                )
                self.ip += 4
            elif instruction == 3:
                if input_idx >= len(inputs):
                    raise RuntimeError("out of input")
                self._write(self._param_addr(1), inputs[input_idx])
                input_idx += 1
                self.ip += 2
            elif instruction == 4:
                outputs.append(self._param(1))
                self.ip += 2
            elif instruction == 5:
                if self._param(1) != 0:
                    self.ip = self._param(2)
                else:
                    self.ip += 3
            elif instruction == 6:
                if self._param(1) == 0:
                    self.ip = self._param(2)
                else:
                    self.ip += 3
            elif instruction == 7:
                self._write(
                    self._param_addr(3),
                    1 if self._param(1) < self._param(2) else 0,
                )
                self.ip += 4
            elif instruction == 8:
                self._write(
                    self._param_addr(3),
                    1 if self._param(1) == self._param(2) else 0,
                )
                self.ip += 4
            elif instruction == 9:
                self.relative_base += self._param(1)
                self.ip += 2
            else:
                raise ValueError(f"unknown opcode {instruction}")

        return outputs


SPRINGSCRIPT_WALK = """\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""


def springscript_input(program: str) -> list[int]:
    return [ord(c) for c in program] + [10]


def solve(data: str) -> str:
    program = parse_program(data)
    inputs = springscript_input(SPRINGSCRIPT_WALK)
    outputs = Intcode(program).run(inputs)
    return str(outputs[-1])
