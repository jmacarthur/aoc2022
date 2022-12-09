#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    instructions = [l.strip().split() for l in f.readlines()]

rope_len = 10 # Try 2 for part 1

knots = [ (0,0) ] * rope_len

direction_map = {
    'R': (1,0),
    'U': (0,-1),
    'L': (-1,0),
    'D': (0,1)
    }

def sgn(x):
    if x>0: return 1
    elif x<0: return -1
    else: return 0

def move_tail(head, tail):
    dx = head[0]-tail[0]
    dy = head[1]-tail[1]
    if dx != 0 and dy != 0:
        if abs(dx)>=2 or abs(dy)>=2:
            return (tail[0] + sgn(dx), tail[1] + sgn(dy))
    else:
        if abs(dx)>=2:
            return (tail[0] + sgn(dx), tail[1])
        elif abs(dy)>=2:
            return (tail[0], tail[1]+sgn(dy))
    return tail

tailpositions = set([knots[-1]])

for (direction, distance) in instructions:
    (mx, my) = direction_map[direction]
    for i in range(0,int(distance)):
        knots[0] = (knots[0][0]+mx, knots[0][1]+my)
        for i in range(1,rope_len):
            knots[i] = move_tail(knots[i-1], knots[i])
        tailpositions.add(knots[-1])
        print(f"After {direction}: Head: {knots[0]}, Tail: {knots[-1]}")

print(f"The tail visited {len(tailpositions)} squares.")
