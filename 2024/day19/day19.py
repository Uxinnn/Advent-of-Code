def read_input(file):
  with open(file, 'r') as f:
    patterns = [pattern.strip() for pattern in f.readline().split(',')]
    f.readline()
    designs = list()
    for line in f.readlines():
      design = line.strip()
      designs.append(design)
  return patterns, designs


def get_design_count(patterns, design):
  dp = [0] * (len(design) + 1)
  dp[0] = 1
  for i in range(len(design)):
    if not dp[i]:
      continue
    for pattern in patterns:
      j = i + len(pattern)
      if j <= len(design) and pattern == design[i:j]:
        dp[j] += dp[i]
  count = dp[-1]
  return count


def part1(file):
  patterns, designs = read_input(file)
  tot_count = 0
  for design in designs:
    count = get_design_count(patterns, design)
    if count:
      tot_count += 1
  print(f"Part 1: {tot_count}")


def part2(file):
  patterns, designs = read_input(file)
  tot_count = 0
  for design in designs:
    count = get_design_count(patterns, design)
    tot_count += count
  print(f"Part 2: {tot_count}")


file = "input.in"
part1(file)
part2(file)
