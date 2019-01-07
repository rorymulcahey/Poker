# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PokerUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

# To do list:
# 1- finish run button by sending cards to debugtests **DONE
# 2- update comboboxes to not have duplicate results **DONE
# 3- Add button to randomly generate flop
# 4- Remove cards from deck when only 1 is in a hand

import sys
from PyQt4 import QtCore, QtGui
from Table import Deck, Card
from DebugTests import Debug


class MyApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.listify_comboboxes()


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class ComboBox(QtGui.QComboBox):
    new_signal = QtCore.pyqtSignal(int, int, QtGui.QComboBox)

    def __init__(self, parent=None):
        super(ComboBox, self).__init__(parent)
        # super(ComboBox, self).currentIndexChanged[int].connect(self.onActivated)
        self.last_index = 0
        self.currentIndexChanged[int].connect(self.onActivated)

    def onActivated(self, index):
        self.new_signal.emit(self.last_index, index, self)
        self.last_index = index


class Ui_MainWindow(object):
    def __init__(self):
        # initialize deck with all 52 cards
        self.deck = Deck()
        self.cards = self.deck.current_cards
        self.str_cards = self.deck.card_to_string(self.cards)
        self.debug = None
        self.comboboxes = []
        self.user_input_cards = []
        self.seat_numbers = []
        self.hand_probs = []
        self.probs = []
        self.current_cb = None
        self.error_msg = ' '

    def listify_comboboxes(self):
        self.comboboxes.append(self.Hand1_Card1)
        self.comboboxes.append(self.Hand1_Card2)
        self.comboboxes.append(self.Hand2_Card1)
        self.comboboxes.append(self.Hand2_Card2)
        self.comboboxes.append(self.Hand3_Card1)
        self.comboboxes.append(self.Hand3_Card2)
        self.comboboxes.append(self.Hand4_Card1)
        self.comboboxes.append(self.Hand4_Card2)
        self.comboboxes.append(self.Hand5_Card1)
        self.comboboxes.append(self.Hand5_Card2)
        self.comboboxes.append(self.Hand6_Card1)
        self.comboboxes.append(self.Hand6_Card2)
        self.comboboxes.append(self.Hand7_Card1)
        self.comboboxes.append(self.Hand7_Card2)
        self.comboboxes.append(self.Hand8_Card1)
        self.comboboxes.append(self.Hand8_Card2)
        self.comboboxes.append(self.Hand9_Card1)
        self.comboboxes.append(self.Hand9_Card2)
        self.comboboxes.append(self.Hand10_Card1)
        self.comboboxes.append(self.Hand10_Card2)
        self.comboboxes.append(self.Flop_Card1)
        self.comboboxes.append(self.Flop_Card2)
        self.comboboxes.append(self.Flop_Card3)
        self.comboboxes.append(self.Turn_Card)
        self.comboboxes.append(self.River_Card)
        self.setup_comboboxes()

    def listify_probabilities(self):
        self.hand_probs.append(self.Hand1_Prob)
        self.hand_probs.append(self.Hand2_Prob)
        self.hand_probs.append(self.Hand3_Prob)
        self.hand_probs.append(self.Hand4_Prob)
        self.hand_probs.append(self.Hand5_Prob)
        self.hand_probs.append(self.Hand6_Prob)
        self.hand_probs.append(self.Hand7_Prob)
        self.hand_probs.append(self.Hand8_Prob)
        self.hand_probs.append(self.Hand9_Prob)
        self.hand_probs.append(self.Hand10_Prob)

    @staticmethod
    def print_combobox_value(prev_index, curr_index, current_cb):

        # test to see index values
        print("Prev card: " + current_cb.itemText(prev_index))  # print prev item in list
        print("Curr card: " + current_cb.itemText(curr_index))  # print current item in list

    def get_user_cards(self):

        # loop through comboboxes and gather index values
        self.user_input_cards = []
        for cb in self.comboboxes:
            self.user_input_cards.append(cb.currentIndex())

    def import_data(self):

        # reset data
        self.debug = Debug()
        self.debug.preflop_cards = []
        self.debug.community_cards = []
        self.seat_numbers = []

        # loops through all cards selected in comboboxes
        for x in range(0, 10):
            if self.user_input_cards[2*x] != 0 and self.user_input_cards[2*x + 1] != 0:
                self.debug.preflop_cards.append([self.cards[self.user_input_cards[2*x] - 1],
                                                self.cards[self.user_input_cards[2*x + 1] - 1]])  # insert cards
                self.seat_numbers.append(x)

        for y in range(20, 23):  # loop all flop cards
            if self.user_input_cards[y] != 0:
                self.debug.community_cards.append(self.cards[self.user_input_cards[y] - 1])

        # make sure flop is full or produce error
        if len(self.debug.community_cards) < 3:
            return

        print(self.debug.community_cards)
        for y in range(23, 25):  # loop remaining community cards
            if self.user_input_cards[y] != 0:
                self.debug.community_cards.append(self.cards[self.user_input_cards[y] - 1])

    def setup_comboboxes(self):

        # initialize comboboxes
        for cb in self.comboboxes:
            cb.addItems(' ')
            cb.addItems(self.str_cards)
            cb.new_signal.connect(self.update_comboboxes)

    def update_comboboxes(self, prev_index, curr_index, current_cb):

        # loop through all comboboxes except current one
        for cb in self.comboboxes:

            # do not edit current cb
            if cb == current_cb:
                continue

            # allow previous index and disable current index from being selected
            cb.model().item(prev_index).setEnabled(True)
            if curr_index != 0:
                cb.model().item(curr_index).setEnabled(False)

            # initial empty cb set to itself
            if curr_index == 0 and prev_index == 0:
                # do nothing
                pass

            # restore old value and reinsert card into deck
            elif curr_index == 0 and prev_index != 0:
                cb.setItemData(prev_index, self.str_cards[prev_index - 1], 0)
                self.cards[prev_index - 1].in_deck = 1

            # currently in initial state and only update new comboboxes
            # and removes card from deck
            elif curr_index != 0 and prev_index == 0:
                cb.setItemData(curr_index, ' ', 0)
                self.cards[curr_index - 1].in_deck = 0

            # last state without initial empty cb
            else:  # curr_index != 0 and prev_index != 0:
                cb.setItemData(prev_index, self.str_cards[prev_index - 1], 0)  # restore old value
                self.cards[prev_index - 1].in_deck = 1  # reinsert card into deck
                cb.setItemData(curr_index, ' ', 0)  # update new comboboxes
                self.cards[curr_index - 1].in_deck = 0  # removes card from deck

    def clear_comboboxes(self):
        for cb in self.comboboxes:
            cb.setCurrentIndex(0)
            # cb.clear()  # Bug: Creates an extra combobox val for every click
        # self.setup_comboboxes()

    def clear_text(self):
        for hb in self.hand_probs:
            hb.setText(' ')
        self.ErrorMsg.setText(' ')

    def set_probabilities(self):
        self.clear_text()
        self.listify_probabilities()
        self.probs = self.debug.stats.winning_chances
        for x in range(0, len(self.seat_numbers)):
            self.hand_probs[self.seat_numbers[x]].setText(str(self.probs[x]) + ' %')

    def fail_error_check(self):
        if len(self.debug.preflop_cards) < 2:
            self.error_msg = "Must have at least 2 players..."
            return True
        if len(self.debug.community_cards) < 3:
            self.error_msg = "Must have at least 3 flop cards..."
            return True
        return False

    def run_program(self):
        self.get_user_cards()
        self.import_data()
        if self.fail_error_check():
            self.ErrorMsg.setText(self.error_msg)
            return
        self.debug.run_tests()
        self.set_probabilities()

    def clear(self):
        self.clear_comboboxes()
        self.clear_text()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(758, 474)
        MainWindow.setMinimumSize(QtCore.QSize(758, 474))
        MainWindow.setMaximumSize(QtCore.QSize(758, 474))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label_20 = QtGui.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(180, 10, 401, 41))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label_20.setFont(font)
        self.label_20.setObjectName(_fromUtf8("label_1"))
        self.groupBox_6 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_6.setGeometry(QtCore.QRect(370, 350, 171, 80))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox"))

        self.ErrorMsg = QtGui.QTextBrowser(self.groupBox_6)
        self.ErrorMsg.setGeometry(QtCore.QRect(10, 20, 151, 51))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ErrorMsg.sizePolicy().hasHeightForWidth())
        self.ErrorMsg.setSizePolicy(sizePolicy)
        self.ErrorMsg.setObjectName(_fromUtf8("ErrorMsg"))

        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 70, 351, 361))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayoutWidget = QtGui.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 40, 171, 311))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.Hand1_Card1 = ComboBox(self.verticalLayoutWidget)
        self.Hand1_Card1.setObjectName(_fromUtf8("Hand1_Card1"))
        self.horizontalLayout.addWidget(self.Hand1_Card1)

        self.Hand1_Card2 = ComboBox(self.verticalLayoutWidget)
        self.Hand1_Card2.setObjectName(_fromUtf8("Hand1_Card2"))
        self.horizontalLayout.addWidget(self.Hand1_Card2)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))

        self.Hand2_Card1 = ComboBox(self.verticalLayoutWidget)
        self.Hand2_Card1.setObjectName(_fromUtf8("Hand2_Card1"))
        self.horizontalLayout_5.addWidget(self.Hand2_Card1)

        self.Hand2_Card2 = ComboBox(self.verticalLayoutWidget)
        self.Hand2_Card2.setObjectName(_fromUtf8("Hand2_Card2"))
        self.horizontalLayout_5.addWidget(self.Hand2_Card2)

        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))

        self.Hand3_Card1 = ComboBox(self.verticalLayoutWidget)
        self.Hand3_Card1.setObjectName(_fromUtf8("Hand3_Card1"))
        self.horizontalLayout_3.addWidget(self.Hand3_Card1)

        self.Hand3_Card2 = ComboBox(self.verticalLayoutWidget)
        self.Hand3_Card2.setObjectName(_fromUtf8("Hand3_Card2"))
        self.horizontalLayout_3.addWidget(self.Hand3_Card2)

        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))

        self.Hand4_Card1 = ComboBox(self.verticalLayoutWidget)
        self.Hand4_Card1.setObjectName(_fromUtf8("Hand4_Card1"))
        self.horizontalLayout_2.addWidget(self.Hand4_Card1)

        self.Hand4_Card2 = ComboBox(self.verticalLayoutWidget)
        self.Hand4_Card2.setObjectName(_fromUtf8("Hand4_Card2"))
        self.horizontalLayout_2.addWidget(self.Hand4_Card2)

        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))

        self.Hand5_Card1 = ComboBox(self.verticalLayoutWidget)
        self.Hand5_Card1.setObjectName(_fromUtf8("Hand5_Card1"))
        self.horizontalLayout_9.addWidget(self.Hand5_Card1)

        self.Hand5_Card2 = ComboBox(self.verticalLayoutWidget)
        self.Hand5_Card2.setObjectName(_fromUtf8("Hand5_Card2"))
        self.horizontalLayout_9.addWidget(self.Hand5_Card2)

        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))

        self.Hand6_Card1 = ComboBox(self.verticalLayoutWidget)
        self.Hand6_Card1.setObjectName(_fromUtf8("Hand6_Card1"))
        self.horizontalLayout_10.addWidget(self.Hand6_Card1)

        self.Hand6_Card2 = ComboBox(self.verticalLayoutWidget)
        self.Hand6_Card2.setObjectName(_fromUtf8("Hand6_Card2"))
        self.horizontalLayout_10.addWidget(self.Hand6_Card2)

        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))

        self.Hand7_Card1 = ComboBox(self.verticalLayoutWidget)
        self.Hand7_Card1.setObjectName(_fromUtf8("Hand7_Card1"))
        self.horizontalLayout_11.addWidget(self.Hand7_Card1)

        self.Hand7_Card2 = ComboBox(self.verticalLayoutWidget)
        self.Hand7_Card2.setObjectName(_fromUtf8("Hand7_Card2"))
        self.horizontalLayout_11.addWidget(self.Hand7_Card2)

        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))

        self.Hand8_Card1 = ComboBox(self.verticalLayoutWidget)
        self.Hand8_Card1.setObjectName(_fromUtf8("Hand8_Card1"))
        self.horizontalLayout_4.addWidget(self.Hand8_Card1)

        self.Hand8_Card2 = ComboBox(self.verticalLayoutWidget)
        self.Hand8_Card2.setObjectName(_fromUtf8("Hand8_Card2"))
        self.horizontalLayout_4.addWidget(self.Hand8_Card2)

        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))

        self.Hand9_Card1 = ComboBox(self.verticalLayoutWidget)
        self.Hand9_Card1.setObjectName(_fromUtf8("Hand9_Card1"))
        self.horizontalLayout_6.addWidget(self.Hand9_Card1)

        self.Hand9_Card2 = ComboBox(self.verticalLayoutWidget)
        self.Hand9_Card2.setObjectName(_fromUtf8("Hand9_Card2"))
        self.horizontalLayout_6.addWidget(self.Hand9_Card2)

        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))

        self.Hand10_Card1 = ComboBox(self.verticalLayoutWidget)
        self.Hand10_Card1.setObjectName(_fromUtf8("Hand10_Card1"))
        self.horizontalLayout_8.addWidget(self.Hand10_Card1)

        self.Hand10_Card2 = ComboBox(self.verticalLayoutWidget)
        self.Hand10_Card2.setObjectName(_fromUtf8("Hand10_Card2"))
        self.horizontalLayout_8.addWidget(self.Hand10_Card2)

        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(260, 40, 73, 306))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

        self.Hand1_Prob = QtGui.QTextBrowser(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Hand1_Prob.sizePolicy().hasHeightForWidth())
        self.Hand1_Prob.setSizePolicy(sizePolicy)
        self.Hand1_Prob.setMaximumSize(QtCore.QSize(16777215, 25))
        self.Hand1_Prob.setObjectName(_fromUtf8("Hand1_Prob"))
        self.verticalLayout_2.addWidget(self.Hand1_Prob)

        self.Hand2_Prob = QtGui.QTextBrowser(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Hand2_Prob.sizePolicy().hasHeightForWidth())
        self.Hand2_Prob.setSizePolicy(sizePolicy)
        self.Hand2_Prob.setMaximumSize(QtCore.QSize(16777215, 25))
        self.Hand2_Prob.setObjectName(_fromUtf8("Hand2_Prob"))
        self.verticalLayout_2.addWidget(self.Hand2_Prob)

        self.Hand3_Prob = QtGui.QTextBrowser(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Hand3_Prob.sizePolicy().hasHeightForWidth())
        self.Hand3_Prob.setSizePolicy(sizePolicy)
        self.Hand3_Prob.setMaximumSize(QtCore.QSize(16777215, 25))
        self.Hand3_Prob.setObjectName(_fromUtf8("Hand3_Prob"))
        self.verticalLayout_2.addWidget(self.Hand3_Prob)

        self.Hand4_Prob = QtGui.QTextBrowser(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Hand4_Prob.sizePolicy().hasHeightForWidth())
        self.Hand4_Prob.setSizePolicy(sizePolicy)
        self.Hand4_Prob.setMaximumSize(QtCore.QSize(16777215, 25))
        self.Hand4_Prob.setObjectName(_fromUtf8("Hand4_Prob"))
        self.verticalLayout_2.addWidget(self.Hand4_Prob)

        self.Hand5_Prob = QtGui.QTextBrowser(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Hand5_Prob.sizePolicy().hasHeightForWidth())
        self.Hand5_Prob.setSizePolicy(sizePolicy)
        self.Hand5_Prob.setMaximumSize(QtCore.QSize(16777215, 25))
        self.Hand5_Prob.setObjectName(_fromUtf8("Hand5_Prob"))
        self.verticalLayout_2.addWidget(self.Hand5_Prob)

        self.Hand6_Prob = QtGui.QTextBrowser(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Hand6_Prob.sizePolicy().hasHeightForWidth())
        self.Hand6_Prob.setSizePolicy(sizePolicy)
        self.Hand6_Prob.setMaximumSize(QtCore.QSize(16777215, 25))
        self.Hand6_Prob.setObjectName(_fromUtf8("Hand6_Prob"))
        self.verticalLayout_2.addWidget(self.Hand6_Prob)

        self.Hand7_Prob = QtGui.QTextBrowser(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Hand7_Prob.sizePolicy().hasHeightForWidth())
        self.Hand7_Prob.setSizePolicy(sizePolicy)
        self.Hand7_Prob.setMaximumSize(QtCore.QSize(16777215, 25))
        self.Hand7_Prob.setObjectName(_fromUtf8("Hand7_Prob"))
        self.verticalLayout_2.addWidget(self.Hand7_Prob)

        self.Hand8_Prob = QtGui.QTextBrowser(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Hand8_Prob.sizePolicy().hasHeightForWidth())
        self.Hand8_Prob.setSizePolicy(sizePolicy)
        self.Hand8_Prob.setMaximumSize(QtCore.QSize(16777215, 25))
        self.Hand8_Prob.setObjectName(_fromUtf8("Hand8_Prob"))
        self.verticalLayout_2.addWidget(self.Hand8_Prob)

        self.Hand9_Prob = QtGui.QTextBrowser(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Hand9_Prob.sizePolicy().hasHeightForWidth())
        self.Hand9_Prob.setSizePolicy(sizePolicy)
        self.Hand9_Prob.setMaximumSize(QtCore.QSize(16777215, 25))
        self.Hand9_Prob.setObjectName(_fromUtf8("Hand9_Prob"))
        self.verticalLayout_2.addWidget(self.Hand9_Prob)

        self.Hand10_Prob = QtGui.QTextBrowser(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Hand10_Prob.sizePolicy().hasHeightForWidth())
        self.Hand10_Prob.setSizePolicy(sizePolicy)
        self.Hand10_Prob.setMaximumSize(QtCore.QSize(16777215, 25))
        self.Hand10_Prob.setObjectName(_fromUtf8("Hand10_Prob"))
        self.verticalLayout_2.addWidget(self.Hand10_Prob)

        self.horizontalLayoutWidget_7 = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget_7.setGeometry(QtCore.QRect(90, 20, 261, 30))
        self.horizontalLayoutWidget_7.setObjectName(_fromUtf8("horizontalLayoutWidget_7"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget_7)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_7.addWidget(self.label_2)
        self.label = QtGui.QLabel(self.horizontalLayoutWidget_7)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_7.addWidget(self.label)
        self.label_13 = QtGui.QLabel(self.horizontalLayoutWidget_7)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_7.addWidget(self.label_13)
        self.verticalLayoutWidget_3 = QtGui.QWidget(self.groupBox)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(20, 40, 61, 311))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_9 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_3.addWidget(self.label_9)
        self.label_10 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_3.addWidget(self.label_10)
        self.label_4 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.label_11 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.verticalLayout_3.addWidget(self.label_11)
        self.label_12 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.verticalLayout_3.addWidget(self.label_12)
        self.label_8 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_3.addWidget(self.label_8)
        self.label_7 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_3.addWidget(self.label_7)
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        self.label_6 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_3.addWidget(self.label_6)
        self.label_5 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_3.addWidget(self.label_5)
        self.groupBox_5 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(370, 70, 371, 271))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox_5)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 180, 161, 71))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.horizontalLayoutWidget_16 = QtGui.QWidget(self.groupBox_4)
        self.horizontalLayoutWidget_16.setGeometry(QtCore.QRect(70, 10, 81, 30))
        self.horizontalLayoutWidget_16.setObjectName(_fromUtf8("horizontalLayoutWidget_16"))
        self.horizontalLayout_26 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_16)
        self.horizontalLayout_26.setObjectName(_fromUtf8("horizontalLayout_26"))
        self.label_19 = QtGui.QLabel(self.horizontalLayoutWidget_16)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.horizontalLayout_26.addWidget(self.label_19)
        self.layoutWidget_2 = QtGui.QWidget(self.groupBox_4)
        self.layoutWidget_2.setGeometry(QtCore.QRect(60, 30, 91, 40))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.horizontalLayout_14 = QtGui.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.River_Card = ComboBox(self.layoutWidget_2)
        self.River_Card.setObjectName(_fromUtf8("River_Card"))
        self.horizontalLayout_14.addWidget(self.River_Card)
        self.horizontalLayoutWidget_17 = QtGui.QWidget(self.groupBox_4)
        self.horizontalLayoutWidget_17.setGeometry(QtCore.QRect(10, 20, 61, 21))
        self.horizontalLayoutWidget_17.setObjectName(_fromUtf8("horizontalLayoutWidget_17"))
        self.horizontalLayout_27 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_17)
        self.horizontalLayout_27.setObjectName(_fromUtf8("horizontalLayout_27"))

        self.groupBox_3 = QtGui.QGroupBox(self.groupBox_5)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 100, 161, 71))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayoutWidget_14 = QtGui.QWidget(self.groupBox_3)
        self.horizontalLayoutWidget_14.setGeometry(QtCore.QRect(70, 10, 81, 30))
        self.horizontalLayoutWidget_14.setObjectName(_fromUtf8("horizontalLayoutWidget_14"))
        self.horizontalLayout_24 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_14)
        self.horizontalLayout_24.setObjectName(_fromUtf8("horizontalLayout_24"))
        self.label_18 = QtGui.QLabel(self.horizontalLayoutWidget_14)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.horizontalLayout_24.addWidget(self.label_18)
        self.layoutWidget = QtGui.QWidget(self.groupBox_3)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 30, 91, 40))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.Turn_Card = ComboBox(self.layoutWidget)
        self.Turn_Card.setObjectName(_fromUtf8("Turn_Card"))
        self.horizontalLayout_13.addWidget(self.Turn_Card)
        self.horizontalLayoutWidget_15 = QtGui.QWidget(self.groupBox_3)
        self.horizontalLayoutWidget_15.setGeometry(QtCore.QRect(10, 20, 61, 21))
        self.horizontalLayoutWidget_15.setObjectName(_fromUtf8("horizontalLayoutWidget_15"))
        self.horizontalLayout_25 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_15)
        self.horizontalLayout_25.setObjectName(_fromUtf8("horizontalLayout_25"))
        self.layoutWidget.raise_()
        self.horizontalLayoutWidget_15.raise_()
        self.horizontalLayoutWidget_14.raise_()
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox_5)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 20, 351, 71))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayoutWidget_12 = QtGui.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_12.setGeometry(QtCore.QRect(70, 10, 271, 31))
        self.horizontalLayoutWidget_12.setObjectName(_fromUtf8("horizontalLayoutWidget_12"))
        self.horizontalLayout_22 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_12)
        self.horizontalLayout_22.setObjectName(_fromUtf8("horizontalLayout_22"))
        self.label_15 = QtGui.QLabel(self.horizontalLayoutWidget_12)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_22.addWidget(self.label_15)
        self.label_16 = QtGui.QLabel(self.horizontalLayoutWidget_12)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.horizontalLayout_22.addWidget(self.label_16)
        self.label_14 = QtGui.QLabel(self.horizontalLayoutWidget_12)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.horizontalLayout_22.addWidget(self.label_14)
        self.layoutWidget_3 = QtGui.QWidget(self.groupBox_2)
        self.layoutWidget_3.setGeometry(QtCore.QRect(60, 30, 281, 38))
        self.layoutWidget_3.setObjectName(_fromUtf8("layoutWidget_3"))
        self.horizontalLayout_12 = QtGui.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.Flop_Card1 = ComboBox(self.layoutWidget_3)
        self.Flop_Card1.setObjectName(_fromUtf8("Flop_Card1"))
        self.horizontalLayout_12.addWidget(self.Flop_Card1)
        self.Flop_Card2 = ComboBox(self.layoutWidget_3)
        self.Flop_Card2.setObjectName(_fromUtf8("Flop_Card2"))
        self.horizontalLayout_12.addWidget(self.Flop_Card2)
        self.Flop_Card3 = ComboBox(self.layoutWidget_3)
        self.Flop_Card3.setObjectName(_fromUtf8("Flop_Card3"))
        self.horizontalLayout_12.addWidget(self.Flop_Card3)
        self.horizontalLayoutWidget_13 = QtGui.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_13.setGeometry(QtCore.QRect(10, 20, 61, 21))
        self.horizontalLayoutWidget_13.setObjectName(_fromUtf8("horizontalLayoutWidget_13"))
        self.horizontalLayout_23 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_13)
        self.horizontalLayout_23.setObjectName(_fromUtf8("horizontalLayout_23"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(570, 400, 160, 40))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_15 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))

        self.Run = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.Run.setObjectName(_fromUtf8("Run"))
        self.horizontalLayout_15.addWidget(self.Run)
        self.Run.clicked.connect(self.run_program)  # runs DebugTests.py

        self.Clear = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.Clear.setObjectName(_fromUtf8("Clear"))
        self.horizontalLayout_15.addWidget(self.Clear)
        self.Clear.clicked.connect(self.clear)  # runs DebugTests.py

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 758, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_20.setText(_translate("MainWindow", "Poker Hand Solver", None))
        self.groupBox_6.setTitle(_translate("MainWindow", "Error Msg", None))
        self.groupBox.setTitle(_translate("MainWindow", "Preflop", None))
        self.label_2.setText(_translate("MainWindow", "Card 1", None))
        self.label.setText(_translate("MainWindow", "Card 2", None))
        self.label_13.setText(_translate("MainWindow", "Probability", None))
        self.label_9.setText(_translate("MainWindow", "Hand 1", None))
        self.label_10.setText(_translate("MainWindow", "Hand 2", None))
        self.label_4.setText(_translate("MainWindow", "Hand 3", None))
        self.label_11.setText(_translate("MainWindow", "Hand 4", None))
        self.label_12.setText(_translate("MainWindow", "Hand 5", None))
        self.label_8.setText(_translate("MainWindow", "Hand 6", None))
        self.label_7.setText(_translate("MainWindow", "Hand 7", None))
        self.label_3.setText(_translate("MainWindow", "Hand 8", None))
        self.label_6.setText(_translate("MainWindow", "Hand 9", None))
        self.label_5.setText(_translate("MainWindow", "Hand 10", None))
        self.groupBox_5.setTitle(_translate("MainWindow", "Community Cards", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "River", None))
        self.label_19.setText(_translate("MainWindow", "Card ", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Turn", None))
        self.label_18.setText(_translate("MainWindow", "Card ", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Flop", None))
        self.label_15.setText(_translate("MainWindow", "Card 1", None))
        self.label_16.setText(_translate("MainWindow", "Card 2", None))
        self.label_14.setText(_translate("MainWindow", "Card 3", None))
        self.Run.setText(_translate("MainWindow", "Run", None))
        self.Clear.setText(_translate("MainWindow", "Clear", None))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.setWindowTitle("Texas Hold'em")
    window.show()
    sys.exit(app.exec_())
