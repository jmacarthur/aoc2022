#!/usr/bin/env python3

import sys
import re

grid = []
facing_deltas = [ (1,0), (0,1), (-1,0), (0,-1) ]

with open(sys.argv[1]) as f:
    while True:
        l = f.readline()
        if l == "": break
        if l.strip() == "":
            instruction_line = f.readline().strip()
            break
        else:
            grid.append([" "] + list(l.strip('\n')))

instructions = re.split("([LR])", instruction_line)


grid_width = max([len(row) for row in grid])+1
grid_height = len(grid)
print(f"Finding start postiion. Map is {grid_width} x {grid_height}")
# Pad grid with space characters, including around the edge

for row in grid:
    row.extend([" "]*(grid_width-len(row)))

grid.insert(0, [" "]*grid_width)
grid.append([" "]*grid_width)

start_x = 0
for (n, char) in enumerate(grid[1],0):
    if char == '.':
        start_x = n+1
        break

start_y = 1

print(f"Starting at {start_x}, {start_y}")
(x, y) = (start_x, start_y)

for row in grid:
    print("|" + "".join(row) + "|")


facing = 0

for i in instructions:
    if i.isnumeric():
        distance = int(i)
        for d in range(0,distance):
            (dx, dy) = facing_deltas[facing]
            (new_x, new_y) = (x, y)
            while True:
                new_x = (new_x+dx)%grid_width
                new_y = (new_y+dy)%grid_height
                print(f"  Step {d} potentially forward to {new_x}, {new_y}")
                if grid[new_y][new_x] != ' ':
                    break
            if grid[new_y][new_x] == '.':
                (x, y) = (new_x, new_y)
        print(f"Forward {distance}, to col {x}, row {y}")
    elif i == 'L':
        facing = (facing - 1) % 4
        print(f"Left, now facing {facing}")
    elif i == 'R':
        facing = (facing + 1) % 4
        print(f"Right, now facing {facing}")

print(f"Finished on column {x}, row {y}, facing in direction {facing}")
print(f"Password: {(y)*1000 + (x)*4 + facing}")

