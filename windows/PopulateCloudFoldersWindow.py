import logging
from log_setter import set_logging
## STEP6a - import the tool function from the file you imported into the CTOOLS3 project folder
from populate import run_populate
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
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600
OUTPUT_HEIGHT = 250
class populateCloudFoldersWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.setWindowTitle("CTools 3.0")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.generalLayout = QVBoxLayout()
        self.top = QHBoxLayout()
        welcome = QLabel("<h2>Welcome to CTools!</h2><h5>One tool for all</h5>")
        pic_label = QLabel(self)
        pixmap = QPixmap("C:\\Users\\lakea\\Desktop\\CTERA\\ctools\\logo.png")#replace with image location
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
        tools = create_tool_bar(self.widget, 13)
        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)
        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)
    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        tooltip = """Populate edge filer shares for every cloud folder in its portal (excluding My Files).
  -  Address: The IP address of the CTERA Portal
  -  Username: The global admin username of the CTERA Portal
  -  Password: The global admin password of the CTERA Portal
  -  Device Name: The name of the edge filer to populate shares on
  -  Domain Name: The domain name of the edge filer. This is only needed if domain users are cloud folder owners
  -  Ignore cert warnings for login: Check this box to ignore certificate warnings when logging in
  -  Verbose Logging: Check this box to enable debug logging
  
  DISCLAIMER: This tool's output goes to the commandline window separate from the GUI. Please do not close the commandline window while the tool is running."""

        # Step3 - You will change the next two lines according to the KB
        BoilerLayout, self.input_widgets = gen_custom_tool_layout("Populate Cloud Folders as Shares (Except My Files)", ["Device Name", "Domain Name (Only needed if domain users are cloud folder owners)"], ["Ignore cert warnings for login", "Verbose Logging"], tooltip=tooltip)
        toolView.addLayout(BoilerLayout)
        # Create action buttons
        actionButtonLayout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.start = QPushButton("Start")
        actionButtonLayout.addWidget(self.cancel)
        actionButtonLayout.addWidget(self.start)
        toolView.addLayout(actionButtonLayout)
        # STEP5 - Add button listeners
        self.start.clicked.connect(self.tool)
        # Create Output box
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        toolView.addWidget(self.output)
        self.mainContent.addLayout(toolView)
    # STEP4 - Grab the arguments for you tool
    def tool(self):
        portal_address = self.input_widgets[0].text()
        portal_username = self.input_widgets[1].text()
        portal_password = self.input_widgets[2].text()
        device_name = self.input_widgets[3].text()
        domain_name = self.input_widgets[4].text()
        ignore_cert = self.input_widgets[5].isChecked()
        verbose = self.input_widgets[6].isChecked()
        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()
        ## Step6b - Run the tool here
        # Ex: run_status(global_admin, filename, all_tenants_flag)
        run_populate(portal_address, portal_username, portal_password, device_name, domain_name)
        self._updateOutput()
    def _updateOutput(self):
        file = open("output.tmp", 'r')
        with file:
            text = file.read()
            self.output.setText(text)
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())