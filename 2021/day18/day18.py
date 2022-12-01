from ast import literal_eval
from math import floor, ceil
from itertools import permutations
from copy import deepcopy


class Node:
    def __init__(self, left_child, right_child, parent=None):
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent
        if isinstance(self.left_child, Node):
            self.left_child.parent = self
        if isinstance(self.right_child, Node):
            self.right_child.parent = self

    def __repr__(self):
        return f"[{self.left_child}, {self.right_child}]"


def read_input():
    with open("input.in", "r") as file:
        numbers = [convert_to_node(literal_eval(number.strip())) for number in file.readlines()]
    return numbers


def convert_to_node(number, parent=None):
    left_child = convert_to_node(number[0], number) if isinstance(number[0], list) else number[0]
    right_child = convert_to_node(number[1], number) if isinstance(number[1], list) else number[1]
    return Node(left_child, right_child, parent)


def add_numbers(n1, n2):
    result = Node(n1, n2)
    reduce(result)
    return result


def reduce(root):
    while True:
        sorted_leaves = sort_numbers(root)
        is_exploded = explode(root, sorted_leaves)
        if is_exploded:
            continue
        is_split = split(root)
        if is_split:
            continue
        if not is_exploded and not is_split:
            return


def sort_numbers(root):
    nodes = []
    nodes += sort_numbers(root.left_child) if isinstance(root.left_child, Node) else [root]
    if isinstance(root.right_child, Node):
        nodes += sort_numbers(root.right_child)
    elif isinstance(root.left_child, Node):
        nodes += [root]
    return nodes


def explode(n, sorted_leaves, layer=0):
    if layer == 4:
        # Explode node
        node_index = sorted_leaves.index(n)
        if node_index != 0:
            if isinstance(sorted_leaves[node_index - 1].right_child, int):
                sorted_leaves[node_index - 1].right_child += n.left_child
            else:
                sorted_leaves[node_index - 1].left_child += n.left_child
        if node_index != len(sorted_leaves) - 1:
            if isinstance(sorted_leaves[node_index + 1].left_child, int):
                sorted_leaves[node_index + 1].left_child += n.right_child
            else:
                sorted_leaves[node_index + 1].right_child += n.right_child
        if n.parent.left_child is n:
            n.parent.left_child = 0
        else:
            n.parent.right_child = 0
        return True
    exploded_left, exploded_right = False, False
    if isinstance(n.left_child, Node):
        exploded_left = explode(n.left_child, sorted_leaves, layer + 1)
    if isinstance(n.right_child, Node) and not exploded_left:
        exploded_right = explode(n.right_child, sorted_leaves, layer + 1)
    return exploded_left or exploded_right


def split(n):
    if isinstance(n.left_child, int) and n.left_child > 9:
        new_node = Node(floor(n.left_child / 2), ceil(n.left_child / 2))
        n.left_child = new_node
        new_node.parent = n
        return True
    split_left, split_right = False, False
    if isinstance(n.left_child, Node):
        split_left = split(n.left_child)
        if split_left:
            return True
    if isinstance(n.right_child, Node) and not split_left:
        split_right = split(n.right_child)
        if split_right:
            return True
    if isinstance(n.right_child, int) and n.right_child > 9:
        new_node = Node(floor(n.right_child / 2), ceil(n.right_child / 2))
        n.right_child = new_node
        new_node.parent = n
        return True
    return False


def get_magnitude(number):
    tot = 0
    left_magnitude = get_magnitude(number.left_child) if isinstance(number.left_child, Node) else number.left_child
    right_magnitude = get_magnitude(number.right_child) if isinstance(number.right_child, Node) else number.right_child
    tot += (3 * left_magnitude + 2 * right_magnitude)
    return tot


def part1():
    numbers = read_input()
    tot = numbers[0]
    for i in range(1, len(numbers)):
        tot = add_numbers(tot, numbers[i])
    magnitude = get_magnitude(tot)

    print(f"Part 1: {magnitude}")


def part2():
    numbers = read_input()
    number_pairs = list(permutations(numbers, 2))
    max_magnitude = -1
    for pair in number_pairs:
        number = add_numbers(deepcopy(pair[0]), deepcopy(pair[1]))
        magnitude = get_magnitude(number)
        if magnitude > max_magnitude:
            max_magnitude = magnitude
    print(f"Part 2: {max_magnitude}")


if __name__ == "__main__":
    part1()
    part2()
