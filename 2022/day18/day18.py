"""
Key idea is that if an empty coordinate is next to a droplet coordinate, then that adds 1 to the surface area value.
"""


def read_input(file):
    with open(file, 'r') as f:
        pts = set(tuple(map(int, line.strip().split(','))) for line in f)
    return pts


def is_in_boundary(pt, boundaries):
    return not any(coordinate < boundary[0] or coordinate > boundary[1] for coordinate, boundary in zip(pt, boundaries))


def get_adjacent_pts(pt):
    x, y, z = pt
    adj_pts = {(x, y, z + 1), (x, y, z - 1),
               (x, y + 1, z), (x, y - 1, z),
               (x + 1, y, z), (x - 1, y, z),
               }
    return adj_pts


def get_exterior_area(start_pt, pts, boundaries):
    """
    Flood fill to find exterior area.
    """
    stack = [start_pt]
    visited = set()
    area = 0
    while stack:
        pt = stack.pop()
        if pt in visited:
            continue
        visited.add(pt)
        for adj_pt in get_adjacent_pts(pt):
            if adj_pt in visited or not is_in_boundary(pt, boundaries):
                pass
            elif adj_pt in pts:
                area += 1
            else:
                stack.append(adj_pt)
    return area


def part1(file):
    """
    Each point have 6 adjacent points. If an adjacent point of a droplet is another droplet, then
    the boundary between the 2 would not contribute to the surface area. However, if the adjacent
    point is nothing, then that it will contribute to the surface area.
    """
    pts = read_input(file)
    area = 0
    for pt in pts:
        adj_pts = get_adjacent_pts(pt)
        area += len(adj_pts.difference(pts))
    print(f"Part 1: {area}")


def part2(file):
    pts = read_input(file)
    boundaries = tuple((min(vals) - 1, max(vals) + 1) for vals in zip(*pts))
    start_pt = tuple(r[0] for r in boundaries)
    area = get_exterior_area(start_pt, pts, boundaries)
    print(f"Part 2: {area}")


input_file = "input.in"
part1(input_file)
part2(input_file)
