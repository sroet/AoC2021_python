import sys
import itertools as itt
from collections import Counter
import time


def read_file(f_name):
    with open(f_name, 'r') as f:
        lines = (i.strip() for i in f.readlines())
        out = [int(i.split()[-1]) for i in lines]
    return out


def play_deterministic_game(inp):
    score = {0: 0,
             1: 0}
    p1 = inp[0]
    p2 = inp[1]
    players = [p1, p2]
    player = 1
    die = (i for _ in range(int(1e6)) for i in range(1, 101))
    c = 0
    while score[player] < 1000:
        player = int(not player)
        place = players[player]
        dies = sum(next(die) for _ in range(3))
        c += 3
        new_place = (place+dies-1) % 10 + 1
        score[player] += new_place
        players[player] = new_place
    score = score[int(not player)]
    print(f"score: {score}")
    print(f"rolls: {c}")
    print(f"answer part 1: {score*c}")


def play_dirac_game(inp):
    possibilities = {}
    pos_score_counter = {(inp[0], inp[1]): {(0, 0): 1}}
    win_counter = Counter()
    for pos1 in itt.product([1, 2, 3], repeat=3):
        for pos2 in itt.product([1, 2, 3], repeat=3):
            s1 = sum(pos1)
            s2 = sum(pos2)
            val = possibilities.get((s1, s2), 0)
            possibilities[(s1, s2)] = val+1
    while pos_score_counter:
        new_pos_score_counter = {}
        for (pos1, pos2), score_counter in pos_score_counter.items():
            for (r1, r2), val in possibilities.items():
                new_s1 = (pos1+r1-1) % 10 + 1
                new_s2 = (pos2+r2-1) % 10 + 1
                scores = (((s1+new_s1, s2+new_s2), v*val)
                          for (s1, s2), v in score_counter.items())
                new_pos = new_pos_score_counter.get((new_s1, new_s2), {})
                for (s1, s2), value in scores:
                    if s1 >= 21:
                        win_counter.update({1: value})
                    elif s2 >= 21:
                        win_counter.update({2: value})
                    else:
                        new_val = new_pos.get((s1, s2), 0)
                        new_pos[(s1, s2)] = new_val+value
                if new_pos:
                    new_pos_score_counter[(new_s1, new_s2)] = new_pos
        pos_score_counter = new_pos_score_counter
    # Correct for the fact that we roll player 2 after player 1 has won
    win_counter[1] = win_counter[1] // 3**3
    print(f"player 1: {win_counter[1]}")
    print(f"player 2: {win_counter[2]}")


def main(f_name):
    s = time.time()
    out = read_file(f_name)
    print(f"time for file_reading: {time.time()-s}")
    s1 = time.time()
    play_deterministic_game(out)
    print(f" deterministic time: {time.time()-s1}")
    s1 = time.time()
    play_dirac_game(out)
    print(f" dirac_time: {time.time()-s1}")
    print(f"total time: {time.time()-s}")


if __name__ == "__main__":
    main(sys.argv[1])
