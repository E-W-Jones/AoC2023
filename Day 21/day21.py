# Have a set of visited nodes
# A queue of the boundary nodes
# Iterate through the queue of boundary nodes for each step:
#     checking if not in visited nodes
#         and if its not then adding to the next round of boundary nodes
# We actually dont want to check if it's in boundary either

# Constants (just for reading in the file)
START = "S"
GARDEN = "."
ROCK = "#"
BOUNDARY = "O"
NEIGHBOURS = ((0, 1), (0, -1), (1, 0), (-1, 0))

def pprint(bounds, start=None, garden_plots=[], rocks=[], boundary_nodes=[], tile=1):
    """
    Pretty print the data provided as sets of coordinates as a map.
    
    Tiling is general untested, try to use tile = 1 or 3 only.
    """
    N, M = bounds
    output = [["_" for _ in range(M)] for _ in range(N)]
    if start:
        i, j = start
        output[i][j] = GARDEN
    for i, j in garden_plots:
        output[i][j] = GARDEN
    for i, j in rocks:
        output[i][j] = ROCK

    tiled_output = [[output[i%N][j%M] for j in range(tile*M)] for i in range(tile*N)]

    for (i, j) in boundary_nodes:
        x, y = 0, 0
        # print(i, j, x, y, end=" -> ")
        x += tile // 2
        y += tile // 2
        i += x*N
        j += y*M
        tiled_output[i][j] = BOUNDARY
        # print(i, j)

    if start:
        i, j = start
        x = tile // 2
        y = tile // 2
        i += x*N
        j += y*M
        tiled_output[i][j] = START

    print("\n".join(map("".join, tiled_output)))

def read_input(filename):
    garden_plots = set()
    rocks = set()

    with open(filename, "r") as filein:
        for i, line in enumerate(filein.read().split("\n")):
            for j, point in enumerate(line):
                coordinate = (i, j)
                if point == START:
                    start = coordinate
                elif point == GARDEN:
                    garden_plots.add(coordinate)
                elif point == ROCK:
                    rocks.add(coordinate)
                else:
                    raise ValueError(f"Invalid value in input {filename}: {point} should instead be one of {START}, {GARDEN}, {ROCK}")

    # The bounds of the map, starting with 0
    bounds = (i+1, j+1)
    return start, garden_plots, frozenset(rocks), bounds

def visited_plots(start, rocks, bounds, number_of_steps):
    visited = {start}
    next_visited = set()

    for t in range(number_of_steps):
        for x, y in visited:
            for dx, dy in NEIGHBOURS:
                xp, yp = x+dx, y+dy
                if (0 <= xp < bounds[0]) and (0 <= yp < bounds[1]):
                    if (xp, yp) in rocks:
                        continue
                    else:
                        next_visited.add((xp, yp))

        visited = next_visited
        next_visited = set()
    return visited


def visited_plots_pbc(start, rocks, bounds, number_of_steps):
    visited = {start}
    next_visited = set()

    for t in range(number_of_steps):
        for x, y in visited:
            for dx, dy in NEIGHBOURS:
                xp, yp = x+dx, y+dy
                if (xp % bounds[0], yp % bounds[1]) not in rocks:
                    next_visited.add((xp, yp))

        visited = next_visited
        next_visited = set()
    return visited



# def visited_plots_pbc(start, rocks, bounds, start_time, end_time):
#     visited = {start}
#     next_visited = set()

#     infected = dict()

#     prev_n = -99
#     for t in range(start_time, end_time):
#         for x, y in visited:
#             for dx, dy in NEIGHBOURS:
#                 xp, yp = x+dx, y+dy
#                 if (0 <= xp < bounds[0]) and (0 <= yp < bounds[1]):
#                     if (xp, yp) in rocks:
#                         continue
#                     else:
#                         next_visited.add((xp, yp))
#                 elif (dx, dy) not in infected:
#                     # We 'infect' the next grid at time t
#                     t_infected = t+1
#                     next_start = (xp % bounds[0], yp % bounds[1])
#                     infected[(dx, dy)] = (t_infected, next_start)
#         if prev_n == len(next_visited):
#             # we can actually stop iterating bc it just alternates
#             if (end_time - t) % 2 == 0:
#                 visited = next_visited
#             # else visited stays as visited
#             break
#         else:
#             prev_n = len(visited)
#             visited = next_visited
#             next_visited = set()
#     return len(visited), infected

# def infinite_map(start, rocks, bounds, number_of_steps):
#     number_visited, infected = visited_plots_pbc(start, rocks, bounds, 0, number_of_steps)
#     image = 0, 0
#     total_visited = {image: number_visited}
#     # total_visited = number_visited
#     infected_dict = infected
#     to_visit = list(infected_dict.keys())

#     while to_visit:
#         image = to_visit.pop(0)
#         print(image)
#         t_infected, start = infected_dict[image]
#         number_visited, infected = visited_plots_pbc(start, rocks, bounds, t_infected, number_of_steps)
#         print(f"visited {number_visited} in {image}")
#         total_visited[image] = number_visited
#         for ((dx, dy), values) in infected.items():
#             new_image = image[0] + dx, image[1] + dy
#             if (new_image in total_visited) or ( (new_image in to_visit) and (infected_dict[new_image][0] < values[0]) ):
#                 continue
#             else:
#                 to_visit.append(new_image)
#                 infected_dict[new_image] = values

#     return total_visited




def main():
    # --- Task 1 ---
    filename, number_of_steps = "sample_input.txt", 6
    filename, number_of_steps = "input.txt", 64
    start, garden_plots, rocks, bounds = read_input(filename)
    # Generate the boundary after so many steps
    boundary_nodes = visited_plots(start, rocks, bounds, number_of_steps)
    # Print the output
    # pprint(bounds, start, garden_plots, rocks, boundary_nodes)
    print(f"There are {len(boundary_nodes)} garden plots the elf can reach.")

    # --- Task 2 ---
    # Excessive maths taken from the solution megathread on the subreddit
    # Basically using this: https://en.wikipedia.org/wiki/Newton_polynomial
    x = 26501365  # = 202300 * 131 + 65
    h = 131
    x0 = 65
    x1, x2 = x0 + h, x0 + 2*h
    y0, y1, y2 = [len(visited_plots_pbc(start, rocks, bounds, x)) for x in [x0, x1, x2]]
    total = y0 + (y1 - y0)/h * (x-x0) + (y2 - 2*y1 + y0)/(2*h*h) * (x-x0)*(x-x1)
    print(f"There are {total} garden plots the elf can reach.")
    

if __name__ == "__main__":
    main()