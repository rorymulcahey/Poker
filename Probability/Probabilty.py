from SolvePokerHands import *


class Probability:
    def __init__(self):
        self.percentage = 0
        self.winning_hands = 0
        self.total_hands = 1
        self.num_of_players = 2
        self.cards_remaining = 0

    def calculate(self):
        if self.cards_remaining == 0:
            return self.winning_hands/self.total_hands

