"""

Input Notation
c : clubs
d : diamonds
h : hearts
s : spades
1 : ace
2 : two
3 : three
4 : four
5 : five
6 : six
7 : seven
8 : eight
9 : nine
10 : ten
11 : jack
12 : queen
13 : king

Format:
    Place suit first, then number for card inputs
    suits are alphabetical

Numbers Array:
index - 1 = card number; Ace has two values
eg: Two = 1; Ace = 0 or 13

=================================================================================
To do list:
    Announce more than one winner if needed, and match winning hand to seat position.
    Build GUI to facilitate hand comparison
    Include chance to win percentages to show hand strength from current community board

Notes:
    Accept two hands as input and then compare the two** Done
    - Need to accept multiple hands and store them.
    - Consider using *args or **kwargs
    - May want to store number of hands in play, use "If hand is None:" to eliminate empty seat position
    Show the 5 best cards with the type of hand** Done
    - Reference the original 7 cards for the final hand by reformatting get_all_cards function
    - Work on straight flush func
    Write "get" functions if check function is true**
    Consolidate cards_array** Done
    Use better return statements (like quads)** Done
    Remove None value from a list without removing the 0 value **Done
    Goal: Try to use any number of cards (preflop, flop, turn, river)** Done
=================================================================================

"""
import re


class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.num = number

    def __repr__(self):
        return self.suit + str(self.num)

    # def __str__(self):
    #    return self.suit + str(self.num)


class Hand:
    def __init__(self, preflop_cards, community_cards):
        self.pre_cards = preflop_cards
        self.comm_cards = community_cards
        # self.index = len(preflop_cards) + len(community_cards)
        self.cards = self.possible_cards()
        self.num_array = [0] * 14
        self.hand_position = []

    # Output is an array that include the community cards with the hand
    def create_player_hand(self):
        array = []
        for x in range(0, 2):
            if self.pre_cards[x] is None:
                return None
            array.append(self.pre_cards[x])
        for y in range(0, 5):
            array.append(self.comm_cards[y])
        return array

    # Remove None values from the card list
    def possible_cards(self):
        index = 0
        array_length = 7
        self.cards = self.create_player_hand()
        while index < array_length and self.cards:
            # if self.cards[index].suit is None or self.cards[index].num is None:
            if self.cards[index] is None:
                del self.cards[index]
                array_length -= 1
                index -= 1
            index += 1
        return self.cards

    # assign values of 1 or more for numerical cards in play and zeros for cards not in play
    # @staticmethod
    # def cards_number_array(cards):
    #     num_array = [0] * 14
    #     for y in range(0, len(cards)):
    #         num_array[cards[y].num - 1] += 1
    #         # Increment first and last element of array for aces
    #         if cards[y].num == 1:
    #             num_array[13] += 1
    #     return num_array

    # assign values of 1 or more for numerical cards in play and zeros for cards not in play
    @staticmethod
    def cards_number_array(cards):
        num_array = [0] * 14
        cards = repr(cards)
        card_list = re.findall(r'[0-9]+', cards)
        for y in range(0, len(card_list)):
            card_list[y] = int(card_list[y])
            num_array[card_list[y] - 1] += 1
            # Increment first and last element of array for aces
            if card_list[y] == 1:
                num_array[13] += 1
        return num_array

    def get_num_array(self):
        self.cards = self.possible_cards()
        array = self.cards_number_array(self.cards)
        return array


