def decode_addresses(addr: int, mask: str) -> list[int]:
    addrs = [addr]
    for i, ch in enumerate(mask):
        bit = 35 - i
        if ch == "1":
            addrs = [a | (1 << bit) for a in addrs]
        elif ch == "X":
            new_addrs: list[int] = []
            for a in addrs:
                new_addrs.append(a & ~(1 << bit))
                new_addrs.append(a | (1 << bit))
            addrs = new_addrs
    return addrs


def solve(data: str) -> str:
    memory: dict[int, int] = {}
    mask = ""
    for line in data.strip().splitlines():
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
        else:
            addr_part, val_part = line.split(" = ")
            addr = int(addr_part[4:-1])
            value = int(val_part)
            for decoded in decode_addresses(addr, mask):
                memory[decoded] = value
    return str(sum(memory.values()))
