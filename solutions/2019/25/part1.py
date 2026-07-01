from collections import deque
import copy
import itertools
import re


def parse_program(data: str) -> list[int]:
    return [int(x) for x in data.strip().split(",")]


class Intcode:
    def __init__(self, program: list[int]) -> None:
        self.memory = dict(enumerate(program))
        self.ip = 0
        self.relative_base = 0
        self.halted = False
        self.input_value: int | None = None
        self.output_value = 0

    def copy(self) -> "Intcode":
        return copy.deepcopy(self)

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
                self._write(self._param_addr(3), self._param(1) + self._param(2))
                self.ip += 4
            elif instruction == 2:
                self._write(self._param_addr(3), self._param(1) * self._param(2))
                self.ip += 4
            elif instruction == 5:
                self.ip = self._param(2) if self._param(1) != 0 else self.ip + 3
            elif instruction == 6:
                self.ip = self._param(2) if self._param(1) == 0 else self.ip + 3
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


DIRS = ["north", "south", "east", "west"]
OPPOSITE = {"north": "south", "south": "north", "east": "west", "west": "east"}
DANGEROUS = {
    "infinite loop",
    "photons",
    "giant electromagnet",
    "escape pod",
    "molten lava",
}


def run_commands(vm: Intcode, commands: list[str]) -> str:
    output: list[str] = []
    for cmd in commands:
        for ch in cmd + "\n":
            while True:
                status = vm.step_until_io()
                if status == "output":
                    output.append(chr(vm.output_value))
                elif status == "input":
                    vm.provide_input(ord(ch))
                    break
                elif status == "halt":
                    return "".join(output)
    while True:
        status = vm.step_until_io()
        if status == "output":
            output.append(chr(vm.output_value))
        elif status in ("input", "halt"):
            break
    return "".join(output)


def parse_room(text: str) -> tuple[str, list[str], list[str]] | None:
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    if not lines or not lines[0].startswith("=="):
        return None
    name = lines[0].strip("=").strip()
    doors: list[str] = []
    items: list[str] = []
    section: str | None = None
    for line in lines[1:]:
        if line.startswith("Doors here lead:"):
            section = "doors"
            continue
        if line.startswith("Items here:"):
            section = "items"
            continue
        if line.startswith("Command?"):
            break
        if section == "doors" and line.startswith("- "):
            doors.append(line[2:])
        if section == "items" and line.startswith("- "):
            items.append(line[2:])
    return name, doors, items


def explore(program: list[int]) -> tuple[dict[str, dict], dict[str, dict[str, str]]]:
    vm = Intcode(program)
    start_out = run_commands(vm, [])
    parsed = parse_room(start_out)
    if parsed is None:
        raise RuntimeError("failed to parse starting room")
    name, doors, items = parsed
    room_info: dict[str, dict] = {name: {"doors": set(doors), "items": list(items)}}
    graph: dict[str, dict[str, str]] = {}
    queue: deque[tuple[Intcode, str]] = deque([(vm.copy(), name)])
    visited_edges: set[tuple[str, str]] = set()

    while queue:
        vm_state, room = queue.popleft()
        for direction in room_info[room]["doors"]:
            edge = (room, direction)
            if edge in visited_edges:
                continue
            visited_edges.add(edge)
            test_vm = vm_state.copy()
            out = run_commands(test_vm, [direction])
            parsed_move = parse_room(out)
            if parsed_move is None or "Alert" in out:
                continue
            next_name, next_doors, next_items = parsed_move
            graph.setdefault(room, {})[direction] = next_name
            if next_name not in room_info:
                room_info[next_name] = {
                    "doors": set(next_doors),
                    "items": list(next_items),
                }
            else:
                room_info[next_name]["doors"].update(next_doors)
            queue.append((test_vm, next_name))

    return room_info, graph


def bfs_path(
    graph: dict[str, dict[str, str]], start: str, end: str
) -> list[str] | None:
    queue: deque[tuple[str, list[str]]] = deque([(start, [])])
    seen = {start}
    while queue:
        room, path = queue.popleft()
        if room == end:
            return path
        for direction, nxt in graph.get(room, {}).items():
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, path + [direction]))
    return None


def find_password(program: list[int]) -> str:
    room_info, graph = explore(program)
    checkpoint = "Security Checkpoint"
    if checkpoint not in room_info:
        raise RuntimeError("security checkpoint not found")

    vm = Intcode(program)
    run_commands(vm, [])

    inventory: list[str] = []
    for room_name, info in room_info.items():
        for item in info["items"]:
            if item in DANGEROUS:
                continue
            path = bfs_path(graph, "Hull Breach", room_name)
            if path is None:
                continue
            run_commands(vm, path)
            run_commands(vm, [f"take {item}"])
            inventory.append(item)
            run_commands(vm, [OPPOSITE[d] for d in reversed(path)])

    path = bfs_path(graph, "Hull Breach", checkpoint)
    if path is None:
        raise RuntimeError("no path to security checkpoint")

    vm_at_checkpoint = vm.copy()
    run_commands(vm_at_checkpoint, path)

    sensor_dir = None
    for direction in DIRS:
        out = run_commands(vm_at_checkpoint.copy(), [direction])
        if "heavier" in out or "lighter" in out or "Pressure" in out:
            sensor_dir = direction
            break
    if sensor_dir is None:
        raise RuntimeError("pressure-sensitive floor not found")

    for size in range(len(inventory) + 1):
        for combo in itertools.combinations(inventory, size):
            test_vm = vm.copy()
            for item in inventory:
                run_commands(test_vm, [f"drop {item}"])
            for item in combo:
                run_commands(test_vm, [f"take {item}"])
            run_commands(test_vm, path)
            out = run_commands(test_vm, [sensor_dir])
            if "heavier" in out or "lighter" in out:
                continue
            match = re.search(r"\b(\d+)\b", out)
            if match:
                return match.group(1)

    raise RuntimeError("password not found")


def solve(data: str) -> str:
    program = parse_program(data)
    return find_password(program)
