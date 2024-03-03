from itertools import pairwise

PATH = '.'
FOREST = '#'
STEPS = UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
# A dictionary of character: step
SLOPES = {
    '^': UP,
    '>': RIGHT,
    'v': DOWN,
    '<': LEFT
}

def read_input(filename):
    with open(filename, 'r') as filein:
        return tuple(tuple(char for char in row) for row in filein.read().split('\n'))
        # return [[char for char in row] for row in filein.read().split('\n')]

def valid_step(x, y, dx, dy, path, trail_map):
    xp, yp = x + dx, y + dy
    try:
        char = trail_map[xp][yp]
    except IndexError:
        return False
    
    if (xp, yp) in path:
        return False
    elif char == PATH:
        return True
    elif char in SLOPES:
        i, j = SLOPES[char]
        if dx == -i and dy == -j:
            # You're trying to go uphill, but can't
            return False
        else:
            return True
    elif char == '#':
        return False
    else:
        raise ValueError("Something's gone wrong, or I've missed a case.")

def generate_valid_steps(path, trail_map):
    x, y = path[-1]
    char = trail_map[x][y]
    if char == PATH:
        # Terse list comprehension:
        #     for each step we could make up, down, left, or right:
        #         calculate the coordinates of the next point: xp, yp
        #         check it's not a forest, and we've not visited it yet
        #     return a list of these points
        return [(x + dx, y + dy) for (dx, dy) in STEPS if valid_step(x, y, dx, dy, path, trail_map)]
    elif char in SLOPES:
        # We can only move in that direction
        dx, dy = SLOPES[char]
        return [(x + dx, y + dy)]
    else:
        raise ValueError(f"{char} is not a valid location, should be one of {PATH, *SLOPES}.")

def find_splits(trail_map):
    splits = []
    N, M = len(trail_map), len(trail_map[0])
    for i in range(1, N-1):
        for j in range(1, M-1):
            if trail_map[i][j] == FOREST:
                continue
            if sum(trail_map[i + di][j + dj] != FOREST for di, dj in STEPS) > 2:
                splits.append((i, j))

    return splits

def AtoB(A, B, splits, trail_map):
    incomplete_paths = [[A]]

    while incomplete_paths:
        path = incomplete_paths.pop()
        for step in generate_valid_steps(path, trail_map):
            if step == B:
                return path + [step]
            elif step in splits:
                break
            else:
                incomplete_paths.append(path + [step])
    return []

def sub_path_lengths(splits, trail_map):
    sub_paths = {split: {} for split in splits}
    for A in splits:
        # There is symmetry in task 2, not task 1
        for B in splits:
            # Work out travelling from A to B, without hitting any other splits
            length = len(AtoB(A, B, splits, trail_map))
            if length > 0:
                sub_paths[A][B] = length - 1
    return sub_paths

def generate_paths(A, B, sub_paths):
    incomplete_paths = [[A]]
    complete_paths = []

    while incomplete_paths:
        path = incomplete_paths.pop()
        for next_split in sub_paths[path[-1]]:
            if next_split in path:
                continue
            if next_split == B:
                complete_paths.append(path + [next_split])
            else:
                incomplete_paths.append(path + [next_split])
    return complete_paths

def path_length(path, sub_paths):
    return sum(sub_paths[A][B] for A, B in pairwise(path))

def find_longest_path(start, finish, trail_map):
    # Split the paths into smaller `sub_paths` that go from one branching point to another
    splits = find_splits(trail_map)
    splits += [start, finish]
    # Find the lengths of these
    sub_paths = sub_path_lengths(splits, trail_map)
    # Add the sub_paths together and find the total path length, return the maximum
    return max(path_length(path, sub_paths) for path in generate_paths(start, finish, sub_paths))

def main():
    # --- Task 1 ---
    trail_map = read_input("input.txt")
    N, M = len(trail_map), len(trail_map[0])
    start = (0, 1)
    second = (1, 1)
    finish = (N-1, N-2)

    print(f"The longest path is {find_longest_path(start, finish, trail_map)} steps long.")
    # --- Task 2 ---
    # Remove all the slopes
    trail_map = tuple(tuple('.' if char != '#' else '#' for char in row) for row in trail_map)
    print(f"The longest path is {find_longest_path(start, finish, trail_map)} steps long.")

if __name__ == "__main__":
    main()