from copy import deepcopy


def read_input():
    scanners = []
    scanner = set()
    with open("input.in", "r") as file:
        for line in file:
            if line == "\n":
                continue
            elif line.startswith("---"):
                if scanner:
                    scanners.append(scanner)
                scanner = set()
            else:
                beacon_coordinate = tuple([int(coordinate) for coordinate in line.strip().split(',')])
                scanner.add(beacon_coordinate)
        scanners.append(scanner)
    return scanners


# Rotate coordinates about specified axis
def rotate_90(direction, scanner):
    rotation = set()
    if direction == "x":
        rotation = set([(point[0], point[2], -point[1]) for point in scanner])
    elif direction == "y":
        rotation = set([(point[2], point[1], -point[0]) for point in scanner])
    elif direction == "z":
        rotation = set([(point[1], -point[0], point[2]) for point in scanner])
    return rotation


# Rotate about 1 axis to get 4 different coordinate frames
def get_rotations(direction, scanner):
    rotation = deepcopy(scanner)
    rotations = [rotation]
    for i in range(3):
        rotation = rotate_90(direction, rotation)
        rotations.append(rotation)
    return rotations


# Get +x, -x, +y, -y, +z, -z coordinate frames
def get_directions(scanner):
    directions = [deepcopy(scanner), rotate_90("y", scanner)]
    direction = directions[1]
    for i in range(3):
        direction = rotate_90("z", direction)
        directions.append(direction)
    directions.append(rotate_90("y", directions[1]))
    return directions


# For each of the 6 possible axis, rotate about each one to get 4 * 6 possible coordinate frames
def get_all_orientations(scanner):
    orientations = []
    directions = get_directions(scanner)
    for direction in directions:
        orientations += get_rotations("x", direction)
    return orientations


# Get offset between every beacon of 2 scanners and check if at least 12 beacons match
def align_beacons(beacons0, beacons1):
    for beacon0 in beacons0:
        for beacon1 in beacons1:
            offset = (beacon0[0] - beacon1[0], beacon0[1] - beacon1[1], beacon0[2] - beacon1[2])
            count = 1
            for ref_beacon in beacons1:
                offset_beacon = tuple(map(lambda i, j: i + j, offset, ref_beacon))
                if offset_beacon in beacons0:
                    count += 1
            if count >= 12:
                return offset
    return None


def combine_scanners(scanner0, scanner1, offset):
    for beacon in scanner1:
        offset_beacon = tuple(map(lambda i, j: i + j, offset, beacon))
        scanner0.add(offset_beacon)


def match(scanner0, scanner1, scanner_coordinates):
    orientations = get_all_orientations(scanner1)
    for orientation in orientations:
        offset = align_beacons(scanner0, orientation)
        if offset is not None:
            scanner_coordinates.append(offset)
            combine_scanners(scanner0, orientation, offset)
            return True
    return False


def get_max_manhattan(scanner_coordinates):
    max_dist = -1
    for i in range(len(scanner_coordinates)):
        for j in range(len(scanner_coordinates)):
            s0 = scanner_coordinates[i]
            s1 = scanner_coordinates[j]
            dist = abs(s0[0] - s1[0]) + abs(s0[1] - s1[1]) + abs(s0[2] - s1[2])
            if dist > max_dist:
                max_dist = dist
    return max_dist


def combine_all(scanners):
    ref_scanner = scanners[0]
    relative_scanners = scanners[1:]
    scanner_coordinates = [(0, 0, 0)]
    while len(relative_scanners) != 0:
        is_removed = False
        for i in range(len(relative_scanners)):
            scanner = relative_scanners[i]
            if match(ref_scanner, scanner, scanner_coordinates):
                # Remove scanner from relative_scanners
                is_removed = True
                break
        if is_removed:
            del relative_scanners[i]
    return ref_scanner, scanner_coordinates


def part1():
    scanners = read_input()
    ref_scanner, _ = combine_all(scanners)
    print(f"Part 1: {len(ref_scanner)}")


def part2():
    scanners = read_input()
    _, scanner_coordinates = combine_all(scanners)
    max_dist = get_max_manhattan(scanner_coordinates)
    print(f"Part 2: {max_dist}")


if __name__ == "__main__":
    part1()
    part2()
