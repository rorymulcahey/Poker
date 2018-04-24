
'''
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
    Accept two hands as input and then compare the two
        - Need to accept multiple hands and store them.
        - Consider using *args or **kwargs
        - May want to store number of hands in play, use "If hand is None:" to eliminate empty seat positions
        - Use the classes to create arrays
    Build GUI to facilitate hand comparison
    Include chance to win percentages to show hand strength from current community board

Notes:
    Show the 5 best cards with the type of hand** Done
    - Reference the original 7 cards for the final hand by reformatting get_all_cards function
    - Work on straight flush func
    Write "get" functions if check function is true**
    Consolidate cards_array** Done
    Use better return statements (like quads)** Done
    Remove None value from a list without removing the 0 value **Done
    Goal: Try to use any number of cards (preflop, flop, turn, river)** Done
=================================================================================

'''

import pprint


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


# Return final 5 cards for the hand. Be sure to send in lists as arguments
def get_all_cards(all_cards, hand_cards, high_cards):
    final_cards = []
    for z in range(0, len(all_cards)):
        for x in range(0, len(hand_cards)):
            # print(hand_cards)
            # need to include Ace into this function (it cant read 13, needs to read 0)
            if hand_cards[x] == 13:
                hand_cards[x] = 0
                # print(hand_cards)
            if all_cards[z][1] - 1 == hand_cards[x]:
                final_cards.append(all_cards[z])
                # print(len(final_cards))
            if len(final_cards) == 5:
                print(final_cards)
                return final_cards
        for y in range(0, len(high_cards)):
            if high_cards[y] == 13:
                high_cards[y] = 0
            if all_cards[z][1] - 1 == high_cards[y] and high_cards:
                final_cards.append(all_cards[z])
                # print(len(final_cards))
            if len(final_cards) == 5:
                print(final_cards)
                return final_cards
    print("Error with get_all_cards")
    return True


# Remove None values from the cards array
def possible_cards(all_cards):
    index = 0
    array_length = 7
    while index < array_length and all_cards:
        if all_cards[index][1] is None:
            del all_cards[index]
            array_length -= 1
            index -= 1
        index += 1
    print(all_cards)
    return all_cards


# assign values of 1 or more for numerical cards in play and zeros for cards not in play
def cards_number_array(all_cards):
    array = [0] * 14
    for y in range(0, len(all_cards)):
        array[all_cards[y][1] - 1] += 1
        # Increment first and last element of array for aces
        if all_cards[y][1] == 1:
            array[13] += 1
    return array


# consider how we will compare high cards between hands
def check_high_card(array, index):
    i = 1
    high_card = []
    for x in range(13, 0, -1):
        if array[x] == 1:
            # high_card["rank{0}".format(i)] = x
            high_card.append(x)
            i += 1
            if i > index:
                break
    return high_card


def check_pair(array):
    pair = False
    pair_card = []
    for x in range(1, 14):
        if array[x] == 2:
            pair_card.append(x)
            pair = True
            break
    tie_breaker_cards = check_high_card(array, 3)
    if pair:
        pass
        # print(pair_card)
        # print(get_card(pair_card[0]))
        # print(tie_breaker_cards)
    return pair, pair_card, tie_breaker_cards


def check_two_pair(array):
    two_pair = False
    number = 0
    two_pair_cards = []
    for x in range(13, 0, -1):
        if array[x] == 2:
            number += 1
            two_pair_cards.append(x)
        if number == 2:
            two_pair = True
            break
    tie_breaker_cards = check_high_card(array, 1)
    if two_pair:
        # print(tie_breaker_cards)
        pass
    return two_pair, two_pair_cards, tie_breaker_cards


def check_trips(array):
    trips = False
    trips_card = []
    for x in range(1, 14):
        if array[x] == 3:
            trips_card.append(x)
            trips = True
            break
    tie_breaker_cards = check_high_card(array, 2)
    if trips:
        pass
        # print(trips_card)
        # print(tie_breaker_cards)
    return trips, trips_card, tie_breaker_cards


def check_straight(array):
    straight = False
    straight_cards = []
    for x in range(13, 0, -1):
        if array[x] >= 1:
            number = 0
            for y in range(0, 5):
                if x-y < 14 and array[x-y] >= 1:
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


# assign values of 1 or more for suit cards in play and zeros for cards not in play, returns true if suit >= 5:
def check_flush(all_cards):
    array = [0] * 4
    suits = ['c', 'd', 'h', 's']
    for y in range(0, len(all_cards)):
        if all_cards[y][0] == 'c':
            array[0] += 1
        elif all_cards[y][0] == 'd':
            array[1] += 1
        elif all_cards[y][0] == 'h':
            array[2] += 1
        elif all_cards[y][0] == 's':
            array[3] += 1
    for x in range(0, 4):
        if array[x] >= 5:
            current_suit = suits[x]
            return True, current_suit
    return False, None


# returns the cards for the flush:
def get_cards_flush(array, suit, index):
    suited_array = [0] * 14
    for x in range(0, index):
        if array[x][0] == suit:
            suited_array[array[x][1]-1] = 1
            if array[x][1] == 1:
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


def check_full_house(array):
    have_trips = False
    have_pair = False
    trips_card = []
    pair_card = []
    for x in range(13, 0, -1):
        if array[x] == 3:
            trips_card.append(x)
            have_trips = True
            break
    for y in range(13, 0, -1):
        if have_trips and 1 < array[y] < 4 and y != trips_card[0]:
            pair_card.append(y)
            have_pair = True
            break
    return have_pair and have_trips, trips_card, pair_card


