#!/usr/bin/python3
# ctools.py
# CTERA Portal/Edge Filer Maintenance Tool
# Version 1.3

# import local modules
from status import status 
from login import login 
from unlock import unlock

from cterasdk import *
import logging
import sys

def quit():
    sys.exit("Exiting ctools")

# Print possible tasks and prompt user to pick a task by entering corresponding number.
def switch():
    tasks_str = """Available tasks:
    0. Quit ctools
    1. Record status details of all connected Edge Filers.
    2. Enable telnet on one or more connected Edge Filers.
    """
    print(tasks_str)
    try:
        option = int(input("Enter a task number to run: "))
        tasks.get(option,default)()
    except ValueError:
        print("Not a task number")
        quit()

# Dictionary to map numbers to functions/tasks user can choose to run.
tasks = {
        0 : quit,
        1 : status,
        2 : unlock,
}
# If an invalid number is entered, call this function and exit.
def default():
    print("ERROR: Invalid option given.")
    logging.warning("Invalid option given. Exiting ctools.exe")

if __name__ == "__main__":
    switch()

