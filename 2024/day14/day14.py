import re


def read_input(file):
  state = list()
  velocities = list()
  with open(file) as f:
    for line in f.readlines():
      robot_state = [int(x) for x in re.findall(r"\-?\d+", line)]
      state.append((robot_state[1], robot_state[0]))
      velocities.append((robot_state[3], robot_state[2]))
  return state, velocities


def get_grid_dims(file):
  if file == "example.in":
    return 7, 11
  else:
    return 103, 101


def move(s, v, m, n):
  return (s[0] + v[0]) % m, (s[1] + v[1]) % n


def get_quadrant_counts(state, m, n):
  count = [0, 0, 0, 0]
  qm, qn = m // 2, n // 2  # dimensions of a quadrant
  for s in state:
    if s[0] < qm and s[1] < qn:
      count[0] += 1
    elif s[0] > qm and s[1] < qn:
      count[1] += 1
    elif s[0] < qm and s[1] > qn:
      count[2] += 1
    elif s[0] > qm and s[1] > qn:
      count[3] += 1
  return count


def get_safety_factor(state, m, n):
  count = get_quadrant_counts(state, m, n)
  safety_factor = 1
  for c in count:
    safety_factor *= c
  return safety_factor


def print_grid(state, m, n):
  grid = [['.'] * n for _ in range(m)]
  for s in state:
    grid[s[0]][s[1]] = '0'
  for row in grid:

    print(''.join(row))


def check_heuristics(state):
  """
  Check if there is a long row of robots in the state.
  Return True if so.
  """
  positions = set(state)
  max_len = 0
  while positions:
    row_len = 1
    i, j = positions.pop()
    # Go backwards until there is no more robots in the row.
    i2, j2 = i - 1, j
    while (i2, j2) in positions:
      positions.remove((i2, j2))
      row_len += 1
      i2 -= 1
    # Go forward until there is no more robots in the row.
    i2, j2 = i + 1, j
    while (i2, j2) in positions:
      positions.remove((i2, j2))
      row_len += 1
      i2 += 1
    max_len = max(max_len, row_len)
  min_row_len = 16
  return max_len > min_row_len


def part1(file):
  state, velocities = read_input(file)
  m, n = get_grid_dims(file)
  for _ in range(100):
    new_state = list()
    for i, s in enumerate(state):
      new_state.append(move(s, velocities[i], m, n))
    state = new_state
  safety_factor = get_safety_factor(state, m, n)
  print(f"Part 1: {safety_factor}")


def part2(file):
  state, velocities = read_input(file)
  m, n = get_grid_dims(file)
  itr = 0
  while not check_heuristics(state):
    new_state = list()
    for i, s in enumerate(state):
      new_state.append(move(s, velocities[i], m, n))
    state = new_state
    itr += 1
  # print_grid(state, m, n)
  print(f"Part 2: {itr}")


file = "input.in"
part1(file)
part2(file)
