import logging

from log_setter import set_logging
from run_cmd import run_cmd

from ui_help import gen_tool_layout, gen_custom_tool_layout
from login import global_admin_login

from PySide2.QtCore import Qt

from PySide2.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QTextEdit,
    QFrame,
)

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
OUTPUT_HEIGHT = 250

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
    
    def runCmd(self):
        portal_address = self.input_widgets[0].text()
        portal_username = self.input_widgets[1].text()
        portal_password = self.input_widgets[2].text()
        command = self.input_widgets[3].text()
        device_name = self.input_widgets[4].text()
        all_tenants_flag = self.input_widgets[5].isChecked()
        ignore_cert = self.input_widgets[6].isChecked()
        verbose = self.input_widgets[7].isChecked()

        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()

        global_admin = global_admin_login(portal_address, portal_username, portal_password, ignore_cert)
        
        if not device_name:
            run_cmd(global_admin, command, all_tenants_flag)
        else:
            run_cmd(global_admin, command, all_tenants_flag, device_name)
        self._updateOutput()

    def _updateOutput(self):
        file = open("output.tmp", 'r')

        with file:
            text = file.read()
            self.output.setText(text)
        
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())

    def goToShowStatus(self):
        self.widget.setCurrentIndex(1)