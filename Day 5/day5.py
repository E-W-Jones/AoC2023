from tqdm import tqdm

class Map:
    def __init__(self):
        self.input = []
        self.output = []
    
    def append(self, output, input, length):
        self.input.append(range(input, input+length))
        self.output.append(range(output, output+length))
    
    def __call__(self, x):
        for input, output in zip(self.input, self.output):
            if x in input:
                # find how many steps it is in, add that onto the start of output
                # print(x)
                return output.start + x - input.start
        return x

    def inverse(self, x):
        for input, output in zip(self.input, self.output):
            if x in output:
                # find how many steps it is in, add that onto the start of input
                return input.start + x - output.start
        return x

    def __repr__(self):
        string = ""
        maximum = 0
        for r in self.input:
            for i in r:
                if i > maximum:
                    maximum = i
        for i in range(maximum+1):
            string += f"{i} -> {self(i)}\n"
        return string

def read_input():
    filein = open("input.txt", "r")
    # --- seeds --- #
    seed_line = filein.readline()
    seeds = seed_line.strip("seeds:\n")
    seeds = [int(seed) for seed in seeds.split()]

    # --- maps --- #
    filein.readline()
    maps = {}
    map_ = Map()
    map_name = ""
    for line in filein.readlines():
        line = line.rstrip("\n")
        if line == "":
            # We finish the current map, create a new one
            maps[map_name] = map_
            map_ = Map()
            continue
        elif line[0].isalpha():
            # It provides a new name
            map_name = line.rstrip(" map:")
        else:
            # It's a value to add to the current map:
            # Making sure to cast elements to ints
            values = map(int, line.split())
            map_.append(*values)
    else:
        maps[map_name] = map_

    filein.close()
    return seeds, maps

def compose_seed_to_location(maps):
    def seed_to_location(seed):
        return maps["humidity-to-location"](
               maps["temperature-to-humidity"](
               maps["light-to-temperature"](
               maps["water-to-light"](
               maps["fertilizer-to-water"](
               maps["soil-to-fertilizer"](
               maps["seed-to-soil"](
                   seed
               )))))))
        
    return seed_to_location

def task1():
    # For each seed, find the location
    seeds, maps = read_input()
    seed_to_location = compose_seed_to_location(maps)
    locations = [seed_to_location(seed) for seed in seeds]
    print(f"The lowest location number is {min(locations)}")

def valid_location(location, maps, seed_pairs):
    def location_to_seed(location):
        return maps["seed-to-soil"].inverse(
               maps["soil-to-fertilizer"].inverse(
               maps["fertilizer-to-water"].inverse(
               maps["water-to-light"].inverse(
               maps["light-to-temperature"].inverse(
               maps["temperature-to-humidity"].inverse(
               maps["humidity-to-location"].inverse(
                   location
               )))))))
    test_seed = location_to_seed(location)
    for seeds in seed_pairs:
        if test_seed in seeds:
            return True
    return False

def task2():
    # Will take too long to iterate through all the seeds
    # Try iterating through all the locations instead!
    seeds, maps = read_input() 

    # In task 2 its not just individual seeds, but rather pairs of seeds that define ranges
    seed_pairs = []
    for i in range(len(seeds) // 2):
        start  = seeds[2*i]
        length = seeds[2*i + 1]
        seed_pairs.append(range(start, start+length))

    location = 0
    while not valid_location(location, maps, seed_pairs):
        location += 1

    print(f"The lowest location number is {location}")

if __name__ == "__main__":
    task1()
    task2()