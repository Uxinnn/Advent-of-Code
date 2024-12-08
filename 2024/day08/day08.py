from collections import defaultdict
from itertools import combinations


def read_input(file):
  antennas = defaultdict(set)
  with open(file, 'r') as f:
    for i, line in enumerate(f.readlines()):
      line = line.strip()
      for j, x in enumerate(line):
        if x != '.':
          antennas[x].add((i, j))
  bounds = i + 1, j + 1
  return bounds, antennas


def print_grid(bounds, antinodes):
  grid = [['.'] * bounds[1] for _ in range(bounds[0])]
  for i, j in antinodes:
    grid[i][j] = '#'
  for row in grid:
    print(''.join(row))


def is_valid_antinode(antinode, bounds):
  return -1 < antinode[0] < bounds[0] and -1 < antinode[1] < bounds[1]


def part1(file):
  bounds, antennas = read_input(file)
  antinodes = set()
  for antenna_type, positions in antennas.items():
    for pos1, pos2 in combinations(positions, 2):
      diff = pos1[0] - pos2[0], pos1[1] - pos2[1]
      antinode1 = pos1[0] + diff[0], pos1[1] + diff[1]
      if is_valid_antinode(antinode1, bounds):
        antinodes.add(antinode1)
      antinode2 = pos2[0] - diff[0], pos2[1] - diff[1]
      if is_valid_antinode(antinode2, bounds):
        antinodes.add(antinode2)
  antinode_count = len(antinodes)
  print(f"Part 1: {antinode_count}")


def part2(file):
  bounds, antennas = read_input(file)
  antinodes = set()
  for antenna_type, positions in antennas.items():
    for pos1, pos2 in combinations(positions, 2):
      diff = pos1[0] - pos2[0], pos1[1] - pos2[1]
      # Propagate signal forward
      antinode = pos1
      while is_valid_antinode(antinode, bounds):
        antinodes.add(antinode)
        antinode = antinode[0] + diff[0], antinode[1] + diff[1]
      # Propagate signal backward
      antinode = pos1
      while is_valid_antinode(antinode, bounds):
        antinodes.add(antinode)
        antinode = antinode[0] - diff[0], antinode[1] - diff[1]
  antinode_count = len(antinodes)
  print(f"Part 2: {antinode_count}")


file = "input.in"
part1(file)
part2(file)
