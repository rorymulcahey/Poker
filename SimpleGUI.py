import sys
from PyQt4 import QtGui, QtCore


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Poker Hands")
        self.setGeometry(50, 50, 500, 300)

        extractAction = QtGui.QAction("&Test code", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

        self.home()

    def home(self):
        btn = QtGui.QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)
        btn.resize(50, 30)
        btn.move(450, 270)
        self.show()

    def close_application(self):
        sys.exit()

        
def run():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    sys.exit(app.exec())


run()