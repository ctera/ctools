# ctools.py

"""CTools is a GUI toolset to interact with your CTERA Environment"""

import sys, os

from status import run_status

from windows.RunCmdWindow import runCmdWindow
from windows.ShowStatusWindow import showStatusWindow
from windows.SuspendSyncWindow import suspendSyncWindow
from windows.DeleteSharesWindow import deleteSharesWindow
from windows.EnableTelnetWindow import enableTelnetWindow
from windows.EnableSSHWindow import enableSSHWindow
from windows.DisableSSHWindow import disableSSHWindow
from windows.UnsuspendSyncWindow import unsuspendSyncWindow
from windows.ResetPasswordWindow import resetPasswordWindow
from windows.CloudFoldersWindow import cloudFoldersWindow
from windows.ImportSharesWindow import importSharesWindow
from windows.AddMembersWindow import addMembersWindow
from windows.ReportZonesWindow import reportZonesWindow
from windows.PopulateCloudFoldersWindow import populateCloudFoldersWindow
#from windows.SMBAuditWindow import smbAuditWindow

from PySide6 import QtCore

from PySide6.QtWidgets import (
    QApplication,
    QStackedWidget,
)

from PySide6.QtGui import QIcon

def main():
    """CTools's main function."""

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    ctoolsApp = QApplication(sys.argv)
    
    
    widget = QStackedWidget()

    widget.setWindowTitle("CTools v3.1c")

    widget.setWindowIcon(QIcon('icon.jpeg'))
    
    run_cmd = runCmdWindow(widget)
    widget.addWidget(run_cmd)

    show_status = showStatusWindow(widget) 
    widget.addWidget(show_status)


    suspend_sync = suspendSyncWindow(widget) 
    widget.addWidget(suspend_sync)
    
    unsuspend_sync = unsuspendSyncWindow(widget)
    widget.addWidget(unsuspend_sync)

    enable_ssh = enableSSHWindow(widget)
    widget.addWidget(enable_ssh)
    
    disable_ssh = disableSSHWindow(widget)
    widget.addWidget(disable_ssh)

    enable_telnet = enableTelnetWindow(widget)
    widget.addWidget(enable_telnet)

    reset_password = resetPasswordWindow(widget)
    widget.addWidget(reset_password)

    cloud_folders = cloudFoldersWindow(widget)
    widget.addWidget(cloud_folders)

    delete_shares = deleteSharesWindow(widget) 
    widget.addWidget(delete_shares)

    import_shares = importSharesWindow(widget)
    widget.addWidget(import_shares)
    
    add_members = addMembersWindow(widget)
    widget.addWidget(add_members)

    report_zones = reportZonesWindow(widget)
    widget.addWidget(report_zones)

    populate_shares = populateCloudFoldersWindow(widget)
    widget.addWidget(populate_shares)

    ## STEP7- Add new windows above this line ##

    widget.setCurrentWidget(run_cmd)

    widget.show()

    ctoolsApp.exec()

    

if __name__ == "__main__":
    main()
