import sys


def read_file(f_name):
    out_dict = {}
    with open(f_name, 'r') as f:
        for line in f.readlines():
            s = line.strip().split('-')
            out_dict[s[0]] = out_dict.get(s[0], set()) | set([s[1]])
            out_dict[s[1]] = out_dict.get(s[1], set()) | set([s[0]])
    return out_dict


def dfs(path_dict, current_node='start', visited=None, path=None):
    c = 0
    if visited is None:
        visited = set()
    if path is None:
        path = [current_node]
    else:
        path = path.copy()
        path.append(current_node)

    if current_node.upper() != current_node:
        new_visited = visited | set([current_node])
    else:
        new_visited = visited.copy()
    for next_node in path_dict[current_node]:
        if next_node in visited:
            continue
        elif next_node == 'end':
            c += 1
        else:
            c += dfs(path_dict, current_node=next_node, visited=new_visited,
                     path=path)
    return c


def dfs_2(path_dict, current_node='start', visited=None, path=None):
    c = 0
    if visited is None:
        visited = set()
    if path is None:
        path = [current_node]
    else:
        path = path.copy()
        path.append(current_node)

    if current_node.upper() != current_node:
        new_visited = visited | set([current_node])
    else:
        new_visited = visited.copy()
    for next_node in path_dict[current_node]:
        temp_visited = new_visited.copy()
        if next_node == 'start':
            continue
        elif next_node in visited:
            if '2' not in visited:
                temp_visited |= set(['2'])
            else:
                continue
        elif next_node == 'end':
            temp_path = path.copy()
            temp_path.append('end')
            c += 1
            continue
        c += dfs_2(path_dict, current_node=next_node, visited=temp_visited,
                   path=path)
    return c


def main(f_name):
    out = read_file(f_name)
    print(dfs(out))
    print(dfs_2(out))


if __name__ == "__main__":
    main(sys.argv[1])
