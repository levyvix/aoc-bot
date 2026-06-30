import re

REQUIRED = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
VALID_ECL = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def parse_fields(block: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for token in block.replace("\n", " ").split():
        key, _, value = token.partition(":")
        fields[key] = value
    return fields


def valid_byr(value: str) -> bool:
    return len(value) == 4 and value.isdigit() and 1920 <= int(value) <= 2002


def valid_iyr(value: str) -> bool:
    return len(value) == 4 and value.isdigit() and 2010 <= int(value) <= 2020


def valid_eyr(value: str) -> bool:
    return len(value) == 4 and value.isdigit() and 2020 <= int(value) <= 2030


def valid_hgt(value: str) -> bool:
    m = re.fullmatch(r"(\d+)(cm|in)", value)
    if not m:
        return False
    n = int(m.group(1))
    unit = m.group(2)
    if unit == "cm":
        return 150 <= n <= 193
    return 59 <= n <= 76


def valid_hcl(value: str) -> bool:
    return bool(re.fullmatch(r"#[0-9a-f]{6}", value))


def valid_ecl(value: str) -> bool:
    return value in VALID_ECL


def valid_pid(value: str) -> bool:
    return len(value) == 9 and value.isdigit()


VALIDATORS = {
    "byr": valid_byr,
    "iyr": valid_iyr,
    "eyr": valid_eyr,
    "hgt": valid_hgt,
    "hcl": valid_hcl,
    "ecl": valid_ecl,
    "pid": valid_pid,
}


def is_valid_passport(fields: dict[str, str]) -> bool:
    if not REQUIRED <= fields.keys():
        return False
    return all(VALIDATORS[key](fields[key]) for key in REQUIRED)


def solve(data: str) -> str:
    count = sum(
        1
        for block in data.strip().split("\n\n")
        if is_valid_passport(parse_fields(block))
    )
    return str(count)
