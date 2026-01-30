import logging

from log_setter import set_logging
## STEP6a - import the tool function from the file you imported into the CTOOLS3 project folder
from unlock import disable_ssh

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

class disableSSHWindow(QMainWindow):
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
        tools = create_tool_bar(self.widget, 5)

        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)

        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)

    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        tooltip = """Disable SSH on an edge filer
  -  Address: The IP address of the CTERA Portal
  -  Username: The global admin username of the CTERA Portal
  -  Password: The global admin password of the CTERA Portal
  -  Device Name: The name of the device to disable SSH on
  -  Tenant Name: The name of the tenant the device is in
  -  Verbose Logging: Enable debug logging
  
  DISCLAIMER: This tool's output goes to the commandline window separate from the GUI. Please do not close the commandline window while the tool is running."""

        # Step3 - You will change the next two lines according to the KB
        DisableSSHLayout, self.input_widgets = gen_custom_tool_layout("Disable SSH", ["Device Name", "Tenant Name"], ["Verbose Logging"], tooltip=tooltip)
        toolView.addLayout(DisableSSHLayout)

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
        tenant_name = self.input_widgets[4].text()
        verbose = self.input_widgets[5].isChecked()

        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()

        global_admin = global_admin_login(portal_address, portal_username, portal_password, True)

        global_admin.portals.browse_global_admin()

        global_admin.api.put('/rolesSettings/readWriteAdminSettings/allowSSO', 'true')

        global_admin = global_admin_login(portal_address, portal_username, portal_password, True)
        
        ## Step6 - Run the tool here
        # Ex: run_status(global_admin, filename, all_tenants_flag)
        disable_ssh(global_admin, device_name, tenant_name)


        self._updateOutput()

    def _updateOutput(self):
        file = open("output.tmp", 'r')

        with file:
            text = file.read()
            self.output.setText(text)
        
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
