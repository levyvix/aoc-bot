import importlib.util
from copy import deepcopy
from pathlib import Path

_part1_path = Path(__file__).with_name("part1.py")
_spec = importlib.util.spec_from_file_location("day24_part1", _part1_path)
_part1 = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_part1)

Group = _part1.Group
parse = _part1.parse


def apply_boost(groups: list[Group], boost: int) -> list[Group]:
    boosted: list[Group] = []
    for group in groups:
        clone = deepcopy(group)
        if clone.army == "immune":
            clone.attack_damage += boost
        boosted.append(clone)
    return boosted


def fight_round(groups: list[Group]) -> bool:
    living = [g for g in groups if g.units > 0]
    if not living:
        return False

    targets: dict[int, Group] = {}
    taken: set[int] = set()

    order = sorted(
        living,
        key=lambda g: (
            -g.effective_power,
            0 if g.army == "immune" else 1,
            -g.initiative,
        ),
    )
    for attacker in order:
        enemies = [
            g
            for g in living
            if g.army != attacker.army and id(g) not in taken
        ]
        if not enemies:
            continue
        best = max(
            enemies,
            key=lambda d: (
                attacker.damage_to(d),
                d.effective_power,
                d.initiative,
            ),
        )
        if attacker.damage_to(best) == 0:
            continue
        targets[id(attacker)] = best
        taken.add(id(best))

    attack_order = sorted(
        (g for g in living if id(g) in targets),
        key=lambda g: -g.initiative,
    )

    total_damage = 0
    units_before = sum(g.units for g in groups)
    for attacker in attack_order:
        defender = targets[id(attacker)]
        damage = attacker.damage_to(defender)
        total_damage += damage
        defender.apply_damage(damage)

    units_after = sum(g.units for g in groups)
    return units_after < units_before


def immune_wins(groups: list[Group]) -> int | None:
    while True:
        immune_alive = any(g.units > 0 for g in groups if g.army == "immune")
        infection_alive = any(g.units > 0 for g in groups if g.army == "infection")
        if not infection_alive and immune_alive:
            return sum(g.units for g in groups if g.army == "immune" and g.units > 0)
        if not immune_alive or not infection_alive:
            return None
        if not fight_round(groups):
            return None


def find_min_boost(groups: list[Group]) -> int:
    lo, hi = 0, 1
    while immune_wins(apply_boost(groups, hi)) is None:
        hi *= 2

    while lo < hi:
        mid = (lo + hi) // 2
        if immune_wins(apply_boost(groups, mid)) is not None:
            hi = mid
        else:
            lo = mid + 1
    return lo


def solve(data: str) -> str:
    groups = parse(data)
    boost = find_min_boost(groups)
    remaining = immune_wins(apply_boost(groups, boost))
    assert remaining is not None
    return str(remaining)
