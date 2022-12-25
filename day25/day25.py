#!/usr/bin/env python3

import math
import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()

char_value = { '2':  2,
               '1':  1,
               '0':  0,
               '-': -1,
               '=': -2 }
digit_char = { v: k for k, v in char_value.items() }

supertotal = 0

for line in lines:
    val = 1
    line_total = 0
    for charpos in range(len(line.strip())-1, -1, -1):
        char = line[charpos]
        line_total += char_value[char]*val
        val *= 5
    print(f"{line.strip()} => {line_total}")
    supertotal += line_total

last_pos = None
digit_string = ""

print(f"Total in decimal: {supertotal}")

while supertotal != 0:
    position = 0
    digit_range = 1
    while supertotal > 2*digit_range or supertotal < -2*digit_range:
        position += 1
        digit_range += 5**position
        
    if last_pos:
        for j in range(0, last_pos-position-1):
            digit_string += "0"

    digit = round(supertotal/(5**position))
    last_pos = position
    digit_string += digit_char[digit]
    supertotal -= digit*(5**position)

for j in range(0, position):
    digit_string += "0"

print(f"Total in SNAFU: {digit_string}")
