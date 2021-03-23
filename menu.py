from status import run_status
from login import login 
from unlock import unlock, start_ssh
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
    2. Run a specified command on all connected Edge Filers.
    3. Enable telnet on an Edge Filer, Virtual, or C-Series Gateway.
    4. Enable SSH on an Edge Filer.
    """
    print(tasks_str)
    try:
        option = int(input('Enter a task number to run: '))
        if option in (1, 2, 3, 4):
            from getpass import getpass
            if option == 1:
                run_status('T', None, None, None, None)
                menu()
            elif option == 2:
                unlock('T', None, None, None, None, None, None)
                menu()
            elif option == 3:
                run_cmd('T', None, None, None, None)
                menu()
            else:
                start_ssh('T', None, None, None, None)
    except ValueError:
        logging.info('Invalid value.')
        print('Invalid number')
        quit()
