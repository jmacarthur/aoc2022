#!/usr/bin/env python3

import re
import sys

sensors = []

input_pattern = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

class Sensor():
    def __init__(self, sx, sy, bx, by):
        self.sx = sx
        self.sy = sy
        self.bx = bx
        self.by = by
        dx = bx-sx
        dy = by-sy
        self.detect_range = abs(dx)+abs(dy)
    def inrange(self, x, y):
        dx = x-self.sx
        dy = y-self.sy
        return (abs(dx)+abs(dy))<=self.detect_range
    def perimeter(self):
        for i in range(0, self.detect_range+1):
            yield((self.sx + i, self.sy-self.detect_range-1+i))
            yield((self.sx + self.detect_range+1-i, self.sy - i))
            yield((self.sx - i, self.sy+self.detect_range+1-i))
            yield((self.sx - self.detect_range-i+i, self.sy + i))
    def __str__(self):
        return f"{self.sx},{self.sy} range {self.detect_range}"

with open(sys.argv[1]) as f:
    for l in f.readlines():
        m = re.match(input_pattern, l.strip())
        if m:
            sensor = [int(m.group(n)) for n in range(1,5)]
            sensors.append(Sensor(sensor[0], sensor[1], sensor[2], sensor[3]))
            print(sensor)
        else:
            print(f"Unmatched line: {l}")
            sys.exit(1)

part1 = True
part2 = True

""" Part 1: A pretty simple brute force search."""

if part1:
    min_x = min([s.sx - s.detect_range for s in sensors])
    max_x = max([s.sx + s.detect_range for s in sensors])
    print(f"Max horizontal range is {min_x} to {max_x}")
    total = 0
    y = 2000000
    for x in range(min_x, max_x+1):
        if any(s.bx == x and s.by == y for s in sensors):
            # We're ON a beacon, so don't count this
            pass
        elif any(s.inrange(x, y) for s in sensors):
            total += 1
    print(f"On line {y}, {total} positions cannot contain a beacon")

""" Part 2: Still mostly brute force, but with an observation: If
there is only one space which could contain the distress beacon, it
must be *just* outside the sensing range of at least one beacon. So we
only need to search the perimeter around each beacon's range, not each
individual square. """

if part2:
    maxrange = 4000000
    for s in sensors:
        print(f"Searching perimeter of beacon {s}...")
        for pos in s.perimeter():
            if pos[0]<0 or pos[1]<0 or pos[0]>maxrange or pos[1]>maxrange:
                continue
            if not any(s.inrange(pos[0], pos[1]) for s in sensors):
                print(f"{pos} is not in range of any beacon.")
                sys.exit(0)
