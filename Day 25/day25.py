import random
from itertools import product
from copy import deepcopy

def read_input(filename):
    connections = []
    with open(filename, "r") as filein:
        for line in filein.read().split("\n"):
            token1, token2 = line.split(": ")
            for module in token2.split():
                connections.append(frozenset((token1, module)))
    modules = {module for connection in connections for module in connection}
    return modules, connections

def create_mapping(modules, connections):
    """Create a dictionary that takes a module and returns all the modules it's connected to."""
    # Dont end up using this: (for a module, show all connections involving it)
    # module_connections = {module: {connection for connection in connections if module in connection} for module in modules}
    module_module_map = {module: {m for m in modules if frozenset((m, module)) in connections} for module in modules}
    return module_module_map

def add_connection(module_module_map, connection):
    first, second = connection
    module_module_map[first].add(second)
    module_module_map[second].add(first)
    return module_module_map

def remove_connection(module_module_map, connection):
    first, second = connection
    module_module_map[first].remove(second)
    module_module_map[second].remove(first)
    return module_module_map

modules, connections = read_input("input.txt")
module_module_map = create_mapping(modules, connections)

# This seems to be an existing problem in graph theory, the minimum cut problem: https://en.wikipedia.org/wiki/Minimum_cut
# Start with the stochastic choice (Karger's algorith: https://en.wikipedia.org/wiki/Karger%27s_algorithm),
# and try running it a bunch until we hit 3 cuts

def flatten(nest):
    if isinstance(nest, str):
        return {nest}
    x, y = nest
    if isinstance(x, str) and isinstance(y, str):
        return {x, y}
    else:
        return flatten(x) | flatten(y) 

def find_cuts(nodes1, nodes2, connections):
    potential_cuts = {frozenset((node1, node2)) for node1, node2 in product(nodes1, nodes2)}
    return potential_cuts.intersection(connections)


def kargers_algorithm(module_module_map, connections):
    module_module_map = deepcopy(module_module_map)
    while len(module_module_map) > 2:
        # pick an edge at random to contract
        first = random.choice(list(module_module_map.keys()))
        second = module_module_map[first].pop()
        edge = frozenset((first, second))

        module_module_map[edge] = (module_module_map[first] | module_module_map[second]) - edge
        del module_module_map[first]
        del module_module_map[second]
        for vertex in module_module_map[edge]:
            module_module_map[vertex] -= edge
            module_module_map[vertex].add(edge)

    group1, group2 = tuple(map(flatten, module_module_map.keys()))

    return find_cuts(group1, group2, connections), group1, group2


# Might also want to investigate the Minimum Spanning Tree of the graph? See if that tells us anything about where to make cuts
# "if all the edge weights of a given graph are the same, then every spanning tree of that graph is minimum." might mean it doesn't help

# def spanning_tree(module_module_map):
#     module_module_map = {module: list(connected) for module, connected in module_module_map.items()}
#     N = len(module_module_map)
#     start = random.choice(tuple(module_module_map.keys()))
#     paths = [[start]]

#     while paths:
#         path = paths.pop()
#         for potential_node in module_module_map[path[-1]]:
#             if potential_node not in path:
#                 path.append(potential_node)
#                 if len(path) == N:
#                     return path, [len(module_module_map[node]) for node in path]
#                 paths.append(path)

# print(spanning_tree(module_module_map))
cuts, group1, group2 = kargers_algorithm(module_module_map, connections)
while len(cuts) > 3:
    cuts, group1, group2 = kargers_algorithm(module_module_map, connections)
    print(len(cuts))

sizes_total = len(group1) * len(group2)
print(f"The product of sizes is {sizes_total}")

# Results = {frozenset({'vfj', 'nvg'}), frozenset({'sqh', 'jbz'}), frozenset({'fch', 'fvh'})}