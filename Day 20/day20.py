from typing import NamedTuple
from collections import OrderedDict
from math import lcm

LOW = 0
HIGH = 1

class Pulse(NamedTuple):
    broadcaster: str  # broadcaster probably slightly confysingly named
    destination: str
    type: int

    def __str__(self):
        low_high = 'low' if self.type == LOW else 'high'
        return f"{self.broadcaster} -{low_high}-> {self.destination}"

class Module:
    def __init__(self, id, destinations):
        self.id = id
        self.destinations = destinations
    
    def recieve(self, pulse):
        return None

    def state(self):
        return False
    
    def all_states(self):
        return False,

class FlipFlop(Module):
    OFF = 0
    ON = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state = self.OFF

    def _flip(self):
        if self._state == self.OFF:
            self._state = self.ON
        else:
            self._state = self.OFF

    def _send(self):
        send = HIGH if self._state == self.ON else LOW
        return [Pulse(self.id, destination, send) for destination in self.destinations]

    def recieve(self, pulse):
        if pulse.type == HIGH:
            return None
        elif pulse.type == LOW:
            self._flip()
            return self._send()
        else:
            raise ValueError(f"Invalid {pulse = }")
    
    def state(self):
        "Return 0 if in an OFF state, 1 if in an ON state"
        return self._state == self.ON

    def all_states(self):
        # Can be either on, or off
        return False, True

class Conjunction(Module):
    def __init__(self, inputs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.memory = OrderedDict({input: LOW for input in inputs})

    def recieve(self, pulse):
        self.memory[pulse.broadcaster] = pulse.type
        send = LOW if all(x == HIGH for x in self.memory.values()) else HIGH
        return [Pulse(self.id, destination, send) for destination in self.destinations]

    def state(self):
        return sum(2**i * (m == HIGH) for i, m in enumerate(self.memory.values()))

    def all_states(self):
        # Assumes each thing in memory can be high or low (true)
        return range(2 ** len(self.memory)) 

    def __str__(self) -> str:
        return str(self.state())
    
    def all(self):
        return all(x == HIGH for x in self.memory.values())

class Broadcaster(Module):
    def recieve(self, pulse):
        return [Pulse(self.id, destination, pulse.type) for destination in self.destinations]

class Button(Module):
    def __init__(self):
        super().__init__("button", ["broadcaster"])
    
    def press(self):
        return [Pulse(self.id, destination, LOW) for destination in self.destinations]

def read_input(filename):
    # Work on this, should generally be fine?
    # split line on " -> "
    # if starts with %: flip flow
    # & conjuction
    # neither: broadcaster
    with open(filename, "r") as filein:
        lines = filein.read().split("\n")

    conjuction_ids = []
    id_destination_maps = {}
    modules = {}
    for line in lines:
        id, destinations = line.split(" -> ")
        destinations = tuple(destinations.split(", "))
        if id[0] == "%":
            id = id[1:]
            id_destination_maps[id] = destinations
            modules[id] = FlipFlop(id, destinations)
        elif id[0] == "&":
            id = id[1:]
            conjuction_ids.append(id)
            id_destination_maps[id] = destinations
        else:
            id = id
            id_destination_maps[id] = destinations
            modules[id] = Broadcaster(id, destinations)

    for id in conjuction_ids:
        inputs = []
        for potential_input in id_destination_maps:
            if id in id_destination_maps[potential_input]:
                inputs.append(potential_input)
        modules[id] = Conjunction(tuple(inputs), id, id_destination_maps[id])

    # Check if there's a dummy modules
    for destinations in id_destination_maps.values():
        for id in destinations:
            if id not in modules:
                modules[id] = Module(id, tuple())
    return modules

# Pulses processed in order sent, i.e. in a FIFO queue
def press_button(modules, verbose=False):
    queue = Button().press()
    N_low = N_high = 0

    while queue:
        pulse = queue.pop(0)
        if verbose:
            print(pulse)
        if pulse.type == HIGH:
            N_high += 1
        else:
            N_low += 1
        if new_pulses:=modules[pulse.destination].recieve(pulse):
            queue += new_pulses
    return N_low, N_high

def task1(modules):
    low = high = 0
    for _ in range(1000):
        # In AoC style, might need to identify when we reach a cycle, and abuse that
        l, h = press_button(modules)
        low += l
        high += h
    return low * high

# --- Task 1 ---
modules = read_input("input.txt")
total_pulses_product = task1(modules)
print(f"The product of totals is {total_pulses_product}")
# --- Task 2 ---
# I don't know if I still completely understand why task 2 works: it seems to me like the fact you get a high pulse in the middle of a button press should have some side effects, as opposed to it just being the LCM?
# Reset modules
modules = read_input("input.txt")

# for rx to recieve a low pulse, need all of ln, db, vq, tf to send high pulses to tg
# Each of these sends a high pulse when each of bk, tp, pt, vd send a low pulse
# So how many button presses for that to happen?
cycle_counts = {id: 0 for id in ["ln", "db", "vq", "tf"]}
presses = 0
while not all(cycle_counts.values()):
    # You can't just check at the end of the button press
    queue = Button().press()
    presses += 1

    while queue:
        pulse = queue.pop(0)
        if pulse.destination == "tg" and pulse.type == HIGH:
            cycle_counts[pulse.broadcaster] = presses
        if new_pulses:=modules[pulse.destination].recieve(pulse):
            queue += new_pulses

print(f"The total number of button presses is {lcm(*cycle_counts.values())}")