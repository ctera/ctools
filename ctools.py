# ctools.py

"""CTools is a GUI toolset to interact with your CTERA Environment"""

import sys

from run_cmd import run_cmd

from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QToolBar,
    QLabel,
    QHBoxLayout
)

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
class CToolsWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CTools 3.0")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createToolBar()
        self._createRunCMDDisplay()
        self._createActionButtons()

    def _createToolBar(self):
        tools = QToolBar()
        tools.addAction("Run CMD", self.close)
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)
    
    def _createRunCMDDisplay(self):
        RunCMDLayout = QGridLayout()
        requiredArgs = QLabel("<h4><b>Required Arguments:</b></h4>")
        address = QLabel("Address (Portal IP, hostname, or FQDN):")
        username = QLabel("Portal Admin Username:")
        password = QLabel("Password")
        filename = QLabel("Output Filename")
        addressField = QLineEdit()
        usernameField = QLineEdit()
        passwordField = QLineEdit()
        filenameField = QLineEdit()

        RunCMDLayout.addWidget(requiredArgs, 0, 0, 1, 2)
        RunCMDLayout.addWidget(address, 1, 0)
        RunCMDLayout.addWidget(username, 1, 1)
        RunCMDLayout.addWidget(addressField, 2, 0)
        RunCMDLayout.addWidget(usernameField, 2, 1)
        RunCMDLayout.addWidget(password, 3, 0)
        RunCMDLayout.addWidget(filename, 3, 1)
        RunCMDLayout.addWidget(passwordField, 4, 0)
        RunCMDLayout.addWidget(filenameField, 4, 1)

        self.generalLayout.addLayout(RunCMDLayout)

    def _createActionButtons(self):
        actionButtonLayout = QHBoxLayout()
        cancel = QPushButton("Cancel")
        start = QPushButton("Start")

        actionButtonLayout.addWidget(cancel)
        actionButtonLayout.addWidget(start)

        self.generalLayout.addLayout(actionButtonLayout)



def main():
    """PyCalc's main function."""
    ctoolsApp = QApplication(sys.argv)
    ctoolsWindow = CToolsWindow()
    ctoolsWindow.show()

    ctoolsApp.exec_()

if __name__ == "__main__":
    main()