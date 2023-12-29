def read_input(file):
    with open(file, 'r') as f:
        grid = [line.strip() for line in f]
    return grid


def get_start_and_end_pts(grid):
    """
    Find and return the starting and ending points in the grid.
    """
    start = (0, grid[0].index('.'))
    end = (len(grid) - 1, grid[-1].index('.'))
    return start, end


def replace_slopes(grid):
    """
    Replace all '<>^v' with '.'
    """
    for i in range(len(grid)):
        for slope in "<>v^":
            grid[i] = grid[i].replace(slope, '.')


def get_adjacency_list(grid):
    """
    Convert grid to adjacency list of intersection points.
    First initialize the list with all '.' points in the grid, then slowly
    merge points together. If a point has only 2 neighbouring points, then we
    remove it and join the 2 neighboring points together with their added
    weight. Idea was from a post on reddit that I saw.
    """
    max_i, max_j = len(grid), len(grid[0])
    adjacency_list = dict()
    # Fill the adjacency list with all '.' points first.
    for i in range(max_i):
        for j in range(max_j):
            pt = grid[i][j]
            if pt == '.':
                neighboring_pts = list()
                for i2, j2 in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                    if -1 < i2 < max_i and -1< j2 < max_j and grid[i2][j2] == '.':
                        neighboring_pts.append([i2, j2, 1])
                adjacency_list[(i, j)] = neighboring_pts
    # Slowly remove all points with 2 neighbors, while joining the 2 neighbors
    # together.
    while True:
        modified = False
        for pt, neighboring_pts in adjacency_list.items():
            i, j = pt
            if len(neighboring_pts) == 2:
                i1, j1, w1 = neighboring_pts[0]
                i2, j2, w2 = neighboring_pts[1]
                w = w1 + w2
                # Join both neighbors to each other.
                for npt in adjacency_list[(i1, j1)]:
                    if npt[0] == i and npt[1] == j:
                        npt[0] = i2
                        npt[1] = j2
                        npt[2] = w
                for npt in adjacency_list[(i2, j2)]:
                    if npt[0] == i and npt[1] == j:
                        npt[0] = i1
                        npt[1] = j1
                        npt[2] = w
                # Remove old point
                del adjacency_list[pt]
                modified = True
                break
        if not modified:
            # No more points with only 2 neighbors exist.
            break
    return adjacency_list


def dfs(start, end, grid):
    """
    Used for part 1 with the grid and slopes.
    """
    max_i, max_j = len(grid), len(grid[0])
    stack = [[start, set(), 0]]
    max_path_len = 0
    while stack:
        pt, visited, path_len = stack.pop()
        i, j = pt
        if (pt in visited or i < 0 or i >= max_i or j < 0 or j >= max_j or
                grid[i][j] == "#"):
            continue
        visited.add(pt)
        if pt == end:
            max_path_len = max(max_path_len, path_len)
        if grid[i][j] in '>.':
            next_pt = [(i, j + 1), visited.copy(), path_len + 1]
            stack.append(next_pt)
        if grid[i][j] in '<.':
            next_pt = [(i, j - 1), visited.copy(), path_len + 1]
            stack.append(next_pt)
        if grid[i][j] in '^.':
            next_pt = [(i - 1, j), visited.copy(), path_len + 1]
            stack.append(next_pt)
        if grid[i][j] in 'v.':
            next_pt = [(i + 1, j), visited.copy(), path_len + 1]
            stack.append(next_pt)
    return max_path_len


def dfs2(start, end, adjacency_list):
    """
    Used for part 2 with the adjacency list and no slopes.
    """
    stack = [[start, set(), 0]]
    max_path_len = 0
    while stack:
        pt, visited, path_len = stack.pop()
        if pt in visited:
            continue
        visited.add(pt)
        if pt == end:
            max_path_len = max(max_path_len, path_len)
        for i2, j2, w in adjacency_list[pt]:
            next_pt = [(i2, j2), visited.copy(), path_len + w]
            stack.append(next_pt)
    return max_path_len


def part1(file):
    grid = read_input(file)
    start, end = get_start_and_end_pts(grid)
    longest_path = dfs(start, end, grid)
    print(f"Part 1: {longest_path}")


def part2(file):
    grid = read_input(file)
    start, end = get_start_and_end_pts(grid)
    replace_slopes(grid)
    adjacency_list = get_adjacency_list(grid)
    longest_path = dfs2(start, end, adjacency_list)
    print(f"Part 2: {longest_path}")


file = "input.in"
part1(file)
part2(file)
