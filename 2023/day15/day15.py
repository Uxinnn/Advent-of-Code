def read_input(file):
    with open(file, 'r') as f:
        steps = f.readline().strip().split(',')
        for step in steps:
            yield step


def compute_hash(step):
    curr_val = 0
    for c in step:
        curr_val += ord(c)
        curr_val *= 17
        curr_val %= 256
    return curr_val


def get_label(step):
    """
    Return the alpha part of the given step.
    """
    label = list()
    for i, c in enumerate(step):
        if not c.isalpha():
            break
        label.append(c)
    return i, "".join(label)


def add_lens(box, label, focal_length):
    for lens in box:
        if lens[0] == label:
            lens[1] = focal_length
            break
    else:
        box.append([label, focal_length])


def remove_lens(box, label):
    for lens in box:
        if lens[0] == label:
            box.remove(lens)
            return


def get_focusing_power(i, box):
    focusing_power = sum(
        [(i + 1) * (j + 1) * lens[1] for j, lens in enumerate(box)])
    return focusing_power


def part1(file):
    steps = read_input(file)
    hash_sum = sum([compute_hash(step) for step in steps])
    print(f"Part 1: {hash_sum}")


def part2(file):
    steps = read_input(file)
    boxes = [list() for _ in range(256)]
    for step in steps:
        i, label = get_label(step)
        box_id = compute_hash(label)
        op = step[i]
        if op == '=':
            focal_length = int(step[i + 1:])
            add_lens(boxes[box_id], label, focal_length)
        else:
            remove_lens(boxes[box_id], label)
    tot_focusing_power = sum(get_focusing_power(i, box)
                             for i, box in enumerate(boxes)
                             )
    print(f"Part 2: {tot_focusing_power}")


file = "input.in"
part1(file)
part2(file)
