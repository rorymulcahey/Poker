"""
 
 This  file will contain the needed code to setup and maintain a poker table.
 Stored here is the information about each players chip count, the location
 of the button and big blind. Using that information, the program will begin
 to assign chip counts and cards to each seat of the table. Then it will 
 collect antes and blinds from the players, preparing the entire game to 
 be played. 
 

"""


class InitializeGame:
    def __init__(self, total_players, starting_chip_amount):
        self.index = len(total_players)
        # self.seats = total_players
        self.st_chips = starting_chip_amount
        self.ch_counts = []
        self.seat_occupied = [1] * 10
        # self.seats = self.occupied_seats(self.players)
        self.initialize()

    def initialize(self):
        # give out chips
        for y in range(0, self.index):
            if self.seat_occupied[y]:
                self.ch_counts[y].append(self.st_chips)
                # give out cards
                self.create_hand(y)

        # place button

    """
    def occupied_seats(self):
        array = [0] * self.index
        for y in range(0, self.index):

        return array[]
    """

    def create_hand(self, seat):


    def setup_next_hand(self):


