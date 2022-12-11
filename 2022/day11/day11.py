from math import prod


class Monkey:
    def __init__(self, _id, op, test_val, test_true, test_false, items=None):
        self.id = _id
        self.items = items if items else []
        self.op = lambda old: eval(op)
        self.test_val = test_val
        self.test = lambda x: test_true if not x % test_val else test_false
        self.active_level = 0

    def __repr__(self):
        return f"Monkey {self.id}: {self.active_level}, {self.items}"

    def __lt__(self, monkey2):
        if isinstance(monkey2, Monkey):
            return self.get_active_level() < monkey2.get_active_level()

    def __gt__(self, monkey2):
        if isinstance(monkey2, Monkey):
            return self.get_active_level() > monkey2.get_active_level()

    def run(self, test_val_mod, is_part1=True):
        for item in self.items:
            self.active_level += 1
            worry_level = self.op(item) % test_val_mod
            if is_part1:
                worry_level = worry_level // 3
            next_monkey = self.test(worry_level)
            yield next_monkey, worry_level
        self.items.clear()

    def get_active_level(self):
        return self.active_level

    def add_item(self, item):
        self.items.append(item)


def read_input():
    monkeys = []
    with open("input.in", 'r') as f:
        token = 0
        for line in f:
            line = line.strip()
            if token == 0:
                _id = int(line.split()[-1][:-1])
                token = 1
            elif token == 1:
                starting_items = eval("[" + line.split(": ")[-1] + "]")
                token = 2
            elif token == 2:
                op = line.split(" = ")[-1]
                token = 3
            elif token == 3:
                test_val = int(line.split("by ")[-1])
                token = 4
            elif token == 4:
                test_true = int(line.split("monkey ")[-1])
                token = 5
            elif token == 5:
                test_false = int(line.split("monkey ")[-1])
                token = 6
            else:
                monkey = Monkey(_id, op, test_val, test_true, test_false, starting_items)
                monkeys.append(monkey)
                token = 0
        if token != 0:
            monkey = Monkey(_id, op, test_val, test_true, test_false, starting_items)
            monkeys.append(monkey)
    return monkeys


def run_rounds(rounds, monkeys, is_part1=True):
    # if worry level is divisible by this, then we can safely take the remainder to track worry levels with
    # smaller values.
    test_val_mod = prod([monkey.test_val for monkey in monkeys])
    for _ in range(rounds):
        for monkey in monkeys:
            thrown_items = monkey.run(test_val_mod, is_part1=is_part1)
            for next_monkey, item in thrown_items:
                monkeys[next_monkey].add_item(item)
    monkeys.sort(reverse=True)
    answer = monkeys[0].get_active_level() * monkeys[1].get_active_level()
    return answer


def part1():
    monkeys = read_input()
    rounds = 20
    answer = run_rounds(rounds, monkeys)
    print(f"Part 1: {answer}")


def part2():
    monkeys = read_input()
    rounds = 10000
    answer = run_rounds(rounds, monkeys, is_part1=False)
    print(f"Part 2: {answer}")


part1()
part2()
