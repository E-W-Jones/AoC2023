from math import lcm

# Seen some other solutions that use itertools.cycle() and enumerate, but I like mine still
class list_pbc(list):
    """Subclass of list that automatically indexes with periodic boundary conditions"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.N = len(self)

    def __getitem__(self, i):
        return super().__getitem__(i % self.N)

def read_input(filename):
    with open(filename, "r") as filein:
        instructions_string = filein.readline().rstrip("\n")
        instructions = list_pbc(0 if instruction == "L" else 1 for instruction in instructions_string)
        filein.readline()  # Blank line in input

        nodes = {}
        for line in filein.readlines():
            name, next = line.rstrip("\n").split(" = ")
            next = next.strip("()").split(", ")
            nodes[name] = next

    return instructions, nodes

def main():
    instructions, nodes = read_input("input.txt")
    # --- Task 1 ---
    i = 0
    node = "AAA"
    while node != "ZZZ":
        node = nodes[node][instructions[i]]
        i += 1
    else:
        print(f"It took {i} steps to reach {node}.")
    
    # --- Task 2 ---
    # If we assume they journeys are cyclic, then we can calculate each trip as above, indivually.
    # The lowest common multiple of these will be the total no. of steps.
    # I'm especially proud of this, because this is a technique I learnt in a previous advent of code.
    i_values = []
    for node in filter(lambda node: node[-1] == "A", nodes):
        i = 0
        while node[-1] != "Z":
            node = nodes[node][instructions[i]]
            i += 1
        else:
            i_values.append(i)

    print(f"The total number of steps needed is {lcm(*i_values)}")

    

if __name__ == "__main__":
    main()