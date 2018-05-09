from math import*
from PyQt4 import QtCore, QtGui
from projectile_ui import Ui_Form

constants = {
    'Sun': (0, 0),
    'Mercury': (0, 0),
    'Venus': (0, 0),
    'Earth': (6.4*10**6, 9.81),
    'Mars': (0, 0),
    'Jupiter': (0, 0),
    'Saturn': (0, 0),
    'Uranus': (0, 0),
    'Neptune': (0, 0),
    }

class MyForm(QtGui.QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.radioButtons = QtGui.QButtonGroup(self)
        self.radioButtons.addButton(self.Sun)
        self.radioButtons.addButton(self.Mercury)
        self.radioButtons.addButton(self.Venus)
        self.radioButtons.addButton(self.Earth)
        self.radioButtons.addButton(self.Mars)
        self.radioButtons.addButton(self.Jupiter)
        self.radioButtons.addButton(self.Saturn)
        self.radioButtons.addButton(self.Uranus)
        self.radioButtons.addButton(self.Neptune)
        self.pushButton.clicked.connect(self.handleCalculate)

    def handleCalculate(self):
        loopiterations = int()

        dt = self.dt.value() # time step

        Vo = self.Vo.value()
        xo = 0
        yo = 0
        angle = self.angle.value()
        angle = angle * (pi / 180)
        Vox = Vo * cos(angle)
        Voy = Vo * sin(angle)
        y =  (yo + Voy * dt)

        iterations = y = r = g = 0

        button = self.radioButtons.checkedButton()

        if button is not None:
            # r= 6.4*10**6 for earth, g= m/s **2
            r, g = constants[str(button.objectName())]

            Vy=Voy - g * dt

            if r > 0 and g > 0:

                while not (Vy < 0):
                    y =  (yo + Voy * dt)
                    Vy= (Voy - g * dt)
                    x = (xo + Vox * dt)
                    Vx = Vox
                    iterations = iterations + 1
                    yo = y
                    xo = x
                    Vox = Vx
                    Voy = Vy

        self.LCDheight.display(y)
        self.lcdTotaltime.display(iterations)

if __name__ == "__main__":

    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())