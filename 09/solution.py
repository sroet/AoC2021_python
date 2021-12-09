import sys
import numpy as np


def read_file(f_name):
    with open(f_name, 'r') as f:
        out = []
        for line in f.readlines():
            out.append([int(i) for i in line.strip()])
    return np.array(out, dtype=int)


def find_low(arr):
    buffered = np.pad(arr, 1, constant_values=10)
    neighbors = (np.roll(buffered, 1, 0), np.roll(buffered, -1, 0),
                 np.roll(buffered, 1, 1), np.roll(buffered, -1, 1))
    a = set(coord_to_tuples(np.where(arr >= 0)))
    for n in neighbors:
        temp = arr - n[1:-1, 1:-1]
        a -= set(coord_to_tuples(np.where(temp >= 0)))
    return a


def count_part_one(arr, a):
    s = 0
    for x, y in a:
        s += arr[x, y]+1
    return s


def find_basins(arr, a):
    out = []
    buffered = np.pad(arr, 1, constant_values=10)
    for x, y in a:
        out.append(find_basin_size(buffered, x+1, y+1))
    out.sort()
    return (out[-1]*out[-2]*out[-3])


def find_basin_size(arr, x, y):
    known = set([(x, y)])
    next_starts = set([(x, y)])
    c = 0
    while len(next_starts) != 0:
        c += len(next_starts)
        temp = []
        for x, y in next_starts:
            for x1, y1 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if arr[x1, y1] < 9:
                    temp.append((x1, y1))
        next_starts = set(temp)-known
        known |= next_starts
    return c


def coord_to_tuples(where):
    out = []
    for x, y in zip(where[0], where[1]):
        out.append((x, y))
    return out


def main(f_name):
    out = read_file(f_name)
    minima = find_low(out)
    print(count_part_one(out, minima))
    print(find_basins(out, minima))


if __name__ == "__main__":
    main(sys.argv[1])
