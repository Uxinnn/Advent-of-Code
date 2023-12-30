from collections import defaultdict


def read_input(file):
    with open(file, 'r') as f:
        nodes = defaultdict(list)
        for line in f:
            line = line.strip()
            src, line = line.split(': ')
            dsts = line.split()
            for dst in dsts:
                nodes[src].append(dst)
                nodes[dst].append(src)
    return nodes


def get_interconnect_count(group_1, group_2, nodes):
    """
    Get the number of wires between the 2 groups.
    """
    count = 0
    for node in group_1:
        neighbors = nodes[node]
        for neighbor in neighbors:
            if neighbor in group_2:
                count += 1
    return count


def get_degree_heuristic(node, group_1, group_2, nodes):
    """
    Estimated heuristic of how likely a node belongs to group 2.
    Given node must be in group 2.
    For the node, check how many connections it has to the group 2 nodes,
    compared to the connections it has to the group 1 nodes.
    """
    neighbors = nodes[node]
    in_degree = sum([1 for neighbor in neighbors if neighbor in group_2])
    out_degree = sum([1 for neighbor in neighbors if neighbor in group_1])
    return in_degree - out_degree


def part1(file):
    nodes = read_input(file)
    # Initialize 2 groups.
    # 1 group has a random node, the other has all other nodes.
    group_1_seed = list(nodes.keys())[0]
    group_1 = {group_1_seed}
    group_2 = set(nodes.keys())
    group_2.remove(group_1_seed)
    interconnect_count = len(nodes[group_1_seed])
    # Node shifting till criteria is reached.
    while interconnect_count != 3:
        # Find the node in group 2 with the smallest heuristic value, which
        # indicates that it is the most likely node to be in group 1, instead
        # of group 2.
        min_node, min_val = None, float("inf")
        for n2 in group_2:
            score = get_degree_heuristic(n2, group_1, group_2, nodes)
            if score < min_val:
                min_node = n2
                min_val = score
        # Remove the node from group 2 and add it to group 1.
        group_1.add(min_node)
        group_2.remove(min_node)
        interconnect_count = get_interconnect_count(group_1, group_2, nodes)
    # 2 groups with 3 interconnections have been found.
    res = len(group_1) * len(group_2)
    print(f"Part 1: {res}")


file = "input.in"
part1(file)
