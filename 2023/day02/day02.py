def read_input(file):
    """
    Yield each game in the form [game_id, game_sets]
    where game_sets is [game_set1, game_set2, ...]
    where a game_set is {"red": int, "blue": int, "green": int}
    """
    with open(file, 'r') as f:
        for line in f:
            raw_line = line.strip()
            # Get game id
            for i in range(len(raw_line)):
                if raw_line[i] == ":":
                    game_id = raw_line[:i].split(" ")[1]
                    break
            raw_line = raw_line[i + 2:]
            game_sets = list()
            # Get game sets
            for game_set_str in raw_line.split(";"):
                cubes = game_set_str.split(",")
                cube_count = {"red": 0, "blue": 0, "green": 0}
                for cube in cubes:
                    cube = cube.strip()
                    count, cube_color = cube.split(" ")
                    cube_count[cube_color] += int(count)
                game_sets.append(cube_count)
            yield [game_id, game_sets]


def part1(file):
    max_cubes = {"red": 12, "blue": 14, "green": 13}
    games = read_input(file)
    res = 0
    for game_id, game_sets in games:
        is_possible = True
        for game_set in game_sets:
            for color in max_cubes:
                if max_cubes[color] < game_set[color]:
                    is_possible = False
                    break
            if not is_possible:
                break
        if is_possible:
            res += int(game_id)
    print(f"Part 1: {res}")


def part2(file):
    games = read_input(file)
    res = 0
    for game_id, game_sets in games:
        min_cubes = {"red": 0, "blue": 0, "green": 0}
        for game_set in game_sets:
            for color in min_cubes:
                min_cubes[color] = max(min_cubes[color], game_set[color])
        res += min_cubes["red"] * min_cubes["blue"] * min_cubes["green"]
    print(f"Part 2: {res}")


file = "input.in"
part1(file)
part2(file)
