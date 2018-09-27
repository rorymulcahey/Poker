"""

 This  file will contain everything that entails a poker deck.
 That will include all 52 cards possible in play.


"""


class Deck:
    def __init__(self):
        self.current_cards = []
        self.create_deck()

    def create_deck(self):
        self.current_cards = []
        for x in ['c', 'd', 'h', 's']:
            for y in range(1, 14):
                self.current_cards.append(Card(x, y))


class Card:
    def __init__(self, suit, number):
        # super().__init__()
        self.suit = suit
        self.num = number

    def __repr__(self):
        # return self.suit + str(self.num)
        return "Card('" + self.suit + "', " + str(self.num) + ")"


if __name__ == "__main__":
    deck = Deck()
    print(deck.current_cards)
