from heapq import heappop, heappush


def read_input(file):
    with open(file, 'r') as f:
        return tuple([int(n) for n in row.strip()] for row in f)


def dijkstra(grid, part):
    """
    States are in the form: (heat_loss, coordinate, direction, count).
    Count: How many steps are taken in the current direction.
    Direction: (0, 1) --> Right
               (0, -1) --> Left
               (1, 0) --> Top
               (-1, 0) --> Bot
    Visited states are stored in the form (i, j, direction, count).
    This is so as for each coordinate, different directions and count taken to
    reach the coordinate can lead to different paths in reaching the destination
    (and hence different heat_loss).
    """
    max_i, max_j = len(grid), len(grid[0])
    dst = (max_i - 1, max_j - 1)
    h = [(0, (0, 0), (0, 1), 0), (0, (0, 0), (1, 0), 0)]
    visited = set()
    while h:
        heat_loss, (i, j), dirn, count = heappop(h)
        # Check for stop condition and if coordinate has been visited.
        if (i, j) == dst and (part == 1 or (part == 2 and count >= 4)):
            # Part 1 simply needs to reach destination.
            # Part 2 needs to ensure a minimum of 4 steps is taken in the last
            # direction before the heat_loss found is valid.
            return heat_loss
        elif (i, j, dirn, count) in visited:
            continue
        else:
            visited.add((i, j, dirn, count))
        # Move to next neighbouring coordinate.
        for next_dirn in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            next_coor = (i + next_dirn[0], j + next_dirn[1])
            if (next_coor[0] < 0 or next_coor[0] >= max_i or
                    next_coor[1] < 0 or next_coor[1] >= max_j):
                # Out of bounds
                continue
            elif (dirn and dirn[0] + next_dirn[0] == 0 and
                  dirn[1] + next_dirn[1] == 0):
                # Reverse direction
                continue
            # unique condition for part 1
            elif part == 1 and next_dirn == dirn and count == 3:
                continue
            # unique conditions for part 2
            elif part == 2 and count == 10 and next_dirn == dirn:
                continue
            elif part == 2 and count < 4 and next_dirn != dirn:
                continue
            else:
                new_heat_loss = heat_loss + grid[next_coor[0]][next_coor[1]]
                new_count = count + 1 if dirn == next_dirn else 1
                heappush(h, (new_heat_loss, next_coor, next_dirn, new_count))


def part1(file):
    grid = read_input(file)
    heat_loss = dijkstra(grid, part=1)
    print(f"Part 1: {heat_loss}")


def part2(file):
    grid = read_input(file)
    heat_loss = dijkstra(grid, part=2)
    print(f"Part 2: {heat_loss}")


file = "input.in"
part1(file)
part2(file)
