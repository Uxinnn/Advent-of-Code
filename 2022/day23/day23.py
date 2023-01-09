from operator import add


def read_input(file):
    with open(file, 'r') as f:
        elves = set((i, j) for i, row in enumerate(f) for j, pt in enumerate(row) if pt == '#')
    return elves


class DirectionGenerator:
    def __init__(self):
        self.direction = ['N', 'S', 'W', 'E']

    def get_directions(self):
        directions = tuple(self.direction)
        front_direction = self.direction.pop(0)
        self.direction.append(front_direction)
        return directions


def check_empty_surroundings(elf, elves):
    y, x = elf
    check_pts = ((y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
                 (y, x - 1), (y, x + 1),
                 (y + 1, x - 1), (y + 1, x), (y + 1, x + 1),
                 )
    return not any([pt in elves for pt in check_pts])


def propose_move(elf, directions, elves):
    direction2pts = {'N': ((-1, -1), (-1, 0), (-1, 1)),
                     'S': ((1, -1), (1, 0), (1, 1)),
                     'E': ((-1, 1), (0, 1), (1, 1)),
                     'W': ((-1, -1), (0, -1), (1, -1)),
                     }
    proposed_pt = elf
    for direction in directions:
        check_pts = tuple(tuple(map(add, elf, check_pt)) for check_pt in direction2pts[direction])
        if not any([pt in elves for pt in check_pts]):
            proposed_pt = check_pts[1]
            break
    return proposed_pt


def get_elves_bounds(elves):
    y_range = tuple(pt[0] for pt in elves)
    x_range = tuple(pt[1] for pt in elves)
    min_y, max_y, min_x, max_x = min(y_range), max(y_range), min(x_range), max(x_range)
    return min_y, max_y, min_x, max_x


def print_elves(elves):
    min_y, max_y, min_x, max_x = get_elves_bounds(elves)
    modified_elves = set((y - min_y, x - min_x) for y, x in elves)
    grid = [['.' for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]
    for y, x in modified_elves:
        grid[y][x] = '#'
    for row in grid:
        for pt in row:
            print(pt, end='')
        print()


def get_empty_pts(elves):
    min_y, max_y, min_x, max_x = get_elves_bounds(elves)
    empty_pts_count = (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)
    return empty_pts_count


def simulate_round(elves, directions):
    new_positions = set()
    new2old = dict()
    for elf in elves:
        if check_empty_surroundings(elf, elves):
            # No elves beside this elf, don't need to move
            new_positions.add(elf)
            continue
        new_pt = propose_move(elf, directions, elves)
        if new_pt in new_positions:
            # Clash in proposed positions
            new_positions.remove(new_pt)
            new_positions.add(elf)
            new_positions.add(new2old[new_pt])
        else:
            new_positions.add(new_pt)
            new2old[new_pt] = elf
    return new_positions


def part1(file):
    elves = read_input(file)
    direction_generator = DirectionGenerator()
    rounds = 10
    for i in range(rounds):
        directions = direction_generator.get_directions()
        elves = simulate_round(elves, directions)
    empty_pts_count = get_empty_pts(elves)
    print(f"Part 1: {empty_pts_count}")


def part2(file):
    elves = read_input(file)
    direction_generator = DirectionGenerator()
    count = 1
    while True:
        directions = direction_generator.get_directions()
        new_elves = simulate_round(elves, directions)
        if new_elves == elves:
            print(f"Part 2: {count}")
            return
        else:
            elves = new_elves
            count += 1


input_file = "input.in"
part1(input_file)
part2(input_file)
