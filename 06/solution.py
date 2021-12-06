import sys


def read_file(f_name):
    with open(f_name, 'r') as f:
        out = []
        for line in f.readlines():
            out.append([int(i) for i in line.split(',')])
    return out


def count_lantern_fish(inp, n=18):
    state = {i: 0 for i in range(9)}
    for i in inp:
        state[i] += 1
    for i in range(n):
        state = update_state(state)
    return sum(state.values())


def update_state(inp):
    state = {i: 0 for i in range(9)}
    for i, val in inp.items():
        if i > 0:
            state[i-1] += val
        else:
            state[6] += val
            state[8] += val
    return state


def main(f_name, n):
    out = read_file(f_name)
    print(count_lantern_fish(out[0], int(n)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
