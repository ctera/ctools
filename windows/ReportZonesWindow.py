import logging
from log_setter import set_logging
from report_zones import create
## STEP6a - import the tool function from the file you imported into the CTOOLS3 project folder
from ui_help import gen_tool_layout, gen_custom_tool_layout, create_tool_bar
from login import global_admin_login

from pathlib import Path

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
    QGridLayout,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QFileDialog
)
from PySide6.QtGui import (
    QPixmap
)
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600
OUTPUT_HEIGHT = 250
class reportZonesWindow(QMainWindow):
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
        tools = create_tool_bar(self.widget, 12)
        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)
        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)
    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        tooltip = """Create zones report for details such as Devices, Total Size, Total Folders, and Total Files in the desired output location.
  -  Address: IP or FQDN of the portal.
  -  Username: Username of the portal admin.
  -  Password: Password of the portal admin.
  -  Output Location: Select the browse button to select a folder where you would like the report to be generated."""

        # Step3 - You will change the next two lines according to the KB
        ReportZonesLayout = QGridLayout()

        tool_header = QHBoxLayout()
        tool_name = QLabel("<h2><b>Zones Report</b></h2>")

        #generate tool tip
        info_button = QPushButton("i")
        info_button.setToolTip(tooltip)
        info_button.setFixedSize(20, 20)  # Set width and height to make it smaller
        info_button.setStyleSheet("""
            QPushButton {
                border: 1px solid #ccc;
                border-radius: 10px;
                background-color: #e0e0e0;
                color: #363636;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        tool_header.addWidget(tool_name)
        tool_header.addWidget(info_button)

        requiredArgs = QLabel ("<h4><b>Required Arguments</b></h4>")
       
        address = QLabel("Address (Portal IP, hostname, FQDN):")
        self.address_field = QLineEdit()

        username = QLabel("Portal Admin Username:")
        self.username_field = QLineEdit()

        password = QLabel("Portal Admin Password:")
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)

        output_dir = QLabel("Output Location:")
        self.output_field = QHBoxLayout()
        self.output_filename_edit = QLineEdit()

        output_file_browse = QPushButton("Browse")
        output_file_browse.clicked.connect(self.open_directory_dialog)

        self.output_field.addWidget(self.output_filename_edit)
        self.output_field.addWidget(output_file_browse)



        self.verbose_box = QCheckBox("Verbose Logging")

        ReportZonesLayout.addLayout(tool_header, 0, 0, 1, 2)
        ReportZonesLayout.addWidget(requiredArgs, 1, 0, 1, 2)
        ReportZonesLayout.addWidget(address, 2, 0)
        ReportZonesLayout.addWidget(self.address_field, 3, 0)
        ReportZonesLayout.addWidget(username, 2, 1)
        ReportZonesLayout.addWidget(self.username_field, 3, 1)
        ReportZonesLayout.addWidget(password, 4, 0)
        ReportZonesLayout.addWidget(self.password_field, 5, 0)
        ReportZonesLayout.addWidget(output_dir, 4, 1)
        ReportZonesLayout.addLayout(self.output_field, 5, 1)



        toolView.addLayout(ReportZonesLayout)
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

    def open_directory_dialog(self):
      directory = QFileDialog.getExistingDirectory(
        self,
        "Select a directory",
      )

      if directory:
        path = Path(directory)
        self.output_filename_edit.setText(str(path))

    # STEP4 - Grab the arguments for you tool
    def tool(self):
        address = self.address_field.text()
        user = self.username_field.text()
        password = self.password_field.text()
        output_dir = self.output_filename_edit.text()
        verbose = self.verbose_box.isChecked()
        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()
        ## Step6b - Run the tool here
        create(address, user, password, output_dir)
        self._updateOutput()
    def _updateOutput(self):
        file = open("output.tmp", 'r')
        with file:
            text = file.read()
            self.output.setText(text)
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())