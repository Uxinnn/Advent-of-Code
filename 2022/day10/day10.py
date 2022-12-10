"""
Can definitely do better by tracking cycles for each command since commands are in order.
Did not do so due to misunderstanding of question initially which made me write all these ._.
"""


class Buffer:
    def __init__(self):
        self.buffer = []

    def run_cycle(self, cycle, cmd):
        if cmd == "noop":
            end_cycle = self.buffer[-1][0] + 1 if self.buffer else cycle
            self.buffer.append((end_cycle, 0))
        else:
            end_cycle = self.buffer[-1][0] + 2 if self.buffer else cycle + 1
            val = int(cmd.split()[-1])
            self.buffer.append((end_cycle, val))
        return self.pop_buffer(cycle)

    def is_empty(self):
        return not bool(self.buffer)

    def pop_buffer(self, cycle):
        if self.buffer and self.buffer[0][0] == cycle:
            _, v = self.buffer.pop(0)
            return v
        return 0


def read_input():
    with open("input.in", 'r') as f:
        cmds = [cmd.strip() for cmd in f.readlines()]
    return cmds


def record_cycle(cycle, reg_x, points_to_record):
    if points_to_record and cycle == points_to_record[0]:
        points_to_record.pop(0)
        return cycle * reg_x
    return 0


def crt_printer(reg_x, cycle):
    if abs(reg_x - ((cycle - 1) % 40)) < 2:
        print("#", end="")
    else:
        print(".", end="")
    if cycle % 40 == 0:
        print()


def part1():
    cmds = read_input()
    reg_x = 1
    points_to_record = [20, 60, 100, 140, 180, 220]
    answer = 0
    cycle = 0
    buffer = Buffer()
    for i, cmd in enumerate(cmds):
        cycle = i + 1
        answer += record_cycle(cycle, reg_x, points_to_record)
        reg_x += buffer.run_cycle(cycle, cmd)
    while not buffer.is_empty():
        cycle += 1
        answer += record_cycle(cycle, reg_x, points_to_record)
        reg_x += buffer.pop_buffer(cycle)
    print(f"Part 1: {answer}")


def part2():
    cmds = read_input()
    reg_x = 1
    cycle = 0
    buffer = Buffer()
    for i, cmd in enumerate(cmds):
        cycle = i + 1
        crt_printer(reg_x, cycle)
        reg_x += buffer.run_cycle(cycle, cmd)
    while not buffer.is_empty():
        cycle += 1
        crt_printer(reg_x, cycle)
        reg_x += buffer.pop_buffer(cycle)


part1()
part2()
