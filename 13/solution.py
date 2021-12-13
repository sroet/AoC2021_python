import sys


def read_file(f_name):
    out_set = set()
    with open(f_name, 'r') as f:
        lines = (i for i in f.readlines())
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                break
            out_set |= set([tuple(int(i) for i in line.split(','))])
        instructions = []
        for line in lines:
            temp = line.strip().split()[-1].split('=')
            instructions.append((temp[0], int(temp[1])))
    return out_set, instructions


def do_folds(coord_set, instructions):
    for i, e in enumerate(instructions):
        coord_set = do_fold(coord_set, e)
        if i == 0:
            print(len(coord_set))
    print_code(coord_set)


def do_fold(coord_set, instruction):
    if instruction[0] == 'x':
        fold_idx = 0
    else:
        fold_idx = 1
    fold_line = instruction[1]

    gen = (tuple(e if j != fold_idx else new_coord(e, fold_line)
           for j, e in enumerate(i))
           for i in coord_set)
    return set(gen)


def print_code(coord_set):
    max_x = max(i[0] for i in coord_set)
    max_y = max(i[1] for i in coord_set)
    out = ""
    for line in range(0, max_y+1):
        out += "".join(["#" if (i, line) in coord_set else " "
                        for i in range(max_x+1)])
        out += "\n"
    print(out)


def new_coord(x, fold_x):
    if x < fold_x:
        return x
    else:
        return fold_x-(x-fold_x)


def main(f_name):
    out, instructions = read_file(f_name)
    do_folds(out, instructions)


if __name__ == "__main__":
    main(sys.argv[1])
