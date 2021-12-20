import sys
import numpy as np
import time


def read_file(f_name):
    out = []
    with open(f_name, 'r') as f:
        lines = (i.strip() for i in f.readlines())
        enhancement = [1 if i == '#' else 0 for i in next(lines)]
        enhancement = {i: e for i, e in enumerate(enhancement)}
        _ = next(lines)  # empty line
        for line in lines:
            out.append([1 if i == '#' else 0 for i in line])
    out = np.array(out)
    return out, enhancement


def apply_image_enhancement(inp, enhancement, n=0):
    temp = np.pad(inp, 2, "constant", constant_values=n)
    x_shape, y_shape = temp.shape
    out = np.zeros_like(temp)
    for x in range(1, x_shape-1):
        for y in range(1, y_shape-1):
            subarr = temp[x-1:x+2, y-1:y+2]
            out[x, y] = convolve(subarr, enhancement)
    return out[1:-1, 1:-1]


def convolve(inp, enhancement):
    temp = [i for i in inp.ravel()]
    key = bin_to_num(temp)
    return enhancement[key]


def bin_to_num(inp):
    return sum(2**i for i, e in enumerate(inp[::-1]) if e)


def count_lit(inp):
    return(np.sum(inp))


def main(f_name):
    s = time.time()
    out, enhancement = read_file(f_name)
    print(f"time reading file: {time.time()-s}")
    s = time.time()
    infinite_sea = 0
    for i in range(50):
        out = apply_image_enhancement(out, enhancement, infinite_sea)
        infinite_sea = convolve(np.array([infinite_sea for _ in range(9)]),
                                enhancement)
        if i == 1:
            print(count_lit(out))
            print(f"2 convolutions: {time.time()-s}")
    print(count_lit(out))
    print(f"50 convolutions: {time.time()-s}")

if __name__ == "__main__":
    main(sys.argv[1])
