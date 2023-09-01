import logging

from log_setter import set_logging
## STEP6a - import the tool function from the file you imported into the CTOOLS3 project folder
from filer import get_filers

from ui_help import gen_custom_tool_layout, create_tool_bar
from login import global_admin_login

import csv

from cterasdk import CTERAException

from PySide2.QtCore import Qt

from PySide2.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QTextEdit,
    QFrame,
    QInputDialog
)

from PySide2.QtGui import (
    QPixmap
)

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
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
        welcome = QLabel("<h2>Welcome to CTools!</h2>")
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
        DeleteSharesLayout, self.input_widgets = gen_custom_tool_layout("Delete Shares", [], ["Ignore Cert Warnings for Login"])
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
        logging.info("hello")

        portal_address = self.input_widgets[0].text()
        portal_username = self.input_widgets[1].text()
        portal_password = self.input_widgets[2].text()
        ignore_cert = self.input_widgets[3].isChecked()

        global_admin = global_admin_login(portal_address, portal_username, portal_password, ignore_cert)

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
                shares = filer.get('/config/fileservices/share')
                for share in shares:
                    logging.info(f"Share name: '{share.name}'")  # Add this line
                    if isinstance(share.name, str) and self.inputText in share.name:
                        shares_to_delete.append(share)

                if shares_to_delete:
                    logging.info(f"The following shares from filer {filer.name} will be deleted:")
                    for share in shares_to_delete:
                        logging.info(f"Share {share.name}")

                    prompt = input('Do you want to proceed? Type Y to confirm:')
                    if prompt.lower() == 'y':
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

        


        self._updateOutput()

    def _updateOutput(self):
        file = open("output.tmp", 'r')

        with file:
            text = file.read()
            self.output.setText(text)
        
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
