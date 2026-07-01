from __future__ import annotations

from collections import deque


class Intcode:
    def __init__(self, program: list[int]) -> None:
        self.program = program
        self.mem: dict[int, int] = {}
        self.ip = 0
        self.rel = 0
        self.halted = False
        self._input: deque[int] = deque()
        self.reset()

    def reset(self) -> None:
        self.mem = {i: v for i, v in enumerate(self.program)}
        self.ip = 0
        self.rel = 0
        self.halted = False
        self._input.clear()

    def _get(self, addr: int) -> int:
        return self.mem.get(addr, 0)

    def _set(self, addr: int, value: int) -> None:
        self.mem[addr] = value

    def _mode(self, mode: int, offset: int) -> int:
        if mode == 0:
            return self._get(self.ip + offset)
        if mode == 1:
            return self.ip + offset
        if mode == 2:
            return self.rel + self._get(self.ip + offset)
        raise ValueError(f"bad parameter mode {mode}")

    def _decode(self) -> tuple[int, list[int], list[int]]:
        raw = self._get(self.ip)
        opcode = raw % 100
        modes = [(raw // 100) % 10, (raw // 1000) % 10, (raw // 10000) % 10]
        if opcode in (1, 2, 7, 8):
            params = [self._mode(modes[i], i + 1) for i in range(2)]
            dest = self._mode(modes[2], 3)
            return opcode, params, [dest]
        if opcode in (3, 4):
            params = [self._mode(modes[0], 1)]
            return opcode, params, []
        if opcode in (5, 6):
            params = [self._mode(modes[i], i + 1) for i in range(2)]
            return opcode, params, []
        if opcode == 9:
            params = [self._mode(modes[0], 1)]
            return opcode, params, []
        if opcode == 99:
            return opcode, [], []
        raise ValueError(f"unknown opcode {opcode} at {self.ip}")

    def run(self, inputs: list[int]) -> list[int]:
        self.reset()
        self._input = deque(inputs)
        outputs: list[int] = []
        while not self.halted:
            opcode, params, dests = self._decode()
            if opcode == 99:
                self.halted = True
                break
            if opcode == 1:
                self._set(dests[0], self._get(params[0]) + self._get(params[1]))
                self.ip += 4
            elif opcode == 2:
                self._set(dests[0], self._get(params[0]) * self._get(params[1]))
                self.ip += 4
            elif opcode == 3:
                if not self._input:
                    raise RuntimeError("intcode needs input")
                self._set(params[0], self._input.popleft())
                self.ip += 2
            elif opcode == 4:
                outputs.append(self._get(params[0]))
                self.ip += 2
            elif opcode == 5:
                self.ip = self._get(params[1]) if self._get(params[0]) else self.ip + 3
            elif opcode == 6:
                self.ip = self._get(params[1]) if not self._get(params[0]) else self.ip + 3
            elif opcode == 7:
                self._set(dests[0], int(self._get(params[0]) < self._get(params[1])))
                self.ip += 4
            elif opcode == 8:
                self._set(dests[0], int(self._get(params[0]) == self._get(params[1])))
                self.ip += 4
            elif opcode == 9:
                self.rel += self._get(params[0])
                self.ip += 2
        return outputs


def parse_program(data: str) -> list[int]:
    return [int(x) for x in data.strip().split(",")]


class BeamScanner:
    def __init__(self, program: list[int]) -> None:
        self.vm = Intcode(program)
        self.cache: dict[tuple[int, int], bool] = {}

    def __call__(self, x: int, y: int) -> bool:
        key = (x, y)
        if key not in self.cache:
            self.cache[key] = self.vm.run([x, y])[0] == 1
        return self.cache[key]


def solve(data: str) -> str:
    beam = BeamScanner(parse_program(data))
    count = sum(1 for y in range(50) for x in range(50) if beam(x, y))
    return str(count)
