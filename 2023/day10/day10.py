def read_input(file):
    with open(file, 'r') as f:
        pipes = [line.strip() for line in f]
        return pipes


def convert_S(S_coor, pipes):
    """
    Replace S to the appropriate pipe type in its place.
    """
    i, j = S_coor
    max_i, max_j = len(pipes), len(pipes[0])
    # Find which 2 directions does S point to using its adjacent pipes
    adj_pipes_2_symbol = {(i, j - 1): [{'-', 'L', 'F'}, 'L'],
                          (i - 1, j): [{'|', '7', 'F'}, 'U'],
                          (i + 1, j): [{'|', 'L', 'J'}, 'D'],
                          (i, j + 1): [{'-', 'J', '7'}, 'R'],
                          }
    adjacent_dirns = list()
    for (adj_i, adj_j), (valid_symbols, dirn) in adj_pipes_2_symbol.items():
        if -1 < adj_i < max_i and -1 < adj_j < max_j:
            if pipes[adj_i][adj_j] in valid_symbols:
                adjacent_dirns.append(dirn)
    # Using the 2 directions which S points to, deduce the pipe type that
    # should be used in place of S.
    adjacent_dirns = "".join(sorted(adjacent_dirns))
    adjacent_dirns_2_S_val = {'LU': 'J', 'LR': '-', 'DU': '|',
                              'DL': '7', 'RU': 'L', 'DR': 'F',
                              }
    S_val = adjacent_dirns_2_S_val[adjacent_dirns]
    # Replace S with the correct pipe
    pipes[i] = pipes[i][:j] + S_val + pipes[i][j + 1:]


def find_next(main_pipe, pipes):
    """
    Find the next pipe in the main_pipe and add it to the main_pipe.
    """
    tile_2_adj = {'|': ((-1, 0), (1, 0)),
                  '-': ((0, -1), (0, 1)),
                  'L': ((-1, 0), (0, 1)),
                  'J': ((-1, 0), (0, -1)),
                  '7': ((1, 0), (0, -1)),
                  'F': ((1, 0), (0, 1)),
                  }
    last_tile_coor = main_pipe[-1]
    if len(main_pipe) < 2:
        # When the main_pipe only has 1 coordinate (The start S coordinate)
        prev_tile_coor = None
    else:
        # Use this so we don't add a pipe that is already part of the main_pipe.
        # (So we don't go backwards)
        prev_tile_coor = main_pipe[-2]
    last_tile = pipes[last_tile_coor[0]][last_tile_coor[1]]
    for adj_i, adj_j in tile_2_adj[last_tile]:
        next_tile_coor = (last_tile_coor[0] + adj_i, last_tile_coor[1] + adj_j)
        if prev_tile_coor is None or next_tile_coor != prev_tile_coor:
            main_pipe.append(next_tile_coor)
            break


def get_main_pipe(pipes):
    # Locate S
    for i, row in enumerate(pipes):
        if 'S' in row:
            j = row.index('S')
            break
    S_coor = (i, j)
    convert_S(S_coor, pipes)
    main_pipe = [S_coor]
    find_next(main_pipe, pipes)
    # Keep extending the main_pipe until it loops back on itself.
    while main_pipe[-1] != main_pipe[0]:
        find_next(main_pipe, pipes)
    main_pipe = main_pipe[:-1]
    return main_pipe


def replace_interior_coors(grid, main_pipe, pipes, max_i, max_j):
    """
    All interior points will be tagged with a '1'.
    Find interior points based on parity. Everytime a wall is met, switch
    parity.
    For '7LJF', need to check previous edge since it can either be a blocking
    wall or you can just be walking along the wall.
    """
    for i in range(max_i):
        parity = 0
        prev_edge = None
        for j in range(max_j):
            if (i, j) in main_pipe:
                sym = pipes[i][j]
                if sym == '|':
                    parity = (parity + 1) % 2
                elif sym == '7' and prev_edge == 'L':
                    parity = (parity + 1) % 2
                elif sym == 'J' and prev_edge == 'F':
                    parity = (parity + 1) % 2
                grid[i][j] = 0
                if sym != '-':
                    prev_edge = sym
            else:
                grid[i][j] = parity


def part1(file):
    pipes = read_input(file)
    main_pipe = get_main_pipe(pipes)
    furthest_idx = len(main_pipe) // 2
    print(f"Part 1: {furthest_idx}")


def part2(file):
    pipes = read_input(file)
    main_pipe = set(get_main_pipe(pipes))
    max_i, max_j = len(pipes), len(pipes[0])
    grid = [['v'] * max_j for _ in range(max_i)]
    replace_interior_coors(grid, main_pipe, pipes, max_i, max_j)
    interior_tiles_count = 0
    for row in grid:
        interior_tiles_count += row.count(1)
    print(f"Part 2: {interior_tiles_count}")


file = "input.in"
part1(file)
part2(file)
