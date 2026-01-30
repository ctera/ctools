import logging

from log_setter import set_logging
from worm_settings import get_worm_settings, display_worm_settings, set_worm_grace_period, parse_target_date, calculate_days_until_date

from ui_help import gen_custom_tool_layout, create_tool_bar
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
    QComboBox,
)

from PySide6.QtGui import (
    QPixmap
)

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
OUTPUT_HEIGHT = 200


class wormSettingsWindow(QMainWindow):
    """WORM Settings Management Window."""

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
        tools = create_tool_bar(self.widget, 17)

        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)

        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)

    def _createToolViewLayout(self):
        toolView = QVBoxLayout()

        tooltip = """Manage WORM (Write Once Read Many) settings for folders in CTERA Portal.
Address: The IP address of the CTERA Portal
  -  Username: The global admin username of the CTERA Portal
  -  Password: The global admin password of the CTERA Portal
  -  Folder ID: The numeric ID of the folder
  -  Operation: Get Settings (view) or Set Grace Period (update)
  -  Grace Period Value: Numeric value for grace period (Set operation only)
  -  Grace Period Type: Days, Hours, or Minutes (Set operation only)
  -  Target Date: Alternative to Grace Period Value - specify a future date
     Formats: "20 Feb 2026", "2026-02-20", "20/02/2026"
  -  Verbose Logging: Check this box if you would like to see debug logs

  DISCLAIMER: This tool's output goes to the commandline window separate from the GUI. Please do not close the commandline window while the tool is running."""

        wormSettingsLayout, self.input_widgets = gen_custom_tool_layout(
            "WORM Settings",
            ["Folder ID", "Grace Period Value", "Target Date (e.g., '26 Aug 2026')"],
            ["Verbose Logging"],
            tooltip=tooltip
        )

        toolView.addLayout(wormSettingsLayout)

        # Add operation selector
        operationLabel = QLabel("Operation:")
        self.operationCombo = QComboBox()
        self.operationCombo.addItems(["Get Settings", "Set Grace Period"])
        wormSettingsLayout.addWidget(operationLabel, 9, 0)
        wormSettingsLayout.addWidget(self.operationCombo, 10, 0)

        # Add grace period type selector
        periodTypeLabel = QLabel("Period Type:")
        self.periodTypeCombo = QComboBox()
        self.periodTypeCombo.addItems(["Days", "Hours", "Minutes"])
        wormSettingsLayout.addWidget(periodTypeLabel, 9, 1)
        wormSettingsLayout.addWidget(self.periodTypeCombo, 10, 1)

        # Create action buttons
        actionButtonLayout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.start = QPushButton("Start")

        actionButtonLayout.addWidget(self.cancel)
        actionButtonLayout.addWidget(self.start)

        toolView.addLayout(actionButtonLayout)

        # Add button listeners
        self.start.clicked.connect(self.tool)

        # Create Output box
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMinimumHeight(OUTPUT_HEIGHT)
        toolView.addWidget(self.output)

        self.mainContent.addLayout(toolView)

    def tool(self):
        portal_address = self.input_widgets[0].text()
        portal_username = self.input_widgets[1].text()
        portal_password = self.input_widgets[2].text()
        folder_id = self.input_widgets[3].text()
        grace_period_value = self.input_widgets[4].text()
        target_date_str = self.input_widgets[5].text()
        verbose = self.input_widgets[6].isChecked()

        operation = self.operationCombo.currentText()
        period_type = self.periodTypeCombo.currentText()

        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()

        # Validate folder ID
        if not folder_id:
            logging.error("Folder ID is required")
            self._updateOutput()
            return

        try:
            folder_id_int = int(folder_id)
        except ValueError:
            logging.error("Folder ID must be a valid integer")
            self._updateOutput()
            return

        global_admin = global_admin_login(portal_address, portal_username, portal_password, True)

        if operation == "Get Settings":
            # Get WORM settings
            logging.info("Retrieving WORM settings for folder ID: %s", folder_id_int)
            folder_obj = get_worm_settings(global_admin, folder_id_int)

            if folder_obj:
                display_worm_settings(folder_obj, folder_id_int)
                logging.info("WORM settings retrieved successfully!")
            else:
                logging.error("Failed to retrieve folder settings")

        else:  # Set Grace Period
            # Determine amount and period type
            amount = None
            final_period_type = period_type

            # If target date is provided, use it
            if target_date_str.strip():
                try:
                    target_date = parse_target_date(target_date_str)
                    amount = calculate_days_until_date(target_date)
                    final_period_type = 'Days'
                    logging.info("Target date: %s", target_date.strftime('%d %b %Y'))
                    logging.info("Calculated days from today: %s", amount)
                except ValueError as e:
                    logging.error("Date parsing error: %s", str(e))
                    self._updateOutput()
                    return
            # Otherwise use the grace period value
            elif grace_period_value.strip():
                try:
                    amount = int(grace_period_value)
                except ValueError:
                    logging.error("Grace Period Value must be a valid integer")
                    self._updateOutput()
                    return
            else:
                logging.error("Either Grace Period Value or Target Date must be provided for Set operation")
                self._updateOutput()
                return

            # Set WORM grace period
            success = set_worm_grace_period(global_admin, folder_id_int, amount, final_period_type)

            if success:
                # Retrieve and display updated settings
                logging.info("Retrieving updated WORM settings...")
                folder_obj = get_worm_settings(global_admin, folder_id_int)
                if folder_obj:
                    display_worm_settings(folder_obj, folder_id_int)
            else:
                logging.error("Failed to update WORM grace period")

        global_admin.logout()
        self._updateOutput()

    def _updateOutput(self):
        file = open("output.tmp", 'r')

        with file:
            text = file.read()
            self.output.setText(text)

        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
