import sys
import numpy as np


def read_file(f_name):
    out = []
    with open(f_name, 'r') as f:
        lines = (i.strip() for i in f.readlines())
        _ = next(lines)
        temp = []
        for line in lines:
            if line.startswith("--"):
                out.append(np.array(temp))
                temp = []
            elif len(line) != 0:
                temp.append(tuple([int(i.strip()) for i in line.split(",")]))
        if len(temp) != 0:
            out.append(np.array(temp))
    return out


def make_distance(matrix):
    out = []
    for scanner in matrix:
        temp = [sum((i-j)**2 for i, j in zip(b1, b2))
                for b1 in scanner for b2 in scanner]
        temp = np.array(temp)
        out.append(temp.reshape((len(scanner), len(scanner))))
    return out


def count_overlaps(matrix, n=3):
    out = {}
    for i, scanner1 in enumerate(matrix):
        for j, scanner2 in enumerate(matrix):
            c = 0
            temp = []
            if i >= j:
                continue
            for k, b1 in enumerate(scanner1):
                for l, b2 in enumerate(scanner2):
                    if len(set(b1) & set(b2)) >= n:
                        c += 1
                        temp.append((k, l))
            if len(temp) != 0:
                out[(i, j)] = temp

    return out


def allign_beacons(matrix, overlaps):
    out = {}
    out[0] = matrix[0]
    to_allign = set([i for i in range(len(matrix))])-set([0])
    alligned = set([0])
    while len(to_allign) != 0:
        for (i, j), values in overlaps.items():
            print(f"alligning {i} and {j}")
            if i in alligned and j in alligned:
                continue  # already aligned
            if i in to_allign and j in to_allign:
                continue  # not yet allignable
            if i in alligned:
                base_grid = out.get(i, matrix[i])
                other_grid = matrix[j]
                reverse = False
            else:
                base_grid = out[j]
                other_grid = matrix[i]
                reverse = True
            needed_overlaps = values[:4]
            if reverse:
                needed_overlaps = [(i[-1], i[0]) for i in needed_overlaps]
            other_grid = translate(base_grid, other_grid, needed_overlaps[0])
            other_grid = rotate(base_grid, other_grid, needed_overlaps)
            if reverse:
                out[i] = other_grid
            else:
                out[j] = other_grid

            alligned = set(out)
            to_allign -= alligned
    return out


def translate(base_grid, other_grid, overlap_point):
    a = base_grid[overlap_point[0]]
    b = other_grid[overlap_point[1]]
    diff = a-b
    temp = other_grid + diff
    return temp


def rotate(base_grid, other_grid, overlap_points):
    a = base_grid[overlap_points[0][0]]
    b = other_grid[overlap_points[0][1]]
    base_points = base_grid[[i[0] for i in overlap_points[1:]]]
    other_points = other_grid[[i[1] for i in overlap_points[1:]]]
    # figure out the axis first
    xyz = [0 for _ in base_points.T]
    dirs = [1 for _ in base_points.T]
    for idx1, e in enumerate((base_points-a).T):  # find overlapping axes
        for idx2, f in enumerate((other_points-b).T):
            if set(e) == set(f):
                xyz[idx1] = idx2
            elif set(e) == set(-f):
                xyz[idx1] = idx2
                dirs[idx1] = -1
    # swap axes

    temp = (other_grid-b)[:, xyz].copy()

    # invert if neccessary
    for i, direction in enumerate(dirs):
        temp[:, i] *= direction
    other_grid = temp + a
    return other_grid


def count_beacons(alligned):
    temp = set([tuple(i) for sensor in alligned.values() for i in sensor])
    return len(temp)


def find_biggest_distance(alligned):
    biggest = 0
    for i in alligned.values():
        for j in alligned.values():
            temp = sum(np.abs(j[-1]-i[-1]))
            if temp > biggest:
                biggest = temp
    print(biggest)


def add_origins(inp):
    out = []
    for i in inp:
        temp = np.vstack([i, np.array([[0, 0, 0]])])
        out.append(temp)
    return out


def main(f_name, n=12):
    out = read_file(f_name)
    dist = make_distance(out)
    overlaps = count_overlaps(dist, int(n))

    alligned = allign_beacons(out, overlaps)
    print(count_beacons(alligned))

    # Add 0,0 points for part 2 and repeat alignement
    out = add_origins(out)

    alligned = allign_beacons(out, overlaps)
    find_biggest_distance(alligned)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
