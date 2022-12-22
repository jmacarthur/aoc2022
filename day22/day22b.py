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

grid_width = max([len(row) for row in grid])
grid_height = len(grid)
print(f"Finding start postiion. Map is {grid_width} x {grid_height}")

start_x = 0
for (n, char) in enumerate(grid[1],0):
    if char == '.':
        start_x = n
        break

start_y = 1

print(f"Starting at {start_x}, {start_y}")
(x, y) = (start_x, start_y)

print(" " + "0123456789"*15)
for row in grid:
    print("|" + "".join(row) + "|")


facing = 0

def remap(new_x, new_y, new_facing):
    region = grid[new_y][new_x]
    print(f"Remap from region {region}")

    # The plan: trace along the region until we get to the capital, counting the distance.
    # Then, find the other capital, not us.. except sometimes there's only one! if that happens, we need to do something different.
    # Then, move along until we find the entry point. Then it's only a matter of remapping the facing direction.
    sys.exit(1)

for i in instructions:
    if i.isnumeric():
        distance = int(i)
        for d in range(0,distance):
            (dx, dy) = facing_deltas[facing]
            (new_x, new_y) = (x+dx, y+dy)
            new_facing = facing
            if grid[new_y][new_x] not in ["#", "."]:
                (new_x, new_y, new_facing) = remap(new_x, new_y, facing)
            elif grid[new_y][new_x] == '.':
                print(f"Forward 1 to {new_x}, {new_y}")
                (x, y) = (new_x, new_y)
                facing = new_facing
            elif grid[new_y][new_x] == '#':
                print(f"Blocked.")
        print(f"Forward {distance}, to col {x}, row {y}")
    elif i == 'L':
        facing = (facing - 1) % 4
        print(f"Left, now facing {facing}")
    elif i == 'R':
        facing = (facing + 1) % 4
        print(f"Right, now facing {facing}")

print(f"Finished on column {x}, row {y}, facing in direction {facing}")
print(f"Password: {(y)*1000 + (x)*4 + facing}")

