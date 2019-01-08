import sys
from PyQt4 import QtCore, QtGui



class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(443, 340)
        self.Tilte = QtGui.QLabel(Form)
        self.Tilte.setGeometry(QtCore.QRect(130, 10, 131, 16))
        self.Tilte.setObjectName(_fromUtf8("Tilte"))
        self.Vo = QtGui.QDoubleSpinBox(Form)
        self.Vo.setGeometry(QtCore.QRect(20, 40, 81, 22))
        self.Vo.setMaximum(999999999.0)
        self.Vo.setObjectName(_fromUtf8("Vo"))
        self.angle = QtGui.QDoubleSpinBox(Form)
        self.angle.setGeometry(QtCore.QRect(20, 70, 81, 22))
        self.angle.setMaximum(90.0)
        self.angle.setObjectName(_fromUtf8("angle"))
        self.dt = QtGui.QDoubleSpinBox(Form)
        self.dt.setGeometry(QtCore.QRect(20, 100, 81, 22))
        self.dt.setDecimals(3)
        self.dt.setMinimum(0.0)
        self.dt.setMaximum(1.0)
        self.dt.setSingleStep(0.001)
        self.dt.setProperty("value", 0.01)
        self.dt.setObjectName(_fromUtf8("dt"))
        self.Jupiter = QtGui.QRadioButton(Form)
        self.Jupiter.setGeometry(QtCore.QRect(20, 240, 82, 17))
        self.Jupiter.setObjectName(_fromUtf8("Jupiter"))
        self.Saturn = QtGui.QRadioButton(Form)
        self.Saturn.setGeometry(QtCore.QRect(20, 260, 82, 17))
        self.Saturn.setObjectName(_fromUtf8("Saturn"))
        self.Sun = QtGui.QRadioButton(Form)
        self.Sun.setGeometry(QtCore.QRect(20, 140, 82, 17))
        self.Sun.setCheckable(True)
        self.Sun.setObjectName(_fromUtf8("Sun"))
        self.Venus = QtGui.QRadioButton(Form)
        self.Venus.setGeometry(QtCore.QRect(20, 180, 82, 17))
        self.Venus.setObjectName(_fromUtf8("Venus"))
        self.Mars = QtGui.QRadioButton(Form)
        self.Mars.setGeometry(QtCore.QRect(20, 220, 82, 17))
        self.Mars.setObjectName(_fromUtf8("Mars"))
        self.Neptune = QtGui.QRadioButton(Form)
        self.Neptune.setGeometry(QtCore.QRect(20, 300, 82, 17))
        self.Neptune.setObjectName(_fromUtf8("Neptune"))
        self.Earth = QtGui.QRadioButton(Form)
        self.Earth.setGeometry(QtCore.QRect(20, 200, 82, 17))
        self.Earth.setObjectName(_fromUtf8("Earth"))
        self.Uranus = QtGui.QRadioButton(Form)
        self.Uranus.setGeometry(QtCore.QRect(20, 280, 82, 17))
        self.Uranus.setObjectName(_fromUtf8("Uranus"))
        self.Mercury = QtGui.QRadioButton(Form)
        self.Mercury.setGeometry(QtCore.QRect(20, 160, 82, 17))
        self.Mercury.setObjectName(_fromUtf8("Mercury"))
        self.Vo_Label = QtGui.QLabel(Form)
        self.Vo_Label.setGeometry(QtCore.QRect(110, 40, 71, 21))
        self.Vo_Label.setObjectName(_fromUtf8("Vo_Label"))
        self.Angle_Label = QtGui.QLabel(Form)
        self.Angle_Label.setGeometry(QtCore.QRect(110, 70, 61, 21))
        self.Angle_Label.setObjectName(_fromUtf8("Angle_Label"))
        self.dt_Label = QtGui.QLabel(Form)
        self.dt_Label.setGeometry(QtCore.QRect(110, 100, 61, 21))
        self.dt_Label.setObjectName(_fromUtf8("dt_Label"))
        self.LCDheight = QtGui.QLCDNumber(Form)
        self.LCDheight.setGeometry(QtCore.QRect(230, 150, 181, 71))
        self.LCDheight.setObjectName(_fromUtf8("LCDheight"))
        self.lcdTotaltime = QtGui.QLCDNumber(Form)
        self.lcdTotaltime.setGeometry(QtCore.QRect(230, 250, 181, 71))
        self.lcdTotaltime.setObjectName(_fromUtf8("lcdTotaltime"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(230, 132, 181, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(230, 232, 181, 21))
        self.label_2.setObjectName(_fromUtf8("hand_prob_2"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(230, 50, 181, 61))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.Tilte.setText(QtGui.QApplication.translate("Form", "Projectile Motion Calculator", None, QtGui.QApplication.UnicodeUTF8))
        self.Jupiter.setText(QtGui.QApplication.translate("Form", "Jupiter", None, QtGui.QApplication.UnicodeUTF8))
        self.Saturn.setText(QtGui.QApplication.translate("Form", "Saturn", None, QtGui.QApplication.UnicodeUTF8))
        self.Sun.setText(QtGui.QApplication.translate("Form", "Sun ", None, QtGui.QApplication.UnicodeUTF8))
        self.Venus.setText(QtGui.QApplication.translate("Form", "Venus", None, QtGui.QApplication.UnicodeUTF8))
        self.Mars.setText(QtGui.QApplication.translate("Form", "Mars", None, QtGui.QApplication.UnicodeUTF8))
        self.Neptune.setText(QtGui.QApplication.translate("Form", "Neptune", None, QtGui.QApplication.UnicodeUTF8))
        self.Earth.setText(QtGui.QApplication.translate("Form", "Earth", None, QtGui.QApplication.UnicodeUTF8))
        self.Uranus.setText(QtGui.QApplication.translate("Form", "Uranus", None, QtGui.QApplication.UnicodeUTF8))
        self.Mercury.setText(QtGui.QApplication.translate("Form", "Mercury", None, QtGui.QApplication.UnicodeUTF8))
        self.Vo_Label.setText(QtGui.QApplication.translate("Form", "Initial Velocity ", None, QtGui.QApplication.UnicodeUTF8))
        self.Angle_Label.setText(QtGui.QApplication.translate("Form", "Angle", None, QtGui.QApplication.UnicodeUTF8))
        self.dt_Label.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Smaller number gives more accurate results.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.dt_Label.setText(QtGui.QApplication.translate("Form", "Time Step", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Max Height ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Total Time ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Calculate", None, QtGui.QApplication.UnicodeUTF8))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
