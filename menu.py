from status import run_status
from login import login 
from unlock import unlock
from run_cmd import run_cmd

from cterasdk import *
import logging
import sys

def default():
    """If an invalid number is entered, call this function and exit."""
    logging.info('Invalid task number.')
    print('Invalid task number.')
    quit()

def quit():
    logging.info('Exiting ctools')
    sys.exit('Exiting ctools')

def menu():
    """Prompt which task integer to run"""
    tasks_str = """
    #################
       ctools menu 
         v 1.5.1
    #################

    Available tasks:

    0. Quit
    1. Record status details of all connected Edge Filers.
    2. Enable telnet on one or more connected Edge Filers.
    3. Run a specified command on all connected Edge Filers.
    """
    print(tasks_str)
    try:
        option = int(input('Enter a task number to run: '))
        tasks.get(option,default)()
    except ValueError:
        logging.info('Invalid value.')
        print('Invalid number')
        quit()

# Dictionary to map numbers to functions/tasks user can choose to run.
tasks = {
        0 : quit,
        1 : run_status,
        2 : unlock,
        3 : run_cmd,
}

