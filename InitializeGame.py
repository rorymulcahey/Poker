"""
 
 This  file will contain the needed code to setup and maintain a poker table.
 Stored here is the information about each players chip count, the location
 of the button and big blind. Using that information, the program will begin
 to assign chip counts and cards to each seat of the table. Then it will 
 collect antes and blinds from the players, preparing the entire game to 
 be played. 
 

"""


class InitializeGame:
    # takes in as parameters the total number of seats on the table and starting chip ammounts
    def __init__(self, max_num_seats, starting_chip_amount):
        # self.seats = total_players
        self.st_chips = starting_chip_amount
        self.ch_counts = []
        self.seat_occupied = [1] * max_num_seats
        # self.seats = self.occupied_seats(self.players)
        self.initialize()

    # needs dynamic blind level allocation
    def initialize(self):
        # give out chips
        for x in range(0, self.index):
            if self.seat_occupied[x]:
                self.ch_counts[x].append(self.st_chips)
                # give out cards
                self.create_hand(x)

        # place button

    """
    def occupied_seats(self):
        array = [0] * self.index
        for y in range(0, self.index):

        return array[]
    """

    def setup_next_hand():
     chipVal = ch_counts[seat_num]
     create_hand(seat_num)
     move_button_and_blinds()
     get_antes()
     place_blinds()
     
    
    def create_hand(self, seat):
     
    def setup_next_hand(self):
     
    def move_button_and_blinds(self):
     
    def get_antes(self):
     
    def place_blinds(self):
     # return BB seat
     
    def play_game(self):
     # First action = BBseat


