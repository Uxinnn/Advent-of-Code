def read_file(file):
  registers = list()
  with open(file, 'r') as f:
    for _ in range(3):
      line = f.readline()
      registers.append(int(line.split(':', 1)[1].strip()))
    f.readline()  # Empty line
    line = f.readline().strip()
    line = line.split(':', 1)[1].strip()
    program = [int(v) for v in line.split(',')]
  return registers, program


def resolve_x(x, registers):
  if x < 4:
    return x
  elif x == 7:
    raise Exception("Invalid combo operand 7.")
  else:
    return registers[x - 4]


def op0(i, x, registers, out):
  # adv
  x = resolve_x(x, registers)
  res = registers[0] // (2 ** x)
  registers[0] = res
  return i + 2


def op1(i, x, registers, out):
  # bxl
  res = registers[1] ^ x
  registers[1] = res
  return i + 2


def op2(i, x, registers, out):
  # bst
  x = resolve_x(x, registers)
  res = x % 8
  registers[1] = res
  return i + 2


def op3(i, x, registers, out):
  # jnz
  if registers[0] != 0:
    return x
  return i + 2


def op4(i, x, registers, out):
  # bxc
  x = registers[1] ^ registers[2]
  registers[1] = x
  return i + 2


def op5(i, x, registers, out):
  # out
  x = resolve_x(x, registers)
  res = x % 8
  out.append(res)
  return i + 2


def op6(i, x, registers, out):
  # bdv
  x = resolve_x(x, registers)
  res = registers[0] // (2 ** x)
  registers[1] = res
  return i + 2


def op7(i, x, registers, out):
  # cdv
  x = resolve_x(x, registers)
  res = registers[0] // (2 ** x)
  registers[2] = res
  return i + 2


def run_op(op_idx, i, x, registers, out):
  idx2op = [op0, op1, op2, op3, op4, op5, op6, op7]
  op = idx2op[op_idx]
  return op(i, x, registers, out)


def run(registers, program):
  out = list()
  i = 0
  n = len(program)
  while i < n:
    op_idx, x = program[i:i + 2]
    i = run_op(op_idx, i, x, registers, out)
  return out


def part1(file):
  registers, program = read_file(file)
  out = run(registers, program)
  res = ",".join(str(x) for x in out)
  print(f"Part 1: {res}")


def part2(file):
  # Got some help from:
  # https://www.reddit.com/r/adventofcode/comments/1hg38ah/comment/m2vn8nx/
  registers, program = read_file(file)
  out = list()
  last_n = len(program) - 1
  registers[0] = 8 ** 15
  p = 14
  while out != program:
    registers[0] += 8 ** p
    out = run(registers.copy(), program)
    if out[last_n:] == program[last_n:]:
      p = max(0, p - 1)
      last_n -= 1

  reg_a = registers[0]
  print(f"Part 2: {reg_a}")


file = "input.in"
part1(file)
part2(file)
