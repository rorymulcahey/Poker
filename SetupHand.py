"""

This file will manage the setup of each hand before players take action.
Including the placement of the dealer button, collection of blinds and
antes. Then dealing cards to each player.

"""
from Table import Table
from PlayGame import PlayGame


class SetupHand:
    def __init__(self, max_num_seats, starting_chip_amount):
        self.first_hand = True
        self.current_table = Table(max_num_seats, starting_chip_amount)
        self.button_seat = self.current_table.button()
        self.setup_next_hand()
        self.current_players = self.current_table.active_players()
        # need to manage side pots
        self.chip_pot_size = 0
        self.ante_size = 0
        self.small_blind_size = 0
        self.big_blind_size = 0

    def setup_next_hand(self):
        game = PlayGame(self.current_players)
        if not self.first_hand:
            self.move_dealer_button()
        self.get_antes(self.ante_size)
        self.place_blinds(self.small_blind_size, self.big_blind_size)
        self.deal_cards()
        self.first_hand = False

    # will produce an infinite loop if current_players = 0
    def move_dealer_button(self):
        while True:
            self.button_seat += 1
            if self.button_seat == len(self.current_players) + 1:
                self.button_seat = 1
            if self.current_players[self.button_seat] is None:
                continue
            else:
                break
        return self.button_seat

    def ante_size(self):
        return self.ante_size

    def small_blind_size(self):
        return self.small_blind_size

    def big_blind_size(self):
        return self.big_blind_size

    def get_antes(self, ante_size):
        for x in range(0, len(self.current_players)):
            self.chip_pot_size += ante_size
            self.current_players[x][0] -= ante_size

    def place_blinds(self, sb, bb):
        # need button seat to circle around at 9 and 10
        self.chip_pot_size += sb
        self.current_players[self.button_seat + 1][0] -= sb
        self.chip_pot_size += bb
        self.current_players[self.button_seat + 2][0] -= bb

    def deal_cards(self):
        self.get_card()
        # loop until each player gets two cards

    def get_card(self):
        pass
