from collections import defaultdict, deque
from functools import reduce
from math import gcd


def _parse(data: str):
    modules: dict[str, dict] = {}
    for line in data.strip().splitlines():
        left, right = line.split(" -> ")
        dests = [d.strip() for d in right.split(", ")]

        if left.startswith("%"):
            modules[left[1:]] = {"type": "flip", "dests": dests}
        elif left.startswith("&"):
            modules[left[1:]] = {"type": "conj", "dests": dests}
        elif left == "broadcaster":
            modules["broadcaster"] = {"type": "broadcast", "dests": dests}
        else:
            modules[left] = {"type": "plain", "dests": dests}

    inputs: dict[str, list[str]] = defaultdict(list)
    for name, mod in modules.items():
        for dest in mod["dests"]:
            inputs[dest].append(name)

    conj_memory = {
        name: {src: False for src in inputs[name]}
        for name, mod in modules.items()
        if mod["type"] == "conj"
    }
    return modules, conj_memory, inputs


def _lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def solve(data: str) -> str:
    modules, conj_memory, inputs = _parse(data)

    rx_feeder = next(name for name, mod in modules.items() if "rx" in mod["dests"])
    watch = inputs[rx_feeder]

    flip_on = {name: False for name, mod in modules.items() if mod["type"] == "flip"}
    memory = {name: dict(states) for name, states in conj_memory.items()}
    first_high: dict[str, int] = {}
    press = 0

    while len(first_high) < len(watch):
        press += 1
        queue: deque[tuple[str, str, bool]] = deque([("button", "broadcaster", False)])

        while queue:
            src, dst, pulse = queue.popleft()

            if dst == rx_feeder and pulse and src in watch and src not in first_high:
                first_high[src] = press

            if dst not in modules:
                continue

            mod = modules[dst]
            if mod["type"] == "broadcast":
                for dest in mod["dests"]:
                    queue.append((dst, dest, pulse))
            elif mod["type"] == "flip":
                if pulse:
                    continue
                flip_on[dst] = not flip_on[dst]
                out = flip_on[dst]
                for dest in mod["dests"]:
                    queue.append((dst, dest, out))
            elif mod["type"] == "conj":
                memory[dst][src] = pulse
                out = not all(memory[dst].values())
                for dest in mod["dests"]:
                    queue.append((dst, dest, out))

    return str(reduce(_lcm, first_high.values()))
