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
from itertools import product
from functools import cache
from collections import defaultdict

def read_input(filename):
    with open(filename, "r") as filein:
        return [[int(heat) for heat in line] for line in filein.read().split("\n")]

heat_cost = read_input("input.txt")
N, M = len(heat_cost), len(heat_cost[0])

class Node(NamedTuple):
    """x, y are the coordinates. z is a list of the last three steps."""
    x: int
    y: int
    z: tuple

def heuristic(neighbour: Node, N=N, M=M):
    return 0

def generate_neighbours(node: Node, N: int, M: int):
    # In 2D, there are 4 neighbours: north, east, south, west
    # In 3D, also have a last turned and a direction to take into account.
    # However all this does is restrict the number of valid neighbours?
    # We cannot go north if we've gone north three times already
    x, y, z = node
    # neighbours = [(x + 1, y) if x < N-1 & (z < 2 | dx != 1) else None,
    #               (x - 1, y) if x > 0   & (z < 2 | dx !=-1) else None,
    #               (x, y + 1) if y < M-1 & (z < 2 | dy != 1) else None,
    #               (x, y - 1) if y > 0   & (z < 2 | dy !=-1) else None]

    #return [neighbour for neighbour in neighbours if neighbour]
    neighbours = []
    dx, dy = z[-1] if len(z) != 0 else (1, 1)
    if len(z) < 3:
        # We can just make any turn we want
        # Provided is doesn't take us off the edge
        # But also dont want to go back on ourselves
        neighbours = [Node(x+1, y, z + (( 1, 0),)) if x < N-1 and dx != -1 else None,
                      Node(x-1, y, z + ((-1, 0),)) if x > 0   and dx !=  1 else None,
                      Node(x, y+1, z + (( 0, 1),)) if y < M-1 and dy != -1 else None,
                      Node(x, y-1, z + (( 0,-1),)) if y > 0   and dy !=  1 else None
                      ]        
    elif len(set(z)) > 1:
        # print("Want to generate our neighbours")
        # We can just make any turn we want
        # Provided is doesn't take us off the edge
        # print(f"{x = }, {y = }, {N-1 = }, {M-1 = }")
        # print(f"{x < N-1 = }, {x > 0 = }, {y < M-1 = }, {y > 0 = }")
        neighbours = [Node(x+1, y, z[1:] + (( 1, 0),)) if x < N-1 and dx != -1 else None,
                      Node(x-1, y, z[1:] + ((-1, 0),)) if x > 0   and dx !=  1 else None,
                      Node(x, y+1, z[1:] + (( 0, 1),)) if y < M-1 and dy != -1 else None,
                      Node(x, y-1, z[1:] + (( 0,-1),)) if y > 0   and dy !=  1 else None
                      ]
    else:
        neighbours = [
            Node(x+1, y, z[1:] + (( 1, 0),)) if x < N-1 and abs(dy) else None,
            Node(x-1, y, z[1:] + ((-1, 0),)) if x > 0   and abs(dy) else None,
            Node(x, y+1, z[1:] + (( 0, 1),)) if y < M-1 and abs(dx) else None,
            Node(x, y-1, z[1:] + (( 0,-1),)) if y > 0   and abs(dx) else None
                      ]
    return [neighbour for neighbour in neighbours if neighbour]

start = Node(0, 0, tuple())
total_cost = defaultdict(lambda: inf, {start: 0})
previous_node = {}
end = (N-1, M-1)

queue = [(0, start)]
heapq.heapify(queue)
visited = set()
# for i in range(100):
while queue:
    _, node = heapq.heappop(queue)
    # print(len(queue))
    # print(f"{node = }, {_ = } {max(total_cost.values()) = }")
    if node[:2] == end:
        # print("Found end:")
        # for neighbour in generate_neighbours(node, N, M):
            # print(f"\t{neighbour = }")
        break
    if node in visited:
        # print("Visited node")
        continue
    for neighbour in generate_neighbours(node, N, M):
        # print(f"\t{neighbour = }")
        if neighbour in visited:
            # print("\t\tVisited neighbour")
            continue
        new_total = heat_cost[neighbour.x][neighbour.y] + total_cost[node]
        if new_total < total_cost[neighbour]:
            total_cost[neighbour] = new_total
            previous_node[neighbour] = node
        heapq.heappush(queue, (total_cost[neighbour]+heuristic(neighbour), neighbour))
    visited.add(node)
# else:
    # print("Ran out of nodes in queue")
print(f"{node = }, {total_cost[node] = }")
# final_nodes = {total_cost[node]: node for node in nodes if not node and total_cost[node] is not inf}
# print(final_nodes)
# final_node = final_nodes[min(final_nodes)]
final_node = node

path = [final_node]
while True:
    try:
        path.append(previous_node[path[-1]])
    except KeyError:
        break
print(*path, sep="\n")

simple_path = [node[:2] for node in path]

print("\n".join(["".join(map(str, ["*" if (i, j) in simple_path else heat_cost[i][j] for j in range(M)])) for i in range(N)]))