from status import run_status
from login import login 
from unlock import unlock, start_ssh
from run_cmd import run_cmd
from suspend_sync import suspend_filer_sync
from unsuspend_sync import unsuspend_filer_sync

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
    2. Run a specified command on all connected Edge Filers.
    3. Enable telnet on an Edge Filer, Virtual, or C-Series Gateway.
    4. Enable SSH on an Edge Filer.
    5. Suspend Cloud Sync on an Edge Filer.
    6. Unsuspend Cloud Sync on an Edge Filer.
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
        2 : run_cmd,
        3 : unlock,
        4 : start_ssh,
        5 : suspend_filer_sync,
        6 : unsuspend_filer_sync,
}

