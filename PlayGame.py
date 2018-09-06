"""

 This  file will contain the needed code to play a poker game. This class
 will handle the needed code to execute normal game functionality. It will
 include the ability to find the players turn, give action to the player on
 their turn, calculate bet sizes, verify if bet size is valid, etc.
 Stored here is the information about each players chip count, how many
 players are in the hand, the size of the pot, all side pots, etc.


"""
import SetupGame


class PlayGame:
    # takes in as parameters the total number of seats on the table and starting chip amounts
    def __init__(self, chip_counts):
        self.current_chip_counts = chip_counts


