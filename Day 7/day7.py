from math import prod

# Hashing idea:
# Lets start with 2 cards, A and B, where B > A
# If we have a hand of 1, then there are two possibilities:
# A, B
# These will hash like {A => 0, B => 1}
# So the order is 
# A, B

# Now consider a hand of 2 cards, there are 4 possibilities:
# AA, AB, BA, BB
# The first will look like 
# 2**1 * 0 + 2**0 * 0 = 0
# the second
# 2**1 * 0 + 2**0 * 1 = 1
# the third
# 2**1 * 1 + 2**0 * 0 = 2
# the fourth
# 2**1 * 1 + 2**0 * 1 = 3
# which is incorrect. Instead, add a leading type bit
# The first will look like 
# 2**2 * 1 + 2**1 * 0 + 2**0 * 0 = 4
# the second
# 2**2 * 0 + 2**1 * 0 + 2**0 * 1 = 1
# the third
# 2**2 * 0 + 2**1 * 1 + 2**0 * 0 = 2
# the fourth
# 2**2 * 1 + 2**1 * 1 + 2**0 * 1 = 7
# So we get the mapping {AB=> 1, BA=> 2, AA => 4, BB => 7}

# The base should always be the larger number out of:
#     types of hands, which is just the length of the string
# or
#     number of cards
# So we can in general have a hand "X0 X1 X2 ... XN"
# N**(N+1) * (type of hand) + N**(N) * (value of X0) + ... N**(0) * (value of XN)

def kind_day1(hand):
    frequencies = [hand.count(card) for card in set(hand)]
    match max(frequencies):
        case 5:
            return 7
        case 4:
            return 6
        case 3:
            if len(frequencies) == 2:
                return 5
            else:
                return 4
        case 2:
            if len(frequencies) == 3:
                # 2 pairs: [1, 2, 2]
                return 3
            else:
                # 1 pair: [1, 1, 1, 2]
                return 2
        case 1:
            return 1

def hash_day1(hand, card_value={card: value for value, card in enumerate("23456789TJQKA")}):
    hash = 0
    N = len(hand)

    for i, card in enumerate(hand):
        hash += (13 ** (N-i-1)) * card_value[card]
    
    hash += (13 ** N) * kind_day1(hand)
    return hash

def kind_day2(hand):
    n_jacks = hand.count("J")
    frequencies = [hand.count(card) for card in set(hand) if card != "J"]
    if frequencies:
        max_freq = max(frequencies)
    else:
        # All 5 letters were jacks
        max_freq = 0
    match max_freq + n_jacks:
        case 5:
            return 7
        case 4:
            return 6
        case 3:
            if len(frequencies) == 2:
                return 5
            else:
                return 4
        case 2:
            if len(frequencies) == 3:
                # 2 pairs: [1, 2, 2]
                return 3
            else:
                # 1 pair: [1, 1, 1, 2]
                return 2
        case 1:
            return 1

def hash_day2(hand, card_value={card: value for value, card in enumerate("J23456789TQKA")}):
    hash = 0
    N = len(hand)

    for i, card in enumerate(hand):
        hash += (13 ** (N-i-1)) * card_value[card]
    
    hash += (13 ** N) * kind_day2(hand)
    return hash

def read_input():
    hands = []
    bids = []
    with open("input.txt", "r") as filein:
        for line in filein.readlines():
            hand, bid = line.rstrip("\n").split()
            hands.append(hand)
            bids.append(int(bid))
    return hands, bids

def find_rank(hands, hash):
    sorted_hands = sorted(hands, key=hash)
    ranks = [1 + sorted_hands.index(hand) for hand in hands]
    return ranks

def task1():
    hands, bids = read_input()
    rank = find_rank(hands, hash=hash_day1)
    winnings = map(prod, zip(rank, bids))
    print(f"The total winnings are {sum(winnings)}")

def task2():
    hands, bids = read_input()
    rank = find_rank(hands, hash=hash_day2)
    winnings = map(prod, zip(rank, bids))
    print(f"The total winnings are {sum(winnings)}")

if __name__ == "__main__":
    task1()
    task2()