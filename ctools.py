# ctools.py

"""CTools is a GUI toolset to interact with your CTERA Environment"""

import sys, os

from status import run_status

from windows.RunCmdWindow import runCmdWindow
from windows.ShowStatusWindow import showStatusWindow
from windows.SuspendSyncWindow import suspendSyncWindow
from windows.TestFuncWindow import testFuncWindow
from windows.EnableTelnetWindow import enableTelnetWindow
from windows.EnableSSHWindow import enableSSHWindow
from windows.DisableSSHWindow import disableSSHWindow
from windows.UnsuspendSyncWindow import unsuspendSyncWindow
from windows.ResetPasswordWindow import resetPasswordWindow
from windows.CloudFoldersWindow import cloudFoldersWindow
from windows.SMBAuditWindow import smbAuditWindow

from PySide2.QtCore import Qt

from PySide2.QtWidgets import (
    QApplication,
    QStackedWidget
)

def main():
    """PyCalc's main function."""

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    ctoolsApp = QApplication(sys.argv)
    
    
    widget = QStackedWidget()
    
    run_cmd = runCmdWindow(widget)
    widget.addWidget(run_cmd)

    show_status = showStatusWindow(widget) 
    widget.addWidget(show_status)


    suspend_sync = suspendSyncWindow(widget) 
    widget.addWidget(suspend_sync)

    test_func = testFuncWindow(widget) 
    widget.addWidget(test_func)

    enable_telnet = enableTelnetWindow(widget)
    widget.addWidget(enable_telnet)

    enable_ssh = enableSSHWindow(widget)
    widget.addWidget(enable_ssh)
    
    disable_ssh = disableSSHWindow(widget)
    widget.addWidget(disable_ssh)

    unsuspend_sync = unsuspendSyncWindow(widget)
    widget.addWidget(unsuspend_sync)

    reset_password = resetPasswordWindow(widget)
    widget.addWidget(reset_password)

    cloud_folders = cloudFoldersWindow(widget)
    widget.addWidget(cloud_folders)

    smb_audit = smbAuditWindow(widget)
    widget.addWidget(smb_audit)
    ## STEP7- Add new windows above this line ##

    widget.setCurrentWidget(run_cmd)   # setting the page that you want to load when application starts up. you can also use setCurrentIndex(int)

    widget.show()

    ctoolsApp.exec_()

    

if __name__ == "__main__":
    main()