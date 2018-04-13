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



#assign values of 1 or more for numerical cards in play and zeros for cards not in play
def cards_number_array(card1,card2,card3,card4,card5,card6,card7):
    allcards = [card1, card2, card3, card4, card5, card6, card7]
    array = [0] * 14
    for y in range(0, 7):
        array[allcards[y][1]-1] += 1
        if array[allcards[y][1]-1] == array[0]:
            array[13] += 1
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
            return True



def check_straight():
    array = cards_number_array(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
    straight = False
    for x in range(0, 14):
        if array[x] == 1:
            number = 0
            for y in range(0, 5):
                if x+y < 14 and array[x+y] >= 1:
                    number += 1
                else:
                    break
            if number == 5:
                straight = True
                break
    if straight:
        print("You have a straight!")
        return True



def check_pair():
    array = cards_number_array(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
    pair = False
    for x in range(0, 14):
        if array[x] == 2:
            pair = True
    if pair:
        print("You have a pair!")
    return True



def check_high_card():
    array = cards_number_array(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
    high_card = False
    if high_card:
        print("You have a high card!")
    return True



def check_two_pair():
    array = cards_number_array(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
    two_pair = False
    number = 0
    for x in range(0, 14):
        if array[x] == 2:
            number += 1
        if number == 2:
            two_pair = True
    if two_pair:
        print("You have two pair!")
    return True



def check_trips():
    array = cards_number_array(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
    trips = False
    for x in range(0, 14):
        if array[x] == 3:
            trips = True
    if trips:
        print("You have a trips!")
    return True



#incomplete
def check_fullhouse():
    array = cards_number_array(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
    fullhouse = False
    if fullhouse:
        print("You have a fullhouse!")
    return True



def check_quads():
    array = cards_number_array(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
    quads = False
    for x in range(0, 14):
        if array[x] == 4:
            quads = True
    if quads:
        print("You have quads!")
    return True



#incomplete
def check_straight_flush():
    straight_flush = False
    if straight_flush:
        print("You have a straight flush!")
    return True



#Cards in play:
preflop1 = preflop('c', 1)
preflop2 = preflop('h', 1)
flop1 = community_card('d', 10)
flop2 = community_card('d', 10)
flop3 = community_card('d', 10)
turn = community_card('d', 10)
river = community_card('d', 13)

#Functions to check hand combinations:
preflop_hand(preflop1.card[0], preflop1.card[1], preflop2.card[0], preflop2.card[1])
check_flush(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
check_straight()
check_pair()
check_two_pair()
check_trips()
check_quads()











