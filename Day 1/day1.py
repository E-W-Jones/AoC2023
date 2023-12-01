import re

words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
TABLE = {key: str(value) for value, key in enumerate(words)}

def calibration_value(line):
    """
    Calculates the calibration value of a line.
    
    Calibration values are the first and last digit in a string, concatenated.
    """
    matches = re.findall(r"\d", line)
    if matches:
        return int(matches[0] + matches[-1])
    else:
        raise ValueError(f"The input line `{line}` had no matches")

def task1():
    with open("input.txt", "r") as filein:
        values = [calibration_value(line) for line in filein.readlines()]

    print(f"The sum of calibration values is {sum(values)}")

def replace_digits(string, table=TABLE):
    """
    Replace all instances of a number written out with the digit.
    
    For example: zero -> 0, one -> 1, ..., up to nine -> 9.
    """
    indexes = {}
    
    for word in table:
        for match in re.finditer(f"(?={word})", string):
            indexes[match.end()] = table[word] 
    for i in sorted(indexes, reverse=True):
        string = string[:i] + indexes[i] + string[i:]
    return string

def task2():
    with open("input.txt", "r") as filein:
        values = [calibration_value(replace_digits(line)) for line in filein.readlines()]

    print(f"The sum of calibration values is {sum(values)}")

if __name__ == "__main__":
    task1()
    task2()
