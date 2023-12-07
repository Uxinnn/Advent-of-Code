def read_input(file, part):
    with open(file, 'r') as f:
        # Process seeds
        seeds_line = f.readline().strip()
        seeds_str = seeds_line.split(': ', 1)[1].split()
        raw_seeds = [int(seed) for seed in seeds_str]
        # Cast initial seeds into ranges
        if part == 1:
            seed_intervals = [[seed, seed + 1] for seed in raw_seeds]
        elif part == 2:
            interval_starts = [raw_seeds[i]
                               for i in range(0, len(raw_seeds), 2)
                               ]
            interval_ends = [raw_seeds[i] + raw_seeds[i - 1]
                             for i in range(1, len(raw_seeds), 2)
                             ]
            seed_intervals = list(list(p)
                                  for p in zip(interval_starts, interval_ends)
                                  )
        f.readline()
        # Process stages
        # Each stage will have range mappings in the form ((range_start,
        # range_end), offset), where offset is used to convert from the old
        # interval to the new interval (new_seed = old_seed + offset).
        stages = list()
        for line in f:
            line = line.strip()
            if line.endswith("map:"):
                stage = list()
            elif not line:
                stages.append(stage)
            else:
                dst_start, src_start, interval = [int(num)
                                                  for num in line.split()
                                                  ]
                src_range = (src_start, src_start + interval)
                offset = dst_start - src_start
                stage.append((src_range, offset))
            # Important to make processing simpler in handle_seed_interval
            stage.sort()
        stages.append(stage)
        return seed_intervals, stages


def handle_stage(seed_intervals, stage):
    """
    Each stage involves mapping each seed_interval into new intervals based on
    the ranges given in the stage.
    """
    new_seed_intervals = list()
    for seed_interval in seed_intervals:
        handle_seed_interval(seed_interval, stage, new_seed_intervals)
    return new_seed_intervals


def handle_seed_interval(seed_interval, stage, new_seed_intervals):
    # Split each input seed_interval into new intervals
    has_remaining = True
    for (src_start, src_end), offset in stage:
        if seed_interval[0] < src_start:
            # If input interval starts before the given mapping range
            if seed_interval[1] <= src_start:
                new_seed_intervals.append(seed_interval)
                has_remaining = False
                break
            else:
                new_interval = [seed_interval[0], src_start]
                new_seed_intervals.append(new_interval)
                seed_interval[0] = src_start
        if seed_interval[0] < src_end:
            # If input interval starts after the given mapping range
            # and before the mapping range ends
            new_interval = [seed_interval[0] + offset,
                            min(seed_interval[1], src_end) + offset
                            ]
            new_seed_intervals.append(new_interval)
            if seed_interval[1] <= src_end:
                has_remaining = False
                break
            else:
                seed_interval[0] = src_end
    if has_remaining:
        # If there are any intervals beyond the largest mapping range
        new_seed_intervals.append(seed_interval)


def get_min_location(seed_intervals, stages):
    """
    Put intervals through all stages to get final intervals.
    Return the smallest final value (location).
    """
    for stage in stages:
        seed_intervals = handle_stage(seed_intervals, stage)
    min_loc = min(seed_intervals)[0]
    return min_loc


def part1(file):
    seed_intervals, stages = read_input(file, 1)
    min_loc = get_min_location(seed_intervals, stages)
    print(f"Part 1: {min_loc}")


def part2(file):
    seed_intervals, stages = read_input(file, 2)
    min_loc = get_min_location(seed_intervals, stages)
    print(f"Part 2: {min_loc}")


file = "input.in"
part1(file)
part2(file)
