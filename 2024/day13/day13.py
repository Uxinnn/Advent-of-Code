from sympy import Eq, solve
from sympy.abc import x, y
import re


def read_input(file):
  with open(file) as f:
    puzzles = list()
    while line := f.readline():
      puzzle = list()
      while True:
        vals = [int(v) for v in re.findall(r"\d+", line)]
        puzzle.append(vals)
        line = f.readline()
        if not line.strip():
          break
      puzzles.append(puzzle)
    return puzzles


def solve_puzzles(puzzles):
  tot_tokens = 0
  for puzzle in puzzles:
    soln = solve_puzzle(puzzle)
    if soln[x].is_integer and soln[y].is_integer:
      tot_tokens += get_tokens(soln)
  return tot_tokens


def solve_puzzle(puzzle):
  eqns = list()
  for eqn in zip(*puzzle):
    eqn = Eq(eqn[0] * x + eqn[1] * y, eqn[2])
    eqns.append(eqn)
  soln = solve(eqns)
  return soln


def get_tokens(soln):
  return 3 * int(soln[x]) + int(soln[y])


def part1(file):
  puzzles = read_input(file)
  tot_tokens = solve_puzzles(puzzles)
  print(f"Part 1: {tot_tokens}")


def part2(file):
  puzzles = read_input(file)
  for puzzle in puzzles:
    puzzle[2][0] += 10000000000000
    puzzle[2][1] += 10000000000000
  tot_tokens = solve_puzzles(puzzles)
  print(f"Part 2: {tot_tokens}")


file = "input.in"
part1(file)
part2(file)
