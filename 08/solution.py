import sys


def read_file(f_name):
    with open(f_name, 'r') as f:
        out = []
        for line in f.readlines():
            s_line = line.split('|')
            out.append(([s_line[0].split()], s_line[1].split()))
    return out


def is_zero(code, d):
    return len(code) == 6 and d['m'] not in code


def is_one(code, *args):
    return len(code) == 2


def is_two(code, d):
    return len(code) == 5 and d['tl'] not in code and d['br'] not in code


def is_three(code, d):
    return len(code) == 5 and d['tl'] not in code and d['bl'] not in code


def is_four(code, *args):
    return len(code) == 4


def is_five(code, d):
    return len(code) == 5 and d['bl'] not in code and d['tr'] not in code


def is_six(code, d):
    return len(code) == 6 and d['tr'] not in code


def is_seven(code, *args):
    return len(code) == 3


def is_eight(code, *args):
    return len(code) == 7


def is_nine(code, d):
    return len(code) == 6 and d['bl'] not in code


def count_numbers_part_1(out):
    sums = 0
    for posibilities, numbers in out:
        for num in numbers:
            sums += sum(int(f(num))
                        for f in [is_one, is_four, is_seven, is_eight]
                        )
    return sums


def get_bottom_mid(pos):
    a = 'abcdefg'
    b = [c for c in a if sum(c in p for p in pos) == 7]
    for p in pos:
        if is_four(p):
            m = [c for c in b if c in p][0]
            b = [c for c in b if c not in p][0]
    return b, m


def get_top_top_right(pos):
    a = 'abcdefg'
    b = [c for c in a if sum(c in p for p in pos) == 8]
    for p in pos:
        if is_seven(p):
            s = p
        elif is_one(p):
            o = p
    t = [c for c in b if (c in s and c not in o)][0]
    tr = [c for c in b if (c in s and c in o)][0]
    return t, tr


def get_top_left(pos):
    a = 'abcdefg'
    b = [c for c in a if sum(c in p for p in pos) == 6]
    return b[0]


def get_bottom_left(pos):
    a = 'abcdefg'
    b = [c for c in a if sum(c in p for p in pos) == 4]
    return b[0]


def get_bottom_right(pos):
    a = 'abcdefg'
    b = [c for c in a if sum(c in p for p in pos) == 9]
    return b[0]


def get_mapping(pos):
    pos = pos[0]
    d = {}
    b, m = get_bottom_mid(pos)
    d['b'] = b
    d['m'] = m
    d['tl'] = get_top_left(pos)
    d['bl'] = get_bottom_left(pos)
    d['br'] = get_bottom_right(pos)
    t, tr = get_top_top_right(pos)
    d['t'] = t
    d['tr'] = tr
    return d


def get_number(numbers, mapping):
    out = ''
    temp = [
        (is_zero, '0'),
        (is_one, '1'),
        (is_two, '2'),
        (is_three, '3'),
        (is_four, '4'),
        (is_five, '5'),
        (is_six, '6'),
        (is_seven, '7'),
        (is_eight, '8'),
        (is_nine, '9'),
            ]
    for num in numbers:
        out += [f[1] for f in temp if f[0](num, mapping)][0]
    return int(out)


def count_numbers_part_2(out):
    sums = 0
    for posibilities, numbers in out:
        mapping = get_mapping(posibilities)
        sums += get_number(numbers, mapping)
    return sums


def main(f_name):
    out = read_file(f_name)
    print(count_numbers_part_1(out))
    print(count_numbers_part_2(out))


if __name__ == "__main__":
    main(sys.argv[1])
