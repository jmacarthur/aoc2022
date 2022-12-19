#!/usr/bin/env python3
from copy import deepcopy
import sys

blueprints = []

with open(sys.argv[1]) as f:
    for l in f.readlines():
        recipes = l.strip().split(": ")[1].strip().split('.')
        print(recipes)
        blueprint = {}
        for r in recipes:
            if r:
                fields = r.split()
                result = fields[1]
                ingredient_string = " ".join(fields[4:])
                ingredients = []
                print(f"Ingredients: {ingredient_string}")
                ingredient_strings = ingredient_string.split(" and ")
                for i in ingredient_strings:
                    f = i.split()
                    ingredients.append((int(f[0]), f[1]))
                    print(result, ingredients)
                blueprint[result] = ingredients
        blueprints.append(blueprint)


blueprint = blueprints[0]
stock = { 'ore': 0, 'clay': 0, 'obsidian': 0 }
robots = { 'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0 }
def complete_run(minutes_remaining, stock, robots):
    if minutes_remaining == 0:
        return 0
    if minutes_remaining > 7:
        print(f"With {minutes_remaining} minutes remaining, we have {stock} and {robots}")

    # Build new robots
    most_geodes = -1
    ideal_build = None
    updated_stock = deepcopy(stock)
    # Generate stocks from robots
    for stocktype in ['ore', 'clay', 'obsidian']:
        updated_stock[stocktype] = stock[stocktype] + robots[stocktype]

    if minutes_remaining > 1:
        for (build_result,v) in blueprint.items():
            # Making one robot?
            new_stock = deepcopy(updated_stock)
            new_robots = deepcopy(robots)
            for (amount,ingredient) in v:
                if stock[ingredient] < amount:
                    break
                new_stock[ingredient] -= amount
                new_robots[build_result] += 1

            g = complete_run(minutes_remaining-1, new_stock, new_robots)
            if g > most_geodes:
                ideal_build = build_result
                most_geodes = g

    new_stock = deepcopy(stock)
    new_robots = deepcopy(robots)
    no_build_geodes = complete_run(minutes_remaining-1, new_stock, new_robots)
    if no_build_geodes > most_geodes:
        #print(f"Do not build anything on rem.minute {minutes_remaining}")
        return no_build_geodes + robots['geode']
    else:
        #print(f"Build {ideal_build} robot on rem.minute {minutes_remaining}")
        return most_geodes + robots['geode']


geodes = complete_run(24, stock, robots)
print(f"On this blueprint: {geodes} geodes.")

# We have to make as many geode robots as possible, as quick as possible.
"""
We know we must make one geode robot as soon as possible. Then, we have to make another one as soon as possible.

So, we must make one obsidian robot asap; and therefore one clay robot asap; whether we make another ore robot is undecided. So we must wait at least until minute 2, and then depending on the blueprint, we can make another ore robot or a clay robot. 

E.g. blueprint 1; if we rush it, we get:

Build clay robot during minute 3.

1 clay at end of minute 4, hence 8 clay by the end of minute 11. By then, we also have 9 ore.

Build obsidian robot during minute 12. At end of minute 12, we have 7 ore.

1 obsidian at end of minute 13, hence 7 obsidian by end of minute 19. We will have plenty of ore. Build geode robot during minute 20; then, we have turns 21, 22, 23, 24 to collect geodes (4). Not optimal!
 
Instead, we could build more obsidian robots, which makes it quicker to build geode robots. 


you can create a max of one robot per turn, so there are  3**24 (282 429 536 481) options here, and not all of them are valid. No blueprint allows the construction of any robot until minute 3, for example.


"""
