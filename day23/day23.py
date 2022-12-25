#!/usr/bin/env python3

import sys

elves = []

class Elf():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def add_pos_tuple(self, pos):
        return (self.x + pos[0], self.y + pos[1])

with open(sys.argv[1]) as f:
    for (row, line) in enumerate(f.readlines()):
        for (col, char) in enumerate(line):
            if char == '#':
                elves.append(Elf(col, row))

print(f"{len(elves)} total elves")

move_plans = [ ((-1, -1), (0, -1), ( 1, -1)),
               ((-1,  1), (0,  1), ( 1,  1)),
               ((-1, -1), (-1, 0), (-1,  1)),
               (( 1, -1), ( 1, 0), ( 1,  1)) ]

all_neighbours = [ (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0) ]

def cycle(elves) :
    proposed_destinations = {}
    elfpos = [(e.x, e.y) for e in elves]
    for e in elves:
        e.target = None
        if any([e.add_pos_tuple(n) in elfpos for n in all_neighbours]):
            for (diag1, mid, diag2) in move_plans:
                if e.add_pos_tuple(diag1) not in elfpos and e.add_pos_tuple(mid) not in elfpos and e.add_pos_tuple(diag2) not in elfpos:
                    e.target = e.add_pos_tuple(mid)
                    if e.target not in proposed_destinations:
                        proposed_destinations[e.target]=1
                    else:
                        proposed_destinations[e.target] += 1
                    break

    single_destinations = [k for k in proposed_destinations.keys() if proposed_destinations[k]==1]

    print(f"{len(proposed_destinations)} destinations proposed, of which {len(single_destinations)} are single targets")

    new_elves = []
    move_count = 0
    for e in elves:
        if e.target and e.target in single_destinations:
            new_elves.append(Elf(e.target[0], e.target[1]))
            move_count += 1
        else:
            new_elves.append(e)
    return (move_count, new_elves)

round = 0
while True:
    round += 1
    (move_count, elves) = cycle(elves)
    move_plans.append(move_plans.pop(0))

    print("Move plans now: ")
    for n in move_plans:
        print(n)
    
    width = max([e.x for e in elves]) - min([e.x for e in elves]) + 1
    height = max([e.y for e in elves]) - min([e.y for e in elves]) + 1


    print(elves)
    min_x = min([e.x for e in elves])
    min_y = min([e.y for e in elves])
    elfpos = [(e.x, e.y) for e in elves]
    for row in range(-2,height+5):
        line = ""
        for col in range(0,width+5):
            if (col, row) in elfpos:
                line += "#"
            else:
                line += "."
        print(line)
    print(f"End of round {round}. Bounding box: {width} * {height}: area {width*height}; empty tiles {width*height-len(elves)}. Move count {move_count}")
    if move_count == 0:
        break



