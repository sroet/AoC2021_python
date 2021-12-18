import sys
numbers = {str(i) for i in range(10)}


def read_file(f_name):
    out = []
    with open(f_name, 'r') as f:
        lines = (i for i in f.readlines())
        for line in lines:
            out.append((line.strip()))
    return out


def sum_snailf(part1, part2):
    out = f"[{part1},{part2}]"
    return(reduce_snailf(out))


def reduce_snailf(out):
    out_list = [out]  # trick to force pass by reference
    reduced = False
    while not reduced:
        gen = ((i, e) for i, e in enumerate(out_list[0]))
        exploded = explode(out_list, gen)
        if exploded:
            continue
        gen = ((i, e) for i, e in enumerate(out_list[0]))
        splitted = split(out_list, gen)
        if not splitted:
            break
    return out_list[0]


def explode(out_list, gen):
    level = 0
    left_idx = None
    new_number = True
    for i, e in gen:
        if e in numbers and new_number:
            left_idx = i
            new_number = False
        elif e not in numbers:
            new_number = True
        if e == "[":
            level += 1
        elif e == "]":
            level -= 1

        if level == 5:
            # do explosion
            left_bracket = i
            left_num = ""
            for i, e in gen:
                if e not in numbers:
                    break
                left_num += e
            left_num = int(left_num)
            right_num = ""
            for i, e in gen:
                if e not in numbers:
                    break
                right_num += e
            right_bracket = i
            right_num = int(right_num)
            # Now replace right to left so indices make sense
            # find next number index
            for i, e in gen:
                if e in numbers:
                    add_to_num(out_list, i, right_num)
                    break

            # Replace the nested_list
            temp = (out_list[0][:left_bracket] +
                    str(0) +
                    out_list[0][right_bracket+1:])
            out_list[0] = temp

            if left_idx:
                add_to_num(out_list, left_idx, left_num)
            return True
    return False


def add_to_num(out_list, start_idx, add):
    out = ""
    for i, e in enumerate(out_list[0][start_idx:]):
        if e not in numbers:
            break
        out += e
    if len(out) == 0:
        return
    end_index = start_idx+i
    out = int(out)+add
    temp = out_list[0][:start_idx]+str(out)+out_list[0][end_index:]
    out_list[0] = temp


def split(out_list, gen):
    out = ""
    left_idx = None
    for i, e in gen:
        if e in numbers:
            if left_idx is None:
                left_idx = i
            out += e
        else:
            if len(out) > 0 and int(out) >= 10:
                temp = int(out)
                temp_split = str([temp//2, temp//2+int(temp % 2 != 0)])
                temp_split = "".join([i for i in temp_split if i != " "])
                out_list[0] = (out_list[0][:left_idx] +
                               temp_split +
                               out_list[0][i:])
                return True
            left_idx = None
            out = ""
    return False


def calc_magnitude(inp, gen=None):
    c = 0
    if gen is None:
        gen = (i for i in inp)
    left = ""
    for c in gen:
        if c == "[":
            left = calc_magnitude(inp, gen)
        elif c == ",":
            left = int(left)
            break
        else:
            left += c
    right = ""
    for c in gen:
        if c == "[":
            right = calc_magnitude(inp, gen)
        elif c == "]":
            right = int(right)
            break
        else:
            right += c
    if type(right) == str:  # outer loop
        return left

    return (3*left+2*right)


def main(f_name):
    out = read_file(f_name)
    o1 = out[0]
    for o2 in out[1:]:
        o1 = sum_snailf(o1, o2)
    print(f"reduced answer: {o1}")
    print(calc_magnitude(o1))
    # part 2
    max_mag = 0
    for i, e in enumerate(out):
        for j, f in enumerate(out):
            if i == j:
                continue
            temp = sum_snailf(e, f)
            mag = calc_magnitude(temp)
            if mag > max_mag:
                max_mag = mag
    print(max_mag)


if __name__ == "__main__":
    main(sys.argv[1])
