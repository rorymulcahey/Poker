# "#!/usr/bin/env python
#
# import os
# import sys
#
# # Resolve path configuration
# root = os.path.join(os.path.dirname(__file__), "..")
# src = os.path.join(root, "Poker")
# sys.path.append(root)
# sys.path.append(src)

from Probability.Probabilty import Probability
from SolvePokerHands import *
from CurrentHand import *


def main():

    # test random card configurations
    currenthand = CurrentHand(10, 2000)
    preflophands = []
    remaining_deck = []
    community_cards = []
    for x in range(0, 5):
        community_cards.append(currenthand.get_card())
    for x in range(0, len(currenthand.player_cards)):
        preflophands.append(currenthand.player_cards[x][1])
        print('seat number: ' + str(x + 1) + '  ' + str(preflophands[x]))
    for x in range(0, len(currenthand.deck.current_cards)):
        remaining_deck.append(currenthand.get_card())
    calculateProbability = Probability(remaining_deck, preflophands, community_cards)

    print(community_cards)
    print('\n')
    print(preflophands)
    print('\n')
    # end of random test

    # test hand bug (Seat position is incorrect)
    # preflophands = [[Card('h', 3), Card('c', 13)], [Card('s', 12), Card('s', 9)], [Card('d', 6), Card('d', 5)],
    #                 [Card('d', 13), Card('c', 2)], [Card('h', 4), Card('h', 9)], [Card('s', 1), Card('s', 6)],
    #                 [Card('c', 7), Card('s', 8)], [Card('h', 13), Card('d', 2)], [Card('d', 3), Card('c', 3)],
    #                 [Card('c', 8), Card('h', 7)]]
    # community_cards = [Card('c', 5), Card('d', 10), Card('c', 10), Card('c', 9), Card('h', 10)]
    # end of test

    # Keep this bug. Very good for testing. Good way to test seat position
    # **FIXED** test hand bug (Removes winning straight during tie break) **FIXED**
    # This bug occurs because the num array always increments the highest value when an Ace is present, therefore
    # an ace with on the low end because the 6 to 2 straight because it compares with the high end ace.
    # preflophands = [[Card('h', 4), Card('s', 12)], [Card('h', 7), Card('d', 8)], [Card('c', 1), Card('s', 3)],
    #                 [Card('s', 5), Card('s', 8)], [Card('h', 2), Card('d', 12)], [Card('s', 10), Card('d', 1)],
    #                 [Card('h', 6), Card('d', 10)], [Card('s', 1), Card('s', 6)], [Card('h', 9), Card('c', 8)],
    #                 [Card('h', 1), Card('s', 7)]]
    # community_cards = [Card('c', 3), Card('h', 5), Card('c', 4), Card('h', 3), Card('c', 2)]
    # end of test

    # Test quads (Works)
    # preflophands = [[Card('h', 1), Card('c', 1)], [Card('d', 6), Card('c', 9)], [Card('c', 7), Card('s', 7)],
    #                 [Card('h', 11), Card('h', 8)], [Card('s', 3), Card('h', 4)], [Card('d', 12), Card('h', 10)],
    #                 [Card('c', 11), Card('h', 6)], [Card('d', 13), Card('c', 13)], [Card('s', 5), Card('h', 5)],
    #                 [Card('h', 12), Card('s', 10)]]
    # community_cards = [Card('d', 1), Card('d', 5), Card('s', 1), Card('d', 3), Card('c', 5)]
    # end of test

    # Test two pair (Needs to show which seats have the announced winning hand)
    # preflophands = [[Card('s', 7), Card('h', 1)], [Card('s', 8), Card('d', 1)], [Card('d', 2), Card('h', 9)],
    #                [Card('h', 10), Card('d', 7)], [Card('c', 2), Card('c', 13)], [Card('c', 6), Card('s', 5)],
    #                [Card('s', 2), Card('d', 10)], [Card('s', 6), Card('d', 11)], [Card('h', 3), Card('s', 4)],
    #                [Card('h', 13), Card('h', 7)]]
    # community_cards = [Card('d', 12), Card('s', 10), Card('d', 5), Card('c', 7), Card('c', 12)]
    # end of test

    hands = []
    hand_strengths = []
    all_hand_details = []
    for x in range(0, len(preflophands)):
        hands.append(Hand(preflophands[x], community_cards))
        hand_strengths.append(HandType(hands[x].get_num_array(), hands[x].possible_cards()))
        all_hand_details.append(hand_strengths[x].check_hand_strength())
    # Ideal scenario would be: winning_hand = HandCompare(preflophands, community_cards)
    winning_hand = HandCompare(all_hand_details)
    # print("Winning hand is:", winning_hand.compare_hand_strength())
    display_final = ['tied hand(s): ' + str(winning_hand.seat_position), winning_hand.get_winning_hand(),
                     winning_hand.get_winning_cards()]
    # print(all_hand_details)
    print(display_final)
    # self.lcdTotaltime.display(display_final)


if __name__ == "__main__":
    main()
    '''
    # import sys
    # app = QtGui.QApplication(sys.argv)
    # myapp = MyForm()
    # myapp.show()
    # sys.exit(app.exec_())
    '''

    '''
    Old code:
    # Cards in play:
    hand1 = [Card('s', 4), Card('s', 3)]
    hand2 = [Card('s', 1), Card('h', 7)]
    hand3 = None
    hand4 = None
    hand5 = [Card('h', 13), Card('c', 13)]
    hand6 = None
    hand7 = None
    hand8 = None
    hand9 = None
    hand10 = None
    preflophands = [hand1, hand2, hand3, hand4, hand5,
                    hand6, hand7, hand8, hand9, hand10]
    hand_position = [0] * 10

    # remove 'None' hands from preflop cards list
    # consider using this with create_player_hand to remove empty preflop hands and store position
    # all_preflop_hands, number_of_hands, hand_positions = all_hands(hands)
    # hands are numerically ordered in accordance with their seat position #

    for x in range(0, 10):
        if preflophands[x] is not None:
            hand_position[x] = 1
    # print(hand_position)
    index = 0
    number_of_hands = 10
    while index < number_of_hands and preflophands:
        if preflophands[index] is None:
            del preflophands[index]
            number_of_hands -= 1
            index -= 1
        index += 1
    flop1 = Card('d', 13)
    flop2 = Card('s', 11)
    flop3 = Card('s', 10)
    turn = Card('s', 12)
    river = Card('s', 13)
    community_cards = [flop1, flop2, flop3, turn, river]
    print(community_cards)
    print(preflophands)
    '''