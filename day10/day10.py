#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    instructions = [l.strip().split() for l in f.readlines()]

delays = {
    "addx": 1,
    "noop": 0
}

def sprite_on(xpos, sprite_pos):
    return xpos >= (register_x-1) and xpos <= (register_x+1)

cycle = 1
register_x = 1
current_instruction = instructions.pop(0)
delay = delays[current_instruction[0]]
signal_strength = 0
lines = []

while True:
    print(f"{cycle:4}: {current_instruction[0]} {register_x}")
    if cycle%40 == 20:
        signal_strength += cycle * register_x
        print(f"Increase signal strength by {cycle * register_x} to {signal_strength}")
    xpos = (cycle-1)%40
    if xpos == 0:
        lines.append("")
    lines[-1] += "#" if sprite_on(xpos, register_x) else "."
    if delay == 0:
        if current_instruction[0] == 'addx':
            register_x += int(current_instruction[1])

        # Fetch next instruction
        if instructions:
            current_instruction = instructions.pop(0)
            delay = delays[current_instruction[0]]
        else:
            break
    else:
        delay -= 1
    cycle += 1

print(f"Final X: {register_x}")
print(f"Signal strength: {signal_strength}")

print("\n".join(lines))
