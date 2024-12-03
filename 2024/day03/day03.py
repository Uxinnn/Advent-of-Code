import re


def read_input(file):
  with open(file) as f:
    for line in f.readlines():
      yield line.strip()


def extract_muls(line):
  muls = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(don't\(\))|(do\(\))", line)
  for i, mul in enumerate(muls):
    if mul[0] and mul[1]:
      muls[i] = int(mul[0]), int(mul[1]), "", ""
  return muls


def part1(file):
  lines = read_input(file)
  tot = 0
  for line in lines:
    muls = extract_muls(line)
    tot += sum([a * b for a, b, c, d in muls if a and b])
  print(f"Part 1: {tot}")


def part2(file):
  lines = read_input(file)
  tot = 0
  is_enabled = True
  for line in lines:
    muls = extract_muls(line)
    for mul in muls:
      if mul[2]:
        is_enabled = False
      elif mul[3]:
        is_enabled = True
      elif is_enabled and mul[0] and mul[1]:
        tot += mul[0] * mul[1]
  print(f"Part 2: {tot}")


file = "input.in"
part1(file)
part2(file)
