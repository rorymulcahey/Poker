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


class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.num = number

    def __repr__(self):
        return self.suit + str(self.num)

    #def __str__(self):
    #    return self.suit + str(self.num)


class Hand:
    def __init__(self, preflop_cards, community_cards):
        self.pre_cards = preflop_cards
        self.comm_cards = community_cards
        #self.index = len(preflop_cards) + len(community_cards)
        self.cards = []

    # Output is an array that include the community cards with the hand
    def create_player_hand(self):
        array = []
        for x in range(0, 2):
            array.append(self.pre_cards[x])
        for y in range(0, 5):
            array.append(self.comm_cards[y])
        return array

    # Remove None values from the card list
    def possible_cards(self):
        index = 0
        array_length = len(self.pre_cards) + len(self.comm_cards)
        # print(array_length)
        self.cards = self.create_player_hand()
        while index < array_length and self.cards:
            #if self.cards[index].suit is None or self.cards[index].num is None:
            if self.cards[index] is None:
                del self.cards[index]
                array_length -= 1
                index -= 1
            index += 1
        # print(self.cards)
        return self.cards

    # assign values of 1 or more for numerical cards in play and zeros for cards not in play
    def cards_number_array(self):
        array = [0] * 14
        self.cards = self.possible_cards()
        for y in range(0, len(self.cards)):
            array[self.cards[y].num - 1] += 1
            # Increment first and last element of array for aces
            if self.cards[y].num == 1:
                array[13] += 1
        return array


class HandType:
    def __init__(self, number_array, cards_array):
        self.num_array = number_array
        self.cards = cards_array
        self.index = len(cards_array)
        self.hc_index = []
        self.straight_array = number_array

    # def __repr__(self):
    #   return self.suit + str(self.num)

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
                break
        tie_breaker_cards = self.check_high_card(3)
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
                break
        tie_breaker_cards = self.check_high_card(1)
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
                break
        tie_breaker_cards = self.check_high_card(2)
        if trips:
            pass
            # print(trips_card)
            # print(tie_breaker_cards)
        return trips, trips_card, tie_breaker_cards

    def check_straight(self):
        straight = False
        straight_cards = []
        for x in range(13, 0, -1):
            if self.straight_array[x] >= 1:
                number = 0
                for y in range(0, 5):
                    if 0 <= x-y < 14 and self.straight_array[x - y] >= 1:
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
        for y in range(0, len(self.cards)):
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
                current_suit = suits[x]
                self.get_cards_flush(current_suit)
                return True, current_suit
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
                break
        tie_breaker_cards = self.check_high_card(1)
        return quads, quads_card, tie_breaker_cards

    def check_straight_flush(self, suit):
        suited_array = [0]*14
        for x in range(0, self.index):
            if self.cards[x].suit == suit:
                suited_array[self.cards[x][1]-1] = 1
                if self.cards[x].num == 1:
                    suited_array[13] = 1
        return self.check_straight(suited_array)

    # Return final 5 cards for the hand. Be sure to send in lists as arguments
    def get_all_cards(self, hand_cards, high_cards):
        final_cards = []
        for z in range(0, self.index):
            for x in range(0, len(hand_cards)):
                print('test')
                if hand_cards[x] == 13:
                    hand_cards[x] = 0
                if self.cards[z].num - 1 == hand_cards[x]:
                    final_cards.append(self.cards[z])
                if len(final_cards) == 5:
                    print(final_cards)
                    return final_cards
            for y in range(0, len(high_cards)):
                print('test2')
                if high_cards[y] == 13:
                    high_cards[y] = 0
                if self.cards[z].num - 1 == high_cards[y] and high_cards:
                    final_cards.append(self.cards[z])
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
        current_hand = possible_hands[0]
        empty = []
        final_hand_cards = []
        final_high_cards = []
        current_hand_strength = 0

        # check hand for pair and return 5 cards for final hand
        check_pair_boolean, paired_card, pair_high_cards = self.check_pair()
        if check_pair_boolean:
            current_hand = possible_hands[1]
            final_hand_cards = paired_card
            final_high_cards = pair_high_cards
            current_hand_strength = 1

        # check hand for pair and return 5 cards for final hand
        check_two_pair_boolean, two_paired_cards, two_paired_high_card = self.check_two_pair()
        if check_two_pair_boolean:
            current_hand = possible_hands[2]
            final_hand_cards = two_paired_cards
            final_high_cards = two_paired_high_card
            current_hand_strength = 2

        # check hand for pair and return 5 cards for final hand
        check_trips_boolean, trips_card, trips_high_cards = self.check_trips()
        if check_trips_boolean:
            current_hand = possible_hands[3]
            final_hand_cards = trips_card
            final_high_cards = trips_high_cards
            current_hand_strength = 3

        straight_boolean, straight_cards = self.check_straight()
        if straight_boolean:
            current_hand = possible_hands[4]
            final_hand_cards = straight_cards
            final_high_cards = empty
            current_hand_strength = 4

        flush_boolean, flush_suit = self.check_flush()
        if self.check_flush()[0]:
            flush_cards = self.get_cards_flush(flush_suit)
            final_hand_cards = flush_cards
            final_high_cards = empty
            current_hand = possible_hands[5]
            current_hand_strength = 5

        check_full_house_boolean, trips_card, pair_card = self.check_full_house()
        if check_full_house_boolean:
            final_hand_cards = trips_card
            final_high_cards = pair_card
            current_hand = possible_hands[6]
            current_hand_strength = 6

        check_quads_boolean, quads_card, high_card = self.check_quads()
        if check_quads_boolean:
            final_hand_cards = quads_card
            final_high_cards = high_card
            current_hand = possible_hands[7]
            current_hand_strength = 7

        if straight_boolean and flush_boolean:
            straight_flush_boolean, straight_flush_cards = self.check_straight_flush(flush_suit)
            if straight_flush_boolean:
                current_hand = possible_hands[8]
                final_hand_cards = straight_flush_cards
                final_high_cards = empty
                current_hand_strength = 8

        if current_hand == possible_hands[0]:
            final_hand_cards = self.check_high_card(5)
            final_high_cards = empty

        final_cards = self.get_all_cards(final_hand_cards, final_high_cards)
        print(current_hand)
        return current_hand_strength, final_cards