class HandType:
    def __init__(self, number_array, cards_array):
        self.num_array = number_array
        self.cards = cards_array
        self.index = len(cards_array)
        self.hc_index = 5
        self.name = "High Card"
        self.flush_suit = None
        self.suited_array = None

    def check_high_card(self, index):
        i = 1
        high_cards = []
        for x in range(13, 0, -1):
            if self.num_array[x] == 1:
                high_cards.append(x)
                i += 1
                if i > index:
                    break
            if index == 1:
                if self.num_array[x] == 2:
                    high_cards.append(x)
                    break
        return high_cards

    def check_pair(self):
        pair = False
        pair_card = []
        for x in range(1, 14):
            if self.num_array[x] == 2:
                pair_card.append(x)
                pair = True
                self.hc_index = 3
                break
        tie_breaker_cards = self.check_high_card(self.hc_index)
        if pair:
            pass
        return pair, pair_card, tie_breaker_cards

    def check_two_pair(self):
        two_pair = False
        number = 0
        two_pair_cards = []
        for x in range(13, 0, -1):
            if self.num_array[x] == 2:
                number += 1
                two_pair_cards.append(x)
            if number == 2:
                two_pair = True
                self.hc_index = 1
                break
        tie_breaker_cards = self.check_high_card(self.hc_index)
        if two_pair:
            pass
        return two_pair, two_pair_cards, tie_breaker_cards

    def check_trips(self):
        trips = False
        trips_card = []
        for x in range(1, 14):
            if self.num_array[x] == 3:
                trips_card.append(x)
                trips = True
                self.hc_index = 2
                break
        tie_breaker_cards = self.check_high_card(self.hc_index)
        if trips:
            pass
        return trips, trips_card, tie_breaker_cards

    @staticmethod
    def check_straight(array):
        straight = False
        straight_cards = []
        for x in range(13, 0, -1):
            if array[x] >= 1:
                number = 0
                for y in range(0, 5):
                    if 0 <= x-y < 14 and array[x-y] >= 1:
                        number += 1
                        straight_cards.append(x-y)
                    else:
                        break
                if number == 5:
                    straight = True
                    break
                else:
                    straight_cards = []
        return straight, straight_cards

    def check_flush(self):
        array = [0] * 4
        suits = ['c', 'd', 'h', 's']
        for y in range(0, self.index):
            if self.cards[y].suit == 'c':
                array[0] += 1
            elif self.cards[y].suit == 'd':
                array[1] += 1
            elif self.cards[y].suit == 'h':
                array[2] += 1
            elif self.cards[y].suit == 's':
                array[3] += 1
        for x in range(0, 4):
            if array[x] >= 5:
                self.flush_suit = suits[x]
                self.get_cards_flush(self.flush_suit)
                return True, self.flush_suit
        return False, None

    # returns the cards for the flush:
    def get_cards_flush(self, suit):
        suited_array = [0] * 14
        for x in range(0, self.index):
            if self.cards[x].suit == suit:
                suited_array[self.cards[x].num - 1] = 1
                if self.cards[x].num == 1:
                    suited_array[13] = 1
        i = 1
        high_card = []
        for y in range(13, 0, -1):
            if suited_array[y] == 1:
                high_card.append(y)
                i += 1
                if i > 5:
                    break
        return high_card

    def check_full_house(self):
        have_trips = False
        have_pair = False
        trips_card = []
        pair_card = []
        for x in range(13, 0, -1):
            if self.num_array[x] == 3:
                trips_card.append(x)
                have_trips = True
                break
        for y in range(13, 0, -1):
            if have_trips and 1 < self.num_array[y] < 4 and y != trips_card[0]:
                pair_card.append(y)
                have_pair = True
                break
        return have_pair and have_trips, trips_card, pair_card

    def check_quads(self):
        quads = False
        quads_card = []
        for x in range(1, 14):
            if self.num_array[x] == 4:
                quads = True
                quads_card.append(x)
                self.hc_index = 1
                break
        tie_breaker_cards = self.check_high_card(self.hc_index)
        return quads, quads_card, tie_breaker_cards

    def check_straight_flush(self, suit):
        self.suited_array = [0]*14
        for x in range(0, self.index):
            if self.cards[x].suit == suit:
                self.suited_array[self.cards[x].num - 1] = 1
                if self.cards[x].num == 1:
                    self.suited_array[13] = 1
        return self.check_straight(self.suited_array)

    # Return final 5 cards for the hand.
    # get all cards : investigate why len() is used for the two nested loops
    def get_final_cards(self, hand_cards, high_cards):
        final_cards = []
        index = 0
        for z in range(0, self.index):
            for x in range(0, len(hand_cards)):
                if hand_cards[x] == 13:
                    hand_cards[x] = 0
                if self.cards[z].num - 1 == hand_cards[x]:
                    final_cards.append(self.cards[z])
                if len(final_cards) == 5:
                    print(final_cards)
                    return final_cards
            for y in range(0, len(high_cards)):
                if self.hc_index == index:
                    break
                # Ace is 1 in self.cards; Ace is 13 in high_cards.
                if high_cards[y] == 13:
                    high_cards[y] = 0
                if self.cards[z].num - 1 == high_cards[y] and high_cards:
                    final_cards.append(self.cards[z])
                    index += 1
                if len(final_cards) == 5:
                    print(final_cards)
                    return final_cards
        print("Error with get_all_cards")
        return True

    # Check for all possible hands and return the current best possible
    def check_hand_strength(self):
        # 9 possible hands
        possible_hands = ['High Card', 'Pair', 'Two Pair', 'Trips', 'Straight', 'Flush', 'Full House', 'Quads',
                          'Straight Flush']
        self.name = possible_hands[0]
        empty = []
        final_hand_cards = []
        final_high_cards = []
        current_hand_strength = 0

        # check hand for pair and return 5 cards for final hand
        check_pair_boolean, paired_card, pair_high_cards = self.check_pair()
        if check_pair_boolean:
            self.name = possible_hands[1]
            final_hand_cards = paired_card
            final_high_cards = pair_high_cards
            current_hand_strength = 1

        # check hand for pair and return 5 cards for final hand
        check_two_pair_boolean, two_paired_cards, two_paired_high_card = self.check_two_pair()
        if check_two_pair_boolean:
            self.name = possible_hands[2]
            final_hand_cards = two_paired_cards
            final_high_cards = two_paired_high_card
            current_hand_strength = 2

        # check hand for pair and return 5 cards for final hand
        check_trips_boolean, trips_card, trips_high_cards = self.check_trips()
        if check_trips_boolean:
            self.name = possible_hands[3]
            final_hand_cards = trips_card
            final_high_cards = trips_high_cards
            current_hand_strength = 3

        straight_boolean, straight_cards = self.check_straight(self.num_array)
        if straight_boolean:
            self.name = possible_hands[4]
            final_hand_cards = straight_cards
            final_high_cards = empty
            current_hand_strength = 4

        flush_boolean, flush_suit = self.check_flush()
        if self.check_flush()[0]:
            flush_cards = self.get_cards_flush(flush_suit)
            final_hand_cards = flush_cards
            final_high_cards = empty
            self.name = possible_hands[5]
            current_hand_strength = 5

        check_full_house_boolean, trips_card, pair_card = self.check_full_house()
        if check_full_house_boolean:
            final_hand_cards = trips_card
            final_high_cards = pair_card
            self.name = possible_hands[6]
            current_hand_strength = 6

        check_quads_boolean, quads_card, high_card = self.check_quads()
        if check_quads_boolean:
            final_hand_cards = quads_card
            final_high_cards = high_card
            self.name = possible_hands[7]
            current_hand_strength = 7

        if straight_boolean and flush_boolean:
            straight_flush_boolean, straight_flush_cards = self.check_straight_flush(flush_suit)
            if straight_flush_boolean:
                self.name = possible_hands[8]
                final_hand_cards = straight_flush_cards
                final_high_cards = empty
                current_hand_strength = 8

        if self.name == possible_hands[0]:
            final_hand_cards = self.check_high_card(self.hc_index)
            final_high_cards = empty

        final_cards = self.get_final_cards(final_hand_cards, final_high_cards)
        print(self.name)
        return current_hand_strength, final_cards

    def get_hand_details(self):
        return self.check_hand_strength(), self.get_final_cards


