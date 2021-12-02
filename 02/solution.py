import sys


def get_distance_part_2(com_l):
    aim = 0
    depth = 0
    pos = 0
    for com, d in com_l:
        if com == "up":
            aim -= int(d)
        elif com == "down":
            aim += int(d)
        elif com == "forward":
            pos += int(d)
            depth += aim*int(d)
    return depth*pos


def get_distance(com_l):
    pos = 0
    depth = 0
    for com, d in com_l:
        if com == "up":
            depth -= int(d)
        elif com == "down":
            depth += int(d)
        elif com == "forward":
            pos += int(d)
    return depth * pos


def read_as_tuple(f_name):
    with open(f_name, 'r') as f:
        out = [tuple(j.split()) for j in f.readlines()]
    return out


def main(f_name):
    out = read_as_tuple(f_name)
    print(f"total distance: {get_distance(out)}")
    print(f"total distance new: {get_distance_part_2(out)}")


if __name__ == "__main__":
    main(sys.argv[1])
