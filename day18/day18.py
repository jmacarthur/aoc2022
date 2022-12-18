#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()

droplets = [tuple(map(int, l.strip().split(","))) for l in lines]

directions = [ (1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1) ]

exposed = 0
for (x,y,z) in droplets:
    for (dx,dy,dz) in directions:
        if (x+dx, y+dy, z+dz) not in droplets:
            exposed += 1

print(f"Total exposed sides (part 1): {exposed}")

# Get the bounding box, expanding it by 1 so the steam can fill the
# perimeter regardless of which droplets are present.
bounding_box = [ (min([p[i] for p in droplets])-1, max([p[i] for p in droplets])+1) for i in range(0,3) ]

# Flood fill, starting from the min x,y,z coordinate
steam_list = set([(bounding_box[0][0], bounding_box[1][0], bounding_box[2][0])])

def in_bounding_box(position, bonding_box):
    for i in range(0,3):
        if position[i] < bounding_box[i][0] or position[i] > bounding_box[i][1]:
            return False
    return True

expanding_steam = steam_list
while True:
    new_steam_list = set()
    for (x, y, z) in expanding_steam:
        for (dx, dy, dz) in directions:
            p = (x+dx, y+dy, z+dz)
            if in_bounding_box(p, bounding_box) and p not in droplets and p not in steam_list:
                new_steam_list.add(p)
    expanding_steam = new_steam_list
    steam_list |= expanding_steam
    if len(expanding_steam) == 0:
        break

# Now check the exposures again, but only count where there's steam.
steam_exposed = 0
for (x, y, z) in droplets:
    for (dx, dy, dz) in directions:
        if (x+dx, y+dy, z+dz) in steam_list:
            steam_exposed += 1

print(f"Total exposed sides (part 2): {steam_exposed}")
