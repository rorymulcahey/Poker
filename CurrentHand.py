"""

This file will manage the setup of each hand before players take action.
Including the placement of the dealer button, collection of blinds and
antes. Then dealing cards to each player. Seat number is key identifier
for current cards and active player info at index 0. Seat number is
one indexed, vs the array being 0 indexed.

"""
from Table import *
import random


# move variables out of setup hand, like current_player_info, and manage them in table.py. Play game will use them
class CurrentHand:
    def __init__(self, max_num_seats, num_community_cards):
        self.first_hand = True
        self.current_table = Table(max_num_seats)
        self.button_seat = self.current_table.button
        # need to manage side pots
        self.main_pot = 0
        self.side_pots = []
        self.ante_size = 1
        self.small_blind_size = 25
        self.big_blind_size = 50
        self.player_cards = []  # [seat number, [Card 1, Card2]]
        self.deck = Deck()
        self.setup_next_hand()
        self.preflophands = []
        self.num_community_cards = num_community_cards
        self.community_cards = []

    def __eq__(self, other):
        if not isinstance(other, CurrentHand):
            # Delegate comparison to the other instance's __eq__.
            return NotImplemented

    def __ne__(self, other):
        # By using the == operator, the returned NotImplemented is handled correctly.
        return not self == other
        # sum(1 for _ in filter(None.__ne__, lst))

    def setup_next_hand(self):
        if not self.first_hand:
            self.move_dealer_button()
        self.get_antes(self.ante_size)
        self.place_blinds(self.small_blind_size, self.big_blind_size)
        self.deal_cards()
        self.first_hand = False

    def move_dealer_button(self):
        self.button_seat = self.next_seat(self.button_seat, 1)

    def ante_size(self):
        return self.ante_size

    def small_blind_size(self):
        return self.small_blind_size

    def big_blind_size(self):
        return self.big_blind_size

    def get_antes(self, ante_size):
        for x in range(0, len(self.current_table.active_player_info)):
            self.main_pot += ante_size
            self.current_table.active_player_info[x].chip_count -= ante_size

    # need to add side pots
    # need to take smaller amount of chips if person has less than blind
    def place_blinds(self, sb, bb):
        # modified for heads up poker
        if self.current_table.active_num_players == 2:
            self.main_pot += bb
            self.current_table.active_player_info[self.next_seat(self.button_seat, 1)-1].chip_count -= bb
            self.main_pot += sb
            self.current_table.active_player_info[self.next_seat(self.button_seat, 2)-1].chip_count -= sb
        # all other number of player setups
        else:
            self.main_pot += sb
            self.current_table.active_player_info[self.next_seat(self.button_seat, 1)-1].chip_count -= sb
            self.main_pot += bb
            self.current_table.active_player_info[self.next_seat(self.button_seat, 2)-1].chip_count -= bb

    # loop until each player gets two cards
    # has texas hold'em format, dealing two cards to each player
    def deal_cards(self):
        for x in range(0, len(self.current_table.active_player_info)):
            self.player_cards.append([x + 1])  # seat number
            self.player_cards[x].append([self.get_card(), self.get_card()])  # cards

    # used to deal cards, and community cards.
    def get_card(self):
        return self.deck.current_cards.pop(random.randint(0, len(self.deck.current_cards) - 1))

    # will produce an infinite loop if no players = 0
    # need button seat to circle around at 9 and 10, i think it does
    def next_seat(self, current_seat, number_of_times):
        if all(v is None for v in self.current_table.active_player_info):
            return None
        while True:
            current_seat = current_seat % self.current_table.possible_seats + 1
            if self.current_table.active_player_info[current_seat-1] is None:
                continue
            elif number_of_times > 1:
                number_of_times -= number_of_times
            else:
                return current_seat

    def current_player_count(self):
        counter = 0
        print(len(self.current_table.active_player_info))
        for x in range(0, len(self.current_table.active_player_info)):
            if all(v is None for v in self.current_table.active_player_info):
                pass
            else:
                counter += 1
            return counter

    def create_hands(self):
        # Grab random cards from the deck and add them to the list
        # test random card configurations
        for x in range(0, self.num_community_cards):
            self.community_cards.append(self.get_card())
        for x in range(0, len(self.player_cards)):
            self.preflophands.append(self.player_cards[x][1])
            print('seat number: ' + str(x + 1) + '  ' + str(self.preflophands[x]))
        remaining_deck = self.deck.current_cards
        print("Community cards: " + str(self.community_cards))
        print('\n')
        print("All preflop hands below")
        print(self.preflophands)  # this is printed for debugging purposes. copy paste these results if incorrect.
        print('\n')

# Test CurrentHand.py
# a = CurrentHand(10)
# result = []
# for y in range(0, len(a.current_table.active_player_info)):
#     result.append(a.current_table.active_player_info[y].chip_count)
# print(result)
# print(a.button_seat)
# print(a.player_cards)
# print(a.deck.current_cards)
