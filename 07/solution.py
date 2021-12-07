import sys
import numpy as np


def read_file(f_name):
    with open(f_name, 'r') as f:
        out = []
        for line in f.readlines():
            out.append([int(i) for i in line.split(',')])
    return np.array(out, dtype=int)


def find_cost_line(inp):
    b = 0
    fuel_cost = {i: (b := b+i) for i in range(0, np.max(inp)+1)}
    best = 0
    last_temp = np.inf
    best_cost = np.inf
    for i in range(0, np.max(inp)):
        temp = sum(fuel_cost[j] for j in np.abs(inp-i).ravel())
        if temp < best_cost:
            best = i
            best_cost = temp
        if temp > last_temp:
            return best, best_cost
        last_temp = temp


def main(f_name):
    out = read_file(f_name)
    print(find_cost_line(out))


if __name__ == "__main__":
    main(sys.argv[1])
