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
from contextlib import contextmanager

# sip.setapi('QVariant', 2)
# try:
#     import puzzle_rc3
# except ImportError:
#     import puzzle_rc2


class PokerHands(QtGui.QWidget):

    # SolvePokerHands = QtCore.pyqtSignal()
    solvePokerHands = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(PokerHands, self).__init__(parent)

        self.piecePixmaps = []
        self.pieceRects = []
        self.pieceLocations = []
        self.highlightedRect = QtCore.QRect()
        self.inPlace = 0
        self.deck = Deck(pixmap=True)
        self.cards = self.deck.current_cards
        self.currentHand = []

        # pixel dimensions card placement map
        self.setAcceptDrops(True)
        #self.setMinimumSize(572, 256)
        #self.setMaximumSize(572, 256)
        self.setMinimumSize(88, 64)
        self.setMaximumSize(88, 64)

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
            self.currentHand.append(pixmap.card_value)
            print(pixmap.card_value)

            self.pieceLocations.append(location)
            self.piecePixmaps.append(pixmap)
            self.pieceRects.append(square)

            self.hightlightedRect = QtCore.QRect()
            self.update(square)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

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

                # identify card
                if location == QtCore.QPoint(square.x() / 48, square.y() / 64):
                    self.inPlace += 1

    # draws red background behind the future card placement
    def paintEvent(self, event):
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

    # creates dropping grid of individual card cell
    def targetSquare(self, position):
        return QtCore.QRect(position.x() // 44 * 44, position.y() // 64 * 64, 44, 64)

    # adds the card value to the pixmap
    def getPixmapCard(self, pixmap, location):
        pixmap.card_value = self.cards[location.x() + location.y() * 13]
        return pixmap


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


    # http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#ItemFlag-enum
    def flags(self, index):
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

        self.deckImage = PixMapCard()

        self.setupMenus()
        self.setupWidgets()

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                QtGui.QSizePolicy.Fixed))
        self.setWindowTitle("Puzzle")

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
        frame = QtGui.QFrame()
        frameLayout = QtGui.QHBoxLayout(frame)

        self.piecesList = QtGui.QListView()
        self.piecesList.setDragEnabled(True)
        self.piecesList.setViewMode(QtGui.QListView.IconMode)
        self.piecesList.setIconSize(QtCore.QSize(43, 64))
        self.piecesList.setGridSize(QtCore.QSize(43, 64))
        self.piecesList.setSpacing(10)
        self.piecesList.setMovement(QtGui.QListView.Snap)
        self.piecesList.setAcceptDrops(True)
        self.piecesList.setDropIndicatorShown(True)

        self.model = PokerCards(self)
        self.piecesList.setModel(self.model)
        frameLayout.addWidget(self.piecesList)

        self.all_hands = []
        for x in range(10):
            self.handsWidget = PokerHands()
            self.handsWidget.solvePokerHands.connect(self.setCompleted,
                                                     QtCore.Qt.QueuedConnection)
            frameLayout.addWidget(self.handsWidget)
            self.all_hands.append(self.handsWidget)
        print(self.all_hands)

        self.setCentralWidget(frame)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    # window.openImage('c:/Users/rmulcahey/PycharmProjects/puzzle/example.png')
    window.openImage('C:/Users/Administrator.abodearchitectu/PycharmProjects/Poker/PokerUserInterface/cards.png')
    window.show()
    sys.exit(app.exec_())
