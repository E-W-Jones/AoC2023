from collections import OrderedDict

def hash(string):
    current_value = 0
    for c in string:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value

def hashmap(string, boxes):
    if string[-1] == "-":
        label = string[:-1]
        box = hash(label)
        if label in boxes[box]:
            del boxes[box][label]
    else:
        label, focal_length = string.split("=")
        boxes[hash(label)][label] = int(focal_length)

def main():
    with open("input.txt", "r") as filein:
        input = filein.read().split(",")
    # --- Task 1 ---
    print(f"The sum of results is {sum(map(hash, input))}")

    # --- Task 2 ---
    boxes = [OrderedDict() for _ in range(256)]

    for step in input:
        hashmap(step, boxes)

    power = sum((i+1) * (slot+1) * focal_length 
                for i, box in enumerate(boxes)
                for slot, focal_length in enumerate(box.values())
                )

    print(f"The focusing power is {power}")

if __name__ == "__main__":
    main()
