from SolvePokerHands import *
from Probability.Probability import Probability
from Table import Deck

# import sys
# sys.stdout = open('DebugTests.txt', 'w')

# ===============================================================
# ===============================================================
# start of specified tests in HandCompare.py
# ===============================================================
# ===============================================================

# test hand bug (Seat position is incorrect)
# preflop_cards = [[Card('h', 3), Card('c', 13)], [Card('s', 12), Card('s', 9)], [Card('d', 6), Card('d', 5)],
#                 [Card('d', 13), Card('c', 2)], [Card('h', 4), Card('h', 9)], [Card('s', 1), Card('s', 6)],
#                 [Card('c', 7), Card('s', 8)], [Card('h', 13), Card('d', 2)], [Card('d', 3), Card('c', 3)],
#                 [Card('c', 8), Card('h', 7)]]
# community_cards = [Card('c', 5), Card('d', 10), Card('c', 10), Card('c', 9), Card('h', 10)]
# end of test

# Test quads
# **FIXED**
# preflop_cards = [[Card('h', 1), Card('c', 1)], [Card('d', 6), Card('c', 9)], [Card('c', 7), Card('s', 7)],
#                 [Card('h', 11), Card('h', 8)], [Card('s', 3), Card('h', 4)], [Card('d', 12), Card('h', 10)],
#                 [Card('c', 11), Card('h', 6)], [Card('d', 13), Card('c', 13)], [Card('s', 5), Card('h', 5)],
#                 [Card('h', 12), Card('s', 10)]]
# community_cards = [Card('d', 1), Card('d', 5), Card('s', 1), Card('d', 3), Card('c', 5)]
# end of test

# Bug: nested lists
# **FIXED** the error was adding a nested list
# preflop_cards = [[Card('h', 5), Card('s', 11)], [Card('c', 12), Card('s', 8)], [Card('s', 5), Card('h', 8)],
# [Card('h', 13), Card('s', 3)], [Card('s', 1), Card('h', 9)], [Card('h', 1), Card('s', 4)],
# [Card('h', 10), Card('d', 11)], [Card('c', 4), Card('h', 12)], [Card('d', 6), Card('h', 2)],
# [Card('d', 2), Card('h', 4)]]
# community_cards = [Card('d', 5), Card('s', 13), Card('c', 7), Card('c', 2), Card('c', 1)]
# end of test

# Test multiple winner (not returning both seat positions)
# **FIXED** Involves the try and except statements to create correct variable type
# preflop_cards = [[Card('h', 9), Card('d', 3)], [Card('d', 5), Card('c', 3)], [Card('s', 5), Card('d', 9)],
# [Card('d', 6), Card('h', 2)], [Card('s', 6), Card('d', 7)], [Card('h', 6), Card('c', 5)],
# [Card('c', 4), Card('h', 8)], [Card('h', 7), Card('c', 8)], [Card('d', 4), Card('d', 1)],
# [Card('s', 1), Card('s', 4)]]
# community_cards = [Card('h', 1), Card('d', 10), Card('s', 7), Card('s', 13), Card('c', 9)]
# end of test

# Bug: Returns incorrect winning hand
# Fix: card number array needs to remove ace from the low end unless the hand is a straight (Ace-5)
# **FIXED** required setting first value of card num array to zero inside find_tie_break
# preflop_cards = [[Card('h', 1), Card('s', 1)], [Card('s', 13), Card('c', 9)], [Card('d', 5), Card('c', 6)],
# [Card('s', 2), Card('d', 11)], [Card('d', 6), Card('h', 11)]]
# community_cards = [Card('c', 2), Card('d', 8), Card('h', 7)]
# end of test

# Keep this bug. Very good for testing. Good way to test seat position
# Bug: test hand bug (Removes winning straight during tie break)
# **FIXED** This bug occurs because the num array always increments the highest value when an Ace is present, therefore
# an ace with on the low end because the 6 to 2 straight because it compares with the high end ace.
# preflop_cards = [[Card('h', 4), Card('s', 12)], [Card('h', 7), Card('d', 8)], [Card('c', 1), Card('s', 3)],
#                 [Card('s', 5), Card('s', 8)], [Card('h', 2), Card('d', 12)], [Card('s', 10), Card('d', 1)],
#                 [Card('h', 6), Card('d', 10)], [Card('s', 1), Card('s', 6)], [Card('h', 9), Card('c', 8)],
#                 [Card('h', 1), Card('s', 7)]]
# community_cards = [Card('c', 3), Card('h', 5), Card('c', 4), Card('h', 3), Card('c', 2)]
# end of test

# =================
# code to test bugs
# =================

# print("Preflop cards: " + str(preflop_cards))
# print("Community cards: " + str(community_cards))
# winning_hand = HandCompare(preflop_cards, community_cards)
# winning_hand.print_winning_hand()

# ===============================================================
# ===============================================================
# start of specified tests in # Probability.py
# ===============================================================
# ===============================================================

# Bug: Incorrect odds; Disagrees with two other calculators (which also happen to disagree with each other)
# preflop_cards = [[Card('s', 10), Card('s', 1)], [Card('h', 7), Card('c', 11)], [Card('c', 13), Card('h', 1)],
# [Card('s', 6), Card('h', 2)], [Card('d', 11), Card('h', 11)]]
# community_cards = [Card('h', 9), Card('s', 3), Card('c', 5)]
# end of test

# Bug: Incorrect odds; Full house 10s full aces beats Ks full of tens
# Solution: need to compare the trips cards first
# Bug (new): Quads returns the wrong winning seat and deletes other hand
preflop_cards = [[Card('h', 10), Card('s', 1)], [Card('c', 13), Card('h', 11)]]
community_cards = [Card('h', 13), Card('s', 13), Card('c', 10)]
# end of test
# =================
# code to test bugs
# =================

deck = Deck()
current_cards = deck.current_cards
deck_length = len(current_cards)
for x in range(0, len(preflop_cards)):
    index = 0
    while deck_length > index:
        if preflop_cards[x] == current_cards[index]:
            current_cards.pop(index)
            deck_length -= 1
            break
        index += 1
for y in range(0, len(community_cards)):
    index = 0
    while deck_length > index:
        if community_cards[y] == current_cards[index]:
            current_cards.pop(index)
            deck_length -= 1
            break
        index += 1
Probability(current_cards, preflop_cards, community_cards)
print(preflop_cards)
print(community_cards)
