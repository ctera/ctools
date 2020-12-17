#!/usr/bin/python3
# login.py
# Module for ctools.py, a CTERA Portal/Edge Filer Maintenance Tool
# Version 1.0
from cterasdk import *
from getpass import getpass
import logging

def login():
    try:
        address = input("Portal (IP, Hostname or FQDN): ")
        username = input("Admin Username: ")
        password = getpass("Admin Password: ")
    except CTERAException as error:
        logging.error(error)
    
    try:
        logging.info("Logging into " + address)
        global_admin = GlobalAdmin(address)
        global_admin.login(username, password)
        logging.info("Successfully logged in to " + address)
        return global_admin
    except CTERAException as error:
        logging.warning(error)

