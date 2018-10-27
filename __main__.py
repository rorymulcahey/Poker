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

# sys.stdout = open('text.txt', 'w')

from Probability.Probabilty import Probability
from CurrentHand import *
import timeit


# test random card configurations
def main():
    number_of_community_cards = 4
    number_of_players = 5
    currenthand = CurrentHand(number_of_players)
    start = timeit.default_timer()
    preflophands = []
    community_cards = []
    for x in range(0, number_of_community_cards):
        community_cards.append(currenthand.get_card())
    for x in range(0, len(currenthand.player_cards)):
        preflophands.append(currenthand.player_cards[x][1])
        print('seat number: ' + str(x + 1) + '  ' + str(preflophands[x]))
    remaining_deck = currenthand.deck.current_cards

    print(community_cards)
    print('\n')
    print(preflophands)
    print('\n')

    # winning_hand = HandCompare(preflophands, community_cards)
    # display_final = ['Winning hand seat(s): ' + str(winning_hand.get_winning_seat_position()),
    #                  winning_hand.get_winning_hand(), winning_hand.get_winning_cards()]
    # print(display_final)
    # print(winning_hand.get_winning_seat_position())
    calculateProbability = Probability(remaining_deck, preflophands, community_cards)
    stop = timeit.default_timer()
    print('Time: ', stop - start, 'seconds')


if __name__ == "__main__":
    main()
    # import sys
    # app = QtGui.QApplication(sys.argv)
    # myapp = MyForm()
    # myapp.show()
    # sys.exit(app.exec_())
