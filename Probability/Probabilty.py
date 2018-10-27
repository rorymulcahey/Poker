

from SolvePokerHands import *
from CurrentHand import *
from collections import Counter
import timeit
# import sys
# sys.stdout = open('text.txt', 'w')


# to do: modify cards from comm_cards to test out probability.
class Probability:
    def __init__(self, remaining_deck, preflop_hands, comm_cards):
        self.community_cards = comm_cards
        self.preflop_hands = preflop_hands
        self.current_deck = remaining_deck
        self.current_cards_in_play = Hand(preflop_hands, self.community_cards)
        self.deck_num_array = self.create_deck_num_array(self.current_deck)
        self.winning_chances = len(self.preflop_hands) * [0]
        self.drawing_chances = len(self.preflop_hands) * [0]

    def create_deck_num_array(self, cards):
        return self.current_cards_in_play.cards_number_array(cards)

    def number_of_cards_remaining(self):
        total = len(self.current_deck)
        if len(self.community_cards) == 4:
            self.one_card_remaining(self.current_deck.copy())
        elif len(self.community_cards) == 3:
            self.two_cards_remaining(self.current_deck.copy())
            total *= total - 1
        elif len(self.community_cards) == 0:
            self.five_cards_remaining()
        else:
            print("bug with number of cards remaining")
        print(sum(self.winning_chances))
        print(sum(self.drawing_chances))
        print(total)
        self.winning_chances[:] = [round(j * 100 / total, 2) for j in self.winning_chances]
        self.drawing_chances[:] = [round(k * 100 / total, 2) for k in self.drawing_chances]
        print("Winning chances: " + str(self.winning_chances))
        print("Drawing chances: " + str(self.drawing_chances))

    def one_card_remaining(self, current_deck):
        deck_cards = current_deck
        self.deck_num_array = self.create_deck_num_array(current_deck)
        # total = len(deck_cards)
        # winning_chances = len(self.preflop_hands) * [0]
        # drawing_chances = len(self.preflop_hands) * [0]
        flush_suit = []
        for z in range(0, 4):
            flush_suit.append(self.community_cards[z].suit)
        flush_suit = Counter(flush_suit).most_common(1)
        if flush_suit[0][1] > 1:
            flush_suit = flush_suit[0][0]
        else:
            flush_suit = None
        if flush_suit:
            length = len(deck_cards)
            y = 0
            while length > y:
                if deck_cards[y].suit == flush_suit:
                    self.community_cards.append(deck_cards[y])
                    winning_hand = HandCompare(self.preflop_hands, self.community_cards)
                    # display_final = ['Winning hand seat(s): ' +
                    #                  str(winning_hand.get_winning_seat_position()),
                    #                  winning_hand.get_winning_hand(),
                    #                  winning_hand.get_winning_cards()]
                    winning_seat = winning_hand.get_winning_seat_position()  # needs hand list
                    self.calculate_winning_chances(winning_hand, winning_seat, None)
                    # if len(winning_seat) == 1:
                    #     winning_chances[winning_seat[0] - 1] += 1
                    # else:  # drawing chances
                    #     for i in range(0, len(winning_seat)):
                    #         drawing_chances[winning_seat[i] - 1] += 1
                    # print(display_final)
                    # print('Community cards: ' + str(community_cards))
                    # print('\n')
                    self.community_cards.pop()
                    self.deck_num_array[deck_cards[y].num - 1] -= 1
                    deck_cards.pop(y)
                    length -= 1
                    y -= 1
                y += 1
        # print(deck_cards)
        # print(len(deck_cards))  # returns correct results
        print('\n')
        print("==================================================================")
        print('\n')
        # print(flush_suit)

        '''
        This function uses a deck_cards number array, which increments the index of a list
        for each occurrence of a specific number of card. Very similar to the card
        number array that exists in the SolvePokerHands.py except this array looks
        for every card that is remaining in the deck_cards and only those cards. The function
        uses that deck_cards number array to iterate through all the possible hands that a 
        user can make. Then it multiplies the outcome of the hand by the number of 
        card occurrences that happen in the deck_cards. This reduces the number of times 
        the SolvePokerHands.py needs to run by approximately a factor of 3.
        '''
        w = -1  # increases the speed by immediately picking a card
        for y in range(0, len(self.deck_num_array)-1):
            w += self.deck_num_array[y]  # relies on numerically sorted deck_cards
            if self.deck_num_array[y] > 0:
                self.community_cards.append(deck_cards[w])
                winning_hand = HandCompare(self.preflop_hands, self.community_cards)
                # display_final = ['Winning hand seat(s): ' +
                #                  str(winning_hand.get_winning_seat_position()),
                #                  winning_hand.get_winning_hand(),
                #                  winning_hand.get_winning_cards()]
                winning_seat = winning_hand.get_winning_seat_position()  # needs hand list
                self.calculate_winning_chances(winning_hand, winning_seat, y)
                # if len(winning_seat) == 1:
                #     winning_chances[winning_seat[0] - 1] += self.deck_num_array[y]
                # else:  # drawing chances
                #     for i in range(0, len(winning_seat)):
                #         drawing_chances[winning_seat[i] - 1] += self.deck_num_array[y]
                # print(display_final)
                # print('Community cards: ' + str(community_cards))
                # print('\n')
                self.community_cards.pop()
        # winning_chances[:] = [round(j * 100 / total, 2) for j in winning_chances]
        # drawing_chances[:] = [round(k * 100 / total, 2) for k in drawing_chances]
        # print("Winning chances: " + str(winning_chances))
        # print("Drawing chances: " + str(drawing_chances))

    def two_cards_remaining(self, current_deck):
        # need a way to modify the the one community card and send the rest of the deck into one card remaining
        for x in range(0, len(current_deck)):
            deck_cards = current_deck
            self.community_cards.append(deck_cards[x])
            # print(deck_cards[x])
            # print(len(deck_cards))
            # print(deck_cards)
            deck_cards = [n for n in deck_cards if n != deck_cards[x]]  # removes deck_cards[x] from the deck
            # print(deck_cards)
            # print(len(deck_cards))
            # print('\n')
            self.one_card_remaining(deck_cards)
            self.community_cards.pop()

    def five_cards_remaining(self):
        pass

    def calculate_winning_chances(self, winning_hand, winning_seat, card_number):
        if card_number is not None:
            if len(winning_seat) == 1:
                self.winning_chances[winning_seat[0] - 1] += self.deck_num_array[card_number]
            else:  # drawing chances
                for i in range(0, len(winning_seat)):
                    self.drawing_chances[winning_seat[i] - 1] += \
                        float(self.deck_num_array[card_number])/len(winning_seat)
        else:
            if len(winning_seat) == 1:
                self.winning_chances[winning_seat[0] - 1] += 1
            else:  # drawing chances
                for i in range(0, len(winning_seat)):
                    self.drawing_chances[winning_seat[i] - 1] += (1.0/len(winning_seat))
        display_final = ['Winning hand seat(s): ' +
                         str(winning_hand.get_winning_seat_position()),
                         winning_hand.get_winning_hand(),
                         winning_hand.get_winning_cards()]
        print(display_final)
        print("Deck num array: " + str(self.deck_num_array))
        print('Community cards: ' + str(community_cards) + '\n')


