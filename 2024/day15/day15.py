def read_input(file):
  with open(file, 'r') as f:
    grid = list()
    line = f.readline().strip()
    while line:
      grid.append(list(line))
      line = f.readline().strip()
    moves = list()
    for line in f.readlines():
      line = line.strip()
      moves.append(list(line))
    moves = [m for move_line in moves for m in move_line]
  # Change moves to coordinates
  move2coor = {'<': (0, -1),
               '>': (0, 1),
               '^': (-1, 0),
               'v': (1, 0),
               }
  for i, move in enumerate(moves):
    moves[i] = move2coor[move]
  return grid, moves


def expand_grid(grid):
  new_grid = list()
  c2c = {'#': ['#', '#'],
         'O': ['[', ']'],
         '.': ['.', '.'],
         '@': ['@', '.'],
         }
  for row in grid:
    new_row = [c2c[r] for r in row]
    new_row = [c for p in new_row for c in p]
    new_grid.append(new_row)
  return new_grid


def replace_start_pos(grid):
  start_pos = None
  for i, row in enumerate(grid):
    for j, c in enumerate(row):
      if c == '@':
        start_pos = i, j
        grid[i][j] = '.'
  return start_pos


def get_gps_coordinates(grid, _id):
  gps_coors = list()
  for i, row in enumerate(grid):
    for j, c in enumerate(row):
      if c == _id:
        gps_coors.append(i * 100 + j)
  return gps_coors


def part1(file):
  def can_move(pos, grid, move):
    i, j = pos
    i2, j2 = i + move[0], j + move[1]
    if grid[i2][j2] == '.':
      return True
    elif grid[i2][j2] == '#':
      return False
    else:
      return can_move((i2, j2), grid, move)

  def do_move(c, next_pos, grid, move):
    i2, j2 = next_pos
    if grid[i2][j2] == 'O':
      grid[i2][j2] = c
      do_move('O', (i2 + move[0], j2 + move[1]), grid, move)
    elif grid[i2][j2] == '.':
      grid[i2][j2] = c
    else:
      raise Exception("Invalid c")

  grid, moves = read_input(file)
  pos = replace_start_pos(grid)
  for move in moves:
    if can_move(pos, grid, move):
      pos = pos[0] + move[0], pos[1] + move[1]
      do_move('.', pos, grid, move)
  gps_coors = get_gps_coordinates(grid, 'O')
  tot_gps_coors = sum(gps_coors)
  print(f"Part 1: {tot_gps_coors}")


def part2(file):
  def can_move(pos, grid, move):
    i, j = pos
    i2, j2 = i + move[0], j + move[1]
    if grid[i2][j2] == '.':
      return True
    elif grid[i2][j2] == '#':
      return False
    if move == (-1, 0) or move == (1, 0):  # Up or down
      offset = 1 if grid[i2][j2] == '[' else -1
      return (can_move((i2, j2), grid, move) and
              can_move((i2, j2 + offset), grid, move))
    else:  # Left or right
      return can_move((i2, j2), grid, move)

  def do_move(c, next_pos, grid, move, visited):
    i2, j2 = next_pos
    visited.add((i2, j2))
    if move == (-1, 0) or move == (1, 0):  # Up or down
      if grid[i2][j2] == '[':
        grid[i2][j2] = c
        do_move('[', (i2 + move[0], j2 + move[1]), grid, move, visited)
        diag = (i2, j2 + 1)
        if diag not in visited:
          do_move('.', diag, grid, move, visited)
      elif grid[i2][j2] == ']':
        grid[i2][j2] = c
        do_move(']', (i2 + move[0], j2 + move[1]), grid, move, visited)
        diag = (i2, j2 - 1)
        if diag not in visited:
          do_move('.', diag, grid, move, visited)
      elif grid[i2][j2] == '.':
        grid[i2][j2] = c
      else:
        raise Exception("Invalid c")
    else:  # Left or right
      if grid[i2][j2] == ']' or grid[i2][j2] == '[':
        c2 = ']' if grid[i2][j2] == ']' else '['
        grid[i2][j2] = c
        do_move(c2, (i2 + move[0], j2 + move[1]), grid, move, visited)
      elif grid[i2][j2] == '.':
        grid[i2][j2] = c
      else:
        raise Exception(f"Invalid c: {grid[i2][j2]}")

  grid, moves = read_input(file)
  grid = expand_grid(grid)
  pos = replace_start_pos(grid)
  for move in moves:
    if can_move(pos, grid, move):
      pos = pos[0] + move[0], pos[1] + move[1]
      do_move('.', pos, grid, move, set())
  gps_coors = get_gps_coordinates(grid, '[')
  tot_gps_coors = sum(gps_coors)
  print(f"Part 2: {tot_gps_coors}")


file = "input.in"
part1(file)
part2(file)