class HandCompare:
    def __init__(self, hand_details):

        self.hand_details = hand_details
        self.hand_strength_list = []
        self.hand_strength = []
        self.tied_hands = []
        self.hand_position = [0] * 10

    def only_hand_strength(self):
        for x in range(0, len(self.hand_details)):
            self.hand_strength_list.append(self.hand_details[x][0])

    # max hand strength is not working as intended. grabbing hand and strength
    def compare_hand_strength(self):
        self.only_hand_strength()
        self.hand_strength = max(self.hand_strength_list)
        hand_occurrences = self.hand_strength_list.count(max(self.hand_strength_list))
        best_hand = []
        if hand_occurrences == 1:
            for x in range(0, len(self.hand_details)):
                if self.hand_strength == self.hand_details[x][0]:
                    best_hand = self.hand_details[x][1]
        elif hand_occurrences == 2:
            for y in range(0, len(self.hand_details)):
                if self.hand_strength == self.hand_details[y][0]:
                    self.tied_hands.append(self.hand_details[y][1])
            best_hand = self.find_tie_break()
        elif hand_occurrences > 2:
            pass
            # this statement is used to break more than 1 tie
        # print(best_hand)
        return best_hand

    # index 0: takes hand strength, index 1 and 2 take the two hands and compares them
    def find_tie_break(self):
        best_hand = []
        # need to determine how to announce more than one tie breaking winner
        # print(len(best_hand)) **this can be used to determine if we need to denote more than 1 winning hand
        if self.hand_strength != 1 and self.hand_strength != 2 and self.hand_strength != 3 and self.hand_strength != 7:
            print('tied breaker engaged')
            # super().cards_number_array(self.tied_hand[1])
            hand_to_compare1 = Hand.cards_number_array(self.tied_hands[0])
            # print(self.tied_hands[2])
            if self.tied_hands[1]:
                hand_to_compare2 = Hand.cards_number_array(self.tied_hands[1])
                for x in range(13, 0, -1):
                    if hand_to_compare1[x] > hand_to_compare2[x]:
                        best_hand.append(self.tied_hands[1])
                        return best_hand
                    if hand_to_compare2[x] > hand_to_compare1[x]:
                        best_hand.append(self.tied_hands[1])
                    return best_hand
        # return both hands if tie is not broken
        # could also consider using tie_broken_boolean
        best_hand.append(self.tied_hands[0])
        best_hand.append(self.tied_hands[1])
        return best_hand


