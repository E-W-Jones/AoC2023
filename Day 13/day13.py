def read_input(filename):
    with open(filename, "r") as filein:
        pattern = []
        patterns = []
        for line in filein.read().split("\n"):
            if line:
                pattern.append(line)
            else:
                patterns.append(pattern)
                pattern = []
        patterns.append(pattern)
    return patterns

def check_reflections(pattern, ignore=-99):
    N = len(pattern)
    for i in range(1, N):
        # Start by checking the boundary between the first and second row, then keep going out
        # print(i, N)
        for j in range(i, 0, -1):
            # print("\t", j-1, 2*i-j)
            if 2*i - j >= N:
                continue
            if pattern[j-1] != pattern[2*i-j]:
                break
        else:
            if i == ignore:
                pass
            else:
                return i
    else:
        return False

def transpose(pattern):
    return list(map("".join, zip(*pattern)))

def unsmudge(string, i):
    """Return a new string with element i replaced with substring."""
    token = '#' if string[i] == '.' else '.'
    return string[:i] + token + string[i+1:]

def check_smudged(pattern):
    # Find the original result
    original, horizontal = (result, True) if (result:=check_reflections(pattern)) else (check_reflections(transpose(pattern)), False)
    
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            pattern[i] = unsmudge(pattern[i], j)
            if result:=100*check_reflections(pattern, ignore=original if horizontal else -99):
                return result
            if result:=check_reflections(transpose(pattern), ignore=original if not horizontal else -99):
                return result

            pattern[i] = unsmudge(pattern[i], j)  # Resmudge it

def main():
    patterns = read_input("input.txt")
    # --- Task 1 ---
    total = 0
    for pattern in patterns:
        if result:=check_reflections(pattern):
            total += 100 * result
        else:
            total += check_reflections(transpose(pattern))
    print(f"The solution to task 1 is {total}")

    # --- Task 2 ---
    total = 0
    for pattern in patterns:
        total += check_smudged(pattern)
    print(f"The solution to task 2 is {total}")

if __name__ == "__main__":
    main()