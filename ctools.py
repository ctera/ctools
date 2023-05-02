# ctools.py

"""CTools is a GUI toolset to interact with your CTERA Environment"""

import sys

from status import run_status
from functools import partial

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
WINDOW_HEIGHT = 800
OUTPUT_HEIGHT = 200

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
        self._createOutput()

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
        self.addressField = QLineEdit()
        self.usernameField = QLineEdit()
        self.passwordField = QLineEdit()
        self.commandField = QLineEdit()

        RunCMDLayout.addWidget(requiredArgs, 0, 0, 1, 2)
        RunCMDLayout.addWidget(address, 1, 0)
        RunCMDLayout.addWidget(username, 1, 1)
        RunCMDLayout.addWidget(self.addressField, 2, 0)
        RunCMDLayout.addWidget(self.usernameField, 2, 1)
        RunCMDLayout.addWidget(password, 3, 0)
        RunCMDLayout.addWidget(filename, 3, 1)
        RunCMDLayout.addWidget(self.passwordField, 4, 0)
        RunCMDLayout.addWidget(self.commandField, 4, 1)

        self.generalLayout.addLayout(RunCMDLayout)

    def _createActionButtons(self):
        actionButtonLayout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.start = QPushButton("Start")

        actionButtonLayout.addWidget(self.cancel)
        actionButtonLayout.addWidget(self.start)

        self.generalLayout.addLayout(actionButtonLayout)

    def _createOutput(self):
        self.output = QLineEdit()
        self.output.setFixedHeight(OUTPUT_HEIGHT)
        self.output.setReadOnly(True)
        self.generalLayout.addWidget(self.output)

class CTools:
    """CTools controller class"""
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _runCmd(self):
        output = run_status(self._view.addressField.text(), self._view.usernameField.text(), self._view.passwordField.text(), self._view.commandField.text())
        

    def _connectSignalsAndSlots(self):
        startButton = self._view.start
        startButton.clicked.connect(self._runCmd)



def main():
    """PyCalc's main function."""
    ctoolsApp = QApplication(sys.argv)
    ctoolsWindow = CToolsWindow()
    ctoolsWindow.show()

    ctoolsApp.exec_()

if __name__ == "__main__":
    main()