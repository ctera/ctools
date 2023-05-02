# ctools.py

"""CTools is a GUI toolset to interact with your CTERA Environment"""

import sys

from run_cmd import run_cmd
from functools import partial
from login import global_admin_login

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
    QHBoxLayout,
    QTextEdit
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
        self.output = QTextEdit()
        self.output.setFixedHeight(OUTPUT_HEIGHT)
        self.output.setReadOnly(True)
        self.generalLayout.addWidget(self.output)
        
    def _updateOutput(self):
        current = self.output.toPlainText()
        result = str(current) + 'Clicked\n'
        self.output.setText(str(result))


class CTools:
    """CTools controller class"""
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _runCmd(self):
        address = self._view.addressField
        username = self._view.usernameField
        password = self._view.passwordField
        command = self._view.commandField

        global_admin = global_admin_login(str(address), str(username), str(password))

        result = self._evaluate(global_admin, command)
        #self._view._updateOutput()
        print(result)
    
    def _test(self):
        print("testing")

    def _connectSignalsAndSlots(self):
        #self._view.start.clicked.connect(self._view._updateOutput)
        #self._view.cancel.clicked.connect(lambda: print("Cancel"))
        self._view.start.clicked.connect(self._runCmd)
        #self._view.start.clicked.connect(self._test)

def model(address, username, password, command):
    run_cmd(address, username, password, command)
    return "HI"

def main():
    """PyCalc's main function."""
    ctoolsApp = QApplication(sys.argv)
    ctoolsWindow = CToolsWindow()
    ctoolsWindow.show()
    controller = CTools(model=model, view=ctoolsWindow)
    ctoolsApp.exec_()

if __name__ == "__main__":
    main()