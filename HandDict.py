'''
# this is old code that was used to find the winning hand. The method involved a dictionary
# lookup.
# problems arise with the list nesting. sometimes it needs to be flattened other it does not
def get_winning_seat_position(self):
    best_hand = self.get_winning_cards()
    try:
        if len(best_hand[0]) > 1:
            self.seat_position = []
            for x in range(len(best_hand)):  # needs to be nested inside of a list for iteration
                self.seat_position.append(self.hand_and_seat.get(str([best_hand[x]])))
            print(self.hand_and_seat)
            print(self.seat_position)
    except TypeError:
        best_hand = [best_hand]  # needs to be nested inside of a list for dictionary lookup
        self.seat_position = self.hand_and_seat.get(str(best_hand))
    return self.seat_position

# Requires winning hand return to show all tied hands
# use a dictionary lookup on the cards to reveal the winning hand
def combine_hand_and_seat(self):
    self.hand_and_seat = {}
    for x in range(0, len(self.hand_details)):
        if str(self.hand_details[x][1]) in self.hand_and_seat:
            self.hand_and_seat[str([self.hand_details[x][1]])].append(x+1)  # needs to best nested inside of a list
        else:
            self.hand_and_seat[str([self.hand_details[x][1]])] = [x+1]  # needs to best nested inside of a list
    print(self.hand_and_seat)
    return self.hand_and_seat
'''
