from math import log10, floor


def read_input(file):
  with open(file) as f:
    for line in f.readlines():
      target, vals = line.split(':')
      target = int(target)
      vals = [int(val) for val in vals.strip().split()]
      yield target, vals


def check_valid_1(target, curr, i, vals):
  if i == len(vals):
    return curr == target
  elif curr > target:
    return False
  else:
    return (check_valid_1(target, curr + vals[i], i + 1, vals) or
            check_valid_1(target, curr * vals[i], i + 1, vals)
            )


def part1(file):
  equations = read_input(file)
  tot = 0
  for target, vals in equations:
    if check_valid_1(target, vals[0], 1, vals):
      tot += target
  print(f"Part 1: {tot}")


def concat_ints(a, b):
  return a * 10 ** (floor(log10(b)) + 1) + b


def check_valid_2(target, curr, i, vals):
  if i == len(vals):
    return curr == target
  elif curr > target:
    return False
  else:
    return (check_valid_2(target, curr + vals[i], i + 1, vals) or
            check_valid_2(target, curr * vals[i], i + 1, vals) or
            check_valid_2(target, concat_ints(curr, vals[i]), i + 1, vals)
            )


def part2(file):
  equations = read_input(file)
  tot = 0
  for target, vals in equations:
    if check_valid_2(target, vals[0], 1, vals):
      tot += target
  print(f"Part 2: {tot}")


file = "input.in"
part1(file)
part2(file)
