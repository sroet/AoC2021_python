import sys
import numpy as np


def read_file(f_name):
    with open(f_name, 'r') as f:
        out = []
        for line in f.readlines():
            out.append([int(j) for j in line.strip()])
    return np.array(out)


def do_steps(arr, n):
    c = 0
    for i in range(n):
        f, arr = do_step(arr)
        c += f
    return c


def find_flash(arr):
    i = 1
    while True:
        i += 1
        f, arr = do_step(arr)
        if f == arr.shape[0]*arr.shape[1]:
            return i


def do_step(arr):
    f = 0
    # Step 1
    arr += 1
    buffered = np.pad(arr, 1, 'constant')
    # Step 2
    flashed = set()
    while np.any(buffered > 9):
        where = np.where(buffered > 9)
        coord = set(coord_to_tuples(where)) - flashed
        for x, y in coord:
            f += 1
            buffered[x-1:x+2, y-1:y+2] += 1
        flashed |= coord
        # reset buffers
        buffered[0, :] = 0
        buffered[-1, :] = 0
        buffered[:, 0] = 0
        buffered[:, -1] = 0
        # Reset flashed
        xs, ys = tuples_to_coord(flashed)
        buffered[xs, ys] = 0
    return f, buffered[1:-1, 1:-1]


def tuples_to_coord(tuples):
    xs = []
    ys = []
    for x, y in tuples:
        xs.append(x)
        ys.append(y)
    return xs, ys


def coord_to_tuples(where):
    out = []
    for x, y in zip(where[0], where[1]):
        out.append((x, y))
    return out


def main(f_name, n):
    out = read_file(f_name)
    print(do_steps(out, int(n)))
    print(find_flash(out))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
