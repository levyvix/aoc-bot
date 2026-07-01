import re
from dataclasses import dataclass, field


@dataclass
class Group:
    army: str
    units: int
    hp: int
    attack_damage: int
    attack_type: str
    initiative: int
    weak: set[str] = field(default_factory=set)
    immune: set[str] = field(default_factory=set)

    @property
    def effective_power(self) -> int:
        return self.units * self.attack_damage

    def damage_to(self, defender: "Group") -> int:
        if self.attack_type in defender.immune:
            return 0
        if self.attack_type in defender.weak:
            return 2 * self.effective_power
        return self.effective_power

    def apply_damage(self, damage: int) -> None:
        killed = damage // self.hp
        self.units = max(0, self.units - killed)


GROUP_RE = re.compile(
    r"(\d+) units each with (\d+) hit points"
    r"(?: \(([^)]*)\))?"
    r" with an attack that does (\d+) (\w+) damage at initiative (\d+)"
)


def parse_modifiers(text: str) -> tuple[set[str], set[str]]:
    weak: set[str] = set()
    immune: set[str] = set()
    if not text:
        return weak, immune
    for part in text.split(";"):
        part = part.strip()
        if part.startswith("weak to "):
            weak = set(part[8:].split(", "))
        elif part.startswith("immune to "):
            immune = set(part[10:].split(", "))
    return weak, immune


def parse_group_line(army: str, line: str) -> Group | None:
    m = GROUP_RE.search(line)
    if not m:
        return None
    units, hp, mods, attack_damage, attack_type, initiative = m.groups()
    weak, immune = parse_modifiers(mods or "")
    return Group(
        army=army,
        units=int(units),
        hp=int(hp),
        attack_damage=int(attack_damage),
        attack_type=attack_type,
        initiative=int(initiative),
        weak=weak,
        immune=immune,
    )


def parse(data: str) -> list[Group]:
    groups: list[Group] = []
    army = ""
    buffer = ""
    for line in data.strip().splitlines():
        line = line.strip()
        if line == "Immune System:":
            army = "immune"
            buffer = ""
            continue
        if line == "Infection:":
            army = "infection"
            buffer = ""
            continue
        buffer = f"{buffer} {line}".strip() if buffer else line
        group = parse_group_line(army, buffer)
        if group is not None:
            groups.append(group)
            buffer = ""
    return groups


def fight_round(groups: list[Group]) -> bool:
    """Run one round. Return False if no damage was dealt (stalemate)."""
    living = [g for g in groups if g.units > 0]
    if not living:
        return False

    targets: dict[int, Group] = {}
    taken: set[int] = set()

    order = sorted(living, key=lambda g: (-g.effective_power, -g.initiative))
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
    for attacker in attack_order:
        defender = targets[id(attacker)]
        damage = attacker.damage_to(defender)
        total_damage += damage
        defender.apply_damage(damage)

    return total_damage > 0


def simulate(groups: list[Group]) -> str:
    while True:
        immune_alive = any(g.units > 0 for g in groups if g.army == "immune")
        infection_alive = any(g.units > 0 for g in groups if g.army == "infection")
        if not immune_alive or not infection_alive:
            break
        if not fight_round(groups):
            break
    return str(sum(g.units for g in groups if g.units > 0))


def solve(data: str) -> str:
    groups = parse(data)
    return simulate(groups)
