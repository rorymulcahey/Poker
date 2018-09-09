"""
 
 This  file will contain the needed code to setup a poker table.
 Stored here is the information about each players chip count, the location
 of the button and big blind. Using that information, the program will begin
 to assign chip counts and cards to each seat of the table. Then it will 
 collect antes and blinds from the players, preparing the entire game to 
 be played. 
 

"""
import random
import Player


class Table:
    # takes in as parameters the total number of seats on the table and starting chip amounts
    def __init__(self, max_num_seats, starting_chip_amount):
        # self.seats = total_players
        self.starting_chip_count = starting_chip_amount
        self.active_players = []
        # need a better way to organize seat layout
        self.seats_occupied = [1] * max_num_seats
        # self.seats = self.occupied_seats(self.players)
        self.button = None
        self.table_number = 1

    # needs dynamic blind level allocation
    def create_new_table(self):
        # give out chips
        for x in range(0, self.seats_occupied):
            if self.seats_occupied[x]:
                self.active_players.append(Player.NewPlayer(self.starting_chip_count, x, self.table_number))
            # currently will not enter this block. need to add empty seat capability
            else:
                self.active_players[x] = None
        self.place_button()

    def place_button(self):
        self.button = random.randint(1, 10)

    def button(self):
        return self.button

    def active_players(self):
        return self.active_players

    def set_blind_levels(self):
        pass
