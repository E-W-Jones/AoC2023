def read_input(filename):
    with open(filename, "r") as filein:
        return [list(line.rstrip("\n")) for line in filein.readlines()]

def pprint(rocks):
    print(*map("".join, rocks), sep="\n")

def calculate_load(grid):
    return sum((i+1)*row.count('O')  for i, row in enumerate(reversed(grid)))

def hash(grid):
    return tuple((i, j)
                 for i, row in enumerate(grid)
                 for j, char in enumerate(row)
                 if char == 'O'
                 )

def unhash(hash, grid):
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == '#':
                pass
            elif (i, j) in hash:
                grid[i][j] = 'O'
            else:
                grid[i][j] = '.'
    return grid

def calculate_runs_north_south(grid):
    runs = []
    run = []
    for j in range(len(grid[0])):
        run = []
        for i in range(len(grid)):
            if grid[i][j] == "#":
                if run:
                    runs.append(run)
                run = []
            else:
                run.append((i, j))
        else:
            if run:
                runs.append(run)
                run = []
    return runs

def calculate_runs_south_north(grid):
    # south to north is just a reverse of each run in north to south
    return [list(reversed(run)) for run in calculate_runs_north_south(grid)]

def calculate_runs_west_east(grid):
    runs = []
    run = []
    for i in range(len(grid)):
        run = []
        for j in range(len(grid[0])):
            if grid[i][j] == "#":
                if run:
                    runs.append(run)
                run = []
            else:
                run.append((i, j))
        else:
            if run:
                runs.append(run)
                run = []
    return runs

def calculate_runs_east_west(grid):
    return [list(reversed(run)) for run in calculate_runs_west_east(grid)]

def slide(grid, runs):
    for run in runs:
        count = 0
        for i, j in run:
            if grid[i][j] == 'O':
                count += 1
                grid[i][j] = '.'
        for i, j in run[:count]:
            grid[i][j] = 'O'
    return grid

def spin_cycle(rocks, north, south, east, west):
    return slide(slide(slide(slide(rocks, runs=north), runs=west), runs=south), runs=east)

def main():
    # --- Task 1 ---
    rocks = read_input("input.txt")
    rocks = slide(rocks, calculate_runs_north_south(rocks))
    print(f"The load after sliding north once is {calculate_load(rocks)}")

    # --- Task 2 ---
    runs = {
        "north": calculate_runs_north_south(rocks),
        "east": calculate_runs_east_west(rocks),
        "south": calculate_runs_south_north(rocks),
        "west": calculate_runs_west_east(rocks),
        }    

    rocks = read_input("input.txt")
    table = {}
    for i in range(1_000_000_000):
        key = hash(rocks)
        if key in table:
            # Had to look at the reddit to get the idea of looking for a cyclical
            # solution to cut out needless calculations
            break
        else:
            table[key] = i
        rocks = spin_cycle(rocks, **runs)

    reversed_table = {v: k for k, v in table.items()}

    offset = table[key]
    period = i - table[key]
    index = (1_000_000_000-offset) % period + offset
    final_rocks = unhash(reversed_table[index], rocks)
    print(f"The load after 1_000_000_000 spin cycles is {calculate_load(final_rocks)}")

if __name__ == "__main__":
    main()