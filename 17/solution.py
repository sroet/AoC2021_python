import sys


def read_file(f_name):
    out = []
    with open(f_name, 'r') as f:
        lines = (i for i in f.readlines())
        for line in lines:
            temp = line.strip().split()
            temp_x = temp[2].split("..")
            x_min = int(temp_x[0][2:])  # split off 'x='
            x_max = int(temp_x[1][:-1])  # split off ','
            temp_y = temp[3].split("..")
            y_min = int(temp_y[0][2:])  # split of 'y='
            y_max = int(temp_y[1][:])

            out.append(((x_min, x_max), (y_min, y_max)))

    return out


def part_1(target):
    # Here we use the trick that velocity comming down == vel going up
    x_target, y_target = target
    max_y_vel = -1*(min(y_target)+1)
    max_y_dist = sum(max_y_vel-i for i in range(max_y_vel))
    print(max_y_dist)


def part_2(target):
    x_target, y_target = target
    max_x_vel = max(x_target)
    max_y_vel = -1*(min(y_target)+1)
    min_y_vel = min(y_target)
    xs = [j for j in range(1, max_x_vel+1)]
    ys = [i for i in range(min_y_vel, max_y_vel+1)]
    out = sum(1 for x in xs for y in ys if hits_target((x, y), target))
    print(out)


def hits_target(speed, target):
    coord = [0, 0]
    x_target, y_target = target
    x_speed, y_speed = speed
    while True:
        if (min(x_target) <= coord[0] <= max(x_target) and
            min(y_target) <= coord[1] <= max(y_target)):
            return True
        elif coord[0] > max(x_target) or coord[1] < min(y_target):
            return False
        else:
            coord[0] += x_speed
            coord[1] += y_speed
            x_speed = max([x_speed-1, 0])
            y_speed -= 1


def main(f_name):
    out = read_file(f_name)
    for o in out:
        part_1(o)
        part_2(o)


if __name__ == "__main__":
    main(sys.argv[1])
