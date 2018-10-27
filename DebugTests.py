#__main__.py
# start of specified tests

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

# Test two pair (Should return none because hands are the same but does not do so. Needs to show which seats have
# the announced winning hand)
# preflophands = [[Card('s', 7), Card('h', 1)], [Card('s', 8), Card('d', 1)], [Card('d', 2), Card('h', 9)],
#                [Card('h', 10), Card('d', 7)], [Card('c', 2), Card('c', 13)], [Card('c', 6), Card('s', 5)],
#                [Card('s', 2), Card('d', 10)], [Card('s', 6), Card('d', 11)], [Card('h', 3), Card('s', 4)],
#                [Card('h', 13), Card('h', 7)]]
# community_cards = [Card('d', 12), Card('s', 10), Card('d', 5), Card('c', 7), Card('c', 12)]
# end of test

# Test pair (Prefers kings over aces)
# **FIXED** the error was adding a nested list
# preflophands = [[Card('h', 5), Card('s', 11)], [Card('c', 12), Card('s', 8)], [Card('s', 5), Card('h', 8)],
# [Card('h', 13), Card('s', 3)], [Card('s', 1), Card('h', 9)], [Card('h', 1), Card('s', 4)],
# [Card('h', 10), Card('d', 11)], [Card('c', 4), Card('h', 12)], [Card('d', 6), Card('h', 2)],
# [Card('d', 2), Card('h', 4)]]
# community_cards = [Card('d', 5), Card('s', 13), Card('c', 7), Card('c', 2), Card('c', 1)]
# end of test

# Test multiple winner (not returning both seat positions)
# **FIXED**
# preflophands = [[Card('h', 9), Card('d', 3)], [Card('d', 5), Card('c', 3)], [Card('s', 5), Card('d', 9)],
# [Card('d', 6), Card('h', 2)], [Card('s', 6), Card('d', 7)], [Card('h', 6), Card('c', 5)],
# [Card('c', 4), Card('h', 8)], [Card('h', 7), Card('c', 8)], [Card('d', 4), Card('d', 1)],
# [Card('s', 1), Card('s', 4)]]
# community_cards = [Card('h', 1), Card('d', 10), Card('s', 7), Card('s', 13), Card('c', 9)]
# end of specified tests


# Probability.py
# start = timeit.default_timer()
# ch = CurrentHand(3)
# pre = []
# dck = []
# community_cards = []
# for g in range(0, 5):
#     community_cards.append(ch.get_card())
# for g in range(0, len(ch.player_cards)):
#     pre.append(ch.player_cards[g][1])
# for x in range(0, len(ch.deck.current_cards)):
#     dck.append(ch.get_card())
# calculateProbability = Probability(ch.deck.current_cards, pre, community_cards)
# calculateProbability.number_of_cards_remaining()
# stop = timeit.default_timer()
# print('Time: ', stop - start)
# calculateProbability.one_card_remaining()


