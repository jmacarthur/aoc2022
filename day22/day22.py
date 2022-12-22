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
            grid.append(list(l.strip('\n')))

instructions = re.split("([LR])", instruction_line)

print("Finding start postiion.")

start_x = 0
for (n, char) in enumerate(grid[0],0):
    if char == '.':
        start_x = n
        break

start_y = 0

print(f"Starting at {start_x+1}, {start_y+1}")
(x, y) = (start_x, start_y)

grid_width = max([len(row) for row in grid])
grid_height = len(grid)

# Pad grid with space characters
for row in grid:
    row += " "*(grid_width-len(row))

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
                print(f"  Step {d} potentially forward to {new_x+1}, {new_y+1}")
                if grid[new_y][new_x] != ' ':
                    break
            if grid[new_y][new_x] == '.':
                (x, y) = (new_x, new_y)
        print(f"Forward {distance}, to col {x+1}, row {y+1}")
    elif i == 'L':
        facing = (facing - 1) % 4
        print(f"Left, now facing {facing}")
    elif i == 'R':
        facing = (facing + 1) % 4
        print(f"Right, now facing {facing}")

print(f"Finished on column {x+1}, row {y+1}, facing in direction {facing}")
print(f"Password: {(y+1)*1000 + (x+1)*4 + facing}")

