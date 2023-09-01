import logging

from log_setter import set_logging
## STEP6a - import the tool function from the file you imported into the CTOOLS3 project folder
from suspend_sync import suspend_filer_sync
from smb_audit import smb_audit

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
    QComboBox,
    QFileDialog,
    QLineEdit,
    QCheckBox
)

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
OUTPUT_HEIGHT = 250

class smbAuditWindow(QMainWindow):
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
        tools = create_tool_bar(self.widget, 9)

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
        #SMBAuditLayout, self.input_widgets = gen_custom_tool_layout(["Function", "Source Directory", "Output file", "Input file", "Time interval", "Search String", "Search Field"], ["Enable Debug output of args", "Verbose Logging"], False)
        
        SMBAuditLayout = QGridLayout()
        requiredArgs = QLabel("<h4><b>Required Arguments:</b></h4>")

        #Create input fields for SMB Audit
        function = QLabel("Function")
        self.function_field = QComboBox()
        self.function_field.addItem("Parse")
        self.function_field.addItem("Summarize")
        self.function_field.addItem("Search")

        source_directory = QLabel("Source log directory containing only audit log files")
        self.source_directory_field = QHBoxLayout()
        self.filename_edit = QLineEdit()
        
        file_browse = QPushButton("Browse")
        file_browse.clicked.connect(self.open_file_dialog_source)

        self.source_directory_field.addWidget(self.filename_edit)
        self.source_directory_field.addWidget(file_browse)
        #source_directory_field = QFileDialog()
        #source_directory_field.setFileMode(QFileDialog.FileMode.ExistingFiles)
        
        output_file = QLabel("Label for output files")
        self.output_file_field = QLineEdit()

        ftr_file = QLabel("Name of input file (Format: customer_location.ftr)")
        self.ftr_file_field = QHBoxLayout()
        self.ftr_filename_edit = QLineEdit()

        ftr_file_browse = QPushButton("Browse")
        ftr_file_browse.clicked.connect(self.open_file_dialog_ftr)

        self.ftr_file_field.addWidget(self.ftr_filename_edit)
        self.ftr_file_field.addWidget(ftr_file_browse)
        #ftr_file_field = QFileDialog()
        #ftr_file_field.setFileMode(QFileDialog.FileMode.ExistingFiles)

        time_interval = QLabel("Time interval for summary computations")
        self.time_interval_field = QComboBox()
        self.time_interval_field.addItem("5min")
        self.time_interval_field.addItem("10min")
        self.time_interval_field.addItem("15min")
        self.time_interval_field.addItem("20min")
        self.time_interval_field.addItem("30min")
        self.time_interval_field.addItem("60min")

        search_string = QLabel("String to search for in the specified area")
        self.search_string_field = QLineEdit()

        search_field= QLabel("Fields to be searched from the audit logs:")
        self.search_field_field = QComboBox()
        self.search_field_field.addItem("path")
        self.search_field_field.addItem("share")
        self.search_field_field.addItem("user")

        is_debug = QLabel("Enable debug output of arguments")
        self.is_debug_box = QCheckBox("is_debug")
        verbose = QLabel("Add verbose logging")
        self.verbose_box = QCheckBox("Verbose")

        SMBAuditLayout.addWidget(requiredArgs, 0, 0, 1, 2)
        SMBAuditLayout.addWidget(function, 1, 0)
        SMBAuditLayout.addWidget(source_directory, 1, 1)
        SMBAuditLayout.addWidget(self.function_field, 2, 0)
        SMBAuditLayout.addLayout(self.source_directory_field, 2, 1)
        SMBAuditLayout.addWidget(output_file, 3, 0)
        SMBAuditLayout.addWidget(ftr_file, 3, 1)
        SMBAuditLayout.addWidget(self.output_file_field, 4, 0)
        SMBAuditLayout.addLayout(self.ftr_file_field, 4, 1)
        SMBAuditLayout.addWidget(time_interval, 5, 0)
        SMBAuditLayout.addWidget(search_string, 5, 1)
        SMBAuditLayout.addWidget(self.time_interval_field, 6, 0)
        SMBAuditLayout.addWidget(self.search_string_field, 6, 1)
        SMBAuditLayout.addWidget(search_field, 7, 0)
        SMBAuditLayout.addWidget(is_debug, 7, 1)
        SMBAuditLayout.addWidget(self.search_field_field, 8, 0)
        SMBAuditLayout.addWidget(self.is_debug_box, 8, 1)
        SMBAuditLayout.addWidget(verbose, 9, 0)
        SMBAuditLayout.addWidget(self.verbose_box, 10, 0)
        
        toolView.addLayout(SMBAuditLayout)

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
    
    def open_file_dialog_source(self):
        filename = QFileDialog.getExistingDirectory(self, "Select a directory")

        if filename:
            path = Path(filename)
            self.filename_edit.setText(str(path))

    def open_file_dialog_ftr(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a file",
        )

        if filename:
            path = Path(filename)
            self.ftr_filename_edit.setText(str(path))

    # STEP4 - Grab the arguments for you tool
    def tool(self):
        function = self.function_field.currentText()
        source_directory = self.filename_edit.text()
        output_file = self.output_file_field.text()
        ftr_file = self.ftr_filename_edit.text()
        time_interval = self.time_interval_field.currentText()
        search_string = self.search_string_field.text()
        search_field = self.filename_edit.text()
        is_debug = self.is_debug_box.isChecked()
        verbose = self.verbose_box.isChecked()

        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()

        
        ## Step6 - Run the tool here
        # Ex: run_status(global_admin, filename, all_tenants_flag)
        smb_audit({"function": function, "source_directory": source_directory, "output_file": output_file, "ftr_file": ftr_file, "time_interval": time_interval, "search_field": search_field, "search_string": search_string, "is_debug": is_debug, "verbose": verbose})


        self._updateOutput()

    def _updateOutput(self):
        file = open("output.tmp", 'r')

        with file:
            text = file.read()
            self.output.setText(text)
        
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
