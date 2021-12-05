import sys
import numpy as np


def read_file(f_name):
    with open(f_name, 'r') as f:
        out = []
        for line in f.readlines():
            temp = [int(j)
                    for i in line.split('->')
                    for j in i.split(',')]
            min_x, min_y, max_x, max_y = tuple(int(i) for i in temp)
            out.append((min_x, max_x, min_y, max_y))
    return out


def count_steam_lines(instructions):
    arr = np.zeros((1000, 1000))
    for x_min, x_max, y_min, y_max in instructions:
        if x_min == x_max or y_min == y_max:
            if x_min > x_max:
                x_min, x_max = x_max, x_min
            if y_min > y_max:
                y_min, y_max = y_max, y_min
            arr[x_min:x_max+1, y_min:y_max+1] += 1
        else:
            x_dir = 1 if x_min < x_max else -1
            y_dir = 1 if y_min < y_max else -1
            for x, y in zip(range(x_min, x_max+x_dir, x_dir),
                            range(y_min, y_max+y_dir, y_dir)):
                arr[x, y] += 1
    return np.count_nonzero(arr > 1)


def main(f_name):
    out = read_file(f_name)
    crosses = count_steam_lines(out)
    print(crosses)


if __name__ == "__main__":
    main(sys.argv[1])
