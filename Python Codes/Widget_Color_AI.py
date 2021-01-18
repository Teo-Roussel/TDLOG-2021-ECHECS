
## Imports

from PyQt5 import QtCore, QtGui, QtWidgets
import Play_Window as PlW

## Class

class Window_Choice(object):
    """
    Crucial class launched in order to choose names or color of IA
    """

    def __init__(self, PVP, MainWindowAssoc, Initial_WindowAssoc, FEN=None):
        """
        Init method
        Inputs:
            PVP : bool. If true then will open a PVP PlayWindow
            MainWindowAssoc : Ui_PlayWindow Object. Will be the one opened
            Initial_WindowAssoc : Ui_MainWindow Object. Will be closed
        Kwargs:
            FEN : str, FEN mode. None by default. If not, will open the FEN in
            the associated Ui_PlayWindow
        """
        self.PVP = PVP
        self.FEN = FEN
        self.IwAssoc = Initial_WindowAssoc
        self.WindowAssoc = MainWindowAssoc
        self.WindowAssoc.setStyleSheet(
            "background-color : rgb(255,255,222);border : 2px solid rgb(180,0,0);"
        )
        self.WindowAssoc.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.WindowAssoc.resize(QtCore.QSize(800, 200))

        # -----------------| Font |-----------------#
        self.font = QtGui.QFont()
        self.font.setFamily("Rockwell")
        self.font.setPointSize(11)

        # -----------------| Central widget |-----------------#
        self.centralWidget = QtWidgets.QWidget(self.WindowAssoc)
        self.centralWidget.setObjectName("centralwidget")

        # -----------------| Layout |-----------------#
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")

        # -----------------| Name of player 1 |-----------------#
        self.nameText = QtWidgets.QLabel(self.centralWidget)
        self.nameText.setFont(self.font)
        self.nameTextText = f"Enter {'name of White player' if self.PVP else 'your name'} (max : 12 caracters) :"
        self.nameText.setObjectName("nameText")
        self.nameText.setStyleSheet(
            "border-color : rgb(80,0,0);\n border-width : 2px; \n border-style : inset;"
        )
        self.gridLayout.addWidget(self.nameText, 0, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFont(self.font)
        self.gridLayout.addWidget(self.lineEdit, 0, 2, 1, 1)

        # -----------------| Choosing color to play (AI mode only) |-----------------#
        if not self.PVP:
            self.colorText = QtWidgets.QLabel(self.centralWidget)
            self.colorText.setObjectName("colorText")
            self.colorText.setFont(self.font)
            self.colorText.setStyleSheet(
                "border-color : rgb(80,0,0);\n border-width : 2px; \n border-style : inset;"
            )
            self.gridLayout.addWidget(self.colorText, 1, 1, 1, 1)
            self.nameChoiceBox = QtWidgets.QComboBox(self.centralWidget)
            self.nameChoiceBox.setFont(self.font)
            self.nameChoiceBox.setObjectName("nameChoiceBox")
            self.nameChoiceBox.addItem("")
            self.nameChoiceBox.addItem("")
            self.gridLayout.addWidget(self.nameChoiceBox, 1, 2, 1, 1)

        # -----------------| Name of Player 2 (only PVP mode) |-----------------#
        if self.PVP:
            self.nameText2 = QtWidgets.QLabel(self.centralWidget)
            self.nameText2.setFont(self.font)
            self.nameTextText2 = "Enter name of Black player (max : 12 caracters) :"
            self.nameText2.setObjectName("nameText2")
            self.nameText2.setStyleSheet(
                "border-color : rgb(80,0,0);\n border-width : 2px; \n border-style : inset;"
            )
            self.gridLayout.addWidget(self.nameText2, 1, 1, 1, 1)
            self.lineEdit2 = QtWidgets.QLineEdit(self.centralWidget)
            self.lineEdit2.setObjectName("lineEdit2")
            self.lineEdit2.setFont(self.font)
            self.gridLayout.addWidget(self.lineEdit2, 1, 2, 1, 1)

        # -----------------| Validation Button |-----------------#
        self.ValidateButton = QtWidgets.QPushButton(self.centralWidget)
        self.ValidateButton.setFixedSize(QtCore.QSize(30, 30))
        self.ValidateButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("Images_IG/bouton_valider.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.ValidateButton.setIcon(icon)
        self.ValidateButton.setIconSize(QtCore.QSize(26, 26))
        self.ValidateButton.setObjectName("ValidateButton")
        self.ValidateButton.clicked.connect(self.openPlayWindow)
        self.gridLayout.addWidget(self.ValidateButton, 2, 3, 1, 1)

        # -----------------| Close Button |-----------------#
        self.CloseButton = QtWidgets.QPushButton(self.centralWidget)
        self.CloseButton.setFixedSize(QtCore.QSize(30, 30))
        self.CloseButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("Images_IG/CloseIcon.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.CloseButton.setIcon(icon)
        self.CloseButton.setIconSize(QtCore.QSize(26, 26))
        self.CloseButton.setObjectName("ValidateButton")
        self.CloseButton.clicked.connect(self.WindowAssoc.close)
        self.CloseButton.setStyleSheet("background-color : rgb(195,0,0);")
        self.gridLayout.addWidget(self.CloseButton, 2, 0, 1, 1)

        # -----------------| Open a game |-----------------#
        self.openGameButton = QtWidgets.QPushButton(self.centralWidget)
        self.openGameButton.setText("Open a pre-existing game")
        self.openGameButton.setObjectName("openGameButton")
        self.openGameButton.setMinimumSize(QtCore.QSize(0, 30))
        self.openGameButton.setStyleSheet(
            "background-color : rgb(120,0,0); color : rgb(195,195,195)"
        )
        self.openGameButton.setFont(self.font)
        self.openGameButton.clicked.connect(self.open_Game)
        self.gridLayout.addWidget(self.openGameButton, 2, 1, 1, 1)

        # -----------------| Manage Files |-----------------#
        self.handleFileButton = QtWidgets.QPushButton(self.centralWidget)
        self.handleFileButton.setText("Manage your game files")
        self.handleFileButton.setObjectName("handleFileButton")
        self.handleFileButton.setMinimumSize(QtCore.QSize(0, 30))
        self.handleFileButton.setStyleSheet(
            "background-color : rgb(120,0,0); color : rgb(195,195,195)"
        )
        self.handleFileButton.setFont(self.font)
        self.handleFileButton.clicked.connect(self.handle_File)
        self.gridLayout.addWidget(self.handleFileButton, 2, 2, 1, 1)

        # -----------------| Layout Constraint |-----------------#
        self.gridLayout.setRowStretch(0, 5)
        self.gridLayout.setRowStretch(1, 5)
        self.gridLayout.setRowStretch(2, 4)
        self.WindowAssoc.setCentralWidget(self.centralWidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.centralWidget)

    def retranslateUi(self):
        """
        Method to retranscript names of Window and labels, etc
        """
        _translate = QtCore.QCoreApplication.translate
        self.nameText.setText(_translate("Form", self.nameTextText))
        if not self.PVP:
            self.colorText.setText(
                _translate("Form", "Which color do you want to play ?")
            )
            self.nameChoiceBox.setItemText(0, _translate("Form", "White"))
            self.nameChoiceBox.setItemText(1, _translate("Form", "Black"))
        else:
            self.nameText2.setText(_translate("Form", self.nameTextText2))

    def openPlayWindow(self):
        """
        Method allowing the oppening of the associated Ui_PlayWindow
        """
        if self.PVP:
            cont = True
            self.nameW = self.lineEdit.text()
            self.nameB = self.lineEdit2.text()
            if len(self.nameW) > 12 or self.nameW == "":
                self.lineEdit.clear()
                cont = False
            if len(self.nameB) > 12 or self.nameB == "":
                self.lineEdit2.clear()
                cont = False
            if cont:
                self.open_PlayWindowPVP()
        else:
            self.namePlayer = self.lineEdit.text()
            if len(self.namePlayer) > 12 or self.namePlayer == "":
                self.lineEdit.clear()
            else:
                colorAIName = self.nameChoiceBox.currentText()
                self.colorAI = 2 if colorAIName == "Black" else 1
                self.open_playwindowAI()
        return None

    def open_Game(self):
        """
        Subsidiary method of Window_Choice.openePlayWindow. Never call that one
        outside of the aformementionned one please. It is used to check
        wether or not the fields are correct and manage the openning and
        closing of windows
        """
        self.PW = PlW.Game(self.PVP, self.IwAssoc, "", "", 1, FEN=None)
        MainWindow = QtWidgets.QMainWindow()
        self.WindowOpen = PlW.ErW.Ui_SaveWindow(
            MainWindow,
            self.PVP,
            InitialWindowAssoc=self.IwAssoc,
            playWindowAssoc=self.PW.playWin,
        )
        self.WindowOpen.getNames()
        if self.WindowOpen.existingFiles.toPlainText().split(":")[1] != " ":
            self.WindowOpen.WindowSave.show()
            self.WindowAssoc.close()
        else:
            self.WindowOpen.WindowSave.close()
            self.openGameButton.setText("No existing Game")
            self.openGameButton.setEnabled(False)

    def handle_File(self):
        """
        Method allowing to oppend the window that allows to manage saved games
        """
        MainWindow = QtWidgets.QMainWindow()
        self.WindowHandle = PlW.HdF.Ui_MainWindow(
            MainWindow, self.PVP, InitialWindowAssoc=self.IwAssoc, playWindowAssoc=None
        )
        self.WindowHandle.WindowHandle.show()

    def open_PlayWindowPVP(self):
        """
        Subsidiary function of openPlayWindow meant for PVP modes
        """
        self.PW = PlW.Game(
            True, self.IwAssoc, self.nameW, nameP2=self.nameB, FEN=self.FEN
        )
        self.IwAssoc.MainWindow.close()
        self.WindowAssoc.close()
        self.PW.show()

    def open_playwindowAI(self):
        """
        Subsidiary function of openPlayWindow meant for AI vs Player modes
        """
        self.PW = PlW.Game(
            False, self.IwAssoc, self.namePlayer, colorAI=self.colorAI, FEN=self.FEN
        )
        self.IwAssoc.MainWindow.close()
        self.WindowAssoc.close()
        self.PW.show()


if __name__ == "__main__":
    import sys
    from Initial_Window import Ui_MainWindow

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow2 = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui2 = Window_Choice(False, MainWindow2, ui)
    ui.MainWindow.show()
    ui2.WindowAssoc.show()
    sys.exit(app.exec_())
