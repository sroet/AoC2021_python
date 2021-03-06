import numpy as np
import sys


def count_increase(arr):
    arr2 = np.roll(arr, 1)
    diff = arr-arr2
    c = np.count_nonzero(diff[1:] > 0)  # Do not count first measurement
    return c


def count_windowed_increase(arr, window=3):
    conv_window = range(len(arr)-window+1)
    sum_arr = np.array([sum(arr[i:i+window])
                        for i in conv_window])
    return(count_increase(sum_arr))


def count_convoluted_increase(arr, window=3):
    sum_arr = np.convolve(arr, np.ones(window, dtype=int), 'valid')
    return count_increase(sum_arr)


def count_clever_convoluted_increase(arr, window=3):
    diff_filter = np.array([1]+[0]*(window-1)+[-1])
    diff_arr = np.convolve(arr, diff_filter, 'valid')
    return (np.count_nonzero(diff_arr > 0))


def read_as_int_array(f_name):
    with open(f_name, 'r') as f:
        out = [int(i) for i in f.readlines()]
    out_arr = np.array(out, dtype=int)
    return out_arr


def main(f_name):
    arr = read_as_int_array(f_name)
    print(f"increased: {count_increase(arr)}")
    print(f"windowed increase: {count_windowed_increase(arr)}")
    print(f"convolved increase: {count_convoluted_increase(arr)}")
    print(f"clever convolved increase: {count_clever_convoluted_increase(arr)}")


if __name__ == "__main__":
    main(sys.argv[1])
