def get_track(grid, start, end):
  """
  Return a list of nodes in the track, given the grid.
  """
  track = [start, start]
  while track[-1] != end:
    i, j = track[-1]
    for i2, j2 in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
      if grid[i2][j2] == '.' and (i2, j2) != track[-2]:
        track.append((i2, j2))
        break
  return track[1:]


def read_input(file):
  grid = list()
  with open(file, 'r') as f:
    for line in f.readlines():
      grid.append(list(line.strip()))
  start, end = None, None
  for i, row in enumerate(grid):
    for j, c in enumerate(row):
      if c == 'S':
        start = (i, j)
        grid[i][j] = '.'
      elif c == 'E':
        end = (i, j)
        grid[i][j] = '.'
    if start and end:
      break
  track = get_track(grid, start, end)
  return track


def get_neighbors_dists(track, node, n):
  """
  Get neighboring nodes within a radius of n nodes distance away.
  """
  neighbors = set()
  for neighbor in track:
    dist = abs(node[0] - neighbor[0]) + abs(node[1] - neighbor[1])
    if dist <= n:
      neighbors.add((neighbor, dist))
  return neighbors


def get_savings(track, min_save, cheat_duration):
  node2step = {node: i for i, node in enumerate(track)}
  savings = list()
  for node in track:
    neighbors = get_neighbors_dists(track, node, cheat_duration)
    for neighbor, dist in neighbors:
      steps = node2step[neighbor] - node2step[node] - dist
      if steps > min_save:
        savings.append(steps)
  return savings


def part1(file):
  track = read_input(file)
  savings = get_savings(track, 99, 2)
  count = len(savings)
  print(f"Part 1: {count}")


def part2(file):
  track = read_input(file)
  savings = get_savings(track, 99, 20)
  count = len(savings)
  print(f"Part 2: {count}")


file = "input.in"
part1(file)
part2(file)
