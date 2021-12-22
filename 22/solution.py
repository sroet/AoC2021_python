import sys
import numpy as np
import time


def read_file(f_name):
    out = []
    with open(f_name, 'r') as f:
        lines = (i.strip() for i in f.readlines())
        for line in lines:
            temp = []
            split = line.replace(',', ' ').split()
            temp.append(1 if split[0] == 'on' else 0)  # on or off
            for x in split[1:]:
                xs = x.split("..")
                temp.append([int(xs[0][2:]), int(xs[1])+1])
            out.append(temp)
    return out


def reboot_part1(steps):
    arr = np.zeros((101, 101, 101))
    offset = 50
    limits = (-50 + offset, 50+1+offset)
    for i, xs, ys, zs in steps:
        xs = [clip(x+offset, limits) for x in xs]
        ys = [clip(x+offset, limits) for x in ys]
        zs = [clip(x+offset, limits) for x in zs]
        arr[xs[0]:xs[1], ys[0]:ys[1], zs[0]:zs[1]] = i
    print(np.count_nonzero(arr))


def reboot_part2(steps):
    ons = []
    for i, xs, ys, zs in steps:
        if i:  # turn on
            temp = [[xs, ys, zs]]
            for x, y, z in ons:
                temp = turn_off(temp, x, y, z)
            ons.extend(temp)
        else:
            ons = turn_off(ons, xs, ys, zs)
    print(count_on(ons))


def count_on(ons):
    c = 0
    for xs, ys, zs in ons:
        temp = np.prod([i[1]-i[0] for i in [xs, ys, zs]])
        c += temp
    return c


def turn_off(ons, xs, ys, zs):
    out = []
    for xos, yos, zos in ons:
        xis = [clip(x, xos) for x in xs]
        yis = [clip(y, yos) for y in ys]
        zis = [clip(z, zos) for z in zs]
        if xis[0] == xis[1] or yis[0] == yis[1] or zis[0] == zis[1]:
            # Not overlapping in at least 1 dim
            out.append([xos, yos, zos])
            continue
        if xis == xos and yis == yos and zis == zos:
            # fully overlapping
            continue
        # Deal with x
        xos = xos.copy()
        if xis[0] > xos[0]:
            out.append([[xos[0], xis[0]], yos, zos])
            xos[0] = xis[0]
        if xis[1] < xos[1]:
            out.append([[xis[1], xos[1]], yos, zos])
            xos[1] = xis[1]

        # Deal with y
        yos = yos.copy()
        if yis[0] > yos[0]:
            out.append([xos, [yos[0], yis[0]], zos])
            yos[0] = yis[0]
        if yis[1] < yos[1]:
            out.append([xos, [yis[1], yos[1]], zos])
            yos[1] = yis[1]

        # Deal with z
        zos = zos.copy()
        if zis[0] > zos[0]:
            out.append([xos, yos, [zos[0], zis[0]]])
            zos[0] = zis[0]
        if zis[1] < zos[1]:
            out.append([xos, yos, [zis[1], zos[1]]])
            zos[1] = zis[1]
    return out


def clip(inp, limits):
    if inp < limits[0]:
        return limits[0]
    elif inp > limits[1]:
        return limits[1]
    else:
        return inp


def main(f_name):
    s = time.time()
    out = read_file(f_name)
    print(f"time file read: {time.time()-s}")
    s1 = time.time()
    reboot_part1(out)
    print(f"time part 1: {time.time()-s1}")
    s1 = time.time()
    reboot_part2(out)
    print(f"time part 2: {time.time()-s1}")
    print(f"total time: {time.time()-s}")


if __name__ == "__main__":
    main(sys.argv[1])
