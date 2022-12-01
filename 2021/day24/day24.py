"""
For each `inp w`, commands are very similar to each other. Only 3 commands are different (index 4, 5, 15).
Each block starting with `inp w` can thus be modelled as a function. The function is shown below. A, B, C
are values in index 4, 5, and 15 respectively. w, x, y, z are the registers.
* Everytime A == 1: w condition is true since B is always > 9

x = w != (z % 26 + B)
if A == 26:
    z = z // 26
    if x:
        x = 1
        y = w + C
        z = z * 26 + w + C  # Incremented
    else:
        x = 0
        y = 0
        z = z
else:
    x = 1
    y = w + C
    z = z * 26 + w + C  # Incremented

The algorithm acts like a stack, can see it below in the written blocks. There are 7 blocks with
A == 1 and 7 blocks with A == 26. When A == 1, values are pushed to stack. When A == 26, top value
is popped from the stack. If the w condition is false, then the block's value is pushed to the stack.
To get an output of 0, there should thus be 7 push and 7 pops. Thus the w conditions must all be true
to ensure there are 7 pushes only. This generates 7 conditions between the model value numbers and
the max and min of the model number can be derived from there.

Writing out the blocks will look something like this:
0: z = w0 + 6
1: z = (w0 + 6) * 26 + w1 + 6
2: z = (w0 + 6) * 26^2 + (w1 + 6) * 26 + (w2 + 3)
3: z = (w0 + 6) * 26 + (w1 + 6)    OR    (w0 + 6) * 26^2 + (w1 + 6) * 26 + (w3 + 11)
  MUST POP ONLY!!
  w3 == (w2 + 3) - 11 --> MUST BE TRUE
4: z = (w0 + 6) * 26^2 + (w1 + 6) * 26 + (w4 + 9)
5: z = (w0 + 6) * 26 + (w1 + 6)
  w5 == (w4 + 9) - 1
6: z = (w0 + 6) * 26^2 + (w1 + 6) * 26 + (w6 + 13)
7: z = (w0 + 6) * 26^3 + (w1 + 6) * 26^2 + (w6 + 13) * 26 + (w7 + 6)
8: z = (w0 + 6) * 26^2 + (w1 + 6) * 26 + (w6 + 13)
  w8 == (w7 + 6)
9: z = (w0 + 6) * 26^3 + (w1 + 6) * 26^2 + (w6 + 13) * 26 + (w9 + 10)
10: z = (w0 + 6) * 26^2 + (w1 + 6) * 26^1 + (w6 + 13)
  w10 == (w9 + 10) - 5
11: z = (w0 + 6) * 26 + (w1 + 6)
  w11 = (w6 + 13) - 16
12: z = (w0 + 6)
  w12 = (w1 + 6) - 7
13: z = 0
  w13 = (w0 + 6) - 11
"""


def read_input():
    with open("input.in", "r") as file:
        return [tuple(line.strip().split()) for line in file.readlines()]


def process_input(raw_input):
    specials = []
    for i in range(len(raw_input) // 18):
        special = int(raw_input[4 + 18 * i][2]), int(raw_input[5 + 18 * i][2]), int(raw_input[15 + 18 * i][2])
        specials.append(special)
    return specials


def get_conditions(specials):
    stack = []
    conds = []
    for i in range(len(specials)):
        special = specials[i]
        if special[0] == 1:
            # Push to stack
            stack.append((i, special[2]))
        else:
            # Pop from stack
            head = stack.pop()
            conds.append((i, head[0], head[1], special[1]))
    return conds


def print_conditions(conds):
    for cond in conds:
        print(f"w{cond[0]} == (w{cond[1]} + {cond[2]}) + {cond[3]}")


def get_max_model(conds):
    model = [None] * 14
    for cond in conds:
        factor = cond[2] + cond[3]
        model[cond[0]] = 9 + factor if factor < 0 else 9
        model[cond[1]] = 9 - factor if factor >= 0 else 9
    return int("".join(map(str, model)))


def get_min_model(conds):
    model = [None] * 14
    for cond in conds:
        factor = cond[2] + cond[3]
        model[cond[0]] = 1 if factor < 0 else 1 + factor
        model[cond[1]] = 1 if factor >= 0 else 1 - factor
    return int("".join(map(str, model)))


def part1():
    specials = process_input(read_input())
    conds = get_conditions(specials)
    max_model = get_max_model(conds)
    print(f"Part 1: {max_model}")


def part2():
    specials = process_input(read_input())
    conds = get_conditions(specials)
    min_model = get_min_model(conds)
    print(f"Part 2: {min_model}")


if __name__ == "__main__":
    part1()
    part2()
