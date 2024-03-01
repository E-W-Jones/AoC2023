from typing import NamedTuple
from itertools import product

class Brick(NamedTuple):
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    def __contains__(self, __key) -> bool:
        try:
            x, y, z = __key
        except ValueError as e:
            print(f"Incorrect {__key = }, should look like (x, y, z)")
            raise e
        return (self.x1 <= x <= self.x2) and (self.y1 <= y <= self.y2) and (self.z1 <= z <= self.z2)

    def __lt__(self, other):
        for xs, ys in product(range(self.x1, self.x2+1), range(self.y1, self.y2+1)):
            for xo, yo in product(range(other.x1, other.x2+1), range(other.y1, other.y2+1)):
                if (xs == xo) and (ys == yo) and (other.z1 - self.z2 == 1):
                    return True
        return False

    @classmethod
    def from_string(cls, string):
        # Split the string into two tokens on the tilde, then into coords on the commas
        # Before mapping to ints
        return cls(*[int(coord) for token in string.split('~') for coord in token.split(',')])

def read_input(filename):
    with open(filename, "r") as filein:
        return [Brick.from_string(line) for line in filein.read().split("\n")]

def lower_bricks(bricks):
    brick_queue = sorted(bricks, key=lambda x: x.z2)
    
    max_x = max(max(b.x1 for b in bricks), max(b.x2 for b in bricks))
    max_y = max(max(b.y1 for b in bricks), max(b.y2 for b in bricks))
    max_z = max(max(b.z1 for b in bricks), max(b.z2 for b in bricks))
    filled_spaces = [[[z == 0 for z in range(max_z+1)] for _ in range(max_y+1)] for _ in range(max_x + 1)]
    for x, y, z in product(range(max_x+1), range(max_y+1), range(1, max_z+1)):
        filled_spaces[x][y][z] = any((x, y, z) in brick for brick in bricks)
    
    lowered_bricks = []

    for i, brick in enumerate(brick_queue):
        potential_z = []
        for x, y in product(range(brick.x1, brick.x2+1), range(brick.y1, brick.y2+1)):
            for z in range(brick.z1, 0, -1):
                if filled_spaces[x][y][z-1]:
                    # Brick would be as low as can go
                    potential_z.append(z)
                    break

        z = max(potential_z)
        z1 = z
        z2 = z + brick.z2 - brick.z1

        for x, y in product(range(brick.x1, brick.x2+1), range(brick.y1, brick.y2+1)):
            for z in range(brick.z1, brick.z2+1):
                filled_spaces[x][y][z] = False
            for z in range(z1, z2+1):
                filled_spaces[x][y][z] = True
        # Add to the list to return
        lowered_bricks.append(Brick(brick.x1, brick.y1, z1, brick.x2, brick.y2, z2))
    return lowered_bricks
        
def test_rests_on(brick, bricks):
    # Test and return the bricks that rest on brick
    res = []
    for i, brick2 in enumerate(bricks):
        if brick is brick2:
            continue
        if brick2 < brick:  # Overloaded '<'
            res.append(i)
    return res

def test_disintergratable(i, rests_on):
    # If you remove brick i, will other bricks fall?
    for key in rests_on:
        if key == i:
            pass
        elif i in rests_on[key] and len(rests_on[key]) == 1:
            return False
    return True

def cache(func):
    # My own cache function that just uses the first arguments, not the unhashable dictionary
    _cache = {}
    def wrapper(*args, **kwargs):
        key = args[:2]
        if key not in _cache:
            result = func(*args, **kwargs)
            _cache[key] = result
            return result
        else:
            return _cache[key]
    return wrapper

@cache
def test_holds_up(i, x, rests_on):
    # Test if we removed x, would i fall
    if len(rests_on[i]) == 0:
        return False
    if x in rests_on[i]:
        if len(rests_on[i]) == 1:
            return True
        else:
            return False
    # Now we need to go through and check if ALL the ones it rests on drop too
    result = True
    for j in rests_on[i]:
        result &= test_holds_up(j, x, rests_on)
    return result



def main():
    bricks = read_input("input.txt")
    bricks = lower_bricks(bricks)
    # Dictionary reads: key rests on the bricks stored in value
    rests_on = {i: test_rests_on(brick, bricks) for i, brick in enumerate(bricks)}
    disintergratable = [i for i in rests_on if test_disintergratable(i, rests_on)]

    # --- Task 1 ---
    total_disintergratable = len(disintergratable)
    print(f"{total_disintergratable} bricks could be safely disintergrated")

    # --- Task 2 ---
    # Look at every pair of bricks being removed and if it falls, and track if it does
    total_fall = sum(
                    test_holds_up(i, x, rests_on)
                        for i in rests_on
                        for x in rests_on if x not in disintergratable
                    )
    print(f"{total_fall} bricks fall in total")

if __name__ == "__main__":
    main()