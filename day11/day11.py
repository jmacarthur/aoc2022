#!/usr/bin/env python3
import sys
from primefac import primefac
import functools

class Item():
    def __init__(self, worry=0):
        self.worry = worry
        self.remainders = {}
    def __str__(self):
        return str(self.worry)
    def __repr__(self):
        return str(self.worry)

def evaluate(operation, old_value):
    """ If you're certain about the inputs, you could use eval() here instead, but it's a bad habit to get into. """
    fields = operation.split()
    if fields[1] == '+':
        return old_value + int(fields[2])
    elif fields[1] == '*':
        if fields[2] == 'old':
            return old_value * old_value
        else:
            return old_value * int(fields[2])

class Monkey():
    def __init__(self):
        self.items = []
        self.operation = None
        self.divisor = None
        self.false_destination = None
        self.true_destination = None
        self.inspection_count = 0
        self.index = None
    def __str__(self):
        return f"Monkey {self.index} with items {self.items}, operation {self.operation}, divisor {self.divisor}, false to {self.false_destination}, true to {self.true_destination}, has inspected things {self.inspection_count} times"
    def inspect(self, item):
        self.inspection_count += 1
        new_worry = evaluate(self.operation, item.worry)
        item.worry = new_worry
        print(f"After inspection, the worry level is {item.worry}")

monkey = None
monkeys = []
divisors = []
with open(sys.argv[1]) as f:
    for l in f.readlines():
        fields = l.strip().split()
        if not fields:
            continue
        if fields[0] == "Monkey":
            monkey = Monkey()
            monkey.index = len(monkeys)
            monkeys.append(monkey)
        elif fields[0] == "Starting":
            for i in fields[2:]:
                monkey.items.append(Item(int(i.strip(","))))
        elif fields[0] == "Operation:":
            monkey.operation = (" ".join(fields[3:]))
        elif fields[0] == "Test:":
            monkey.divisor = int(fields[3])
            divisors.append(int(fields[-1]))
        elif fields[0] == "If":
            if fields[1] == "true:":
                monkey.true_destination = int(fields[5])
            elif fields[1] == "false:":
                monkey.false_destination = int(fields[5])
        else:
            print(f"Unrecognisable field {fields[0]}")

worry = 0
for r in range(0,10000):
    print(f"Round {r}.")
    for (index,m) in enumerate(monkeys):
        while m.items:
            i = m.items.pop(0)
            print(f"Monkey {index} inspects item {i}")
            m.inspect(i)
            i.worry = i.worry % 9699690
            #i.worry //= 3
            print(f"Worry is reduced to {i.worry}")
            if i.worry % m.divisor == 0:
                print(f"Item is divisible by {m.divisor}. Passing to {i.worry} to {m.true_destination}")
                monkeys[m.true_destination].items.append(i)
            else:
                print(f"Item is not divisible by {m.divisor}. Passing to {i.worry} to {m.false_destination}")
                monkeys[m.false_destination].items.append(i)

for m in sorted(monkeys, key = lambda x: x.inspection_count):
    print(m)
