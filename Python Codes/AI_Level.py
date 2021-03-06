# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AI_Level.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LevelWindow(object):
    """
    Class allowing, through a window, to manage the depth of IA search
    and therefore its level
    """

    def __init__(self, MainWindow, playWindowAssoc):
        """
        Init method
        Inputs :
            MainWindow : QMainWindow on which the features will appear
            playWindowAssoc : Ui_PlayWindow object in which the depth of search will change
        Goal :
            Implementing framework
        """
        # ---------------| Fields |---------------#
        self.MainWindow = MainWindow
        self.playWindow = playWindowAssoc

        # ---------------| Window |---------------#
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(512, 200)
        self.MainWindow.setStyleSheet(
            "background-color : rgb(255,255,222);border : 2px solid rgb(180,0,0);"
        )
        self.MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        # -----------------| Font |-----------------#
        self.font = QtGui.QFont()
        self.font.setFamily("Rockwell")
        self.font.setPointSize(11)

        # ------------| CentralWidget |------------#
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ------------ | Grid Layout | ------------  #
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # ------------| Message Label |------------#
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setFont(self.font)
        self.label.setStyleSheet("border-color : rgb(120,0,0); border-width : 1px;")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        # -----------| Message Label 2 |-----------#
        self.dangerMess = QtWidgets.QLabel(self.centralwidget)
        self.dangerMess.setObjectName("label")
        self.dangerMess.setFont(self.font)
        self.dangerMess.setAlignment(QtCore.Qt.AlignCenter)
        self.dangerMess.setStyleSheet("border-width : 0px;")
        self.dangerMess.setFixedHeight(25)
        self.gridLayout.addWidget(self.dangerMess, 2, 0, 1, 5)

        # ------------| Horizontal Slicer | ------------#
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(6)
        self.horizontalSlider.setProperty("value", self.playWindow.difficultyAI)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setStyleSheet("border-width : 0px;")
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.valueChanged.connect(self.valueChange)
        self.gridLayout.addWidget(self.horizontalSlider, 0, 2, 1, 3)

        # ------------| Validate Button | ------------#
        self.validateButton = QtWidgets.QPushButton(self.centralwidget)
        self.validateButton.setObjectName("validateButton")
        self.validateButton.setFixedSize(QtCore.QSize(55, 55))
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("Images_IG/PlayIcon.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.validateButton.setIcon(icon)
        self.validateButton.setIconSize(QtCore.QSize(55, 55))
        self.validateButton.setStyleSheet("border-width : 0px;")
        self.validateButton.clicked.connect(self.validateAction)
        self.gridLayout.addWidget(self.validateButton, 1, 2, 1, 1)

        # -----------------| Layout Constraint |-----------------#
        self.gridLayout.setRowStretch(0, 5)
        self.gridLayout.setRowStretch(1, 5)
        self.gridLayout.setRowStretch(2, 1)

        # ------------| Window arrangement | ------------#
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Method to retranscript names and labels' text
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", " Please choose AI level : "))
        self.dangerMess.setText(
            _translate(
                "MainWindow", " Remind that the higher the level, the longer it takes "
            )
        )
        self.validateButton.setText(_translate("MainWindow", ""))

    def valueChange(self):
        """
        Method linked to the change of QHorizontalSlicer change of value.
        Goal :
            Changes self.playWindowAssoc depth of AI search
        """
        self.playWindow.difficultyAI = self.horizontalSlider.value()

    def validateAction(self):
        """
        Method to close the level window
        """
        self.MainWindow.close()


if __name__ == "__main__":
    import sys
    from Initial_Window import Ui_MainWindow as IwM
    from Play_Window import Game

    app = QtWidgets.QApplication(sys.argv)
    Iw = IwM()
    Iw.setupUi(QtWidgets.QMainWindow())
    g = Game(False, Iw, "Balafre", colorAI=2)
    g.show()
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_LevelWindow(MainWindow, g.playWin)
    ui.MainWindow.show()
    sys.exit(app.exec_())

    # sys.exit(app.exec_())
