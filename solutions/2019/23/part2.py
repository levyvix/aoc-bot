from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load_part1():
    path = Path(__file__).with_name("part1.py")
    spec = spec_from_file_location("aoc_2019_23_part1_shared", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_part1 = _load_part1()
NetworkComputer = _part1.NetworkComputer
parse_program = _part1.parse_program


def run_network_nat(program: list[int], n: int = 50) -> int:
    computers = [NetworkComputer(program, i) for i in range(n)]
    pending: list[list[int]] = [[] for _ in range(n)]
    nat_packet: tuple[int, int] | None = None
    last_nat_y: int | None = None

    while True:
        activity = False
        for i, comp in enumerate(computers):
            if comp.vm.halted:
                continue
            outputs = comp.run_until_idle()
            if outputs:
                activity = True
            for output in outputs:
                pending[i].append(output)
                if len(pending[i]) == 3:
                    dest, x, y = pending[i]
                    pending[i] = []
                    if dest == 255:
                        nat_packet = (x, y)
                    elif 0 <= dest < n:
                        computers[dest].queue.append((x, y))

        if activity or nat_packet is None:
            continue

        x, y = nat_packet
        computers[0].queue.append((x, y))
        if last_nat_y == y:
            return y
        last_nat_y = y


def solve(data: str) -> str:
    program = parse_program(data)
    return str(run_network_nat(program))
