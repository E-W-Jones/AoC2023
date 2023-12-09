from math import prod

def read_input():
    with open("input.txt", "r") as filein:
        times = filein.readline().strip("Time: \n").split()
        distances = filein.readline().strip("Distance: \n").split()
    return [(int(time), int(distance)) for time, distance in zip(times, distances)]

def wins(time, max_distance):
    return sum([t*(time-t) > max_distance for t in range(time)])

def task1():
    races = read_input()
    ways_to_win = [wins(time, max_distance) for time, max_distance in races]
    print(f"The product of ways to win is {prod(ways_to_win)}")

def task2():
    with open("input.txt", "r") as filein:
        time = filein.readline().strip("Time: \n").split()
        distance = filein.readline().strip("Distance: \n").split()
    time = int("".join(time))
    distance = int("".join(distance))
    print(f"There are {wins(time, distance)} ways to win")

if __name__ == "__main__":
    task1()
    task2()