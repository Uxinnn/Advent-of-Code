from collections import defaultdict
from itertools import combinations
from functools import cmp_to_key


def read_input(file):
  with open(file, 'r') as f:
    rules = defaultdict(set)
    while True:
      line = f.readline().strip()
      if not line:
        break
      a, b = line.split('|')
      rules[a].add(b)
    updates = list()
    for line in f.readlines():
      updates.append(line.strip().split(','))
  return rules, updates


def get_sorter(rules):
  def sorter(a, b):
    if a in rules.keys() and b in rules[a]:
      return 1
    elif b in rules.keys() and a in rules[b]:
      return -1
    else:
      return 0
  return sorter


def is_correct_update(sorter, update):
  for a, b in combinations(update, 2):
    if sorter(a, b) == -1:
      return False
  return True


def get_mid_sum(updates):
  tot_mid_val = 0
  for update in updates:
    mid_idx = len(update) // 2
    mid_val = update[mid_idx]
    tot_mid_val += int(mid_val)
  return tot_mid_val


def part1(file):
  rules, updates = read_input(file)
  sorter = get_sorter(rules)
  correct_updates = list()
  for update in updates:
    if is_correct_update(sorter, update):
      correct_updates.append(update)
  tot_mid_val = get_mid_sum(correct_updates)
  print(f"Part 1: {tot_mid_val}")


def part2(file):
  rules, updates = read_input(file)
  sorter = get_sorter(rules)
  incorrect_updates = list()
  for update in updates:
    if not is_correct_update(sorter, update):
      incorrect_updates.append(update)
  for update in incorrect_updates:
    update.sort(key=cmp_to_key(sorter))
  tot_mid_val = get_mid_sum(incorrect_updates)
  print(f"Part 2: {tot_mid_val}")


file = "input.in"
part1(file)
part2(file)
