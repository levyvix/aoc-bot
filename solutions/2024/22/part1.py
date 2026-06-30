MOD = 16777216


def next_secret(secret: int) -> int:
    secret = (secret ^ (secret * 64)) % MOD
    secret = (secret ^ (secret // 32)) % MOD
    secret = (secret ^ (secret * 2048)) % MOD
    return secret


def solve(data: str) -> str:
    total = 0
    for line in data.strip().splitlines():
        secret = int(line.strip())
        for _ in range(2000):
            secret = next_secret(secret)
        total += secret
    return str(total)
