def read_input():
    with open("input.in", 'r') as f:
        datastream = f.readline().strip()
    return datastream


def get_unique_substr_index(datastream, k):
    """
    Return the first index in which a sliding window has of length k are all unique values.
    :param datastream: input datastream
    :param k: length of sliding window
    :return: first index i in which values of index (i-k+1) to k are all unique.
    """
    window = ""
    for i, c in enumerate(datastream):
        if len(window) == k and len(set(window)) == k:
            return i
        else:
            if len(window) == k:
                window = window[1:]
            window += c


def part1():
    datastream = read_input()
    idx = get_unique_substr_index(datastream, 4)
    print(f"Part 1: {idx}")


def part2():
    datastream = read_input()
    idx = get_unique_substr_index(datastream, 14)
    print(f"Part 2: {idx}")


part1()
part2()
