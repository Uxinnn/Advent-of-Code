import sympy as sp


def read_input(file):
    with open(file, 'r') as f:
        hailstones = list()
        for line in f:
            line = line.strip()
            raw_pos, raw_vel = line.split(" @ ")
            pos = tuple(map(int, raw_pos.split(", ")))
            vel = tuple(map(int, raw_vel.split(", ")))
            hailstones.append((pos, vel))
    return hailstones


def get_mc(hs):
    pos, vel = hs
    m = vel[1] / vel[0]
    c = pos[1] - m * pos[0]
    return m, c


def is_in_future(hs, x1):
    x0 = hs[0][0]
    vx = hs[1][0]
    return (x1 - x0) / vx >= 0


def part1(file):
    hailstones = read_input(file)
    valid_intersection_count = 0
    if file == "example.in":
        min_bound, max_bound = 7, 27
    else:
        min_bound, max_bound = 200000000000000, 400000000000000
    for i, hs1 in enumerate(hailstones):
        for j in range(i):
            hs2 = hailstones[j]
            m1, c1 = get_mc(hs1)
            m2, c2 = get_mc(hs2)
            if m1 == m2:
                # parallel lines, will not intersect
                continue
            # get intersection point
            x = (c2 - c1) / (m1 - m2)
            y = m1 * x + c1
            if (min_bound <= x <= max_bound and min_bound <= y <= max_bound and
                    is_in_future(hs1, x) and is_in_future(hs2, x)):
                valid_intersection_count += 1
    print(f"Part 1: {valid_intersection_count}")


def part2(file):
    hailstones = read_input(file)
    vel_x, vel_y, vel_z = sp.symbols('vel_x, vel_y, vel_z')
    pos_x, pos_y, pos_z = sp.symbols('pos_x, pos_y, pos_z',
                                     positive=True,
                                     integer=True,
                                     )
    linear_system = []
    for hs in hailstones:
        pos, vel = hs
        linear_system.append(sp.Eq((pos[0] - pos_x) * (vel_y - vel[1]),
                            (pos[1] - pos_y) * (vel_x - vel[0])))
        linear_system.append(sp.Eq((pos[0] - pos_x) * (vel_z - vel[2]),
                            (pos[2] - pos_z) * (vel_x - vel[0])))
    vel_x, vel_y, vel_z, pos_x, pos_y, pos_z = sp.solve(
        linear_system, [vel_x, vel_y, vel_z, pos_x, pos_y, pos_z])[0]
    print(f"Part 2: {pos_z + pos_y + pos_x}")


file = "input.in"
part1(file)
part2(file)
