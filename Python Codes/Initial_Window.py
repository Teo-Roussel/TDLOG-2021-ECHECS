
## Imports
from PyQt5 import QtCore, QtGui, QtWidgets
from Widget_Color_AI import Window_Choice

## Class

class Ui_MainWindow(object):
    def open_playwindowPVP(self):
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Window_Choice(True, MainWindow, self)
        self.ui.WindowAssoc.show()

    def open_playwindowAI(self):
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Window_Choice(False, MainWindow, self)
        self.ui.WindowAssoc.show()

    def setupUi(self, MainWindow):

        self.MainWindow = MainWindow
        iconExe = QtGui.QIcon("Images_IG/IconExe2.ico")
        self.MainWindow.setWindowIcon(iconExe)
        self.MainWindow.setIconSize(QtCore.QSize(10, 5))
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(931, 694)
        self.MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(True)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 40))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(209, 209, 209))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 0, 0))
        self.pushButton.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(85, 0, 0);")
        self.pushButton.setObjectName("pushButton")
        # open window to play
        self.pushButton.clicked.connect(self.open_playwindowPVP)
        self.verticalLayout.addWidget(self.pushButton)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Images_IG/Image_Fenetre_Initiale.jpg"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(85, 0, 0);")
        self.pushButton_2.setObjectName("pushButton_2")
        # open window to play
        self.pushButton_2.clicked.connect(self.open_playwindowAI)

        self.verticalLayout.addWidget(self.pushButton_2)
        self.MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ponts'Chess - Menu window"))
        self.pushButton.setText(_translate("MainWindow", "Player VS Player Mode"))
        self.pushButton_2.setText(_translate("MainWindow", "Player VS AI Mode"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.MainWindow.show()
    sys.exit(app.exec_())
