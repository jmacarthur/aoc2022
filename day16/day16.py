#!/usr/bin/env python3

import copy
import re
import sys

input_pattern = re.compile("Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)$")


class Valve():
    def __init__(self, identity, flowrate, connections):
        self.identity = identity
        self.flowrate = flowrate
        self.connections = connections

roomstate = {}
rooms = {}
useful_valve_count = 0
roomlist = []
with open(sys.argv[1]) as f:
    for l in f.readlines():
        m = re.match(input_pattern, l.strip())
        if m:
            flow = int(m.group(2))
            ident = m.group(1)
            rooms[m.group(1)] = Valve(ident, flow, m.group(3).split(", "))
            roomstate[ident] = False
            roomlist.append(ident)
            if flow>0:
                useful_valve_count += 1
        else:
            print(f"Unrecognised line: {l.strip()}")
            sys.exit(1)

start_room = "AA"

print(f"Starting in room {start_room}; there are {useful_valve_count} useful valves.")
assert rooms[start_room].flowrate == 0

max_flow = sum([r.flowrate for r in rooms.values()])

def find_route(start, end, visited):
    if start == end:
        return []
    best_route = None
    for d in rooms[start].connections:
        if end == d:
            return [d]
        elif d in visited:
            continue
        else:
            r = find_route(d, end, visited+[d])
            if r and (best_route is None or len(r) < len(best_route)-1):
                best_route = [d] + r
    return best_route

routes = {}

print("Precomputing travel times...")
valve_rooms = [r for r in roomlist if rooms[r].flowrate > 0]
for start in valve_rooms + [start_room]:
    routes[(start, start)] = 0
    for end in valve_rooms:
        if (start, end) in routes:
            continue
        route = find_route(start, end, [])
        if start != end:
            routes[(start, end)] = len(route)
            routes[(end, start)] = len(route)

def valves_complete(moves_so_far, minute):
    valves_complete = []
    move_time = 0
    if len(moves_so_far) <= 1:
        return []
    for i in range(1,len(moves_so_far)):
        last = moves_so_far[i-1]
        dest = moves_so_far[i]
        move_time += routes[(last, dest)] + 1
        if minute > move_time:
            valves_complete.append(dest)
    return valves_complete

def can_move(moves_so_far, minute):
    """Determine if we're ready to move; assuming we turned on a valve
    after each move.
    """
    move_time = 0
    if len(moves_so_far) <= 1:
        return True
    for i in range(1,len(moves_so_far)):
        last = moves_so_far[i-1]
        dest = moves_so_far[i]
        move_time += routes[(last, dest)] + 1
    return minute > move_time

def complete_run(minute, player_moves, player_available, max_time):
    flow = sum([rooms[v].flowrate for v in valves_complete(player_moves, minute)])

    if minute >= max_time:
        return flow

    if len(player_moves) >= len(player_available)+1:
        # We can't make any more moves. But we might still be in the
        # middle of an uncompeted move, so we still use recursion to
        # figure out the final score.
        return flow + complete_run(minute+1, player_moves, [], max_time)

    if can_move(player_moves, minute):
        best_score = None
        best_dest = None
        for dest in player_available:
            if dest in player_moves:
                continue
            potential_score = complete_run(minute+1, player_moves + [dest], player_available, max_time)
            if best_score is None or potential_score > best_score:
                best_score = potential_score
                best_dest = dest
        if best_dest:
            return flow + best_score

    return flow + complete_run(minute+1, player_moves, player_available, max_time)

# Part 1: Max score in 30 minutes, one actor
score = complete_run(1, ['AA'], valve_rooms, 30)
print(f"Score for part 1: {score}")

# Part 2: Max score in 26 minutes, two actors
""" Partition the valve rooms into two lists; there are
2**(valve_rooms) ways to do this, although it doesn't matter which
list gets given to which actor, so we only need to process half of
that. Then, each actor only has to get the optimal path for their
valve rooms independently, and the total released is just the sum of
each actor.  """

print(f"Enumerating {2**(len(valve_rooms)-1)} partitions.")
max_score = None
for i in range(0, 2**(len(valve_rooms)-1)):
    player_available = []
    elephant_available = []
    for j in range(0,len(valve_rooms)):
        if (i >> j) & 1 == 0:
            player_available.append(valve_rooms[j])
        else:
            elephant_available.append(valve_rooms[j])

    score = complete_run(1, ['AA'], player_available, 26)
    score += complete_run(1, ['AA'], elephant_available, 26)
    print(f"Partition {i} ({player_available}, {elephant_available}: best score {score}")
    if max_score is None or score > max_score:
        print("New best!")
        max_score = score
print(f"Overall best for part 2: {max_score}")
