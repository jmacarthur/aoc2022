#!/usr/bin/env python3

import sys

lines = []

with open(sys.argv[1]) as f:
    while True:
        l = f.readline()
        if l == "": break
        lines.append(l.split())

print(lines)

class Directory():
    def __init__(self):
        self.entries = {}
        self.parent = None
    def dump(self, indent):
        for (k,v) in self.entries.items():
            if type(v) == Directory:
                print(f"{indent}{k}: (size {v.size()})")
                v.dump(indent+"  ")
            else:
                print(f"{indent}{k} {v}")
    def size(self):
        total = 0
        for (k,v) in self.entries.items():
            if type(v) == Directory:
                total += v.size()
            elif type(v) == int:
                total += v
            else:
                raise Exception("Something that isn't a directory or file is in this directory.")
        return total
    def add_directory(self, dirname):
        if dirname not in self.entries:
            self.entries[dirname] = Directory()
            self.entries[dirname].parent = self
            self.size_cache = None
        return self.entries[dirname]
    def add_file(self, filename, filesize):
        self.entries[filename] = filesize

tld = Directory()
cwd = tld
alldirectories = []

for l in lines:
    print(f"Input line: {l}")
    if l[0] == '$':
        command = l[1]
        if command == 'cd':
            if l[2] == '/':
                cwd = tld
            elif l[2] == '..':
                if cwd.parent:
                    cwd = cwd.parent
            else:
                if l[2] in cwd.entries:
                    cwd = cwd.entries[l[2]]
                else:
                    print(f"Create new directory {l[2]}")
                    cwd = cwd.add_directory(l[2])
                    alldirectories.append(cwd)
    elif l[0] == 'dir':
        # Make sure directory exists but don't change to it
        print(f"Create new directory {l[1]}")
        if l[1] not in cwd.entries:
            newdir = cwd.add_directory(l[1])
            alldirectories.append(newdir)
    else:
        """ Must be a file at this point """
        filesize = int(l[0])
        filename = l[1]
        cwd.add_file(filename, filesize)

tld.dump("..")

fullsize = tld.size()
freespace = 70000000 - fullsize
targetspace = 30000000
spaceneeded = targetspace - freespace

total = 0
deletion_candidate = None
for d in alldirectories:
    s = d.size()
    if(s <= 100000):
        total += s
    if(s >= spaceneeded):
        if deletion_candidate is None or deletion_candidate.size() > s:
            deletion_candidate = d
print(total)
print(f"{freespace} bytes free ({spaceneeded} must be freed for the update)")
print(f"Recommend {deletion_candidate} with {deletion_candidate.size()} bytes for deletion")


# 16727590 too high

# 996474 Too low


#What is lfrctthp? Multiple directories with one name!
