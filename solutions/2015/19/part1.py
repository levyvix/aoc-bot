from __future__ import annotations


def _parse(data: str) -> tuple[list[tuple[str, str]], str]:
    rules: list[tuple[str, str]] = []
    medicine = ""
    for line in data.strip().splitlines():
        if "=>" not in line:
            medicine = line.strip()
            continue
        left, right = (part.strip() for part in line.split("=>", 1))
        rules.append((left, right))
    if not medicine:
        raise ValueError("missing medicine molecule in input")
    return rules, medicine


def solve(data: str) -> str:
    rules, medicine = _parse(data)
    molecules: set[str] = set()
    for left, right in rules:
        start = 0
        while True:
            idx = medicine.find(left, start)
            if idx == -1:
                break
            molecules.add(medicine[:idx] + right + medicine[idx + len(left) :])
            start = idx + 1
    return str(len(molecules))
