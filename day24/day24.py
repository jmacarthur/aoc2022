#!/usr/bin/env python3

# Uses python-astar by Julien Rialland. Get this from https://github.com/jrialland/python-astar.git
from python_astar import astar
import sys

if len(sys.argv)<5:
    print("Usage: dy24.py <input> <start_time> <f|r> <time_limit>")
    print("If 'r' (reverse) is supplied, trace from bottom right to "
          "top left to bottom right, otherwise trace top left to bottom right "
          "as usual. Max time explored is start_time + time_limit.")
    sys.exit(0)

with open(sys.argv[1]) as f:
    lines = f.readlines()
    header = lines.pop(0)
    footer = lines.pop(-1)

blizzard_char = ['>', 'v', '<', '^' ]
dx = [ 1, 0, -1, 0 ]
dy = [ 0, 1, 0, -1 ]
blizzards = []

width = 0
for (y, l) in enumerate(lines):
    chars = l.strip()[1:-1]
    for (x, char) in enumerate(chars):
        width = max(width, x+1)
        if char in blizzard_char:
            direction = blizzard_char.index(char)
            blizzards.append((x,y,direction))
height = y+1
            
cycle_time = width
while cycle_time % height > 0:
    cycle_time += width

print(f"Field size: {width} x {height}. Cycle time {cycle_time}.")

# Precompute a 3D array which shows which map squares are occupied by blizzards at any given time.
occupied_at_time = [None]*cycle_time
for t in range(0,cycle_time):
    occupied_at_time[t] = [None]*height
    for y in range(0,height):
        occupied_at_time[t][y] = [False]*width
    for (sx, sy, direction) in blizzards:
        bx = (sx + dx[direction]*t) % width
        by = (sy + dy[direction]*t) % height
        occupied_at_time[t][by][bx] = True

start_time = int(sys.argv[2])
time_limit = int(sys.argv[4])
end_time = start_time+time_limit
if sys.argv[3] == 'r':
    direction = -1
    start = (width-1, height, start_time)
    end = (0, -1, end_time)
else:
    direction = 1
    start = (0,-1,start_time)
    end = (width-1, height, end_time)

def can_move(x, y, time):
    if (x==0 and y==-1) or (x==width-1 and y==height):
        return True
    if x < 0 or y < 0 or x>=width or y>=height:
        return False
    if occupied_at_time[time%cycle_time][y][x]:
        return False
    return True
    
def moves(position):
    global direction
    (x, y, time) = position
    if time > end_time:
        return []
    if (x == width-1 and y==height and direction==1) or (x==0 and y==-1 and direction==-1):
        # Reached the destination? Just stay here.
        return [(x,y,time+1)]
    candidates = []
    for direction in range(0,4):
        if can_move(x+dx[direction], y+dy[direction], time+1):
            candidates.append((x+dx[direction], y+dy[direction], time+1))
    if can_move(x, y, time+1):
        # Add the 'waiting here' option.
        candidates.append((x,y,time+1))
    return candidates

print(f"Looking for: {start} to {end}")

# A* is usually (in my experience) used to search a physical space,
# but it's just as easy to search a three-dimensional space of which
# one dimension is time, which is what we're doing here.

path = astar.find_path( start,
                        end,
                        neighbors_fnct = moves,
                        heuristic_cost_estimate_fnct = lambda a,b: 1,
                        distance_between_fnct = lambda a,b: 1)

if path:
    print(list(path))
else:
    print("No path to solution")
