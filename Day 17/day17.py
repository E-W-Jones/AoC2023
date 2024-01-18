"""
I wanna try having a tuple of x, y values for each node
Then an array (actually tuples for immutability) we index for the cost
Then an array we index/update for total cost

Can have a function that generates neighbours - Or actually even another array? Idk I might wanna cache it anyway

And at some point we can even flatten it!! But don't think too hard and idk if there's even any benefit to that
"""
from typing import NamedTuple
import heapq
from math import inf

def read_input(filename):
    with open(filename, "r") as filein:
        return [[int(heat) for heat in line] for line in filein.read().split("\n")]

def generate_neighbours(x: int, y: int, N: int, M: int):
    # In 2D, there are 4 neighbours: north, east, south, west
    neighbours = [(x + 1, y) if x < N-1 else None,
                  (x - 1, y) if x > 0   else None,
                  (x, y + 1) if y < M-1 else None,
                  (x, y - 1) if y > 0   else None]
    return [neighbour for neighbour in neighbours if neighbour]

class Node(NamedTuple):
    x: int
    y: int
    end: bool

    def __bool__(self):
        return not self.end

heat_cost = read_input("sample_input.txt")
N, M = len(heat_cost), len(heat_cost[0])
nodes = [Node(i, j, i==N-1 & j==M-1) for i in range(N) for j in range(M)]
neighbours = [[generate_neighbours(i, j, N, M) for j in range(M)] for i in range(N)]
total_cost = [[inf if i|j else 0 for j in range(M)] for i in range(N)]

queue = [(total_cost[node.x][node.y], node) for node in nodes]
# Currently don't even need to use the priority queue
heapq.heapify(queue)

while node:=heapq.heappop(queue)[1]:
    for i, j in neighbours[node.x][node.y]:
        total_cost[i][j] = min(total_cost[i][j], heat_cost[i][j] + total_cost[node.x][node.y])

print(total_cost)