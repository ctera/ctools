# ctools.py

"""CTools is a GUI toolset to interact with your CTERA Environment"""

import sys, logging, os

from status import run_status

from windows.RunCmdWindow import runCmdWindow
from windows.ShowStatusWindow import showStatusWindow

from ui_help import gen_custom_tool_layout

from log_setter import set_logging

from PySide2.QtCore import Qt

from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QTextEdit,
    QFrame,
    QStackedWidget
)

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
OUTPUT_HEIGHT = 250








def main():
    """PyCalc's main function."""
    
    # Store initial contents of log file

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    ctoolsApp = QApplication(sys.argv)
    
    
    widget = QStackedWidget()
    
    run_cmd = runCmdWindow(widget)
    widget.addWidget(run_cmd)   # create an instance of the first page class and add it to stackedwidget

    show_status = showStatusWindow(widget) 
    widget.addWidget(show_status)   # adding second page

    widget.setCurrentWidget(run_cmd)   # setting the page that you want to load when application starts up. you can also use setCurrentIndex(int)

    widget.show()

    ctoolsApp.exec_()

    

if __name__ == "__main__":
    main()