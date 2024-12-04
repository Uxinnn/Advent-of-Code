import numpy as np
import re


def read_input(file):
  with open(file) as f:
    return np.array(list(list(line.strip()) for line in f.readlines()))


def part1(file):
  grid = read_input(file)
  m, n = grid.shape
  horizontals = list(grid)
  verticals = list(grid.T)
  bot_diagonals = [grid.diagonal(i) for i in range(-m + 1, n)]
  top_diagonals = [grid[::-1, :].diagonal(i) for i in range(-m + 1, n)]
  lines = ["".join(line) for line in
           horizontals + verticals + bot_diagonals + top_diagonals
           ]
  count = 0
  for line in lines:
    count += len(re.findall("XMAS", line))
    count += len(re.findall("SAMX", line))
  print(f"Part 1: {count}")


def part2(file):
  grid = read_input(file)
  m, n = grid.shape
  count = 0
  to_match = {("M", "A", "S"), ("S", "A", "M")}
  for i in range(1, m - 1):
    for j in range(1, n - 1):
      subgrid = grid[i - 1: i + 2, j - 1: j + 2]
      top_diagonal = subgrid[0][0], subgrid[1][1], subgrid[2][2]  # dirn: \
      bot_diagonal = subgrid[2][0], subgrid[1][1], subgrid[0][2]  # dirn: /
      if top_diagonal in to_match and bot_diagonal in to_match:
        count += 1
  print(f"Part 2: {count}")


file = "input.in"
part1(file)
part2(file)
