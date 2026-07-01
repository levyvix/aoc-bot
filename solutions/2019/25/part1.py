from __future__ import annotations

import re
from collections import deque
from itertools import combinations

OPPOSITE = {"north": "south", "south": "north", "east": "west", "west": "east"}
DIRECTIONS = ("north", "south", "east", "west")
DANGEROUS = frozenset(
    {
        "photons",
        "escape pod",
        "molten lava",
        "infinite loop",
        "infinite loop detector",
        "giant electromagnet",
    }
)


class Intcode:
    def __init__(self, program: list[int]) -> None:
        self.mem = {i: v for i, v in enumerate(program)}
        self.ip = 0
        self.rel = 0
        self.halted = False
        self._input: deque[int] = deque()
        self._output: deque[int] = deque()

    def queue_input(self, values: list[int]) -> None:
        self._input.extend(values)

    def send(self, text: str) -> None:
        self.queue_input([ord(c) for c in text + "\n"])

    def read_output(self) -> str:
        chars: list[str] = []
        while self._output:
            value = self._output.popleft()
            if value == 10:
                break
            chars.append(chr(value))
        return "".join(chars)

    def read_all_output(self) -> str:
        parts: list[str] = []
        while True:
            line = self.read_output()
            if not line and not self._output:
                break
            if line:
                parts.append(line)
        return "\n".join(parts)

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

    def run_until_input_or_halt(self) -> None:
        while not self.halted:
            opcode, params, dests = self._decode()
            if opcode == 99:
                self.halted = True
                return
            if opcode == 1:
                self._set(dests[0], self._get(params[0]) + self._get(params[1]))
                self.ip += 4
            elif opcode == 2:
                self._set(dests[0], self._get(params[0]) * self._get(params[1]))
                self.ip += 4
            elif opcode == 3:
                if not self._input:
                    return
                self._set(params[0], self._input.popleft())
                self.ip += 2
            elif opcode == 4:
                self._output.append(self._get(params[0]))
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


def _parse_room(text: str) -> tuple[str, set[str], list[str]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    name = ""
    doors: set[str] = set()
    items: list[str] = []
    section = ""

    for line in lines:
        if line.startswith("== ") and line.endswith(" =="):
            name = line[3:-3]
            continue
        if line == "Doors here lead:":
            section = "doors"
            continue
        if line == "Items here:":
            section = "items"
            continue
        if line.startswith("- "):
            value = line[2:]
            if section == "doors" and value in DIRECTIONS:
                doors.add(value)
            elif section == "items":
                items.append(value)

    return name, doors, items


def _collect_output(computer: Intcode) -> str:
    computer.run_until_input_or_halt()
    chunks: list[str] = []
    while computer._output:
        value = computer._output.popleft()
        chunks.append(chr(value))
    return "".join(chunks)


def _command(computer: Intcode, cmd: str) -> str:
    computer.send(cmd)
    return _collect_output(computer)


def _move(computer: Intcode, direction: str) -> str:
    return _command(computer, direction)


def _take(computer: Intcode, item: str) -> None:
    _command(computer, f"take {item}")


def _drop(computer: Intcode, item: str) -> None:
    _command(computer, f"drop {item}")


def _explore(
    computer: Intcode,
    output: str,
    visited: set[str],
    doors: dict[str, set[str]],
    graph: dict[str, dict[str, str]],
    inventory: list[str],
) -> None:
    name, room_doors, room_items = _parse_room(output)
    if not name:
        return
    visited.add(name)
    doors[name] = room_doors

    for item in room_items:
        if item in DANGEROUS:
            continue
        if item not in inventory:
            _take(computer, item)
            inventory.append(item)

    for direction in room_doors:
        out = _move(computer, direction)
        next_name, _, _ = _parse_room(out)
        if not next_name or "You can't go that way" in out:
            _move(computer, OPPOSITE[direction])
            continue
        graph.setdefault(name, {})[direction] = next_name
        graph.setdefault(next_name, {})[OPPOSITE[direction]] = name
        if next_name not in visited:
            _explore(computer, out, visited, doors, graph, inventory)
        _move(computer, OPPOSITE[direction])


def _find_security(rooms: set[str]) -> str | None:
    for name in rooms:
        if "Security" in name:
            return name
    return None


def _path_to_room(start: str, goal: str, graph: dict[str, dict[str, str]]) -> list[str]:
    if start == goal:
        return []
    queue: deque[tuple[str, list[str]]] = deque([(start, [])])
    seen = {start}
    while queue:
        room, path = queue.popleft()
        for direction, nroom in graph.get(room, {}).items():
            if nroom in seen:
                continue
            npath = path + [direction]
            if nroom == goal:
                return npath
            seen.add(nroom)
            queue.append((nroom, npath))
    return []


def _path_to(computer: Intcode, path: list[str]) -> None:
    for direction in path:
        _move(computer, direction)


def _crack_weight(computer: Intcode, inventory: list[str]) -> str:
    held = set(inventory)
    for size in range(len(inventory) + 1):
        for combo in combinations(range(len(inventory)), size):
            target = {inventory[i] for i in combo}
            for item in inventory:
                if item in held and item not in target:
                    _drop(computer, item)
                    held.discard(item)
                elif item not in held and item in target:
                    _take(computer, item)
                    held.add(item)

            out = _move(computer, "west")
            if computer.halted:
                match = re.search(r"\b(\d{5,})\b", out)
                if match:
                    return match.group(1)
                match = re.search(r"\b(\d+)\b", out)
                if match:
                    return match.group(1)
                raise RuntimeError(f"passed sensor but no password in output: {out!r}")

            _move(computer, "east")

    raise RuntimeError("could not find correct item combination")


def solve(data: str) -> str:
    program = [int(x) for x in data.strip().split(",")]
    computer = Intcode(program)

    visited: set[str] = set()
    doors: dict[str, set[str]] = {}
    graph: dict[str, dict[str, str]] = {}
    inventory: list[str] = []

    initial = _collect_output(computer)
    _explore(computer, initial, visited, doors, graph, inventory)

    security = _find_security(visited)
    if security is None:
        raise RuntimeError(f"security room not found; rooms={sorted(visited)}")

    start = "Hull Breach"
    _path_to(computer, _path_to_room(start, security, graph))

    return _crack_weight(computer, inventory)
