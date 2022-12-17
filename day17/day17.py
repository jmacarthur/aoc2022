#!/usr/bin/env python3

import sys

class Grid():
    def __init__(self, width, height):
        self.grid = [['.']* width for y in range(height)]
        self.width = width
        self.height = height

    def get(self, x, y):
        if x<0 or y<0 or x>=self.width or y>=self.height:
            return None
        return self.grid[y][x]

    def set(self, x, y, char):
        if x<0 or y<0 or x>=self.width or y>=self.height:
            return
        self.grid[y][x] = char

with open(sys.argv[1]) as f:
    instructions = f.readline().strip()

# Copy the instructions four times. This ensures the length is divisible by 5.
instructions *= 5

piece_sources = [ [ "####" ],
                  [ ".#.",
                    "###",
                    ".#." ],
                  [ "..#",
                    "..#",
                    "###" ],
                  [ "#",
                    "#",
                    "#",
                    "#" ],
                  [ "##",
                    "##" ] ]

pieces = []
for p in piece_sources:
    g = Grid(len(p[0]), len(p))
    for (row, line) in enumerate(p):
        for (col, char) in enumerate(line):
            g.set(col, row, char)
    pieces.append(g)

def collides(arena, current_piece, xpos, ypos):
    for dy in range(0, current_piece.height):
        if ypos+dy < 0 or ypos + dy >= len(arena):
            return True
        for dx in range(0, current_piece.width):
            if xpos+dx < 0 or xpos + dx >= 7:
                return True
            if arena[ypos+dy][xpos+dx] == '#' and current_piece.get(dx, dy) == '#':
                return True
    return False

def solidify(arena, current_piece, xpos, ypos):
    # There's no range checks on this!
    #print(f"Solidifying piece!")
    for dy in range(0, current_piece.height):
        for dx in range(0, current_piece.width):
            if current_piece.get(dx, dy) == '#':
                arena[ypos+dy][xpos+dx] = '#'

arena = [ ['.']*7 ]

def find_first_occupied_line(arena):
    for (n,l) in enumerate(arena):
        if not all([c=='.' for c in l]):
            # Non-empty line
            return n
    else:
        return len(arena)

next_piece_no = 0
instruction_position = 0
removed_lines = 0
print(f"Instruction line is {len(instructions)} characters long.")
for p in range(0,2022):
    current_piece = pieces[next_piece_no% len(pieces)]
    next_piece_no += 1
    xpos = 2
    ypos = 0
    if p % 1000==0:
        print(f"Iteration {p}")
    # Scan for a complete line and remove everything after it, but retain the count
    for (n,l) in enumerate(arena):
        if all([c=='#' for c in l]):
            removed_lines += (len(arena)-n)
            arena = arena[:n]

    # Scan for the highest blank line (and increase arena size if necessary)
    first_occupied_line = find_first_occupied_line(arena)

    while first_occupied_line < 3 + current_piece.height:
        arena.insert(0, ['.']*7)
        first_occupied_line += 1

    ypos = first_occupied_line - current_piece.height - 3

    while True:
       # First, push left or right
       instruction = instructions[instruction_position]
       instruction_position = (instruction_position+1) % len(instructions)
       dx = -1 if instruction=='<' else 1
       if collides(arena, current_piece, xpos+dx, ypos):
           pass
           #print(f"Piece tries to move by {dx}, but is blocked")
       else:
           xpos += dx
           #print(f"Piece moves by {dx} to {xpos}")
       if collides(arena, current_piece, xpos, ypos+1):
           #print(f"Piece tries to move down, but is blocked")
           solidify(arena, current_piece, xpos, ypos)
           if ypos == 3:
               print(f"Piece lands on a fault line after instruction {instruction_position}")
           break
       else:
           ypos += 1
           #print(f"Piece moves down")

# Print arena
for l in arena:
    print("|" + "".join(l) + "|")

first_occupied_line = find_first_occupied_line(arena)
dist = len(arena)-first_occupied_line
print(dist + removed_lines)
