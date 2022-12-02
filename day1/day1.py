#!/usr/bin/env python3

"""This just produces the calorie counts per elf. I just run
'./day2.py | sort -n' and read off the last or last three values.

"""

with open("input1.txt") as f:
    tcal = 0
    while True:
        l = f.readline()
        if l == "": break
        if l.strip() == "":
            print(tcal)
            tcal = 0
        else:
            cal = int(l)
            tcal += cal

print(tcal)
