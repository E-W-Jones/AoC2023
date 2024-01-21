from math import inf
from itertools import pairwise

def read_input(filename):
    direction, length, colour = [], [], []
    with open(filename, "r") as filein:
        for line in filein.read().split("\n"):
            d, l, c = line.split()
            direction.append(d)
            length.append(int(l))
            colour.append(c)
    return direction, length, colour

def dig_up(path, length):
    # Up DEcrements the FIRST index
    x, y = path[-1]
    for dx in range(1, length + 1):
        path.append((x - dx, y))

def dig_down(path, length):
    # Down INcrements the FIRST index
    x, y = path[-1]
    for dx in range(1, length + 1):
        path.append((x + dx, y))

def dig_left(path, length):
    # Left DEcrements the SECOND index
    x, y = path[-1]
    for dy in range(1, length + 1):
        path.append((x, y - dy))

def dig_right(path, length):
    # Right INcrements the SECOND index
    x, y = path[-1]
    for dy in range(1, length + 1):
        path.append((x, y + dy))

def dig_trenches(directions, lengths):
    path = [(0, 0)]
    for direction, length in zip(directions, lengths):
        match direction:
            case "U":
                dig_up(path, length)
            case "D":
                dig_down(path, length)
            case "L":
                dig_left(path, length)
            case "R":
                dig_right(path, length)
            case other:
                raise ValueError(f"Invalid value of {direction = }")
    return path

def flood_fill(path):
    filled = set(path)
    # Want to do a flood fill
    # Take a point inside the path:
    # Generate the 4 neighours:
    # If they haven't yet been flood-filled, fill them
    to_fill = [(1, 1)]  # This won't always work
    while to_fill:
        node = to_fill.pop()
        if node in filled:
            continue
        x, y = node
        neighbours = (x+1, y), (x-1, y), (x, y-1), (x, y+1)
        for neighbour in neighbours:
            if neighbour in filled:
                continue
            else:
                to_fill.append(neighbour)
        filled.add(node)
    return filled

def find_limits(path):
    min_x = min_y = inf
    max_x = max_y = 0
    for x, y in path:
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        elif y > max_y:
            max_y = y
    return min_x, max_x, min_y, max_y

def print_path(path, save="output.txt"):
    # Work out the boundaries
    min_x, max_x, min_y, max_y = find_limits(path)

    N = max_x - min_x
    M = max_y - min_y
    out_string = "\n".join(["".join(["#" if (x, y) in path else "." for y in range(min_y, max_y+1)]) for x in range(min_x, max_x+1)])
    if save:  # Can't print the ascii on my screen, it's too wide
        with open(save, "w") as fileout:
            fileout.write(out_string)
    print(out_string)

def find_vertices(directions, lengths):
    vertices = [(0, 0)]
    for direction, length in zip(directions, lengths):
        x, y = vertices[-1]
        match direction:
            case "U":
                x -= length
            case "D":
                x += length
            case "L":
                y -= length
            case "R":
                y += length
            case other:
                raise ValueError(f"Invalid value of {direction = }")
        vertices.append((x, y))
    return vertices

def find_vertices_hex(colours):
    vertices = [(0, 0)]
    lengths = []
    for colour in colours:
        x, y = vertices[-1]
        length = int(colour[2:-2], base=16)
        direction = colour[-2]
        match direction:
            case "3":
                x -= length
            case "1":
                x += length
            case "2":
                y -= length
            case "0":
                y += length
            case other:
                raise ValueError(f"Invalid value of {direction = }")
        vertices.append((x, y))
        lengths.append(length)
    return vertices, lengths

def area(vertices):
    """
    Calculate the area of a polygon given its vertices.
    
    https://en.wikipedia.org/wiki/Polygon#Area
    """
    return abs(sum((x1-x2)*(y1+y2) for (x1, y1), (x2, y2) in pairwise(vertices))) / 2
    return abs(sum(x1*y2 - x2*y1 for (x1, y1), (x2, y2) in pairwise(vertices))) / 2

def volume(*args):
    """
    Use the arithmetic area and Pick's Theorem to calculate the volume.

    https://en.wikipedia.org/wiki/Pick%27s_theorem
    """
    if len(args) == 2:
        directions, lengths = args
        vertices = find_vertices(directions, lengths)
    elif len(args) == 1:
        colours, = args
        vertices, lengths = find_vertices_hex(colours)
    else:
        ValueError(f"volume takes 1 or 2 arguments ({len(args)} given)")
    
    A = area(vertices)
    b = sum(lengths)
    i = A + 1 - b/2
    return int(i + b)

def main():
    directions, lengths, colours = read_input("input.txt")
    # --- Task 1 ---
    # path = dig_trenches(directions, lengths)
    # hole = flood_fill(path)
    # print(f"The total volume is {len(hole)} m^3")
    print(f"The total volume is {volume(directions, lengths)} m^3")
    # --- Task 2 ---
    # For task 2 we run out of memory trying to hold all the points,
    # so instead we record the vertices, and get the area mathematically
    # Less fun, but definitely faster
    print(f"The total volume is {volume(colours)} m^3")

if __name__ == "__main__":
    main()