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
card - 1 = card number; Ace has two values
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


class Hand:
    def __init__(self, preflop_cards, community_cards):
        self.pre_cards = preflop_cards
        self.comm_cards = community_cards
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
        self.num_of_cards = len(cards_array)
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
        for y in range(0, self.num_of_cards):
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

    # returns the cards for the flush
    # needs to actually return cards for the flush because its sending non flush cards to final hand
    def get_cards_flush(self, suit):
        suited_array = [0] * 14
        for x in range(0, self.num_of_cards):
            if self.cards[x].suit == suit:
                suited_array[self.cards[x].num - 1] = 1
                if self.cards[x].num == 1:
                    suited_array[13] = 1
        i = 1
        flush_cards = []
        for y in range(13, 0, -1):
            if suited_array[y] == 1:
                flush_cards.append(y)
                i += 1
                if i > 5:
                    break
        return flush_cards

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
        for x in range(0, self.num_of_cards):
            if self.cards[x].suit == suit:
                self.suited_array[self.cards[x].num - 1] = 1
                if self.cards[x].num == 1:
                    self.suited_array[13] = 1
        return self.check_straight(self.suited_array)

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

        # check hand for pair, two pair, etc.. and return final hand w/ high cards
        check_pair_boolean, paired_card, pair_high_cards = self.check_pair()
        if check_pair_boolean:
            self.name = possible_hands[1]
            final_hand_cards = paired_card
            final_high_cards = pair_high_cards
            current_hand_strength = 1

        check_two_pair_boolean, two_paired_cards, two_paired_high_card = self.check_two_pair()
        if check_two_pair_boolean:
            self.name = possible_hands[2]
            final_hand_cards = two_paired_cards
            final_high_cards = two_paired_high_card
            current_hand_strength = 2

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
        print('^' + self.name)
        return current_hand_strength, final_cards

    # Return final 5 cards for the hand.
    # get all cards : investigate why len() is used for the two nested loops
    def get_final_cards(self, hand_cards, high_cards):
        final_cards = []
        index = 0
        if self.name == 'Flush' or 'Straight Flush':
            for z in range(0, self.num_of_cards):
                for x in range(0, len(hand_cards)):
                    if hand_cards[x] == 13:
                        hand_cards[x] = 0
                    if self.cards[z].num - 1 == hand_cards[x] and self.cards[z].suit == self.flush_suit:
                        final_cards.append(self.cards[z])
                    if len(final_cards) == 5:
                        print(final_cards)
                        return final_cards

        if self.name == 'Straight':
            for x in range(0, len(hand_cards)):
                for y in range(0, self.num_of_cards):
                    if hand_cards[x] == 13:
                        hand_cards[x] = 0
                    if self.cards[y].num - 1 == hand_cards[x]:
                        final_cards.append(self.cards[y])
                        if len(final_cards) == 5:
                            print(final_cards)
                            return final_cards
                        break

        # does not return correct straight cards if one of them is paired
        # this function checks each of the 7 playable cards and sees if the player has that number
        # therefore it takes pairs when it looks for straights.
        # better if we check the current hand_cards then find one that fits the criteria
        for z in range(0, self.num_of_cards):
            for x in range(0, len(hand_cards)):
                if hand_cards[x] == 13:
                    hand_cards[x] = 0
                if self.cards[z].num - 1 == hand_cards[x]:
                    final_cards.append(self.cards[z])
                if len(final_cards) == 5:
                    print(final_cards)
                    return final_cards

            for y in range(0, len(high_cards)):
                if self.hc_index == 0:
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
        return

    def get_hand_details(self):
        return self.check_hand_strength(), self.get_final_cards


