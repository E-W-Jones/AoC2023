"""
Each game consists of taking handfuls out of the bag
Each handful can be represented as a dictionary* of {colour: count} pairs
A game is a list of these handfuls
The games are stored in another dictionary, keyed by the game ID.

Instead of dictionaries, use default dictionary, returning 0 for colours we havent seen before.
"""
from math import prod
from collections import defaultdict

def read_game(line):
    ID_string, game_string = line.rstrip("\n").split(":")
    ID = int(ID_string[5:])
    game = []
    for handful_string in game_string.split(";"):
        handful = defaultdict(int)
        for pair in handful_string.split(","):
            N, colour = pair.split()
            handful[colour] = int(N)
        game.append(handful)
    return ID, game

def read_input():
    games = {}
    with open("input.txt", "r") as filein:
        for line in filein.readlines():
            ID, game = read_game(line)
            games[ID] = game
    return games

def handful_is_valid(content, handful):
    for colour in handful:
        if handful[colour] > content[colour]:
            return False
    return True

def game_is_valid(content, game):
    for handful in game:
        if not handful_is_valid(content, handful):
            return False
    return True

def filter_by_valid(content, games):
    return {ID: game for ID, game in games.items() if game_is_valid(content, game)}

def task1():
    # Told bag contains 12 red cubes, 13 green cubes, and 14 blue cubes
    content = defaultdict(int, {"red": 12,
                                "green": 13,
                                "blue": 14})
    games = read_input()
    valid_games = filter_by_valid(content, games)
    IDs = valid_games.keys()
    print(f"The sum of IDs for possible games is {sum(IDs)}")

def power(game):
    content = defaultdict(int)
    for handful in game:
        for colour in handful:
            if content[colour] < handful[colour]:
                content[colour] = handful[colour]
    return prod(content.values())

def task2():
    games = read_input()
    powers = [power(game) for game in games.values()]
    print(f"The sum of powers for all games is {sum(powers)}")

if __name__ == "__main__":
    task1()
    task2()
