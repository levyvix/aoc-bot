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
    _rules, medicine = _parse(data)
    elements = sum(1 for char in medicine if char.isupper())
    steps = elements - medicine.count("Rn") - medicine.count("Ar") - 2 * medicine.count("Y") - 1
    return str(steps)
