import sys
import time
from z3 import Int, Optimize, If
import re

reg = (
r"""inp w
mul x 0
add x z
mod x 26
div z (1|26)
add x (-?\d+)
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y (-?\d+)
mul y x
add z y"""
)


def read_file_fancy(f_name):
    string = "".join(open(f_name).readlines())
    a = []
    b = []
    c = []
    for ai, bi, ci in re.findall(reg, string):
        a.append(int(bi))
        b.append(int(ci))
        c.append(bool(ai == '26'))
    return a, b, c


def input_numbers():
    inps = [Int(f"inp{i}") for i in range(14)]
    constraints = [i < 10 for i in inps] + [i > 0 for i in inps]
    return inps, constraints


def fancy_func(z, a, b, c, d):
    x = (z % 26 + a)
    if c:
        z /= 26

    return If(x != d, 26 * z + d + b, z)


def run(instructions, part2=False):
    inputs, constraints = input_numbers()
    z = 0
    n = sum([10**i*e for i, e in enumerate(inputs)])
    for a, b, c, d in zip(*instructions, inputs):
        z = fancy_func(z, a, b, c, d)

    constraints += [z == 0]
    o = Optimize()
    for i in constraints:
        o.add(i)
    if part2:
        o.minimize(n)
    else:
        o.maximize(n)
    o.check()
    m = o.model()
    print(sum([m[e].as_long()*10**i for i, e in enumerate(inputs[::-1])]))


def main(f_name, trials=None):
    s = time.time()
    out = read_file_fancy(f_name)
    run(out, False)
    run(out, True)

    print(f"total time: {time.time()-s}")


if __name__ == "__main__":
    main(sys.argv[1])
