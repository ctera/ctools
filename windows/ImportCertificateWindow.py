import logging

from log_setter import set_logging
## STEP6a - import the tool function from the file you imported into the CTOOLS3 project folder
#from filer_cert_import import import_cert
from filer_cert_import import import_cert

from ui_help import gen_tool_layout, gen_custom_tool_layout, create_tool_bar
from login import global_admin_login

from PySide6.QtCore import Qt

from pathlib import Path

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
    QFileDialog,
    QCheckBox
)

from PySide6.QtGui import (
    QPixmap
)

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
OUTPUT_HEIGHT = 250

class importCertificateWindow(QMainWindow):
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
        tools = create_tool_bar(self.widget, 16)

        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)

        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)

    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        tooltip = """Import a certificate to an Edge Filer.
  -  Edge IP Address: IP of the Edge Filer.
  -  Admin Username: Username of the Edge Filer.
  -  Admin Password: Password of the Edge Filer.
  -  Private Key File: Path to the private key file.
  -  Certificate Files: Path to the certificate files. Be sure to select all files when you browse files.
  
  DISCLAIMER: This tool's output goes to the commandline window separate from the GUI. Please do not close the commandline window while the tool is running."""

        # Create the layout for the tool
        CloudFoldersLayout = QGridLayout()

        # Headers and labels
        tool_header = QHBoxLayout()
        tool_name = QLabel("<h2><b>Import Certificate</b></h2>")

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


        requiredArgs = QLabel("<h4><b>Required Arguments</b></h4>")

        # Address input
        address = QLabel("Edge IP Address")
        self.address_field = QLineEdit()

        # Username input
        username = QLabel("Admin Username")
        self.username_field = QLineEdit()

        # Password input
        password = QLabel("Admin Password")
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)

        # Private Key File input
        priv_key_file = QLabel("Private Key File")
        self.priv_key_file_field = QHBoxLayout()
        self.priv_key_filename_edit = QLineEdit()
        priv_key_file_browse = QPushButton("Browse")
        priv_key_file_browse.clicked.connect(self.open_priv_key_file_dialog)
        self.priv_key_file_field.addWidget(self.priv_key_filename_edit)
        self.priv_key_file_field.addWidget(priv_key_file_browse)

        # **Certificate Files input (Multiple files)**
        cert_files_label = QLabel("Certificate Files")
        self.cert_files_field = QHBoxLayout()
        self.cert_files_edit = QLineEdit()
        cert_files_browse = QPushButton("Browse")
        cert_files_browse.clicked.connect(self.open_cert_files_dialog)
        self.cert_files_field.addWidget(self.cert_files_edit)
        self.cert_files_field.addWidget(cert_files_browse)

        # Verbose Logging checkbox
        self.verbose_box = QCheckBox("Verbose Logging")

        # Adding widgets to the layout
        CloudFoldersLayout.addLayout(tool_header, 0, 0, 1, 2)
        CloudFoldersLayout.addWidget(requiredArgs, 1, 0, 1, 2)
        CloudFoldersLayout.addWidget(address, 2, 0)
        CloudFoldersLayout.addWidget(username, 2, 1)
        CloudFoldersLayout.addWidget(self.address_field, 3, 0)
        CloudFoldersLayout.addWidget(self.username_field, 3, 1)
        CloudFoldersLayout.addWidget(password, 4, 0)
        CloudFoldersLayout.addWidget(priv_key_file, 4, 1)
        CloudFoldersLayout.addWidget(self.password_field, 5, 0)
        CloudFoldersLayout.addLayout(self.priv_key_file_field, 5, 1)
        CloudFoldersLayout.addWidget(cert_files_label, 6, 0, 1, 2)
        CloudFoldersLayout.addLayout(self.cert_files_field, 7, 0, 1, 2)
        CloudFoldersLayout.addWidget(self.verbose_box, 8, 0, 1, 2)

        toolView.addLayout(CloudFoldersLayout)

        # Create action buttons
        actionButtonLayout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.start = QPushButton("Start")
        self.cancel.clicked.connect(self.close)  # Assuming you have a close method
        self.start.clicked.connect(self.tool)

        actionButtonLayout.addWidget(self.cancel)
        actionButtonLayout.addWidget(self.start)

        toolView.addLayout(actionButtonLayout)

        # Create Output box
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        toolView.addWidget(self.output)

        self.mainContent.addLayout(toolView)

    def open_priv_key_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Private Key File",
            "",
            "Private Key Files (*.pem *.key);;All Files (*)"
        )
        if filename:
            path = Path(filename)
            self.priv_key_filename_edit.setText(str(path))

    def open_cert_files_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Certificate Files",
            "",
            "Certificate Files (*.pem *.crt);;All Files (*)"
        )
        if files:
            # Join the file paths with semicolons or another separator
            self.cert_files_edit.setText('; '.join(files))

    # STEP4 - Grab the arguments for you tool
    def tool(self):
        edge_address = self.address_field.text()
        edge_username = self.username_field.text()
        edge_password = self.password_field.text()
        priv_key_file = self.priv_key_filename_edit.text()
        certificate_files_text = self.cert_files_edit.text()
        # Split the text into a list of file paths
        certificate_files = [file.strip() for file in certificate_files_text.split(';') if file.strip()]
        verbose = self.verbose_box.isChecked()

        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()
        
        ## Step6 - Run the tool here
        # Ex: run_status(global_admin, filename, all_tenants_flag)
        import_cert(edge_address, edge_username, edge_password, priv_key_file, *certificate_files)
        
        self._updateOutput()

    def _updateOutput(self):
        file = open("output.tmp", 'r')

        with file:
            text = file.read()
            self.output.setText(text)
        
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
