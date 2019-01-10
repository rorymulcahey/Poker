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

======================================================================================================
To do list:
    Debug and test for hands that win when they should not.
    Build GUI to facilitate hand comparison.
    Add preflop probabilities
    Refactor possible cards. Remove if its not needed.

Bug:
preflop = [[Card('c', 13), Card('c', 12)], [Card('h', 6), Card('d', 6)]]
community cards = [Card('s', 6), Card('c', 6), Card('c', 7)]
Problem: Check high card only appends instances of 1 card.
Solution: Check high card should append a card of 7 even though there is more than 1 instance of it.

Notes:
    Probabilities are close but not exact. (Probably bugs here)

========================================================================================================

"""
import re


# class Card:
#     def __init__(self, suit, number):
#         self.suit = suit
#         self.num = number
#
#     def __repr__(self):
#         return self.suit + str(self.num)


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
        for y in range(0, len(self.comm_cards)):
            array.append(self.comm_cards[y])
        return array

    # Remove None values from the card list
    # currently suspending this function as these cards lists do not have None cards
    def possible_cards(self):
        index = 0
        array_length = 7
        self.cards = self.create_player_hand()
        return self.cards
        len(self.cards)
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
        self.num_of_high_cards = 5
        self.name = "High Card"
        self.flush_suit = None
        self.suited_array = None
        self.final_cards = []

    def check_high_card(self, index):
        i = 1
        high_cards = []
        for x in range(13, 0, -1):
            if self.num_array[x] == 1:
                high_cards.append(x)
                i += 1
                if i > index:
                    break
        return high_cards

    def check_pair(self):
        pair = False
        pair_card = []
        for x in range(13, 0, -1):
            if self.num_array[x] == 2:
                pair_card.append(x)
                pair = True
                self.num_of_high_cards = 3
                break
        tie_breaker_cards = self.check_high_card(self.num_of_high_cards)
        return pair, pair_card, tie_breaker_cards

    def check_two_pair(self):
        two_pair = False
        number = 0
        two_pair_cards = []
        tie_breaker_cards = []
        for x in range(13, 0, -1):
            if self.num_array[x] == 2:
                number += 1
                two_pair_cards.append(x)
            if number == 2:
                two_pair = True
                self.num_of_high_cards = 1
                break
        if two_pair:
            for x in range(13, 0, -1):
                if self.num_array[x] > 0 and x not in two_pair_cards:
                    tie_breaker_cards.append(x)
                    break
        return two_pair, two_pair_cards, tie_breaker_cards

    def check_trips(self):
        trips = False
        trips_card = []
        for x in range(1, 14):
            if self.num_array[x] == 3:
                trips_card.append(x)
                trips = True
                self.num_of_high_cards = 2
                break
        tie_breaker_cards = self.check_high_card(self.num_of_high_cards)
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
        tie_breaker_card = []
        for x in range(1, 14):
            if self.num_array[x] == 4:
                quads = True
                quads_card.append(x)
                self.num_of_high_cards = 1
                break
        for x in range(13, 0, -1):
            if self.num_array[x] >= 1 and self.num_array[x] != 4:
                tie_breaker_card.append(x)
                break
        return quads, quads_card, tie_breaker_card

    def check_straight_flush(self, suit):
        self.suited_array = [0]*14
        for x in range(0, self.num_of_cards):
            if self.cards[x].suit == suit:
                self.suited_array[self.cards[x].num - 1] = 1
                if self.cards[x].num == 1:
                    self.suited_array[13] = 1
        return self.check_straight(self.suited_array)

    def check_hand_strength(self):
        """Check for all possible hands and return the current best possible"""
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
            final_hand_cards = self.check_high_card(self.num_of_high_cards)
            final_high_cards = empty
        self.final_cards = self.get_final_cards(final_hand_cards, final_high_cards)
        self.print_final_hand()
        return [current_hand_strength, self.final_cards]  # needs list designation or else becomes tuple

    # Return final 5 cards for the hand.
    # get all cards : investigate why len() is used for the two nested loops
    def get_final_cards(self, hand_cards, high_cards):
        final_cards = []
        if hand_cards[0] == 13:
            hand_cards[0] = 0
        if self.name == 'Quads':
            for x in range(self.num_of_cards):
                if self.cards[x].num - 1 == hand_cards[0]:
                    final_cards.append(self.cards[x])
            for y in range(self.num_of_cards):
                if self.cards[y].num - 1 == high_cards[0]:
                    final_cards.append(self.cards[y])
                    return final_cards

        if self.name == 'Flush' or 'Straight Flush':
            for z in range(0, self.num_of_cards):
                for x in range(0, len(hand_cards)):
                    if hand_cards[x] == 13:
                        hand_cards[x] = 0
                    if self.cards[z].num - 1 == hand_cards[x] and self.cards[z].suit == self.flush_suit:
                        final_cards.append(self.cards[z])
                    if len(final_cards) == 5:
                        return final_cards

        if self.name == 'Straight':
            for x in range(0, len(hand_cards)):
                for y in range(0, self.num_of_cards):
                    if hand_cards[x] == 13:
                        hand_cards[x] = 0
                    if self.cards[y].num - 1 == hand_cards[x]:
                        final_cards.append(self.cards[y])
                        if len(final_cards) == 5:
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
                    return final_cards

            for y in range(0, len(high_cards)):
                if self.num_of_high_cards == 0:
                    break
                # Ace is 1 in self.cards; Ace is 13 in high_cards.
                if high_cards[y] == 13:
                    high_cards[y] = 0
                if self.cards[z].num - 1 == high_cards[y] and high_cards:
                    final_cards.append(self.cards[z])
                if len(final_cards) == 5:
                    return final_cards
        return

    def print_final_hand(self):
        print(self.name + ": " + str(self.final_cards))


class HandCompare:
    """Compare the hands and returns the winner(s) hand(s) and seat(s) and announces the type of winning hand.
       Requires all preflop cards from the players on the table and the community cards"""
    # def __init__(self, hand_details):
    def __init__(self, preflop_cards, community_cards):
        self.preflop_cards = preflop_cards
        self.community_cards = community_cards
        self.hand_details = self.create_hand_types()
        self.hand_strength_list = []
        self.hand_strength = 0
        self.seat_position = []
        self.name = []
        self.best_hand = []
        self.multiple_tied_hands = False
        self.tied_hands = []
        self.tied_hand_seats = []
        self.compare_hand_strength()

    def create_hand_types(self):
        """Loop through the preflop and community cards to prepare them for hand compare"""
        hands = []
        hand_strengths = []
        all_hand_details = []
        for x in range(0, len(self.preflop_cards)):
            hands.append(Hand(self.preflop_cards[x], self.community_cards))
            hand_strengths.append(HandType(hands[x].get_num_array(), hands[x].possible_cards()))
            all_hand_details.append(hand_strengths[x].check_hand_strength())
        return all_hand_details  # all_hand_details = [(current hand strength, final_cards)]

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
        # no tie breaks required
        if hand_occurrences == 1:
            for x in range(0, len(self.hand_details)):
                if self.hand_strength == self.hand_details[x][0]:
                    self.best_hand = self.hand_details[x][1]
                    self.seat_position.append(x+1)
        # tie breaks required
        else:
            break_tied_hands = []
            winning_seats = []
            # create list of tied hands
            for y in range(0, len(self.hand_details)):
                if self.hand_strength == self.hand_details[y][0]:
                    break_tied_hands.append(self.hand_details[y][1])
                    winning_seats.append(y+1)

            # simple case of only 2 tied hands
            if hand_occurrences == 2:
                self.best_hand, self.seat_position = self.find_tie_break(break_tied_hands, winning_seats)
                if self.best_hand is None:
                    self.best_hand = []
                    self.seat_position = []
                    self.best_hand.extend([break_tied_hands[0], break_tied_hands[1]])
                    self.seat_position.extend(winning_seats)

            # hand_occurrences > 2:
            else:
                temp = []
                temp_seat = []
                first_correct_hand, first_correct_seat = self.find_tie_break([break_tied_hands[0], break_tied_hands[1]],
                                                                             winning_seats)
                if first_correct_hand is None:
                    temp.extend([break_tied_hands[0], break_tied_hands[1]])
                    temp_seat.extend([winning_seats[0], winning_seats[1]])
                else:
                    temp.append(first_correct_hand)
                    temp_seat.append(first_correct_seat)
                for y in range(1, len(break_tied_hands)-1):
                    two_hands = []
                    two_seats = []
                    two_hands.extend((temp[-1], break_tied_hands[y+1]))
                    two_seats.extend((temp_seat[-1], winning_seats[y+1]))
                    check_return, check_seat = self.find_tie_break(two_hands, two_seats)
                    if check_return is None:
                        temp.append(break_tied_hands[y+1])
                        temp_seat.append(winning_seats[y+1])
                    else:
                        if temp[-1] != check_return:
                            temp.append(check_return)
                            temp_seat.append(check_seat)
                if len(temp) == 1:
                    self.best_hand = temp
                    self.seat_position = temp_seat
                else:
                    self.best_hand.append(temp[len(temp)-1])
                    self.seat_position.append(temp_seat[len(temp_seat)-1])
                # best hand can be initialized here because its going to be correct
                for z in range(len(temp)-1, 0, -1):
                    two_hands = []
                    two_seats = []
                    two_hands.extend((self.best_hand[-1], temp[z-1]))
                    two_seats.extend((self.seat_position[-1], temp_seat[z-1]))
                    check_return, check_seat = self.find_tie_break(two_hands, two_seats)
                    if check_return is None:
                        self.best_hand.append(temp[z-1])
                        self.seat_position.append(temp_seat[z-1])
                    else:
                        if self.best_hand[-1] != check_return:
                            self.best_hand.append(check_return)
                            self.seat_position.append(check_seat)
                if len(self.best_hand) == 1:
                    self.best_hand = self.best_hand[0]
                    self.seat_position = self.seat_position[0]

    # this function takes in two different hands of equal strength. it will break a tie and return the winning hand.
    # if tie cannot be broken it will return None
    # Need to implement seat_num
    def find_tie_break(self, tied_hand_details, seat_num):
        hand_to_compare0 = Hand.cards_number_array(tied_hand_details[0])
        hand_to_compare1 = Hand.cards_number_array(tied_hand_details[1])

        # cards number array needs to remove high end ace if straight is on the low end
        if self.hand_strength == 4 or self.hand_strength == 8:  # straight or straight flush
            self.fix_straight(hand_to_compare0[0] == 1 and hand_to_compare0[1] == 1, hand_to_compare0)
            self.fix_straight(hand_to_compare1[0] == 1 and hand_to_compare0[1] == 1, hand_to_compare1)

        else:  # cards number array needs to remove low end ace if not low end straight
            hand_to_compare0[0] = 0
            hand_to_compare1[0] = 0

        # break ties using cards_number_array
        if self.hand_strength == 7:  # quads
            quad_card0 = [i for i, x in enumerate(hand_to_compare0) if x == 4]
            quad_card1 = [i for i, x in enumerate(hand_to_compare1) if x == 4]
            if quad_card0 > quad_card1:
                return tied_hand_details[0], seat_num[0]
            if quad_card1 > quad_card0:
                return tied_hand_details[1], seat_num[1]
        elif self.hand_strength == 6:  # full house
            trip_card0 = [i for i, x in enumerate(hand_to_compare0) if x == 3]
            trip_card1 = [i for i, x in enumerate(hand_to_compare1) if x == 3]
            if trip_card0 > trip_card1:
                return tied_hand_details[0], seat_num[0]
            if trip_card1 > trip_card0:
                return tied_hand_details[1], seat_num[1]
            pair_card0 = [i for i, x in enumerate(hand_to_compare0) if x == 2]
            pair_card1 = [i for i, x in enumerate(hand_to_compare1) if x == 2]
            if pair_card0 > pair_card1:
                return tied_hand_details[0], seat_num[0]
            if pair_card1 > pair_card0:
                return tied_hand_details[1], seat_num[1]
        elif self.hand_strength == 3:  # trips
            trip_card0 = [i for i, x in enumerate(hand_to_compare0) if x == 3]
            trip_card1 = [i for i, x in enumerate(hand_to_compare1) if x == 3]
            if trip_card0 > trip_card1:
                return tied_hand_details[0], seat_num[0]
            if trip_card1 > trip_card0:
                return tied_hand_details[1], seat_num[1]
        elif self.hand_strength == 2:  # 2pair
            two_pair_card0 = [i for i, x in enumerate(hand_to_compare0) if x > 1]
            two_pair_card1 = [i for i, x in enumerate(hand_to_compare1) if x > 1]
            for x in range(1, -1, -1):
                if two_pair_card0[x] > two_pair_card1[x]:
                    return tied_hand_details[0], seat_num[0]
                if two_pair_card1[x] > two_pair_card0[x]:
                    return tied_hand_details[1], seat_num[1]
        elif self.hand_strength == 1:  # pair
            pair_card0 = [i for i, x in enumerate(hand_to_compare0) if x == 2]
            pair_card1 = [i for i, x in enumerate(hand_to_compare1) if x == 2]
            if pair_card0 > pair_card1:
                return tied_hand_details[0], seat_num[0]
            if pair_card1 > pair_card0:
                return tied_hand_details[1], seat_num[1]
        else:  # 5 card hand; self.hand_strength == 4, 5 or 8
            pass

        # Compare high cards
        for x in range(13, 0, -1):
            if hand_to_compare0[x] > hand_to_compare1[x]:
                return tied_hand_details[0], seat_num[0]
            elif hand_to_compare1[x] > hand_to_compare0[x]:
                return tied_hand_details[1], seat_num[1]
        # return none if tie is not broken
        return None, None

    @staticmethod
    def fix_straight(ace_low_straight, cards):
        if ace_low_straight:
            cards[13] = 0  # remove high end ace
        else:
            cards[0] = 0  # remove low end ace

    def get_winning_hand(self):
        return self.name

    def get_winning_cards(self):
        best_hand = []
        # creates an error with quads: if len(self.best_hand) == 1:
        # TypeError: object of type 'NoneType' has no len()
        if len(self.best_hand) == 1:
            return self.best_hand
        for x in range(0, len(self.best_hand)):
            if self.best_hand[x] is not None:
                best_hand.append(self.best_hand[x])
        return best_hand  # returns 5 cards

    def get_winning_seat_position(self):
        temp = []
        # Converts seat position list to proper format. Certain tie breaks do not make a list.
        # This is a very difficult bug to find. Consider fixing this work around later.
        try:
            for x in range(0, len(self.seat_position)):
                temp.append(self.seat_position[x])
        except TypeError:
            return [self.seat_position]
        return temp

    def print_winning_hand(self):
        display_final = ['Winning hand seat(s): ' + str(self.get_winning_seat_position()),
                         self.get_winning_hand(), self.get_winning_cards()]
        print(display_final)
        print('community cards', self.community_cards)
        print('\n')
