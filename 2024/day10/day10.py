def read_input(file):
  with open(file, 'r') as f:
    return [[int(v) for v in line.strip()] for line in f.readlines()]


def follow_trial(grid, i, j, v, m, n, paths, part):
  """
  Flood fill method to get:
    (1) number of unique 9-height positions reachable from each trial head.
    (2) number of unique trials from each trial head.
  (1) is for part 1 and (2) is for part 2.
  """
  if paths[i][j] is not None:
    # Already traversed this position.
    return
  if grid[i][j] == 9:
    paths[i][j] = {(i, j)} if part == 1 else 1
    return
  # Flood fill
  count = set() if part == 1 else 0
  for i2, j2 in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
    if -1 < i2 < m and -1 < j2 < n:
      if grid[i2][j2] == v + 1:
        follow_trial(grid, i2, j2, grid[i2][j2], m, n, paths, part)
        if part == 1:
          count.update(paths[i2][j2])
        else:
          count += paths[i2][j2]
  paths[i][j] = count


def get_score_rating(grid, paths, part):
  tot_score = 0
  for i, line in enumerate(grid):
    for j, v in enumerate(line):
      if v == 0:
        tot_score += len(paths[i][j]) if part == 1 else paths[i][j]
  return tot_score


def part1(file):
  grid = read_input(file)
  m, n = len(grid), len(grid[0])
  paths = [[None] * m for _ in range(n)]
  for i, line in enumerate(grid):
    for j, v in enumerate(line):
      follow_trial(grid, i, j, v, m, n, paths, 1)
  # Sum trialheads
  tot_score = get_score_rating(grid, paths, 1)
  print(f"Part 1: {tot_score}")


def part2(file):
  grid = read_input(file)
  m, n = len(grid), len(grid[0])
  paths = [[None] * m for _ in range(n)]
  for i, line in enumerate(grid):
    for j, v in enumerate(line):
      follow_trial(grid, i, j, v, m, n, paths, 2)
  # Sum trialheads
  tot_rating = get_score_rating(grid, paths, 2)
  print(f"Part 2: {tot_rating}")


file = "input.in"
part1(file)
part2(file)
