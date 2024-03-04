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

def main():
    hailstones = read_input("input.txt")
    # area = 7, 27
    area = 200_000_000_000_000, 400_000_000_000_000
    # --- Task 1 ---
    all_intersections = find_intersections(hailstones)
    valid_intersections_count = sum(in_bounds(intersection, *area) for intersection in all_intersections)
    print(f"There are {valid_intersections_count} intersections in the area {area}.")

if __name__ == "__main__":
    main()