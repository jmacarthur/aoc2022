#!/usr/bin/env python3

from enum import Enum
from functools import cmp_to_key
import json
import sys

pairs = []

class Result(Enum):
    LOWER = -1
    EQUAL = 0
    HIGHER = 1

with open(sys.argv[1]) as f:
    while True:
        l = f.readline()
        if l == "": break
        if l.strip() == "":
            continue
        left = json.loads(l.strip())
        right = json.loads(f.readline().strip())
        pairs.append((left, right))

print(pairs)

def compare(left, right, indent=""):
    if type(left)==int and type(right)==int:
        print(f"{indent}Comparing {left} and {right}: Both integers")
        if left < right:
            return Result.LOWER
        elif left > right:
            return Result.HIGHER
        else:
            return Result.EQUAL
    elif type(left) == list and type(right)==list:
        index = 0
        while True:
            print(f"{indent}Comparing {left} and {right}: Both lists, check index {index}")
            if index >= len(left) and index >= len(right):
                return Result.EQUAL
            elif index >= len(left):
                return Result.LOWER
            elif index >= len(right):
                return Result.HIGHER
            res = compare(left[index], right[index], indent+"  ")
            if res != Result.EQUAL:
                return res
            print(f"{indent}Nothing definitive at index {index}")
            index += 1
    elif type(left) == int:
        print(f"{indent}Comparing {left} and {right}: Convert left")
        return compare([left], right, indent+"  ")
    elif type(right) == int:
        print(f"{indent}Comparing {left} and {right}: Convert right")
        return compare(left, [right], indent+"  ")
    else:
        print(f"{indent}Unhandled case: comparing {left} and {right}")
        sys.exit(1)

total = 0
for (index, p) in enumerate(pairs, start=1):
    res = compare(p[0], p[1])
    if res == Result.LOWER:
        total += index
    print(index, res)

print(total)

all_packets = []
for (left, right) in pairs:
    all_packets.append(left)
    all_packets.append(right)

all_packets.append([[2]])
all_packets.append([[6]])

sorted_packets = sorted(all_packets, key=cmp_to_key(lambda a,b: compare(a,b).value))

for (index, p) in enumerate(sorted_packets, start=1):
    print(index, p)
