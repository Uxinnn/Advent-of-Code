from collections import defaultdict
from heapq import heappush, heappop


def read_input(file):
  with open(file, 'r') as f:
    grid = [list(row.strip()) for row in f.readlines()]
  # Find start and end positions
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
  return start, end, grid


def rotate(dirn):
  mapper = {(0, 1): ((1, 0), (-1, 0)),
            (0, -1): ((1, 0), (-1, 0)),
            (1, 0): ((0, 1), (0, -1)),
            (-1, 0): ((0, 1), (0, -1)),
            }
  return mapper[dirn]


def dijsktra(start, end, grid):
  frontier = [[0, start, (0, 1), set()]]
  min_score = float("inf")
  all_visited = set()
  # To track min score for each point
  min_point_score = defaultdict(lambda: float("inf"))
  while frontier:
    s, c, dirn, visited = heappop(frontier)
    if s > min_point_score[(c, dirn)] or s > min_score:
      continue
    min_point_score[(c, dirn)] = s
    visited.add(c)
    if c == end:
      # Found the end. Show min score
      if s > min_score:
        return s, all_visited
      min_score = s
      all_visited |= visited
      continue
    c2 = c[0] + dirn[0], c[1] + dirn[1]
    if grid[c2[0]][c2[1]] == '.':
      heappush(frontier, [s + 1, c2, dirn, visited.copy()])
    for dirn2 in rotate(dirn):
      heappush(frontier, [s + 1000, c, dirn2, visited.copy()])
  return min_score, all_visited


def part1(file):
  start, end, grid = read_input(file)
  score, _ = dijsktra(start, end, grid)
  print(f"Part 1: {score}")


def part2(file):
  start, end, grid = read_input(file)
  _, visited = dijsktra(start, end, grid)
  count = len(visited)
  print(f"Part 2: {count}")


file = "input.in"
part1(file)
part2(file)
