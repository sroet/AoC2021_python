import sys
import numpy as np
import time


def read_file(f_name):
    out = []
    with open(f_name, 'r') as f:
        lines = (i for i in f.readlines())
        for line in lines:
            temp = line.strip()
            out.append([int(i) for i in temp])
    return np.array(out, dtype=int)


def repeat_array(inp):
    x_len, y_len = inp.shape
    out = np.zeros((x_len*5, y_len*5))
    out[0:x_len, 0:y_len] = inp
    temp = inp.copy()
    for i in range(1, 5):
        temp += 1
        temp[temp > 9] = 1
        out[x_len*i:x_len*(i+1), 0:y_len] = temp.copy()
    temp = out[:, 0:y_len].copy()
    for i in range(1, 5):
        temp += 1
        temp[temp > 9] = 1
        out[:, y_len*i:y_len*(i+1)] = temp.copy()
    return out


def do_dijkstra(out):
    weights = np.ones(out.shape)*np.inf
    visited = set()
    next_points = set()
    current_point = (0, 0)
    current_weight = 0
    while current_point != (out.shape[0]-1, out.shape[1]-1):
        visited |= set([current_point])
        xc, yc = current_point
        for x, y in [(xc-1, yc), (xc+1, yc), (xc, yc-1), (xc, yc+1)]:
            if x < 0 or y < 0 or x >= out.shape[0] or y >= out.shape[1]:
                continue
            next_points |= set([(x, y)])
            if current_weight + out[x, y] < weights[x, y]:
                weights[x, y] = current_weight + out[x, y]
        next_points -= visited
        next_pos = list(next_points)
        next_weights = weights[tuples_to_xys(next_pos)]
        idx = next_weights.argsort()[0]
        current_point = next_pos[idx]
        current_weight = next_weights[idx]
    print(current_weight)


def xys_to_tuples(xs, ys):
    return [(x, y) for x, y in zip(xs, ys)]


def tuples_to_xys(tuples):
    xs = []
    ys = []
    for x, y in tuples:
        xs.append(x)
        ys.append(y)
    return xs, ys


def main(f_name):
    s = time.time()
    out = read_file(f_name)
    do_dijkstra(out)
    print(f"time: {time.time()-s}")
    repeated = (repeat_array(out))
    s = time.time()
    do_dijkstra(repeated)
    print(f"time: {time.time()-s}")


if __name__ == "__main__":
    main(sys.argv[1])
