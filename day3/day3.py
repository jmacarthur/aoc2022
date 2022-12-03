#!/usr/bin/env python3

def priority(character):
    if ord(character) >= ord('a') and ord(character) <= ord('z'):
        return ord(character) - ord('a') + 1
    elif ord(character) >= ord('A') and ord(character) <= ord('Z'):
        return ord(character) - ord('A') + 27
    else:
        raise Exception("Character out of range!")

with open("input3.txt") as f:
    total_priority = 0
    line = 0
    badges = []
    group_shared_items = set()
    while True:
        l = f.readline()
        if l == "":
            break
        fullcontents = l.strip()
        compartment1 = fullcontents[:len(fullcontents)//2]
        compartment2  =fullcontents[len(fullcontents)//2:]
        shareditems = set()
        if line%3 == 0:
            if group_shared_items:
                badge = group_shared_items.pop()
                badges.append(badge)
                print(f"This group has badge {badge}.")
            group_shared_items = set(list(fullcontents))
        else:
            group_shared_items &= set(list(fullcontents))
        for c in compartment1:
            if c in compartment2:
                shareditems.add(c)
        for c in shareditems:
            total_priority += priority(c)
        print(f"Compartments are {compartment1} and {compartment2}, sharing {shareditems}.")
        line += 1
    print(f"Total priority: {total_priority}.")
    if group_shared_items:
        badges.append(group_shared_items.pop())
    badge_score = sum([priority(b) for b in badges])
    print(f"Badges: {badges}, giving priority {badge_score}.")
