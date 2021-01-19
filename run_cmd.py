#!/usr/bin/python3
# runcmd.py
# Module for ctools.py, a CTERA Portal/Edge Filer Maintenance Tool
# Module to execute an arbitrary task on all Filers
# Version 1.0

from login import login
from cterasdk import *

def run_cmd():
    global_admin = login()
    cmd_str = get_cmd()
    filers = global_admin.devices.filers(allPortals=True)
    for filer in filers:
        try:
            print("### Start command on:",filer.name)
            response = filer.cli.run_command(cmd_str)
            print("Response:\n", response)
            print("### End command on:",filer.name)
        except CTERAException as error:
            logging.warning(error)
            print("Something went wrong running the command")

    global_admin.logout()

def get_cmd():
    _cmd_str = input("Enter command to run: ")
    print("You enetered: ", _cmd_str)
    return _cmd_str

