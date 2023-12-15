# This day was a mess...

def generate_neighbours(indexes):
    def neighbours(i, j):
        return [(i+di, j+dj) for di, dj in indexes]
    return neighbours

NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)
valid_neighbours = {
    "|": generate_neighbours((NORTH, SOUTH)),
    "-": generate_neighbours((EAST, WEST)),
    "L": generate_neighbours((NORTH, EAST)),
    "J": generate_neighbours((NORTH, WEST)),
    "7": generate_neighbours((SOUTH, WEST)),
    "F": generate_neighbours((SOUTH, EAST))
}

def find_start(maze):
    for i, row in enumerate(maze):
        for j, pipe in enumerate(row):
            if pipe == "S":
                return i, j

def generate_path(maze):
    start = find_start(maze)
    path = [start]
    # There is only one shape, we can just iterate through the 4 neighbours until we see any that match up
    i, j = start
    if maze[i-1][j] in "|7F":
        i -= 1
    elif maze[i+1][j] in "|LJ":
        i += 1
    elif maze[i][j+1] in "-7J":
        j += 1
    elif maze[i][j-1] in "-FL":
        j -= 1
    path.append((i, j))

    while path[-1] != start:
        i_old, j_old = i, j
        previous = path[-2]
        for i, j in valid_neighbours[maze[i_old][j_old]](i_old, j_old):
            if (i == previous[0]) and (j == previous[1]):
                continue
            else:
                path.append((i, j))
                break
    return path

def is_enclosed(sub_string):
    no_pipes = sub_string.count("|")
    no_LJ = no_L7 = no_F7 = no_FJ = 0
    L = F = False
    for char in sub_string:
        if char == 'L':
            L = True
        elif char == 'F':
            F = True
        elif char == 'J':
            if L:
                no_LJ += 1
                L = False
            elif F:
                no_FJ += 1
                F = False
        elif char == '7':
            if L:
                no_L7 += 1
                L = False
            elif F:
                no_F7 += 1
                F = False
    return (no_pipes + no_L7 + no_FJ) % 2 == 1

def main():
    # Generate the maze:
    #    This will be a list of indexes, starting at the start
    #    To generate, get the valid neighbours of a pipe, choose the one we've not just come from
    #    Add this to the list, check the next neighbour
    # --- Task 1 ---
    with open("input.txt", "r") as filein:
        maze = [list(line.rstrip("\n")) for line in filein.readlines()]
    
    path = generate_path(maze)
    print(f"The furthest point is {len(path) // 2} away")

    # --- Task 2 ---
    # We want an even number of pipes
    # And an even number of L/F + J/7 pairs?
    # So! count the number of |
    # Count the number of LJ pairs - these do count
    # Count the number of L7 pairs - these don't count
    # Count the number of FJ pairs - these do count
    # Count the number of F7 pairs - these don't count
    # To be enclosed:
    #     no. | + no. L7 + no. FJ is odd
    maze = [["." if (i, j) not in path else pipe for j, pipe in enumerate(row)] for i, row in enumerate(maze)]
    # I know for my input, S should be an L: could try this programatically
    maze[path[0][0]][path[0][1]] = "L"
    count = 0
    for i, row in enumerate(maze):
        for j, pipe in enumerate(row):
            if (i, j) in path:
                continue
            if is_enclosed(row[:j]):
                count += 1

    print(f"{count} points are enclosed")


if __name__ == "__main__":
    main()
