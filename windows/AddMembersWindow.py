import logging
from log_setter import set_logging
from add_members import add_user_to_admin
## STEP6a - import the tool function from the file you imported into the CTOOLS3 project folder
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
    QGridLayout,
    QLineEdit,
    QComboBox,
    QCheckBox
)
from PySide6.QtGui import (
    QPixmap
)
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600
OUTPUT_HEIGHT = 250
class addMembersWindow(QMainWindow):
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
        tools = create_tool_bar(self.widget, 11)
        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)
        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)
    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        tooltip = """Add or Remove Users/Groups to Edge Filer Admin Group
  -  Address: The IP address of the CTERA Portal
  -  Username: The global admin username of the CTERA Portal
  -  Password: The global admin password of the CTERA Portal
  -  Add or Remove: Select whether you want to add or remove a user/group
      -  Add: Select whether you want to add a domain user or domain group
      -  Remove: Select whether you want to remove a domain user or domain group
  -  Perform on: Select whether you want to perform the action on one device, all devices on one tenant, or all devices on all tenants
  -  Tenant Name: The name of the tenant you want to perform the action on
  -  Device Name: The name of the device you want to perform the action on
  -  User/Group: The domain user or domain group you want to add/remove
  -  Verbose Logging: Enable debug logging"""

        # Step3 - You will change the next two lines according to the KB
        AddMembersLayout = QGridLayout()

        tool_header = QHBoxLayout()
        tool_name = QLabel("<h2><b>Add or Remove Members to Admin Group</b></h2>")

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
        
        address = QLabel("Portal Address, hostname, or FQDN")
        self.address_field = QLineEdit()
        
        username = QLabel("Username for portal admin")
        self.username_field = QLineEdit()

        password = QLabel("Password")
        self.password_field = QLineEdit()

        self.password_field.setEchoMode(QLineEdit.Password)

        add_or_remove = QLabel("Add or Remove:")
        self.add_or_remove_field = QComboBox()
        self.add_or_remove_field.addItem("Add")
        self.add_or_remove_field.addItem("Remove")

        self.add = QLabel("Add:")
        self.add_type = QComboBox()
        self.add_type.addItem("Domain User")
        self.add_type.addItem("Domain Group")

        self.user_group_field = QLineEdit()

        self.user_group = QLabel("User:")

        self.perform = QLabel("Perform on:")
        self.perform_field = QComboBox()
        self.perform_field.addItem("One Device")
        self.perform_field.addItem("All Devices on One Tenant")
        self.perform_field.addItem("All Devices on All Tenants")

        self.tenant_name = QLabel("Tenant Name:")
        self.tenant_name_field = QLineEdit()

        self.device_name = QLabel("Device Name:")
        self.device_name_field = QLineEdit()
        
        self.verbose_box = QCheckBox("Verbose Logging")

        AddMembersLayout.addLayout(tool_header, 0, 0, 1, 2)
        AddMembersLayout.addWidget(requiredArgs, 1, 0, 1, 2)
        AddMembersLayout.addWidget(address, 2, 0)
        AddMembersLayout.addWidget(username, 2, 1)
        AddMembersLayout.addWidget(self.address_field, 3, 0)
        AddMembersLayout.addWidget(self.username_field, 3, 1)
        AddMembersLayout.addWidget(password, 4, 0, 1, 2)
        AddMembersLayout.addWidget(add_or_remove, 6, 0)
        AddMembersLayout.addWidget(self.add, 6, 1)
        AddMembersLayout.addWidget(self.password_field, 5, 0, 1, 2)
        AddMembersLayout.addWidget(self.add_or_remove_field, 7, 0)
        AddMembersLayout.addWidget(self.add_type, 7, 1)
        AddMembersLayout.addWidget(self.perform, 8, 0, 1, 2)
        AddMembersLayout.addWidget(self.perform_field, 9, 0, 1, 2)
        AddMembersLayout.addWidget(self.user_group, 12, 0)
        AddMembersLayout.addWidget(self.user_group_field, 13, 0)
        AddMembersLayout.addWidget(self.tenant_name, 10, 0)
        AddMembersLayout.addWidget(self.tenant_name_field, 11, 0)
        AddMembersLayout.addWidget(self.device_name, 10, 1)
        AddMembersLayout.addWidget(self.device_name_field, 11, 1)
        AddMembersLayout.addWidget(self.verbose_box, 14, 0)

        self.add_type.currentTextChanged.connect(self.updateLabel)
        self.add_or_remove_field.currentTextChanged.connect(self.updateAddRemove)
        self.perform_field.currentIndexChanged.connect(self.handle_selection_change)


        toolView.addLayout(AddMembersLayout)
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
    def updateLabel(self, text):
        # Update the text of the QLabel based on the current text of the QComboBox
        if text == "Domain User":
            self.user_group.setText("User:")
        else:
            self.user_group.setText("Group:")

    def updateAddRemove(self, text):
        # Update the text of the QLabel based on the current text of the QComboBox
        if text == "Add":
            self.add.setText("Add:")
        else:
            self.add.setText("Remove:")

    def handle_selection_change(self, index):
        # Hide all widgets by default
        self.tenant_name.setVisible(False)
        self.tenant_name_field.setVisible(False)
        self.device_name.setVisible(False)
        self.device_name_field.setVisible(False)

        # Show the appropriate widgets based on the selection
        if index == 0:  # "One Device"
            self.device_name.setVisible(True)
            self.device_name_field.setVisible(True)
            self.tenant_name.setVisible(True)
            self.tenant_name_field.setVisible(True)
        elif index == 1:  # "All Devices on One Tenant"
            self.tenant_name.setVisible(True)
            self.tenant_name_field.setVisible(True)

    def tool(self):
        user = None
        group = None
        add_or_remove = self.add_or_remove_field.currentText()
        portal_address = self.address_field.text()
        portal_username = self.username_field.text()
        portal_password = self.password_field.text()
        if self.tenant_name.isVisible():
            tenant_name = self.tenant_name_field.text()
        else:
            tenant_name = None
        if self.device_name.isVisible():
            device_name = self.device_name_field.text()
        else:
            device_name = None
        if self.add_type.currentText() == "Domain User":
            user = self.user_group_field.text()
        else:
            group = self.user_group_field.text()
        
        if self.perform_field.currentText() == "All Devices on All Tenants":
            all_devices = True
        else:
            all_devices = False
        verbose = self.verbose_box.isChecked()
        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()

        global_admin = global_admin_login(portal_address, portal_username, portal_password, True)

        global_admin.portals.browse_global_admin()

        global_admin.api.put('/rolesSettings/readWriteAdminSettings/allowSSO', 'true')
        global_admin = global_admin_login(portal_address, portal_username, portal_password, True)
        ## Step6b - Run the tool here
        add_user_to_admin(global_admin, add_or_remove, user, group, tenant_name=tenant_name, device_name=device_name, all_devices=all_devices)
        self._updateOutput()
    def _updateOutput(self):
        file = open("output.tmp", 'r')
        with file:
            text = file.read()
            self.output.setText(text)
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())