def main():
    # Cards in play:
    preflophand1 = [Card('s', 9,), Card('s', 3)]
    preflophand2 = [Card('d', 2), Card('h', 7)]
    preflophand3 = None
    preflophand4 = None
    preflophand5 = [Card('s', 1), Card('s', 12)]
    preflophand6 = None
    preflophand7 = None
    preflophand8 = None
    preflophand9 = None
    preflophand10 = None
    preflophands = [preflophand1, preflophand2, preflophand3, preflophand4, preflophand5,
                    preflophand6, preflophand7, preflophand8, preflophand9, preflophand10]
    hand_position = [0] * 10

    # remove 'None' hands from pre flop cards array
    # consider using this with create_player_hand to remove empty preflop hands and store position
    for x in range(0, 10):
        if preflophands[x] is not None:
            hand_position[x] = 1
    print(hand_position)
    index = 0
    array_length = 10
    while index < array_length and preflophands:
        if preflophands[index] is None:
            del preflophands[index]
            array_length -= 1
            index -= 1
        index += 1

    flop1 = Card('s', 8)
    flop2 = Card('s', 11)
    flop3 = Card('s', 10)
    turn = Card('s', 13)
    river = None
    # river = (None, None)
    community_cards = [flop1, flop2, flop3, turn, river]

    hands = []
    hand_strengths = []
    all_hand_details = []
    for x in range(0, index):
        hands.append(Hand(preflophands[x], community_cards))
        hand_strengths.append(HandType(hands[x].get_num_array(), hands[x].possible_cards()))
        all_hand_details.append(hand_strengths[x].check_hand_strength())
    winning_hand = HandCompare(all_hand_details)
    print("Winning hand is:", winning_hand.compare_hand_strength())

    # all_preflop_hands, number_of_hands, hand_positions = all_hands(hands)
    # may not need hand positions #
    # hands are numerically ordered in accordance with their seat position #
    # this can be used to match winner with seat position #
    # player_hands = create_player_hand(all_preflop_hands, community_cards, number_of_hands)

    # Functions to check hand combinations:
    # compare_hand_strength(all_hand_details, only_strengths)


if __name__ == "__main__":
    main()

