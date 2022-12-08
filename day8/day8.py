#!/usr/bin/env python3

import math
import sys

class Grid():
    def __init__(self, lines):
        self.lines = lines
        self.width = max(len(l) for l in self.lines)
        self.height = len(self.lines)
    def __getitem__(self, key):
        (x,y) = key
        return int(self.lines[y][x])

    def _is_visible_in_direction(self, x, y, dx, dy):
        our_height = self[(x,y)]
        while True:
            x += dx
            y += dy
            if x<0 or y<0 or x>=self.width or y>=self.height:
                return True
            if self[(x,y)] >= our_height:
                """ View is blocked in this direction, try next direction """
                return False

    def is_visible(self, x,y):
        directions = [(1,0), (0,-1), (-1,0), (0,1)]
        for (dx,dy) in directions:
            if self._is_visible_in_direction(x,y,dx,dy):
                return True
        return False

    def num_visible(self, x, y):
        directions = [(1,0), (0,-1), (-1,0), (0,1)]
        our_height = self[(x,y)]
        direction_totals = []
        for (dx,dy) in directions:
            direction_total = 0
            (cx, cy) = (x,y)
            while True:
                cx += dx
                cy += dy
                if cx<0 or cy<0 or cx>=self.width or cy>=self.height:
                    break
                # Ok, so there is a tree here
                direction_total += 1
                if self[(cx,cy)] >= our_height:
                    break
            direction_totals.append(direction_total)
        return direction_totals

with open(sys.argv[1]) as f:
    grid = Grid([l.strip() for l in f.readlines()])

print(f"Read in a grid of size {grid.width} x {grid.height}")

total = 0
for row in range(0,grid.height):
    vis = [1 if grid.is_visible(col, row) else 0 for col in range(0,grid.width)]
    total += sum(vis)

print(f"{total} trees are visible")

max_score = None
for x in range(0,grid.width):
    for y in range(0,grid.height):
        score = math.prod(grid.num_visible(x,y))
        if max_score is None or score > max_score:
            print(f"Tree at {x},{y} scores {score}")
            max_score = score

