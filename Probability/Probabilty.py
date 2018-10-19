

from SolvePokerHands import *
from CurrentHand import *


# to do: modify cards from comm_cards to test out probability.
# IMPORTANT: **need accurate tracking of the seat number**
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
        if len(self.community_cards) == 4:
            self.one_card_remaining()
        elif len(self.community_cards) == 3:
            self.two_cards_remaining()
        elif len(self.community_cards) == 0:
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

    # need to create the card, append it to community cards, then send it to solver
    # assume 4 community cards when entering this function
    def one_card_remaining(self):
        # prints out the number of cards in the deck
        for y in range(0, len(self.deck_num_array)):
            if self.deck_num_array[y] >= 1:
                for z in range(0, len(self.deck)):
                    if y+1 == self.deck[z].num:
                        # print(self.deck[z].num)
                        self.community_cards.append(self.deck[z])
                        print(self.community_cards)
                        print('\n\n')
                        winning_hand = HandCompare(preflophands, self.community_cards)
                        display_final = ['tied hand(s): ' + str(winning_hand.seat_position),
                                         winning_hand.get_winning_hand(),
                                         winning_hand.get_winning_cards()]
                        print(display_final)
                        print('\n\n')
                        self.community_cards.pop()
                        break
            # print(self.deck_num_array[y])

    def two_cards_remaining(self):
        pass

    def five_cards_remaining(self):
        pass


currenthand = CurrentHand(10, 2000)
preflophands = []
remaining_deck = []
community_cards = []
for x in range(0, 4):
    community_cards.append(currenthand.get_card())
for x in range(0, len(currenthand.player_cards)):
    preflophands.append(currenthand.player_cards[x][1])
    # print('seat number: ' + str(x + 1) + '  ' + str(preflophands[x]))
for x in range(0, len(currenthand.deck.current_cards)):
    remaining_deck.append(currenthand.get_card())
calculateProbability = Probability(remaining_deck, preflophands, community_cards)
# calculateProbability.number_of_cards_remaining()
# calculateProbability.one_card_remaining()
