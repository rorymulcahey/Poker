"""

 This  file will contain the needed code to play a poker game. This class
 will handle the needed code to execute normal game functionality. It will
 include the ability to find the players turn, give action to the player on
 their turn, calculate bet sizes, verify if bet size is valid, etc.
 Stored here is the information about each players chip count, how many
 players are in the hand, the size of the pot, all side pots, etc.


"""
from CurrentHand import CurrentHand


class PlayGame:
    def __init__(self, max_num_seats, starting_chip_amount):
        self.hand = CurrentHand(max_num_seats, starting_chip_amount)
        # bets in front of the player, not yet into the pot
        self.current_bet_counts = []
        self.current_chip_counts = self.chip_counts()
        self.current_seat_turn = self.hand.next_seat(self.hand.button_seat)

    def chip_counts(self):
        chip_counts = []
        for x in range(0, len(self.hand.current_table.active_player_info)):
            chip_counts.append(self.hand.current_table.active_player_info[x].chip_count)
        return chip_counts

    def main_pot(self):
        return self.main_pot

    def player_raise(self):
        pass

    def player_fold(self):
        self.hand.current_table.active_player_info[self.current_seat_turn] = None

    def player_check(self):
        pass

    def deal_card(self):
        pass






