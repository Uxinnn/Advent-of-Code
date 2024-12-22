from collections import defaultdict


def read_input(file):
  with open(file) as f:
    for line in f.readlines():
      yield int(line.strip())


def mix_and_prune(a, b):
  return (a ^ b) % 16777216


def simulate(secret, n):
  secrets = [secret]
  for _ in range(n):
    secret = mix_and_prune(secret * 64, secret)
    secret = mix_and_prune(secret // 32, secret)
    secret = mix_and_prune(secret * 2048, secret)
    secrets.append(secret)
  return secrets


def part1(file):
  initials = read_input(file)
  tot_secret_sum = sum([simulate(secret, 2000)[-1] for secret in initials])
  print(f"Part 1: {tot_secret_sum}")


def part2(file):
  initials = read_input(file)
  monkeys = list()
  for secret in initials:
    prices = [p % 10 for p in simulate(secret, 2000)]
    diffs = [(prices[i + 1] - prices[i], prices[i + 1])
             for i in range(len(prices) - 1)
             ]
    monkeys.append(diffs)
  bananas = defaultdict(int)
  for diffs in monkeys:
    visited = set()
    for i in range(len(diffs) - 3):
      window = tuple(diffs[i + j][0] for j in range(4))
      if window in visited:
        continue
      bananas[window] += diffs[i + 3][1]
      visited.add(window)
  max_bananas = max(bananas.values())
  print(f"Part 2: {max_bananas}")


file = "input.in"
part1(file)
part2(file)
