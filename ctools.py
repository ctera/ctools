#!/usr/bin/python3
# ctools.py
# CTERA Portal/Edge Filer Maintenance Tool
# Version 1.3

# import local modules
from status import status 
from login import login 

from cterasdk import *
import logging

# Print possible tasks and prompt user to pick a task by entering corresponding number.
def switch():
    print("Tasks to run:\n1. Get Details of all Connected Edge Filers to a specific Portal.")
    option = int(input("Enter a task number to execute: "))
    tasks.get(option,default)()

# Dictionary to map numbers to functions/tasks user can choose to run.
tasks = {
        1 : status,
}
# If an invalid number is entered, call this function and exit.
def default():
    print("ERROR: Invalid option given.")
    logging.warning("Invalid option given. Exiting ctools.exe")

if __name__ == "__main__":
    switch()

