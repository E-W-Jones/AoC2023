from functools import reduce

def diff(x):
    return [x[i] - x[i-1] for i in range(1, len(x))]

def extrapolate_values(arr):
    starts = [arr[0]]
    ends = [arr[-1]]
    while any(arr:=diff(arr)):
        starts.append(arr[0])
        ends.append(arr[-1])
    return reduce(lambda x, y: y-x, reversed(starts)), sum(ends)

def read_input():
    with open("input.txt", "r") as filein:
        return [list(map(int, line.split())) for line in filein.readlines()]

def main():
    data = read_input()
    first_values = []
    next_values = []
    for arr in data:
        first, last = extrapolate_values(arr)
        first_values.append(first)
        next_values.append(last)
    # --- Task 1 ---
    print(f"The sum of extrapolated end values is {sum(next_values)}")
    # --- Task 2 ---
    print(f"The sum of extrapolated starting values is {sum(first_values)}")

if __name__ == "__main__":
    main()