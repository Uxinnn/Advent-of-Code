def read_input(file):
  with open(file, 'r') as f:
    grid = [list(line.strip()) for line in f.readlines()]
  m, n = len(grid), len(grid[0])
  start_pos = None
  for i in range(m):
    for j in range(n):
      if grid[i][j] == '^':
        start_pos = (i, j)
        grid[i][j] = '.'
  return start_pos, grid


def is_in(m, n, pos):
  return -1 < pos[0] < m and -1 < pos[1] < n


def change_dirn(dirn):
  next_dirns = {(-1, 0): (0, 1),
                (0, 1): (1, 0),
                (1, 0): (0, -1),
                (0, -1): (-1, 0),
                }
  return next_dirns[dirn]


def get_visited_positions(pos, dirn, grid):
  visited = set()
  m, n = len(grid), len(grid[0])
  while True:
    i, j = pos
    next_pos = i + dirn[0], j + dirn[1]
    if not is_in(m, n, next_pos):
      visited.add(pos)
      break
    elif grid[next_pos[0]][next_pos[1]] == '#':
      dirn = change_dirn(dirn)
    else:
      visited.add(pos)
      pos = i + dirn[0], j + dirn[1]
  return visited


def part1(file):
  pos, grid = read_input(file)
  dirn = (-1, 0)
  visited = get_visited_positions(pos, dirn, grid)
  tot_visited = len(visited)
  print(f"Part 1: {tot_visited}")


def part2(file):
  start_pos, grid = read_input(file)
  obs_count = 0
  m, n = len(grid), len(grid[0])
  visited = get_visited_positions(start_pos, (-1, 0), grid)
  visited.remove(start_pos)
  # Replace each position that will be visited with a # and run a simulation to
  # see if a loop is created.
  for (a, b) in visited:
    if grid[a][b] == '#' or (a, b) == start_pos:
      continue
    grid[a][b] = '#'
    pos = start_pos
    dirn = (-1, 0)
    visited = set()
    while True:
      if (pos, dirn) in visited:
        obs_count += 1
        break
      i, j = pos
      next_pos = i + dirn[0], j + dirn[1]
      if not is_in(m, n, next_pos):
        break
      elif grid[next_pos[0]][next_pos[1]] == '#':
        dirn = change_dirn(dirn)
      else:
        visited.add((pos, dirn))
        pos = i + dirn[0], j + dirn[1]
    grid[a][b] = '.'
  print(f"Part 2: {obs_count}")


file = "input.in"
part1(file)
part2(file)
