"""
 
 This  file will contain the needed code to setup a poker table.
 Stored here is the information about each players chip count, the location
 of the button and big blind. Using that information, the program will begin
 to assign chip counts and cards to each seat of the table. Then it will 
 collect antes and blinds from the players, preparing the entire game to 
 be played. 
 

"""


class SetupGame:
    # takes in as parameters the total number of seats on the table and starting chip amounts
    def __init__(self, max_num_seats, starting_chip_amount):
        # self.seats = total_players
        self.starting_chip_count = starting_chip_amount
        self.chip_counts = []
        # need a better way to organize seat layout
        self.seats_occupied = [1] * max_num_seats
        # self.seats = self.occupied_seats(self.players)
        self.button = 1
        self.setup_game()

    # needs dynamic blind level allocation
    def setup_game(self):
        # give out chips
        for x in range(0, self.seats_occupied):
            if self.seats_occupied[x]:
                self.chip_counts[x].append(self.starting_chip_count)
                # give out cards
                self.create_hand(x)
        self.place_blinds()



        # place button

    """
    def occupied_seats(self):
        array = [0] * self.index
        for y in range(0, self.index):

        return array[]
    """

    def setup_next_hand(self):
     chipVal = ch_counts[seat_num]
     self.create_hand(seat_num)
     self.move_button_and_blinds()
     self.get_antes()
     self.place_blinds()

    def create_hand(self, seat):
        pass

    def move_button_and_blinds(self):
        pass

    def get_antes(self):
        pass

    def place_blinds(self):
        # subtract from the current chip counts the amount required for the blind

    # return dealer seat position
    # will produce an infinite loop if all seats_occupied = 0
    def dealer_button(self):
        while True:
            self.button += 1
            if self.button == len(self.seats_occupied)+1:
                self.button = 1
            if self.seats_occupied[self.button] == 0:
                continue
            else:
                break
        return self.button

    def play_game(self):
        pass
    # First action = BBseat


