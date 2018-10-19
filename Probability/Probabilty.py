

from SolvePokerHands import *
from CurrentHand import *


# to do: modify cards from comm_cards to test out probability.
class Probability:
    def __init__(self, deck, preflop_cards, comm_cards):
        self.community_cards = comm_cards
        self.percentage = 100
        self.winning_hands = 1
        self.total_hands = 2
        self.num_of_players = 2
        self.cards_remaining = 1
        self.deck = deck
        self.current_cards_in_play = Hand(preflop_cards, self.community_cards)
        self.deck_num_array = []
        self.create_deck_num_array()

    def create_deck_num_array(self):
        # first need to create card number array from the remaining cards in the deck
        self.deck_num_array = self.current_cards_in_play.cards_number_array(self.deck)

    def number_of_cards_remaining(self):
        if len(self.community_cards == 1):
            self.one_card_remaining()
        elif len(self.community_cards == 2):
            self.two_cards_remaining()
        elif len(self.community_cards == 5):
            self.five_cards_remaining()
        else:
            print("bug with number of cards remaining")

    def calculate(self):
        if self.cards_remaining == 0:
            return self.winning_hands/self.total_hands

    def collect_deck(self):
        pass
        # self.deck.append(self.currenthand.get_card())
        # Current collects deck from main
        # Need to instantiate deck or currenthand to work independent from main

    def one_card_remaining(self):
        # prints out the number of cards in the deck
        for y in range(0, len(self.deck_num_array)):
            print(self.deck_num_array[y])

    def two_cards_remaining(self):
        pass

    def five_cards_remaining(self):
        pass


currenthand = CurrentHand(10, 2000)
preflophands = []
remaining_deck = []
community_cards = []
for x in range(0, 5):
    community_cards.append(currenthand.get_card())
for x in range(0, len(currenthand.player_cards)):
    preflophands.append(currenthand.player_cards[x][1])
    # print('seat number: ' + str(x + 1) + '  ' + str(preflophands[x]))
for x in range(0, len(currenthand.deck.current_cards)):
    remaining_deck.append(currenthand.get_card())
calculateProbability = Probability(remaining_deck, preflophands, community_cards)

calculateProbability.one_card_remaining()
