# from SolvePokerHands import *
from Probability.Probability import Probability
from Table import Deck, Card

# import sys
# sys.stdout = open('DebugTests.txt', 'w')

# ===============================================================
# ===============================================================
# start of specified tests in HandCompare.py
# ===============================================================
# ===============================================================

# test hand bug (Seat position is incorrect)
# **FIXED**
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

# Bug: creates an error when the board shows a full house. quads does not show.
# preflop_cards = [[Card('c', 13), Card('c', 12)], [Card('h', 6), Card('d', 6)]]
# community_cards = [Card('s', 6), Card('c', 6), Card('c', 7)]
# Problem: Check high card only appends instances of 1 card.
# **FIXED** Check high card should append a card of 7 even though there is more than 1 instance of it.
# Solution: added special case high card search for quads

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

# Keep for tough tests
# Bug: Returns the incorrect percentages
# **FIXED**
# Bug: Does not credit 6 high straight to win vs wheel
# **FIXED**
# Bug: unknown
# preflop_cards = [[Card('s', 10), Card('s', 1)], [Card('h', 7), Card('c', 11)], [Card('c', 13), Card('h', 1)],
# [Card('s', 6), Card('h', 2)], [Card('d', 11), Card('h', 11)]]
# community_cards = [Card('h', 9), Card('s', 3), Card('c', 5)]
# expected-- Winning chances: [5.8, 5.26, 19.3, 20.51, 49.12]
# end of test

# =================
# code to test bugs
# =================


# To do:
# on button click, collect all the preflop and community cards
# need a way to only
# preflop_cards = get_preflop_cards()
# community_cards = get_community_cards()
# self.Run.clicked.connect(self.debug.run_tests)  # runs pokerUI.py


class Debug:
    def __init__(self):
        # initialize deck with all 52 cards
        self.deck = Deck()
        self.current_cards = self.deck.current_cards
        self.deck_length = len(self.current_cards)
        self.preflop_cards = []
        self.community_cards = []
        self.stats = None

    def run_debug_tests(self):
        self.preflop_cards = preflop_cards
        self.community_cards = community_cards
        self.run_tests()

    def new_deck(self):
        self.deck = Deck()
        self.current_cards = self.deck.current_cards
        self.deck_length = len(self.current_cards)

    def run_tests(self):
        self.new_deck()
        # remove preflop_cards from deck
        for x in range(0, len(self.preflop_cards)):
            index = 0
            second_card = 0
            while self.deck_length > index:
                if self.preflop_cards[x][second_card] == self.current_cards[index]:
                    return_value = self.current_cards.pop(index)
                    print("Card removed from deck: ", return_value)
                    self.deck_length -= 1
                    index = -1  # reset to front of deck
                    if second_card:  # end of current hand
                        break
                    second_card = 1  # cycle to second preflop card
                index += 1

        # remove community_cards from deck
        for y in range(0, len(self.community_cards)):
            index = 0
            while self.deck_length > index:
                if self.community_cards[y] == self.current_cards[index]:
                    return_value = self.current_cards.pop(index)
                    print("Card removed from deck: ", return_value)
                    self.deck_length -= 1
                    break
                index += 1
        print('\n')
        self.stats = Probability(self.current_cards, self.preflop_cards, self.community_cards)
        print(self.preflop_cards)
        print(self.community_cards)


# Run Probability on the current cards
# dbug = Debug()
# dbug.run_debug_tests()
