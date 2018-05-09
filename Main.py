from PyQt4 import QtCore, QtGui
from Poker_ui import Ui_Form
from PokerHands_solve import *

constants = {
    'hand1': (0, 0),
    'hand2': (0, 0),
    'hand3': (0, 0),
    'hand4': (6.4*10**6, 9.81),
    'hand5': (0, 0),
    'hand6': (0, 0),
    'hand7': (0, 0),
    'hand8': (0, 0),
    'hand9': (0, 0),
    'hand10': (0, 0)
    }

class MyForm(QtGui.QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.radioButtons = QtGui.QButtonGroup(self)
        self.radioButtons.addButton(self.hand1)
        self.radioButtons.addButton(self.hand2)
        self.radioButtons.addButton(self.hand3)
        self.radioButtons.addButton(self.hand4)
        self.radioButtons.addButton(self.hand5)
        self.radioButtons.addButton(self.hand6)
        self.radioButtons.addButton(self.hand7)
        self.radioButtons.addButton(self.hand8)
        self.radioButtons.addButton(self.hand9)
        self.radioButtons.addButton(self.hand10)
        self.pushButton.clicked.connect(self.main)

    def main(self):
        # Cards in play:
        self.hand1 = [Card('s', 4), Card('s', 3)]
        self.hand2 = [Card('s', 1), Card('h', 7)]
        self.hand3 = None
        self.hand4 = None
        self.hand5 = [Card('h', 13), Card('c', 13)]
        self.hand6 = None
        self.hand7 = None
        self.hand8 = None
        self.hand9 = None
        self.hand10 = None
        preflophands = [self.hand1, self.hand2, self.hand3, self.hand4, self.hand5,
                        self.hand6, self.hand7, self.hand8, self.hand9, self.hand10]
        hand_position = [0] * 10

        # remove 'None' hands from preflop cards list
        # consider using this with create_player_hand to remove empty preflop hands and store position
        # all_preflop_hands, number_of_hands, hand_positions = all_hands(hands)
        # hands are numerically ordered in accordance with their seat position #
        for x in range(0, 10):
            if preflophands[x] is not None:
                hand_position[x] = 1
        print(hand_position)
        index = 0
        number_of_hands = 10
        while index < number_of_hands and preflophands:
            if preflophands[index] is None:
                del preflophands[index]
                number_of_hands -= 1
                index -= 1
            index += 1

        flop1 = Card('d', 13)
        flop2 = Card('s', 11)
        flop3 = Card('s', 10)
        turn = Card('s', 12)
        river = Card('s', 13)
        community_cards = [flop1, flop2, flop3, turn, river]

        hands = []
        hand_strengths = []
        all_hand_details = []
        for x in range(0, index):
            hands.append(Hand(preflophands[x], community_cards))
            hand_strengths.append(HandType(hands[x].get_num_array(), hands[x].possible_cards()))
            all_hand_details.append(hand_strengths[x].check_hand_strength())
        winning_hand = HandCompare(all_hand_details)
        print("Winning hand is:", winning_hand.compare_hand_strength())


if __name__ == "__main__":

    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())