"""

 This  file will contain the needed code to play a poker game. This class
 will handle the needed code to execute normal game functionality. It will
 include the ability to find the players turn, give action to the player on
 their turn, calculate bet sizes, verify if bet size is valid, etc.
 Stored here is the information about each players chip count, how many
 players are in the hand, the size of the pot, all side pots, etc.


"""
from SetupHand import SetupHand


class PlayGame:
    def __init__(self, current_players):
        self.current_players = current_players
        # bets in front of the player, not yet into the pot
        self.current_bet_counts = []
        self.current_chip_counts = self.chip_counts()
        self.main_pot = 0

    def chip_counts(self):
        chip_counts = []
        for x in range(0, len(self.current_players)):
            chip_counts.append(self.current_players[x][0])
        return chip_counts

    def main_pot(self):
        return self.main_pot

    def player_raise(self):
        pass

    def player_fold(self):
        pass

    def player_check(self):
        pass

    def deal_card(self):
        pass






