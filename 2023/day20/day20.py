import math
from collections import deque


def read_input(file):
    with open(file, 'r') as f:
        modules = dict()
        conjunctions = set()  # Set of names of conjunctions
        for line in f:
            line = line.strip()
            name, outs = line.split(" -> ")
            out_mods = outs.split(", ")
            if line[0] == 'b':
                module = Broadcaster()
            elif line[0] == '%':
                name = name[1:]
                module = FlipFlop()
            elif line[0] == '&':
                name = name[1:]
                module = Conjunction()
                conjunctions.add(name)
            modules[name] = [module, out_mods]
        # This part to make aware conjunctions of their input modules
        for k, v in modules.items():
            for out_mod in v[1]:
                if out_mod in conjunctions:
                    modules[out_mod][0].add_input(k)
    return modules


class Broadcaster:
    def __init__(self):
        pass

    def __repr__(self):
        return "Broadcaster"

    def recv(self, src, signal):
        return signal


class FlipFlop:
    def __init__(self):
        self.state = 0  # 0 for off, 1 for on

    def __repr__(self):
        return "FlipFlop"

    def recv(self, src, signal):
        if signal == 0:
            self.state = (self.state + 1) % 2
            return self.state
        return None


class Conjunction:
    def __init__(self):
        self.inputs = dict()
        self.state = 1

    def __repr__(self):
        return f"Conjunction with inputs: {tuple(self.inputs.keys())}"

    def add_input(self, src):
        self.inputs[src] = 0

    def recv(self, src, signal):
        self.inputs[src] = signal
        if all(map(lambda x: x == 1, self.inputs.values())):
            self.state = 0
            return 0
        else:
            self.state = 1
            return 1


def press_button(modules, part, pulses_count, lowest_parents, press_count):
    pulses = deque([("broadcaster", "button", 0)])  # module, src, signal
    while pulses:
        name, src, signal = pulses.popleft()
        if part == 1:
            pulses_count[signal] += 1
        if part == 2 and name in lowest_parents and not signal:
            # Found a cycle for one of the lowest parents.
            lowest_parents[name] = press_count
        if name not in modules.keys():
            continue
        module, out_modules = modules[name]
        new_signal = module.recv(src, signal)
        if new_signal is None:
            continue
        for out_module in out_modules:
            pulses.append((out_module, name, new_signal))


def part1(file):
    modules = read_input(file)
    pulses_count = [0, 0]
    for i in range(1000):
        press_button(modules, 1, pulses_count, None, None)
    res = pulses_count[0] * pulses_count[1]
    print(f"Part 1: {res}")


def part2(file):
    modules = read_input(file)
    press_count = 0
    # 4 conjunctions before the final conjunction node that feeds into rx.
    lowest_parents = {"kr": None, "zs": None, "kf": None, "qk": None}
    while True:
        if all(lowest_parents.values()):
            # We found the cycles of all lowest parents, able to calculate
            # final answer from here.
            break
        press_count += 1
        press_button(modules, 2, None, lowest_parents, press_count)
    fewest_button_press = math.lcm(*lowest_parents.values())
    print(f"Part 2: {fewest_button_press}")


file = "input.in"
part1(file)
part2(file)
