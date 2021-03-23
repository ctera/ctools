from cterasdk import *
from getpass import getpass
import logging, sys
from tkinter import messagebox

def login(mode,portal,username1,password1):
    try:
        if mode == 'G':
            address = portal
            username = username1
            password = password1
        elif mode == 'T':
            address = input("Portal (IP, Hostname or FQDN): ")
            username = input("Admin Username: ")
            password = getpass("Admin Password: ")
    except CTERAException as error:
        logging.error(error)
        if mode == 'G':
            messagebox.showerror("Error", error)

    try:
        logging.info("Logging into " + address)
        if mode == 'G':
            messagebox.showinfo("Logging into", "Gonna Start logging to " + address)
        global_admin = GlobalAdmin(address)
        global_admin.login(username, password)
        if mode=='G':
            messagebox.showinfo("Success","Successfully logged in to " + address)
        logging.info("Successfully logged in to " + address)
        global_admin.portals.browse_global_admin()
        return global_admin
    except CTERAException as error:
        logging.warning(error)
        if mode == 'G':
            messagebox.showerror("Error", error)
            messagebox.showerror("Error", "There was a problem logging in. Please try again.")
        else:
            sys.exit("There was a problem logging in. Please try again.")
