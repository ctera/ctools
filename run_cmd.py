import menu
from login import login
from cterasdk import *
import logging

def run_cmd():
    logging.info('Starting run_cmd task')
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

    logging.info('Finished run_cmd task')
    print('Finished task. Returning to menu.')
    menu.menu()

def get_cmd():
    _cmd_str = input("Enter command to run: ")
    print("You enetered: ", _cmd_str)
    return _cmd_str

