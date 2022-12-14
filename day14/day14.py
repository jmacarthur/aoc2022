#!/usr/bin/env python3

import sys

lines = []
allcoords = []
with open(sys.argv[1]) as f:
    for l in f.readlines():
        fields = l.split(" -> ")
        coords = []
        for f in fields:
            coord = list(map(int, f.split(",")))
            coords.append(coord)
            allcoords.append(coord)
        lines.append(coords)

print(lines)

""" For part 1, you can limit all coordinates to the min/max of line
coordinates plus a small border, but for part 2 we need a much wider
and taller grid. """
min_x = 0
max_x = 1000
min_y = 0
max_y = max([y for(x,y) in allcoords])+1

print(f"Min X: {min_x} Max X: {max_x} Min Y: {min_y} Max Y: {max_y}")

x_range = max_x - min_x + 1
y_range = max_y - min_y + 1

class Grid():
    def __init__(self, width, height, startx, starty):
        self.grid = [['.']* width for y in range(height)]
        self.startx = startx
        self.starty = starty
        self.width = width
        self.height = height

    def get(self, x, y):
        if x<self.startx or y<self.starty or x-self.startx>=self.width or y-self.starty>=self.height:
            return None
        return self.grid[y-self.starty][x-self.startx]

    def set(self, x, y, char):
        if x<self.startx or y<self.starty or x-self.startx>=self.width or y-self.starty>=self.height:
            return
        self.grid[y-self.starty][x-self.startx] = char

grid = Grid(x_range, y_range, min_x, min_y)

def eachway_range(start, end):
    if end>start:
        return range(start, end+1)
    else:
        return range(end, start+1)

for l in lines:
    start = l[0]
    index = 1
    grid.set(start[0], start[1], '#')
    while index < len(l):
        next_point = l[index]
        if next_point[0] == start[0]:
            for y in eachway_range(start[1], next_point[1]):
                grid.set(start[0], y, '#')
        elif next_point[1] == start[1]:
            for x in eachway_range(start[0], next_point[0]):
                grid.set(x, start[1], '#')
        index += 1
        start = next_point

def trace_sand(grid, x, y, floor = False):
    while True:
        if grid.get(x, y+1) is None:
            if floor:
                grid.set(x, y, 'o')
                return False
            else:
                return True
        if grid.get(x, y+1) == '.':
            y += 1
            continue
        elif grid.get(x-1, y+1) == '.':
            x -= 1
            y += 1
            continue
        elif grid.get(x+1, y+1) == '.':
            x += 1
            y += 1
            continue
        else:
            grid.set(x,y, 'o')
            return False

count = 0
while True:
    count += 1
    escape = trace_sand(grid, 500, grid.starty)
    if escape:
        break

print(f"Sand grain {count} escaped.")

count -= 1 # Account for the one that fell out!

for (n,l)  in enumerate(grid.grid):
    print(f"{n+grid.starty:4} " + "".join(l))

while grid.get(500,0)=='.':
    count += 1
    escape = trace_sand(grid, 500, grid.starty, True)

for (n,l)  in enumerate(grid.grid):
    print(f"{n+grid.starty:4} " + "".join(l))

print(f"Sand grain {count} was placed at the start point.")
