from PyQt4 import QtCore, QtGui
from Poker_ui import Ui_Form
from SolvePokerHands import *
import __main__

try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str

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


if __name__ == "__main__":

    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())