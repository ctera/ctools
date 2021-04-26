from cterasdk import *
from getpass import getpass
import logging, sys
config.http['ssl'] = 'Trust'

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
        global_admin.portals.browse_global_admin()
        return global_admin
    except CTERAException as error:
        logging.warning(error)
        sys.exit("There was a problem logging in. Please try again.")