# get all cards not functioning as intended
card1 = Card('c', 4)
card2 = Card('d', 4)
preflop1 = [card1, card2]
flop1 = Card('s', 13)
flop2 = Card('d', 13)
flop3 = Card('c', 13)
turn = Card('h', 13)
# river = Card('d', 8)
river = None
community = [flop1, flop2, flop3, turn, river]
hand1 = Hand(preflop1, community)
hand_strength1 = HandType(hand1.cards_number_array(), hand1.possible_cards())
print(hand_strength1.check_hand_strength())
# print(hand1.possible_cards())
# print(hand1.create_player_hand())

'''
class HandCompare:
    def __init__(self, suit, num):
        self.card = suit, num

    # remove 'None' hands from pre flop cards array
    def all_hands(self, hands):
        hand_position = [0] * 10
        for x in range(0, 10):
            if hands[x][0][0] is not None or hands[x][1][0] is not None:
                hand_position[x] = 1
        index = 0
        # check array_length for debugs
        array_length = 11
        while index < array_length and hands:
            if hands[index][0][0] is None or hands[index][1][0] is None:
                del hands[index]
                array_length -= 1
                index -= 1
            index += 1
        return hands, index, hand_position

    def compare_hand_strength(self, all_hand_details, hand_strength):
        hand_type = max(hand_strength)
        hand_occurrences = hand_strength.count(hand_type)
        best_hand = []
        if hand_occurrences == 1:
            for x in range(0, len(hand_strength)):
                if hand_type == all_hand_details[x][0]:
                    best_hand = all_hand_details[x]
        elif hand_occurrences == 2:
            tied_hands = [hand_type]
            for y in range(0, len(hand_strength)):
                if hand_type == all_hand_details[y][0]:
                    tied_hands.append(all_hand_details[y][1])
            best_hand = find_tie_break(tied_hands)
        elif hand_occurrences > 2:
            pass
            # this statement is used to break more than 1 tie
        print(best_hand)
        return best_hand

    def find_tie_break(self, tied_hands):
        winning_hand = [tied_hands[0]]
        # need to determine how to announce more than one tie breaking winner
        # print(len(best_hand)) **this can be used to determine if we need to denote more than 1 winning hand
        if tied_hands[0] != 1 and tied_hands[0] != 2 and tied_hands[0] != 3 and tied_hands[0] != 7:
            print('tied breaker engaged')
            hand1 = cards_number_array(tied_hands[1])
            hand2 = cards_number_array(tied_hands[2])
            for x in range(13, 0, -1):
                if hand1[x] > hand2[x]:
                    winning_hand.append(tied_hands[1])
                    return winning_hand
                if hand2[x] > hand1[x]:
                    winning_hand.append(tied_hands[2])
                    return winning_hand
        # return both hands if tie is not broken
        # could also consider using tie_broken_boolean
        winning_hand.append(tied_hands[1])
        winning_hand.append(tied_hands[2])
        return winning_hand


def main():
    # Cards in play:
    hand1 = [('s', 9,), ('s', 3)]
    hand2 = [('s', 2), ('h', 7)]
    hand3 = [('s', 1), ('s', 12)]
    hand4 = [(None, None), (None, None)]
    hand5 = [(None, None), (None, None)]
    hand6 = [(None, None), (None, None)]
    hand7 = [(None, None), (None, None)]
    hand8 = [(None, None), (None, None)]
    hand9 = [(None, None), (None, None)]
    hand10 = [(None, None), (None, None)]
    hands = [hand1, hand2, hand3, hand4, hand5, hand6, hand6, hand7, hand8, hand9, hand10]
    flop1 = ('s', 8)
    flop2 = ('s', 11)
    flop3 = ('d', 10)
    turn = ('s', 13)
    river = ('d', 8)
    # river = (None, None)
    community_cards = [flop1, flop2, flop3, turn, river]

    all_preflop_hands, number_of_hands, hand_positions = all_hands(hands)
    # may not need hand positions #
    # hands are numerically ordered in accordance with their seat position #
    # this can be used to match winner with seat position #
    player_hands = create_player_hand(all_preflop_hands, community_cards, number_of_hands)
    all_hand_details = []
    only_strengths = []
    for x in range(0, number_of_hands):
        all_hand_details.append([])
        cards_array = possible_cards(player_hands[x])
        number_array = cards_number_array(cards_array)

        # hand strength is located with print(all_hand_details[x][0])
        # hand cards are located with print(all_hand_details[x][1])
        hand_details = check_hand_strength(number_array, cards_array)
        only_strengths.append(hand_details[0])
        all_hand_details[x].append(hand_details[0])
        all_hand_details[x].append(hand_details[1])

    # Functions to check hand combinations:
    compare_hand_strength(all_hand_details, only_strengths)


if __name__ == "__main__":
    main()

'''
'''
old code:


class community_card:
    def __init__(self, suit, num):
        self.suit = suit
        self.num = num
        # num = str(num)
        self.card = suit, num


class preflop:
    def __init__(self, suit, num):
        self.suit = ""
        self.num = 0
        self.card = suit, num
        
    

def get_card(card_number):
    if card_number == 0 or card_number == 13:
        return "Ace"
    elif card_number == 1:
        return "Two"
    elif card_number == 2:
        return "Three"
    elif card_number == 3:
        return "Four"
    elif card_number == 4:
        return "Five"
    elif card_number == 5:
        return "Six"
    elif card_number == 6:
        return "Seven"
    elif card_number == 7:
        return "Eight"
    elif card_number == 8:
        return "Nine"
    elif card_number == 9:
        return "Ten"
    elif card_number == 10:
        return "Jack"
    elif card_number == 11:
        return "Queen"
    elif card_number == 12:
        return "King"


# test functions
def preflop_hand(suit1, num1, suit2, num2):
    if suit1 == suit2:
        print("You are suited!")
    if num1 == num2:
        print("You are paired!")
    if num1 == num2 + 1 or num1 == num2 - 1:
        print("You are connected!")
preflop_hand(preflop1.card[0], preflop1.card[1], preflop2.card[0], preflop2.card[1])
        
        
# function to find flush
def check_flush(array):
    for x in range(0, 7):
        number = 1
        flush = False
        for y in range(0, 7):
            if array[x][0] == array[y][0] and x != y:
                number += 1
            if number == 5:
                print("You have a flush!")
                flush = True
                break
        if flush:
            return True, array[x][0]
    return False, None
    
# function call
    flush_boolean, flush_suit = check_flush(cards_array)

def check_flush(array):
    flush_boolean, flush_suit = cards_suit_array(cards_array)
    if flush_boolean:
        suited_array = [0] * 14
    # needs to cycle through all 7 cards, check suit, if correct suit, write number to suited array (for card number)
        for x in range(0, 7):
            if array[x][0] == flush_suit:
                suited_array[x] = array[x][1]
                print(suited_array[x])
        i = 1
        high_card = {}
        for y in range(13, 0, -1):
            if suited_array[y] == 1:
                high_card["rank{0}".format(i)] = y
                i += 1
                if i > 5:
                    break
        print(high_card)
    return flush_boolean, flush_suit


def cards_suit_array(all_cards):
    array = [0] * 4
    suits = ['c', 'd', 'h', 's']
    for x in range(0, 7):
        if all_cards[x][0] == 'c':
            array[0] += 1
        elif all_cards[x][0] == 'd':
            array[1] += 1
        elif all_cards[x][0] == 'h':
            array[2] += 1
        elif all_cards[x][0] == 's':
            array[3] += 1
    for y in range(0, 4):
        if array[y] >= 5:
            current_suit = suits[y]
            i = 1
            high_card_suited = {}
            for z in range(6, 0, -1):
                if all_cards[z][0] == current_suit:
                    high_card_suited["suited_rank{0}".format(i)] = all_cards[z][1]
                    i += 1
                    print("check")
                    if i > 5:
                        break
    print(high_card_suited)
    print(array)
    return array
'''

'''
Useful programs:

# A Python program to to return multiple
# values from a method using tuple

# This function returns a tuple
def fun():
    str = "geeksforgeeks"
    x = 20
    return str, x;  # Return tuple, we could also
    # write (str, x)


# Driver code to test above method
str, x = fun()  # Assign returned tuple
print(str)
print(x)


preflop_hands = [[[None for k in range(2)] for j in range(2)] for i in range(10)]
pprint.pprint(preflop_hands)


def compare_hand_strength(all_hand_details, hand_strength):
for x in range(1, len(all_hand_details)):
    tied_hands = []
    if all_hand_details[x][0] == best_hand[0]:
        tied_hands.append(best_hand[0])
        tied_hands.append(best_hand[1])
        tied_hands.append(all_hand_details[x][1])
        best_hand = find_tie_break(tied_hands)
        # include more than 2 tie breaker hands
        # tied_break_hands = find_tie_break(tied_hands)
        # best_hand = tie_break_hands
    if all_hand_details[x][0] > best_hand[0]:
        best_hand = all_hand_details[x]
'''