from collections import Counter


"""
Create a function to convert a hand to an integer which reflects how strong the 
hand is. Then just sort to rank the hands and find the answer from there.
To get integer, use base 14 since there are 13 unique cards, with the J card 
having 2 possible values. Calculate card strength by: 
c5 * (14 ** 4) + c4 * (14 ** 3) + ... + c1 * (14 ** 0)
Then add hand strength to the front since card strength will only be considered 
for hands with the same strength. Add by:
strength = hand_strength * (14 ** 5) + card_strength
"""


def read_input(file):
    with open(file, 'r') as f:
        hands = list()
        for line in f:
            raw_hand = line.strip().split()
            hand = (raw_hand[0], int(raw_hand[1]))
            hands.append(hand)
        return hands


def get_card_strength(hand, part):
    """
    Get the cumulative score of individual cards.
    """
    card_2_strength = {'A': 13, 'K': 12, 'Q': 11, 'T': 9, '9': 8, '8': 7,
                       '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1,
                       }
    if part == 1:
        card_2_strength['J'] = 10
    elif part == 2:
        card_2_strength['J'] = 0
    strength = 0
    for i, card in enumerate(hand[::-1]):
        strength += card_2_strength[card] * (14 ** i)
    return strength


def convert_joker(hand):
    """
    Converts all jokers to the majority element in hand to get the highest hand
    score.
    """
    j_count = hand.count('J')
    new_hand = hand.replace('J', '')
    card_counts = Counter(new_hand)
    majority_elem, majority_elem_count = 'A', 0
    for elem, elem_count in card_counts.items():
        if elem_count > majority_elem_count:
            majority_elem, majority_elem_count = elem, elem_count
    new_hand += majority_elem * j_count
    return new_hand


def get_hand_strength(hand):
    card_counts = list(Counter(hand).values())
    card_counts.sort()
    card_counts = tuple(card_counts)
    card_counts_2_multiplier = {(5,): 6,  # 5 of a kind
                                (1, 4): 5,  # 4 of a kind
                                (2, 3): 4,  # Full house
                                (1, 1, 3): 3,  # 3 of a kind
                                (1, 2, 2): 2,  # 2 pair
                                (1, 1, 1, 2): 1,  # 1 pair
                                (1, 1, 1, 1, 1): 0,  # High card
                                }
    multiplier = card_counts_2_multiplier[card_counts]
    return multiplier * (14 ** 5)  # 5 since 0-4 will be used by card strength


def compare_hand(hand, part):
    """
    Custom ranker used to sort hands.
    Assigns a value to a hand based on how good it is.
    """
    if part == 2 and 'J' in hand:
        modified_hand = convert_joker(hand)
        hand_strength = get_hand_strength(modified_hand)
    else:
        hand_strength = get_hand_strength(hand)
    card_strength = get_card_strength(hand, part)
    strength = hand_strength + card_strength
    return strength


def part1(file):
    hands_and_bids = read_input(file)
    hands_and_bids.sort(key=lambda x: compare_hand(x[0], 1))
    tot_winnings = sum([(i + 1) * bid
                        for i, (_, bid) in enumerate(hands_and_bids)
                        ])
    print(f"Part 1: {tot_winnings}")


def part2(file):
    hands_and_bids = read_input(file)
    hands_and_bids.sort(key=lambda x: compare_hand(x[0], 2))
    tot_winnings = sum([(i + 1) * bid
                        for i, (_, bid) in enumerate(hands_and_bids)
                        ])
    print(f"Part 2: {tot_winnings}")


file = "input.in"
part1(file)
part2(file)
