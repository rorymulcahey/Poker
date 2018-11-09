
from SolvePokerHands import *
from collections import Counter


class Probability:
    def __init__(self, remaining_deck, preflop_hands, comm_cards):
        self.community_cards = comm_cards
        self.preflop_hands = preflop_hands
        self.current_deck = remaining_deck
        self.current_cards_in_play = Hand(preflop_hands, self.community_cards)
        self.deck_num_array = self.create_deck_num_array(self.current_deck)
        self.winning_chances = len(self.preflop_hands) * [0]
        self.drawing_chances = len(self.preflop_hands) * [0]
        self.number_of_cards_remaining()

    def create_deck_num_array(self, cards):
        return self.current_cards_in_play.cards_number_array(cards)

    '''
    Driver function that calls the appropriate starter function. Here there are currently three working, and one
    still needing to be made, functions. Based on the number of community cards, a specific function will be called
    to find the probability of a winning hand.  
    '''
    def number_of_cards_remaining(self):
        total = len(self.current_deck)
        if len(self.community_cards) == 4:
            self.one_card_remaining(self.current_deck.copy())
        elif len(self.community_cards) == 3:
            self.two_cards_remaining(self.current_deck.copy())
            total *= total - 1
        elif len(self.community_cards) == 0:
            self.five_cards_remaining()
        else:
            total = 1
            winning_hand = HandCompare(self.preflop_hands, self.community_cards)
            winning_seat = winning_hand.get_winning_seat_position()  # needs hand list
            self.calculate_winning_chances(winning_hand, winning_seat, None)
        self.winning_chances[:] = [round(j * 100 / total, 2) for j in self.winning_chances]
        self.drawing_chances[:] = [round(k * 100 / total, 2) for k in self.drawing_chances]
        self.print_probabilities()

    '''
    Here the function will first check if a flush is possible,
    meaning that there is at least 2 community cards of the same suit. If so it will iterate through each of those
    cards in the remaining deck. There cards are popped off a copy of the remaining deck of cards. If this condition 
    is not true then we go directly to the number array choice (section 2). This portion uses a deck_cards number 
    array, which increments the index of a list for each occurrence of a specific number of card. Very similar to the 
    card number array that exists in the SolvePokerHands.py except this array looks for every card that is remaining in 
    the deck_cards and only those cards. The function uses that deck_cards number array to iterate through all the 
    possible hands that a user can make. Then it multiplies the outcome of the hand by the number of card occurrences 
    that happen in the deck_cards. This reduces the number of times the SolvePokerHands.py needs to run by 
    approximately a factor of 3.
    '''
    def one_card_remaining(self, current_deck):
        # section 1 using flush suit
        deck_cards = current_deck
        self.deck_num_array = self.create_deck_num_array(current_deck)
        flush_suit = []
        for z in range(0, 4):
            flush_suit.append(self.community_cards[z].suit)
        flush_suit = Counter(flush_suit).most_common(1)
        if flush_suit[0][1] > 1:
            flush_suit = flush_suit[0][0]
        else:
            flush_suit = None
        if flush_suit:
            length = len(deck_cards)
            y = 0
            while length > y:
                if deck_cards[y].suit == flush_suit:
                    self.community_cards.append(deck_cards[y])
                    winning_hand = HandCompare(self.preflop_hands, self.community_cards)
                    winning_seat = winning_hand.get_winning_seat_position()  # needs hand list
                    self.calculate_winning_chances(winning_hand, winning_seat, None)
                    self.community_cards.pop()
                    self.deck_num_array[deck_cards[y].num - 1] -= 1
                    deck_cards.pop(y)
                    length -= 1
                    y -= 1
                y += 1

        # section 2 using number array
        w = -1  # increases the speed by immediately picking a card
        for y in range(0, len(self.deck_num_array)-1):
            w += self.deck_num_array[y]  # relies on numerically sorted deck_cards
            if self.deck_num_array[y] > 0:
                self.community_cards.append(deck_cards[w])
                winning_hand = HandCompare(self.preflop_hands, self.community_cards)
                winning_seat = winning_hand.get_winning_seat_position()  # needs hand list
                self.calculate_winning_chances(winning_hand, winning_seat, y)
                self.community_cards.pop()

    '''
    This function finds the probability of winning on the flop. It first loops through all
    possible cards, appending it to the community cards one at a time. Then it calls
    one_card_remaining to handle the rest of the calculating.
    
    Input: Is a copy of the deck, so as to the change the original (probably can be optimized).
    
    Output: Probability of winning hand when two cards need to be dealt.
    '''
    def two_cards_remaining(self, current_deck):
        # modifies one community card and send the rest of the deck into one card remaining
        for x in range(0, len(current_deck)):
            deck_cards = current_deck
            self.community_cards.append(deck_cards[x])
            deck_cards = [n for n in deck_cards if n != deck_cards[x]]  # removes deck_cards[x] from the deck
            self.one_card_remaining(deck_cards)
            self.community_cards.pop()

    def five_cards_remaining(self):
        pass

    '''
    This function does the math required to add percentage probabilities to the final output. The function handles
    two types of input. One cases where the final probabilities being assigned to the winning seats will be multiplied
    by the number of cards that have the two, three, ... , king, ace value and the other cases where we analyze flush
    cards and do not need to multiply (or multiply by 1) the output probability. This reduces the number of times
    that HandCompare needs to be called and speeds up the function. Ideally this concept can be optimized.
    '''
    def calculate_winning_chances(self, winning_hand, winning_seat, card_number):
        if card_number is not None:
            if len(winning_seat) == 1:
                self.winning_chances[winning_seat[0] - 1] += self.deck_num_array[card_number]
            else:  # drawing chances
                for i in range(0, len(winning_seat)):
                    self.drawing_chances[winning_seat[i] - 1] += \
                        float(self.deck_num_array[card_number])/len(winning_seat)
        else:  # card_number is None
            if len(winning_seat) == 1:
                self.winning_chances[winning_seat[0] - 1] += 1
            else:  # drawing chances
                for i in range(0, len(winning_seat)):
                    self.drawing_chances[winning_seat[i] - 1] += (1.0/len(winning_seat))
        winning_hand.print_winning_hand()

    def print_probabilities(self):
        print("Winning chances: " + str(self.winning_chances))
        print("Drawing chances: " + str(self.drawing_chances))
