MOD = 16777216


def next_secret(secret: int) -> int:
    secret = (secret ^ (secret * 64)) % MOD
    secret = (secret ^ (secret // 32)) % MOD
    secret = (secret ^ (secret * 2048)) % MOD
    return secret


def buyer_bananas(initial: int) -> dict[tuple[int, int, int, int], int]:
    prices = [initial % 10]
    secret = initial
    for _ in range(2000):
        secret = next_secret(secret)
        prices.append(secret % 10)

    changes = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]
    first: dict[tuple[int, int, int, int], int] = {}
    for i in range(len(changes) - 3):
        seq = (changes[i], changes[i + 1], changes[i + 2], changes[i + 3])
        if seq not in first:
            first[seq] = prices[i + 4]
    return first


def solve(data: str) -> str:
    totals: dict[tuple[int, int, int, int], int] = {}
    for line in data.strip().splitlines():
        initial = int(line.strip())
        for seq, bananas in buyer_bananas(initial).items():
            totals[seq] = totals.get(seq, 0) + bananas
    return str(max(totals.values()))
