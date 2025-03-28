import logging

from log_setter import set_logging
from run_cmd import run_cmd

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



class runCmdWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""

    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle("CTools 3.0")
        self.generalLayout = QVBoxLayout()

        self.top = QHBoxLayout()
        welcome = QLabel("<h2>Welcome to CTools!</h2><h5>One tool for all</h5>")
        pic_label = QLabel(self)
        pixmap = QPixmap("C:\\Users\\lakea\\Desktop\\CTERA\\ctools\\logo.png")
        pic_label.setPixmap(pixmap)
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
        tools = create_tool_bar(self.widget, 0)

        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)

        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)

    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        tooltip = """Run a CLI command on one device, all devices on a tenant, or all devices on all tenants.
Address: The IP address of the CTERA Portal
  -  Username: The global admin username of the CTERA Portal
  -  Password: The global admin password of the CTERA Portal
  -  Command: The CLI command to run on the devices
  -  Tenant Name: The name of the tenant that you would like to perform command on (Not needed if running on all tenants)
  -  Device Name: The name of the device on that tenant that you would like to perform command on (Will perform on all devices on tenant if left blank)
  -  Run on all Tenants: Check this box if you would like to run the command on all tenants
  -  Verbose Logging: Check this box if you would like to see debug logs
  
  DISCLAIMER: This tool's output goes to the commandline window separate from the GUI. Please do not close the commandline window while the tool is running."""
  
        RunCMDLayout, self.input_widgets = gen_custom_tool_layout("Run CMD", ["Command", "Tenant Name", "Device Name (Overrides the \"All Tenants\" checkbox)"], ["Run on all Tenants (No device name needed)","Verbose Logging"], tooltip=tooltip)

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
        tenant_name = self.input_widgets[4].text()
        device_name = self.input_widgets[5].text()
        all_tenants_flag = self.input_widgets[6].isChecked()
        verbose = self.input_widgets[7].isChecked()

        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()

        global_admin = global_admin_login(portal_address, portal_username, portal_password, True)

        global_admin.portals.browse_global_admin()

        global_admin.api.put('/rolesSettings/readWriteAdminSettings/allowSSO', 'true')
        global_admin.logout()

        global_admin = global_admin_login(portal_address, portal_username, portal_password, True)
  
        if not device_name:
            run_cmd(global_admin, command, all_tenants=True)
        else:
            run_cmd(global_admin, command, tenant_name, all_tenants_flag, device_name)

        global_admin.logout()
        self._updateOutput()

    def _updateOutput(self):
        file = open("output.tmp", 'r')

        with file:
            text = file.read()
            self.output.setText(text)
        
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
