def read_input(file):
    with open(file, 'r') as f:
        bricks = list()
        for line in f:
            left, right = line.split('~')
            bot_coor = list(map(int, left.split(',')))
            top_coor = list(map(int, right.split(',')))
            if bot_coor[2] > top_coor[2]:
                bot_coor, top_coor = top_coor, bot_coor
            bricks.append((bot_coor, top_coor))
    bricks.sort(key=lambda brick: brick[0][2])
    return bricks


def get_x_y_bounds(bricks):
    """
    Get the maximum x and y values so that I can construct the ceiling tracker.
    """
    max_x_bot = max(brick[0][0] for brick in bricks)
    max_x_top = max(brick[1][0] for brick in bricks)
    max_x = max(max_x_top, max_x_bot)
    max_y_bot = max(brick[0][1] for brick in bricks)
    max_y_top = max(brick[1][1] for brick in bricks)
    max_y = max(max_y_top, max_y_bot)
    return max_x, max_y


def drop_brick(i, brick, ceiling, brick_supports):
    """
    Drop a brick to update ceiling. A brick will continue dropping until it
    hits the top of a ceiling point that is beneath it. Thus, we just need to
    find the subset of ceiling points beneath the brick and get the ceiling
    points with the tallest height, which will be the support for this
    particular brick.
    Code is not the cleanest but it works...
    NOTE: All bricks are just 1 unit in width.
    """
    if brick[0][0] != brick[1][0]:
        # brick long along x axis
        y = brick[0][1]
        x_left = min(brick[0][0], brick[1][0])
        x_right = max(brick[0][0], brick[1][0])
        ceiling_range = [ceiling[pt][y] for pt in range(x_left, x_right + 1)]
        max_ceiling_range = max(ceiling_range, key=lambda pt: pt[0])[0]
        brick_support = set()
        for pt in range(x_left, x_right + 1):
            top_z_pt = ceiling[pt][y]
            if top_z_pt[0] == max_ceiling_range:
                brick_support.add(top_z_pt[1])
        brick_supports[i] = brick_support
        for pt in range(x_left, x_right + 1):
            ceiling[pt][y][0] = max_ceiling_range + 1
            ceiling[pt][y][1] = i
    elif brick[0][1] != brick[1][1]:
        # brick long along y axis
        x = brick[0][0]
        y_left = min(brick[0][1], brick[1][1])
        y_right = max(brick[0][1], brick[1][1])
        ceiling_range = [ceiling[x][pt] for pt in range(y_left, y_right + 1)]
        max_ceiling_range = max(ceiling_range, key=lambda pt: pt[0])[0]
        brick_support = set()
        for pt in range(y_left, y_right + 1):
            top_z_pt = ceiling[x][pt]
            if top_z_pt[0] == max_ceiling_range:
                brick_support.add(top_z_pt[1])
        brick_supports[i] = brick_support
        for pt in range(y_left, y_right + 1):
            ceiling[x][pt][0] = max_ceiling_range + 1
            ceiling[x][pt][1] = i
    else:
        # brick long along z axis
        x, y = brick[0][0], brick[0][1]
        brick_supports[i] = {ceiling[x][y][1]}
        height = brick[1][2] - brick[0][2] + 1
        ceiling[x][y][0] += height
        ceiling[x][y][1] = i


def part1(file):
    bricks = read_input(file)
    max_x, max_y = get_x_y_bounds(bricks)
    ceiling = [[[0, -1] for _ in range(max_y + 1)] for _ in range(max_x + 1)]
    brick_supports = [set() for _ in range(len(bricks))]
    for i, brick in enumerate(bricks):
        drop_brick(i, brick, ceiling, brick_supports)
    # We assume all bricks can be safely removed first, then slowly check
    # through each brick. If the brick is not safe, then we remove it from the
    # valid supports set.
    valid_supports = set(range(len(bricks)))
    for supports in brick_supports:
        # If the number of supports for the brick is 1, that means that the
        # support is crucial and cannot be destroyed. It is not safe to destroy
        # the particular support.
        if len(supports) == 1:
            v = supports.pop()
            if v in valid_supports:
                valid_supports.remove(v)
    print(f"Part 1: {len(valid_supports)}")


def part2(file):
    bricks = read_input(file)
    max_x, max_y = get_x_y_bounds(bricks)
    ceiling = [[[0, -1] for _ in range(max_y + 1)] for _ in range(max_x + 1)]
    brick_supports = [set() for _ in range(len(bricks))]
    for i, brick in enumerate(bricks):
        drop_brick(i, brick, ceiling, brick_supports)
    res = 0
    for i in range(len(bricks)):
        # See which other bricks will fall when we destroy the i-th brick.
        # Can be done in 1 interation (from smaller to larger index bricks)
        # like this since the support of a brick only comes from bricks of
        # smaller indices, and we will already know if a smaller index brick is
        # destroyed once we reach a larger index brick.
        destroyed = {i}  # bricks that are destroyed/fallen will be in here.
        for j, supports in enumerate(brick_supports):
            if not supports - destroyed:
                # All support has fallen. This brick will thus fall too.
                destroyed.add(j)
        res += len(destroyed) - 1  # -1 to ignore the brick itself.
    print(f"Part 2: {res}")


file = "input.in"
part1(file)
part2(file)
