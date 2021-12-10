import sys

score = {')': 3,
         ']': 57,
         '}': 1197,
         '>': 25137
         }

part_2_score = {')': 1,
                ']': 2,
                '}': 3,
                '>': 4,
                }

matches = {'(': ')',
           '[': ']',
           '{': '}',
           '<': '>'
           }

opens = ['(', '[', '{', '<']
closes = [')', ']', '}', '>']


def read_file(f_name):
    with open(f_name, 'r') as f:
        out = []
        for line in f.readlines():
            out.append(line.strip())
    return out


def find_corrupted_lines(out):
    s = 0
    s2s = []
    for line in out:
        expected_closes = []
        corrupt = False
        for c in line:
            if c in opens:
                expected_closes.append(matches[c])
            elif c in closes:
                if c == expected_closes[-1]:
                    _ = expected_closes.pop()
                else:
                    s += score[c]
                    corrupt = True
                    break
            else:
                print(c)
        if corrupt:
            continue
        s2 = 0
        for c in expected_closes[::-1]:
            s2 *= 5
            s2 += part_2_score[c]
        s2s.append(s2)
    s2s.sort()
    idx = int(len(s2s)//2)
    return s, s2s[idx]


def main(f_name):
    out = read_file(f_name)
    print(find_corrupted_lines(out))


if __name__ == "__main__":
    main(sys.argv[1])
