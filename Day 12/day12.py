from functools import cache

def read_input(filename):
    conditions, groupings = [], []
    with open(filename, "r") as filein:
        for line in filein.readlines():
            condition, grouping = line.split()
            conditions.append(condition)
            groupings.append(tuple(map(int, grouping.split(","))))
    return conditions, groupings

@cache
def recursive(string, groups):
    """
    Based on https://advent-of-code.xavd.id/writeups/2023/day/12/

    Go through the string/groups to see if it is possible to build that
    collection of groups from the current string, and if it is, how many ways
    there are.

    Designed to break it down using recursion + caching so we end up with lots
    of small problems we've already solved
    """
    # print(string, groups)
    if not string:    # We have ran out of springs we could use.
        if groups:    # This will be invalid as we're trying to assign springs
            return 0  # that don't exist 
        else:         # This is fine, we've just happily ran off the end of our
            return 1  # string
    
    if not groups:         # We've ran out of groups of springs
        if '#' in string:  # We have springs that'll be unaccounted for, so
            return 0       # invalid
        else:
            return 1
    
    if string[0] == ".":  # The first character is '.' which does nothing
        return recursive(string[1:], groups)
    
    if string[0] == "?":  # The first character is '?', take sum of branches:
        return ( recursive('#'+string[1:], groups)  # ? is a #
               + recursive(string[1:], groups)      # ? is a ., but we ignore .
               )
    
    if string[0] == "#":
        # There are a couple of checks we need to make:
        potential_group = groups[0]
        # Are there actually enough characters in the string to make the group
        # (This seems like one we could do at the beginning)
        if len(string) < potential_group:
            return 0
        # Is this one continguous group?
        if '.' in string[:potential_group]:
            return 0
        # Is it possible for the group to end?:
        # if we have ###, this can't be a group of 2, but ##? could be
        # If we can't end the group, then its invalid
        if not(len(string) == potential_group or string[potential_group] != "#"):
            return 0
        # Otherwise we're all good! We've found a group
        return recursive(string[potential_group+1:], groups[1:])
    
    # If we've made it to here, something has gone wrong
    raise ValueError("Invalid arguments:"
                     "we have exhausted all recursive possiblities")

def count_arrangments(conditions, groupings):
    count = 0
    for condition, grouping in zip(conditions, groupings):
        count += recursive(condition, grouping)
    return count

def main():
    conditions, groupings = read_input("input.txt")
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