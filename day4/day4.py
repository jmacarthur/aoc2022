#!/usr/bin/env python3

def contains(range1, range2):
    return range1[0] >= range2[0] and range1[1] <= range2[1]

def overlaps(range1, range2):
    if range1[1] < range2[0] or range1[0] > range2[1]:
        return False
    return True

containment_count = 0
overlap_count = 0
with open("input4.txt") as f:
    while True:
        l = f.readline()
        if l == "":
            break
        elves = l.strip().split(",")
        r1 = list(map(int,elves[0].split("-")))
        r2 = list(map(int,elves[1].split("-")))
        if contains(r1, r2) or contains(r2,r1):
            print(f"{r1} contains {r2} or vice-versa")
            containment_count += 1
        if overlaps(r1,r2):
            print(f"{r1} overlaps {r2}")
            overlap_count += 1

print(containment_count)
print(overlap_count)
