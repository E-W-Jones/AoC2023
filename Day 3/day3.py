import numpy as np

EMPTY = '.'

# Pad the array by 1,
# take a slice like x[1:-1, 1:-1] whenever we're ready to use it
array = np.pad(
    np.genfromtxt("input.txt", delimiter=[1]*140, dtype=str, comments=None),
    # np.genfromtxt("sample_input.txt", delimiter=[1]*10, dtype=str, comments=None),
    1,
    constant_values=EMPTY
    )
empty = (array == EMPTY)
numbers = np.char.isdigit(array)
symbols = ~empty & ~numbers
next_to_symbols = ( symbols[2:  , 1:-1]  # Above
                    | symbols[ :-2, 1:-1]  # Below
                    | symbols[1:-1, 2:  ]  # Right
                    | symbols[1:-1,  :-2]  # Left
                    | symbols[2:  ,  :-2]  # Top left
                    | symbols[2:  , 2:  ]  # Top right
                    | symbols[ :-2,  :-2]  # Bottom left
                    | symbols[ :-2, 2:  ]  # Bottom right
                    )
digit_of_part_number = numbers[1:-1, 1:-1] & next_to_symbols

# Now we need to extract the numbers from the digits
number_indices = []
rows, cols = np.where(numbers[1:-1, 1:-1])
for row in np.unique(rows):
    number = [(row, cols[row == rows][0])]
    for col in cols[row == rows][1:]:
        if (col - number[-1][-1]) == 1:
            number.append((row, col))
        else:
            number_indices.append(number)
            number = [(row, col)]
    else:
        number_indices.append(number)

# Now check if these numbers are part numbers
part_number_indices = []
digit_of_part_number_indices = list(zip(*np.where(digit_of_part_number)))
for number in number_indices:
    for pair in number:
        if pair in digit_of_part_number_indices:
            part_number_indices.append(number)
            break

# Now we can convert these indices into part numbers
part_numbers = []
for indices in part_number_indices:
    digits = [array[1:-1, 1:-1][index] for index in indices]
    part_number = int("".join(digits))
    part_numbers.append(part_number)
# print(part_numbers)
print(f"The sum of part numbers is {sum(part_numbers)}")

# Task 2
# We have all our numbers, so look at each asterisk and how many numbers it has around it
# Have a (default) dictionary (w/ an empty list by default) where each key is a gear,
# and each value is a list of numbers
from collections import defaultdict
gears = defaultdict(list, {})
gears_indices = zip(*np.where(array[1:-1, 1:-1] == '*'))
for gear_index in gears_indices:
    # print(f"{gear_index = }")
    for number in number_indices:
        # print(f"\t{number = }")
        for digit in number:
            # print(f"\t\t{digit = }")
            # Check if they're adjacent in any way
            if ( (abs(digit[0] - gear_index[0]) <= 1)
               & (abs(digit[1] - gear_index[1]) <= 1)
               ):
                gears[gear_index].append(number)
                break

gear_ratios = []
for gear in gears:
    if len(gears[gear]) != 2:
        continue

    ratio = 1
    for indices in gears[gear]:
        digits = [array[1:-1, 1:-1][index] for index in indices]
        ratio *= int("".join(digits))
    gear_ratios.append(ratio)

print(f"The sum of all gear ratios is {sum(gear_ratios)}")
