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

# Copy the instructions several times, to ensure the instruction length is divisible by the number of pieces.
instructions *= len(piece_sources)

pieces = []
for (n,p) in enumerate(piece_sources, 1):
    g = Grid(len(p[0]), len(p))
    for (row, line) in enumerate(p):
        for (col, char) in enumerate(line):
            g.set(col, row, char)
    g.ident = n
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

# Various hashes which keep track of repeating loops.
faultlines = {}
repeating_units = {}
piece_count_at_instruction = {}

print(f"Instruction line is {len(instructions)} characters long.")

# Replace this with 2022 for part 1.
piece_count = 1000000000000

while piece_count > 0:
    current_piece = pieces[next_piece_no% len(pieces)]
    piece_count -= 1
    next_piece_no += 1
    xpos = 2
    ypos = 0
    if piece_count % 1000==0:
        print(f"{piece_count} pieces remaining")
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
            # Piece tries to move horizontally, but is blocked.
            pass
        else:
            xpos += dx

        # Now try to move down
        if collides(arena, current_piece, xpos, ypos+1):
            # Piece tries to move down, but is blocked.
            solidify(arena, current_piece, xpos, ypos)

            if ypos == 3:
                # If we landed at ypos 3, then no part of our piece entered a partially occupied line; we call this a
                # fault line because you can draw a complete horizontal line which does not divide any piece.

                # TODO: This doesn't mean the next piece can't drop in under where this one lands. I seem to get away with it
                # for my input, but I might just be lucky.
                if instruction_position in faultlines:
                    # If we already saw a faultline at this instruction position, it's possible we're in a repeating loop.
                    pattern_length = len(arena) - find_first_occupied_line(arena) + removed_lines - faultlines[instruction_position]
                    if instruction_position in repeating_units and repeating_units[instruction_position] == pattern_length:
                        skip_blocks = piece_count // pattern_length
                        piece_count_diff = piece_count_at_instruction[instruction_position] - piece_count
                        print(f"Skip forward {skip_blocks} blocks; of {pattern_length} height and {piece_count_diff} pieces")
                        piece_count -= skip_blocks * piece_count_diff
                        removed_lines += skip_blocks * pattern_length

                        # Clear everything out and start again. This might not be necessary.
                        repeating_units = {}
                        piece_count_at_instuction = {}
                        faultlines = {}
                    else:
                        repeating_units[instruction_position] = pattern_length
                        piece_count_at_instruction[instruction_position] = piece_count
                # Record the total occupied length of the arena in the faultline hash.
                faultlines[instruction_position] = len(arena) - find_first_occupied_line(arena) + removed_lines
            break
        else:
            # Piece moves down normally.
            ypos += 1

# Print arena
for l in arena:
    print("|" + "".join(l) + "|")
print(f"+ {removed_lines} removed lines")

first_occupied_line = find_first_occupied_line(arena)
dist = len(arena)-first_occupied_line
print(dist + removed_lines)
