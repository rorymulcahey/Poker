"""
 
 This  file will contain the needed code to setup a poker table.
 Stored here is the information about each players chip count, the location
 of the button and big blind. Using that information, the program will begin
 to assign chip counts and cards to each seat of the table. Then it will 
 collect antes and blinds from the players, preparing the entire game to 
 be played. Seats are one-indexed.
 

"""
import random

# to do:
# need way to access player variables


class Table:
    # takes in as parameters the total number of seats on the table and starting chip amounts
    def __init__(self, max_num_seats):
        self.starting_chip_count = 2000
        self.active_player_info = []
        self.active_num_players = 0
        # need a better way to organize seat layout
        self.possible_seats = max_num_seats
        self.button = 1
        self.table_number = 1
        self.create_new_table()

    # needs dynamic blind level allocation
    def create_new_table(self):
        for x in range(0, self.possible_seats):
            if self.possible_seats:
                self.active_player_info.append(NewPlayer(x+1, self.starting_chip_count, self.table_number))
                self.active_num_players += 1
            # currently will not enter this block. need to add empty seat capability
            else:
                self.active_player_info[x] = None
        self.place_button()

    # needs update
    # use high card to place button
    def place_button(self):
        self.button = random.randint(1, self.possible_seats)

    def active_players(self):
        return self.active_player_info

    def set_blind_levels(self):
        pass


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


class Deck:
    def __init__(self, pixmap=False):
        self.current_cards = []
        if not pixmap:
            self.suits = ['c', 'd', 'h', 's']
        else:
            self.suits = ['d', 'h', 's', 'c']
        self.create_deck()

    def create_deck(self):
        self.current_cards = []
        for x in range(len(self.suits)):
            for y in range(1, 14):
                self.current_cards.append(Card(self.suits[x], y))

    def card_to_string(self, cards):
        # self.str_cards = []
        string_cards = []
        for x in range(0, len(cards)):
            string_cards.append(str(cards[x].suit) + str(cards[x].num))
        return string_cards


class Card(object):
    def __init__(self, suit, number):
        # super().__init__()
        self.suit = suit
        self.num = number
        self.in_deck = 1

    def __repr__(self):
        # return self.suit + str(self.num)
        # return str(self.__dict__)
        return "Card('" + self.suit + "', " + str(self.num) + ")"

    # def __str__(self):
        # return str(self.__dict__)

    def __eq__(self, other):
        # return self.__dict__ == other.__dict__
        if isinstance(other, Card):
            return self.num == other.num and self.suit == other.suit
        else:
            return other  # returns False if compared with None or 0


if __name__ == "__main__":
    deck = Deck()
    print(deck.current_cards)
