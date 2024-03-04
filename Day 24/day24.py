def read_input(filename):
    hailstones = []
    with open(filename, "r") as filein:
        for line in filein.read().split('\n'):
            position, velocity = line.split(' @ ')
            hailstone = tuple(map(int, position.split(', ') + velocity.split(', ')))
            hailstones.append(hailstone)
    return hailstones

def sign(x):
    return -1 if x < 0 else (1 if x > 0 else 0)

def samesign(x, y):
    return sign(x) * sign(y) > 0

def intersect_2D(A, B):
    # Test if two hailstones intersect in the future, and if they do, where
    xA, yA, _, uA, vA, _ = A
    xB, yB, _, uB, vB, _ = B
    mA, mB = vA / uA, vB / uB
    cA, cB = yA - mA*xA, yB - mB*xB
    denominator = mA - mB

    if abs(denominator) <= 1e-8:
        # They are parallel so never intersect
        return False
    
    x_intercept = (cB - cA) / denominator
    y_intercept = mA * x_intercept + cA
    
    # Would like to refactor to use t parameterisation, then can just check t>0.
    # Make sure both hailstones are moving towards the interception point
    if (samesign(x_intercept - xA, uA)
    and samesign(y_intercept - yA, vA)
    and samesign(x_intercept - xB, uB)
    and samesign(y_intercept - yB, vB)):
        return x_intercept, y_intercept
    else:
        return False

def find_intersections(hailstones):
    N = len(hailstones)
    # Look at every unique pair of hailstones (nested loop)
    # And if they have an interception add that to the list
    return [intercept for i in range(N) for j in range(i+1, N)
            if (intercept := intersect_2D(hailstones[i], hailstones[j]))]

def in_bounds(intersection, lower, upper):
    x, y = intersection
    return (lower <= x <= upper) and (lower <= y <= upper)

import numpy as np
from random import sample

def solve_for_start(hailstones):
    (xn1, xn2, xn3, vn1, vn2, vn3),\
    (xm1, xm2, xm3, vm1, vm2, vm3),\
    (xl1, xl2, xl3, vl1, vl2, vl3)  = sample(hailstones, 3)
    A = np.array([[-vn2+vm2, vn1-vm1,       0,-xn2+xm2, xn1-xm1,       0],
                  [       0,-vn3+vm3, vn2-vm2,       0,-xn3+xm3, xn2-xm2],
                  [-vn3+vm3,       0, vn1-vm1,-xn3+xm3,       0, xn1-xm1],
                  [-vn2+vl2, vn1-vl1,       0,-xn2+xl2, xn1-xl1,       0],
                  [       0,-vn3+vl3, vn2-vl2,       0,-xn3+xl3, xn2-xl2],
                  [-vn3+vl3,       0, vn1-vl1,-xn3+xl3,       0, xn1-xl1]]).astype(int)

    b = np.array([xn1*vn2-xn2*vn1 - xm1*vm2 + xm2*vm1,
                  xn2*vn3-xn3*vn2 - xm2*vm3 + xm3*vm2,
                  xn1*vn3-xn3*vn1 - xm1*vm3 + xm3*vm1,
                  xn1*vn2-xn2*vn1 - xl1*vl2 + xl2*vl1,
                  xn2*vn3-xn3*vn2 - xl2*vl3 + xl3*vl2,
                  xn1*vn3-xn3*vn1 - xl1*vl3 + xl3*vl1]).astype(int)
    return np.linalg.solve(A, b).astype(int)[:3]

def main():
    hailstones = read_input("input.txt")
    # area = 7, 27  # For sample
    area = 200_000_000_000_000, 400_000_000_000_000
    # --- Task 1 ---
    all_intersections = find_intersections(hailstones)
    valid_intersections_count = sum(in_bounds(intersection, *area) for intersection in all_intersections)
    print(f"There are {valid_intersections_count} intersections in the area {area}.")
    # --- Task 2 ---
    # There does appear to be some kind of stochasiticy, guessing rounding error?
    starts = np.median(np.array([solve_for_start(hailstones) for _ in range(100)]), axis=0)
    print(f"The sum of coordinates is {np.abs(np.sum(starts))}.")
    

if __name__ == "__main__":
    main()