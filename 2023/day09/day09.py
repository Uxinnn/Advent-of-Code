def read_input(file):
    with open(file, 'r') as f:
        for line in f:
            history = list(map(int, line.strip().split()))
            yield history


def predict(history):
    """
    Note down the first and last values for each common difference iteration
    since only these values are needed to predict the previous and next value,
    respectively.
    To find first value fv = f1 + f2 + ... + fn
    To find previous value pv = p1 - p2 + p3 - ... +/- pn
      (Alternate between + and -)
    """
    last_vals = [history[-1]]
    first_vals = [history[0]]
    # Iterate common differences until all 0 is reached.
    while any(history):
        new_history = list()
        for i in range(1, len(history)):
            new_history.append(history[i] - history[i - 1])
        history = new_history
        last_vals.append(history[-1])
        first_vals.append(history[0])
    # Find next value
    next_val = sum(last_vals)
    # Find previous value
    prev_val = 0
    for i, v in enumerate(first_vals):
        prev_val += (-1) ** i * v
    return prev_val, next_val


def part1(file):
    histories = read_input(file)
    res = 0
    for history in histories:
        _, next_val = predict(history)
        res += next_val
    print(f"Part 1: {res}")


def part2(file):
    histories = read_input(file)
    res = 0
    for history in histories:
        prev_val, _ = predict(history)
        res += prev_val
    print(f"Part 2: {res}")


file = "input.in"
part1(file)
part2(file)
