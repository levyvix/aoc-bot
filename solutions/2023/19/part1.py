def solve(data: str) -> str:
    workflows_text, parts_text = data.strip().split("\n\n")

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

    def evaluate(part: dict[str, int]) -> bool:
        workflow = "in"
        while workflow not in ("A", "R"):
            for attr, op, val, dest in workflows[workflow]:
                if attr is None:
                    workflow = dest
                    break
                v = part[attr]
                if (op == ">" and v > val) or (op == "<" and v < val):
                    workflow = dest
                    break
        return workflow == "A"

    total = 0
    for line in parts_text.splitlines():
        part = {}
        for item in line.strip("{}").split(","):
            k, v = item.split("=")
            part[k] = int(v)
        if evaluate(part):
            total += sum(part.values())

    return str(total)
