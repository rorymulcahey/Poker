'''
Notation
c : clubs
d : diamonds
h : hearts
s : spades
1 : ace
2 : two
3 : three
4 : four
5 : five
6 : six
7 : seven
8 : eight
9 : nine
10 : ten
11 : jack
12 : queen
13 : king

Code:
place suit first, then number for card arrays

'''



class community_card:

    def __init__(self, suit, num):
        self.suit = suit
        self.num = num
        #num = str(num)
        self.card = suit, num



class preflop:

    def __init__(self, suit, num):
        self.suit = ""
        self.num = 0
        self.card = suit, num



def preflop_hand(suit1, num1, suit2, num2):
    if suit1 == suit2:
        print("You are suited!")
    if num1 == num2:
        print("You are paired!")
    if num1 == num2 + 1 or num1 == num2 - 1:
       print("You are connected!")



#assign values of 1 for numerical cards in play and zeros for cards not in play
def cards_number_array(card1,card2,card3,card4,card5,card6,card7):
    allcards = [card1, card2, card3, card4, card5, card6, card7]
    array = [0] * 14
    for y in range(0, 7):
        if allcards[y][1]:
            array[allcards[y][1]-1] += 1
            if array[allcards[y][1]-1] == 1:
                array[13] = 1
    return array



def check_flush(card1,card2,card3,card4,card5,card6,card7):
    allcards = [card1,card2,card3,card4,card5,card6,card7]
    for x in range(0, 7):
        number = 1
        flush = False
        for y in range(0, 7):
            if allcards[x][0] == allcards[y][0] and x != y:
                number += 1
            if number == 5:
                print("You have a flush!")
                flush = True
                break
        if flush:
            break



def check_straight(array):
    array = cards_number_array(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
    straight = False
    for x in range(0, 14):
        if array[x] == 1:
            number = 0
            for y in range(0, 5):
                if x+y < 14 and array[x+y] == 1:
                    number += 1
                else:
                    break
            if number == 5:
                straight = True
                break
    if straight:
        print("You have a straight!")
        return True



def check_pair(card1,card2,card3,card4,card5,card6,card7):
    pair = False
    return

def check_high_card(card1,card2,card3,card4,card5,card6,card7):
    high_card = False
    return

def check_two_pair(card1,card2,card3,card4,card5,card6,card7):
    two_pair = False
    return

def check_trips(card1,card2,card3,card4,card5,card6,card7):
    trips = False
    return

def check_fullhouse(card1,card2,card3,card4,card5,card6,card7):
    fullhouse = False
    return

def check_quads(card1,card2,card3,card4,card5,card6,card7):
    quads = False
    return

def check_straight_flush(card1,card2,card3,card4,card5,card6,card7):
    straight_flush = False
    return



#Cards in play:
preflop1 = preflop('c', 1)
preflop2 = preflop('h', 12)
flop1 = community_card('d', 10)
flop2 = community_card('d', 12)
flop3 = community_card('d', 8)
turn = community_card('d', 11)
river = community_card('d', 13)

#Functions to check hand combinations:
preflop_hand(preflop1.card[0], preflop1.card[1], preflop2.card[0], preflop2.card[1])
check_flush(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
#check_straight(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
check_straight(cards_number_array)














