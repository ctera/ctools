import logging
from log_setter import set_logging
## STEP6a - import the tool function from the file you imported into the CTOOLS3 project folder
from importshares import import_shares
from copyshares import copyshares
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
    QLineEdit,
    QFrame,
)
from PySide6.QtGui import (
    QPixmap
)
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600
OUTPUT_HEIGHT = 250
class importSharesWindow(QMainWindow):
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
        tools = create_tool_bar(self.widget, 10)
        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)
        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)
    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        tooltip = """Copy shares from source edge filer to another destination edge filer.
  -  Source Device IP/FQDN: IP or FQDN of the source edge filer.
  -  Source Admin Username: Username of the source edge filer.
  -  Source Admin Password: Password of the source edge filer.
  -  Destination Device IP/FQDN: IP or FQDN of the destination edge filer.
  -  Destination Admin Username: Username of the destination edge filer.
  -  Destination Admin Password: Password of the destination edge filer.
  -  Verbose Logging: Enable debug logging."""

        # Step3 - You will change the next two lines according to the KB
        BoilerLayout, self.input_widgets = gen_custom_tool_layout("Copy Shares", ["Source Device IP/FQDN", "Source Admin Username", "Source Admin Password", "Destination Device IP/FQDN", "Destination Admin Username", "Destination Admin Password"], ["Verbose Logging"], False, tooltip=tooltip)
        self.input_widgets[2].setEchoMode(QLineEdit.Password)
        self.input_widgets[5].setEchoMode(QLineEdit.Password)
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
        source_address = self.input_widgets[0].text()
        source_username = self.input_widgets[1].text()
        source_password = self.input_widgets[2].text()
        destination_address = self.input_widgets[3].text()
        destination_username = self.input_widgets[4].text()
        destination_password = self.input_widgets[5].text()
        verbose = self.input_widgets[6].isChecked()
        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()     
        ## Step6b - Run the tool here
        # Ex: run_status(global_admin, filename, all_tenants_flag)
        copyshares(source_address, source_username, source_password, destination_address, destination_username, destination_password)
        self._updateOutput()
    def _updateOutput(self):
        file = open("output.tmp", 'r')
        with file:
            text = file.read()
            self.output.setText(text)
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())