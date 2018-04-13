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
    #print(preflop1.card, preflop2.card)
    if suit1 == suit2:
        print("You are suited!")

    if num1 == num2:
        print("You are paired!")


    if num1 == num2 + 1 or num1 == num2 - 1:
       print("You are connected!")
    #print('Your hand is :', suit1, num1, suit2, num2)



def check_flush(card1,card2,card3,card4,card5,card6,card7):
    allcards = []
    allcards = [card1,card2,card3,card4,card5,card6,card7]
    #print(allcards)
    #print(allcards[0][0])

    #currently counts any pair of suited cards. need to differentiate between suits.

    for x in range(0, 7):
        number = 1
        flush = False
        #print(x)
        for y in range(0, 7):
            if allcards[x][0] == allcards[y][0] and x != y:
                #print(allcards[x][0], x, y)
                number += 1
            if number == 5:
                print("You have a flush!")
                flush = True
                break
        if flush:
            break



def check_straight(card1,card2,card3,card4,card5,card6,card7):
    allcards = [card1, card2, card3, card4, card5, card6, card7]
    array = [0] * 14
    straight = False

    #arrange values of 1 for numerical card values
    for y in range(0, 7):
        print([allcards[y][1]])
        if allcards[y][1]:
            array[allcards[y][1]-1] = 1
            if array[allcards[y][1]-1] == 1:
                array[13] = 1
    for x in range(0, 14):
        if array[x] == 1:
            number = 1
            for y in range(1, 4):
                if array[x+y] == 1:
                    number += 1
                else:
                    break
            if number == 5:
                straight = True
                break
    if straight:
        print("You have a straight!")

     #print(array)
        #if find:
            #break





preflop1 = preflop('c', 1)
preflop2 = preflop('c', 1)
preflop_hand(preflop1.card[0], preflop1.card[1], preflop2.card[0], preflop2.card[1])

flop1 = community_card('c', 1)
flop2 = community_card('d', 7)
flop3 = community_card('d', 12)
turn = community_card('d', 11)
river = community_card('d', 10)

check_flush(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
check_straight(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
#print(flop1.card, river.card)














