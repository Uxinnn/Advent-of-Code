class Node:
    def __init__(self, name, size=0, parent=None):
        self.name = name
        self.size = size
        self.parent = parent
        self.tot_size = 0
        self.children = dict()


def read_input():
    """
    Reads raw input and parse it into a tree of nodes.
    """
    with open("input.in", 'r') as f:
        lines = f.readlines()[1:]
    root_node = Node('/')
    current_node = root_node
    for line in lines:
        parts = line.split()
        if parts[0] == '$':
            # line is a command
            if parts[1] == "cd":
                if parts[2] == "..":
                    # Go up 1 level
                    current_node = current_node.parent
                else:
                    current_node = current_node.children[parts[2]]
            elif parts[1] == "ls":
                pass
        else:
            # ls content
            if parts[0] == "dir":
                current_node.children[parts[1]] = Node(parts[1], parent=current_node)
            else:
                current_node.size += int(parts[0])
    return root_node


def print_node(node):
    """
    For debugging purposes. Prints the contents of a node and all its children.
    """
    print(f"{node.name}: {node.size}, {node.tot_size}, {node.parent}")
    for k, v in node.children.items():
        print(k)
        print_node(v)


def calc_total_size(node, tot_size=0):
    """
    Calculate the total size of a directory.
    Includes the files in the directory and all its subdirectories.
    """
    tot_size += node.size
    for child in node.children.values():
        tot_size += calc_total_size(child)
    node.tot_size = tot_size
    return tot_size


def part1():
    root_node = read_input()
    calc_total_size(root_node)
    max_file_size = 100000
    queue = [root_node]
    answer = 0
    while queue:
        node = queue.pop(0)
        if node.tot_size <= max_file_size:
            answer += node.tot_size
        queue += [child for child in node.children.values()]
    print(f"Part 1: {answer}")


def part2():
    tot_disk_space = 70000000
    target_unused_space = 30000000
    root_node = read_input()
    calc_total_size(root_node)
    space_to_free_up = target_unused_space - (tot_disk_space - root_node.tot_size)
    queue = [root_node]
    dir_to_del_size = root_node.tot_size
    while queue:
        node = queue.pop(0)
        if node.tot_size > space_to_free_up:
            dir_to_del_size = min(dir_to_del_size, node.tot_size)
        queue += [child for child in node.children.values()]
    print(f"Part 2: {dir_to_del_size}")


part1()
part2()
