def read_input():
    file = open('input.in', 'r')
    return [[int(digit) for digit in line.strip()] for line in file.readlines()]


def step(energy_level):
    can_flash = []
    flash_count = 0
    # increment by 1
    for i in range(len(energy_level)):
        for j in range(len(energy_level[0])):
            energy_level[i][j] += 1
            if energy_level[i][j] == 10:
                can_flash.append((i, j))
    while can_flash:
        x, y = can_flash.pop()
        energy_level[x][y] = 11
        flash_count += 1
        surrounding_coordinates = ((x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                                   (x, y - 1), (x, y), (x, y + 1),
                                   (x + 1, y - 1), (x + 1, y), (x + 1, y + 1))
        for x1, y1 in surrounding_coordinates:
            if x1 < 0 or x1 >= len(energy_level) or y1 < 0 or y1 >= len(energy_level[0]):
                continue
            if energy_level[x1][y1] >= 10:
                continue
            energy_level[x1][y1] += 1
            if energy_level[x1][y1] == 10:
                can_flash.append((x1, y1))
    # Reset flashed coordinates back to 0
    for i in range(len(energy_level)):
        for j in range(len(energy_level[0])):
            if energy_level[i][j] == 11:
                energy_level[i][j] = 0
    return flash_count


def n_step(energy_level, n):
    total_flash_count = 0
    for i in range(n):
        total_flash_count += step(energy_level)
    return total_flash_count


def get_synchronous_flash(energy_level):
    count = 0
    flash_count = 0
    while flash_count != len(energy_level) * len(energy_level[0]):
        flash_count = step(energy_level)
        count += 1
    return count


def part1():
    energy_level = read_input()
    total_flash_count = n_step(energy_level, 100)
    print(f"Part 1: {total_flash_count}")


def part2():
    energy_level = read_input()
    count = get_synchronous_flash(energy_level)
    print(f"Part 2: {count}")


if __name__ == "__main__":
    part1()
    part2()
