"""

 This  file will contain everything that entails a poker player.
 That will include their current chip count, seat position at
 the table, and their current table number(only 1 for now).


"""


class Player:

    def __init__(self, seat_number, current_chip_amount, table_number):
        self.chip_count = current_chip_amount
        self.seat_num = seat_number
        self.table_number = table_number


class NewPlayer(Player):

    def __init__(self, seat_number, starting_chip_amount, table_number):
        super(Player, self).__init__()
        self.chip_count = starting_chip_amount
        self.seat_num = seat_number
        self.table_number = table_number

    # add a new player to the table after the game starts
    # def new_player(self):
    #    pass
