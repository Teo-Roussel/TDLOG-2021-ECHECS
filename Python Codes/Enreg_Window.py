## Imports
import os
from PyQt5 import QtCore, QtGui, QtWidgets

## Class

class Ui_SaveWindow(object):
    """
    Class allowing to save a game or open one from a FEN. Please never use the
    save possibility if there's no associated playWindow
    """

    def __init__(
        self, MainWindow, PVP, InitialWindowAssoc=None, playWindowAssoc=None, FEN=None
    ):
        """
        Init method
        Inputs :
            MainWindow : QMainWindow on which the class is built
            PVP : Mode in which you are for save function or which you want to open,
            InitialWindowAssoc : Initial_Window.Ui_MainWindow object,
            playWindowAssoc : Ui_PlayWindow object, necessary for the save method
            FEN : str, FEN format. Determines whether you open or save a game
        """

        self.PVP = PVP
        self.FEN = FEN
        self.windowAssoc = playWindowAssoc
        self.IwAssoc = InitialWindowAssoc
        self.WindowSave = MainWindow
        self.WindowSave.setObjectName("self.WindowSave")
        self.WindowSave.setStyleSheet("background-color : rgb(255,255,222)")
        self.WindowSave.resize(600, 500)
        self.WindowSave.setFixedSize(QtCore.QSize(600, 500))
        self.font = QtGui.QFont()
        self.font.setFamily("Rockwell")
        self.font.setPointSize(11)
        self.centralwidget = QtWidgets.QWidget(self.WindowSave)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # ------------------| Label |------------------#
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.textlabel = " Save as :" if FEN != None else " Open : "
        self.label.setStyleSheet(
            "border-color : rgb(80,0,0);\n border-width : 1px; \n border-style : inset;"
        )
        self.label.setFont(self.font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        # -----------------| Line Save |-----------------#
        self.saveEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.saveEdit.setFont(self.font)
        self.saveEdit.setObjectName("saveEdit")
        self.gridLayout.addWidget(self.saveEdit, 0, 1, 1, 1)

        # ------------------| Txt |------------------#
        self.labelTxt = QtWidgets.QLabel(self.centralwidget)
        self.labelTxt.setObjectName("labelTxt")
        self.labelTxt.setFont(self.font)
        self.gridLayout.addWidget(self.labelTxt, 0, 2, 1, 1)

        # ----------------| Button Save |----------------#
        self.useButton = QtWidgets.QPushButton(self.centralwidget)
        self.useButton.setText("")
        self.useButton.setFixedSize(QtCore.QSize(35, 35))
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("Images_IG/bouton_valider.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.useButton.setIcon(icon)
        self.useButton.setIconSize(QtCore.QSize(33, 33))
        self.useButton.setObjectName("useButton")
        if FEN == None:
            self.useButton.clicked.connect(self.OpenMethod)
        else:
            self.useButton.clicked.connect(self.SaveMethod)
        self.gridLayout.addWidget(self.useButton, 0, 3, 1, 1)

        # ----------------| Files names |----------------#
        self.existingFiles = QtWidgets.QTextEdit(self.centralwidget)
        self.getNames()
        self.existingFiles.setFont(self.font)
        self.existingFiles.setObjectName("existingFiles")
        self.existingFiles.setReadOnly(True)
        self.gridLayout.addWidget(self.existingFiles, 1, 0, 1, 4)

        # ----------------| Layout prop |----------------#
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 15)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 20)
        self.WindowSave.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.WindowSave)

    def retranslateUi(self):
        """
        Method that retranscripts the names of windows, labels,...
        """
        _translate = QtCore.QCoreApplication.translate
        self.WindowSave.setWindowTitle(_translate("self.WindowSave", "WindowSave"))
        self.label.setText(_translate("self.WindowSave", self.textlabel))
        self.labelTxt.setText(_translate("self.WindowSave", " .txt "))

    def getNames(self):
        """
        Allows to get names of files of chosen mode (self.PVP) inside the Save Repository
        under the correct format (see SaveMethod)
        """
        ListFiles = os.listdir("Save")
        centering = "                          "
        stringFiles = centering + "List of {} files in your Save folder : \n \n".format(
            "PVP" if self.PVP else "AI"
        )
        if self.PVP:
            for k in ListFiles:
                if self.PVP and "PVP_mode" == k[:8]:
                    realName = k[9:]
                    stringFiles += "   - " + realName + "\n"
        else:
            stringFiles += " Files where AI is playing white : \n"
            for k in ListFiles:
                if "AI_mode" == k[:7] and k[8] == "B":
                    realName = k[8:]
                    stringFiles += "   - " + realName + "\n"
            stringFiles += "\n Files where AI is playing black : \n"
            for k in ListFiles:
                if "AI_mode" == k[:7] and k[8] == "W":
                    realName = k[8:]
                    stringFiles += "   - " + realName + "\n"
        self.existingFiles.setText(stringFiles)

    def SaveMethod(self):
        """
        Method that allows the user to save the current game inside the repository named Save under the following format :
            AI or PVP + -mode- + name 1 + colorIA or name 2 + name chose by user
        """
        stringName = self.saveEdit.text()
        if stringName.strip(" ") != "":
            if self.PVP:
                nameB = self.windowAssoc.textB
                nameW = self.windowAssoc.textW
                totNames = nameW + "_" + nameB + "_"
            else:
                coulIA = "B" if self.windowAssoc.colorIA == 2 else "W"
                namePlayer = (
                    self.windowAssoc.textW
                    if self.windowAssoc.colorIA == 1
                    else self.windowAssoc.textB
                )
            realName = (
                (
                    "Save/AI_mode_{}_{}_".format(coulIA, namePlayer)
                    if not self.PVP
                    else "Save/PVP_mode_{}".format(totNames)
                )
                + stringName
                + ".txt"
            )
            f = open(realName, "w")
            f.writelines(self.FEN)
            f.close()
            self.getNames()
            self.saveEdit.clear()
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("Images_IG/CloseIcon.png"),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off,
            )
            self.useButton.setIcon(icon)
            self.useButton.setIconSize(QtCore.QSize(27, 27))
            self.useButton.setFixedSize(QtCore.QSize(30, 30))
            self.useButton.setStyleSheet("background-color : rgb(185,0,0)")
            self.useButton.clicked.connect(self.CloseMethod)
        return None

    def OpenMethod(self):
        """
        Method that allows the user to a game saved inside the repository named Save of the chose mode (self.PVP)
        """
        stringName = self.saveEdit.text()
        ListFiles = os.listdir("Save")
        realName = (
            ("PVP_mode_" if self.PVP else "AI_mode_")
            + stringName
            + ("" if stringName[-4:] == ".txt" else ".txt")
        )
        if realName in ListFiles:
            f = open("Save/" + realName, "r")
            fen = f.readlines()[0]
            f.close()
            colorIA = 1 if self.PVP else (1 if stringName[0] == "W" else 2)
            self.WindowSave.close()
            MainWindow = QtWidgets.QMainWindow()
            if self.PVP:
                indFinName1 = 9
                while realName[indFinName1] != "_":
                    indFinName1 += 1
                indFinName2 = indFinName1 + 1
                while realName[indFinName2] != "_":
                    indFinName2 += 1
                self.windowAssoc.textW = realName[9:indFinName1]
                self.windowAssoc.textB = realName[indFinName1 + 1 : indFinName2]

            else:
                indFinNamePlayer = 10
                while realName[indFinNamePlayer] != "_":
                    indFinNamePlayer += 1
                self.windowAssoc.textW = (
                    "AI" if stringName[0] == "B" else realName[10:indFinNamePlayer]
                )
                self.windowAssoc.textB = (
                    "AI" if stringName[0] == "W" else realName[10:indFinNamePlayer]
                )

            self.windowAssoc.InitialisationPerFEN(fen, colorIA)
            if self.IwAssoc != None:
                self.IwAssoc.MainWindow.close()
            self.windowAssoc.MainWindow.show()

        else:
            self.textlabel = "Error - " + (
                " Save as :" if self.FEN != None else " Open : "
            )
            self.saveEdit.clear()

    def CloseMethod(self):
        """
        Close the window
        """
        self.WindowSave.close()


if __name__ == "__main__":
    import sys
    from Play_Window import Game
    from Initial_Window import Ui_MainWindow

    app = QtWidgets.QApplication(sys.argv)
    Iw = Ui_MainWindow()
    Iw.setupUi(QtWidgets.QMainWindow())
    g = Game(False, Iw, "Balafre", 1)
    MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_SaveWindow(MainWindow, True,FEN = "rp4PR/np4PN/bp4PB/qp4PQ/kp4PK/bp4PB/np4PN/rp4PR w KQkq - 0 1")
    ui = Ui_SaveWindow(MainWindow, g.playWin.PVP, playWindowAssoc=g.playWin)
    ui.WindowSave.show()
    sys.exit(app.exec_())
