from itertools import combinations

def read_input(filename):
    """Return a list of coordinates of galaxies."""
    with open(filename, "r") as filein:
        return [(i, j) for (i, line) in enumerate(filein.readlines()) for (j, galaxy) in enumerate(line) if galaxy == "#"]

def check_empty_rows(galaxies, columns=False):
    """Return the empty rows OR columns of the input."""
    occupied = set(galaxy[columns] for galaxy in galaxies)
    all_rows = set(range(max(occupied)))
    empty_rows = all_rows - occupied
    return empty_rows

def apply_expansion(galaxy, empty_rows, empty_cols, a=1):
    """Apply the expansion of the universe to a single galaxy, where empty rows/columns increase by a factor a."""
    i, j = galaxy
    return (i + (a-1)*sum(row < i for row in empty_rows), j + (a-1)*sum(col < j for col in empty_cols)) 

def apply_expansion_all(galaxies, a=1):
    """Apply the expansion of the universe to all galaxies."""
    empty_rows = check_empty_rows(galaxies)
    empty_cols = check_empty_rows(galaxies, columns=True)
    return [apply_expansion(galaxy, empty_rows, empty_cols, a=a) for galaxy in galaxies]

def manhattan_distance(coords):
    """Find the manhattan distance between two 2D coordinates."""
    (i, j), (x, y) = coords
    return abs(i - x) + abs(j - y)

def main():
    raw_galaxies = read_input("input.txt")
    # --- Task 1 ---
    # Here we double each empty row/col
    galaxies = apply_expansion_all(raw_galaxies, a=2)
    distances = [manhattan_distance(pair) for pair in combinations(galaxies, 2)]
    print(f"The sum of distances is {sum(distances)}")
    # --- Task 2 ---
    # Now we increase by a factor of 1_000_000
    # 
    a = 1_000_000
    galaxies = apply_expansion_all(raw_galaxies, a=a)
    distances = [manhattan_distance(pair) for pair in combinations(galaxies, 2)]
    print(f"The sum of distances is {sum(distances)}")

if __name__ == "__main__":
    main()
