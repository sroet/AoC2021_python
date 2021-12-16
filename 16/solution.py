import sys
import numpy as np

# Write binary map
hex_to_bin = {'0': '0000',
              '1': '0001',
              '2': '0010',
              '3': '0011',
              '4': '0100',
              '5': '0101',
              '6': '0110',
              '7': '0111',
              '8': '1000',
              '9': '1001',
              'A': '1010',
              'B': '1011',
              'C': '1100',
              'D': '1101',
              'E': '1110',
              'F': '1111',
              }


def read_file(f_name):
    out = []
    with open(f_name, 'r') as f:
        lines = (i for i in f.readlines())
        for line in lines:
            temp = line.strip()
            out.append(''.join([hex_to_bin[i] for i in temp]))
    return out


def read_packet(inp, ver=[0]):  # Leverage some sneaky python for part 1
    # generator, bits read
    if len(inp) != 2:
        ver[0] = 0  # Needed to reset between example inputs
        gen = [(i for i in inp), 0]
    else:
        gen = inp
    ver[0] += get_version(gen)
    # print(f"ver:{ver}")  # uncomment for part 1
    type_id = get_type_id(gen)
    if type_id == 4:
        return read_literal(gen)
    l_type_id = get_l_type_id(gen)
    length = get_length(gen, l_type_id)
    subpackets = read_subpackets(gen, l_type_id, length)
    f = type_id_to_f[type_id]
    return f(subpackets)


def read_subpackets(inp, l_type_id, length):
    if l_type_id:
        return [read_packet(inp) for _ in range(length)]
    out = []
    start_lenght = inp[1]
    while inp[1]-start_lenght < length:
        out.append(read_packet(inp))
    return out


def read_n_bits(inp, n=1):
    inp[1] += n
    out = "".join([next(inp[0]) for _ in range(n)])
    return out


def get_version(inp):
    bininp = read_n_bits(inp, n=3)
    return bin_to_int(bininp)


def get_type_id(inp):
    bininp = read_n_bits(inp, n=3)
    return bin_to_int(bininp)


def bin_to_int(bininp):
    return sum(2**int(i) for i, e in enumerate(bininp[::-1]) if e == '1')


def read_literal(inp):
    bins = ''
    while True:
        byte = read_n_bits(inp, 5)
        bins += byte[1:]
        if byte[0] == '0':
            break
    return bin_to_int(bins)


def get_l_type_id(gen):
    bins = read_n_bits(gen, 1)
    return int(bins)


def get_length(gen, l_type):
    if l_type:
        bins = read_n_bits(gen, 11)
    else:
        bins = read_n_bits(gen, 15)
    return bin_to_int(bins)


def gt(inp):
    return int(inp[0] > inp[1])


def lt(inp):
    return int(inp[0] < inp[1])


def eq(inp):
    return int(inp[0] == inp[1])


type_id_to_f = {0: np.sum,
                1: np.prod,
                2: min,
                3: max,
                5: gt,
                6: lt,
                7: eq,
                }


def main(f_name):
    out = read_file(f_name)
    for o in out:
        print(read_packet(o))


if __name__ == "__main__":
    main(sys.argv[1])
