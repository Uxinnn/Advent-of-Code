"""
Credits to this youtube video for helping me solve this:
https://www.youtube.com/watch?v=q5I6ZvJmHEo
"""


from functools import lru_cache
from itertools import permutations


def read_input(file):
  with open(file, 'r') as f:
    for line in f.readlines():
      yield line.strip()


num_keys = {'A': (3, 2),
            '0': (3, 1),
            '1': (2, 0),
            '2': (2, 1),
            '3': (2, 2),
            '4': (1, 0),
            '5': (1, 1),
            '6': (1, 2),
            '7': (0, 0),
            '8': (0, 1),
            '9': (0, 2),
            }

dir_keys = {'^': (0, 1),
            'A': (0, 2),
            '<': (1, 0),
            'v': (1, 1),
            '>': (1, 2),
            }

moves2dist = {'^': (-1, 0),
              '<': (0, -1),
              'v': (1, 0),
              '>': (0, 1),
              }


def get_valid_paths(src_coor, board, dist):
  # Get moves needed to get from source to destination
  moves = list()
  c = 'v' if dist[0] > 0 else '^'
  for _ in range(abs(dist[0])):
    moves.append(c)
  c = '>' if dist[1] > 0 else '<'
  for _ in range(abs(dist[1])):
    moves.append(c)
  # Ensure moves does not cause robot arm to go outside of board
  valid_paths = list()
  for path in set(permutations(moves)):
    path = list(path) + ['A']
    coor = src_coor
    for move in path[:-1]:
      move = moves2dist[move]
      coor = coor[0] + move[0], coor[1] + move[1]
      if coor not in board.values():
        break
    else:
      valid_paths.append(path)
  return valid_paths


@lru_cache(None)
def get_paths(src, dst, is_dir_keys):
  board = dir_keys if is_dir_keys else num_keys
  src_coor = board[src]
  dst_coor = board[dst]
  dist = dst_coor[0] - src_coor[0], dst_coor[1] - src_coor[1]
  valid_paths = get_valid_paths(src_coor, board, dist)
  return valid_paths


@lru_cache(None)
def get_path_cost(src, dst, is_dir_keys, depth=0):
  if depth == 0:
    paths = get_paths(src, dst, True)
    return min(len(path) for path in paths)
  paths = get_paths(src, dst, is_dir_keys)
  min_path_cost = float("inf")
  for path in paths:
    path = ['A'] + path
    cost = 0
    for i in range(len(path) - 1):
      subsrc, subdst = path[i], path[i + 1]
      path_cost = get_path_cost(subsrc, subdst, True, depth - 1)
      cost += path_cost
    min_path_cost = min(min_path_cost, cost)
  return min_path_cost


def get_code_cost(code, depth):
  code = list('A' + code)
  cost = 0
  for i in range(len(code) - 1):
    subsrc, subdst = code[i], code[i + 1]
    cost += get_path_cost(subsrc, subdst, False, depth)
  return cost


def part1(file):
  codes = read_input(file)
  res = 0
  for code in codes:
    cost = get_code_cost(code, 2)
    res += cost * int(code[:-1])
  print(f"Part 1: {res}")


def part2(file):
  codes = read_input(file)
  res = 0
  for code in codes:
    cost = get_code_cost(code, 25)
    res += cost * int(code[:-1])
  print(f"Part 2: {res}")


file = "input.in"
part1(file)
part2(file)
