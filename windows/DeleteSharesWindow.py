import logging

from log_setter import set_logging
## STEP6a - import the tool function from the file you imported into the CTOOLS3 project folder
from filer import get_filers

from ui_help import gen_custom_tool_layout, create_tool_bar
from login import global_admin_login

import csv

from cterasdk import CTERAException

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
    QInputDialog,
    QMessageBox
)

from PySide6.QtGui import (
    QPixmap,
)

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600
OUTPUT_HEIGHT = 250

class deleteSharesWindow(QMainWindow):
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

        tooltip = """Tool to assist with deleting shares from multiple filers based on a substring match.
  -  Address: The IP address of the CTERA Portal
  -  Username: The global admin username of the CTERA Portal
  -  Password: The global admin password of the CTERA Portal
  
  It will prompt you for the substring first, and then it will show you all shares that match this substring on each filer one by one and confirm whether you would like to delete them.
  
  DISCLAIMER: This tool's output goes to the commandline window separate from the GUI. Please do not close the commandline window while the tool is running."""

        # Step3 - You will change the next two lines according to the KB
        DeleteSharesLayout, self.input_widgets = gen_custom_tool_layout("Delete Shares", [], [], tooltip=tooltip)
        toolView.addLayout(DeleteSharesLayout)

        # Create action buttons
        actionButtonLayout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.start = QPushButton("Start")

        actionButtonLayout.addWidget(self.cancel)
        actionButtonLayout.addWidget(self.start)

        toolView.addLayout(actionButtonLayout)

        # STEP5 - Add button listeners
        self.start.clicked.connect(self.test_func)
        
        # Create Output box
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        toolView.addWidget(self.output)

        self.mainContent.addLayout(toolView)

    def _getTextInput(self):
        text, ok = QInputDialog.getText(self, "Input", "Please enter the word to delete shares:")

        if ok:
            self.inputText = str(text)
        else:
            self.stop = True

    # STEP4 - Grab the arguments for you tool
    def test_func(self):
        set_logging()
        
        ## Step6 - Run the tool here
        # Ex: run_status(global_admin, filename, all_tenants_flag)
        #testfunc()

        portal_address = self.input_widgets[0].text()
        portal_username = self.input_widgets[1].text()
        portal_password = self.input_widgets[2].text()

        global_admin = global_admin_login(portal_address, portal_username, portal_password, True)

        global_admin.portals.browse_global_admin()

        global_admin.api.put('/rolesSettings/readWriteAdminSettings/allowSSO', 'true')

        global_admin = global_admin_login(portal_address, portal_username, portal_password, True)

        try:
            filers = get_filers(global_admin)

            self.inputText = None
            self.stop = False
            self._getTextInput()
            if not self.stop:
                logging.info(self.inputText)
                # Create/open the CSV file and add headers if it's new
                with open('deleted_shares.csv', 'a+', newline='') as f:
                    f.seek(0)  # Go to the start of the file to check if it's empty
                    writer = csv.writer(f)
                    if f.read() == '':  # If file is empty, write headers
                        writer.writerow(['FilerName', 'ShareName', 'Status'])
                for filer in filers:
                    shares_to_delete = []
                    shares = filer.api.get('/config/fileservices/share')
                    for share in shares:
                        logging.info(f"Share name: '{share.name}'")  # Add this line
                        if isinstance(share.name, str) and self.inputText in share.name:
                            shares_to_delete.append(share)

                    if shares_to_delete:
                        logging.info(f"The following shares from filer {filer.name} will be deleted:")
                        for share in shares_to_delete:
                            logging.info(f"Share {share.name}")

                        formatted_string = "\n".join([f"Filer: {filer.name} - Share: {share.name}" for share in shares_to_delete])

                        confirm = QMessageBox.question(self, 'Confirm', f"Are you sure you want to delete share:\n{formatted_string }", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if confirm == QMessageBox.Yes:
                            with open('deleted_shares.csv', 'a', newline='') as f:
                                writer = csv.writer(f)
                                for share in shares_to_delete:
                                    try:
                                        filer.shares.delete(share.name)
                                        logging.info(f'Share {share.name} deleted')
                                        writer.writerow([filer.name, share.name, 'Deleted'])
                                    except CTERAException as error:
                                        logging.info(f"Failed to delete Share: {share.name} from Filer: {filer.name}")
                                        writer.writerow([filer.name, share.name, 'NotDeleted'])
                        else:
                            logging.info("Request to delete share was not approved.")


        except Exception as e:
            logging.error(e)
        global_admin.logout()
        self._updateOutput()
        

    def _updateOutput(self):
        file = open("output.tmp", 'r')

        with file:
            text = file.read()
            self.output.setText(text)
        
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