# Check hand for four of a kind
def check_quads(array):
    quads = False
    quads_card = []
    for x in range(1, 14):
        if array[x] == 4:
            quads = True
            quads_card.append(x)
            break
    tie_breaker_cards = check_high_card(array, 1)
    return quads, quads_card, tie_breaker_cards


# Check hand for straight flush
def check_straight_flush(array, suit, index):
    suited_array = [0]*14
    for x in range(0, index):
        if array[x][0] == suit:
            suited_array[array[x][1]-1] = 1
            if array[x][1] == 1:
                suited_array[array[x][1] + 12] = 1
    return check_straight(suited_array)


# Check for all possible hands and return the current best possible
def check_hand_strength(number_array, cards_array):
    # 9 possible hands
    possible_hands = ['High Card', 'Pair', 'Two Pair', 'Trips', 'Straight', 'Flush', 'Full House', 'Quads',
                      'Straight Flush']
    check_high_card(number_array, 5)
    current_hand = possible_hands[0]
    empty = []
    # check hand for pair and return 5 cards for final hand
    check_pair_boolean, paired_card, pair_high_cards = check_pair(number_array)
    if check_pair_boolean:
        current_hand = possible_hands[1]
        get_all_cards(cards_array, paired_card, pair_high_cards)

    # check hand for pair and return 5 cards for final hand
    check_two_pair_boolean, two_paired_cards, two_paired_high_cards = check_two_pair(number_array)
    if check_two_pair_boolean:
        current_hand = possible_hands[2]
        get_all_cards(cards_array, two_paired_cards, two_paired_high_cards)

    # check hand for pair and return 5 cards for final hand
    check_trips_boolean, trips_card, trips_high_cards = check_trips(number_array)
    if check_trips_boolean:
        current_hand = possible_hands[3]
        get_all_cards(cards_array, trips_card, trips_high_cards)

    straight_boolean, straight_cards = check_straight(number_array)
    if straight_boolean:
        current_hand = possible_hands[4]
        get_all_cards(cards_array, straight_cards, empty)

    flush_boolean, flush_suit = check_flush(cards_array)
    if check_flush(cards_array)[0]:
        flush_cards = get_cards_flush(cards_array, flush_suit, len(cards_array))
        get_all_cards(cards_array, flush_cards, empty)
        current_hand = possible_hands[5]

    check_full_house_boolean, trips_card, pair_card = check_full_house(number_array)
    if check_full_house_boolean:
        get_all_cards(cards_array, trips_card, pair_card)
        current_hand = possible_hands[6]

    check_quads_boolean, quads_card, high_card = check_quads(number_array)
    if check_quads_boolean:
        get_all_cards(cards_array, quads_card, high_card)
        current_hand = possible_hands[7]

    if straight_boolean and flush_boolean:
        check_straight_flush(cards_array, flush_suit, len(cards_array))
        current_hand = possible_hands[8]

    print(current_hand)
    return current_hand


def compare_hand_strength(*args):
    pass


# remove 'None' hands from array
def all_hands(hands):
    index = 0
    array_length = 11
    while index < array_length and hands:
        if hands[index][0][0] is None or hands[index][1][0] is None:
            del hands[index]
            array_length -= 1
            index -= 1
        index += 1
    return hands, index


# 'pop' the first two cards and create an array ready for check hand strength
# goal: output should be an array that include the community cards with the hand
def create_player_hands(hand_array, community_cards):
    array = []
    for x in range(0, 2):
        # need to store the card value for later
        temp = hand_array[0].pop(0)
        array.append(temp)
        pass
    for y in range(0, 5):
        array.append(community_cards[y])
        pass
    # append flop turn river
    print(array)


def main():
    # Find way to build these with a loop, making an array of (2 (# of cards), 2 (suit, number), 10(seat position))

    # preflop_hands = [[[None for k in range(2)] for j in range(2)] for i in range(10)]
    # pprint.pprint(preflop_hands)

    # Cards in play:
    hand1 = [('c', 8,), ('d', 3)]
    hand2 = [('s', 3), ('h', 7)]
    hand3 = [(None, None), (None, None)]
    hand4 = [(None, None), (None, None)]
    hand5 = [(None, None), (None, None)]
    hand6 = [(None, None), (None, None)]
    hand7 = [(None, None), (None, None)]
    hand8 = [(None, None), (None, None)]
    hand9 = [(None, None), (None, None)]
    hand10 = [(None, None), (None, None)]
    hands = [hand1, hand2, hand3, hand4, hand5, hand6, hand6, hand7, hand8, hand9, hand10]
    all_preflop_hands, number_of_hands = all_hands(hands)

    flop1 = ('s', 2)
    flop2 = ('d', 11)
    flop3 = ('s', 9)
    turn = ('d', 13)
    river = ('d', 8)
    community_cards = [flop1, flop2, flop3, turn, river]

    while all_preflop_hands:
        hand_strength = [0] * number_of_hands
        print(hand_strength)
        create_player_hands(all_preflop_hands, community_cards)
        break

    print(hand1)
    # required because of pop
    hand1 = [('c', 8,), ('d', 3)]
    possible_cards_array = [hand1[0], hand1[1], flop1, flop2, flop3, turn, river]

    # send cards_array into a function, return the array while eliminating None values
    cards_array = possible_cards(possible_cards_array)
    number_array = cards_number_array(cards_array)

    # Functions to check hand combinations:
    check_hand_strength(number_array, cards_array)
    # args =
    compare_hand_strength()


if __name__ == "__main__":
    main()


'''
old code:


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




'''