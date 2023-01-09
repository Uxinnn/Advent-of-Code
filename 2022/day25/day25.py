def read_input(file):
    with open(file, 'r') as f:
        return [snafu_num.strip() for snafu_num in f]


def snafu2dec(snafu_num):
    digit_map = {'2': 2,
                 '1': 1,
                 '0': 0,
                 '-': -1,
                 '=': -2,
                 }
    base = 5
    dec_num = sum([digit_map[snafu_num[len(snafu_num) - 1 - i]] * base ** i for i in range(len(snafu_num))])
    return dec_num


def dec2snafu(dec_num):
    # Convert decimal number to base 5
    base = 5
    base_num = list()
    if dec_num == 0:
        return [0]
    while dec_num:
        base_num.append(int(dec_num % base))
        dec_num //= base
    # Modify to contain - and = digits.
    digit_map = {3: '=', 4: '-', 5: 0}
    carry = 0
    for i, x in enumerate(base_num):
        x = x + carry
        carry = 0
        if 2 < x < 6:
            x = digit_map[x]
            carry = 1
        base_num[i] = str(x)
    if carry == 1:
        base_num.append('1')
    base_num = base_num[::-1]
    snafu_num = "".join(base_num)
    return snafu_num


def part1(file):
    snafu_nums = read_input(file)
    dec_num = sum(map(snafu2dec, snafu_nums))
    snafu_num = dec2snafu(dec_num)
    print(f"Part 1: {snafu_num}")


input_file = "input.in"
part1(input_file)
