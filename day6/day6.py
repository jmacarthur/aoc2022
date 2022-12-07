#!/usr/bin/env python3

def is_all_unique(window):
    seen = set()
    for c in window:
        if c in seen:
            return False
        seen.add(c)
    return True

with open("input6.txt") as f:
    datastream = f.readline()

windowlength = 14
window = []
pos = 0
for c in datastream:
    window.append(c)
    pos += 1
    if len(window) > windowlength:
        window.pop(0)
    if len(window) == windowlength:
        if is_all_unique(window):
            print(f"Header appears at position {pos}")
