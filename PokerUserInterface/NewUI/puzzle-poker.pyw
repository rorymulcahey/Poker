#!/usr/bin/env python

#############################################################################
#
#  Copyright (C) 2010 Riverbank Computing Limited.
#  Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
#  All rights reserved.
#
#  This file is part of the examples of PyQt.
#
#  $QT_BEGIN_LICENSE:BSD$
#  You may use this file under the terms of the BSD license as follows:
#
#  "Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#    * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
#      the names of its contributors may be used to endorse or promote
#      products derived from this software without specific prior written
#      permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
#  $QT_END_LICENSE$
#
#############################################################################


# This is only needed for Python v2 but is harmless for Python v3.
# import sip
import random
from PyQt4 import QtCore, QtGui
from Table import Deck
from DebugTests import Debug
from contextlib import contextmanager

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


# need to add remove card functionalities with streams
class PokerHands(QtGui.QWidget):

    solvePokerHands = QtCore.pyqtSignal()

    def __init__(self, card_location, main_window, parent=None, probability_obj=None):
        super(PokerHands, self).__init__(parent)

        self.main_window = main_window
        self.card_location = card_location
        self.probabilityObj = probability_obj
        self.piecePixmaps = []
        self.pieceRects = []
        self.pieceLocations = []
        self.highlightedRect = QtCore.QRect()
        self.inPlace = 0
        self.deck = Deck(pixmap=True)
        self.cards = self.deck.current_cards
        self.currentCards = []

        # pixel dimensions card placement map
        self.setAcceptDrops(True)
        if card_location < 10:
            self.setMinimumSize(88, 64)
            self.setMaximumSize(88, 64)
        else:
            self.setMinimumSize(220, 64)

    def clear(self):
        self.pieceLocations = []
        self.piecePixmaps = []
        self.pieceRects = []
        self.highlightedRect = QtCore.QRect()
        self.inPlace = 0
        self.update()

    def dragEnterEvent(self, event):
        # print(event)
        if event.mimeData().hasFormat('image/x-puzzle-piece'):
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        # print(event)
        updateRect = self.highlightedRect
        self.highlightedRect = QtCore.QRect()
        self.update(updateRect)
        event.accept()

    @contextmanager
    def wait_cursor(function):
        try:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            yield
        finally:
            QtGui.QApplication.restoreOverrideCursor()

    def dragMoveEvent(self, event):
        updateRect = self.highlightedRect.united(self.targetSquare(event.pos()))

        if event.mimeData().hasFormat('image/x-puzzle-piece') and self.findPiece(self.targetSquare(event.pos())) == -1:
            self.highlightedRect = self.targetSquare(event.pos())
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            self.highlightedRect = QtCore.QRect()
            event.ignore()

        self.update(updateRect)

    def dropEvent(self, event):
        if event.mimeData().hasFormat('image/x-puzzle-piece') and self.findPiece(self.targetSquare(event.pos())) == -1:
            pieceData = event.mimeData().data('image/x-puzzle-piece')
            stream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            square = self.targetSquare(event.pos())
            pixmap = PixMapCard()
            location = QtCore.QPoint()
            stream >> pixmap >> location
            pixmap = self.getPixmapCard(pixmap, location)

            # needs removal
            # needs picking up and dropping same card
            self.currentCards.append(pixmap.card_value)
            # print(pixmap.card_value)

            self.pieceLocations.append(location)
            self.piecePixmaps.append(pixmap)
            self.pieceRects.append(square)

            self.hightlightedRect = QtCore.QRect()
            self.update(square)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

            self.probabilityObj.updateTable(self.card_location, pixmap.card_value, self.main_window)
            # solves the "puzzle" (useful for identifying cards)
            # for poker: replace with cards values
            if location == QtCore.QPoint(square.x() / 48, square.y() / 64):
                self.inPlace += 1
                if self.inPlace == 5:
                    self.solvePokerHands.emit()
            self.highlightedRect = QtCore.QRect()
        else:
            self.highlightedRect = QtCore.QRect()
            event.ignore()

    def findPiece(self, pieceRect):
        try:
            # print(pieceRect)
            # print(self.pieceRect.index(pieceRect))
            return self.pieceRects.index(pieceRect)
        except ValueError:
            return -1

    def mousePressEvent(self, event):
        with self.wait_cursor():
            square = self.targetSquare(event.pos())
            found = self.findPiece(square)
            # print(found)

            if found == -1:
                return

            location = self.pieceLocations[found]
            # print(location)
            pixmap = self.piecePixmaps[found]

            del self.pieceLocations[found]
            del self.piecePixmaps[found]
            del self.pieceRects[found]
            self.probabilityObj.removecard(self.card_location, pixmap.card_value)

            # for poker: replace with cards values
            if location == QtCore.QPoint(square.x() / 48, square.y() / 64):
                self.inPlace -= 1

            self.update(square)

            itemData = QtCore.QByteArray()
            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)

            dataStream << pixmap << location

            mimeData = QtCore.QMimeData()
            mimeData.setData('image/x-puzzle-piece', itemData)

            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(event.pos() - square.topLeft())
            drag.setPixmap(pixmap)

            if drag.start(QtCore.Qt.MoveAction) == 0:
                self.pieceLocations.insert(found, location)
                self.piecePixmaps.insert(found, pixmap)
                self.pieceRects.insert(found, square)
                self.update(self.targetSquare(event.pos()))

                # identify card here with new code
                if location == QtCore.QPoint(square.x() / 48, square.y() / 64):
                    self.inPlace += 1

    def paintEvent(self, event):
        """Draws red background behind the future card placement."""
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QtCore.Qt.white)
        # print(self.highlightedRect)

        if self.highlightedRect.isValid():
            painter.setBrush(QtGui.QColor("#ffcccc"))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRect(self.highlightedRect.adjusted(0, 0, -1, -1))

        for i, pieceRect in enumerate(self.pieceRects):
            painter.drawPixmap(pieceRect, self.piecePixmaps[i])

        painter.end()

    def targetSquare(self, position):
        """creates dropping grid of individual card cell"""
        return QtCore.QRect(position.x() // 44 * 44, position.y() // 64 * 64, 44, 64)

    def getPixmapCard(self, pixmap, location):
        """ adds the card value to the pixmap"""
        pixmap.card_value = location.x() + location.y() * 13
        return pixmap


# need to add remove card functionalities
class HandProbabilities:
    def __init__(self):
        self.user_input_cards = [0] * 25
        self.deck = Deck(pixmap=True)  # consider making cards a global variable
        self.cards = self.deck.current_cards
        self.hand_probs = []
        self.seat_numbers = []
        self.error_msg = ' '
        self.main_window = None

    def updateTable(self, seat_num, card, main_window):
        self.main_window = main_window
        card += 1
        if seat_num == 10:
            seat_num = 20
            for x in range(5):
                if self.user_input_cards[seat_num + x] == 0:
                    self.user_input_cards[seat_num + x] = card
                    break
        elif self.user_input_cards[seat_num*2] == 0:
            self.user_input_cards[seat_num*2] = card
        elif self.user_input_cards[seat_num*2+1] == 0:
            self.user_input_cards[seat_num*2+1] = card
        self.import_data()
        if self.fail_error_check():
            self.main_window.ErrorMsg.setText(self.error_msg)
            return
        self.debug.run_tests()
        self.set_probabilities()

    def removecard(self, seat_num, card):
        if seat_num < 10:
            print("Seat number:", seat_num + 1)
        else:
            print("Community Card")
        print(card)

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
            self.error_msg = "Must have at least 3 community cards..."
            return True
        return False

    def import_data(self):

        # reset data
        self.debug = Debug()
        self.debug.preflop_cards = []
        self.debug.community_cards = []
        self.seat_numbers = []

        # loops through all cards selected in cardwidgets
        for x in range(0, 10):
            # must contain 2 cards for player hands: [2*x] and [2*x + 1]
            if self.user_input_cards[2*x] != 0 and self.user_input_cards[2*x + 1] != 0:
                self.debug.preflop_cards.append([self.cards[self.user_input_cards[2*x] - 1],
                                                self.cards[self.user_input_cards[2*x + 1] - 1]])  # insert cards
                self.seat_numbers.append(x)

        for y in range(20, 23):  # loop all flop cards
            if self.user_input_cards[y] != 0:
                self.debug.community_cards.append(self.cards[self.user_input_cards[y] - 1])

        for y in range(23, 25):  # loop remaining community cards
            if self.user_input_cards[y] != 0:
                self.debug.community_cards.append(self.cards[self.user_input_cards[y] - 1])
        # print(self.debug.community_cards)
        # print(self.debug.preflop_cards)

    def listify_probabilities(self):
        for hp in self.main_window.all_hand_probs:
            self.hand_probs.append(hp)

    def clear_text(self):
        for hp in self.hand_probs:
            hp.setText(' ')
        self.main_window.ErrorMsg.setText(' ')


class PixMapCard(QtGui.QPixmap):
    def __init__(self, parent=None):
        super(PixMapCard, self).__init__(parent)
        self.card_value = None


class PokerCards(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(PokerCards, self).__init__(parent)
        self.locations = []
        self.pixmaps = []
        self.qmodel_index = QtCore.QModelIndex()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        # print(role)
        if not index.isValid():
            return None

        if role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon(self.pixmaps[index.row()].scaled(
                    60, 60, QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation))

        if role == QtCore.Qt.UserRole:
            # print(self.pixmaps[index.row()].card_value)
            return self.pixmaps[index.row()]

        if role == QtCore.Qt.UserRole + 1:
            #print(self.locations[index.row()])
            return self.locations[index.row()]

        return None

    def flags(self, index):
        """http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#ItemFlag-enum"""
        if index.isValid():
            return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable |
                    QtCore.Qt.ItemIsDragEnabled)
            # return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable |
            #         QtCore.Qt.ItemIsDragEnabled)
        return QtCore.Qt.NoItemFlags
        #return QtCore.Qt.ItemIsDropEnabled

    def removeRows(self, row, count, parent):
        if parent.isValid():
            return False

        if row >= len(self.pixmaps) or row + count <= 0:
            return False

        beginRow = max(0, row)
        endRow = min(row + count - 1, len(self.pixmaps) - 1)

        self.beginRemoveRows(parent, beginRow, endRow)

        del self.pixmaps[beginRow:endRow + 1]
        del self.locations[beginRow:endRow + 1]

        self.endRemoveRows()
        return True

    def mimeTypes(self):
        return ['image/x-puzzle-piece']

    def mimeData(self, indexes):
        mimeData = QtCore.QMimeData()
        encodedData = QtCore.QByteArray()

        stream = QtCore.QDataStream(encodedData, QtCore.QIODevice.WriteOnly)

        for index in indexes:
            if index.isValid():
                pixmap = PixMapCard(self.data(index, QtCore.Qt.UserRole))
                location = self.data(index, QtCore.Qt.UserRole + 1)
                stream << pixmap << location

        mimeData.setData('image/x-puzzle-piece', encodedData)
        return mimeData

    def dropMimeData(self, data, action, row, column, parent):
        if not data.hasFormat('image/x-puzzle-piece'):
            return False

        if action == QtCore.Qt.IgnoreAction:
            return True

        if column > 0:
            return False

        if not parent.isValid():
            if row < 0:
                endRow = len(self.pixmaps)
            else:
                endRow = min(row, len(self.pixmaps))
        else:
            endRow = parent.row()

        encodedData = data.data('image/x-puzzle-piece')
        stream = QtCore.QDataStream(encodedData, QtCore.QIODevice.ReadOnly)

        while not stream.atEnd():
            pixmap = PixMapCard()
            location = QtGui.QPoint()
            stream >> pixmap >> location

            self.beginInsertRows(QtCore.QModelIndex(), endRow, endRow)
            self.pixmaps.insert(endRow, pixmap)
            self.locations.insert(endRow, location)
            self.endInsertRows()

            endRow += 1

        return True

    def rowCount(self, parent):
        # print(parent)
        if parent.isValid():
            return 0
        else:
            return len(self.pixmaps)

    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction

    def addCards(self, pixmap):
        # print(isinstance(self, QtCore.QAbstractListModel))
        self.beginRemoveRows(QtCore.QModelIndex(), 0, 51)
        self.pixmaps = []
        self.locations = []
        self.endRemoveRows()

        # creates 52 cards that can be selected on the left
        for y in range(4):
            for x in range(13):
                cardImage = pixmap.copy(x*(44+7.75), y*(64+8.34), 44, 64)
                self.addCard(cardImage, QtCore.QPoint(x, y))
                # cardImage.card_value = self.cards[x+y*13]  # used to create card assignments
                # cardImage.row_number = x+y*13  # assign row location
                # print(cardImage.card_value)

    def addCard(self, pixmap, location):
        row = len(self.pixmaps)
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.pixmaps.insert(row, pixmap)
        self.locations.insert(row, location)
        self.endInsertRows()


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # bug : QObject::startTimer: QTimer can only be used with threads started with QThread
        # solved with setAttribute:
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        # main window sizing
        self.resize(1125, 475)
        self.setMinimumSize(QtCore.QSize(1125, 475))
        self.setMaximumSize(QtCore.QSize(1125, 475))

        # initializer function calls
        self.deckImage = PixMapCard()
        self.setupMenus()
        self.setupWidgets()

        # window properties
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                QtGui.QSizePolicy.Fixed))
        self.setWindowTitle("Poker Hand Solver")

    def openImage(self, path=None):
        if not path:
            path = QtGui.QFileDialog.getOpenFileName(self, "Open Image", '',
                    "Image Files (*.png *.jpg *.bmp)")

        if path:
            newImage = PixMapCard()
            if not newImage.load(path):
                QtGui.QMessageBox.warning(self, "Open Image",
                        "The image file could not be loaded.",
                        QtGui.QMessageBox.Cancel)
                return

            self.deckImage = newImage
            self.setupPuzzle()

    def setCompleted(self):
        QtGui.QMessageBox.information(self, "Puzzle Completed",
                "Congratulations! You have completed the puzzle!\nClick OK "
                "to start again.",
                QtGui.QMessageBox.Ok)

        self.setupPuzzle()

    def setupPuzzle(self):
        self.model.addCards(self.deckImage)
        # print([pm.card_value for pm in self.model.pixmaps])
        for hands in self.all_hands:
            hands.clear()
        self.clearLabels()

    def setupMenus(self):
        fileMenu = self.menuBar().addMenu("&File")

        openAction = fileMenu.addAction("&Open...")
        openAction.setShortcut("Ctrl+O")

        exitAction = fileMenu.addAction("E&xit")
        exitAction.setShortcut("Ctrl+Q")

        gameMenu = self.menuBar().addMenu("&Game")

        restartAction = gameMenu.addAction("&Restart")

        openAction.triggered.connect(self.openImage)
        exitAction.triggered.connect(QtGui.qApp.quit)
        restartAction.triggered.connect(self.setupPuzzle)

    def setupWidgets(self):
        # required initializer for all frames
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        # two main containers, one for cards and the other for the table
        frame = QtGui.QFrame(self.centralwidget)
        frameLayout = QtGui.QHBoxLayout(frame)
        frame.setGeometry(QtCore.QRect(5, 0, 300, 450))
        frame2 = QtGui.QFrame(self.centralwidget)
        frame2.setGeometry(QtCore.QRect(310, 0, 800, 450))
        frame2.setStyleSheet("background-image: url('C:/Users/Administrator.abodearchitectu/PycharmProjects/Poker/"
                             "PokerUserInterface/NewUI/PokerTable.png'); background-attachment: fixed")

        # creates pyqt list view and model object that stores card values (and Qpoint)
        self.setCardLists()
        self.model = PokerCards()
        self.cardsList.setModel(self.model)
        frameLayout.addWidget(self.cardsList)

        # initialize settings for hands and labels
        self.probabilities = HandProbabilities()
        self.setupHandsWidgets(frame2)
        self.setupLabels(frame2)
        self.setupErrorMsg(frame2)

        # required initializer for frames
        self.setCentralWidget(self.centralwidget)

    def setCardLists(self):
        # creates pyqt list object that will contain card models
        self.cardsList = QtGui.QListView()
        self.cardsList.setDragEnabled(True)
        self.cardsList.setViewMode(QtGui.QListView.IconMode)
        self.cardsList.setIconSize(QtCore.QSize(44, 64))
        self.cardsList.setGridSize(QtCore.QSize(43, 64))
        self.cardsList.setSpacing(10)
        self.cardsList.setMovement(QtGui.QListView.Snap)
        self.cardsList.setAcceptDrops(True)
        self.cardsList.setDropIndicatorShown(True)

    def setupHandsWidgets(self, frame):
        # initializes 10 hands into a list
        self.all_hands = []
        for x in range(10):
            handsWidget = PokerHands(x, self, parent=frame, probability_obj=self.probabilities)
            handsWidget.solvePokerHands.connect(self.setCompleted,
                                                     QtCore.Qt.QueuedConnection)
            self.all_hands.append(handsWidget)
        handsWidget = PokerHands(10, self, parent=frame, probability_obj=self.probabilities)
        handsWidget.solvePokerHands.connect(self.setCompleted,
                                                 QtCore.Qt.QueuedConnection)
        self.all_hands.append(handsWidget)

        # positions the hands around the poker table
        self.all_hands[0].setGeometry(QtCore.QRect(350, 30, 88, 64))
        self.all_hands[1].setGeometry(QtCore.QRect(500, 50, 88, 64))
        self.all_hands[2].setGeometry(QtCore.QRect(625, 115, 88, 64))
        self.all_hands[3].setGeometry(QtCore.QRect(625, 260, 88, 64))
        self.all_hands[4].setGeometry(QtCore.QRect(500, 330, 88, 64))
        self.all_hands[5].setGeometry(QtCore.QRect(350, 350, 88, 64))
        self.all_hands[6].setGeometry(QtCore.QRect(200, 330, 88, 64))
        self.all_hands[7].setGeometry(QtCore.QRect(80, 260, 88, 64))
        self.all_hands[8].setGeometry(QtCore.QRect(80, 115, 88, 64))
        self.all_hands[9].setGeometry(QtCore.QRect(200, 50, 88, 64))
        self.all_hands[10].setGeometry(QtCore.QRect(290, 187.5, 220, 64))

        # print(self.all_hands)

    def setupErrorMsg(self, frame):
        # error msg instantiation
        self.ErrorMsg = QtGui.QTextBrowser(frame)
        self.ErrorMsg.setGeometry(QtCore.QRect(290, 260, 220, 25))
        self.ErrorMsg.setStyleSheet('color: white')
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ErrorMsg.sizePolicy().hasHeightForWidth())
        self.ErrorMsg.setSizePolicy(sizePolicy)
        self.ErrorMsg.setObjectName(_fromUtf8("ErrorMsg"))
        self.ErrorMsg.setText(_translate("MainWindow", " ", None))

    def setupLabels(self, frame):
        self.all_hand_probs = []
        for x in range(10):
            self.hand_prob = QtGui.QLabel(frame)
            font = QtGui.QFont()
            font.setPointSize(12)
            self.hand_prob.setFont(font)
            self.hand_prob.setStyleSheet('color: white')
            self.hand_prob.setAlignment(QtCore.Qt.AlignCenter)
            self.hand_prob.setObjectName(_fromUtf8("hand_prob_" + str(x)))
            self.hand_prob.setText(_translate("MainWindow", " ", None))
            self.all_hand_probs.append(self.hand_prob)

        self.all_hand_probs[0].setGeometry(QtCore.QRect(350, 100, 88, 20))
        self.all_hand_probs[1].setGeometry(QtCore.QRect(500, 120, 88, 20))
        self.all_hand_probs[2].setGeometry(QtCore.QRect(625, 185, 88, 20))
        self.all_hand_probs[3].setGeometry(QtCore.QRect(625, 235, 88, 20))
        self.all_hand_probs[4].setGeometry(QtCore.QRect(500, 305, 88, 20))
        self.all_hand_probs[5].setGeometry(QtCore.QRect(350, 325, 88, 20))
        self.all_hand_probs[6].setGeometry(QtCore.QRect(200, 305, 88, 20))
        self.all_hand_probs[7].setGeometry(QtCore.QRect(80, 235, 88, 20))
        self.all_hand_probs[8].setGeometry(QtCore.QRect(80, 185, 88, 20))
        self.all_hand_probs[9].setGeometry(QtCore.QRect(200, 120, 88, 20))

    def clearLabels(self):
        for hp in self.all_hand_probs:
            # print(hp)
            hp.setText(_translate("MainWindow", " ", None))
        self.ErrorMsg.setText(_translate("MainWindow", " ", None))


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    # window.openImage('c:/Users/rmulcahey/PycharmProjects/puzzle/example.png')
    window.openImage('C:/Users/Administrator.abodearchitectu/PycharmProjects/Poker/PokerUserInterface/NewUI/cards.png')
    window.show()
    sys.exit(app.exec_())
