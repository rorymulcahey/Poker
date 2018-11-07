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


def main():
    start = timeit.default_timer()  # test speed of program

    # initialize the driving variables:
    number_of_community_cards = 3  # can be: 3 (flop), 4 (turn), or 5 (river)
    number_of_players = 5   # can be : 2-10 (players)
    currenthand = CurrentHand(number_of_players)  # currently only uses get_card function

    # Grab random cards from the deck and add them to the list
    # test random card configurations
    preflophands = []
    community_cards = []
    for x in range(0, number_of_community_cards):
        community_cards.append(currenthand.get_card())
    for x in range(0, len(currenthand.player_cards)):
        preflophands.append(currenthand.player_cards[x][1])
        print('seat number: ' + str(x + 1) + '  ' + str(preflophands[x]))
    remaining_deck = currenthand.deck.current_cards
    print("Community cards: " + str(community_cards))
    print('\n')
    print("All preflop hands below")
    print(preflophands)  # this is printed for debugging purposes. copy paste these results if incorrect.
    print('\n')

    # Compare the hands and print the results
    # winning_hand = HandCompare(preflophands, community_cards)
    # winning_hand.print_winning_hand()
    Probability(remaining_deck, preflophands, community_cards)

    stop = timeit.default_timer()  # end of speed test
    print('Time: ', stop - start, 'seconds')


if __name__ == "__main__":
    main()
    # import sys
    # app = QtGui.QApplication(sys.argv)
    # myapp = MyForm()
    # myapp.show()
    # sys.exit(app.exec_())
