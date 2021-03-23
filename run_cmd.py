import menu
from login import login
from cterasdk import *
import logging
from tkinter import messagebox


def run_cmd(mode, portal, username, password, command_run):
    logging.info('Starting run_cmd task')
    # global_admin = login()
    global_admin = login(mode, portal, username, password)
    # cmd_str = get_cmd()
    # passing value
    cmd_str = get_cmd(mode, command_run)
    filers = global_admin.devices.filers(allPortals=True)
    for filer in filers:
        try:
            print("### Start command on:", filer.name)
            response = filer.cli.run_command(cmd_str)
            print("Response:\n", response)
            print("### End command on:", filer.name)
        except CTERAException as error:
            logging.warning(error)
            if mode == 'G':
                messagebox.showerror("Error", "Something went wrong running the command")
            print("Something went wrong running the command")

    logging.info('Finished run_cmd task')
    print('Finished task. Returning to menu.')
    if mode == 'G':
        messagebox.showinfo("success", "Finished task. Returning to menu.")
    # menu.menu()


# def get_cmd():
# adding parameters
def get_cmd(mode, command_run):
    if mode == 'T':
        _cmd_str = input("Enter command to run: ")
    else:
        # assigning values
        _cmd_str = command_run
    print("You enetered: ", _cmd_str)
    return _cmd_str
