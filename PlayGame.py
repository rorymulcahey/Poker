"""

 This  file will contain the needed code to play a poker game. This class
 will handle the needed code to execute normal game functionality. It will
 include the ability to find the players turn, give action to the player on
 their turn, calculate bet sizes, verify if bet size is valid, etc.
 Stored here is the information about each players chip count, how many
 players are in the hand, the size of the pot, all side pots, etc.


"""
from CurrentHand import CurrentHand


class PlayGame:
    def __init__(self, max_num_seats):
        self.hand = CurrentHand(max_num_seats)
        # bets in front of the player, not yet into the pot
        self.current_bet_amounts = []
        self.current_chip_counts = self.chip_counts()
        # why does this need to be +1
        self.current_seat_turn = self.hand.next_seat(self.hand.button_seat, 3)
        self.bet_amount = 0

    def chip_counts(self):
        chip_counts = []
        for x in range(0, len(self.hand.current_table.active_player_info)):
            chip_counts.append(self.hand.current_table.active_player_info[x].chip_count)
        return chip_counts

    def main_pot(self):
        return self.hand.main_pot

    def add_to_pot(self, chip_size):
        if self.main_pot:
            self.hand.main_pot += chip_size
        else:
            pass

    def player_raise(self):
        self.bet_amount = int(input("Enter a raise amount: "))
        if not self.bet_amount_valid():
            print("Bet amount invalid")
            return
        self.add_to_pot(self.bet_amount)
        self.hand.current_table.active_player_info[self.current_seat_turn - 1].chip_count \
            = self.hand.current_table.active_player_info[self.current_seat_turn - 1].chip_count - self.bet_amount

    def bet_amount_valid(self):
        if self.bet_amount > self.hand.current_table.active_player_info[self.current_seat_turn - 1].chip_count:
            return False
        else:
            return True

    def player_fold(self):
        # print(self.hand.current_table.active_player_info)
        # print(self.current_seat_turn)
        self.hand.current_table.active_player_info[(self.current_seat_turn - 1)] = None
        print("player folds")

    def player_check(self):
        # pass turn, move to next player
        print("player checks, next players turn")

    def player_call(self):
        # requires a bet amount from a previous player
        # need to make handle turn
        print("player calls amount")

    def deal_card(self):
        self.hand.get_card()

    def handle_turn(self):
        first_seat = self.current_seat_turn
        while True:
            action = {
                'R': self.player_raise,
                'F': self.player_fold,
                'CH': self.player_check,
                'CA': self.player_call
            }
            action[input("Would you like to:\n (R)aise\n (F)old\n (Ca)ll\n (Ch)eck\nEnter action: ").upper()]()
            self.current_seat_turn = self.hand.next_seat(self.current_seat_turn, 1)
            if first_seat == self.current_seat_turn or self.hand.current_player_count() == 1:
                break

    def handle_game(self):
        num_players = len(self.hand.current_table.active_player_info)
        while num_players > 1:
            break


game = PlayGame(2)
game.handle_turn()
result = []
for y in range(0, len(game.hand.current_table.active_player_info)):
    if game.hand.current_table.active_player_info[y] is None:
        result.append(None)
    else:
        result.append(game.hand.current_table.active_player_info[y].chip_count)

# test Playgame.py
# print(result)
# print(game.hand.button_seat)
# print(game.hand.player_cards)
# print(game.hand.deck.current_cards)
# print(game.current_seat_turn)
