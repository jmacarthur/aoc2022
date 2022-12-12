#!/usr/bin/env python3

# Uses python-astar by Julien Rialland. Get this from https://github.com/jrialland/python-astar.git
from python_astar import astar
from functools import partial

import sys
with open(sys.argv[1]) as f:
    lines = [list(l.strip()) for l in f.readlines()]

start = None
end = None

for (rownum, row) in enumerate(lines):
    for colnum in range(len(lines[0])):
        if row[colnum] == 'S':
            row[colnum] = 'a'
            start = (colnum, rownum)
        elif row[colnum] == 'E':
            row[colnum] = 'z'
            end = (colnum, rownum)

print("\n".join(["".join(l) for l in lines]))

print(f"Start: {start}")
print(f"End: {end}")

# For part 2: Uncomment this line with the starting 'a' position.
# For my input, the starting positions was obvious by looking at the map (see NOTES)
# start = (0,27)

def moves(pos, lines=lines):
    (x,y) = pos
    width = len(lines[0])
    height = len(lines)
    current_elevation = lines[y][x]
    directions = [(1,0), (0,-1), (-1,0), (0,1)]
    possible_moves = []
    for (dx, dy) in directions:
        if x+dx < 0 or y+dy < 0 or x+dx >= width or y+dy >= height:
            continue
        new_elevation = lines[y+dy][x+dx]
        if ord(new_elevation) - ord(current_elevation) <= 1:
            possible_moves.append((x+dx, y+dy))
    return possible_moves

def find_route(start, end, lines, route):
    print(f"Trying {route} -> {end}")
    if start == end:
        print(f"Route complete: {route}")
        return route
    possible_moves = moves(start, lines)
    best_route = None
    if len(route) > 30:
        return None
    for p in possible_moves:
        if p in route:
            continue
        r = find_route(p, end, lines, route+[p])
        if r:
            if best_route is None or len(r) < len(best_route):
                best_route = r
    return best_route


path = list(astar.find_path( start,
                             end,
                             neighbors_fnct = partial(moves, lines=lines),
                             heuristic_cost_estimate_fnct = lambda a,b: 1,
                             distance_between_fnct = lambda a,b: 1))

print(path)
print(len(path))
