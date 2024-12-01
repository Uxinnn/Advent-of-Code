from collections import Counter


def read_input(file):
  left, right = list(), list()
  with open(file, 'r') as f:
    for line in f:
      left_val, right_val = line.strip().split()
      left.append(int(left_val))
      right.append(int(right_val))
  return left, right


def part1(file):
  left, right = read_input(file)
  left.sort()
  right.sort()
  tot_dist = sum([abs(left_val - right_val)
                  for left_val, right_val in zip(left, right)
                  ])
  print(f"Part 1: {tot_dist}")


def part2(file):
  left, right = read_input(file)
  counts = Counter(right)
  tot_sim_score = 0
  for left_val in left:
    sim_score = left_val * counts.get(left_val, 0)
    tot_sim_score += sim_score
  print(f"Part 2: {tot_sim_score}")


file = "input.in"
part1(file)
part2(file)
