import logging

from log_setter import set_logging
## STEP6a - import the tool function from the file you imported into the CTOOLS3 project folder
from cloud_folders import create_folders

from ui_help import gen_tool_layout, gen_custom_tool_layout, create_tool_bar
from login import global_admin_login

from PySide2.QtCore import Qt

from pathlib import Path

from PySide2.QtWidgets import (
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
    QFileDialog,
    QCheckBox
)

from PySide2.QtGui import (
    QPixmap
)

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600
OUTPUT_HEIGHT = 250

class cloudFoldersWindow(QMainWindow):
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
        pixmap = QPixmap("logo.png")
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
        tools = create_tool_bar(self.widget, 8)

        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)

        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)

    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        # Step3 - You will change the next two lines according to the KB
        #CloudFoldersLayout, self.input_widgets = gen_custom_tool_layout(["CSV File"], ["Ignore cert warnings for login", "Verbose Logging"])
        
        CloudFoldersLayout = QGridLayout()
        tool_header = QLabel("<h2><b>CloudFS</b></h2>")
        requiredArgs = QLabel ("<h4><b>Required Arguments</b></h4>")
        
        address = QLabel("Portal Address, hostname, or FQDN")
        self.address_field = QLineEdit()
        
        username = QLabel("Username for portal admin")
        self.username_field = QLineEdit()

        password = QLabel("Password")
        self.password_field = QLineEdit()

        csv_file = QLabel("CSV File")
        self.csv_file_field = QHBoxLayout()
        self.filename_edit = QLineEdit()

        file_browse = QPushButton("Browse")
        file_browse.clicked.connect(self.open_file_dialog)

        self.csv_file_field.addWidget(self.filename_edit)
        self.csv_file_field.addWidget(file_browse)

        verbose = QLabel("Add verbose logging")
        self.verbose_box = QCheckBox("Verbose")
        ignore_cert = QLabel("Ignore cert warnings")
        self.ignore_cert_box = QCheckBox("ignore_cert")

        CloudFoldersLayout.addWidget(tool_header, 0, 0, 1, 2)
        CloudFoldersLayout.addWidget(requiredArgs, 1, 0, 1, 2)
        CloudFoldersLayout.addWidget(address, 2, 0)
        CloudFoldersLayout.addWidget(username, 2, 1)
        CloudFoldersLayout.addWidget(self.address_field, 3, 0)
        CloudFoldersLayout.addWidget(self.username_field, 3, 1)
        CloudFoldersLayout.addWidget(password, 4, 0)
        CloudFoldersLayout.addWidget(csv_file, 4, 1)
        CloudFoldersLayout.addWidget(self.password_field, 5, 0)
        CloudFoldersLayout.addLayout(self.csv_file_field, 5, 1)
        CloudFoldersLayout.addWidget(verbose, 6, 0)
        CloudFoldersLayout.addWidget(ignore_cert, 6, 1)
        CloudFoldersLayout.addWidget(self.verbose_box, 7, 0)
        CloudFoldersLayout.addWidget(self.ignore_cert_box, 7, 1)


        toolView.addLayout(CloudFoldersLayout)

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
    
    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a file",
        )

        if filename:
            path = Path(filename)
            self.filename_edit.setText(str(path))

    # STEP4 - Grab the arguments for you tool
    def tool(self):
        portal_address = self.address_field.text()
        portal_username = self.username_field.text()
        portal_password = self.password_field.text()
        csv_file = self.filename_edit.text()
        ignore_cert = self.ignore_cert_box.isChecked()
        verbose = self.verbose_box.isChecked()

        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()

        global_admin = global_admin_login(portal_address, portal_username, portal_password, ignore_cert)

        global_admin.portals.browse_global_admin()

        global_admin.put('/rolesSettings/readWriteAdminSettings/allowSSO', 'true')

        global_admin = global_admin_login(portal_address, portal_username, portal_password, ignore_cert)
        
        ## Step6 - Run the tool here
        # Ex: run_status(global_admin, filename, all_tenants_flag)
        create_folders(global_admin, csv_file)


        self._updateOutput()

    def _updateOutput(self):
        file = open("output.tmp", 'r')

        with file:
            text = file.read()
            self.output.setText(text)
        
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
