from itertools import pairwise, chain

class Beam:
    def __init__(self, direction=(0, 1), path=[(0, 0)], finished=False):
        self.direction = direction
        self.path = path
        self.finished = finished

    def copy(self, new_direction=None):
        return Beam(direction=new_direction if new_direction else (0, 1),
                    path=self.path.copy(),
                    finished=self.finished
                    )

    def update(self, grid, N, M, completed):
        i, j = self.path[-1]
        di, dj = self.direction
        i += di
        j += dj

        if i >= N or i < 0 or j >= M or j < 0:
            self.finished = True
            return self,
        elif (self.path[-1], (i, j)) in pairwise(self.path):
            self.finished = True
            return self,
        else:
            for beam in completed:
                if (self.path[-1], (i, j)) in pairwise(beam.path):
                    self.finished = True
                    return self,
            current = grid[i][j]
            self.path.append((i, j))

        if current == '.':
            return self,
        elif current == "/":
            i, j = self.direction
            self.direction = (-j, -i)
            return self,
        elif current == "\\":
            i, j = self.direction
            self.direction = (j, i)
            return self,
        elif current in "-|":
            return self.beam_splitter(current)

    def beam_splitter(self, splitter):
        match (splitter, self.direction):
            case ("-", (0, j)):
                return self,
            case("-", (i, 0)):
                return self.copy((0, 1)), self.copy((0, -1))
            case ("|", (i, 0)):
                return self,
            case("|", (0, j)):
                return self.copy((1, 0)), self.copy((-1, 0))

# Create a stack of beam objects
# Just take the top one, iterate it, add any back onto the top of the stack
# Like a depth first search
# So to update a Beam:
#     Move in the direction
#     Check if the beam has left the grid:
#         If it has, set finished flag to True
#         Otherwise, continue
#     Check if the beam has been in this position before.
#         If its been in the current and previous position in that order before,
#         you're about to go in a loop. Set finished flag to True.
#     Check the new position, and change the direction accordingly
#     If we need to split, return both beams, otherwise just the one
# Take the new beam(s), put them in either the completed array or the in_progress stack
def simulate_beams(grid, **kwargs):
    N, M = len(grid), len(grid[0])
    completed = []
    in_progress = [Beam(**kwargs)]
    while in_progress:
        # print(f"{len(completed) = }, {len(in_progress) = }")
        beam = in_progress.pop()
        for new_beam in beam.update(grid, N, M, completed):
            if new_beam.finished:
                completed.append(beam)
            else:
                in_progress.append(new_beam)
    return completed

def energised_tiles(grid, direction, starting_point):
    beams = simulate_beams(grid, direction=direction, path=[starting_point])
    unique_points = set(chain.from_iterable(beam.path for beam in beams))
    return len(unique_points)

with open("input.txt", "r") as filein:
    grid = filein.read().split("\n")

# --- Task 1 ---
print(f"The number of energised tiles is {energised_tiles(grid, (0, 1), (0, 0))}")

# --- Task 2 ---
# I have no idea how to do this one...
# Lets just brute force it a little
# Even on 16 cores can still expect it to take ~30 minutes
from multiprocessing import Pool, current_process, cpu_count
# Create all of the pairs of direction, starting points we'll want to simulate
N, M = len(grid), len(grid[0])
left_edge   = [((0, 1), (i, 0)) for i in range(N)]
right_edge  = [((0, -1), (i, M-1)) for i in range(N)]
top_edge    = [((1, 0), (0, j)) for j in range(M)]
bottom_edge = [((-1, 0), (N-1, j)) for j in range(M)]

args = chain(left_edge, right_edge, top_edge, bottom_edge)

def mapping(direction, starting_point):
    print(f"Running {current_process().name:>17}/{cpu_count()}: {direction=} {starting_point=}", end=": ")
    result = energised_tiles(grid, direction, starting_point)
    print(f"{result} energised tiles")
    return result

with Pool() as p:
    energised_tile_count = p.starmap(mapping, args)
print(f"The maximum is {max(energised_tile_count)}")