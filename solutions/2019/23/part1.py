from collections import deque


def parse_program(data: str) -> list[int]:
    return [int(x) for x in data.strip().split(",")]


class Intcode:
    def __init__(self, program: list[int]) -> None:
        self.memory = dict(enumerate(program))
        self.ip = 0
        self.relative_base = 0
        self.halted = False
        self.input_value: int | None = None
        self.output_value: int = 0

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

    def step_until_io(self) -> str:
        while not self.halted:
            instruction = self._read(self.ip) % 100
            if instruction == 99:
                self.halted = True
                return "halt"
            if instruction == 3:
                if self.input_value is None:
                    return "input"
                self._write(self._param_addr(1), self.input_value)
                self.input_value = None
                self.ip += 2
            elif instruction == 4:
                self.output_value = self._param(1)
                self.ip += 2
                return "output"
            elif instruction == 1:
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
        return "halt"

    def provide_input(self, value: int) -> None:
        self.input_value = value


class NetworkComputer:
    def __init__(self, program: list[int], address: int) -> None:
        self.vm = Intcode(program)
        self.address = address
        self.queue: deque[tuple[int, int]] = deque()
        self.booted = False
        self.reading_y = False
        self.pending_out: list[int] = []

    def next_input(self) -> int:
        if not self.booted:
            self.booted = True
            return self.address
        if self.queue:
            x, y = self.queue[0]
            if not self.reading_y:
                self.reading_y = True
                return x
            self.reading_y = False
            self.queue.popleft()
            return y
        self.reading_y = False
        return -1

    def run_until_idle(self) -> list[int]:
        """Run until idle (one -1 consumed) or halt. Returns outputs produced."""
        outputs: list[int] = []
        while not self.vm.halted:
            status = self.vm.step_until_io()
            if status == "halt":
                break
            if status == "output":
                outputs.append(self.vm.output_value)
            elif status == "input":
                value = self.next_input()
                self.vm.provide_input(value)
                if value == -1:
                    break
        return outputs


def deliver_packet(
    computers: list[NetworkComputer],
    pending: list[list[int]],
    dest: int,
    x: int,
    y: int,
) -> int | None:
    if dest == 255:
        return y
    if 0 <= dest < len(computers):
        computers[dest].queue.append((x, y))
    return None


def run_network(program: list[int], n: int = 50) -> int:
    computers = [NetworkComputer(program, i) for i in range(n)]
    pending: list[list[int]] = [[] for _ in range(n)]

    while True:
        for i, comp in enumerate(computers):
            if comp.vm.halted:
                continue
            for output in comp.run_until_idle():
                pending[i].append(output)
                if len(pending[i]) == 3:
                    dest, x, y = pending[i]
                    pending[i] = []
                    result = deliver_packet(computers, pending, dest, x, y)
                    if result is not None:
                        return result


def solve(data: str) -> str:
    program = parse_program(data)
    return str(run_network(program))
