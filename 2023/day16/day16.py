def read_input(file):
    with open(file, 'r') as f:
        return tuple(line.strip() for line in f)


def dirn_2_k(dirn):
    """
    Convert direction to index of `visited`'s 3rd dimension, so I can mark it
    in `visited`.
    """
    mapping = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}
    return mapping[dirn]


def dfs(coor, dirn, grid, visited, max_i, max_j):
    """
    Depth first search each light path to find the tiles that are energized.
    """
    q = [(coor, dirn)]
    while q:
        coor, dirn = q.pop()
        new_coor = (coor[0] + dirn[0], coor[1] + dirn[1])
        i, j, k = new_coor[0], new_coor[1], dirn_2_k(dirn)
        if i < 0 or i >= max_i or j < 0 or j >= max_j:
            # Out of bounds
            continue
        if visited[i][j][k]:
            # Already traverse this coordinate in this direction.
            continue
        else:
            visited[i][j][k] = True
        val = grid[i][j]
        if val == '|' and (dirn == (0, 1) or dirn == (0, -1)):
            # Split light to go top and bot.
            q.append((new_coor, (1, 0)))
            q.append((new_coor, (-1, 0)))
        elif val == '-' and (dirn == (1, 0) or dirn == (-1, 0)):
            # Split light to go right and left.
            q.append((new_coor, (0, 1)))
            q.append((new_coor, (0, -1)))
        elif val == '\\':
            # The reflection by this mirror is just swapping the direction
            # coordinates,
            q.append((new_coor, (dirn[1], dirn[0])))
        elif val == '/':
            # The reflection by this mirror is just swapping the direction
            # coordinates and multiplying by -1.
            q.append((new_coor, (-dirn[1], -dirn[0])))
        else:
            # This tile allows light from this direction to pass through.
            q.append((new_coor, dirn))


def get_count_energized(visited, max_i, max_j):
    """
    Get the number of visited (energized) tiles after light travel have been
    simulated.
    """
    count = 0
    for i in range(max_i):
        for j in range(max_j):
            count += int(any(visited[i][j]))
    return count


def simulate(start, dirn, grid, max_i, max_j):
    """
    Simulate the light travel from the given start and direction and return the
    number of energized tiles.
    """
    visited = [[[0] * 4 for _ in range(max_j)] for _ in range(max_i)]
    dfs(start, dirn, grid, visited, max_i, max_j)
    energized_count = get_count_energized(visited, max_i, max_j)
    return energized_count


def visualize(visited, max_i, max_j):
    """
    Visualize the grid and visited tiles. Used for debugging.
    """
    for i in range(max_i):
        for j in range(max_j):
            if any(visited[i][j]):
                print('#', end='')
            else:
                print('.', end='')
        print()


def part1(file):
    grid = read_input(file)
    max_i, max_j = len(grid), len(grid[0])
    energized_count = simulate((0, -1), (0, 1), grid, max_i, max_j)
    print(f"Part 1: {energized_count}")


def part2(file):
    grid = read_input(file)
    max_i, max_j = len(grid), len(grid[0])
    max_energized_count = 0
    for i in range(max_i):
        # Enter from left
        energized_count = simulate((i, -1), (0, 1), grid, max_i, max_j)
        max_energized_count = max(max_energized_count, energized_count)
        # Enter from right
        energized_count = simulate((i, max_j), (0, -1), grid, max_i, max_j)
        max_energized_count = max(max_energized_count, energized_count)
    for j in range(max_j):
        # Enter from top
        energized_count = simulate((-1, j), (1, 0), grid, max_i, max_j)
        max_energized_count = max(max_energized_count, energized_count)
        # Enter from bot
        energized_count = simulate((max_i, j), (-1, 0), grid, max_i, max_j)
        max_energized_count = max(max_energized_count, energized_count)
    print(f"Part 1: {max_energized_count}")


file = "input.in"
part1(file)
part2(file)
