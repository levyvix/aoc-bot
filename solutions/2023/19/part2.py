def solve(data: str) -> str:
    workflows_text = data.strip().split("\n\n")[0]

    workflows = {}
    for line in workflows_text.splitlines():
        name, rules_text = line.split("{")
        rules_text = rules_text.rstrip("}")
        rules = []
        for rule in rules_text.split(","):
            if ":" in rule:
                cond, dest = rule.split(":")
                attr, op_val = cond[0], cond[1:]
                op, val = op_val[0], int(op_val[1:])
                rules.append((attr, op, val, dest))
            else:
                rules.append((None, None, None, rule))
        workflows[name] = rules

    attr_idx = {"x": 0, "m": 2, "a": 4, "s": 6}

    def valid(ranges: tuple[int, ...]) -> bool:
        for i in range(0, 8, 2):
            if ranges[i] > ranges[i + 1]:
                return False
        return True

    def volume(ranges: tuple[int, ...]) -> int:
        result = 1
        for i in range(0, 8, 2):
            result *= ranges[i + 1] - ranges[i] + 1
        return result

    def split(
        ranges: tuple[int, ...], attr: str, op: str, val: int
    ) -> tuple[tuple[int, ...], tuple[int, ...]]:
        lo, hi = ranges[attr_idx[attr]], ranges[attr_idx[attr] + 1]
        true = list(ranges)
        false = list(ranges)
        if op == ">":
            true[attr_idx[attr]] = max(lo, val + 1)
            false[attr_idx[attr] + 1] = min(hi, val)
        else:
            true[attr_idx[attr] + 1] = min(hi, val - 1)
            false[attr_idx[attr]] = max(lo, val)
        return tuple(true), tuple(false)

    def count(workflow: str, ranges: tuple[int, ...]) -> int:
        if workflow == "A":
            return volume(ranges) if valid(ranges) else 0
        if workflow == "R":
            return 0

        total = 0
        current = ranges
        for attr, op, val, dest in workflows[workflow]:
            if attr is None:
                if valid(current):
                    total += count(dest, current)
                break
            true_range, false_range = split(current, attr, op, val)
            if valid(true_range):
                total += count(dest, true_range)
            current = false_range
            if not valid(current):
                break
        return total

    start = (1, 4000, 1, 4000, 1, 4000, 1, 4000)
    return str(count("in", start))
