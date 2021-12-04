import sys
import numpy as np


def read_as_array(f_name):
    with open(f_name, 'r') as f:
        numbers = {int(e): i for i, e in enumerate(f.readline().split(','))}
        boards = []
        rows = []
        for line in f.readlines():
            if line != "\n":
                rows.append([int(i) for i in line.split()])
            elif len(rows) != 0:
                boards.append(rows)
                rows = []
        if len(rows) != 0:
            boards.append(rows)
            rows = []
    return numbers, np.array(boards)


def find_first_winning(numbers, boards):
    winning = 0
    winning_turn = np.inf
    for i, board in enumerate(boards):
        minimum_turn = np.inf
        for b in (board, board.T):
            for row in b:
                win = max(numbers[i] for i in row)
                if win < minimum_turn:
                    minimum_turn = win
        if minimum_turn < winning_turn:
            winning_turn = minimum_turn
            winning = i
    return boards[winning], winning_turn


def find_last_winning(numbers, boards):
    winning = 0
    winning_turn = 0
    for i, board in enumerate(boards):
        minimum_turn = np.inf
        for b in (board, board.T):
            for row in b:
                win = max(numbers[i] for i in row)
                if win < minimum_turn:
                    minimum_turn = win
        if minimum_turn > winning_turn:
            winning_turn = minimum_turn
            winning = i
    return boards[winning], winning_turn


def find_score(numbers, winning_turn, winning_board):
    pulled = {i for i, j in numbers.items() if j <= winning_turn}

    last = [i for i, j in numbers.items() if j == winning_turn][0]
    score = sum(set(i for i in winning_board.ravel())-pulled)
    return score*last


def main(f_name):
    numbers, boards = read_as_array(f_name)
    winning_board, winning_turn = find_first_winning(numbers, boards)
    score = find_score(numbers, winning_turn, winning_board)

    print(f"numbers:{numbers}")
    print(f"{np.array(boards).shape}")
    print(f"winning board: {winning_board}")
    print(f"score {score}")

    print("PART 2")
    winning_board, winning_turn = find_last_winning(numbers, boards)
    score = find_score(numbers, winning_turn, winning_board)
    print(f"winning board: {winning_board}")
    print(f"score {score}")


if __name__ == "__main__":
    main(sys.argv[1])
