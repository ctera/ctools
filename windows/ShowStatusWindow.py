import logging

from log_setter import set_logging
from status import run_status

from ui_help import gen_tool_layout, gen_custom_tool_layout, create_tool_bar
from login import global_admin_login

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QTextEdit,
    QFrame,
)

from PySide6.QtGui import (
    QPixmap
)

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
OUTPUT_HEIGHT = 250

class showStatusWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""

    def __init__(self, widget):
        self.widget = widget
        super().__init__()
        self.setWindowTitle("CTools 3.0")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.generalLayout = QVBoxLayout()
        
        self.top = QHBoxLayout()
        welcome = QLabel("<h2>Welcome to CTools!</h2><h5>One tool for all</h5>")
        pic_label = QLabel(self)
        pixmap = QPixmap("C:\\Users\\lakea\\Desktop\\CTERA\\ctools\\logo.png")
        pic_label.setPixmap(pixmap)
        #pic_label.setScaledContents(True)
        self.top.addWidget(welcome)
        self.top.addStretch()
        self.top.addWidget(pic_label)

        self.mainContent = QHBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self.generalLayout.addLayout(self.top)
        self.generalLayout.addLayout(self.mainContent)
        self._createToolBar()
        self._createToolViewLayout()

    def _createToolBar(self):
        tools = create_tool_bar(self.widget, 1)

        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)

        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)

    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        tooltip = """Grab in depth stats about all devices in the CTERA Portal. Saved to same directory as this program is run from.
  -  Address: The IP address of the CTERA Portal
  -  Username: The global admin username of the CTERA Portal
  -  Password: The global admin password of the CTERA Portal
  -  File Name: The name of the file to save the output to
  -  Run on all Tenants: Check this box if you would like to run the command on all tenants
  -  Verbose Logging: Check this box if you would like to see debug logs
  
  DISCLAIMER: This tool's output goes to the commandline window separate from the GUI. Please do not close the commandline window while the tool is running."""

        show_status_layout, self.input_widgets = gen_custom_tool_layout("Show Status", ["File Name"], ["Run on all Tenants","Verbose Logging"], tooltip=tooltip)

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
        self.output.setReadOnly(True)
        toolView.addWidget(self.output)

        self.mainContent.addLayout(toolView)
    
    def showStatus(self):
        portal_address = self.input_widgets[0].text()
        portal_username = self.input_widgets[1].text()
        portal_password = self.input_widgets[2].text()
        filename = self.input_widgets[3].text()
        all_tenants_flag = self.input_widgets[4].isChecked()
        verbose = self.input_widgets[5].isChecked()

        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()

        global_admin = global_admin_login(portal_address, portal_username, portal_password, True)

        global_admin.portals.browse_global_admin()

        global_admin.api.put('/rolesSettings/readWriteAdminSettings/allowSSO', 'true')
        global_admin = global_admin_login(portal_address, portal_username, portal_password, True)

        run_status(global_admin, filename, all_tenants_flag)
        self._updateOutput()
    
    def _updateOutput(self):
        file = open("output.tmp", 'r')

        with file:
            text = file.read()
            self.output.setText(text)
    