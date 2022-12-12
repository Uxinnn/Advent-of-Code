from collections import defaultdict
import heapq


class Node:
    def __init__(self, coor, f, steps):
        self.coor = coor
        self.f = f
        self.steps = steps

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.f < other.f

    def __gt__(self, other):
        if isinstance(other, Node):
            return self.f > other.f

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.f == other.f

    def __hash__(self):
        return hash(self.get_coor())

    def __repr__(self):
        return f"{self.get_coor()}: {self.get_steps()}, {self.get_f()}"

    def get_steps(self):
        return self.steps

    def get_coor(self):
        return self.coor

    def get_f(self):
        return self.f

    def same_coor(self, other):
        if isinstance(other, Node):
            return self.get_coor() == other.get_coor()


def add_adj_mat_entry(adj_mat, c1, c2, i1, j1, i2, j2):
    c_diff = ord(c2) - ord(c1)
    if c_diff < 2:
        adj_mat[(i1, j1)].append((c_diff, (i2, j2)))
    return 0


def read_input(file):
    adj_mat = defaultdict(list)
    src, dst = (0, 0), (0, 0)
    a_coors = []
    with open(file, 'r') as f:
        raw_input = [line.strip() for line in f]
        for i, row in enumerate(raw_input):
            for j, c in enumerate(row):
                if c == 'S':
                    src = (i, j)
                    c = 'a'
                elif c == 'E':
                    dst = (i, j)
                    c = 'z'
                if c == 'a':
                    a_coors.append((i, j))
                if i != 0:
                    top_c = raw_input[i - 1][j]
                    if top_c == 'S':
                        top_c = 'a'
                    if top_c == 'E':
                        top_c = 'z'
                    add_adj_mat_entry(adj_mat, c, top_c, i, j, i - 1, j)
                if i != len(raw_input) - 1:
                    bot_c = raw_input[i + 1][j]
                    if bot_c == 'S':
                        bot_c = 'a'
                    if bot_c == 'E':
                        bot_c = 'z'
                    add_adj_mat_entry(adj_mat, c, bot_c, i, j, i + 1, j)
                if j != 0:
                    left_c = raw_input[i][j - 1]
                    if left_c == 'S':
                        left_c = 'a'
                    if left_c == 'E':
                        left_c = 'z'
                    add_adj_mat_entry(adj_mat, c, left_c, i, j, i, j - 1)
                if j != len(row) - 1:
                    right_c = raw_input[i][j + 1]
                    if right_c == 'S':
                        right_c = 'a'
                    if right_c == 'E':
                        right_c = 'z'
                    add_adj_mat_entry(adj_mat, c, right_c, i, j, i, j + 1)
    return adj_mat, src, dst, a_coors


def astar_search(adj_mat, src, dst):
    visited = set()
    visited_f = dict()
    frontier = [Node(src, 0, 0)]
    heapq.heapify(frontier)
    while frontier:
        node = heapq.heappop(frontier)
        visited.add(node.get_coor())
        visited_f[node.get_coor()] = node.get_f()
        new_node_steps = node.get_steps() + 1
        for h_change, successor in adj_mat[node.get_coor()]:
            if successor == dst:
                return new_node_steps
            new_f = node.get_f() + 1 - h_change
            new_frontier_node = Node(successor, new_f, new_node_steps)
            to_add = True
            for frontier_node in frontier:
                if frontier_node.get_coor() == successor and frontier_node.get_f() <= new_f:
                    to_add = False
                    break
            if successor in visited and visited_f[successor] <= new_f:
                to_add = False
            if to_add:
                heapq.heappush(frontier, new_frontier_node)


def part1(file):
    adj_mat, src, dst, _ = read_input(file)
    steps = astar_search(adj_mat, src, dst)
    print(f"Part 1: {steps}")


def part2(file):
    adj_mat, src, dst, a_coors = read_input(file)
    steps = [astar_search(adj_mat, src, dst) for src in a_coors]
    min_step = min([step for step in steps if step])
    print(f"Part 2: {min_step}")


file = "input.in"
part1(file)
part2(file)
