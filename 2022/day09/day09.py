def read_input():
    with open("input.in", 'r') as f:
        cmds = list(map(lambda cmd: (cmd[0], int(cmd[1])), [line.strip().split() for line in f.readlines()]))
    return cmds


def move(snake, direction):
    direction_map = {'U': (1, 1),
                     'D': (1, -1),
                     'L': (0, -1),
                     'R': (0, 1)
                     }
    # move head
    i, v = direction_map[direction]
    snake[0][i] += v
    # move the rest of the body
    for j in range(1, len(snake)):
        diff = [x - y for x, y in zip(snake[j - 1], snake[j])]
        if abs(diff[0]) > 1 or abs(diff[1]) > 1:
            # move back part, all scenarios involve the front part being 2 or -2 distance away from
            # the back part.
            for dist in (2, -2):
                if dist in diff:
                    for k in [c for c in diff if c == dist]:
                        diff[diff.index(k)] -= dist // abs(dist)  # -1 if dist is 2, +1 if dist is -2
            snake[j][0] += diff[0]
            snake[j][1] += diff[1]


def track_tail(past_coors, tail):
    if tuple(tail) not in past_coors:
        past_coors.add(tuple(tail))


def part1():
    cmds = read_input()
    snake = [[0, 0], [0, 0]]
    past_coors = set()
    for direction, step in cmds:
        for _ in range(step):
            move(snake, direction)
            track_tail(past_coors, snake[-1])
    print(f"Part 1: {len(past_coors)}")


def part2():
    cmds = read_input()
    snake = [[0, 0] for _ in range(10)]
    past_coors = set()
    for direction, step in cmds:
        for _ in range(step):
            move(snake, direction)
            track_tail(past_coors, snake[-1])
    print(f"Part 2: {len(past_coors)}")


part1()
part2()
