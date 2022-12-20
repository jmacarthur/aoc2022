#!/usr/bin/env python3

import sys

# For round 1, set decrypt_key = 1 and mix_rounds = 1.
decrypt_key = 811589153
mix_rounds = 10

class Entry():
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.value)

with open(sys.argv[1]) as f:
    input_list = list(map(int,f.readlines()))

# Make two lists; original_values is the Entry objects in the order
# they were supplied, and mixed_values is the same objects, initially
# in the same order.
original_values = [Entry(x*decrypt_key) for x in input_list]
mixed_values = [x for x in original_values]

for i in range(0,mix_rounds):
    for v in original_values:
        old_index = mixed_values.index(v)
        mixed_values.remove(v)
        new_index = (old_index + v.value) % len(mixed_values)
        print(f"Processing {v.value}; removed from {old_index} and inserted at {new_index}")
        mixed_values.insert(new_index, v)

def gps(values):
    start = values.index([v for v in values if v.value==0][0])
    total = 0
    for i in range(1,4):
        total += values[(start+i*1000) % len(values)].value
    return total

print(f"Final mixed value: {mixed_values}")
print(f"GPS value: {gps(mixed_values)}")
