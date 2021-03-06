## Imports
from PyQt5 import QtCore, QtGui, QtWidgets
import os

## Class

class Ui_MainWindow(object):
    """
    Class launched in order to manage existing games
    """

    def __init__(self, MainWindow, PVP, InitialWindowAssoc=None, playWindowAssoc=None):
        """
        Init method
        Inputs :
            MainWindow : QMainwindow object on which our class will be built
            PVP : bool. If True, allows to manage the PVP games else the AI games
        Kwargs:
            InitialWindowAssoc : Initial_Window.Ui_MainWindow object.
            playWindowAssoc : Ui_PlayWindow object

        """
        # ------------------| Initialisation |------------------#
        self.PVP = PVP
        self.playWinAssoc = playWindowAssoc
        self.IwAssoc = InitialWindowAssoc
        self.WindowHandle = MainWindow
        self.WindowHandle.setObjectName("HandleWindow")
        self.WindowHandle.setStyleSheet(
            "background-color : rgb(255,255,222);border : 2px solid rgb(180,0,0);"
        )
        self.WindowHandle.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.WindowHandle.resize(638, 547)
        self.font = QtGui.QFont()
        self.font.setFamily("Rockwell")
        self.font.setPointSize(11)
        self.fontTitle = QtGui.QFont()
        self.fontTitle.setFamily("Rockwell")
        self.fontTitle.setPointSize(11)
        self.fontTitle.setUnderline(True)
        self.palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(220, 220, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

        # ------------------| Central widget |------------------#
        self.centralwidget = QtWidgets.QWidget(self.WindowHandle)
        self.centralwidget.setObjectName("centralwidget")

        # ------------------| GridLayout |------------------#
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # ------------------| Message |------------------#
        self.textMessage = QtWidgets.QLabel(self.centralwidget)
        self.textMessage.setObjectName("textMessage")
        self.textMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.textMessage.setStyleSheet("background-color : rgb(120,0,0)")
        self.textMessage.setFont(self.font)
        self.textMessage.setPalette(self.palette)
        self.textMessage.setMinimumHeight(35)
        self.gridLayout.addWidget(self.textMessage, 0, 0, 1, 2)

        # ------------------| List Widget |------------------#
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setFont(self.font)
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 2)

        # ------------------| Adding Files |------------------#
        self.AddAllItems()

        # ------------------| Delete Button |------------------#
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setFont(self.font)
        self.deleteButton.clicked.connect(self.deleteFiles)
        self.gridLayout.addWidget(self.deleteButton, 2, 1, 1, 1)

        # ------------------| Cancel Button |------------------#
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setFont(self.font)
        self.cancelButton.clicked.connect(self.WindowHandle.close)
        self.gridLayout.addWidget(self.cancelButton, 2, 0, 1, 1)

        # ------------------| Adding to window |------------------#
        self.WindowHandle.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self):
        """
        Method that retranscript the names of the window, labels,...
        """
        _translate = QtCore.QCoreApplication.translate
        self.WindowHandle.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textMessage.setText(
            _translate("MainWindow", "Check every file you want to delete")
        )
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))

    def AddItem(self, text, Checkable=True, indent=False):

        """
        Add a checkable item in the list of files present in your repository
        """

        if Checkable:
            item = QtWidgets.QListWidgetItem()
            item.setText(text)
            item.setFont(self.font)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)
        else:
            item2 = QtWidgets.QListWidgetItem()
            item2.setText(text)
            item2.setFont(self.fontTitle)
            if indent:
                item2.setTextAlignment(QtCore.Qt.AlignCenter)
            self.listWidget.addItem(item2)

    def AddAllItems(self):
        """
        Method that add all the names of your games that correspond to the mode you chose
        """
        ListFiles = os.listdir("Save")
        titleItem = "\n List of {} files in your Save folder : \n ".format(
            "PVP" if self.PVP else "AI"
        )
        self.AddItem(titleItem, False, True)
        if self.PVP:
            for k in ListFiles:
                if self.PVP and "PVP_mode" == k[:8]:
                    realName = k[9:]
                    self.AddItem(realName)
        else:
            subtitle1 = " Files where AI is playing white : \n"
            self.AddItem(subtitle1, False)
            for k in ListFiles:
                if "AI_mode" == k[:7] and k[8] == "B":
                    realName = k[8:]
                    self.AddItem(realName)
            subtitle2 = "\n Files where AI is playing black : \n"
            self.AddItem(subtitle2, False)
            for k in ListFiles:
                if "AI_mode" == k[:7] and k[8] == "W":
                    realName = k[8:]
                    self.AddItem(realName)

    def deleteFiles(self):
        """
        Method that destroy all files that have been checked in the list of files
        """
        toDelete = []
        nbItem = self.listWidget.count()
        for index in range(nbItem):
            if self.listWidget.item(index).checkState() == QtCore.Qt.Checked:
                text = (
                    ("Save/")
                    + ("AI_mode_" if not self.PVP else "PVP_mode_")
                    + self.listWidget.item(index).text()
                )
                toDelete += [text]
        for fileName in toDelete:
            os.remove(fileName)
        if toDelete != []:
            self.WindowHandle.close()
        else:
            self.textMessage.setText(
                "No file selected, please do so or click on cancel to close window"
            )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow, False)
    ui.WindowHandle.show()
    sys.exit(app.exec_())
