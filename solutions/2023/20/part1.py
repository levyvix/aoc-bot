from collections import defaultdict, deque


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
    return modules, conj_memory


def _simulate(modules, conj_memory, presses: int) -> tuple[int, int]:
    flip_on = {name: False for name, mod in modules.items() if mod["type"] == "flip"}
    memory = {name: dict(states) for name, states in conj_memory.items()}
    low = high = 0

    for _ in range(presses):
        queue: deque[tuple[str, str, bool]] = deque([("button", "broadcaster", False)])

        while queue:
            src, dst, pulse = queue.popleft()
            if pulse:
                high += 1
            else:
                low += 1

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

    return low, high


def solve(data: str) -> str:
    modules, conj_memory = _parse(data)
    low, high = _simulate(modules, conj_memory, 1000)
    return str(low * high)
