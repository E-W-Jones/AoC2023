from math import prod

def parse_part(line: str):
    # Bit terse, but it works
    return {x[0]: int(x[2:]) for x in line.strip("{}").split(",")}

def parse_workflow(line: str):
    name, token = line.split("{")
    checks = token.strip("}").split(",")

    def workflow(part):
        for check in checks[:-1]:
            check, return_ = check.split(":")
            field = check[0]
            operator = check[1]
            value = int(check[2:])
            if operator == ">":
                if part[field] > value:
                    return return_
            elif operator == "<":
                if part[field] < value:
                    return return_
            else:
                raise ValueError("Incorrect {operator = }")
        else:
            return checks[-1]
    
    return name, workflow

def read_input(filename):
    part_flag = False
    workflows = {}
    parts = []
    with open(filename, "r") as filein:
        for line in filein.read().split("\n"):
            if line == "":
                part_flag = True
                continue
            if part_flag:
                parts.append(parse_part(line))
            else:
                name, workflow = parse_workflow(line)
                workflows[name] = workflow

    return workflows, parts

def parse_workflow_task2(line: str):
    name, token = line.split("{")
    checks = token.strip("}").split(",")

    def workflow(passes, conditions):
        for check in checks[:-1]:
            condition, return_ = check.split(":")
            conditions.append(condition)
            try:
                if next(passes):
                    return return_, conditions
            except StopIteration:
                return "ran_out", conditions
        else:
            return checks[-1], conditions

    return name, workflow

def read_input_task2(filename):
    workflows = {}
    with open(filename, "r") as filein:
        for line in filein.read().split("\n"):
            if line == "":
                return workflows
            else:
                name, workflow = parse_workflow_task2(line)
                workflows[name] = workflow

def accepted(part, workflows):
    name = "in"
    while name != 'R' and name != 'A':
        name = workflows[name](part)
    else:
        return name == 'A'

def path_traverse(path, workflows):
    path = iter(path.copy())
    name = "in"
    conditions = []
    while name != 'R' and name != 'A' and name != "ran_out":
        name, conditions = workflows[name](path, conditions)
    else:
        return name, conditions

def calculate_paths(workflows):
    incomplete_paths = [[True], [False]]
    accepted_paths = []
    rejected_paths = []
    while incomplete_paths:
        path = incomplete_paths.pop()
        name, conditions = path_traverse(path, workflows)
        # print(f"{name = }, {path = }")
        if name == "A":
            accepted_paths.append((path, conditions))
        elif name == "R":
            rejected_paths.append(path)
        else:
            incomplete_paths.append(path + [True])
            incomplete_paths.append(path + [False])
    return accepted_paths

def value_range(minmax):
    return prod(max_-min_+1 for min_, max_ in minmax.values())

def calculate_accepted_combinations(workflows):
    accepted_paths = calculate_paths(workflows)

    total = 0
    for path, conditions in accepted_paths:
        minmax = {char: [1, 4000] for char in "xmas"}
        for passes, condition in zip(path, conditions):
            field = condition[0]
            operator = condition[1]
            value = int(condition[2:])
            if passes and operator == "<":
                minmax[field][1] = min(minmax[field][1], value-1)
            elif operator == "<":
                minmax[field][0] = max(minmax[field][0], value)
            elif passes and operator == ">":
                minmax[field][0] = max(minmax[field][0], value+1)
            elif operator == ">":
                minmax[field][1] = min(minmax[field][1], value)
        total += value_range(minmax)

    return total

def main():
    # --- Task 1 ---
    workflows, parts = read_input("input.txt")
    total = sum(sum(part.values()) for part in parts if accepted(part, workflows))
    print(f"The total value is {total}")
    # --- Task 2 ---
    workflows = read_input_task2("input.txt")
    combinations = calculate_accepted_combinations(workflows)
    print(f"The total number of valid combinations is {combinations}")

if __name__ == "__main__":
    main()