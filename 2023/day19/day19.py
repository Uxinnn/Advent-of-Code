def read_input(file):
    with open(file, 'r') as f:
        workflows = dict()
        for line in f:
            line = line.strip()
            if not line:
                break
            name, steps = parse_workflow(line)
            workflows[name] = steps
        parts = list()
        for line in f:
            line = line.strip()
            part = parse_part(line)
            parts.append(part)
    return workflows, parts


def parse_workflow(line):
    name, line = line.split('{')
    line = line[:-1]  # Remove closing curly bracket
    steps = list()
    for cond in line.split(','):
        if ':' not in cond:
            step = cond
        else:
            category = cond[0]
            op = cond[1]
            val, true_branch = cond[2:].split(':')
            val = int(val)
            step = (category, op, val, true_branch)
        steps.append(step)
    return name, steps


def parse_part(line):
    line = line[1:-1]
    categories = line.split(',')
    part = dict()
    for category in categories:
        cat, val = category.split('=')
        val = int(val)
        part[cat] = val
    return part


def part1(file):
    workflows, parts = read_input(file)
    accepted_parts = list()
    for part in parts:
        workflow = 'in'
        while True:
            for step in workflows[workflow]:
                if isinstance(step, str):
                    # Reached the end of the workflow
                    next_workflow = step
                    break
                if (step[1] == '<' and part[step[0]] < step[2]) or (
                        step[1] == '>' and part[step[0]] > step[2]):
                    # This condition is satisfied, follow it to the next
                    # workflow.
                    next_workflow = step[3]
                    break
            # Check if the end is reached (Accepted or Rejected). Else repeat.
            if next_workflow == 'A':
                accepted_parts.append(part)
                break
            elif next_workflow == 'R':
                break
            else:
                workflow = next_workflow
    parts_sum = 0
    for part in accepted_parts:
        parts_sum += sum(part.values())
    print(f"Part 1: {parts_sum}")


def part2(file):
    workflows, _ = read_input(file)
    combinations_count = 0
    stack = [{'x': (1, 4000),
              'm': (1, 4000),
              'a': (1, 4000),
              's': (1, 4000),
              'workflow': "in",
              "idx": 0,
              }]
    while stack:
        part = stack.pop()
        if part["workflow"] == 'A':
            # This range is accepted. Multiply all xmas ranges together to get
            # total number of unique combinations.
            combinations_count += ((part['x'][1] - part['x'][0] + 1) *
                                   (part['m'][1] - part['m'][0] + 1) *
                                   (part['a'][1] - part['a'][0] + 1) *
                                   (part['s'][1] - part['s'][0] + 1)
                                   )
            continue
        elif part["workflow"] == 'R':
            # This range is rejected. Just ignore.
            continue
        workflow = workflows[part["workflow"]]
        step = workflow[part["idx"]]  # (category, op, val, true_branch)
        if isinstance(step, str):
            # Only occurs when the last condition of a workflow is reached.
            # Since the last condition of the workflow is the branch to go to
            # without any conditions.
            part["workflow"] = step
            part["idx"] = 0
            stack.append(part)
            continue
        cat = step[0]
        if (step[1] == '>' and part[cat][0] > step[2]) or (
                step[1] == '<' and part[cat][1] < step[2]):
            # Condition passed, proceed to true branch
            part["workflow"] = step[3]
            part["idx"] = 0
            stack.append(part)
        elif (step[1] == '>' and part[cat][1] <= step[2]) or (
                step[1] == '<' and part[cat][0] >= step[2]):
            # Condition failed, proceed to next condition
            part["idx"] += 1
            stack.append(part)
        else:
            # Part of the range satisfy the condition, the other part failed.
            # Split range into 2 separate parts that goes to different branches.
            if step[1] == '>':
                accepted_range = (step[2] + 1, part[cat][1])
                rejected_range = (part[cat][0], step[2])
            else:
                accepted_range = (part[cat][0], step[2] - 1)
                rejected_range = (step[2], part[cat][1])
            # Range that passed the condition moves on to the true branch.
            accepted_part = part.copy()
            accepted_part[cat] = accepted_range
            accepted_part["workflow"] = step[3]
            accepted_part["idx"] = 0
            stack.append(accepted_part)
            # Range that failed the condition moves on to the next condition in
            # the same workflow.
            rejected_part = part.copy()
            rejected_part[cat] = rejected_range
            rejected_part["idx"] += 1
            stack.append(rejected_part)
    print(f"Part 2: {combinations_count}")


file = "input.in"
part1(file)
part2(file)
