def apply_mask(value: int, mask: str) -> int:
    for i, ch in enumerate(mask):
        bit = 35 - i
        if ch == "0":
            value &= ~(1 << bit)
        elif ch == "1":
            value |= 1 << bit
    return value


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
            memory[addr] = apply_mask(value, mask)
    return str(sum(memory.values()))
