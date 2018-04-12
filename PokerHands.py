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


def check_hand(card1,card2,card3,card4,card5,card6,card7):
    allcards = []
    allcards = [card1,card2,card3,card4,card5,card6,card7]
    #print(allcards)
    #print(allcards[0][0])

    #currently counts any pair of suited cards. need to differentiate between suits.
    number = 1
    for x in range(0, 6):
        find = False
        for y in range(0, 6):
            if allcards[x][0] == allcards[y][0] and x != y:
                #need to omit instances where a previous match has been made
                print(allcards[x][0], x, y)
                number += 1
            if number == 5:
                print("You are suited!")
                find = True
                break
        if find:
            break









preflop1 = preflop('c', 1)
preflop2 = preflop('d', 1)
preflop_hand(preflop1.card[0], preflop1.card[1], preflop2.card[0], preflop2.card[1])

flop1 = community_card('d', 1)
flop2 = community_card('d', 13)
flop3 = community_card('h', 12)
turn = community_card('h', 11)
river = community_card('h', 10)

check_hand(preflop1.card,preflop2.card,flop1.card,flop2.card,flop3.card,turn.card,river.card)
#print(flop1.card, river.card)














