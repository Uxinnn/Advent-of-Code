def part1():
    max_calories = -1
    with open("input.in", "r") as f:
        calories = [line.strip() for line in f.readlines()]
    elf_calories = 0
    for calorie in calories:
        if calorie != "":
            elf_calories += int(calorie)
        else:
            max_calories = max(max_calories, elf_calories)
            elf_calories = 0
    print(f"Part 1: {max_calories}")


def part2():
    elf_calories = []
    with open("input.in", "r") as f:
        calories = [line.strip() for line in f.readlines()]
    elf_calorie = 0
    for calorie in calories:
        if calorie != "":
            elf_calorie += int(calorie)
        else:
            elf_calories.append(elf_calorie)
            elf_calorie = 0
    elf_calories.sort(reverse=True)
    print(f"Part 2: {sum(elf_calories[:3])}")


part1()
part2()