class HandCompare:
    def __init__(self, hand_details):
        self.hand_details = hand_details
        self.hand_strength_list = []
        self.hand_strength = 0
        self.seat_position = []
        self.name = []
        self.best_hand = []
        self.multiple_tied_hands = False
        self.tied_hands = []
        self.tied_hand_seats = []
        self.compare_hand_strength()

    def best_hand_strength(self):
        for x in range(0, len(self.hand_details)):
            self.hand_strength_list.append(self.hand_details[x][0])
        self.hand_strength = max(self.hand_strength_list)

    def compare_hand_strength(self):
        self.best_hand_strength()
        possible_hands = ['High Card', 'Pair', 'Two Pair', 'Trips', 'Straight',
                          'Flush', 'Full House', 'Quads', 'Straight Flush']
        hand_occurrences = self.hand_strength_list.count(max(self.hand_strength_list))
        self.name = possible_hands[self.hand_strength]
        self.best_hand = []
        if hand_occurrences == 1:
            for x in range(0, len(self.hand_details)):
                if self.hand_strength == self.hand_details[x][0]:
                    self.best_hand = self.hand_details[x][1]
                    self.seat_position[0] = x + 1
        else:
            break_tied_hands = []
            for y in range(0, len(self.hand_details)):
                if self.hand_strength == self.hand_details[y][0]:
                    break_tied_hands.append(self.hand_details[y][1])
                    self.seat_position.append(y+1)
            if hand_occurrences == 2:
                self.best_hand = self.find_tie_break(break_tied_hands, self.seat_position)
            else:  # hand_occurrences > 2:
                # case 1: all hands tie
                # case 2: 1 and 3 tie
                # case 3: N/A
                # solution: compare for loop forwards then backwards
                # problem: need to store multiple winning hands
                temp = []
                first_correct_hand = self.find_tie_break([break_tied_hands[0], break_tied_hands[1]], self.seat_position)
                if first_correct_hand is None:
                    temp.extend([break_tied_hands[0], break_tied_hands[1]])
                else:
                    temp.append(first_correct_hand)
                for y in range(1, len(break_tied_hands)-1):
                    print(y)
                    two_hands = []
                    two_hands.extend((temp[-1], break_tied_hands[y+1]))
                    # if first result is better, it returns itself causing a bug
                    check_return = self.find_tie_break(two_hands, self.seat_position)
                    if check_return is None:
                        temp.append(break_tied_hands[y+1])
                    else:
                        if temp[-1] != check_return:
                            print('testing inequality')
                            temp.append(check_return)
                self.best_hand.append(temp[len(temp)-1])
                # best hand can be initialized here because its going to be correct
                for z in range(len(temp)-1, 0, -1):
                    print(z)
                    two_hands = []
                    two_hands.extend((temp[z], temp[z-1]))
                    check_return = self.find_tie_break(two_hands, self.seat_position)
                    if check_return is None:
                        # self.best_hand.append(temp[len(temp) - z])
                        self.best_hand.append(temp[z-1])
                    else:
                        self.best_hand.append(check_return)
                    # seat position should be incorrect and we need to iterate backwards somehow

    # this function takes in two different hands of equal strength. it will break a tie and return the winning hand.
    # if tie cannot be broken it will return None
    # Need to implement seat_num
    def find_tie_break(self, tied_hand_details, seat_num):
        best_hand = []
        # function below only calculates hands with 5 determined cards without a high card tie break.
        if self.hand_strength != 1 and self.hand_strength != 2 and self.hand_strength != 3 and self.hand_strength != 7:
            print('tied breaker engaged')
            hand_to_compare0 = Hand.cards_number_array(tied_hand_details[0])
            print(hand_to_compare0)
            hand_to_compare1 = Hand.cards_number_array(tied_hand_details[1])
            print(hand_to_compare1)
            tie_broken = False
            for x in range(13, 0, -1):
                if hand_to_compare0[x] > hand_to_compare1[x]:
                    print('delete2')
                    best_hand.append(tied_hand_details[0])
                    del self.seat_position[1]
                    print(tied_hand_details[0])
                    return tied_hand_details[0]
                elif hand_to_compare1[x] > hand_to_compare0[x]:
                    print('delete1')
                    best_hand.append(tied_hand_details[1])
                    del self.seat_position[0]
                    return tied_hand_details[1]
                else:
                    pass
            # return none if tie is not broken
            if not tie_broken:
                print("Hands are the same. Returning None")
                return

    def get_winning_hand(self):
        return self.name

    def get_winning_cards(self):
        return self.best_hand



