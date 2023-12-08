from math import lcm


def read_input(file):
    with open(file, 'r') as f:
        instrs = f.readline().strip()
        f.readline()
        directions = dict()
        for line in f:
            line = line.strip()
            src, left, right = line[:3], line[7:10], line[12:15]
            directions[src] = {'L': left, 'R': right}
        return instrs, directions


def get_instrs_generator(instrs):
    """
    Creates an infinite generator that constantly loops through the
    instructions given.
    """
    def get_instrs():
        i = 0
        while True:
            instr = instrs[i]
            i = (i + 1) % len(instrs)
            yield instr
    return get_instrs


def navigate_network(node, part, instrs, directions):
    """
    Simulate the navigation of the network from the given start node to the end
    of the network.
    """
    get_instrs = get_instrs_generator(instrs)
    step_count = 0
    for instr in get_instrs():
        node = directions[node][instr]
        step_count += 1
        if (part == 1 and node == "ZZZ") or (part == 2 and node.endswith('Z')):
            break
    return step_count


def part1(file):
    instrs, directions = read_input(file)
    start_node = "AAA"
    step_count = navigate_network(start_node, 1, instrs, directions)
    print(f"Part 1: {step_count}")


def part2(file):
    instrs, directions = read_input(file)
    nodes = [node for node in directions.keys() if node.endswith('A')]
    step_counts = list()
    for node in nodes:
        step_count = navigate_network(node, 2, instrs, directions)
        step_counts.append(step_count)
    # Lowest common multiple is when all start nodes ends with a Z.
    lowest_common_step_count = lcm(*step_counts)
    print(f"Part 2: {lowest_common_step_count}")


file = "input.in"
part1(file)
part2(file)
