import sys
import time
from heapq import heappush, heappop
import itertools

costs = {"A": 1,
         "B": 10,
         "C": 100,
         "D": 1000
         }


def read_file(f_name):
    with open(f_name, 'r') as f:
        lines = (i for i in f.readlines())
        _ = next(lines)  # wall
        hallway = "".join(['.' for i in next(lines) if i == "."])  # hallway
        rooms = []
        for i, e in enumerate(next(lines)):
            if e in costs:
                rooms.append(e)
                hallway = hallway[:i-1]+"R"+hallway[i:]

        for line in lines:
            i = 0
            for e in line:
                if e in costs:
                    rooms[i] += e
                    i = i + 1
    return hallway, tuple(rooms)


def generate_new_moves(state):
    hallway, rooms = state
    idx = [i for i, e in enumerate(hallway) if e == "R"]
    room_map = {"A": (0, idx[0]),
                "B": (1, idx[1]),
                "C": (2, idx[2]),
                "D": (3, idx[3]),
                }
    goal_map = {0: "A",
                1: "B",
                2: "C",
                3: "D"
                }

    # Move from hallway into room
    for i, ami in enumerate(hallway):
        if ami not in room_map:
            continue
        room, ridx = room_map[ami]
        left = min(i, ridx)+1
        right = max(i, ridx)
        if any(i in room_map for i in hallway[left:right]):
            # Blocked
            continue
        temp_room = rooms[room]
        if all(i in "."+ami for i in temp_room):
            hallway_c = hallway[:i] + '.' + hallway[i+1:]
            extra_cost = temp_room.count('.')
            out_room = (temp_room[:extra_cost-1] +
                        ami * (len(temp_room) - extra_cost + 1))
            rooms_c = tuple(r if i != room else out_room
                            for i, r in enumerate(rooms))
            cost = right - left + extra_cost + 1
            yield (hallway_c, rooms_c), cost*costs[ami]

    # Move from room to room
    for i, room in enumerate(rooms):
        if all(i == '.' for i in room):
            continue
        iidx = idx[i]
        topidx = [i for i, e in enumerate(room) if e != '.'][0]
        ami = room[topidx]
        cost = 1+topidx
        # Copy from above, should probably refactor
        roomidx, ridx = room_map[ami]
        if roomidx == i:
            # already in the right room
            continue
        left = min(iidx, ridx)+1
        right = max(iidx, ridx)
        if any(i in room_map for i in hallway[left:right]):
            # Blocked
            continue
        temp_room = rooms[roomidx]
        if all(i in "."+ami for i in temp_room):
            hallway_c = hallway
            extra_cost = temp_room.count('.')
            out_room = (temp_room[:extra_cost-1] +
                        ami * (len(temp_room)-extra_cost + 1))
            rooms_c = tuple(r if i != room else out_room
                            for i, r in enumerate(rooms))
            cost += right - left + extra_cost + 1
            yield (hallway_c, rooms_c), cost*costs[ami]

    # Move from room to hallway
    for i, room in enumerate(rooms):
        if all(i == '.' for i in room):
            continue
        goal = goal_map[i]
        if all(i in "."+goal for i in room):
            continue
        iidx = idx[i]
        topidx = [i for i, e in enumerate(room) if e != '.'][0]
        ami = room[topidx]
        cost = 1+topidx
        rooms_c = []
        for cidx, room in enumerate(rooms):
            if cidx == i:
                room = "".join(e if i != topidx else "."
                               for i, e in enumerate(room))
            rooms_c.append(room)
        rooms_c = tuple(rooms_c)
        # generetate left
        for j in range(0, iidx+1):
            tidx = iidx-j
            if hallway[tidx] in costs:
                break
            elif hallway[tidx] == "R":
                continue
            hallway_c = hallway[:tidx]+ami+hallway[tidx+1:]
            yield (hallway_c, rooms_c), (cost+j)*costs[ami]

        # generate right
        for j in range(0, len(hallway)-iidx):
            tidx = iidx+j
            if hallway[tidx] in costs:
                break
            elif hallway[tidx] == "R":
                continue
            if tidx+1 == len(hallway):
                hallway_c = hallway[:tidx]+ami
            else:
                hallway_c = hallway[:tidx]+ami+hallway[tidx+1:]
            yield (hallway_c, rooms_c), (cost+j)*costs[ami]


def do_dijkstra(out):
    # Following code is altered from
    # https://docs.python.org/3/library/heapq.html
    pq = []                         # list of entries arranged in a heap
    entry_finder = {}               # mapping of tasks to entries
    REMOVED = '<removed-task>'      # placeholder for a removed task
    counter = itertools.count()     # unique sequence count

    def add_task(task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in entry_finder:
            old_prio = entry_finder[task][0]
            if old_prio <= priority:
                return
            remove_task(task)
        count = next(counter)
        entry = [priority, count, task]
        entry_finder[task] = entry
        heappush(pq, entry)

    def remove_task(task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = entry_finder.pop(task)
        entry[-1] = REMOVED

    def pop_task():
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while pq:
            priority, count, task = heappop(pq)
            if task is not REMOVED:
                del entry_finder[task]
                return task, priority
        raise KeyError('pop from an empty priority queue')

    # Self written part
    visited = set()
    current_state = out
    current_weight = 0
    rl = len(current_state[1][0])  # room lenght
    while current_state[1] != ("A"*rl, "B"*rl, "C"*rl, "D"*rl):
        visited |= set([current_state])
        for next_state, cost in generate_new_moves(current_state):
            if next_state in visited:
                continue
            add_task(next_state, current_weight + cost)
        current_state, current_weight = pop_task()
    print(current_weight)


def main(f_name):
    s = time.time()
    out = read_file(f_name)
    do_dijkstra(out)
    print(f"total time: {time.time()-s}")


if __name__ == "__main__":
    main(sys.argv[1])
