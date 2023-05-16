# ctools.py

"""CTools is a GUI toolset to interact with your CTERA Environment"""

import sys, logging, os

from run_cmd import run_cmd
from status import run_status

from testfuncs import fakeFunc
from ui_help import gen_tool_layout, gen_custom_tool_layout

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
    QFrame,
    QStackedWidget
)

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
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


class runCmdWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""

    def __init__(self, widget):
        super().__init__()
        self.widget = widget
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
        self.run_cmd = QPushButton("Run CMD")
        self.run_cmd.setStyleSheet("color: grey")
        self.show_status = QPushButton("Show Status")
        self.exit = QPushButton("Exit")

        tools.addWidget(label, alignment=Qt.AlignTop)
        tools.addWidget(self.run_cmd)
        tools.addWidget(self.show_status)
        tools.addWidget(self.exit)
        tools.addStretch()

        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)

        #Add button listeners
        self.show_status.clicked.connect(self.goToShowStatus)

        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)

    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        RunCMDLayout, self.input_widgets = gen_custom_tool_layout(["Command", "Device Name (Overrides the \"All Tenants\" checkbox)"], ["Run on all Tenants (No device name needed)", "Ignore Cert Warnings for Login", "Verbose Logging"])

        toolView.addLayout(RunCMDLayout)


        # Create action buttons
        actionButtonLayout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.start = QPushButton("Start")

        actionButtonLayout.addWidget(self.cancel)
        actionButtonLayout.addWidget(self.start)

        toolView.addLayout(actionButtonLayout)

        # Add button listeners
        self.start.clicked.connect(self.runCmd)
        
        # Create Output box
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        toolView.addWidget(self.output)

        self.mainContent.addLayout(toolView)
    
    def runTool(self):
        fakeFunc(self.input_widgets[3].text())
        self._updateOutput()
    
    def runCmd(self):
        portal_address = self.input_widgets[0].text()
        portal_username = self.input_widgets[1].text()
        portal_password = self.input_widgets[2].text()
        command = self.input_widgets[3].text()
        device_name = self.input_widgets[4].text()
        all_filers_flag = self.input_widgets[5].isChecked()
        ignore_cert = self.input_widgets[6].isChecked()
        verbose = self.input_widgets[7].isChecked()

        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()

        global_admin = global_admin_login(portal_address, portal_username, portal_password, ignore_cert)
        
        if not device_name:
            run_cmd(global_admin, command, all_filers_flag)
        else:
            run_cmd(global_admin, command, all_filers_flag, device_name)
        self._updateOutput()

    def _updateOutput(self):
        file = open("info-log.txt", 'r')

        with file:
            text = file.read()
            self.output.setText(text)
        
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())

    def goToShowStatus(self):
        self.widget.setCurrentIndex(1)


class showStatusWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""

    def __init__(self, widget):
        self.widget = widget
        super().__init__()
        self.setWindowTitle("CTools 3.0")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.generalLayout = QVBoxLayout()
        self.top = QLabel("<h2>Show Status</h2>")
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
        self.run_cmd = QPushButton("Run CMD")
        self.show_status = QPushButton("Show Status")
        self.show_status.setStyleSheet("color: grey")
        self.exit = QPushButton("Exit")

        tools.addWidget(label, alignment=Qt.AlignTop)
        tools.addWidget(self.run_cmd)
        tools.addWidget(self.show_status)
        tools.addWidget(self.exit)
        tools.addStretch()

        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)

        #Add button listeners
        self.run_cmd.clicked.connect(self.goToRunCmd)

        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)

    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        show_status_layout, self.input_widgets = gen_custom_tool_layout(["File Name"], ["Run on all Tenants (No device name needed)", "Ignore Cert Warnings for Login", "Verbose Logging"])

        toolView.addLayout(show_status_layout)


        # Create action buttons
        actionButtonLayout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.start = QPushButton("Start")

        actionButtonLayout.addWidget(self.cancel)
        actionButtonLayout.addWidget(self.start)

        toolView.addLayout(actionButtonLayout)

        # Add button listeners
        self.start.clicked.connect(self.showStatus)
        
        # Create Output box
        self.output = QTextEdit()
        #self.output.setFixedHeight(OUTPUT_HEIGHT)
        self.output.setReadOnly(True)
        toolView.addWidget(self.output)

        self.mainContent.addLayout(toolView)
    
    def showStatus(self):
        portal_address = self.input_widgets[0].text()
        portal_username = self.input_widgets[1].text()
        portal_password = self.input_widgets[2].text()
        filename = self.input_widgets[3].text()
        global_admin = global_admin_login(portal_address, portal_username, portal_password, True)

        run_status(global_admin, filename, True)
        self._updateOutput()
    
    def _updateOutput(self):
        file = open("info-log.txt", 'r')

        with file:
            text = file.read()
            self.output.setText(text)
    
    def goToRunCmd(self):
        self.widget.setCurrentIndex(0)


def main():
    """PyCalc's main function."""
    
    #set_logging()

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    ctoolsApp = QApplication(sys.argv)
    
    
    widget = QStackedWidget()
    
    run_cmd = runCmdWindow(widget)
    widget.addWidget(run_cmd)   # create an instance of the first page class and add it to stackedwidget

    show_status = showStatusWindow(widget) 
    widget.addWidget(show_status)   # adding second page

    widget.setCurrentWidget(run_cmd)   # setting the page that you want to load when application starts up. you can also use setCurrentIndex(int)

    widget.show()

    ctoolsApp.exec_()

    

if __name__ == "__main__":
    main()