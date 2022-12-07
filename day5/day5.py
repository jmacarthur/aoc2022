#!/usr/bin/env python3

from enum import Enum

class InputState(Enum):
    STACKS = 0
    INSTRUCTIONS = 1

with open("input5.txt") as f:
    mode = 0
    inputState = InputState.STACKS
    stacktext = []
    instructiontext = []
    while True:
        l = f.readline()
        if l == "":
            break
        if l.strip() == "" and inputState == InputState.STACKS:
            inputState = InputState.INSTRUCTIONS
            continue
        if inputState == InputState.STACKS:
            stacktext.append(l)
        else:
            instructiontext.append(l.strip())

# Now parse the stacks
num_stacks = 9
stacks = [None]
for s in range(0,num_stacks):
    stacks.append([])
print(stacktext)
for l in stacktext:
    if "[" in l:
        for s in range(0,num_stacks):
            if len(l) <= s*4+1:
                break
            c = l[s*4+1]
            if c != " ":
                stacks[s+1].append(l[s*4+1])

print(f"Initial state of the stacks: {stacks}")

single_move_mode = False

# Ok, now the move instructions
for inst in instructiontext:
    print(inst)
    fields = inst.split()
    count = int(fields[1])
    from_stack = int(fields[3])
    to_stack = int(fields[5])
    containers = []
    for c in range(0,count):
        containers.append(stacks[from_stack].pop(0))
    if single_move_mode:
        stacks[to_stack] = list(reversed(containers)) + stacks[to_stack]
    else:
        stacks[to_stack] = containers + stacks[to_stack]
    print(stacks)
print([s[0] for s in stacks[1:]])
