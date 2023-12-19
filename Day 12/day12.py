def read_input(filename):
    conditions, groupings = [], []
    with open(filename, "r") as filein:
        for line in filein.readlines():
            condition, grouping = line.split()
            conditions.append(condition)
            groupings.append(tuple(map(int, grouping.split(","))))
    return conditions, groupings

def check_grouping(condition, grouping):
    # print(condition)
    index = 0
    running_total = 1 if condition[0] == "#" else 0
    for i in range(1, len(condition.rstrip('.'))):
        # print("\t"+condition)
        # print("\t"+" "*i + "^")
        if condition[i] == '#':
            running_total += 1
            if running_total > grouping[index]:
                return False
        elif condition[i-1] == "#" and condition[i] == '.':
            if running_total != grouping[index]:
                return False
            if index == len(grouping) - 1:
                return False
            else:
                index += 1
            # print(index, len(grouping))
            running_total = 0

    return index == len(grouping)-1 and running_total == grouping[index]

def generate_conditions_naive(condition):
    conditions = ['']
    for i, char in enumerate(condition):
        if char == '?':
            while len(conditions[0]) == i:
                cond = conditions.pop(0)
                conditions += [cond + '.', cond + '#']
        else:
            conditions = [cond + char for cond in conditions]
    return conditions

def generate_conditions(condition):
    # Need to be smarter! But not entirely sure how
    # Maybe some sort of dynamic/recursive soln to look at just the number instead of all the options?
    # OR we just be smarter about task 2? Bc a lot of the solutions will be similar
    pass

generate_conditions = generate_conditions_naive

def count_arrangments(conditions, groupings):
    count = 0
    for condition, grouping in zip(conditions, groupings):
        # print(condition)
        def filter_by(condition):
            return check_grouping(condition, grouping)
        valid = filter(filter_by, generate_conditions(condition))
        count += len(list(valid))
    return count

def main():
    conditions, groupings = read_input("sample_input.txt")
    # --- Task 1 ---
    # Iterate through each record
    count = count_arrangments(conditions, groupings)
    print(f"The total number of possible arrangements is {count}")
    # --- Task 2 ---
    # Unfold the records, then run
    conditions = ["?".join([condition]*5) for condition in conditions]
    groupings = [g+g+g+g+g for g in groupings]
    count = count_arrangments(conditions, groupings)
    print(f"The total number of possible arrangements is {count}")

if __name__ == "__main__":
    main()