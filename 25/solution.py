import sys
import time


def read_file(f_name):
    out_d, out_r = [], []
    gen = (i.strip() for i in open(f_name).readlines())
    nx = 0
    for i, line in enumerate(gen):
        nx += 1
        ny = len(line)
        out_d.extend([(i, j) for j, e in enumerate(line) if e == 'v'])
        out_r.extend([(i, j) for j, e in enumerate(line) if e == '>'])

    out_d = set(out_d)
    out_r = set(out_r)
    return (out_r, out_d), (nx, ny)


def run_cucumbers(sets, n):
    i = 0
    idxs = [1, 0]
    while True:
        i += 1
        total = sets[0] | sets[1]
        temp_sets = [sets[0], sets[1]]
        for j, (s, idx) in enumerate(zip(sets, idxs)):
            state = temp_sets[0] | temp_sets[1]
            new_set = []
            for item in s:
                trial = tuple(((x + 1) % n[idx] if k == idx else x
                               for k, x in enumerate(item)))
                if trial in state:
                    new_set.append(item)
                else:
                    new_set.append(trial)
            new_set = set(new_set)
            temp_sets[j] = new_set
        sets = temp_sets
        if total == temp_sets[0] | temp_sets[1]:
            print(i)
            return


def plot_state(r_set, d_set, n):
    lines = []
    for temp1 in range(n[0]):
        temp_line = ""
        for temp2 in range(n[1]):
            if (temp1, temp2) in r_set:
                temp_line += ">"
            elif (temp1, temp2) in d_set:
                temp_line += "v"
            else:
                temp_line += '.'
        lines.append(temp_line)
    print("\n".join(lines))


def main(f_name):
    s = time.time()
    out, n = read_file(f_name)
    run_cucumbers(out, n)
    print(f"total time: {time.time()-s}")


if __name__ == "__main__":
    main(sys.argv[1])
