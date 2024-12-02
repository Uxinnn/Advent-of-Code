def read_input(file):
  with open(file, 'r') as f:
    for line in f.readlines():
      report = [int(level) for level in line.strip().split()]
      yield report


def is_safe(report):
  diff = [report[i - 1] - report[i] for i in range(1, len(report))]
  max_diff = max(diff)
  min_diff = min(diff)
  return (max_diff < 4 and min_diff > 0) or (max_diff < 0 and min_diff > -4)


def part1(file):
  count = sum(is_safe(report) for report in read_input(file))
  print(f"Part 1: {count}")


def part2(file):
  count = 0
  for report in read_input(file):
    for i in range(len(report)):
      modified_report = report[:i] + report[i + 1:]
      if is_safe(modified_report):
        count += 1
        break
  print(f"Part 2: {count}")


file = "input.in"
part1(file)
part2(file)
