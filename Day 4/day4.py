def parse_line(line):
    card_number_token, numbers_token = line.rstrip("\n").split(":")
    card_number = int(card_number_token[5:])
    winning_string, numbers_string = numbers_token.split("|")
    winning_numbers = [int(x) for x in winning_string.split()]
    numbers = [int(x) for x in numbers_string.split()]
    return winning_numbers, numbers, card_number

def count_matches(winning_numbers, numbers, *args):
    return sum([int(number in winning_numbers) for number in numbers])

def points(winning_numbers, numbers, *args):
    matches = count_matches(winning_numbers, numbers)

    if matches == 0:
        return 0
    else:
        return 2 ** (matches - 1)

def copies(winning_numbers, numbers, card_number):
    matches = count_matches(winning_numbers, numbers)
    return list(range(card_number+1, card_number+matches+1))

def task1():
    count = 0
    with open("input.txt", "r") as filein:
        for line in filein.readlines():
            count += points(*parse_line(line))
    print(f"The scratchcards are worth {count} points in total")

def task2():
    cards = {}
    your_cards = []
    with open("input.txt", "r") as filein:
        for line in filein.readlines():
            winning_numbers, numbers, card_number = parse_line(line)
            cards[card_number] = (winning_numbers, numbers)
            your_cards.append(card_number)
    total_cards = len(your_cards)

    # Brute forcing it like this isn't the best way
    # For example if card 1 produces one of 2 and one of three, and 2 produces one of 3
    # It would be silly to compute 3 twice, when we could just double the output
    while your_cards:
        card = your_cards.pop()
        new_copies = copies(*cards[card], card)
        your_cards += new_copies
        total_cards += len(new_copies)

    print(f"There are {total_cards} flashcards in total")    

def task2():
    # This method works faster by calculating once which cards give you which other cards
    # And instead of just going "I have one card 2, calculate that result. I have another card 2, calculate that result."
    # we instead say "If card 1 gives you a 3, and card 2 gives you a 3, you have 2 3s total."
    cards = []

    with open("input.txt", "r") as filein:
        for card, line in enumerate(filein.readlines()):
            count = count_matches(*parse_line(line))
            cards.append(range(card+1, card+count+1))

    N = len(cards)
    total = [1] * N
    for i in range(N):
        for card in cards[i]:
            total[card] += total[i]
    print(f"You have a total of {sum(total)} scratchcards")
    

if __name__ == "__main__":
    task1()
    task2()