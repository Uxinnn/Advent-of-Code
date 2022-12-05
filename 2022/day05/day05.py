from collections import defaultdict


def read_input():
    stacks = defaultdict(list)
    with open("input.in", "r") as f:
        line = f.readline()[:-1]  # Remove \n at the end of each line
        while line[1] != '1':  # Read only the crates
            for i in range(1, len(line) + 1, 4):  # Selectively read the crate values in each line
                if line[i] != " ":
                    stacks[(i - 1) / 4 + 1].append(line[i])
            line = f.readline()[:-1]
        for k in stacks:  # Reverse for easy pop and append later
            stacks[k].reverse()
        _ = f.readline()  # Discard useless line
        line = f.readline().strip()
        cmds = []
        while line:  # Read the commands
            raw = line.split()
            n, src, dst = int(raw[1]), int(raw[3]), int(raw[5])
            cmds.append((n, src, dst))
            line = f.readline().strip()
    return stacks, cmds


def part1():
    stacks, cmds = read_input()
    for n, src, dst in cmds:
        for _ in range(n):
            crate = stacks[src].pop()
            stacks[dst].append(crate)
    answer = "".join([stacks[i + 1][-1] for i in range(len(stacks))])
    print(f"Part 1: {answer}")


def part2():
    stacks, cmds = read_input()
    for n, src, dst in cmds:
        crates = stacks[src][-n:]
        stacks[src] = stacks[src][:-n]
        stacks[dst] += crates
    answer = "".join([stacks[i + 1][-1] for i in range(len(stacks))])
    print(f"Part 2: {answer}")


part1()
part2()
