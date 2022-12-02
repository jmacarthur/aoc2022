#!/usr/bin/env python3

inputmap = {
    "A": "Rock",
    "B": "Paper",
    "C": "Scissors",
    "X": "Rock",
    "Y": "Paper",
    "Z": "Scissors"
}

strategymap = {
    "X": "Lose",
    "Y": "Draw",
    "Z": "Win"
}

strategyplay = {
    ("Rock", "Win"): "Paper",
    ("Rock", "Lose"): "Scissors",
    ("Rock", "Draw"): "Rock",
    ("Scissors", "Win"): "Rock",
    ("Scissors", "Lose"): "Paper",
    ("Scissors", "Draw"): "Scissors",
    ("Paper", "Win"): "Scissors",
    ("Paper", "Lose"): "Rock",
    ("Paper", "Draw"): "Paper"
}
scores = {
    "Rock": 1,
    "Paper": 2,
    "Scissors": 3
}

roundscores = {
    ("Rock", "Paper"): 0,
    ("Rock", "Rock"): 3,
    ("Rock", "Scissors"): 6,

    ("Paper", "Paper"): 3,
    ("Paper", "Rock"): 6,
    ("Paper", "Scissors"): 0,

    ("Scissors", "Paper"): 6,
    ("Scissors", "Rock"): 0,
    ("Scissors", "Scissors"): 3
}

# Run both parts, one after the other
playerscore = 0
with open("input2.txt") as f:
    while True:
        l = f.readline()
        if l == "":
            break
        fields = l.split()
        opponent = inputmap[fields[0]]
        player = inputmap[fields[1]]
        playerscore += scores[player] + roundscores[(player, opponent)]
print("Part 1 score:", playerscore)

playerscore = 0
with open("input2.txt") as f:
    while True:
        l = f.readline()
        if l == "":
            break
        fields = l.split()
        opponent = inputmap[fields[0]]
        strategy = strategymap[fields[1]]
        player = strategyplay[(opponent, strategy)]
        playerscore += scores[player] + roundscores[(player, opponent)]
print("Part 2 score:", playerscore)
