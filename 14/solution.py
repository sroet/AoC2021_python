import sys
from collections import Counter


def read_file(f_name):
    out = {}
    with open(f_name, 'r') as f:
        lines = (i for i in f.readlines())
        template = next(lines).strip()
        for line in lines:
            temp = line.strip()
            if len(temp) != 0:
                temp = [i.strip() for i in temp.split("->")]
                out[temp[0]] = temp[1]
    return template, out


def do_polymer_steps_naive(template, instructions, n):
    out = template
    for i in range(n):
        out = do_polymer_step_naive(out, instructions)
    return out


def do_polymer_step_naive(inp, instructions):
    out = ""
    for i, e in enumerate(inp[:-1]):
        j = inp[i+1]
        mid = instructions.get(e+j, "")
        out += e+mid
    return out+j


def do_polymer_steps(template, instructions, n):
    out = Counter()
    out.update(i+j for i, j in zip(template, template[1:]))
    for i in range(n):
        out = do_polymer_step(out, instructions)
    out.update([template[0], template[-1]])  # add extra to count all double
    return out


def do_polymer_step(template, instructions):
    out = Counter()
    for key, value in template.items():
        new = instructions.get(key, "")
        temp = key[0]+new+key[1]
        new_keys = [i+j for i, j in zip(temp, temp[1:])]
        out.update({k: value for k in new_keys})
    return out


def do_counting(counter):
    temp = Counter()
    for key, value in counter.items():
        for k in key:  # needed to not undercount doubles
            temp.update({k: value})
    out = Counter()
    for key, value in temp.items():
        out.update({key: value//2})
    return out


def main(f_name, n=4):
    template, instructions = read_file(f_name)
    polymer = do_polymer_steps(template, instructions, n)
    c = do_counting(polymer)
    sorted_list = c.most_common()
    print(sorted_list[0][1]-sorted_list[-1][1])


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