start = timeit.default_timer()
ch = CurrentHand(3)
pre = []
# dck = []
community_cards = []
for g in range(0, 3):
    community_cards.append(ch.get_card())
for g in range(0, len(ch.player_cards)):
    pre.append(ch.player_cards[g][1])
# for x in range(0, len(ch.deck.current_cards)):
#     dck.append(ch.get_card())
calculateProbability = Probability(ch.deck.current_cards, pre, community_cards)
calculateProbability.number_of_cards_remaining()
stop = timeit.default_timer()
print('Time: ', stop - start)
# calculateProbability.one_card_remaining()


# Old Code
# Original version without flush cards

# need to create the card, append it to community cards, then send it to solver
# must have a numerically sorted deck
# assume 4 community cards when entering this function
# solve for all cards of suit if > than 2 suits are present.
# def one_card_remaining(self):
#     total = len(self.deck)
#     winning_chances = len(self.preflop_hands) * [0]
#     drawing_chances = len(self.preflop_hands) * [0]
#     w = -1  # increases the speed by changing starting point of picking a card to test
#     for y in range(0, len(self.deck_num_array)-1):
#         w += self.deck_num_array[y]  # relies on numerically sorted deck
#         if self.deck_num_array[y] > 0:
#             # print(self.deck[z].num)
#             self.community_cards.append(self.deck[w])
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
