#!/usr/bin/env python3

import sys

monkeys = {}

class Monkey():
    def __init__(self):
        self.value = None
        self.op = None
        self.arg1 = None
        self.arg2 = None
    def set_value(self, value):
        self.value = value
    def set_calculation(self, arg1, op, arg2):
        self.arg1 = arg1
        self.op = op
        self.arg2 = arg2
    def do_calculation(self, arg1v, arg2v):
        if self.op == '+':
            return arg1v+arg2v
        elif self.op == '*':
            return arg1v*arg2v
        elif self.op == '-':
            return arg1v-arg2v
        elif self.op == '/':
            return arg1v//arg2v
        else:
            print(f"Unrecognised op {self.op}")
            sys.exit(1)

humn_ref_count = 0

with open(sys.argv[1]) as f:
    for l in f.readlines():
        fields = l.strip().split(': ')
        equation_fields = fields[1].split()
        m = Monkey()
        if len(equation_fields)>1:
            m.set_calculation(equation_fields[0], equation_fields[1], equation_fields[2])
            if equation_fields[0] == 'humn':
                humn_ref_count += 1
            if equation_fields[2] == 'humn':
                humn_ref_count += 1
        else:
            m.set_value(int(fields[1]))
        monkeys[fields[0]] = m

def solve(monkey_name, monkeys):
    m = monkeys[monkey_name]
    if m.op:
        arg1 = solve(m.arg1, monkeys)
        arg2 = solve(m.arg2, monkeys)
        return m.do_calculation(arg1, arg2)
    else:
        return m.value

print(f"Value of root for part 1: {solve('root', monkeys)}")

# Check humn is referred to only once; if it's more than this, our
# binary chop later won't work.
assert humn_ref_count == 1

high_value = 1

def solve2(monkeys, value, test):
    monkeys['humn'].value = value
    v1 = solve(monkeys['root'].arg1, monkeys)
    v2 = solve(monkeys['root'].arg2, monkeys)
    return test(v1,v2)

def find_initial_value(monkeys, test):
    # We only consider positive values for starting values here, since
    # there were no negative or zero values in the input set.
    value = 1
    while True:
        if solve2(monkeys, value, test):
            return value
        else:
            value *= 10

if len(sys.argv)>2:
    # If a number was supplied on the command line, substitute this for humn's value and show the final comparison.
    monkeys['humn'].set_value(int(sys.argv[2]))
    v1 = solve(monkeys['root'].arg1, monkeys)
    v2 = solve(monkeys['root'].arg2, monkeys)
    print(f"{v1} == {v2}?")
else:
    # If no number was supplied on the command line, perform a binary chop.
    high_value = find_initial_value(monkeys, lambda a,b: a>b)
    low_value = find_initial_value(monkeys, lambda a,b: a<b)

    while abs(low_value - high_value)>1:
        mid_value = (high_value+low_value)//2
        if solve2(monkeys, mid_value, lambda a,b: a<b):
            low_value = mid_value
        else:
            high_value = mid_value

    if solve2(monkeys, low_value, lambda a,b: a==b):
        print(f"Day 2: Humn should shout {low_value}")
    elif solve2(monkeys, high_value, lambda a,b: a==b):
        print(f"Day 2: Humn should shout {high_value}")

