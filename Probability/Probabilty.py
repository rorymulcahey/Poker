

from SolvePokerHands import *
from CurrentHand import *
from collections import Counter


# to do: modify cards from comm_cards to test out probability.
class Probability:
    def __init__(self, remaining_deck, preflop_hands, comm_cards):
        self.community_cards = comm_cards
        self.preflop_hands = preflop_hands
        self.percentage = 100
        self.winning_hands = 1
        self.total_hands = 2
        self.num_of_players = 2
        self.cards_remaining = 1
        self.current_deck = remaining_deck.copy()
        self.current_cards_in_play = Hand(preflop_hands, self.community_cards)
        self.deck_num_array = []
        self.create_deck_num_array()

    def create_deck_num_array(self):
        # first need to create card number array from the remaining cards in the deck
        return self.current_cards_in_play.cards_number_array(self.current_deck)

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

    # Original version without flush cards

    # need to create the card, append it to community cards, then send it to solver
    # must have a numerically sorted deck
    # assume 4 community cards when entering this function
    # solve for all cards of suit if > than 2 suits are present.
    # def one_card_remaining(self):
    #     total = len(self.current_deck)
    #     winning_chances = len(self.preflop_hands) * [0]
    #     drawing_chances = len(self.preflop_hands) * [0]
    #     w = -1  # increases the speed by changing starting point of picking a card to test
    #     for y in range(0, len(self.deck_num_array)-1):
    #         w += self.deck_num_array[y]  # relies on numerically sorted deck
    #         if self.deck_num_array[y] > 0:
    #             # print(self.deck[z].num)
    #             self.community_cards.append(self.current_deck[w])
    #             # print(self.community_cards)
    #             # print('\n')
    #             winning_hand = HandCompare(self.preflop_hands, self.community_cards)
    #             display_final = ['Winning hand seat(s): ' +
    #                              str(winning_hand.get_winning_seat_position()),
    #                              winning_hand.get_winning_hand(),
    #                              winning_hand.get_winning_cards()]
    #
    #             winning_seat = winning_hand.get_winning_seat_position()  # needs to hand list
    #             # need to account for draws
    #             # try or if(non draws)
    #             # except or else (draws)
    #             if len(winning_seat) == 1:
    #                 winning_chances[winning_seat[0] - 1] += self.deck_num_array[y]
    #             else:  # drawing chances
    #                 for i in range(0, len(winning_seat)):
    #                     drawing_chances[winning_seat[i] - 1] += self.deck_num_array[y]
    #             print(display_final)
    #             print('Community cards: ' + str(community_cards))
    #             print('\n')
    #             self.community_cards.pop()
    #             # break
    #             # print(self.deck_num_array[y])
    #     winning_chances[:] = [round(j * 100 / total, 2) for j in winning_chances]
    #     drawing_chances[:] = [round(k * 100 / total, 2) for k in drawing_chances]
    #     print(winning_chances)
    #     print(drawing_chances)

    def one_card_remaining(self):
        total = len(self.current_deck)
        winning_chances = len(self.preflop_hands) * [0]
        drawing_chances = len(self.preflop_hands) * [0]
        flush_suit = []
        deck_num_array = self.create_deck_num_array()
        for z in range(0, 4):
            flush_suit.append(self.community_cards[z].suit)
        flush_suit = Counter(flush_suit).most_common(1)
        if flush_suit[0][1] > 1:
            flush_suit = flush_suit[0][0]
        else:
            flush_suit = None
        if flush_suit:
            length = len(self.current_deck)
            y = 0
            while length > y:
                if self.current_deck[y].suit == flush_suit:
                    self.community_cards.append(self.current_deck[y])
                    winning_hand = HandCompare(self.preflop_hands, self.community_cards)
                    display_final = ['Winning hand seat(s): ' +
                                     str(winning_hand.get_winning_seat_position()),
                                     winning_hand.get_winning_hand(),
                                     winning_hand.get_winning_cards()]
                    winning_seat = winning_hand.get_winning_seat_position()  # needs to hand list
                    if len(winning_seat) == 1:
                        winning_chances[winning_seat[0] - 1] += 1
                    else:  # drawing chances
                        for i in range(0, len(winning_seat)):
                            drawing_chances[winning_seat[i] - 1] += 1
                    print(display_final)
                    print('Community cards: ' + str(community_cards))
                    print('\n')
                    self.community_cards.pop()
                    deck_num_array[self.current_deck[y].num-1] -= 1
                    self.current_deck.pop(y)
                    length -= 1
                    y -= 1
                y += 1
        print(self.current_deck)
        print(deck_num_array)
        print(flush_suit)
        w = -1  # increases the speed by immediately picking a card
        for y in range(0, len(deck_num_array)-1):
            w += deck_num_array[y]  # relies on numerically sorted deck
            if deck_num_array[y] > 0:
                self.community_cards.append(self.current_deck[w])
                winning_hand = HandCompare(self.preflop_hands, self.community_cards)
                display_final = ['Winning hand seat(s): ' +
                                 str(winning_hand.get_winning_seat_position()),
                                 winning_hand.get_winning_hand(),
                                 winning_hand.get_winning_cards()]

                winning_seat = winning_hand.get_winning_seat_position()  # needs to hand list
                # need to account for draws
                if len(winning_seat) == 1:
                    winning_chances[winning_seat[0] - 1] += deck_num_array[y]
                else:  # drawing chances
                    for i in range(0, len(winning_seat)):
                        drawing_chances[winning_seat[i] - 1] += deck_num_array[y]
                print(display_final)
                print('Community cards: ' + str(community_cards))
                print('\n')
                self.community_cards.pop()
        winning_chances[:] = [round(j * 100 / total, 2) for j in winning_chances]
        drawing_chances[:] = [round(k * 100 / total, 2) for k in drawing_chances]
        print("Winning chances: " + str(winning_chances))
        print("Drawing chances: " + str(drawing_chances))

    def two_cards_remaining(self):
        pass

    def five_cards_remaining(self):
        pass


ch = CurrentHand(3, 2000)
pre = []
# dck = []
community_cards = []
for x in range(0, 4):
    community_cards.append(ch.get_card())
for x in range(0, len(ch.player_cards)):
    pre.append(ch.player_cards[x][1])
# for x in range(0, len(ch.deck.current_cards)):
#     dck.append(ch.get_card())
calculateProbability = Probability(ch.deck.current_cards, pre, community_cards)
calculateProbability.number_of_cards_remaining()
# calculateProbability.one_card_remaining()
