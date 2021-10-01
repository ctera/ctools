from filer import get_filer
from cterasdk import *
from getpass import getpass
import logging

def reset_filer_password(self,device_name,tenant_name,user_name,filer_password):
    """Set/reset a local user's password on specified Filer"""
    logging.info("Starting reset_password task.")
    filer = self.devices.device(device_name,tenant_name)
    if filer_password == '?':
        filer_password = getpass(prompt='Filer password: ')
    try:
        filer.users.modify(user_name,filer_password)
        logging.info("Success. Password set for " + user_name)
        logging.info("Finished reset_password task.")
    except CTERAException as error:
        logging.error(error)
        logging.info("Error setting password")
