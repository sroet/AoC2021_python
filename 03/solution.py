import sys
import numpy as np


def get_power(arr):
    n = len(arr)
    s = np.sum(arr, axis=0)
    gamma = ""
    epsilon = ""
    for i in s:
        if i > n//2:
            ans = ["1", "0"]
        else:
            ans = ["0", "1"]
        gamma += ans[0]
        epsilon += ans[1]
    gamma = convert_str_bin_to_int(gamma)
    epsilon = convert_str_bin_to_int(epsilon)
    print(gamma, epsilon)
    return gamma * epsilon


def get_ox_gen(arr, pos=0):
    if len(arr) == 1:
        return convert_str_bin_to_int(arr[0])
    else:
        com = get_most_common_bit(arr, pos=pos)
        idx = np.where(arr[:, pos] == com)[0]
        return get_ox_gen(arr[idx], pos=pos+1)


def get_co2_scrub(arr, pos=0):
    if len(arr) == 1:
        return convert_str_bin_to_int(arr[0])
    else:
        com = get_most_common_bit(arr, pos=pos)
        idx = np.where(arr[:, pos] != com)[0]
        return get_co2_scrub(arr[idx], pos=pos+1)


def get_life_support(arr):
    ox = get_ox_gen(arr)
    co2 = get_co2_scrub(arr)
    return ox*co2


def get_most_common_bit(arr, pos=0):
    n = len(arr)
    s = np.sum(arr, axis=0)
    if s[pos] >= n/2:
        return 1
    else:
        return 0


def convert_str_bin_to_int(bin_str):
    ans = 0
    for i, e in enumerate(bin_str[::-1]):
        if int(e):
            ans += 2**i
    return ans


def read_as_array(f_name):
    with open(f_name, 'r') as f:
        out = [[int(i) for i in j[:-1]] for j in f.readlines()]
    return np.array(out, dtype=int)


def main(f_name):
    out = read_as_array(f_name)
    print(f"total power: {get_power(out)}")
    print(f"life support: {get_life_support(out)}")


if __name__ == "__main__":
    main(sys.argv[1])
