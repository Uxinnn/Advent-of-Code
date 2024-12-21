from collections import deque


def read_file(file):
  with open(file, 'r') as f:
    positions = list()
    for line in f.readlines():
      line = line.strip()
      pos = [int(coor) for coor in line.split(',')]
      positions.append(pos)
  if file == "example.in":
    grid_len = 7
    steps = 12
  else:
    grid_len = 71
    steps = 1024
  return grid_len, steps, positions


def bfs(grid, grid_len, start, end):
  frontier = deque([(start, 0)])
  visited = set()
  while frontier:
    pos, step = frontier.popleft()
    if pos in visited:
      continue
    visited.add(pos)
    if pos == end:
      return step
    y, x = pos
    for y2, x2 in ((y, x + 1), (y, x - 1), (y + 1, x), (y - 1, x)):
      if -1 < y2 < grid_len and -1 < x2 < grid_len and grid[y2][x2] == 0:
        frontier.append(((y2, x2), step + 1))
  return -1


def part1(file):
  grid_len, steps, positions = read_file(file)
  grid = [[0] * grid_len for _ in range(grid_len)]
  for i in range(steps):
    y, x = positions[i]
    grid[y][x] = 1
  step = bfs(grid, grid_len, (0, 0), (grid_len - 1, grid_len - 1))
  print(f"Part 1: {step}")


def part2(file):
  grid_len, steps, positions = read_file(file)
  grid = [[0] * grid_len for _ in range(grid_len)]
  for y, x in positions:
    grid[y][x] = 1
    if bfs(grid, grid_len, (0, 0), (grid_len - 1, grid_len - 1)) < 0:
      break
  else:
    raise Exception("No solution found.")
  print(f"Part 1: {y},{x}")


file = "input.in"
part1(file)
part2(file)
