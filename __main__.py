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
# from SolvePokerHands import *
import timeit


def main():
    start = timeit.default_timer()  # test speed of program

    # initialize the driving variables:
    number_of_community_cards = 3  # can be: 3 (flop), 4 (turn), or 5 (river)
    number_of_players = 5  # can be : 2-10 (players)

    current_hand = CurrentHand(number_of_players, number_of_community_cards)
    current_hand.print_preflop_cards()
    current_hand.print_community_cards()
    current_hand.print_debug_cards()

    # Compare the hands and print the results
    # winning_hand = HandCompare(current_hand.preflop_cards, current_hand.community_cards)
    # winning_hand.print_winning_hand()
    Probability(current_hand.deck.current_cards, current_hand.preflop_cards, current_hand.community_cards)
    # Note: winning_hand.print_winning_hand() is built into the Probability class so every result is visible.

    stop = timeit.default_timer()  # end of speed test
    print('Time: ', stop - start, 'seconds')


if __name__ == "__main__":
    main()
    # import sys
    # app = QtGui.QApplication(sys.argv)
    # myapp = MyForm()
    # myapp.show()
    # sys.exit(app.exec_())
