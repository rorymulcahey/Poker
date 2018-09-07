"""

This file will manage the setup of each hand before players take action.

"""

class SetupHand:
    def __init__(self, max_num_seats, starting_chip_amount):
        self.place_blinds()
        self.create_hand()

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
            if self.button == len(self.seats_occupied ) +1:
                self.button = 1
            if self.seats_occupied[self.button] == 0:
                continue
            else:
                break
        return self.button
