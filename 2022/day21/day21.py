from operator import add, sub, mul, floordiv


def read_input(file):
    """
    Equations (a = op(b, c)) are encoded in the form `a: (b, c, op)`.
    """
    with open(file, 'r') as f:
        monkeys = dict()
        for line in f:
            parts = line.strip().split()
            monkey = parts[0][:-1]
            dep = int(parts[1]) if len(parts) == 2 else (parts[1], parts[3], parts[2])
            monkeys[monkey] = dep
    return monkeys


def sign2op(sign):
    mappings = {"+": add, "-": sub, "*": mul, "/": floordiv}
    return mappings[sign]


def reverse_sign(sign):
    mappings = {'+': '-', '-': '+', '*': '/', '/': '*'}
    return mappings[sign]


def solve(monkey, monkeys):
    """
    Recursive solution to find the value of the specified monkey.
    """
    dep = monkeys[monkey]
    if isinstance(dep, int):
        return dep
    else:
        new_dep = sign2op(dep[2])(solve(dep[0], monkeys), solve(dep[1], monkeys))
        monkeys[monkey] = new_dep
        return new_dep


def reroot(monkey, old_root, new_root, monkeys):
    """
    Reroot the equation tree to obtain a new root node.
    Root equality becomes +0. All operations between the new root and old root have to be modified. These operations
    are found by returning 1 from the new root all the way up to the old root.
    Other operations should stay the same (Operations are unaffected if both their children returns 0).
    Try to draw the operation tree out to visualize things if it gets confusing.
    """
    if monkey == new_root:
        return 1
    dep = monkeys[monkey]
    if isinstance(dep, int):
        return 0
    m1, m2, sign = dep
    flag1 = reroot(m1, old_root, new_root, monkeys)
    flag2 = reroot(m2, old_root, new_root, monkeys)
    if flag1 == 1 or flag2 == 1:
        m1, m2 = (m1, m2) if flag1 == 1 else (m2, m1)
        if monkey == old_root:
            # Since its an equality, just pass on 1 value to the other side.
            monkeys[m1] = (monkey, m2, '+')
            monkeys[old_root] = 0
        else:
            # Creating new equation
            if flag2 == 1 and (sign == '-' or sign == '/'):
                # E.g. a = b - c will have to be modified to c = b - a.
                monkeys[m1] = (m2, monkey, sign)
            else:
                monkeys[m1] = (monkey, m2, reverse_sign(sign))
            # Remove old equation
            del monkeys[monkey]
        return 1
    return 0


def part1(file):
    monkeys = read_input(file)
    root_val = solve("root", monkeys)
    print(f"Part 1: {root_val}")


def part2(file):
    monkeys = read_input(file)
    new_root = "humn"
    old_root = "root"
    reroot(old_root, old_root, new_root, monkeys)
    root_val = solve(new_root, monkeys)
    print(f"Part 2: {root_val}")


input_file = "input.in"
part1(input_file)
part2(input_file)
