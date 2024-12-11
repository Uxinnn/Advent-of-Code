from math import log10, floor
from collections import Counter, defaultdict


def read_input(file):
  with open(file, 'r') as f:
    line = [int(x) for x in f.readline().strip().split()]
    return Counter(line)


def get_digits_count(num):
  return floor(log10(num)) + 1


def split_number(num):
  digits_count = get_digits_count(num)
  factor = 10 ** (digits_count // 2)
  return num // factor, num % factor


def simulate(counts, n):
  for _ in range(n):
    new_counts = defaultdict(int)
    for x, c in counts.items():
      if x == 0:
        new_counts[1] += c
      elif get_digits_count(x) % 2 == 0:
        for x2 in split_number(x):
          new_counts[x2] += c
      else:
        new_counts[x * 2024] += c
    counts = new_counts
  tot_count = sum(counts.values())
  return tot_count


def part1(file):
  counts = read_input(file)
  tot_count = simulate(counts, 25)
  print(f"Part 1: {tot_count}")


def part2(file):
  counts = read_input(file)
  tot_count = simulate(counts, 75)
  print(f"Part 2: {tot_count}")


file = "input.in"
part1(file)
part2(file)
