# ctools.py

"""CTools is a GUI toolset to interact with your CTERA Environment"""

import sys, logging

from run_cmd import run_cmd

from testfuncs import fakeFunc

from functools import partial
from login import global_admin_login

from PySide2.QtCore import Qt

from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QTextEdit,
    QFrame
)

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 450
OUTPUT_HEIGHT = 250


def set_logging(p_level=logging.INFO, log_file="info-log.txt"):
    """
    Set up logging to a given file name.
    Doesn't require CTERASDK_LOG_FILE to be set.

    p_level --  DEBUG, INFO, WARNING, ERROR, Critical. (default INFO)
    log_file -- file name for log file. (default "log.txt")
    """
    logging.root.handlers = []
    logging.basicConfig(
        level=p_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="w"),
            logging.StreamHandler()])

class CToolsWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CTools 3.0")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.generalLayout = QVBoxLayout()
        self.top = QLabel("<h2>Welcome to CTools!</h2>")
        self.mainContent = QHBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self.generalLayout.addWidget(self.top)
        self.generalLayout.addLayout(self.mainContent)
        self._createToolBar()
        self._createToolViewLayout()

    def _createToolBar(self):
        tools = QVBoxLayout()

        label = QLabel("<h4><b>Actions:</b></h4>")
        label.setFixedHeight(50)
        self.run_cmd = QPushButton("Run_CMD")
        self.exit = QPushButton("Exit")

        tools.addWidget(label, alignment=Qt.AlignTop)
        tools.addWidget(self.run_cmd)
        tools.addWidget(self.exit)
        tools.addStretch()

        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)

        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)

    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        # Create Run CMD Layout
        RunCMDLayout = QGridLayout()
        requiredArgs = QLabel("<h4><b>Required Arguments:</b></h4>")
        address = QLabel("Address (Portal IP, hostname, or FQDN):")
        username = QLabel("Portal Admin Username:")
        password = QLabel("Password")
        command = QLabel("Command")
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
        RunCMDLayout.addWidget(command, 3, 1)
        RunCMDLayout.addWidget(self.passwordField, 4, 0)
        RunCMDLayout.addWidget(self.commandField, 4, 1)

        toolView.addLayout(RunCMDLayout)


        # Create action buttons
        actionButtonLayout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.start = QPushButton("Start")

        actionButtonLayout.addWidget(self.cancel)
        actionButtonLayout.addWidget(self.start)

        toolView.addLayout(actionButtonLayout)
        
        # Create Output box
        self.output = QTextEdit()
        self.output.setFixedHeight(OUTPUT_HEIGHT)
        self.output.setReadOnly(True)
        toolView.addWidget(self.output)

        self.mainContent.addLayout(toolView)
    
    
    def _updateOutput(self):
        file = open("info-log.txt", 'r')

        with file:
            text = file.read()
            self.output.setText(text)


        """current = self.output.toPlainText()
        result = str(current) + 'Clicked '
        self.output.setText(str(result))"""



class CTools:
    """CTools controller class"""
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _runCmd(self):
        """address = self._view.addressField
        username = self._view.usernameField
        password = self._view.passwordField"""
        command = self._view.commandField.text()

        #global_admin = global_admin_login(str(address), str(username), str(password))

        #result = self._evaluate(global_admin, command)

        self._evaluate(command)
        self._view._updateOutput()

    
    def _test(self):
        print("testing")

    def _connectSignalsAndSlots(self):
        self._view.start.clicked.connect(self._runCmd)
        #self._view.start.clicked.connect(self._test)

def model(argument):
    #run_cmd(address, username, password, command)
    
    return fakeFunc(argument)

def main():
    """PyCalc's main function."""
    
    set_logging()

    ctoolsApp = QApplication(sys.argv)
    ctoolsWindow = CToolsWindow()
    ctoolsWindow.show()
    controller = CTools(model=model, view=ctoolsWindow)
    ctoolsApp.exec_()

    

if __name__ == "__main__":
    main()