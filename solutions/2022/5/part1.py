def parse_stacks(stack_lines: list[str]) -> list[list[str]]:
    num_stacks = len(stack_lines[-1].split())
    stacks: list[list[str]] = [[] for _ in range(num_stacks)]
    for line in reversed(stack_lines[:-1]):
        for i, ch in enumerate(line):
            if ch.isalpha():
                stacks[i // 4].append(ch)
    return stacks


def solve(data: str) -> str:
    stack_section, move_section = data.strip().split("\n\n", 1)
    stacks = parse_stacks(stack_section.splitlines())

    for line in move_section.splitlines():
        parts = line.split()
        count, src, dst = int(parts[1]), int(parts[3]), int(parts[5])
        for _ in range(count):
            stacks[dst - 1].append(stacks[src - 1].pop())

    return "".join(stack[-1] for stack in stacks)
