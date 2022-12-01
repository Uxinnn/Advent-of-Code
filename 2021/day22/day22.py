def read_input():
    steps = []
    with open("input.in", "r") as file:
        for line in file:
            raw_action, raw_pts = line.strip().split()
            action = 1 if raw_action == "on" else 0
            raw_pts = [j for row in [raw_pt[2:].split("..") for raw_pt in raw_pts.split(',')] for j in row]
            pts = (action, tuple([int(pt) for pt in raw_pts]))
            steps.append(pts)

    return steps


def filter_input(steps):
    filtered_steps = []
    for step in steps:
        if not any(map(lambda x: x < -50 or x > 50, step[1])):
            filtered_steps.append(step)
    return filtered_steps


def get_signed_intersection(sign, cube0, cube1):
    min_x, max_x, min_y, max_y, min_z, max_z = cube0
    intersect = (min_x if min_x > cube1[0] else cube1[0],
                 max_x if max_x < cube1[1] else cube1[1],
                 min_y if min_y > cube1[2] else cube1[2],
                 max_y if max_y < cube1[3] else cube1[3],
                 min_z if min_z > cube1[4] else cube1[4],
                 max_z if max_z < cube1[5] else cube1[5])
    return 0 if sign == 1 else 1, intersect


def carry_out_step(step, on):
    action = step[0]
    min_x, max_x, min_y, max_y, min_z, max_z = step[1]
    new_on = on.copy()
    if action and not on:
        new_on.append(step)
        return new_on
    if action:
        new_on.append(step)
        # On, add points
        for sign, cube in on:
            if (min_x > cube[1]) or (max_x < cube[0]) or (min_y > cube[3]) or (max_y < cube[2]) or (
                    min_z > cube[5]) or (max_z < cube[4]):
                # No overlap
                continue
            else:
                # Append the signed cube of intersection
                new_on.append(get_signed_intersection(sign, step[1], cube))
    else:
        # Off, remove points
        for sign, cube in on:
            if not ((min_x > cube[1]) or (max_x < cube[0]) or (min_y > cube[3]) or (max_y < cube[2]) or (
                    min_z > cube[5]) or (max_z < cube[4])):
                # Have overlap
                # Append the signed cube of intersection
                new_on.append(get_signed_intersection(sign, step[1], cube))
    return new_on


def carry_out_all_steps(steps, on):
    for step in steps:
        on = carry_out_step(step, on)
    return on


def compute_volume(step):
    sign, cube = step
    volume = (cube[1] - cube[0] + 1) * (cube[3] - cube[2] + 1) * (cube[5] - cube[4] + 1) * (1 if sign else -1)
    return volume


def compute_total_volume(final_on):
    return sum(map(compute_volume, final_on))


def part1():
    steps = filter_input(read_input())
    final_on = carry_out_all_steps(steps, [])
    final_volume = compute_total_volume(final_on)
    print(f"Part 1: {final_volume}")


def part2():
    steps = read_input()
    final_on = carry_out_all_steps(steps, [])
    final_volume = compute_total_volume(final_on)
    print(f"Part 1: {final_volume}")


if __name__ == "__main__":
    part1()
    part2()
