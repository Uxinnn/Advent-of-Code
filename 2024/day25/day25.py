from itertools import product


def process_grid(grid, c):
  heights = list()
  for col in range(len(grid[0])):
    for i in range(len(grid)):
      if grid[i][col] != c:
        heights.append(i)
        break
  return heights


def read_input(file):
  with open(file, 'r') as f:
    line = f.readline().strip()
    keys = list()
    locks = list()
    while line:
      grid = [line]
      for _ in range(6):
        grid.append(f.readline().strip())
      c = grid[0][0]
      heights = process_grid(grid, c)
      if c == '.':
        keys.append(heights)
      else:
        locks.append(heights)
      f.readline()
      line = f.readline().strip()
  return keys, locks


def part1(file):
  keys, locks = read_input(file)
  count = 0
  for key, lock in product(keys, locks):
    for i in range(len(key)):
      if key[i] < lock[i]:
        break
    else:
      count += 1
  print(f"Part 1: {count}")


file = "input.in"
part1(file)
